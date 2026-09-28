# P_text training dataset v2 summary

모델 입력은 content만 사용합니다. provenance/ID/platform/synthetic_type/split은 모델 입력이 아닙니다.
v1·원본 리뷰·사람 라벨은 수정하지 않았습니다. 이 단계는 학습 실행이나 실제 positive 성능 검증이 아닙니다.

- seed: 42
- NORMAL exact 추가 중복 제거: 205행
- 보존 기준: 원문이 정확히 같을 때 human_candidate_review 우선, 동순위는 seed 42로 1행 결정. 별개 사용자의 동일한 표현일 수 있으며 위험 판정이나 원본 삭제를 뜻하지 않습니다.
- v1 synthetic 1350행은 사용하지 않고 새로 생성했습니다.

## total

| 항목 | 수 |
| --- | --- |
| total | 3098 |

## label

| 항목 | 수 |
| --- | --- |
| NORMAL | 1847 |
| SUSPICIOUS | 1251 |

## label_origin

| 항목 | 수 |
| --- | --- |
| sampled_non_candidate | 1451 |
| human_candidate_review | 396 |
| human_suspicious | 1 |
| synthetic | 1250 |

## synthetic_type

| 항목 | 수 |
| --- | --- |
| [real/empty] | 1848 |
| PRODUCT_DESCRIPTION_REPLACEMENT | 250 |
| NO_USE_ASSERTIVE_RECOMMENDATION | 250 |
| PROMOTIONAL_TEMPLATE | 250 |
| EXPERIENCE_FREE_CLAIM | 250 |
| COPY_VARIATION | 250 |

## platform

| 항목 | 수 |
| --- | --- |
| ohouse | 1900 |
| elevenst | 175 |
| oliveyoung | 1003 |
| musinsa | 20 |

## split

| 항목 | 수 |
| --- | --- |
| train | 2168 |
| test | 465 |
| validation | 465 |

## evaluation_set

| 항목 | 수 |
| --- | --- |
| training | 2168 |
| real_NORMAL_human | 118 |
| real_NORMAL_weak | 435 |
| synthetic_challenge | 377 |

## platform_x_label

| 항목 | 수 |
| --- | --- |
| ohouse &#124; NORMAL | 1046 |
| elevenst &#124; NORMAL | 115 |
| oliveyoung &#124; NORMAL | 669 |
| musinsa &#124; NORMAL | 17 |
| oliveyoung &#124; SUSPICIOUS | 334 |
| ohouse &#124; SUSPICIOUS | 854 |
| elevenst &#124; SUSPICIOUS | 60 |
| musinsa &#124; SUSPICIOUS | 3 |

## split_x_label

| 항목 | 수 |
| --- | --- |
| train &#124; NORMAL | 1294 |
| test &#124; NORMAL | 276 |
| validation &#124; NORMAL | 277 |
| train &#124; SUSPICIOUS | 874 |
| validation &#124; SUSPICIOUS | 188 |
| test &#124; SUSPICIOUS | 189 |

## split_x_label_origin

| 항목 | 수 |
| --- | --- |
| train &#124; sampled_non_candidate | 1016 |
| train &#124; human_candidate_review | 278 |
| test &#124; human_candidate_review | 59 |
| validation &#124; sampled_non_candidate | 218 |
| test &#124; sampled_non_candidate | 217 |
| validation &#124; human_candidate_review | 59 |
| train &#124; human_suspicious | 1 |
| train &#124; synthetic | 873 |
| validation &#124; synthetic | 188 |
| test &#124; synthetic | 189 |

## evaluation_set_x_split_x_label

| 항목 | 수 |
| --- | --- |
| training &#124; train &#124; NORMAL | 1294 |
| real_NORMAL_human &#124; test &#124; NORMAL | 59 |
| real_NORMAL_weak &#124; validation &#124; NORMAL | 218 |
| real_NORMAL_weak &#124; test &#124; NORMAL | 217 |
| real_NORMAL_human &#124; validation &#124; NORMAL | 59 |
| training &#124; train &#124; SUSPICIOUS | 874 |
| synthetic_challenge &#124; validation &#124; SUSPICIOUS | 188 |
| synthetic_challenge &#124; test &#124; SUSPICIOUS | 189 |

## platform × label × split

| platform / label / split | 수 |
| --- | --- |
| ohouse &#124; NORMAL &#124; train | 729 |
| ohouse &#124; NORMAL &#124; test | 158 |
| ohouse &#124; NORMAL &#124; validation | 159 |
| elevenst &#124; NORMAL &#124; test | 17 |
| elevenst &#124; NORMAL &#124; train | 81 |
| elevenst &#124; NORMAL &#124; validation | 17 |
| oliveyoung &#124; NORMAL &#124; test | 98 |
| oliveyoung &#124; NORMAL &#124; train | 472 |
| oliveyoung &#124; NORMAL &#124; validation | 99 |
| musinsa &#124; NORMAL &#124; train | 12 |
| musinsa &#124; NORMAL &#124; test | 3 |
| musinsa &#124; NORMAL &#124; validation | 2 |
| oliveyoung &#124; SUSPICIOUS &#124; train | 230 |
| ohouse &#124; SUSPICIOUS &#124; train | 600 |
| oliveyoung &#124; SUSPICIOUS &#124; validation | 51 |
| ohouse &#124; SUSPICIOUS &#124; test | 127 |
| ohouse &#124; SUSPICIOUS &#124; validation | 127 |
| elevenst &#124; SUSPICIOUS &#124; train | 42 |
| musinsa &#124; SUSPICIOUS &#124; train | 2 |
| oliveyoung &#124; SUSPICIOUS &#124; test | 53 |
| elevenst &#124; SUSPICIOUS &#124; test | 9 |
| elevenst &#124; SUSPICIOUS &#124; validation | 9 |
| musinsa &#124; SUSPICIOUS &#124; validation | 1 |

## Quality gate

| mandatory | 결과 |
| --- | --- |
| label_conflict_zero | PASS |
| group_leakage_zero | PASS |
| parent_leakage_zero | PASS |
| family_leakage_zero | PASS |
| cross_split_exact_zero | PASS |
| uncertain_zero | PASS |
| existing_validator | PASS |

| targets | 결과 |
| --- | --- |
| 선택_below_30pct | PASS |
| 구성_below_30pct | PASS |
| prefix_below_5pct | PASS |
| mean_length_gap_within_20pct | PASS |

- 선택 등장률: 0.00%
- 구성 등장률: 0.00%
- 유형 내 최빈 시작 구문 비율 (첫 3/4어절 중 최대): 4.00%
- 실제 NORMAL 대비 synthetic 평균 길이 차이: 3.15%
- parent 길이 대비 70~130% 범위: 1250/1250행
- parent 길이 비율 최소/최대: 0.7010/1.2927
- COPY_VARIATION family 최대 크기: 2

## 길이 분포

| 유형 | 수 | 평균 | 중앙값 | 최소 | 최대 |
| --- | --- | --- | --- | --- | --- |
| synthetic | 1250 | 124.91 | 102.0 | 55 | 530 |
| real_NORMAL | 1847 | 128.97 | 90 | 4 | 1327 |
| PRODUCT_DESCRIPTION_REPLACEMENT | 250 | 124.74 | 101.5 | 57 | 392 |
| NO_USE_ASSERTIVE_RECOMMENDATION | 250 | 129.27 | 106.0 | 60 | 530 |
| PROMOTIONAL_TEMPLATE | 250 | 123.22 | 100.0 | 55 | 319 |
| EXPERIENCE_FREE_CLAIM | 250 | 134.52 | 110.0 | 63 | 459 |
| COPY_VARIATION | 250 | 112.8 | 99.0 | 58 | 313 |

## 충돌 / 중복 / 누수

- label conflict 그룹: 0
- cross-split exact-content: 0

| 범위 | exact 그룹 | 참여 행 | 추가 행 |
| --- | --- | --- | --- |
| all | 0 | 0 | 0 |
| NORMAL | 0 | 0 | 0 |
| synthetic | 0 | 0 | 0 |

| leakage 검사 | 결과 |
| --- | --- |
| group_id | 0 |
| parent_review_id | 0 |
| synthetic_family_id | 0 |
| parent_source_row | 0 |
| existing_validator | PASS |

## 비기능어 편중 진단

문서별 포함 횟수(한 행당 1회)를 셉니다. 정규식 토큰화·간단한 조사 제거·기능어 목록에 의한 근사이며 한국어 형태소 분석이 아닙니다. 미탐지/오탐이 가능합니다.

이 근사 진단에서 30% 이상인 비기능어 후보는 없습니다.

| 상위 단어 | 포함 행 |
| --- | --- |
| 만한 | 285 |
| 물건 | 271 |
| 쉬운 | 255 |
| 특징입니다 | 242 |
| 관리 | 197 |
| 탄탄한 | 196 |
| 무난한 | 194 |
| 여러 | 185 |
| 줄여주 | 184 |
| 줄이 | 183 |
| 깔끔한 | 183 |
| 고르게 | 176 |
| 마감 | 173 |
| 두루 | 170 |
| 부담 | 167 |
| 가격 | 165 |
| 일상 | 164 |
| 주변 | 160 |
| 선물용으로 | 158 |
| 기본기 | 151 |
| 표면 | 149 |
| 부담스럽지 | 148 |
| 기대에 | 144 |
| 부응하 | 144 |
| 합리적인 | 144 |
| 알릴 | 138 |
| 다른 | 137 |
| 없겠어요 | 137 |
| 필요하다면 | 135 |
| 부분 | 134 |

## 반복 표현 상위 항목

| 구문 | 문서 빈도 |
| --- | --- |
| 점이 특징입니다 | 242 |
| 선물용으로도 무난한 | 158 |
| 기본기가 탄탄한 | 151 |
| 부담스럽지 않은 | 148 |
| 기대에 부응하는 합리적인 | 144 |
| 주변에도 알릴 만한 | 138 |
| 실속을 챙기기에 충분한 | 130 |
| 언제나 기대한 그대로일 거예요 | 128 |
| 비용에 비해 돋보이는 | 126 |
| 요즘 눈여겨볼 만한 | 126 |
| 받아보는 순간부터 기대할 만한 | 125 |
| 다양한 용도에 잘 맞는 | 125 |
| 소소한 일상을 편하게 만드는 | 124 |
| 마감을 신경 쓴 | 124 |
| 고민할 거리를 줄여주는 | 122 |
| 반박할 부분이 없다고 생각해요 | 121 |
| 군더더기를 덜어낸 실용적인 | 120 |
| 이 부분만큼은 확실하다고 봅니다 | 119 |
| 부족할 일은 없을 겁니다 | 115 |
| 여러 기준을 고르게 채운 | 115 |

## 시작 구문

문장부호를 제거하고 첫 3/4어절을 비교해 표면적으로 가까운 시작을 함께 검사합니다. 의미적으로 유사한 모든 시작을 탐지한다는 뜻은 아닙니다.

### PRODUCT_DESCRIPTION_REPLACEMENT

| 어절 수 | 최빈 비율 |
| --- | --- |
| 3 | 3.20% |
| 4 | 3.20% |

### NO_USE_ASSERTIVE_RECOMMENDATION

| 어절 수 | 최빈 비율 |
| --- | --- |
| 3 | 4.00% |
| 4 | 4.00% |

### PROMOTIONAL_TEMPLATE

| 어절 수 | 최빈 비율 |
| --- | --- |
| 3 | 4.00% |
| 4 | 4.00% |

### EXPERIENCE_FREE_CLAIM

| 어절 수 | 최빈 비율 |
| --- | --- |
| 3 | 4.00% |
| 4 | 4.00% |

### COPY_VARIATION

| 어절 수 | 최빈 비율 |
| --- | --- |
| 3 | 4.00% |
| 4 | 4.00% |

## 평가 및 한계

- Real NORMAL evaluation: validation/test의 human_candidate_review NORMAL과 sampled_non_candidate NORMAL을 따로 집계합니다. false positive rate 확인 목적이며 후자는 사람이 확인하지 않은 약한 라벨이라 참고용입니다.
- Synthetic challenge evaluation: validation/test의 synthetic SUSPICIOUS만 별도로 집계합니다. 실제 positive recall의 대체 지표가 아닙니다.
- 실제 SUSPICIOUS는 1건뿐이므로 실제 positive recall을 신뢰성 있게 평가할 수 없습니다. 데이터셋 생성 중 모델 학습/평가를 실행하지 않았습니다.
- group 단위 70/15/15 목표이며 실제 비율은 연결 그룹 크기에 따라 달라집니다. 모든 원본과 v2 synthetic의 공백 정리 exact 및 15자 이상 char_wb 3~5gram cosine≥0.85 연결요소를 사용합니다. 부모 ID와 원본 행, family를 함께 묶습니다.
- v1 synthetic 문장은 사용하지 않습니다. v2는 실제 seed에서 상품군을 파악하고 유형별 의미 절, 문체, 순서, 권유 방식과 길이를 다르게 조합합니다. 생성 주장은 제품에 대한 검증된 사실이 아닙니다.
- parent는 유지된 실제 리뷰 중 60~600자에서 플랫폼 비례로 뽑습니다. 홍보·COPY 유형은 일반적인 칭찬을 장황하게 늘이지 않도록 300자 이하의 parent만 사용합니다. 짧거나 긴 실제 학습 행을 삭제하지는 않습니다. 길이 제약은 의미 있는 별도 설명/주장 절로 맞추며 무의미한 패딩이나 문자열 잘라내기는 하지 않습니다.
- 정량 목표 통과는 문장 자연스러움·유형 적합성·임상/제품 사실성 검증이 아닙니다. 조합형 생성의 문체 편향이 완전히 사라졌다고 보장할 수 없습니다. 실제 리뷰가 같은 표현을 쓴다는 이유만으로 의심 라벨을 붙이지 마세요.

## 보존 파일 SHA256

- outputs\ptext_training_dataset_v1.xlsx: `1f305a0196884269cc05487e830288aed2f50ec637fc906103c2a96c007696e0`
- outputs\merged_reviews.xlsx: `20cdbc55e40fb69394cbf4cf5462e0dc02f4500cbcbfd8e5d772ec403286fbf4`
- outputs\merged_ptext_candidates_human_review_labeled_v1.xlsx: `b5dd31e1bd1eb4dbe094fab49fc8fa3cf28646bac61a00a8907f13b12a2dd32b`
- reports\ptext_training_dataset_v1_summary.md: `ed961ad1bf81a97eac445bbdaf24a32d307791d7e476cf0d1ad0b20d838eae27`
- reports\ptext_training_dataset_v1_audit.md: `051c5e361df01f6de15f976d3827acede4c216901ceedc700d226bb94e198cd5`
