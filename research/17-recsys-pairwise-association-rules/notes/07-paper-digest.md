# Tóm tắt có cấu trúc của bài báo (từ toàn văn)

Số hiệu mục, bảng, thuật toán, hình đều theo bài báo.

## Mục 1–2: Vấn đề và công trình liên quan
- Collaborative filtering và content-based filtering cần hồ sơ người dùng hoặc mô tả mặt hàng, và lịch sử dài. Khi thiếu thì gặp cold start.
- Có những bối cảnh người dùng ẩn danh, dữ liệu nhạy cảm, hoặc mỗi người chỉ dùng hệ thống ít lần (khảo sát dinh dưỡng). Khi đó không xây được mô hình cá nhân.
- Shaw, Xu, Geva (2010) dùng association rules cho cold start. Pazzani và Billsus coi danh sách chủ đề sách người dùng bình chọn là giao dịch.
- Bài nêu bốn khó khăn khi dùng association rules cho khuyến nghị: số luật rất lớn khi muốn gợi ý cụ thể; ghép tập món đầu vào với antecedent có thể không ra luật nào; một món có thể là consequent của nhiều luật nên cần hàm gộp điểm; ngưỡng support thường đặt cao để danh sách luật đọc được, trong khi khuyến nghị cần cả luật hiếm.
- Roth và cs. (2010) đề xuất implicit social graph cho gợi ý người nhận email. DuMouchel và Pregibon (2001) gợi ý tìm cặp thường đi cùng trước, rồi mới xét tập lớn hơn. Raeder và Chawla (2011) phân tích đồ thị món–món có trọng số.

## Mục 3: Ba thuật toán
- Đầu vào: IF (foods đã chọn). Đầu ra: RF (danh sách món gợi ý có điểm). IF bị loại khỏi RF.
- **AR** (Alg. 1): luật `antecedent ⇒ consequent` với consequent là một món. Với mỗi luật có consequent ∉ IF và antecedent giao IF khác rỗng: `RF[f] += confidence × ms`, `ms = |ant ∩ IF|² / (|ant| × |IF|)`.
- **TIC** (Alg. 2–3): chuẩn hoá các bữa thành tập bữa duy nhất; `TM[m,f]` là xác suất có f khi đã có phần còn lại của bữa m; gợi ý cộng `|m ∩ IF| × TM[m,f]` trên mọi bữa m giao IF.
- **PAR** (Alg. 4–5): huấn luyện chỉ đếm `OD[f]` (số bữa chứa f) và `CD[f,f1]` (số bữa chứa cả hai). Gợi ý: với mỗi món đầu vào, lấy các cặp chứa nó; `p = CD/OD[inf]`; gộp `RF[f] = sum(P) × sum(W)` với `W = OD[inf]`.
- Lý do dùng trọng số W (tác giả giải thích): nếu chỉ cộng xác suất sẽ mất thông tin món gợi ý đã từng đi cùng bao nhiêu món đầu vào, và món đầu vào phổ biến hơn nên có tín hiệu đáng tin hơn.
- Ví dụ của bài: dữ liệu {abcd, ade, de, ab}, IF = {a,b}. AR cho d 2,50; c 1,96; e 0,29. TIC cho d 3,00; c 2,00; e 0,50. PAR cho d 5,8; c 4,2; e 1. Tất cả đã được tái hiện bằng mã trong `code/verify_paper_examples.py`.
- Chỗ không nhất quán: pseudocode Alg. 2 dòng 9 viết `cf/cm`, còn bảng ví dụ và lời giải thích đều ứng với `cm/cf`. Mã dùng `cm/cf`.

## Mục 4: Phương pháp đánh giá
- 20.000 bữa ăn lấy ngẫu nhiên, mỗi bữa ≥ 2 món, người tham gia ở Anh, 2014–2018; thứ tự món trong bữa được xáo ngẫu nhiên.
- 10-fold cross validation; mô hình huấn luyện trên 9 phần, thử trên phần còn lại.
- Mỗi bữa kiểm thử: lấy mẫu một số món làm đầu vào (từ 1 đến 5), các món còn lại (ít nhất một) là món "bị bỏ sót".
- Đo recall (phần trăm dự đoán đúng so với tổng số món người dùng chọn), precision, nDCG@15; xét top 15 gợi ý (chọn 15 vì hơi lớn hơn số kết quả đa số người dùng xem).
- AR dùng FP-growth song song trong Apache Spark; min support và min confidence đặt bằng giá trị nhỏ nhất vẫn chạy xong trong 5 phút (3×10⁻⁴ sau corrigendum). Máy chạy: Mac Pro 2,9 GHz Intel Core i5, 16 GB.

## Mục 5: Kết quả
- 5.1 PAR cho diện tích dưới đường PR lớn nhất, tăng theo số món đầu vào, và nDCG cao hơn TIC và AR ở mọi cỡ đầu vào (Hình 1–3; bài không nêu số). Thời gian (Bảng 4, ms): huấn luyện AR 3905,1; PAR 6904,9; TIC 93710,2. Gợi ý trung bình: AR 39,5; PAR 2,5; TIC 32,0. Tác giả chọn PAR; đồng thời nhận xét chất lượng còn thấp.
- 5.2 So với prompt nhập tay: prompt nhập tay chỉ nhận ra tối đa 8,3% món bị bỏ sót; PAR đạt recall đỉnh 58,0% (nhóm cha trực tiếp) và 79,1% (nhóm cha cấp hai). Gợi ý theo nhóm món cũng giúp xử lý món chưa ai khai báo (cold start ở mức món). Bảng 5 liệt kê các ví dụ món hay quên mà prompt nhập tay chưa phủ.
- 5.3 Xếp hạng tìm kiếm: PAR thay cho FRC cho nDCG cao hơn một chút từ cỡ đầu vào 2, khoảng cách tăng dần.

## Mục 6: Kết luận của tác giả
Thuật toán không cần hồ sơ cá nhân hay lịch sử dài; PAR hoạt động tốt nhất trong ba cách; recall 79,1% so với 8,3% của prompt nhập tay; chỉ đánh giá trên dữ liệu người dùng ở Anh, sẽ xét ảnh hưởng của đặc điểm vùng; phương pháp áp dụng được cho các bài toán khác (ví dụ gợi ý người nhận email, gợi ý tag).

## Bài kiểm chứng arXiv 1903.12264
- Thiết kế: hai khảo sát, so sánh prompt nhập tay với prompt do PAR sinh ra. Gợi ý PAR hiển thị dạng checkbox ở cuối mỗi bữa, tối đa 15 món.
- Khảo sát 1: 50 người tham gia (1 người rút lui giữa chừng), 5 ngày liên tiếp (Thứ Hai đến Thứ Sáu), hai nhóm đổi chiều (hand-coded 3 ngày đầu, n = 19; hand-coded 2 ngày cuối, n = 30); dữ liệu thứ Hai bỏ để giảm hiệu ứng làm quen. 96 recall dùng hand-coded và 97 recall dùng generated.
- Khảo sát 2 (chiến dịch Newcastle Can): 91 người, 77 nữ, 14 nam, tuổi 18–82; một tuần dùng hand-coded, một tuần dùng generated. 133 và 119 recall.
- Kết quả KS1: tỉ lệ recall có nhận ít nhất một món: 66% (hand-coded, 57/86) và 63% (generated, 61/97); số món chấp nhận mỗi recall: 1,1 và 2,3 (P < 0,001); precision: 24% và 2%.
- Kết quả KS2: tỉ lệ recall nhận ít nhất một món: 50% (61/122) và 72% (83/115); số món chấp nhận trung bình: 1,5 và 2,1 (P = 0,002); precision: 16% và 2%.
- Số món khác nhau được chấp nhận: KS1 15 (9% trong 164) và 30 (18% trong 165); KS2 16 (9% trong 186) và 35 (19% trong 189).
- Năng lượng trung bình báo cáo: KS1 1911,8 và 1790,6 kcal (P = 0,159); KS2 1461,7 và 1545,7 kcal (P = 0,02). Thời gian hoàn thành recall: 15,9 và 13,3 phút (P = 0,108); 15,9 và 16,3 phút (P = 0,297).
- Hạn chế do tác giả nêu: hai kiểu prompt khác cách trình bày (câu hỏi lúc nhập món so với danh sách sau bữa); mô hình huấn luyện trên dữ liệu thu khi đã có prompt nhập tay; không xác minh người dùng có thật sự ăn các món đã chấp nhận; precision thấp vì danh sách dài.
- Hướng tiếp theo do tác giả nêu: đưa tỉ lệ chấp nhận (acceptance rate) vào mô hình để rút ngắn danh sách; hơn một nửa món mô hình bắt được chưa có trong cơ sở dữ liệu prompt nhập tay.

## Điều chỉnh so với bản nháp đầu của tiểu luận
1. Bản nháp mô tả PAR như một mô hình đơn lẻ với các hàm gộp điểm tự đặt (max, sum, noisy-or, lift). Bài báo thực ra so sánh ba thuật toán và dùng một công thức gộp cụ thể (`sum(P) × sum(W)`).
2. Bản nháp gán ngưỡng 3×10⁻⁴ cho PAR; thực tế ngưỡng đó áp dụng cho AR.
3. Bản nháp nói kích thước dữ liệu và độ đo "chưa biết"; nay đã có (20.000 bữa; nDCG@15, PR curve; recall 8,3% / 58,0% / 79,1%).
4. Bản nháp dùng item-based CF làm baseline thực nghiệm; bài báo không có baseline này. Thực nghiệm tự thực hiện được làm lại theo đúng ba thuật toán của bài.
