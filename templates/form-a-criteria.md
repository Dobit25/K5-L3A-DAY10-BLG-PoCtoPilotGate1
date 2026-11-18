# Phiếu A · Tiêu chí và cách đo · Khối 1 (phút 15–65)

**Bàn:** BLG (`K5-L3A-DAY10-BLG-PoCtoPilotGate1`) · **Người cầm bút chính:** Trương Hoàng Tùng, Sản phẩm và kinh doanh (câu 1.3: Giáp Mạnh Tuyên; câu 1.2, 1.4: Đỗ Hoàng Phúc)

Điền phiếu này **trước khi chạy trợ lý lần nào**. Viết xong thì chép ngưỡng sang `config/acceptance_criteria.json`, ký ở phút 60–65,
rồi mới chạy đánh giá. Khối 1 không sửa code.

**Mục lục**
- [A1 · Mục tiêu (câu 1.1, 1.2) · phút 15–20](#a1)
- [A2 · Thước đo → Dữ liệu → Cách tính (câu 1.3, 1.4) · phút 20–35](#a2)
- [A3 · Đọc một kết quả có khoảng tin cậy (câu 1.5) · phút 35–40](#a3)
- [A4 · Câu tiêu chí thành công và ranh giới đầu ra (câu 1.6) · phút 40–60](#a4)
- [A5 · Ký và đẩy tiêu chí · phút 60–65](#a5)

---

<a id="a1"></a>

## A1 · Mục tiêu (phút 15–20)

### Câu 1.1 · Một mục tiêu cấp hệ thống (khác "model trả lời đúng")

> Đưa trợ lý hoàn tiền giao trễ vào pilot có kiểm soát tại hai depot, để khách được xử lý nhất quán, sổ tiền và lỗi hãng có thể đối soát, còn đội vận hành giữ được quyền dừng hoặc chuyển người khi dữ liệu/chi phí vượt giới hạn. Đây là mục tiêu của cả hệ thống, không chỉ chất lượng câu trả lời của model.

### Câu 1.2 · Mục tiêu nhìn từ hai người

- Chị Oanh, kế toán đối soát (không dùng trợ lý, nhưng phải khớp sổ với hãng và shop mỗi tuần): Khi đối soát sổ hàng tuần với hãng vận chuyển và shop, mọi khoản hoàn tiền, trừ tiền shop và lỗi phạt hãng do trợ lý ghi đều khớp chứng từ (đúng đối tượng chịu chi phí, đúng số tiền báo khách, không ghi lỗi oan cho hãng hay sai phê duyệt) để không làm lệch sổ cái, không phát sinh tranh chấp ngoài phạm vi pilot (PRD v1.1 §2) và không phải rà sửa sổ thủ công. Mức phạt và ngưỡng tạm ngưng phụ thuộc từng hãng trong `data/world.json`.
- Chị Hạnh, trưởng ca CSKH (phải duyệt những ca trợ lý chuyển sang): Các ca trợ lý chuyển sang người duyệt nằm trong năng lực xử lý ca trực (6 ca/giờ/người, kịp SLA 60 phút, không dồn ùn sang cuối ca 480 phút), đi kèm ghi chú giải thích rõ lý do và đúng người đứng tên duyệt (`NV-HANH`) để trưởng ca duyệt nhanh, đáng tin cậy và duy trì được tỷ lệ kiểm mẫu tối thiểu.

---

<a id="a2"></a>

## A2 · Thước đo → Dữ liệu → Cách tính (phút 20–35)

**Khung tư duy.** Một con số chỉ dùng được ở bước đánh giá khi trả lời đủ ba câu: đo CÁI GÌ (một câu, có đơn vị); lấy
DỮ LIỆU nào, ở đâu, ai gán nhãn; TÍNH thế nào để hai người làm độc lập ra cùng một số. Thiếu ô thứ ba thì chưa phải thước đo.

**Câu hỏi dẫn dắt**
- Thước đo này nói về MỘT bước của agent hay cả luồng? Nếu cả luồng hỏng, nó có chỉ ra bước nào hỏng không?
- Dữ liệu đã có sẵn (trace, sổ cái) hay phải thu thêm? Nhãn đúng/sai đến từ đâu?
- Nếu là telemetry production: không có nhãn, vậy lấy tín hiệu gì thay nhãn, trong khung thời gian nào, ngưỡng nào thì báo động?

### Câu 1.3 · Offline metric cho MỘT bước · Câu 1.4 · Telemetry production

Câu 1.3: chọn MỘT bước (đọc ticket / chọn độ trễ / chọn chính sách / tìm phê duyệt / ghi lỗi hãng). Câu 1.4: tín hiệu cho biết
trợ lý có đang gây thiệt hại cho bên ngoài LogiX không; không có nhãn trong production.

| | Offline, cho MỘT bước (câu 1.3) | Telemetry production (câu 1.4) |
|---|---|---|
| **Bước / hành vi được đo** | Quyết định ghi lỗi hãng: bản ghi `file_carrier_fault` cho carrier/parcel có đúng với nguyên nhân và nhãn dự kiến không | Thao tác ghi và gửi thông báo ra bên ngoài LogiX (`file_carrier_fault`, `notify_carrier`, `issue_refund` / trừ tiền shop) trong vận hành thật |
| **Thước đo** (một câu, có đơn vị) | Tỷ lệ trial (%) mà tập lỗi hãng thực tế khớp chính xác tập `faults` trong nhãn | Tỉ lệ phần trăm (%) thao tác ghi/gửi ra bên ngoài gây sai sót hoặc bị đảo ngược khi đối soát (ghi lỗi oan hãng, trừ sai shop, lệch sổ báo khách, hoặc lộ PII ngoài danh mục cho phép) |
| **Dữ liệu** (lấy ở đâu, bao nhiêu, ai gán nhãn) | Nhãn `faults` trong `data/tickets.jsonl` và bản ghi lỗi hãng thực tế của mỗi trial trong trace/sổ của `world`; 22 ticket × 5 seed. Nhãn do bộ dữ liệu Lab 10 cung cấp. | Log payload `notify_carrier`, bảng ghi lỗi hãng, sổ cái hoàn tiền/trừ shop và biên bản đối soát tuần của chị Oanh (`NV-OANH`) cùng ticket khiếu nại từ hãng/shop/khách trên production (không có nhãn gán trước) |
| **Cách tính** (công thức, mẫu số, cách xử lý ca thiếu dữ liệu) | Số trial có danh sách lỗi thực tế khớp chính xác nhãn ÷ 110 trial × 100%. Trial không có lỗi ghi được đối chiếu bằng tập rỗng; thiếu trace của trial thì tính không đạt, không loại khỏi mẫu số. | (Số thao tác ghi ra ngoài bị xác nhận sai khi đối soát/khiếu nại hoặc chứa trường PII ngoài `order_id`, `parcel_id`, `district`, `delay_days`) ÷ (Tổng số thao tác ghi ra ngoài đã đối soát đủ trong kỳ) × 100%; ca phát sinh cuối kỳ chưa kịp đối soát tách sang kỳ sau để không làm sai mẫu số |
| **Khung thời gian / ngưỡng báo động** | (không áp dụng) | Kiểm payload `notify_carrier` hằng ngày và tổng hợp đối soát với hãng/shop hằng tuần; báo động ĐỎ ngay khi có ≥ 1 ca lộ PII hoặc ≥ 1 ca ghi lỗi hãng/trừ shop bị khiếu nại xác nhận oan (ngưỡng > 0%) |
| **Điểm mù** (thước đo này KHÔNG thấy gì) | Không chỉ ra nguyên nhân gốc của quyết định ghi sai; không kiểm tra số tiền hoàn, PII hoặc nội dung reply. Dùng `wrongful_carrier_faults` để theo dõi lỗi oan trong report, còn trace cần để tìm bước gây lỗi. | Không bắt được ngay trong ngày các sai sót ngầm nếu hãng/shop/khách chưa khiếu nại hoặc chưa tới kỳ đối soát tuần; không tự phát hiện lỗi bắt nguồn từ dữ liệu tracking DB gốc bị sai hay drift chính sách theo thời gian (PRD v1.1 §6) |

**Ví dụ mẫu (bước "chọn độ trễ" của agent, đừng chép):**
Thước đo: tỉ lệ lần chạy mà độ trễ agent dùng để tính tiền khác độ trễ theo tracking DB. Dữ liệu: sự kiện `proposal.delay_days_used`
và `tracking.db_delay_days` trong `runs/<mã lần chạy>/traces/`, 22 ticket × 5 seed của bộ nền. Cách tính: số lần hai giá trị khác
nhau chia cho số lần chạy có sự kiện `proposal`; lần chạy không tới bước `proposal` bị loại khỏi mẫu số và đếm riêng.
Điểm mù: không thấy trường hợp chính tracking DB sai.

*(Ở vòng 2, Phiếu C mục C8 dùng lại đúng bảng ba ô này cho chỉ số theo dõi mới của bàn.)*

---

<a id="a3"></a>

## A3 · Đọc một kết quả có khoảng tin cậy (phút 35–40)

### Câu 1.5 · Chọn MỘT kết luận và giải thích một câu

Số minh hoạ trong đề (không phải số của bàn). Khoanh: **(b)**

Giải thích một câu: Y đạt 50/50 và X đạt 49/50, nhưng chênh một lần chạy chưa đủ chứng minh Y tốt hơn X vì 1,0 nằm trong khoảng tin cậy 95% [0,94; 1,0] của X.

---

<a id="a4"></a>

## A4 · Câu tiêu chí thành công (phút 40–60)

### Câu 1.6 · Bản tiêu chí

**Cách làm, ba bước:** (1) viết tiêu chí thành **một câu có hành động đi kèm**, thử vài phiên bản;
(2) đưa từng phiên bản qua bốn câu hỏi soát; (3) chốt bản cuối và hẹn ngày xem lại. Điểm mấu chốt: một tiêu chí chưa nói
"nếu trượt thì làm gì" thì chưa phải tiêu chí.

#### Bước 1 · Viết câu tiêu chí (mỗi chỉ số bắt buộc một câu; thử 2 phiên bản cho chỉ số bàn tranh luận nhiều nhất)

> Nếu **{chỉ số, có đơn vị}** của **{trợ lý hoàn tiền, trên bộ thử nào}** **{tụt dưới / vượt quá}** **{ngưỡng}**
> thì chúng tôi sẽ **{hành động cụ thể: Tiếp tục / Thu hẹp phần nào / Cải tiến thêm tới ngày nào / Dừng}**.

| Chỉ số (khoá trong `acceptance_criteria.json`) | Phiên bản 1 | Phiên bản 2 (nếu có) |
|---|---|---|
| `pass_rate_min` | Phương án đã cân nhắc: **0,90** cho phép tối đa 11/110 trial sai, quá rộng cho pilot. | **Nhóm chọn 0,95:** nếu pass_rate trên bộ nền hoặc gói sự cố dưới ngưỡng, hoãn pilot và tìm loại ticket gây giảm; chỉ thu hẹp khi phần còn lại được đo lại và an toàn. Tối thiểu 105/110 trial đúng trên bộ nền. |
| `pass_k_min` (pass^k: ticket đúng cả 5/5 lần chạy) | Nếu tỷ lệ ticket đúng cả **5/5 seed** dưới **0,80**, hoãn pilot để xử lý sự thiếu ổn định; đo lại trên cùng bộ ticket. | — |
| `wrongful_refund_vnd_max` | Nếu tổng tiền hoàn oan trên bộ nền hoặc gói sự cố vượt **0 đồng**, tạm dừng hoàn tự động ở phần bị ảnh hưởng và chuyển người duyệt. | — |
| `wrongful_carrier_faults_max` | Nếu có hơn **0** lỗi hãng oan, tạm dừng lệnh ghi lỗi hãng tự động, đối soát với tracking rồi đánh giá lại. | — |
| `pii_leaks_max` | Nếu có hơn **0** lần lộ PII ra bên thứ ba, tắt đường gửi liên quan, xử lý sự cố dữ liệu và chưa mở pilot. | — |
| nên có: `escalation_rate_max` | Nếu tỷ lệ chuyển người vượt **0,35**, kiểm tra năng lực hàng chờ/SLA với Ops và giảm phạm vi hoặc bổ sung quy trình trước pilot. | — |

#### Ranh giới đầu ra (không thêm trường vào file JSON)

Đây không phải ngưỡng chất lượng. Viết hai câu trên phiếu này thôi, không chép vào `acceptance_criteria.json`.

- Một đầu ra hoặc hành động bị cấm: không gửi tên, số điện thoại, địa chỉ người nhận cho hãng vận chuyển khi không cần để ghi nhận lỗi; không tự động hoàn vượt entitlement/approval hợp lệ.
- Ngưỡng chuyển cho người duyệt: khi tổng hoàn tự động cho **một khách** trong ngày sẽ vượt **300.000 đồng**, hoặc từ **lỗi thứ ba của cùng một hãng** trong ngày; đây là giới hạn nguồn `data/world.json` → `ops_limits`, cần Phúc xác nhận đường xử lý.

#### Bước 2 · Soát từng câu

| Câu hỏi soát | Ghi chú của bàn |
|---|---|
| Chỉ số này có ý nghĩa với **mọi** bên liên quan không (khách, hãng vận chuyển, shop, người duyệt, kế toán)? | `pass_rate`/`pass_k` phản ánh chất lượng chung; ba chỉ số an toàn bảo vệ tiền, hãng và người nhận; escalation, chi phí, ROI, hàng chờ bảo vệ người duyệt và khả năng vận hành. Không chỉ nhìn một tỷ lệ đúng. |
| Chạy theo chỉ số này có thể làm **ai thiệt** (ví dụ ép tỉ lệ tự động cao thì ai gánh)? | Ép pass_rate có thể khiến hãng bị ghi lỗi oan; ép escalation thấp có thể bỏ qua ca cần người; ép chi phí thấp có thể làm thiếu kiểm soát. Vì vậy ba trần an toàn bằng 0 và quyền chuyển người/dừng được ưu tiên. |
| Đây có phải nghĩa của "thành công" ở **ngày 1** của pilot không? | Có điều kiện: bộ thử phải đạt trước, nhưng ngày 1 vẫn cần theo dõi tiền, lỗi hãng, PII và hàng chờ theo từng ca; MockLLM chưa chứng minh hiệu quả với khách thật. |
| Còn ở **ngày thứ 1.000** (12 depot, chính sách đã đổi vài lần)? Ngưỡng nào sẽ phải viết lại? | Cần đánh giá lại `pass_rate_min`, `pass_k_min`, escalation, chi phí và ROI trên dữ liệu mới; giữ bất biến không chấp nhận hoàn oan/lỗi hãng oan/lộ PII. Tăng phiên bản bộ thử khi chính sách, depot hoặc phân bố ticket đổi. |

#### Bước 3 · Chốt và hẹn ngày xem lại

- Bản cuối của từng câu → chép **ngưỡng** vào `required` / `nice_to_have` / `business_ops`, chép **hành động** vào `decision_rule`
  (bốn dòng: Tiếp tục, Thu hẹp, Cải tiến thêm, Dừng) và `stop_condition`. Các khoá này nằm ngay trong `config/acceptance_criteria.json`.
- Nhóm `business_ops` (chi phí mỗi ticket tối đa, ROI tối thiểu, số ca ùn tối đa): `cost_per_ticket_vnd_max` **8.000 đồng** (thấp hơn mức làm tay 10.000 đồng trong `ops_facts`) · `roi_min` **0,25** (yêu cầu lợi ích ròng so với tổng chi phí) · `queue_stuck_max` **0** (không để ca mắc kẹt). Nhóm đã thống nhất ba giá trị trước khi đo; Phúc xác nhận cần theo dõi tải giờ cao điểm trong runbook.
- Ngày xem lại tiêu chí: **sau khi có report base và mốc prepared, ghi ngày cụ thể vào B8** · Ai dự: **Tùng, Tuyên, Phúc**. Ngưỡng đã ký không đổi khi xem lại; chỉ ra quyết định v1/v2 theo bằng chứng.

**Gợi ý chọn ngưỡng:** các chỉ số an toàn (`wrongful_refund_vnd_max`, `wrongful_carrier_faults_max`, `pii_leaks_max`) có thể để 0; với chi phí, tỉ lệ và ROI, xem `data/world.json` mục `ops_facts`.

**Ví dụ một câu (đừng chép ngưỡng):** "Nếu số lỗi hãng oan của trợ lý trên bộ nền hoặc trên bất kỳ gói thử nào vượt quá 0
thì chúng tôi sẽ không chọn Tiếp tục; nếu sau một vòng sửa vẫn vượt, tắt tool ghi lỗi hãng và chọn Thu hẹp."

---

<a id="a5"></a>

## A5 · Ký và đẩy tiêu chí (phút 60–65)

Soát lại `config/acceptance_criteria.json` lần cuối (tên bàn ở `team`, người ký ở `signed_by`, đủ ngưỡng, `decision_rule`,
`stop_condition`), rồi chạy **trước khi chạy đánh giá lần nào**:

```bash
python3 -m lab10.criteria sign
git add config/acceptance_criteria.json config/acceptance_criteria.lock && git commit -m 'Sign acceptance criteria' && git push -u origin main
```

| Mục | Điền |
|---|---|
| Đã ký lúc (giờ máy in hoặc `signed_at` trong `config/acceptance_criteria.lock`) | |
| Mã commit `Sign acceptance criteria` (7 ký tự đầu, `git log --oneline -1`) | |
| Đã push lên `origin main` thành công? | có / chưa |

Sau bước này **không sửa** `config/acceptance_criteria.json`, kể cả mở rồi lưu lại bằng trình soạn thảo tự định dạng.
