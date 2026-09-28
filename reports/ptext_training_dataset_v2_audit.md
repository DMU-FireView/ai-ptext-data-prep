# P_text training dataset v2 audit

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

| 시작 3어절 | 수 |
| --- | --- |
| 공간을 적게 차지하는 | 8 |
| 좁은 틈에 남은 | 8 |
| 세척 뒤 건조하기 | 8 |
| 표면의 찌꺼기를 모아주는 | 7 |
| 불필요한 과정을 줄이는 | 6 |
| 손이 닿기 어려운 | 6 |
| 일상적인 관리에 대응하는 | 6 |
| 일상에 필요한 기본적인 | 6 |
| 손에 힘을 싣기 | 6 |
| 보관하기 쉬운 형태예요 | 6 |

### NO_USE_ASSERTIVE_RECOMMENDATION

| 어절 수 | 최빈 비율 |
| --- | --- |
| 3 | 4.00% |
| 4 | 4.00% |

| 시작 3어절 | 수 |
| --- | --- |
| 실제로 이용해보지는 않았는데도 | 10 |
| 써볼 시간이 아직 | 10 |
| 후기를 쓸 만큼 | 10 |
| 새것 그대로 남겨둔 | 10 |
| 기능을 직접 시험하기 | 10 |
| 한 번도 사용하지 | 10 |
| 아직 제 생활에 | 10 |
| 일단 써보는 건 | 10 |
| 택배만 받아둔 상태인데 | 10 |
| 실사용 시간이 전혀 | 10 |

### PROMOTIONAL_TEMPLATE

| 어절 수 | 최빈 비율 |
| --- | --- |
| 3 | 4.00% |
| 4 | 4.00% |

| 시작 3어절 | 수 |
| --- | --- |
| 기대에 부응하는 합리적인 | 10 |
| 주변에도 알릴 만한 | 10 |
| 받아보는 순간부터 기대할 | 10 |
| 실속을 챙기기에 충분한 | 10 |
| 비용에 비해 돋보이는 | 10 |
| 깔끔한 인상을 주는 | 10 |
| 마감을 신경 쓴 | 10 |
| 가격이 부담스럽지 않은 | 10 |
| 무난하게 두루 쓰기 | 10 |
| 고민할 거리를 줄여주는 | 10 |

### EXPERIENCE_FREE_CLAIM

| 어절 수 | 최빈 비율 |
| --- | --- |
| 3 | 4.00% |
| 4 | 4.00% |

| 시작 3어절 | 수 |
| --- | --- |
| 빠짐없이 충족되는 건 | 10 |
| 세척 뒤 건조하기 | 9 |
| 넓은 면을 빠르게 | 8 |
| 일상에 필요한 기본적인 | 8 |
| 진하기를 조절하기 쉬운 | 8 |
| 두껍지 않게 펼쳐지는 | 7 |
| 손에 힘을 싣기 | 7 |
| 벽과 바닥 모서리를 | 7 |
| 쉽게 익힐 수 | 7 |
| 여러 톤에 두루 | 7 |

### COPY_VARIATION

| 어절 수 | 최빈 비율 |
| --- | --- |
| 3 | 4.00% |
| 4 | 4.00% |

| 시작 3어절 | 수 |
| --- | --- |
| 깔끔한 인상을 주는 | 10 |
| 가격이 부담스럽지 않은 | 10 |
| 처음 접하는 분도 | 10 |
| 고민할 거리를 줄여주는 | 10 |
| 여러 기준을 고르게 | 10 |
| 다양한 용도에 잘 | 10 |
| 주변에도 알릴 만한 | 10 |
| 실속을 챙기기에 충분한 | 10 |
| 요즘 눈여겨볼 만한 | 10 |
| 받아보는 순간부터 기대할 | 10 |

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

## v2에서 제외된 NORMAL 중복 행 기록

행 번호는 원본 merged_reviews.xlsx의 source_excel_row입니다. 원본은 보존되어 있습니다.

| 제외 원본 행 | 제외 origin | 보존 원본 행 | 보존 origin |
| --- | --- | --- | --- |
| 664 | human_candidate_review | 665 | human_candidate_review |
| 666 | human_candidate_review | 665 | human_candidate_review |
| 7639 | human_candidate_review | 7645 | human_candidate_review |
| 8643 | human_candidate_review | 8644 | human_candidate_review |
| 8645 | human_candidate_review | 8644 | human_candidate_review |
| 2424 | human_candidate_review | 2425 | human_candidate_review |
| 6043 | human_candidate_review | 6092 | human_candidate_review |
| 6063 | human_candidate_review | 6092 | human_candidate_review |
| 6093 | human_candidate_review | 6092 | human_candidate_review |
| 6553 | human_candidate_review | 6606 | human_candidate_review |
| 6605 | human_candidate_review | 6606 | human_candidate_review |
| 4843 | human_candidate_review | 4838 | human_candidate_review |
| 1442 | human_candidate_review | 1414 | human_candidate_review |
| 7363 | human_candidate_review | 7366 | human_candidate_review |
| 7369 | human_candidate_review | 7366 | human_candidate_review |
| 1439 | human_candidate_review | 2534 | human_candidate_review |
| 4851 | human_candidate_review | 4846 | human_candidate_review |
| 4727 | human_candidate_review | 4732 | human_candidate_review |
| 4191 | human_candidate_review | 4190 | human_candidate_review |
| 4791 | human_candidate_review | 4788 | human_candidate_review |
| 3691 | human_candidate_review | 3690 | human_candidate_review |
| 7481 | human_candidate_review | 7483 | human_candidate_review |
| 4557 | human_candidate_review | 3346 | human_candidate_review |
| 49 | human_candidate_review | 3524 | human_candidate_review |
| 3110 | human_candidate_review | 3109 | human_candidate_review |
| 3995 | human_candidate_review | 3996 | human_candidate_review |
| 3940 | human_candidate_review | 3941 | human_candidate_review |
| 7288 | human_candidate_review | 7286 | human_candidate_review |
| 7038 | human_candidate_review | 7035 | human_candidate_review |
| 4826 | human_candidate_review | 4821 | human_candidate_review |
| 4856 | sampled_non_candidate | 4886 | sampled_non_candidate |
| 4981 | sampled_non_candidate | 4886 | sampled_non_candidate |
| 5031 | sampled_non_candidate | 4886 | sampled_non_candidate |
| 5035 | sampled_non_candidate | 4886 | sampled_non_candidate |
| 5056 | sampled_non_candidate | 4886 | sampled_non_candidate |
| 5096 | sampled_non_candidate | 4886 | sampled_non_candidate |
| 5111 | sampled_non_candidate | 4886 | sampled_non_candidate |
| 3074 | human_candidate_review | 3050 | human_candidate_review |
| 4768 | sampled_non_candidate | 4983 | sampled_non_candidate |
| 4773 | sampled_non_candidate | 4983 | sampled_non_candidate |
| 4808 | sampled_non_candidate | 4983 | sampled_non_candidate |
| 4948 | sampled_non_candidate | 4983 | sampled_non_candidate |
| 4992 | sampled_non_candidate | 4983 | sampled_non_candidate |
| 5093 | sampled_non_candidate | 4983 | sampled_non_candidate |
| 7145 | human_candidate_review | 7148 | human_candidate_review |
| 3175 | human_candidate_review | 3138 | human_candidate_review |
| 3176 | human_candidate_review | 3138 | human_candidate_review |
| 7395 | human_candidate_review | 7398 | human_candidate_review |
| 7401 | human_candidate_review | 7404 | human_candidate_review |
| 6173 | human_candidate_review | 6175 | human_candidate_review |
| 8499 | human_candidate_review | 8498 | human_candidate_review |
| 2094 | human_candidate_review | 2093 | human_candidate_review |
| 128 | human_candidate_review | 3073 | human_candidate_review |
| 1950 | human_candidate_review | 133 | human_candidate_review |
| 8528 | human_candidate_review | 8567 | human_candidate_review |
| 6652 | human_candidate_review | 6655 | human_candidate_review |
| 7238 | human_candidate_review | 7240 | human_candidate_review |
| 7239 | human_candidate_review | 7240 | human_candidate_review |
| 6101 | human_candidate_review | 6102 | human_candidate_review |
| 8486 | human_candidate_review | 8487 | human_candidate_review |
| 6215 | human_candidate_review | 6214 | human_candidate_review |
| 434 | human_candidate_review | 435 | human_candidate_review |
| 1744 | human_candidate_review | 1240 | human_candidate_review |
| 4120 | human_candidate_review | 4121 | human_candidate_review |
| 5266 | human_candidate_review | 5267 | human_candidate_review |
| 4715 | sampled_non_candidate | 4850 | sampled_non_candidate |
| 4815 | sampled_non_candidate | 4850 | sampled_non_candidate |
| 4860 | sampled_non_candidate | 4850 | sampled_non_candidate |
| 4960 | sampled_non_candidate | 4850 | sampled_non_candidate |
| 5030 | sampled_non_candidate | 4850 | sampled_non_candidate |
| 5100 | sampled_non_candidate | 4850 | sampled_non_candidate |
| 4737 | sampled_non_candidate | 4922 | sampled_non_candidate |
| 4812 | sampled_non_candidate | 4922 | sampled_non_candidate |
| 4822 | sampled_non_candidate | 4922 | sampled_non_candidate |
| 4972 | sampled_non_candidate | 4922 | sampled_non_candidate |
| 4977 | sampled_non_candidate | 4922 | sampled_non_candidate |
| 5027 | sampled_non_candidate | 4922 | sampled_non_candidate |
| 5067 | sampled_non_candidate | 4922 | sampled_non_candidate |
| 5087 | sampled_non_candidate | 4922 | sampled_non_candidate |
| 5097 | sampled_non_candidate | 4922 | sampled_non_candidate |
| 6582 | human_candidate_review | 6584 | human_candidate_review |
| 6586 | human_candidate_review | 6584 | human_candidate_review |
| 6588 | human_candidate_review | 6584 | human_candidate_review |
| 6590 | human_candidate_review | 6584 | human_candidate_review |
| 6592 | human_candidate_review | 6584 | human_candidate_review |
| 6594 | human_candidate_review | 6584 | human_candidate_review |
| 6596 | human_candidate_review | 6584 | human_candidate_review |
| 2407 | human_candidate_review | 2406 | human_candidate_review |
| 6836 | human_candidate_review | 6853 | human_candidate_review |
| 6850 | human_candidate_review | 6853 | human_candidate_review |
| 7517 | human_candidate_review | 7515 | human_candidate_review |
| 8741 | human_candidate_review | 7574 | human_candidate_review |
| 1097 | human_candidate_review | 1096 | human_candidate_review |
| 1862 | human_candidate_review | 1861 | human_candidate_review |
| 1161 | human_candidate_review | 3386 | human_candidate_review |
| 7115 | human_candidate_review | 7116 | human_candidate_review |
| 6119 | human_candidate_review | 6121 | human_candidate_review |
| 6120 | human_candidate_review | 6121 | human_candidate_review |
| 6122 | human_candidate_review | 6121 | human_candidate_review |
| 6123 | human_candidate_review | 6121 | human_candidate_review |
| 6124 | human_candidate_review | 6121 | human_candidate_review |
| 2935 | human_candidate_review | 2936 | human_candidate_review |
| 35 | human_candidate_review | 2949 | human_candidate_review |
| 4772 | human_candidate_review | 4767 | human_candidate_review |
| 2824 | human_candidate_review | 2823 | human_candidate_review |
| 1091 | human_candidate_review | 1092 | human_candidate_review |
| 5711 | human_candidate_review | 5709 | human_candidate_review |
| 3274 | human_candidate_review | 3275 | human_candidate_review |
| 19 | human_candidate_review | 2926 | human_candidate_review |
| 3086 | human_candidate_review | 3087 | human_candidate_review |
| 2276 | human_candidate_review | 2275 | human_candidate_review |
| 258 | human_candidate_review | 257 | human_candidate_review |
| 4262 | human_candidate_review | 4263 | human_candidate_review |
| 6217 | human_candidate_review | 6218 | human_candidate_review |
| 8647 | human_candidate_review | 8646 | human_candidate_review |
| 8648 | human_candidate_review | 8646 | human_candidate_review |
| 2943 | human_candidate_review | 2942 | human_candidate_review |
| 2127 | human_candidate_review | 1729 | human_candidate_review |
| 645 | human_candidate_review | 646 | human_candidate_review |
| 2317 | human_candidate_review | 2318 | human_candidate_review |
| 6006 | human_candidate_review | 6007 | human_candidate_review |
| 6720 | human_candidate_review | 6721 | human_candidate_review |
| 4837 | human_candidate_review | 4835 | human_candidate_review |
| 73 | human_candidate_review | 3006 | human_candidate_review |
| 7066 | human_candidate_review | 7068 | human_candidate_review |
| 2308 | human_candidate_review | 2307 | human_candidate_review |
| 361 | human_candidate_review | 362 | human_candidate_review |
| 2198 | human_candidate_review | 1343 | human_candidate_review |
| 3515 | human_candidate_review | 16 | human_candidate_review |
| 6490 | human_candidate_review | 6481 | human_candidate_review |
| 1157 | human_candidate_review | 1158 | human_candidate_review |
| 5856 | human_candidate_review | 5887 | human_candidate_review |
| 6411 | human_candidate_review | 6412 | human_candidate_review |
| 8715 | human_candidate_review | 8714 | human_candidate_review |
| 220 | human_candidate_review | 221 | human_candidate_review |
| 1981 | human_candidate_review | 1982 | human_candidate_review |
| 3011 | human_candidate_review | 3010 | human_candidate_review |
| 318 | human_candidate_review | 317 | human_candidate_review |
| 233 | human_candidate_review | 2468 | human_candidate_review |
| 2968 | human_candidate_review | 2969 | human_candidate_review |
| 3938 | human_candidate_review | 3937 | human_candidate_review |
| 8840 | human_candidate_review | 8835 | human_candidate_review |
| 686 | human_candidate_review | 687 | human_candidate_review |
| 90 | human_candidate_review | 3032 | human_candidate_review |
| 6022 | human_candidate_review | 6021 | human_candidate_review |
| 6049 | human_candidate_review | 6046 | human_candidate_review |
| 7451 | human_candidate_review | 7453 | human_candidate_review |
| 3076 | human_candidate_review | 3075 | human_candidate_review |
| 3684 | human_candidate_review | 3685 | human_candidate_review |
| 6228 | human_candidate_review | 6333 | human_candidate_review |
| 6532 | human_candidate_review | 6608 | human_candidate_review |
| 4645 | human_candidate_review | 4644 | human_candidate_review |
| 3829 | human_candidate_review | 3828 | human_candidate_review |
| 3271 | human_candidate_review | 3265 | human_candidate_review |
| 5275 | human_candidate_review | 5274 | human_candidate_review |
| 4117 | human_candidate_review | 4116 | human_candidate_review |
| 2996 | human_candidate_review | 2995 | human_candidate_review |
| 1653 | sampled_non_candidate | 4744 | sampled_non_candidate |
| 1655 | sampled_non_candidate | 4744 | sampled_non_candidate |
| 1659 | sampled_non_candidate | 4744 | sampled_non_candidate |
| 1663 | sampled_non_candidate | 4744 | sampled_non_candidate |
| 1665 | sampled_non_candidate | 4744 | sampled_non_candidate |
| 1671 | sampled_non_candidate | 4744 | sampled_non_candidate |
| 1676 | sampled_non_candidate | 4744 | sampled_non_candidate |
| 1684 | sampled_non_candidate | 4744 | sampled_non_candidate |
| 1686 | sampled_non_candidate | 4744 | sampled_non_candidate |
| 1708 | sampled_non_candidate | 4744 | sampled_non_candidate |
| 4714 | sampled_non_candidate | 4744 | sampled_non_candidate |
| 4719 | sampled_non_candidate | 4744 | sampled_non_candidate |
| 4734 | sampled_non_candidate | 4744 | sampled_non_candidate |
| 4754 | sampled_non_candidate | 4744 | sampled_non_candidate |
| 4799 | sampled_non_candidate | 4744 | sampled_non_candidate |
| 4819 | sampled_non_candidate | 4744 | sampled_non_candidate |
| 4834 | sampled_non_candidate | 4744 | sampled_non_candidate |
| 4874 | sampled_non_candidate | 4744 | sampled_non_candidate |
| 4894 | sampled_non_candidate | 4744 | sampled_non_candidate |
| 4904 | sampled_non_candidate | 4744 | sampled_non_candidate |
| 4934 | sampled_non_candidate | 4744 | sampled_non_candidate |
| 7247 | human_candidate_review | 7297 | human_candidate_review |
| 6107 | human_candidate_review | 6106 | human_candidate_review |
| 4789 | human_candidate_review | 4792 | human_candidate_review |
| 2981 | human_candidate_review | 2980 | human_candidate_review |
| 5834 | human_candidate_review | 6543 | human_candidate_review |
| 53 | human_candidate_review | 2978 | human_candidate_review |
| 2940 | human_candidate_review | 2941 | human_candidate_review |
| 8623 | human_candidate_review | 8621 | human_candidate_review |
| 8494 | human_candidate_review | 8490 | human_candidate_review |
| 2143 | human_candidate_review | 2144 | human_candidate_review |
| 2708 | human_candidate_review | 2707 | human_candidate_review |
| 6303 | human_candidate_review | 6307 | human_candidate_review |
| 6304 | human_candidate_review | 6307 | human_candidate_review |
| 6305 | human_candidate_review | 6307 | human_candidate_review |
| 6306 | human_candidate_review | 6307 | human_candidate_review |
| 6308 | human_candidate_review | 6307 | human_candidate_review |
| 6407 | human_candidate_review | 6408 | human_candidate_review |
| 1003 | human_candidate_review | 1090 | human_candidate_review |
| 4001 | human_candidate_review | 4002 | human_candidate_review |
| 3614 | human_candidate_review | 195 | human_candidate_review |
| 1939 | human_candidate_review | 9 | human_candidate_review |
| 2616 | human_candidate_review | 2617 | human_candidate_review |
| 2288 | human_candidate_review | 2287 | human_candidate_review |
| 6343 | human_candidate_review | 6339 | human_candidate_review |
| 8770 | human_candidate_review | 8771 | human_candidate_review |
| 8721 | human_candidate_review | 8769 | human_candidate_review |
| 8724 | human_candidate_review | 8769 | human_candidate_review |
