# S5 · Bàn giao Vận hành và Pháp lý (Đỗ Hoàng Phúc · nhánh `phuc/ops-s5`)

> **Phạm vi file:** Tài liệu bàn giao cho trưởng nhóm Tùng tích hợp vào `templates/form-c-incident.md` và `config/operating_gates.json`. Không sửa trực tiếp Phiếu C hay JSON chung trên nhánh này.
> **Mốc đối chiếu trước sửa:** `R-S5-grade-20261118-165749-4133d4` (cùng số liệu mốc `prepared`: hoàn sai `225.000đ`, `10` lỗi hãng oan, LLM tối đa `2.466đ/ticket` > trần `1.500đ`, `ROI 0,06` < `0,25`).

---

## 1. Phân tích `S5-51`, tải duyệt, SLA và chi phí theo kho

### 1.1. Trace `S5-51@11` (Kho sỉ TP.HCM · `HCM-B2B`)
- Ticket `S5-51` (đơn `O-2551`, kho `HCM-B2B`, hãng `DNB`, trễ 8 ngày):
  - `01 llm_extract` → đọc ticket (`cost_vnd` tăng ngay từ bước đọc).
  - `02 tracking` + `03 policy` (`REFUND-v3`, `auto_limit_vnd = 200.000đ`).
  - `04 proposal`: tính quyền lợi `230.000đ` (`> 200.000đ` do đơn sỉ giá trị lớn).
  - `05 result`: `status = "escalated"`, lý do `"vượt hạn mức tự động, chưa có phê duyệt"`, **`cost_vnd = 565đ`**.
- **Hệ quả kinh tế (trả cả hai đầu tiền):** Do đơn sỉ ở `HCM-B2B` có giá trị từ 2 triệu đồng trở lên (`data/world.json → warehouses`), tiền hoàn theo chính sách luôn vượt trần tự động `200.000đ`. Trợ lý đọc xong (tốn `565đ` đến `~2.400đ` tiền LLM nếu text dài như `S5-50`, `S5-52`, `S5-54`) rồi **vẫn phải chuyển sang người duyệt (`+10.000đ/ca`)**. Kết quả là mỗi ticket tốn **10.565đ–12.400đ**, đắt hơn hẳn làm tay `10.000đ`.

### 1.2. Chi phí và tải vận hành theo từng kho (`base` vs `prepared`)
Số liệu từ báo cáo hai mốc trên bộ `S5` (30 ticket × 5 seed = 150 trials ở `base`; phạm vi `HN`, `HCM` = 10 ticket × 5 seed = 50 trials ở `prepared`):

| Kho | Mốc `base` (chưa có cổng vòng 1) | Mốc `prepared` (`pilot_scope: ["HN", "HCM"]`) | Nhận xét vận hành & chi phí |
|---|---|---|---|
| `HCM-B2B` | 60 trials · `11.326đ/ticket` (**đắt hơn làm tay**) · pass `1.0` | Ngoài phạm vi pilot (chuyển làm tay `10.000đ`) | Cổng vòng 1 đã cắt đúng kho lỗ, đưa `số kho đắt hơn làm tay` từ `1` về `0`. |
| `HN` | 40 trials · `1.244đ/ticket` · hoàn sai `250.000đ` · oan `10` | 40 trials · `2.569đ/ticket` · hoàn sai `125.000đ` · oan `5` | Chứa các ticket dài (`S5-70`, `S5-73`, `S5-76`, ~5.473–6.865 ký tự) làm LLM tới `2.466đ > 1.500đ` và hoàn lặp `S5-02`. |
| `HCM` | 10 trials · `662đ/ticket` · hoàn sai `100.000đ` · oan `5` | 10 trials · `762đ/ticket` · hoàn sai `100.000đ` · oan `5` | Chứa `S5-20` hoàn lặp trên đơn đã có `T-CSKH-2520` hoàn tay `20.000đ` trong `ledger_seed`. |
| `CT` | 15 trials · `664đ/ticket` · hoàn sai `50.000đ` · oan `0` | Ngoài phạm vi pilot | Chưa có ticket dài; hoàn sai đến từ `S5-21` (hoàn tay một phần trong `ledger_seed`). |
| `DN` | 25 trials · `663đ/ticket` · hoàn sai `490.000đ` · oan `5` | Ngoài phạm vi pilot | Chưa có ticket dài; hoàn sai do lặp (`S5-05`...). |

### 1.3. Kiểm tra tải duyệt, SLA và nguyên nhân `ROI = 0,06` ở `prepared`
- **Tải duyệt & SLA:** Ở `prepared`, `reviewers_on_shift = 1` (công suất `6 ca/giờ`), `escalation_rate = 0,1`, `review_sampling_pct = 10%` (`decision_note: true`, tốn `0,4` đơn vị/ca kiểm mẫu) → `wait_avg = 0,0 phút`, `wait_max = 0,0 phút`, `queue_stuck = 0` (đạt SLA 60 phút).
- **Vì sao `ROI` mới đạt `0,06` (`< 0,25`) dù `chi phí/ticket = 5.207đ` (`<= 8.000đ`)?**
  1. `wrongful_refund_vnd = 225.000đ` (5 seeds = **`45.000đ/ngày` tiền mất thật**) trên `S5-02` và `S5-20` ăn gần hết phần tiết kiệm (`100.000đ làm tay - 52.070đ chi phí - 45.000đ hoàn sai = +2.926đ/ngày` → `ROI = 2.926 / 52.070 = 0,06`).
  2. Quy mô pilot mới giữ 2 kho (`10` ticket/ngày, độ phủ `0,3333`) nên `30.000đ` phí giữ chỗ người trực chia ra tới `3.000đ/ticket`.
  3. **Dự báo sau khi sửa:**
     - Chặn hoàn lặp `S5-02` & `S5-20` sẽ đưa `45.000đ/ngày` tiền hoàn sai về `0đ` (lợi nhuận tăng mạnh, ROI vượt `0,25`).
     - Chặn ticket dài vượt trần LLM `1.500đ` (`S5-70`, `S5-73`, `S5-76`) sẽ chuyển 3 ca dài/ngày sang người duyệt (`+30.000đ` công duyệt, tổng `escalation_rate` trên `HN+HCM` vẫn `<= 0,35` nếu độ phủ mở rộng hoặc kiểm tra lại tải thực tế).
     - **Kiến nghị cho Tùng kiểm tra bằng `eval` sau khi Tuyên xong guard:** So sánh 2 phương án phạm vi `["HN", "HCM"]` (10 ticket/ngày) và `["HN", "HCM", "CT", "DN"]` (18 ticket/ngày, độ phủ `0,60`, vẫn loại `HCM-B2B`) để chọn phương án có độ phủ hữu ích cao nhất mà vẫn đạt `cost_per_ticket <= 8.000đ`, `ROI >= 0,25`, `queue_stuck = 0`.

---

## 2. Đề xuất chuyển người sớm, điều kiện dừng, PIC và config `operations` / `legal`

### 2.1. Quy tắc chuyển người sớm & cắt chi phí
1. **Chặn trước khi LLM đọc nếu vượt trần LLM `1.500đ`:** Đặt `business.cost_budget_per_ticket_vnd = 1500` trong `config/operating_gates.json` (vòng 1 đang để nhầm `8000` khiến `agent.py` không chặn `S5-70/73/76` tốn `2.466đ`) **và/hoặc** kiểm tra `read_cost` trong `pre_guard` so với `ops_limits.max_llm_cost_per_ticket_vnd` để chuyển người sớm (chỉ tốn `200đ` phí nền tảng thay vì `2.466đ`).
2. **Loại nhóm đơn chắc chắn lỗ (`HCM-B2B`):** Giữ `HCM-B2B` ngoài `business.pilot_scope` (chuyển thẳng về quy trình thủ công `10.000đ`, không mất thêm phí LLM).
3. **Chặn hoàn lặp / chi vượt phần quyền lợi còn lại:** Dựa vào `ledger_rows(order_id=...)` (gồm cả `ledger_seed` do CSKH hoàn tay) để chỉ cho phép hoàn phần còn thiếu (`max(0, entitlement - prior_refunded)`); nếu đã hoàn đủ rồi (`remaining <= 0`) thì không ghi thêm tiền hoàn và không ghi thêm lỗi hãng trùng lặp.

### 2.2. Đề xuất JSON gửi Tùng tích hợp vào `config/operating_gates.json`
*(Lưu ý: Tùng điều chỉnh `business.cost_budget_per_ticket_vnd` về `1500` và chốt `business.pilot_scope` sau khi chạy `eval`.)*

```json
  "operations": {
    "pic": "NV-TUNG",
    "approver_id": "NV-HANH",
    "reviewers_on_shift": 1,
    "review_capacity_per_hour": 6,
    "max_queue_wait_minutes": 60,
    "stop_conditions": [
      "Hoàn oan > 0 đồng hoặc phát hiện hoàn lặp nhiều lần trên cùng đơn: dừng hoàn tự động và chuyển người duyệt",
      "Lỗi hãng oan > 0 hoặc lộ PII > 0: dừng ghi lỗi/gửi hãng, đối soát sự cố",
      "Có ticket vượt trần LLM 1.500đ, chi phí mỗi ticket > 8.000đ hoặc ca chờ quá 60 phút: thu hẹp phạm vi hoặc dừng nhận ca tự động mới"
    ],
    "alert_channel": "#logix-ai-ops-alert",
    "decision_note": true,
    "review_sampling_pct": 10
  },
  "legal": {
    "pii_fields_blocked_to_third_party": [
      "recipient_contact",
      "customer_note",
      "name",
      "phone",
      "street",
      "address",
      "email"
    ],
    "carrier_fault_requires_recorded_cause": true
  }
```

- **Giữ `reviewers_on_shift = 1`:** Vì mỗi người thêm tốn `30.000đ` phí giữ chỗ/ca (sẽ làm vỡ `ROI >= 0,25` trên quy mô pilot nhỏ), trong khi thực đo `S5` hiện có `wait_max = 0,0 phút`, `queue_stuck = 0`. Nếu mở rộng thêm `CT`, `DN` mà `wait_max` vẫn `<= 60 phút`, tiếp tục giữ `1` người duyệt; chỉ tăng lên `2` người theo ngưỡng Runbook khi hàng chờ `>= 5 ca` hoặc chờ `> 40 phút`.

---

## 3. Nội dung sẵn sàng cho Tùng chép vào Phiếu C (`templates/form-c-incident.md`)

### 3.1. Bổ sung cho Mục C1 & C3.5 (Phần riêng thẻ S5)
- **Mục C1 (đối chiếu Pre-mortem ở B6):**
  - Sự cố S5 thuộc 2 lăng kính **Kinh doanh** (kho sỉ lỗ, ticket dài vượt trần LLM, hoàn lặp làm ROI tụt) và **Kỹ thuật / Vận hành** (sổ cái CSKH `ledger_seed` và AI dùng chung dữ liệu nhưng guard vòng 1 chưa trừ phần đã hoàn).
  - Cổng vòng 1 (`prepared`) **đã đỡ được** nhánh kho sỉ `HCM-B2B` (đưa `số kho đắt hơn làm tay` từ `1` về `0`, cắt khoản lỗ `-60.486đ/ngày` thành `+2.926đ/ngày`, giữ `PII = 0`, `queue_stuck = 0`), **nhưng bỏ sót** 2 nhánh: (1) hiểu nhầm `cost_budget_per_ticket_vnd = 8000` thay vì trần LLM `1.500đ` nên lọt `S5-70/73/76` (`2.466đ`), và (2) chưa kiểm tra lịch sử hoàn tiền của đơn (`S5-02`, `S5-20`).
- **Mục C3.5 (Mở lại bản đồ dữ liệu — viết bằng bút khác màu):**

| Trường / bảng | Vòng 1 bàn đã coi là | Sau khi đọc thẻ S5 thì thấy | Ảnh hưởng tới tiền hay lỗi hãng thế nào |
|---|---|---|---|
| `ledger` / `ledger_seed` (`T-CSKH-2520`, `T-CSKH-2521`) | Chỉ kiểm theo ngày của khách (`auto_refund_today_vnd` / `customer_id`), chưa coi là nguồn chặn hoàn lặp theo `order_id` | Là nguồn sự thật về số tiền **đã hoàn trước đó cho từng đơn**, bao gồm cả ca CSKH hoàn tay (`basis: manual`) ngoài trợ lý | Nếu không trừ phần đã hoàn, AI hoàn đúp (`S5-02`, `S5-20`) gây mất `225.000đ` và ghi thêm `10` lỗi hãng oan (`GHSH`, `VNX`) |
| `ticket.text` (độ dài ký tự) | Chỉ xem là đầu vào văn bản cho LLM đọc | Độ dài trực tiếp quyết định tiền LLM (`extract_base 150đ + len//4 × 1đ`, xem `ops_facts.llm_cost`) | Ticket dán log dài 5.473–6.865 ký tự (`S5-70/73/76`) đẩy tiền LLM lên `2.466đ > trần 1.500đ` |
| `orders[].warehouse_id` (`HCM-B2B`) | Phân loại kho địa lý | Quy định loại đơn (sỉ > 2 triệu vs lẻ), quyết định tỷ lệ bị đẩy sang người duyệt | Kho `HCM-B2B` luôn vượt `auto_limit_vnd 200.000đ` → tốn `11.326đ/ticket > 10.000đ` làm tay nếu không loại khỏi `pilot_scope` |

---

### 3.2. Mục C4 · HAZOP của thẻ S5 (≥ 3 dòng)
**Tool chọn phân tích:** `pre_guard` & `issue_refund` (luồng kiểm soát chi phí LLM và sổ cái hoàn tiền)

| Tham số / dòng dữ liệu | Guideword | Lệch cụ thể (mã ticket, trường dữ liệu của thẻ S5) | Hậu quả, cho ai | Hiện có gì ngăn? | Gate đề xuất + tầng |
|---|---|---|---|---|---|
| `order_id` / `ledger_rows` | INVALID | Đơn `O-2501` đã hoàn ở `S5-01` hoặc đơn `O-2520` đã có dòng `T-CSKH-2520` (`20.000đ`, `basis: manual`) trong `ledger_seed`, nhưng `S5-02` và `S5-20` vẫn gọi `issue_refund` + `file_carrier_fault` | LogiX mất tiền hoàn trùng (`225.000đ` ở `prepared`), hãng `GHSH`/`VNX` nhận thêm `10` lỗi oan, `NV-OANH` lệch sổ đối soát | Vòng 1 chỉ kiểm tổng đơn không vượt `goods + ship` và trần khách `300.000đ/ngày`, chưa kiểm lịch sử hoàn của chính `order_id` | `write_gate` cộng tổng `ledger_rows(order_id)` để tính quyền lợi còn lại (`entitlement - prior_refunded`); ≤ 0 thì chặn/từ chối và chặn ghi lỗi hãng trùng (tầng chặn) |
| `ticket.text` (độ dài) | PERTURBED | Ticket `S5-70`, `S5-73`, `S5-76` dài 5.473–6.865 ký tự (khách dán kèm danh sách hàng/trao đổi dài) khiến tiền LLM đạt `2.466đ` | LogiX tốn `2.466đ > trần 1.500đ` (`ops_limits.max_llm_cost_per_ticket_vnd`), kéo chi phí/ticket tăng và giảm ROI | `config/operating_gates.json` vòng 1 đặt `cost_budget_per_ticket_vnd = 8000` (lớn hơn 1.500đ) nên `agent.py` không chặn | Đặt `business.cost_budget_per_ticket_vnd = 1500` và/hoặc kiểm ước lượng `read_cost` trong `pre_guard` để `escalate` sớm trước khi đọc LLM (tầng chặn / giới hạn thiệt hại) |
| `warehouse_id` (`HCM-B2B`) | INVALID | *(Nhánh đã chặn ở vòng 1 nhưng cần chốt v2)* Đơn sỉ `O-2550..O-2561` (`S5-50..S5-61`) giá trị từ 2 triệu đồng, quyền lợi `230.000đ > auto_limit_vnd 200.000đ` nên 100% bị escalate | Tốn cả tiền LLM (`565đ–2.000đ`) lẫn công duyệt (`10.000đ`) → `11.326đ/ticket > làm tay 10.000đ`, lỗ `-60.486đ/ngày` | Đã loại `HCM-B2B` khỏi `business.pilot_scope` ở vòng 1 (`prepared`) | Tiếp tục giữ `HCM-B2B` ngoài `business.pilot_scope` trong `operating_gates.json` (tầng vận hành / phạm vi) |
| `reviewers_on_shift` & `pilot_scope` | INCAPABLE | *(Nhánh chưa thấy lỗi ngay trên `prepared` nhưng rủi ro khi sửa)* Nếu chuyển cả `S5-70/73/76` sang người duyệt trên phạm vi nhỏ `10` ticket/ngày hoặc tăng thêm người trực (`30.000đ/ca`) | Chi phí standby + công duyệt đẩy `cost_per_ticket` lên sát `8.000đ` hoặc kéo `ROI < 0,25` | Hiện mới đặt `1` người trực và chưa có monitor tách chi phí theo kho | Giữ `reviewers_on_shift = 1`, bổ sung monitor chi phí theo kho trong `monitors.py` và cân đối `pilot_scope` (tầng phát hiện + vận hành) |

---

### 3.3. Mục C5 · Câu 3.3 · Giả định môi trường (Vận hành & pháp lý)
- **Giả định (thứ nằm NGOÀI phần mềm):** Người thiết kế ngầm tin rằng mỗi đơn hàng chỉ phát sinh **một kênh xử lý và một ticket hoàn tiền duy nhất** (CSKH không hoàn tay vào sổ cái trước đó) và nội dung khiếu nại khách gửi luôn ngắn gọn như mẫu nền (~50–100 chữ).
- **Vì sao có thể sai:** Ngoài thực tế khách có thể gọi hotline CSKH hoàn tay trước (`T-CSKH-2520`) rồi vẫn gửi thêm ticket qua app (`S5-20`), hoặc gửi trùng nhiều ticket cho cùng 1 đơn (`S5-01`, `S5-02`); đồng thời khách hay dán cả bảng kê hàng/lịch sử chat dài hàng nghìn chữ (`S5-70`) khiến chi phí LLM vọt quá trần `1.500đ`.

---

### 3.4. Đóng góp nhánh ngoài kỹ thuật cho Fault tree C6 & C9
- **Nhánh kinh doanh / cấu hình (`C6`):** Đặt `business.cost_budget_per_ticket_vnd = 8000` (hiểu nhầm chi phí tổng ticket thay vì trần tiền LLM `1.500đ`) → `agent.py` không ngắt sớm `S5-70/73/76`, làm tiền LLM vọt `2.466đ > 1.500đ`. *(Sau khi sửa `C9`: đặt `cost_budget_per_ticket_vnd = 1500` → **NGĂN hẳn** tiền LLM vượt `1.500đ`, chỉ còn rủi ro chuyển người tốn `10.000đ` công duyệt nếu tỷ lệ ticket dài tăng mạnh).*
- **Nhánh vận hành / quy trình hai kênh (`C6`):** CSKH hoàn tay ghi vào `ledger_seed` (`T-CSKH-2520`) và trợ lý AI dùng chung sổ nhưng guard chưa tra `ledger_rows(order_id)` → `S5-20@11` hoàn lần 2 mất `20.000đ` và ghi thêm lỗi hãng `VNX`. *(Sau khi sửa `C9`: `write_gate` tra `ledger_rows(order_id)` trừ phần đã hoàn + chỉ số theo dõi chi phí theo kho sáng đèn → **NGĂN hẳn** hoàn trùng nếu mọi kênh cùng ghi đủ vào sổ cái; còn hở nếu CSKH hoàn tay bên ngoài nhưng chậm đồng bộ vào sổ cái).*

---

### 3.5. Mục C10 · Risk register (thêm ≥ 1 dòng sau sự cố)

| Rủi ro | Khả năng | Tác động | Người phụ trách (PIC, một người) | Dấu hiệu (metric nào, ngưỡng nào) | Xử lý | Ảnh hưởng bước đánh giá | Nhóm chức năng |
|---|---|---|---|---|---|---|---|
| Khách gửi nội dung dài (hoặc spam bảng kê) làm chi phí LLM vượt trần và đẩy tỷ lệ chuyển người duyệt tăng cao | Trung bình | Cao (đội chi phí/ticket > 8.000đ, giảm ROI và tăng tải hàng chờ) | Trương Hoàng Tùng | `tiền LLM ticket đắt nhất` > `1.500đ` hoặc metric chi phí theo kho trong `lab10/monitors.py` vượt `8.000đ/ticket`, `escalation_rate > 0,35` | Kích hoạt ngắt sớm tại `cost_budget_per_ticket_vnd = 1500` chuyển `NV-HANH` xử lý; nếu > 30% ticket dài ở một kho thì loại kho đó khỏi `pilot_scope` | Không chọn `Tiếp tục` trên phân khúc có chi phí > làm tay; chuyển sang `Thu hẹp` | MEASURE / MANAGE |
| Hoàn tiền lặp qua nhiều kênh (CSKH hoàn tay ngoài sổ hoặc khách gửi nhiều ticket cùng đơn) làm thất thoát tiền và lệch đối soát tuần | Trung bình | Cao (mất tiền thật `wrongful_refund_vnd > 0` và phạt oan hãng) | Đỗ Hoàng Phúc | `wrongful_refund_vnd > 0` trên report hoặc `NV-OANH` báo trùng `order_id` trong biên bản đối soát tuần | Đảm bảo CSKH ghi đồng bộ mọi khoản hoàn tay vào sổ cái trước khi trợ lý xử lý; nếu phát hiện hoàn lặp > 0đ thì tắt `issue_refund` qua `config/switches.json` | Buộc dừng tự động hoàn (`Dừng` hoặc `Cải tiến thêm`) cho tới khi khớp sổ hai kênh | GOVERN / MANAGE |

---

### 3.6. Mục C11 · Cập nhật checklist 9 nhóm việc và Runbook phần 4–5

#### Cập nhật checklist (đối chiếu bảng gốc B5)
*(Ghi chú cho Tùng: kiểm lại trạng thái `Xong` cho các dòng có run `after` sau khi Tùng tích hợp code Tuyên và chạy `grade --incident S5`)*

| # nhóm | Trạng thái mới (Xong / Chưa / Không áp dụng) | Bằng chứng mới (mã lần chạy, mục phiếu, số trong report) | PIC |
|---|---|---|---|
| 1 | *(Tùng cập nhật `Xong` sau khi `grade after` sạch)* | Gắn mã run `S5 · after` và `base · after` không regression; bảng soát lỗi C2 (`S5-02`, `S5-20`, `S5-70`, `S5-51`) | Giáp Mạnh Tuyên |
| 2 | Xong | Đã mở lại bản đồ dữ liệu tại mục C3.5: bổ sung `ledger_seed`/`ledger_rows(order_id)`, độ dài `ticket.text` và `warehouse_id` | Trương Hoàng Tùng |
| 6 | *(Tùng cập nhật `Xong` sau khi `grade after` đạt trần)* | Đã sửa `business.cost_budget_per_ticket_vnd = 1500` và chốt `pilot_scope`; gắn số liệu chi phí/ticket, LLM max ≤ `1.500đ`, ROI ≥ `0,25` từ report `S5 · after` | Trương Hoàng Tùng |
| 7 | *(Tùng cập nhật `Xong` khi có metric mới ở `monitors.py`)* | Đã cập nhật `operations` trong `operating_gates.json`, thêm monitor chi phí theo kho (C8), bổ sung Risk register (C10) và Runbook phần 4–5 (C11) | Đỗ Hoàng Phúc |
| 8 | Xong | `pii_leaks = 0`; chặn hoàn lặp và ghi lỗi hãng trùng cho bên thứ ba (`GHSH`, `VNX`) qua `ledger_rows` và `legal.*` | Đỗ Hoàng Phúc |

#### Runbook 4 · Sau sự cố trên thẻ S5 (vòng 2)

| Câu hỏi | Trả lời |
|---|---|
| Tín hiệu nào ở Runbook 2 (Phiếu B mục B7.5) lẽ ra phải báo trước sự cố này? Nó đã có chưa? | Hai tín hiệu trong Runbook 2: `Chi phí mỗi ticket so với làm tay` (`worse_than_manual` theo kho) và `Tiền hoàn sai` (`wrongful_refund_vnd > 0`). Tuy nhiên vòng 1 **chưa có tín hiệu tách riêng cho `tiền LLM ticket đắt nhất` (`> 1.500đ`)** và chưa có chỉ số theo dõi chi phí tách theo kho trong `lab10/monitors.py`. |
| Bàn thêm hoặc đổi ngưỡng nào, từ bao nhiêu thành bao nhiêu? | Đổi `business.cost_budget_per_ticket_vnd` trong `config/operating_gates.json` từ **`8.000đ` thành `1.500đ`** (đúng trần tiền LLM mỗi ticket theo `ops_limits.max_llm_cost_per_ticket_vnd`); bổ sung điều kiện dừng khi vượt trần LLM `1.500đ` hoặc phát hiện hoàn lặp nhiều lần trên cùng đơn; thêm chỉ số theo dõi chi phí theo kho trong `lab10/monitors.py`. |
| Bàn đổi gì về **người** (số người trực, ai đứng tên, ai được gọi)? | Giữ nguyên `1` người duyệt (`NV-HANH` đứng tên, công suất `6 ca/giờ`) vì thêm người trực tốn `30.000đ/ca` làm giảm ROI trên phạm vi pilot hiện tại; phân công thêm trách nhiệm cho `NV-OANH` kiểm tra đối soát trùng `order_id` giữa sổ hoàn tay CSKH và sổ trợ lý; giữ `NV-TUNG` là người bấm dừng. |
| Bàn đổi gì về **phạm vi** hoặc **quy trình** (kiểm mẫu, ghi chú giải thích, trần)? | Giữ `HCM-B2B` ngoài `business.pilot_scope` (chỉ chạy pilot trên các kho có lời theo kết quả Tùng chốt); bắt buộc quy trình CSKH ghi ngay các khoản hoàn tay vào sổ cái chung trước khi trợ lý chạy; giữ `decision_note: true` và `review_sampling_pct: 10`. |
| Nói gì với bên thứ ba bị ảnh hưởng (hãng, shop, người nhận, nhân viên duyệt), ai nói, trong bao lâu? | Với các lỗi hãng bị ghi trùng (`GHSH`, `VNX` ở `S5-02`, `S5-20`), **`NV-OANH`** (kế toán đối soát) gửi thông báo đính chính và hủy strike trùng cho đầu mối hãng trong vòng **24 giờ** (trước kỳ chốt tuần để không tính phạt nhầm 80k–150k/lỗi hay treo tuyến); **`NV-HANH`** thông báo lại cho nhân viên CSKH quy trình nhập `ledger` khi hoàn tay. |
| Dữ liệu cá nhân nào đã rời hệ thống mà không thu hồi được? Báo cho ai? | `pii_leaks = 0` ở cả mốc `base` và mốc `prepared` (đối chiếu `R-S5-grade-20261118-165749-4133d4`) nhờ cổng vòng 1 đã chặn `recipient_contact` và các trường PII trong `notify_carrier` → chưa phát sinh rò rỉ dữ liệu cá nhân (Tùng xác nhận giữ `0` ở mốc `after`). |
| Sự cố lộ ra trước qua số máy đo, phản hồi của người, hay đọc nội dung? Nguồn nào bàn chưa có? | Lộ ra từ **ba nguồn**: bảng tổng hợp chi phí của CFO + phản ánh đối soát hoàn trùng của chị Oanh (phản hồi của người), và cột `chi phí/ticket` + `LLM max` trên report `eval` (số máy đo). Nguồn nhóm còn thiếu ở vòng 1 là **chỉ số `monitors.py` cảnh báo chi phí theo từng kho** và **cảnh báo đồng bộ khi CSKH vừa hoàn tay cho một đơn**. |

#### Runbook 5 · Ba kịch bản "nếu … thì …" cho tuần đầu chạy thử thật
1. **Nếu số ticket tăng gấp `3` lần trong một giờ thì:** Khi hàng chờ đạt `>= 5 ca` hoặc thời gian chờ lâu nhất `> 40 phút`, `NV-HANH` gọi thêm 1 người duyệt dự phòng (lên `2 người = 12 ca/giờ`); nếu vẫn vượt `10 ca` chờ hoặc chạm SLA `60 phút` (`stuck > 0`), `NV-TUNG` thu hẹp `business.pilot_scope` về kho có chi phí thấp nhất (`HN`/`HCM`) hoặc chuyển sang xử lý tay theo Runbook 3.
2. **Nếu nhà cung cấp LLM lỗi quá `10` phút (hoặc chi phí LLM vọt quá trần `1.500đ/ticket` trên > 20% lượng đơn) thì:** `NV-TUNG` chuyển công tắc `issue_refund` và `file_carrier_fault` sang `"off"` trong `config/switches.json` trong tối đa 5 phút, đẩy toàn bộ ticket mới sang quy trình CSKH làm tay (`10.000đ/ticket`) do `NV-HANH` điều phối, chỉ bật lại khi xác nhận dịch vụ LLM và chi phí mỗi ticket trở về mức bình thường.
3. **Nếu người duyệt báo không tin một quyết định của trợ lý (nghi hoàn trùng, thiếu ghi chú giải thích hoặc sai phê duyệt) thì:** Chuyển ngay sang chế độ kiểm tra bổ sung (`review_sampling_pct = 100%` hoặc tắt `issue_refund` tạm thời), `NV-TUNG` và `NV-HANH` mở trace của ticket đó kiểm tra nguồn dữ liệu (`ledger_rows`, `approvals`, `decision_note`); giữ nguyên trạng thái tạm dừng đối với thao tác ghi lỗi cho tới khi sửa guard và kiểm chứng lại trên bộ nền + gói sự cố đều đạt `0` lỗi an toàn.
