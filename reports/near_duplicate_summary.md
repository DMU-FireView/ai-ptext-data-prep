# Near-duplicate 후보 요약

이 결과는 사람이 확인할 후보입니다. 유사도가 높다는 이유로 조작 리뷰, 광고 리뷰, SUSPICIOUS 또는 삭제 대상으로 자동 판단하지 않습니다.
상품 간 유사 후보는 향후 REPETITION / PRODUCT_COPY 검토에 참고할 수 있지만, 현재 단계에서는 패턴 라벨을 부여하지 않습니다.

- 입력 파일: raw/폼_Review_data.xlsx
- Reviews 유효 header 수: 2, 마지막 header: Excel 9행
- 공통 컬럼이 모두 빈 행 제외: 0행
- threshold: 0.85
- min_length: 15

| 항목 | 개수 |
| --- | ---: |
| 전체 리뷰 수 | 4711 |
| 유사도 분석 대상 리뷰 수 | 4650 |
| min_length로 제외된 리뷰 수 | 61 |
| content 빈값으로 제외된 리뷰 수 | 0 |
| content가 문자열이 아니어서 제외된 리뷰 수 | 0 |
| 분석 대상 중 추출 가능한 n-gram이 없는 리뷰 수 | 0 |
| near-duplicate pair 수 | 21 |
| normalized_exact pair 수 | 8 |
| 같은 상품 내 pair 수 | 7 |
| 서로 다른 상품 간 pair 수 | 14 |
| 상품 식별 불가 pair 수 | 0 |

## Similarity 구간별 개수

구간은 반올림 전 점수의 하한 이상·상한 미만입니다. 예: 0.85~0.89는 0.85 이상 0.90 미만을 뜻합니다.

| 구간 | pair 수 |
| --- | ---: |
| 0.85~0.89 | 1 |
| 0.90~0.94 | 9 |
| 0.95~0.99 | 3 |
| 1.00 | 8 |

## 계산 및 해석 기준

- 공통 컬럼 11개를 모두 가진 마지막 유효 header 이후만 읽습니다.
- 계산용 문자열에서만 연속 공백을 정리하고 양끝 공백을 제거합니다. 최소 길이는 이 문자열의 문자 수입니다.
- 소문자화 및 한글·영문·숫자·특수문자 제거는 하지 않습니다. 원문 content와 ID 값/타입은 유지합니다.
- TF-IDF: analyzer=char_wb, ngram_range=(3, 5), lowercase=False, norm=l2. cosine similarity를 사용합니다.
- 128행씩 sparse 유사도를 계산하며 전체 dense 유사도 행렬은 만들지 않습니다.
- 후보도 한 행씩 Excel에 기록하며 전체 pair 목록을 메모리에 누적하지 않습니다.
- raw content가 정확히 같은 pair는 제외합니다. 공백 차이 등으로 원문이 다르면 유사도 1.00 후보도 가능합니다.
- 부동소수점 오차를 고려해 1과의 차이가 1e-12 이하인 유사도는 1.00으로 처리합니다.
- 각 pair는 한 번만 기록하며 자기 자신과의 비교는 제외합니다. exact_duplicate는 항상 false입니다.
- normalized_exact는 원문은 다르지만 공백·줄바꿈 정리 후 동일한 리뷰를 뜻합니다. prepare_candidates의 계산용 문자열이 완전히 같을 때만 true입니다.
- normalized_exact는 진단용 필드이며 후보 필터링이나 자동 라벨링에 사용하지 않습니다.
- same_product는 (platform, product_id) 원본 값 비교입니다. 어느 쪽이든 키가 비면 Excel에는 빈값으로 기록하고 상품 식별 불가로 별도 집계합니다.
- 식별자 타입을 통일하지 않습니다. Python 비교에서 int와 float가 같게 처리될 수 있습니다.
- source_excel_row_a/b는 원본 Excel 행 번호이며 a/b 필드는 각 리뷰의 원본 값입니다.
- 수식 셀은 계산하지 않고 원본 수식 문자열로 읽습니다.
- 짧거나 비어 있는 content는 분석 대상에서만 제외하며 원본 행을 삭제하지 않습니다.
- 보고서에는 리뷰 본문을 싣지 않습니다. 원문은 로컬 결과 Excel에서 검토합니다.
