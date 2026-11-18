# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): `BLG`
- Lớp: `L3A`
- Repo của bàn: `K5-L3A-DAY10-BLG-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8): **S5** — CFO: mỗi ticket qua trợ lý đang đắt hơn làm tay.

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; thêm dòng nếu cần. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
|   1 | Trương Hoàng Tùng | 2A202603651 | Sản phẩm và kinh doanh | Trưởng nhóm |
|   2 | Giáp Mạnh Tuyên | 2A202603648 | Kỹ sư cổng | Thành viên |
|   3 | Đỗ Hoàng Phúc | 2A202603652 | Vận hành và pháp lý | Thành viên |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

## TruongHoangTung-2A202603651

### Phần việc phụ trách

Trưởng nhóm, vai Sản phẩm và kinh doanh. Phụ trách câu 1.1 và 1.6 (Phiếu A A1/A4), câu 2.3 và 2.9 (Phiếu B B3/B7.4), tích hợp quyết định v1/v2 ở B8/C12 và phần thông tin nhóm. File phụ trách: `config/acceptance_criteria.json`, mục `business` trong `config/operating_gates.json`, ba phiếu trong `templates/`, `TEAM.md` và hồ sơ gom nộp.

### Đóng góp cụ thể

Chuẩn bị mục tiêu cấp hệ thống và bản tiêu chí trước khi đo, dựa trên eval card/PRD v1.1 Lab 9 cùng `data/world.json` của Lab 10. Tích hợp đề xuất kỹ thuật của Giáp Mạnh Tuyên và đề xuất vận hành/pháp lý của Đỗ Hoàng Phúc vào phiếu và config dùng chung; điều phối ký tiêu chí, chạy các mốc đánh giá, chốt cổng vòng 1 và quyết định v1 có run ID. Với S5, phân tích tiền máy, công người, phí trực, hoàn sai và lát cắt kho; tích hợp code/monitor và runbook, sửa cổng hoàn phần quyền lợi còn lại, giữ từ chối tự động khoản đã hoàn đủ, mở pilot bốn kho bán lẻ sau khi đo. Phiếu C C0–C12 đã có bằng chứng; v2 **Tiếp tục** bốn kho bán lẻ đã ký sau hai review và grade cuối.

### Bằng chứng

Phiếu A tại `templates/form-a-criteria.md`; tiêu chí tại `config/acceptance_criteria.json` đã ký trước lần eval đầu. Commit ký: `b5ef4b58a135812b56007c3a5705d9a0a362db74`; hash tiêu chí: `63eef882317d0ade80c4bfcb9c952a650a16a50d8c9f41662980de697cf76599`. Nhóm thống nhất v1 Thu hẹp HN/HCM; checkpoint `f60329ce`, prepared nền `R-base-prepared-20261118-164010-4133d4` đạt 65/65. Lượt S5 đầu `R-S5-grade-20261118-165749-4133d4` có prepared pass_rate 0,8, hoàn sai 225.000đ/5 seed, 10 lỗi hãng oan, LLM max 2.466đ và ROI 0,06. Sau tích hợp Tuyên/Phúc và sửa cân bằng ledger/phạm vi, `R-S5-grade-20261118-173600-4fa077` PASS-VISIBLE: integrity/criteria/visible/regression/monitor xanh; S5 after 90/90, 0 hoàn oan/lỗi hãng oan/PII, 3.980đ/ticket, ROI 1,51, độ phủ 18/30, escalation 0,1667. Bộ nền after `R-base-after-20261118-173610-4fa077` 110/110; gate S5 exit 0, không có ca mới hỏng. V2 đã ký: Tiếp tục pilot HN/HCM/CT/DN, giữ HCM-B2B làm tay. Grade kiểm chứng cuối `R-S5-grade-20261118-215041-4fa077` PASS-VISIBLE, integrity xanh; hồ sơ đã gom và checker báo ĐỦ THÀNH PHẦN.

### Exit ticket

- Điều học được: cách phối hợp đội nhóm để hoàn thành project.
- Điều còn chưa chắc: cách phối hợp để tối ưu công việc hơn thay vì chỉ chia ba vai trò đơn thuần.

### Sử dụng AI

Dùng Codex hỗ trợ khám phá repo, lập kế hoạch và phân công, phân tích report/trace, hiện thực và tích hợp guard/config, soạn hồ sơ, thao tác Git và kiểm chứng bằng grade/checker. Trưởng nhóm duyệt ngưỡng, xác nhận review hai thành viên và ủy quyền ký v2 dựa trên report cuối; Exit ticket do Tùng cung cấp trực tiếp.

## GiapManhTuyen-2A202603648

### Phần việc phụ trách

Kỹ sư cổng. Theo kế hoạch nhóm: kiểm tra code/CLI ở CP1; đề xuất cách tính metric ở CP2; phân tích baseline và trace, thiết kế 2–3 cổng phòng ngừa trong CP3; sửa cổng theo thẻ sự cố đã bốc và thêm monitor ở CP4. Phụ trách ghi trực tiếp `lab10/guards.py` và `lab10/monitors.py`; gửi run ID, trace và nội dung kỹ thuật cho trưởng nhóm tích hợp vào các phiếu.

### Đóng góp cụ thể

Hiện thực cổng vòng 1 và S5 trong `lab10/guards.py`: kiểm tra ledger, dự báo chi phí trước khi gọi LLM và chuyển sớm ca cần approval. Thêm monitor `llm_cost_max_per_ticket_vnd`. Dò trace hoàn trùng/ticket dài; review `36d1747`, xác nhận S5-02/20 bị từ chối, S5-21 hoàn phần thiếu 12.000đ, S5-70 chuyển người trước LLM; public tests 13/13 và bộ nền không có ca mới hỏng.

### Bằng chứng

Commit S5 `a56d7b5` trên `tuyen/guards-s5`, tích hợp qua `ff50974`. Review `36d1747` được ghi tại Phiếu C C12; Tuyên cung cấp eval `R-S5-after-20261118-195116-f084e2` và grade `R-S5-grade-20261118-195151-f084e2` với lưu ý integrity. Grade cuối trên clone chuẩn `R-S5-grade-20261118-215041-4fa077` xác nhận integrity/visible/regression/monitor xanh; hash code khác nhau nên không coi hai lượt là cùng bytes.

### Exit ticket

Chờ Tuyên xác nhận nội dung tự đánh giá. Gợi ý theo công việc thực tế (chưa phải lời tự khai): điều học được — chống hoàn trùng phải xét quyền lợi còn lại để không chặn hoàn một phần hợp lệ; điều còn chưa chắc — ledger đồng bộ chậm và xử lý đồng thời ảnh hưởng cổng thế nào.

### Sử dụng AI

Chờ Tuyên xác nhận có dùng AI hay không; nếu có, ghi công cụ, phần hỗ trợ và cách tự kiểm chứng. Chưa có lời xác nhận cá nhân trong bàn giao.

## DoHoangPhuc-2A202603652

### Phần việc phụ trách

Vai Vận hành và pháp lý. Phụ trách câu 1.2 và 1.4 (Phiếu A mục A1/A2), duyệt 5 ngưỡng vận hành/pháp lý và ranh giới đầu ra (Phiếu A mục A4), câu 2.4 và 2.10 (Phiếu B mục B4 HAZOP vòng 1, B5 checklist 9 nhóm có PIC, B7.5–B7.6 Runbook phần 1–3 và Giờ cao điểm), đề xuất mục `operations` và `legal` cho `config/operating_gates.json`, phần điều tra sự cố/risk register/runbook phần 4–5 ở Phiếu C, và điền `submission/submission.json` cuối buổi.

### Đóng góp cụ thể

Hoàn thành mục tiêu nhìn từ kế toán đối soát (`NV-OANH`) và trưởng ca CSKH (`NV-HANH`), thiết kế telemetry production phát hiện tác hại ra bên ngoài LogiX, kiểm tra công suất ca trực/SLA/PII/chi phí để duyệt ngưỡng trong `config/acceptance_criteria.json` trước khi ký. Ở vòng 1, thực hiện HAZOP mở rộng (kỹ thuật trên `file_carrier_fault` và 4 thành phần ngoài kỹ thuật), lập checklist go-live 9 nhóm có PIC, soạn Runbook phần 1–3, phương án Giờ cao điểm và đề xuất cấu hình `operations`/`legal` theo `data/world.json`. Với S5, soạn bàn giao vận hành/pháp lý: HAZOP, risk register, runbook phần 4–5 và đề xuất operations/legal; nội dung được Tùng tích hợp vào Phiếu C và config. Review bản `36d1747`, đồng ý cấu hình, quy trình ledger hai kênh, runbook giữ nguyên switches.json và quyết định v2 Tiếp tục bốn kho bán lẻ. Tùng hoàn thiện submission.json và gom hồ sơ cuối.

### Bằng chứng

Commit `9fc347d` (nhánh `phuc/form-a`) / `e17778b` (trên `main`) cho Câu 1.2 và 1.4 tại `templates/form-a-criteria.md`; nhánh `phuc/ops-round1` cho các mục `B4`, `B5`, `B7.5–B7.6` tại `templates/form-b-evaluation-gates.md` và đề xuất `operations`/`legal` cho `config/operating_gates.json`. Commit `359091e` trên `phuc/ops-s5` tạo `docs/s5_ops_handoff.md`, tích hợp qua `b433549`. Review v2 được ghi tại C12; Phúc duyệt theo `R-S5-grade-20261118-173600-4fa077`, sau đó grade cuối `R-S5-grade-20261118-215041-4fa077` xác nhận bản nộp đạt PASS-VISIBLE và integrity xanh.

### Exit ticket

- Một điều học được: Phải tách chi phí theo từng kho/phân khúc (kho sỉ HCM-B2B lỗ dù model chạy đúng) và kiểm soát hoàn lặp chéo kênh (CSKH hoàn tay + AI) kèm trần LLM trước khi đọc.
- Một điều còn chưa chắc: Độ trễ đồng bộ sổ cái hoàn tay giữa CSKH và trợ lý ngoài thực tế, cũng như tải duyệt giờ cao điểm khi mở pilot 4 kho bán lẻ.

### Sử dụng AI

Chờ Phúc xác nhận có dùng AI hay không; nếu có, ghi công cụ, phần hỗ trợ và cách tự kiểm chứng. Chưa có lời xác nhận cá nhân trong bàn giao.
