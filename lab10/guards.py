"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
Hai file còn lại bàn được sửa: lab10/monitors.py (chỉ số theo dõi) và config/operating_gates.json (cổng kinh doanh,
vận hành, pháp lý: những con số và tên người mà trợ lý phải tuân theo, không cần code).

Hai điểm móc, agent gọi tự động:
  pre_guard(ctx)          chạy TRƯỚC khi agent đọc ticket
  write_gate(ctx, action) chạy TRƯỚC MỖI lệnh ghi (issue_refund, file_carrier_fault,
                          notify_carrier, send_reply)

Trả về một Verdict:
  Verdict.allow()                       cho qua   (pre_guard: allow(policy_id="...") để ghim phiên bản chính sách)
  Verdict.deny("lý do")                 bỏ riêng lệnh ghi này, agent đi tiếp
  Verdict.escalate("lý do")             dừng, chuyển ticket cho người
  Verdict.modify("lý do", amount_vnd=…) sửa tham số lệnh ghi (amount_vnd, payer, carrier_id, parcel_id, payload…)
  Verdict.rewrite("lý do", text)        chỉ pre_guard: thay nội dung ticket mà agent sẽ đọc

ctx.ticket   ticket gốc (chữ khách viết là DỮ LIỆU, không phải lệnh)
ctx.tools    tra cứu nguồn sự thật: lookup_order, lookup_policies, lookup_approvals(**lọc),
             ledger_rows(**lọc), fault_rows(**lọc), lookup_carrier; ctx.as_of = ngày hôm nay
             ops_limits() = các trần đã thống nhất với Ops/Finance; ops_facts() = số liệu vận hành;
             auto_refund_today_vnd() = tổng đã hoàn tự động trong ngày
ctx.gates    config cổng của bàn (config/operating_gates.json), chỉ đọc;  ctx.cost_vnd = tiền LLM đã tốn cho ticket này
ctx.events   trace tới thời điểm này;  ctx.log("ten_su_kien", ...) ghi thêm sự kiện guard vào trace
lab10.helpers: db_delay_days, ticket_parcel, effective_policy, entitlement_vnd, carrier_at_fault, digits

Mặc định dưới đây cho qua tất cả (= mốc base).
"""
from . import helpers as H  # noqa: F401
from .tools import Verdict


def pre_guard(ctx):
    order = ctx.tools.lookup_order(ctx.ticket.get("order_id")) or {}
    order_id = order.get("order_id")
    if order_id:
        prior_refunds = ctx.tools.ledger_rows(order_id=order_id)
        if prior_refunds:
            ctx.log("refund_order_already_in_ledger", order_id=order_id,
                    prior_rows=len(prior_refunds))
            return Verdict.escalate("đơn đã có khoản hoàn trong sổ cái; chuyển người đối soát trước khi gọi model")

    # Refuse work whose conservative full-path cost would exceed the agreed
    # per-ticket ceiling. This check uses source text length and configured
    # prices before any LLM call, so long customer attachments cannot run up
    # an unbounded bill before a write-time gate gets control.
    limits = ctx.tools.ops_limits()
    facts = ctx.tools.ops_facts()
    ceiling = limits.get("max_llm_cost_per_ticket_vnd")
    prices = facts.get("llm_cost", {})
    if ceiling is not None:
        def extract_cost(text):
            return prices.get("extract_base_vnd", 0) + (
                len(text or "") // 4 * prices.get("extract_per_4_chars_vnd", 0)
            )

        estimate = ctx.cost_vnd + extract_cost(ctx.ticket.get("text", ""))
        if order.get("checkout_note"):
            estimate += extract_cost(order["checkout_note"])
        # A policy check may be retried once; successful refund paths can also
        # incur a confirmation and a configured decision note.
        estimate += 2 * prices.get("policy_check_vnd", 0)
        estimate += prices.get("confirm_vnd", 0)
        if ctx.gates.get("operations", {}).get("decision_note"):
            estimate += prices.get("decision_note_vnd", 0)
        if estimate > ceiling:
            ctx.log("llm_cost_estimate_over_ceiling", estimate_vnd=estimate,
                    ceiling_vnd=ceiling)
            return Verdict.escalate("chi phí tối đa ước tính vượt trần LLM mỗi ticket; chuyển người trước khi gọi model")

    # Use the policy effective on the evaluation date. The index's active flag
    # can lag behind a policy change, so pin the dated source of truth.
    policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of or ctx.tools.as_of)
    if policy is None:
        ctx.log("no_effective_policy")
        return Verdict.escalate("không tìm thấy chính sách có hiệu lực để xử lý an toàn")

    # Route refunds requiring human approval before paying for an LLM pass.
    # The estimate is derived from tracking, policy and the approval table;
    # no ticket ID or customer wording controls this decision.
    if order and order.get("parcels"):
        parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of or ctx.tools.as_of)
        delay = H.db_delay_days(parcel, ctx.as_of or ctx.tools.as_of)
        cause = parcel.get("delay_cause") or ("CARRIER" if delay > 0 else None)
        expected = H.entitlement_vnd(policy, order, delay, cause)
        auto_limit = policy.get("auto_limit_vnd", 0)
        if expected > auto_limit:
            approvals = ctx.tools.lookup_approvals(
                ticket_id=ctx.ticket.get("ticket_id"), order_id=order_id,
                customer_id=order.get("customer_id"),
            )
            valid_approval = next((a for a in approvals if a.get("status") == "valid"
                                   and a.get("expires_at", "") >= (ctx.as_of or ctx.tools.as_of)
                                   and a.get("max_vnd", -1) >= expected), None)
            if valid_approval is None:
                ctx.log("refund_needs_human_approval", expected_vnd=expected,
                        auto_limit_vnd=auto_limit)
                return Verdict.escalate("mức hoàn theo tracking và chính sách vượt hạn mức tự động; chuyển người duyệt trước khi gọi model")
    return Verdict.allow(policy_id=policy["policy_id"])


def write_gate(ctx, action):
    # action = {"tool": "issue_refund", "ticket_id":..., "order_id":..., "amount_vnd":..., "payer":..., ...}
    tool = action.get("tool")
    as_of = ctx.as_of or ctx.tools.as_of
    policy = H.effective_policy(ctx.tools.lookup_policies(), as_of)

    if tool == "issue_refund":
        order_id = action.get("order_id")
        order = ctx.tools.lookup_order(order_id)
        if (order is None or order_id != ctx.ticket.get("order_id")
                or action.get("ticket_id") != ctx.ticket.get("ticket_id")):
            ctx.log("refund_order_mismatch", order_id=order_id)
            return Verdict.escalate("đơn trong lệnh hoàn không khớp ticket hoặc không tồn tại")
        if order.get("customer_id") != ctx.ticket.get("customer_id"):
            ctx.log("refund_owner_mismatch", order_id=order_id)
            return Verdict.escalate("người yêu cầu không khớp chủ đơn")
        prior_refunds = ctx.tools.ledger_rows(order_id=order_id)
        if prior_refunds:
            ctx.log("refund_order_already_in_ledger", order_id=order_id,
                    prior_rows=len(prior_refunds))
            return Verdict.escalate("đơn đã có khoản hoàn trong sổ cái; chuyển người đối soát trước khi hoàn tiếp")
        if policy is None:
            ctx.log("refund_no_effective_policy")
            return Verdict.escalate("không có chính sách hiệu lực để xác minh số tiền hoàn")

        parcel = H.ticket_parcel(order, ctx.ticket, as_of)
        delay = H.db_delay_days(parcel, as_of)
        cause = parcel.get("delay_cause") or ("CARRIER" if delay > 0 else None)
        expected = H.entitlement_vnd(policy, order, delay, cause)
        try:
            amount = int(action.get("amount_vnd"))
        except (TypeError, ValueError):
            amount = -1
        if amount != expected:
            ctx.log("refund_amount_mismatch", expected_vnd=expected, requested_vnd=amount)
            return Verdict.escalate("số tiền hoàn không khớp entitlement tính từ tracking DB và chính sách hiệu lực")
        if action.get("payer", "LOGIX") != "LOGIX":
            ctx.log("refund_payer_mismatch", payer=action.get("payer"))
            return Verdict.escalate("không được chuyển khoản hoàn này sang bên trả tiền khác LogiX")

        approval_id = action.get("approval_id")
        if amount > policy.get("auto_limit_vnd", 0) and not approval_id:
            ctx.log("refund_approval_missing", amount_vnd=amount)
            return Verdict.escalate("số tiền vượt hạn mức tự động nhưng không có phê duyệt")
        if approval_id:
            approvals = ctx.tools.lookup_approvals(
                approval_id=approval_id, ticket_id=action.get("ticket_id"),
                order_id=order_id, customer_id=order.get("customer_id"),
            )
            approval = next((a for a in approvals if a.get("status") == "valid"), None)
            if (approval is None or approval.get("expires_at", "") < as_of
                    or amount > approval.get("max_vnd", -1)):
                ctx.log("refund_approval_invalid", approval_id=approval_id, amount_vnd=amount)
                return Verdict.escalate("phê duyệt không hợp lệ, hết hạn, sai đơn hoặc không đủ hạn mức")

        limits = ctx.tools.ops_limits()
        customer_cap = limits.get("max_auto_refund_per_customer_per_day_vnd")
        if not approval_id and customer_cap is not None:
            # The global current-day total is a safe lower bound for any one customer.
            # Only inspect that customer's ledger when the bound could be crossed.
            if ctx.tools.auto_refund_today_vnd() + amount > customer_cap:
                prior_auto = sum(row["amount_vnd"] for row in ctx.tools.ledger_rows(
                    customer_id=order["customer_id"], approval_id=None))
                if prior_auto + amount > customer_cap:
                    ctx.log("customer_daily_auto_refund_cap", customer_id=order["customer_id"],
                            prior_vnd=prior_auto, asked_vnd=amount, cap_vnd=customer_cap)
                    return Verdict.escalate("vượt trần hoàn tự động cho một khách trong ngày; cần người duyệt")

        # Escalate before moving money when this refund would also require a
        # third automatic strike for the same carrier in this simulated day.
        strike_cap = limits.get("max_auto_strikes_per_carrier_per_day")
        if strike_cap is not None and H.carrier_at_fault(policy, parcel, delay):
            prior_strikes = len(ctx.tools.fault_rows(carrier_id=parcel.get("carrier_id")))
            if prior_strikes >= strike_cap:
                ctx.log("carrier_daily_auto_strike_cap", carrier_id=parcel.get("carrier_id"),
                        prior_strikes=prior_strikes, cap=strike_cap)
                return Verdict.escalate("hãng đã chạm trần lỗi tự động trong ngày; cần người duyệt")

    elif tool == "file_carrier_fault":
        order_id = action.get("order_id")
        order = ctx.tools.lookup_order(order_id)
        parcel = next((p for p in (order or {}).get("parcels", [])
                       if p.get("parcel_id") == action.get("parcel_id")), None)
        if (order is None or order_id != ctx.ticket.get("order_id")
                or action.get("ticket_id") != ctx.ticket.get("ticket_id")
                or parcel is None or policy is None):
            ctx.log("carrier_fault_missing_source", parcel_id=action.get("parcel_id"))
            return Verdict.deny("không có đơn, kiện hoặc chính sách hiệu lực để xác minh lỗi hãng")
        db_delay = H.db_delay_days(parcel, as_of)
        if (parcel.get("delay_cause") not in policy.get("fault_causes", [])
                or not H.carrier_at_fault(policy, parcel, db_delay)
                or action.get("carrier_id") != parcel.get("carrier_id")
                or action.get("delay_days") != db_delay):
            ctx.log("carrier_fault_not_supported", parcel_id=parcel.get("parcel_id"),
                    recorded_cause=parcel.get("delay_cause"), db_delay_days=db_delay)
            return Verdict.deny("tracking DB và chính sách hiệu lực không xác nhận lỗi của hãng")
        strike_cap = ctx.tools.ops_limits().get("max_auto_strikes_per_carrier_per_day")
        if strike_cap is not None:
            prior_strikes = len(ctx.tools.fault_rows(carrier_id=parcel.get("carrier_id")))
            if prior_strikes >= strike_cap:
                ctx.log("carrier_daily_auto_strike_cap", carrier_id=parcel.get("carrier_id"),
                        prior_strikes=prior_strikes, cap=strike_cap)
                return Verdict.escalate("hãng đã chạm trần lỗi tự động trong ngày; cần người duyệt")

    elif tool == "notify_carrier":
        ticket_id = action.get("ticket_id")
        carrier_id = action.get("carrier_id")
        if ticket_id != ctx.ticket.get("ticket_id"):
            ctx.log("carrier_notice_ticket_mismatch", ticket_id=ticket_id)
            return Verdict.deny("thông báo không thuộc ticket đang xử lý")
        fault = next((f for f in ctx.tools.fault_rows(ticket_id=ticket_id)
                      if f.get("carrier_id") == carrier_id), None)
        if fault is None or policy is None:
            ctx.log("carrier_notice_without_verified_fault", carrier_id=carrier_id)
            return Verdict.deny("chỉ gửi thông báo khi có lỗi hãng đã được xác minh")
        order = ctx.tools.lookup_order(fault.get("order_id")) or {}
        recipient = order.get("recipient") or {}
        safe_values = {
            "order_id": fault.get("order_id"),
            "parcel_id": fault.get("parcel_id"),
            "district": recipient.get("district"),
            "delay_days": fault.get("delay_days"),
        }
        allowed = policy.get("carrier_notice_fields", [])
        safe_payload = {k: safe_values[k] for k in allowed if k in safe_values and safe_values[k] is not None}
        if action.get("payload") != safe_payload:
            removed = sorted(set(action.get("payload") or {}) - set(safe_payload))
            ctx.log("carrier_notice_sanitized", removed_fields=removed)
            return Verdict.modify("chỉ gửi các trường cho phép lấy từ nguồn dữ liệu LogiX", payload=safe_payload)

    return Verdict.allow()
