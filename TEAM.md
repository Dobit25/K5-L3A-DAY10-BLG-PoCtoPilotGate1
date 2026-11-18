# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): `BLG`
- Lớp: `L3A`
- Repo của bàn: `K5-L3A-DAY10-BLG-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8): Chưa bốc

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

Chuẩn bị mục tiêu cấp hệ thống và bản tiêu chí trước khi đo, dựa trên eval card/PRD v1.1 Lab 9 cùng `data/world.json` của Lab 10. Tích hợp đề xuất kỹ thuật của Giáp Mạnh Tuyên và đề xuất vận hành/pháp lý của Đỗ Hoàng Phúc vào phiếu và config dùng chung; điều phối ký tiêu chí, chạy các mốc đánh giá, chốt cổng vòng 1, tổng hợp quyết định Gate 1 có run ID. Nội dung về kết quả eval và quyết định sẽ bổ sung sau khi có report thực tế.

### Bằng chứng

Phiếu A tại `templates/form-a-criteria.md`; tiêu chí tại `config/acceptance_criteria.json` đã ký trước lần eval đầu. Commit ký: `b5ef4b58a135812b56007c3a5705d9a0a362db74`; hash tiêu chí: `63eef882317d0ade80c4bfcb9c952a650a16a50d8c9f41662980de697cf76599`. Baseline `R-base-before-20261118-160604-bde05c` (bộ `base`, mốc `base`): pass_rate 0,9909; pass_k 0,9545; hoàn oan 20.000 đồng và 1 lỗi hãng oan ở `T-002@55`; gate exit 1 vì hai ngưỡng an toàn. Trace `T-002@55`: khách khai trễ 5 ngày, tracking DB ghi 2 ngày, sự kiện `model_override` dẫn tới hoàn 20.000 đồng và ghi lỗi hãng oan. Bổ sung hash checkpoint và các run sau đúng mốc của đề.

### Exit ticket

Tùng tự ghi một điều học được và một điều còn chưa chắc sau buổi lab; chưa thể điền trước khi thực hiện và demo.

## GiapManhTuyen-2A202603648

### Phần việc phụ trách

Kỹ sư cổng. Theo kế hoạch nhóm: kiểm tra code/CLI ở CP1; đề xuất cách tính metric ở CP2; phân tích baseline và trace, thiết kế 2–3 cổng phòng ngừa trong CP3; sửa cổng theo thẻ sự cố đã bốc và thêm monitor ở CP4. Phụ trách ghi trực tiếp `lab10/guards.py` và `lab10/monitors.py`; gửi run ID, trace và nội dung kỹ thuật cho trưởng nhóm tích hợp vào các phiếu.

### Đóng góp cụ thể

Chưa ghi nhận; cập nhật sau khi hoàn thành các phần việc trong buổi lab.

### Bằng chứng

Chưa có mã commit, mã lần chạy (`runs/<mã>`) hoặc dòng phiếu được xác nhận; bổ sung sau khi thực hiện.

### Exit ticket

Điền sau buổi lab: một điều học được và một điều còn chưa chắc.
