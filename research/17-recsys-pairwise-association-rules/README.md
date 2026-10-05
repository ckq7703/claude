# Đề tài 17 (2018): Recommender system based on pairwise association rules

Thư mục tổng hợp tư liệu và tiểu luận môn Khai phá dữ liệu cho đề tài trên.

| Mục | Nội dung |
|---|---|
| Bài báo | Osadchiy, Poliakov, Olivier, Rowland, Foster. *Expert Systems with Applications* 115 (2019), 535–542. DOI 10.1016/j.eswa.2018.07.077 |
| Nhóm kỹ thuật | Association Rule Mining |
| Ứng dụng | Recommender Systems using Association Rules |

## Cấu trúc

```
research/17-recsys-pairwise-association-rules/
├── report/TIEU-LUAN-recsys-pairwise-association-rules.md   tiểu luận chính
├── sources/        toàn văn bài báo (kèm corrigendum), bài kiểm chứng arXiv 1903.12264, bản văn bản trích ra
├── notes/          01 nhật ký nguồn · 02 thông tin xuất bản · 03 bối cảnh Intake24 · 04 lý thuyết
│                   05 tài liệu tham khảo · 06 danh sách đối chiếu · 07 tóm tắt có cấu trúc của bài báo
├── code/           paper_algorithms.py (AR, TIC, PAR) · verify_paper_examples.py · synthetic_meals.py
│                   run_paper_style_experiment.py · make_figures.py
└── results/        kết quả CSV/JSON của thực nghiệm, hình, kết quả kiểm tra ví dụ
```

## Lưu ý về độ tin cậy

- Nội dung về bài báo lấy từ toàn văn trong `sources/` (hai PDF do người dùng tải về). Bài chính có giấy phép CC BY 4.0.
- Các Bảng 1–3 của bài (ví dụ {abcd, ade, de, ab}) được tái hiện đúng bằng mã (`results/verify_paper_examples.txt`).
- Thực nghiệm trong `code/` chạy trên **dữ liệu bữa ăn tổng hợp** vì dữ liệu Intake24 không công khai. Kết quả chỉ minh hoạ giao thức, không thay cho số liệu của bài.
- Chỗ chưa có thông tin được đánh dấu `[CẦN BỔ SUNG]` trong tiểu luận.

## Chạy lại

```bash
pip install numpy matplotlib
cd research/17-recsys-pairwise-association-rules/code
python3 verify_paper_examples.py
python3 run_paper_style_experiment.py     # khoảng 1–2 phút
python3 make_figures.py
```
