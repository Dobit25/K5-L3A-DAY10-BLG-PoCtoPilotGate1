# Kế hoạch thực hiện Lab 10 — PoC to Pilot, Gate 1

> Tài liệu chia việc cho nhóm 3 người. Các mốc phút là **thứ tự của đề bài trong buổi lab 240 phút**, không phải cam kết rằng có thể tự chạy trước khi Lab Coach phát thẻ. Repo làm việc: `K5-L3A-DAY10-BLG-PoCtoPilotGate1`; mọi lệnh dưới đây chạy từ **gốc repo**, nơi có `README.md`.

## 1. Mục tiêu và trạng thái hiện tại

Nhóm đóng vai đội LogiX-VN quyết định có đưa trợ lý AI hoàn tiền giao trễ từ PoC sang pilot với khách thật hay không. Sản phẩm cuối gồm tiêu chí chấp nhận đã ký trước khi đo, bằng chứng đánh giá ba mốc `base` / `prepared` / `after`, cổng phòng ngừa bằng code và config, phân tích sự cố đúng thẻ đã bốc, quyết định Gate 1 v1/v2 có số liệu, cùng bộ hồ sơ nộp hoàn chỉnh. Quyết định **Tiếp tục / Thu hẹp / Cải tiến thêm / Dừng** đều có thể đúng nếu khớp tiêu chí và report; không chọn “Tiếp tục” khi còn vượt trần hoặc chưa đạt ngưỡng đã ký.

Trạng thái khi lập kế hoạch: repo đang ở `main`, `origin` trỏ về repo nhóm, `upstream` trỏ về repo mẫu của giảng viên; cây Git ban đầu sạch. Python 3.13.9 chạy `python -m unittest discover -s tests` cho **13/13 test OK**. `TEAM.md`, ba phiếu, các config và `submission.json` còn là mẫu; `lab10/guards.py` đang cho qua hết; `lab10/monitors.py` mới có `escalation_rate`. `incidents/` hiện chỉ có `README.md`, **chưa có thẻ Sx**. Chưa có bằng chứng đã ký tiêu chí, checkpoint vòng 1, hay kết quả eval; không tự điền số hoặc quyết định trước khi có report.

Đầu vào chính: [đề bài](problem-set.md), [timeline và lệnh](README.md), [rubric](RUBRIC.md), [checkpoint](CHECKPOINTS.md), [hướng dẫn](docs/guide.md), [quy tắc](RULES.md), [hướng dẫn nộp](SUBMISSION.md), ba mẫu trong `templates/`, `data/world.json` (`ops_limits`, `ops_facts`, đơn hàng, chính sách), `data/tickets.jsonl`, eval card và PRD v1.1 của Lab 9 do nhóm chọn. Lab 10 dùng Python 3 chuẩn, **không yêu cầu cài dependency hay sửa môi trường Conda**.

## 2. Quyền sở hữu file để cùng làm trên một nhánh

**Nguyên tắc:** mỗi file do đúng một người ghi/commit. Thành viên khác nghiên cứu và gửi nội dung, bằng chứng, mã run, đề xuất qua chat hoặc review cho chủ file. Không cùng lúc mở, lưu hoặc `git add` một file thuộc người khác. Phân vai theo nội dung đề vẫn giữ nguyên; quyền ghi file được tập trung để tránh conflict.

| Người | Chịu trách nhiệm chuyên môn | File được ghi trực tiếp | Đầu vào phải bàn giao cho chủ file khác |
|---|---|---|---|
| **@Mạnh Tuyên — kỹ sư cổng** | Baseline, trace, 2–3 cổng phòng ngừa, regression, monitor sự cố | `lab10/guards.py`, `lab10/monitors.py` | Run ID, dòng trace, bảng lỗi, thiết kế cổng, kết quả test, nội dung B1–B2/B7.1–B7.3 và C2/C7–C9 để trưởng nhóm chép vào phiếu |
| **@Hoàng Phúc — vận hành và pháp lý** | HAZOP, 9 nhóm checklist có PIC, con người/pháp lý, runbook, hàng chờ, hồ sơ nộp | `submission/submission.json` **sau khi** trưởng nhóm chốt v1/v2 và C12 | Đề xuất JSON `operations`/`legal` kèm lý do từ `world.json`, B4–B5/B7.5–B7.6, C4/C10–C11, phần cá nhân trong TEAM.md; gửi trưởng nhóm để tích hợp |
| **Tôi — sản phẩm, kinh doanh, trưởng nhóm** | Tiêu chí, ngân sách/ROI, phạm vi pilot, quyết định và tích hợp tài liệu | `config/acceptance_criteria.json`, `config/operating_gates.json` **toàn file**, cả 3 `templates/form-*.md`, `TEAM.md`, `plan01.md`; điều phối file sinh từ lệnh | Chốt ngưỡng, số liệu kinh doanh, phạm vi pilot, nội dung v1/v2/C12; gửi quyết định và ba dòng C12 cho Hoàng Phúc điền `submission.json` |

**Điểm chồng lấn do trưởng nhóm xử lý:** `config/operating_gates.json` chứa cả `business` lẫn `operations`/`legal`, nên chỉ trưởng nhóm merge đề xuất của Phúc vào một JSON. Ba phiếu chứa ý kiến cả ba vai, nên trưởng nhóm là người biên tập/commit cuối cùng; Tuyên và Phúc gửi câu trả lời đúng số mục, có run ID/trace/PIC, không sửa phiếu. `TEAM.md` cũng do trưởng nhóm tích hợp, nhưng **từng người phải tự viết nội dung mục cá nhân** rồi gửi. `submission/` do lệnh 7 tự tạo nhiều file; chỉ trưởng nhóm chạy lệnh gom và commit các file sinh, còn Phúc chỉ sửa `submission/submission.json`. Checkpoint vòng 1 và lệnh ký cũng chỉ trưởng nhóm chạy một lần trên bản đã được cả nhóm duyệt.

Không chỉnh `lab10/agent.py`, `helpers.py`, `eval.py`, `grade.py`, `criteria.py`, `checkpoint.py`, `check_submission.py`, `tests/test_public.py`, dữ liệu nền, file `incidents/Sx/*`, `lab10/MANIFEST.json` hoặc các file đề khóa bằng hash. Sau khi ký không sửa `config/acceptance_criteria.json`/`.lock`. Sau checkpoint không sửa `lab10/guards_round1.py`, `config/operating_gates.round1.json`, `config/round1.lock`. Không sửa bản chép trong `submission/docs/`; sửa phiếu gốc rồi gom lại. Không hardcode mã ticket/câu chữ để vượt test ẩn. `plan01.md` là tài liệu điều phối thêm, không thay thế ba phiếu bắt buộc.

### Quy tắc Git cho **một nhánh `main` chung**

1. `origin` là repo nhóm; **không push lên `upstream`**. Mỗi người làm ở clone riêng hoặc worktree riêng. Trước khi sửa, pull thay đổi mới nhất của `origin/main`; chỉ `git add` đúng file mình sở hữu, không dùng `git add .`.
2. Mỗi người commit phần mình, thông báo hash và file đã sửa; push **tuần tự**, người push sau lấy `origin/main` mới rồi mới push. Nếu pull/rebase báo xung đột hoặc có sửa dở, dừng và báo trưởng nhóm; không dùng `push --force`, không reset file của người khác.
3. Trưởng nhóm công bố các “điểm đóng băng”: **trước ký**, **trước eval đầu**, **trước checkpoint**, **trước kéo thẻ**, **trước lệnh gom nộp**. Tại các điểm này, mọi người ngừng sửa code/config tới khi run và commit xong. Chỉ trưởng nhóm chạy các lệnh tạo bằng chứng trên một clone chuẩn, để `runs/journal.jsonl` và report ba mốc không phân tán giữa máy.
4. Riêng commit `Sign acceptance criteria` phải chứa tiêu chí và lock; **push trước lần chạy `eval` đầu tiên**. Commit chốt vòng 1 chứa snapshot và B8, push **trước khi nhận thẻ**. Khi Lab Coach phát thẻ, trưởng nhóm dùng đúng lệnh kéo `upstream` của đề sau khi cả nhóm đã commit/push và cây sạch. Chỉ mở thẻ được bốc.

## 3. Lịch triển khai và handoff

| Mốc | Việc có thể làm song song | Điểm đồng bộ và đầu ra |
|---|---|---|
| **CP1, phút 0–15** | Tuyên kiểm tra code/CLI; Phúc đọc checklist và dữ kiện vận hành; trưởng nhóm xác nhận repo private, quyền Read của team chấm, thông tin ba thành viên, Git identity | `TEAM.md` đủ tên/MSSV/vai; `origin`/`upstream` đúng; 13 public tests OK; chọn eval card và PRD Lab 9 chung |
| **CP2, phút 15–65** | Tuyên đề xuất cách tính metric; Phúc đề xuất tiêu chí pháp lý/vận hành; trưởng nhóm viết Phiếu A và JSON tiêu chí | Cả nhóm duyệt ngưỡng **trước khi đo**. Trưởng nhóm `sign` đúng một lần, commit/push, điền A5 giờ ký và hash |
| **CP3a, phút 65–85** | Sau ký: Tuyên phân tích baseline/trace; Phúc HAZOP và checklist; trưởng nhóm bản đồ dữ liệu và pre-mortem kinh doanh | Trưởng nhóm chạy baseline/gate/trace trên clone chuẩn, chuyển run ID và bằng chứng cho cả nhóm; điền B0–B6 |
| **CP3b, phút 85–105** | Tuyên code guards; Phúc soạn số người trực, SLA, pháp lý, runbook; trưởng nhóm điền business và tích hợp JSON/phiếu | Trưởng nhóm chạy `base --stage after`, ad hoc trace, 13 tests; giữ ca đúng, phạm vi pilot > 0, chi phí và hàng chờ có cơ sở |
| **CP3c, phút 105–115** | Cả nhóm duyệt cổng v1 và quyết định; các file tạm ngừng sửa | Trưởng nhóm chạy checkpoint **một lần**, `base --stage prepared`, gate, ghi B8, commit/push bản chốt; snapshot bất biến |
| **CP4a, từ phút 125** | Sau khi Coach phát thẻ: trưởng nhóm kéo upstream, ghi số thẻ; Tuyên đọc trace; Phúc điều tra nguyên nhân ngoài kỹ thuật; trưởng nhóm đối chiếu tiêu chí và chi phí | Chạy `grade --incident Sx` **trước khi sửa**; xác nhận integrity và thẻ khớp; có report `base`/`prepared`; chỉ làm đúng Sx |
| **CP4b, phút 135–185** | Tuyên sửa guards + thêm monitor; Phúc soạn HAZOP sự cố, fault tree, risk register, runbook 4–5; trưởng nhóm chỉnh config và phiếu C | Chạy `Sx --stage after`, `base --stage after`, `grade`; ghi C0–C11 với hai ticket lỗi khác kiểu, số liệu trước/sau, monitor sáng đèn, không có ca nền mới hỏng |
| **CP5, phút 185–240** | Trưởng nhóm chốt v2/C12; Phúc điền `submission.json` theo quyết định đã duyệt; Tuyên chuẩn bị demo ba mốc và ticket ad hoc | Trưởng nhóm gom nộp tới `ĐỦ THÀNH PHẦN`, demo, chạy lại grade+collect nếu demo đổi config, commit/push; mỗi người hoàn thành TEAM và tự nộp link LMS |

## 4. Công việc chi tiết theo vai

### @Mạnh Tuyên — kỹ sư cổng

| Việc | Đầu vào | Đầu ra và kiểm tra |
|---|---|---|
| Thiết kế phép đo, baseline | `problem-set.md` câu 1.3; `data/tickets.jsonl`; tiêu chí đã ký; output `base --stage base` | Bảng “thước đo → dữ liệu → cách tính” cho A2; giải thích `pass_rate` và `pass_k` (= pass^5, đúng cả 5 seed); run ID, khoảng tin cậy, chỉ số sai và lát cắt kho/hãng cho B0–B1 |
| Soát lỗi nền | Trace `T-002@55` và ledger/fault/outbound | B2 ba phần: lỗi người dùng thấy, nguồn lỗi, hướng xử lý; mỗi kết luận có dòng trace hoặc row làm bằng chứng. Một phép thử hành vi gồm hai ticket hiểm chạy `--adhoc` cho B7.3 |
| Code cổng vòng 1 | Pre-mortem B6, HAZOP B4, `lab10/helpers.py` và API `Verdict` | `lab10/guards.py`: 2–3 cổng tổng quát; `pre_guard(ctx)` trước đọc ticket, `write_gate(ctx, action)` trước `issue_refund`, `file_carrier_fault`, `notify_carrier`, `send_reply`; ưu tiên DB/chính sách/approval hơn lời khách, tránh ghi sai/PII. Không chặn sạch mọi ca; báo rõ khi escalate/modify |
| Sửa theo thẻ và theo dõi | Thẻ Sx đã bốc, report `prepared`, hai trace lỗi khác kiểu, fault tree | Sửa **tiếp** `lab10/guards.py`, giữ cổng vòng 1; thêm ít nhất một hàm số trong `lab10/monitors.py` và đăng ký trong `MONITORS`. Monitor dùng trial **không có nhãn đúng/sai**, chạy không lỗi và giá trị đổi giữa nền và sự cố; `escalation_rate` có sẵn không tính |
| Kiểm chứng | Code/config sau tích hợp, `grade` và report ba mốc do trưởng nhóm tạo | 13 public tests OK; report integrity, visible, regression, monitor; bằng chứng ca hợp lệ vẫn đúng. Gửi hash commit guards/monitors, trace và run ID để trưởng nhóm điền B7, C2, C7–C9 |

**Lệnh trên clone chuẩn do trưởng nhóm điều phối** (trên Windows dùng `python` thay `python3`):

```powershell
python -m lab10.eval --suite base --stage base --note "baseline"
python -m lab10.gate --run runs/<run-id>/report.json
python -m lab10.trace --suite base --ticket T-002 --seed 55
python -m lab10.eval --suite base --stage after --note "cong vong 1"
python -m unittest discover -s tests
```

### @Hoàng Phúc — vận hành và pháp lý

| Việc | Đầu vào | Đầu ra và kiểm tra |
|---|---|---|
| Tiêu chí và nguồn dữ liệu | `data/world.json` (`ops_limits`, `ops_facts`), Phiếu A câu 1.2/1.4, tiêu chí chưa ký | Đề xuất metric pháp lý/vận hành, cách tính và nguồn dữ liệu; gửi trưởng nhóm trước ký, không tự sửa JSON tiêu chí |
| HAZOP/checklist vòng 1 | Tool ghi của agent, dữ kiện Ops/Finance, Phiếu B | B4 ít nhất 3 dòng, trong đó ít nhất 2 dòng **ngoài kỹ thuật**; B5 đủ 9 nhóm go-live, mỗi dòng có **PIC tên cụ thể**; B6 lăng kính vận hành và pháp lý, có 2–3 lý do thành cổng |
| Cổng số và runbook | `ops_limits`, `ops_facts`, baseline, công suất người duyệt | Đề xuất `operations.pic`, `approver_id`, `reviewers_on_shift`, `review_capacity_per_hour`, `max_queue_wait_minutes`, `stop_conditions`, `alert_channel`, `decision_note`, `review_sampling_pct`; `legal.pii_fields_blocked_to_third_party`, `carrier_fault_requires_recorded_cause`. Mỗi số có lý do; runbook phần 1–3 và giờ cao điểm khớp config. Gửi đoạn JSON `operations`/`legal` cho trưởng nhóm tích hợp |
| Điều tra sự cố | Sx đã bốc, trace và report ba mốc, B4/B5 đã lưu | C4 HAZOP sự cố **riêng**, C6/C9 nhánh fault tree ngoài kỹ thuật, C10 risk register ít nhất 1 dòng, C11 checklist cập nhật và runbook phần 4–5; chỉ ra chủ trách nhiệm, thời gian phản ứng, stop/rollback, PII và thông báo bên thứ ba |
| Gói nộp | Quyết định v1/v2, ba câu C12, số thẻ, danh sách thành viên từ trưởng nhóm | Sửa duy nhất `submission/submission.json`: `team` khớp **chính xác** tên repo và tiêu chí, `members` dạng `HoVaTen-MSSV` khớp TEAM, `incident` đúng Sx, quyết định thuộc 4 giá trị hợp lệ, `three_lines` chép nguyên từ C12; gửi hash commit cho trưởng nhóm |

### Tôi — sản phẩm và kinh doanh, nhóm trưởng

| Việc | Đầu vào | Đầu ra và kiểm tra |
|---|---|---|
| Thiết lập và chia vai | Tên repo, MSSV/role đủ 3 người, tài khoản team chấm | Xác nhận repo tên chuẩn và **private**, mời quyền Read, Git identity theo MSSV + `<MSSV>@example.com`, `TEAM.md` đủ bảng và các mục `## HoVaTen-MSSV`; mỗi người cung cấp đóng góp, commit, run ID, exit ticket, việc dùng AI nếu có |
| Tiêu chí trước khi đo | Eval card + PRD v1.1 của Lab 9, đề câu 1.1–1.6, đề xuất Tuyên/Phúc, `world.json` | Phiếu A A1–A4; `config/acceptance_criteria.json` điền `team`, `signed_by`, toàn bộ `required`, `nice_to_have`, `business_ops`, `stop_condition`, bốn `decision_rule`. Chọn ngưỡng có giải thích; không chép ngưỡng example. Cả nhóm duyệt rồi ký/commit/push và ghi A5 |
| Tích hợp vòng 1 | Baseline, B2 của Tuyên, B4/B5 của Phúc, dữ kiện kinh doanh | Phiếu B B0–B8; B3 bản đồ dữ liệu + drift; B6 đủ bốn lăng kính; `config/operating_gates.json` phần `business` (trần hoàn/ngày, budget/ticket, pilot_scope, ROI floor), tích hợp `operations`/`legal` của Phúc; lý do từng con số lấy từ report/`world.json` |
| Chốt v1 | Report base/prepared + gate, danh sách vượt trần, lát cắt kho/hãng | Checkpoint một lần, ghi commit ký/hash snapshot/run ID và quyết định có điều kiện trong B8; commit/push trước khi bốc thẻ |
| Tích hợp vòng 2 và v2 | Sx, grade trước/sau, fault tree, monitor, chi phí/ROI/hàng chờ | Phiếu C C0–C12 hoàn chỉnh: bảng soát lỗi, phần riêng **đúng thẻ** (S4 không bắt buộc C3), HAZOP, specification, fault tree trước/sau, bảng sửa “giảm/ngăn”, monitor, risk register, runbook, quyết định v2. So sánh v1/v2, nêu 3 bằng chứng có run ID, segment xấu nhất, giả định chưa đo; gửi quyết định và 3 câu C12 cho Phúc |
| Nộp và demo | File của Tuyên/Phúc đã commit, Phiếu A/B/C, report chuẩn | Chạy lệnh 7 tới `ĐỦ THÀNH PHẦN`; kiểm `submission/runs/` có journal, grade-report, ba mốc, manifest; demo ca ad hoc và ba mốc; nếu đổi config lúc demo thì trả về v2 và chạy lại grade/collect; commit/push và nhắc **từng người** nộp link LMS |

## 5. Thứ tự lệnh và bằng chứng bắt buộc

| Thời điểm | Lệnh trên clone chuẩn (thay `Sx`, `<run-id>` bằng giá trị thật) | Bằng chứng cần lưu |
|---|---|---|
| Trước eval đầu | `python -m lab10.criteria sign` rồi commit/push **`config/acceptance_criteria.json` + `config/acceptance_criteria.lock`** với message `Sign acceptance criteria` | `ĐÃ KÝ.`, giờ/commit trong A5, lịch sử Git ký trước journal đầu |
| Baseline | `python -m lab10.eval --suite base --stage base --note "baseline"`; `python -m lab10.gate --run runs/<run-id>/report.json`; `python -m lab10.trace --suite base --ticket T-002 --seed 55` | Run ID, report, trace, B0–B2, lát cắt kho/hãng |
| Trước chốt | `python -m lab10.eval --suite base --stage after --note "cong vong 1"`; ad hoc trace; `python -m unittest discover -s tests` | Regression/chi phí/ROI/queue và 13 tests; B7 |
| Chốt vòng 1 | `python -m lab10.checkpoint`; `python -m lab10.eval --suite base --stage prepared`; `python -m lab10.gate --run runs/<run-id>/report.json`; commit/push guards, config, snapshot, lock, Phiếu B | Hash checkpoint; snapshot `guards_round1.py`, `operating_gates.round1.json`, `round1.lock`; B8 v1 |
| Sau khi Coach phát thẻ | `git pull --no-rebase --no-edit --allow-unrelated-histories -X ours upstream main`; ghi Sx; `python -m lab10.grade --incident Sx` **trước sửa** | Chỉ đọc `incidents/Sx/card.md`; thẻ khớp; report trước sửa, integrity ✅ |
| Sau khi sửa | `python -m lab10.eval --suite Sx --stage after --note "doi mot thu"`; `python -m lab10.eval --suite base --stage after --note "kiem lai bo nen"`; `python -m lab10.grade --incident Sx` | Report `base`/`prepared`/`after`; monitor và regression; số liệu C7–C12 |
| Gom bài | Phúc hoàn tất `submission/submission.json`; trưởng nhóm chạy `python -m lab10.check_submission --collect` và lặp lại sau từng mục `[THIẾU]` | Dòng cuối `ĐỦ THÀNH PHẦN`, `submission/manifest.json`, docs/code/config/runs đủ; commit/push cuối |

Không có sẵn Sx thì lệnh grade từ chối là **đúng thiết kế**; không tự tạo/đoán thẻ. Các lần `eval` tạo report và `runs/journal.jsonl`; không sửa JSON report bằng tay. Bằng chứng ba mốc dùng cho quyết định phải được tạo trên đúng code/config cuối cùng. Nếu demo đổi số, chạy lại grade và collect sau khi hoàn nguyên.

## 6. Definition of Done theo vai và toàn nhóm

### Kỹ sư cổng — @Mạnh Tuyên

- [ ] `lab10/guards.py` có 2–3 cổng vòng 1 tổng quát và phần sửa vòng 2 đúng nguyên nhân của Sx; không sửa snapshot, agent, helper, test đề.
- [ ] `lab10/monitors.py` có ít nhất một monitor mới từ trial không nhãn, chạy không lỗi và “sáng đèn” trên sự cố.
- [ ] Có trace của `T-002@55` và ít nhất hai trace lỗi Sx khác kiểu, kèm event/row cụ thể; public tests 13/13 OK và không có ca nền mới hỏng.
- [ ] Gửi trưởng nhóm commit hash, run ID, kết quả grade và đoạn viết đủ cho các mục phiếu kỹ thuật.

### Vận hành và pháp lý — @Hoàng Phúc

- [ ] B4 HAZOP ≥3 dòng, ≥2 dòng ngoài kỹ thuật; B5 đủ 9 nhóm có PIC tên thật; C4 HAZOP sự cố độc lập, C10 risk register ≥1 dòng, C11 cập nhật checklist và runbook.
- [ ] Đề xuất `operations`/`legal` có tên PIC/người duyệt, năng lực hàng chờ, thời gian tối đa, stop condition, kênh cảnh báo, quy tắc PII và ghi lỗi hãng; con số/biện pháp khớp dữ kiện và runbook.
- [ ] `submission/submission.json` khớp tên repo/TEAM/thẻ/quyết định và ba dòng C12; commit chỉ file mình sở hữu.
- [ ] Đã gửi nội dung cá nhân `TEAM.md` và tự nộp link repo lên LMS.

### Sản phẩm và kinh doanh, trưởng nhóm — tôi

- [ ] Tiêu chí có metric bắt buộc, business ops, stop condition và bốn decision rule giải thích được; ký **trước eval đầu**, commit/push; không sửa sau ký.
- [ ] `config/operating_gates.json` đầy đủ ba mục business/operations/legal, có số hợp lý từ `world.json`/report, pilot scope còn giá trị và không dùng tăng người trực vô lý để làm xanh bài.
- [ ] Phiếu A A1–A5, B B0–B8, C C0–C12 đã điền mọi mục bắt buộc, có mã run/trace/PIC và quyết định v1/v2 nhất quán với report. TEAM có đủ mục cá nhân từng người; ghi AI nếu có dùng.
- [ ] Đã chốt/push vòng 1 trước thẻ; snapshot/lock nguyên vẹn; kéo upstream và chỉ làm đúng thẻ bốc.
- [ ] Chạy lệnh 7 in `ĐỦ THÀNH PHẦN`, `submission/runs/` có journal + grade-report + ba report, `submission/manifest.json` được sinh; commit/push cuối và mỗi thành viên nộp link LMS đúng hạn.

### Điều kiện qua của toàn nhóm

- [ ] `grade` in `integrity ✅`; file khóa, tiêu chí đã ký và snapshot vòng 1 không bị thay đổi.
- [ ] Report có ba mốc và ghi được cổng phòng ngừa đã giúp gì **trước khi** biết sự cố; `visible`, `regression`, `monitor` được kiểm trên đúng Sx. Test ẩn là phần chấm sau buổi học, không thể khẳng định đã pass trước khi team chấm chạy.
- [ ] V2 khớp cả `decision_rule` đã ký lẫn số liệu (`required`, chi phí/ROI/queue, trần tiền/pháp lý). Nếu còn vượt ngưỡng, chọn `Thu hẹp`, `Cải tiến thêm` hoặc `Dừng` có căn cứ; không tự chọn “Tiếp tục”.
- [ ] Repo nhóm đúng tên, private, team chấm có quyền Read; `team` trong hai JSON bằng đúng tên repo; từng thành viên có mục cá nhân và tự nộp link LMS.

**Lưu ý bàn giao:** các ngưỡng cụ thể, số người trực, phạm vi pilot và v1/v2 phải do nhóm chọn từ dữ liệu và report, giải thích được lúc demo. Kế hoạch này không điền sẵn đáp án hay kết quả thẻ chưa phát.
