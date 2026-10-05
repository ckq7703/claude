# Thông tin bài báo (đối chiếu với bản PDF)

| Trường | Giá trị |
|---|---|
| Tiêu đề | Recommender system based on pairwise association rules |
| Tác giả | Timur Osadchiy, Ivan Poliakov, Patrick Olivier, Maisie Rowland, Emma Foster |
| Đơn vị | Osadchiy, Poliakov, Olivier: Open Lab, School of Computing, Newcastle University. Rowland, Foster: Institute of Health and Society, Newcastle University. Trong corrigendum, Olivier ghi thêm Monash University |
| Tạp chí | Expert Systems With Applications, tập 115 (2019), trang 535–542 |
| Mốc thời gian | Nhận 04/04/2018; sửa 09/07/2018; chấp nhận 10/07/2018; online 21/08/2018 |
| DOI | 10.1016/j.eswa.2018.07.077 |
| Từ khoá (do tác giả nêu) | Association rules; Cold-start problem; Data mining; Ontologies; Recommender systems |
| Giấy phép | CC BY 4.0 |
| Corrigendum | DOI 10.1016/j.eswa.2019.05.022 |

## Corrigendum, nói đúng phạm vi

Câu bị in sai nằm ở Mục 4: "To gather as many association rules as possible we set both the minimum support and the minimum confidence to the lowest value (3 × 10⁴)…". Giá trị đúng là 3 × 10⁻⁴. Corrigendum giải thích lỗi xuất hiện khi chuyển từ LaTeX sang PDF.

Câu này nói về thuật toán **AR** (khai phá bằng FP-growth trong Apache Spark), không phải PAR. PAR không dùng ngưỡng support hay confidence. Bản nháp đầu của tiểu luận gán nhầm ngưỡng này cho PAR và đã được sửa.

## Trích dẫn

Osadchiy, T., Poliakov, I., Olivier, P., Rowland, M., & Foster, E. (2019). Recommender system based on pairwise association rules. *Expert Systems with Applications, 115*, 535–542. https://doi.org/10.1016/j.eswa.2018.07.077

Osadchiy, T., Poliakov, I., Olivier, P., Rowland, M., & Foster, E. (2019). Corrigendum to "Recommender system based on pairwise association rules" [Expert Systems with Applications 115 (2018) 535–542]. https://doi.org/10.1016/j.eswa.2019.05.022

Osadchiy, T., Poliakov, I., Olivier, P., Rowland, M., & Foster, E. (2019). Validation of a recommender system for prompting omitted foods in online dietary assessment surveys. arXiv:1903.12264.
