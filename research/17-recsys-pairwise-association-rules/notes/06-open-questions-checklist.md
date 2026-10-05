# Danh sách đối chiếu (đã xử lý sau khi có toàn văn)

| Câu hỏi ban đầu | Trả lời từ toàn văn |
|---|---|
| Công thức xếp hạng của PAR | `RF[f] = sum(P[f]) × sum(W[f])`; P là các xác suất có điều kiện `CD[in,f]/OD[in]`, W là các tần suất `OD[in]` của món đầu vào (Algorithm 5; arXiv viết lại thành `R_f = C_f × W_f`) |
| Có dùng ngưỡng support/confidence, lift không | PAR không dùng. Ngưỡng 3×10⁻⁴ (sau corrigendum) chỉ dành cho AR |
| Kích thước dữ liệu | 20.000 bữa ăn, mỗi bữa ≥ 2 món, người tham gia ở Anh, 2014–2018 |
| Giao thức đánh giá | 10-fold cross validation; lấy 1–5 món làm đầu vào, phần còn lại là món bị bỏ sót; top 15; PR curve, nDCG@15 |
| Thuật toán so sánh | AR (FP-growth, Spark), TIC (chuyển thể từ implicit social graph của Roth và cs.), PAR |
| Kết quả định lượng | Có: Bảng 4 (thời gian), 8,3% so với 58,0% và 79,1% recall; PR/nDCG chỉ có ở hình, bài không nêu số |
| "Ranking task" | Xếp hạng kết quả tìm kiếm món ăn: PAR thay cho FRC (food report count) |
| Hạn chế do tác giả nêu | Chỉ đánh giá trên dữ liệu người dùng ở Anh; chất lượng PAR vẫn thấp ở bước đầu và được cải thiện bằng cách dùng taxonomy |
| Số liệu của bài arXiv | Có đầy đủ, xem `07-paper-digest.md` |

Còn lại [CẦN BỔ SUNG] nếu giảng viên yêu cầu: độ lớn khoảng giá trị đọc từ các hình PR/nDCG (bài không ghi số), vì cần đo trực tiếp trên hình.
