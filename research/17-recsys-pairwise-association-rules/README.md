# Đề tài 17 (2018): Recommender system based on pairwise association rules

Thư mục tổng hợp toàn bộ dữ liệu nghiên cứu cho tiểu luận môn Khai phá dữ liệu (Data Mining).

| Mục | Nội dung |
|---|---|
| Đề tài | Recommender system based on pairwise association rules |
| Tác giả | Timur Osadchiy, Ivan Poliakov, Patrick Olivier, Maisie Rowland, Emma Foster |
| Công bố | *Expert Systems with Applications*, vol. 115, pp. 535–542 (online 2018, số tạp chí 2019), DOI `10.1016/j.eswa.2018.07.077` |
| Nhóm kỹ thuật | Association Rule Mining |
| Ứng dụng | Recommender Systems using Association Rules |

## Cấu trúc thư mục

```
research/17-recsys-pairwise-association-rules/
├── README.md                      (tệp này)
├── report/
│   └── TIEU-LUAN-recsys-pairwise-association-rules.md   ← TIỂU LUẬN CHÍNH
├── notes/
│   ├── 01-source-log.md           nhật ký truy vấn và nguồn, nêu rõ cái gì xác minh được và cái gì không
│   ├── 02-paper-metadata.md       thông tin chính thức của bài báo, corrigendum, BibTeX
│   ├── 03-intake24-context.md     bối cảnh hệ thống Intake24 (nơi bài báo được áp dụng)
│   ├── 04-theory-association-rules-recsys.md   lý thuyết: luật kết hợp, độ đo, hệ khuyến nghị, cold start, đánh giá top-N
│   ├── 05-related-work-and-citations.md        bảng công trình liên quan đã xác minh trích dẫn
│   └── 06-open-questions-checklist.md          các điểm cần đối chiếu với bản đầy đủ của bài báo
├── code/
│   ├── par_recommender.py         cài đặt minh hoạ bộ khuyến nghị luật kết hợp theo cặp (PAR) và 2 baseline
│   ├── synthetic_data.py          sinh dữ liệu "bữa ăn" tổng hợp có cấu trúc kết hợp đã biết
│   ├── run_experiment.py          chạy thực nghiệm (so sánh, kích thước ngữ cảnh, ngưỡng, kích thước tập huấn luyện)
│   ├── make_figures.py            vẽ biểu đồ và xuất danh sách luật hàng đầu
│   └── worked_example.py          ví dụ tay 6 bữa ăn dùng trong tiểu luận
└── results/
    ├── results.csv  dataset_summary.json  top_rules_by_lift.csv  worked_example.txt
    └── fig1_model_comparison.png  fig2_context_size.png  fig3_training_size.png
```

## Phạm vi và độ tin cậy (đọc trước khi dùng)

1. **Không đọc được toàn văn bài báo.** Mạng của môi trường làm việc chặn các trang nhà xuất bản, kho lưu trữ và arXiv; chỉ công cụ tìm kiếm web hoạt động. Vì vậy nội dung về bài báo gốc giới hạn ở những gì xác minh được qua các bản tóm tắt, trang metadata và các công trình liên quan (xem `notes/01-source-log.md`).
2. **Không tái lập số liệu của bài báo.** Dữ liệu Intake24 không công khai. Phần thực nghiệm trong thư mục này dùng dữ liệu tổng hợp tự sinh, chỉ để minh hoạ ý tưởng; mã trong `code/` là cài đặt của học viên, không phải mã của nhóm tác giả.
3. Trong tiểu luận, mỗi khẳng định được gắn nhãn nguồn: **[V]** đã xác minh qua nguồn tìm được, **[K]** kiến thức giáo khoa chuẩn, **[S]** kết quả thực nghiệm tổng hợp của học viên.

## Chạy lại thực nghiệm

```bash
pip install numpy matplotlib
cd research/17-recsys-pairwise-association-rules/code
python3 run_experiment.py      # ghi results/results.csv và dataset_summary.json
python3 make_figures.py        # ghi các hình và top_rules_by_lift.csv
python3 worked_example.py      # ví dụ tay
```
