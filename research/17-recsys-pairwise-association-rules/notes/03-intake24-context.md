# Bối cảnh ứng dụng: Intake24

**Intake24** là hệ thống hồi tưởng khẩu phần ăn 24 giờ (24-hour dietary recall) trực tuyến, mã nguồn mở, người trả lời tự điền, dựa trên quy trình *multiple-pass* (nhiều lượt nhắc để người dùng nhớ lại đủ món). [V]

## Thông tin đã xác minh

- Phát triển ban đầu tại Newcastle University với kinh phí từ cơ quan thực phẩm Scotland (Food Standards Scotland / Food Standards Agency, Scotland), thiết kế cho nhóm 11–24 tuổi; nay được duy trì cùng Cambridge và Monash. [V]
- Nhóm tác giả gồm các thành viên Human Nutrition Research Centre và Digital Interaction Group (Open Lab), trùng với nhóm tác giả bài báo. [V]
- Cơ sở dữ liệu hơn 2500 món ăn và hơn 2500 ảnh khẩu phần; hệ thống có nhiều **prompt** nhắc món "hay bị quên" và "hay ăn cùng nhau". [V]
- Phát triển lặp qua 4 vòng thử nghiệm người dùng, kết hợp phỏng vấn recall bởi người phỏng vấn để phát hiện món hay bị bỏ sót. [V]
- Thử nghiệm thực địa (Rowland và cs., *Nutrients* 2018): khoảng 60% (n = 230) người đồng ý tham gia hoàn thành ít nhất một recall, khoảng 50% (n = 195) hoàn thành từ hai recall trở lên; khó khăn chính được báo cáo là tìm món trong cơ sở dữ liệu. [V]

## Vì sao đây là bài toán hợp với luật kết hợp theo cặp

| Đặc điểm của Intake24 | Hệ quả cho thuật toán |
|---|---|
| Người dùng đăng nhập không đều, nhiều khảo sát chỉ một hai lần | Không có lịch sử cá nhân dài, lọc cộng tác bị cold start |
| Dữ liệu là **giao dịch**: tập món đã chọn trong một recall | Phù hợp trực tiếp với mô hình giỏ hàng (basket) của luật kết hợp |
| Không có rating, chỉ có "đã ăn món này" | Dữ liệu nhị phân ngầm định (implicit, binary) |
| Quyền riêng tư dữ liệu ăn uống nhạy cảm | Mô hình tập thể không cần hồ sơ cá nhân |
| Cần nhắc món bị quên dựa trên vài món đã chọn | Ngữ cảnh ngắn: luật theo cặp (1 món gợi ý món khác) tính nhanh theo thời gian thực |
| Trước đây prompt do nutritionist viết tay | Cần tự động hoá, dễ cập nhật theo dữ liệu mới |

Bài kiểm chứng đi kèm (arXiv 1903.12264) cho thấy prompt sinh tự động **bắt được nhiều món bị quên hơn** prompt viết tay nhưng **độ chính xác thấp hơn đáng kể**. [V, định tính]

## Công trình sau đó của nhóm

Progressive 24-hour recall (JMIR 2020): cho phép thêm nhiều recall nhỏ trong ngày; 33 người tham gia; 65% cho biết nhớ tốt hơn về nội dung bữa ăn và khẩu phần; cải thiện độ chính xác ở mức nhỏ. [V]
