# Lý thuyết nền tảng

Nhãn: [K] kiến thức giáo khoa chuẩn; [V] đã xác minh qua nguồn tìm được.

## 1. Luật kết hợp (Agrawal, Imielinski, Swami, SIGMOD 1993 [V])

Cho tập mặt hàng I = {i1, …, im} và tập giao dịch D = {T1, …, Tn}, mỗi T ⊆ I. Luật kết hợp có dạng X → Y với X, Y ⊆ I, X ∩ Y = ∅.

| Độ đo | Công thức | Ý nghĩa |
|---|---|---|
| support(X) | \|{T : X ⊆ T}\| / n | tần suất xuất hiện |
| support(X → Y) | support(X ∪ Y) | độ phủ của luật |
| confidence(X → Y) | support(X ∪ Y) / support(X) = P(Y\|X) | độ tin cậy có điều kiện |
| lift(X → Y) | confidence / support(Y) = P(Y\|X) / P(Y) | >1: đi cùng nhau nhiều hơn ngẫu nhiên (Brin và cs. 1997 [V]) |
| conviction(X → Y) | (1 − support(Y)) / (1 − confidence) | luật có hướng, đo mức "sai" của luật (Brin và cs. 1997 [V]) |

Khai phá luật gồm hai bước: (1) tìm các tập phổ biến có support ≥ minsup; (2) sinh luật có confidence ≥ minconf. Tính chất **anti-monotone** của support (tập con của tập phổ biến cũng phổ biến) là cơ sở cắt tỉa của Apriori [K]. FP-growth (Han, Pei, Yin, SIGMOD 2000 [V]) tránh sinh ứng viên bằng cấu trúc FP-tree.

## 2. Luật theo cặp (pairwise)

Luật theo cặp là trường hợp **|X| = |Y| = 1**: a → b. Hệ quả [K]:

- Chỉ cần đếm **đồng xuất hiện của từng cặp**, không cần Apriori nhiều tầng: một lượt duyệt dữ liệu, độ phức tạp thời gian ≈ Σ|T|² trên các giao dịch, bộ nhớ tối đa O(m²) (thực tế thưa).
- Mô hình là một ma trận m × m (confidence hoặc lift) có thể tra cứu O(|ngữ cảnh|·m) khi khuyến nghị.
- Đánh đổi: không biểu diễn được tương tác bậc cao (a và b cùng nhau mới dẫn tới c).
- Cùng họ với item-to-item CF (Sarwar 2001, Linden 2003 [V]) ở chỗ cả hai đều dựa trên quan hệ **mặt hàng–mặt hàng**, nhưng luật có hướng và có độ đo xác suất diễn giải được (P(b|a)).

Các biến thể liên quan: khai phá luật với support thích nghi theo từng người dùng (Lin, Alvarez, Ruiz, DMKD 2002 [V]); các bộ khuyến nghị theo luật đa điều kiện và công cụ RuleRec (Feremans & Goethals [V]), trong đó "pairwise rule mining" được tổng quát hoá bằng chỉ mục đảo.

## 3. Hệ khuyến nghị và cold start

- **Lọc cộng tác** dựa trên lịch sử đánh giá của người dùng/mặt hàng; **lọc theo nội dung** dựa trên mô tả mặt hàng và hồ sơ người dùng; **lai** kết hợp cả hai [K].
- **Cold start**: người dùng hoặc mặt hàng mới thiếu dữ liệu (Schein, Popescul, Ungar, SIGIR 2002 [V]).
- Bài báo đang xét nhắm tới hệ thống dùng không đều, quyền riêng tư và ít chỉ báo sở thích: mô hình **tập thể** không cần dữ liệu cá nhân. [V]

## 4. Đánh giá top-N

- Cremonesi, Koren, Turrin (RecSys 2010 [V]): với bài toán top-N, các độ đo sai số như RMSE không phù hợp tự nhiên; nên dùng độ đo xếp hạng.
- Độ đo thường dùng [K]: Precision@N, Recall@N, Hit-rate@N, MRR, nDCG. Với bài toán "một món bị quên", Hit-rate@N chính là Recall@N.
- Trong bài kiểm chứng của nhóm tác giả: recall (bắt được nhiều món quên) cao hơn prompt thủ công nhưng precision thấp hơn đáng kể. [V, định tính]

## 5. Liên hệ giữa độ đo của luật và độ đo của khuyến nghị

| Độ đo luật | Vai trò khi khuyến nghị |
|---|---|
| support | lọc nhiễu: loại luật dựa trên quá ít giao dịch |
| confidence P(b\|a) | điểm khuyến nghị trực tiếp: xác suất b xuất hiện khi đã có a |
| lift | hiệu chỉnh thiên lệch phổ biến: tránh gợi ý món ai cũng ăn |
| conviction | xếp hạng theo độ "bất ngờ" khi b vắng mặt |
