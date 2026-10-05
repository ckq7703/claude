# Nhật ký nguồn và truy vấn

Ngày thực hiện: 2026-10-05. Công cụ khả dụng: tìm kiếm web (WebSearch). Truy cập trực tiếp (WebFetch, curl) tới nhà xuất bản, DOI, Crossref, OpenAlex, Semantic Scholar, arXiv, kho ePrints Newcastle, Monash, trang SPMF... đều bị proxy mạng chặn (`EGRESS_BLOCKED` hoặc `CONNECT tunnel failed 403`). Do đó mọi thông tin dưới đây đến từ kết quả tìm kiếm (tiêu đề, đoạn tóm tắt, metadata).

## A. Nguồn chính về bài báo (đã xác minh bằng nhiều kết quả độc lập)

| Nguồn (URL xuất hiện trong kết quả) | Thông tin lấy được | Mức |
|---|---|---|
| ScienceDirect, `https://www.sciencedirect.com/science/article/pii/S095741741830441X` | Trang bài báo gốc (chỉ thấy qua kết quả tìm kiếm) | V |
| Monash, `https://research.monash.edu/en/publications/recommender-system-based-on-pairwise-association-rules/` | Bản ghi công bố, tóm tắt | V |
| Mendeley catalogue `https://www.mendeley.com/catalogue/7a858336-aae3-3776-922f-b307f63bcbc7/` | Tóm tắt, metadata | V |
| SciSpace `https://scispace.com/papers/recommender-system-based-on-pairwise-association-rules-391ohavvbj` | Tóm tắt, ghi nhận bản open access | V |
| ResearchGate `https://www.researchgate.net/publication/327151706_Recommender_system_based_on_pairwise_association_rules` | Bản ghi bài báo | V |
| SCIRP reference `https://www.scirp.org/reference/referencespapers?referenceid=3162574` | Trích dẫn: ESWA 115, 535–542 | V |
| Newcastle ePrints (corrigendum) `https://eprints.ncl.ac.uk/258166` | Tiêu đề corrigendum: "Corrigendum to 'Recommender system based on pairwise association rules' [Expert Systems With Applications 115 (2018) 535–542]"; sửa tham số min support / min confidence từ 3×10^4 thành 3×10^-4 | V |
| DataLearner `https://datalearner.com/academic/journal-papers/0957-4174/volumes-and-issues/319/paper-detail/14674` | Metadata: DOI 10.1016/j.eswa.2018.07.077 | V |

## B. Công trình đi kèm của cùng nhóm tác giả

| Nguồn | Thông tin | Mức |
|---|---|---|
| arXiv 1903.12264 `https://arxiv.org/abs/1903.12264` | "Validation of a recommender system for prompting omitted foods in online dietary assessment surveys": so sánh prompt do thuật toán sinh với prompt nutritionist viết tay trong hai nghiên cứu; thuật toán bắt được nhiều món bị quên hơn nhưng độ chính xác thấp hơn đáng kể | V (tóm tắt) |
| JMIR 2020 `https://jmir.org/2020/2/e13266` | "Progressive 24-Hour Recall…": 33 người tham gia, 65% nhớ tốt hơn với progressive recall | V |
| Open Lab Newcastle `https://openlab.ncl.ac.uk/people/timur-osadchiy` | Timur Osadchiy là cựu thành viên Open Lab | V |

## C. Intake24 (bối cảnh ứng dụng)

| Nguồn | Thông tin | Mức |
|---|---|---|
| `https://intake24.abudhabi.nyu.edu` (trang giới thiệu, tính năng) | Hệ thống mở, tự điền, multiple-pass 24h recall; hơn 2500 món, hơn 2500 ảnh khẩu phần; prompt cho món hay quên và hay ăn cùng nhau | V |
| PMC6266941 "Field Testing of the Use of Intake24" (Rowland và cs., Nutrients 2018) | Thử nghiệm thực địa tại Scotland; ~60% (n=230) hoàn thành ≥ 1 recall, ~50% (n=195) hoàn thành ≥ 2 | V |
| PMC4924199, `Intake24-Development.pdf`, `Intake24-Comparison.pdf` | Bài về phát triển và so sánh Intake24 (chỉ thấy tiêu đề) | một phần |

## D. Công trình liên quan được dùng làm cơ sở lý thuyết

| Công trình | Xác minh |
|---|---|
| Agrawal, Imielinski, Swami (SIGMOD 1993, tr. 207–216) | V, kết quả tìm kiếm nêu trang và hội nghị |
| Brin, Motwani, Ullman, Tsur (SIGMOD 1997) | V; luật "implication", lift, conviction |
| Han, Pei, Yin, FP-growth (SIGMOD 2000) | V |
| Sarwar, Karypis, Konstan, Riedl, "Analysis of recommendation algorithms for e-commerce" (2000) | V (năm, tác giả, nội dung); trang chưa xác minh |
| Sarwar và cs., item-based CF (WWW10, 2001, tr. 285–295) | V |
| Linden, Smith, York (IEEE Internet Computing 7(1), 2003, tr. 76–80) | V |
| Lin, Alvarez, Ruiz (DMKD 6(1), 2002, tr. 83–105) | V |
| Schein, Popescul, Ungar (SIGIR 2002, tr. 253–260) | V |
| Cremonesi, Koren, Turrin (RecSys 2010, tr. 39–46) | V |
| Feremans & Goethals, RuleRec (Springer chapter) | V (tóm tắt) |
| Luận văn HCMIU "Applying Pairwise Association Rules For Recommendation" (`https://keep.hcmiu.edu.vn/handle/123456789/4563`) | V (tóm tắt) |
| Agrawal & Srikant, Apriori (VLDB 1994) | không truy vấn trực tiếp; trích theo kiến thức chuẩn [K], không ghi trang |

## E. Những gì KHÔNG xác minh được

- Toàn văn bài báo: công thức xếp hạng chính xác, kích thước tập dữ liệu Intake24 dùng trong bài, các độ đo đánh giá cụ thể và số liệu kết quả.
- Số liệu cụ thể trong bài arXiv 1903.12264 (chỉ có kết luận định tính).
- Phần Related work của bài báo gốc.
Xem `06-open-questions-checklist.md` để biết cần đối chiếu những gì khi có bản đầy đủ.
