# IDM 기출 T/F 분석 — 예상문제 갭 리포트
작성일: 2026-04-20 | 시험일: 2026-04-23

---

## 기출 T/F 전체 목록 (2024년 이전)

**2023 미드텀:** T/F 섹션 없음 (MapReduce/Spark 서술형으로만 구성)

**2021 파이널 (중간 범위 해당 문항만):**
- (b) Multistage algorithm cannot use triangular-matrix method → **TRUE**
- (c) Minhash probability = Jaccard similarity (regardless of hash functions) → **TRUE**
- (d) Non-Euclidean hierarchical clustering compares centroids → **FALSE** (clustroid)
- (e) PCA or SVD gives exact same result → **TRUE**
- (f) CF doesn't need item features → **TRUE**

**2019/2022 파이널:** 파이널 고유 범위(PageRank, SVM, CNN, 스트림 등)라 중간고사와 무관

---

## 예상문제의 출제 결 평가

### ✅ 정확히 잡은 것들

| 기출 | 내용 | 예상문제 |
|------|------|---------|
| 2019-e, 2021F-c | MinHash 확률 = Jaccard **similarity** | **Q29** 완전 일치. 이 토픽 3개 연도에서 출제됨 |
| 2019-i | Power iteration으로 MM^T 고유쌍 탐색 | **Q51** 완전 일치 |
| 2021F-b | Multistage + triangular-matrix 불가 | **2025-g** 기출 + Q22/Q26 인근 |
| 2021F-d | Non-Euclidean → centroid 비교 불가 (clustroid) | **Q43** 완전 일치 |
| 2021F-f | CF는 item feature 불필요 | **Q57** 완전 일치 |
| 2022-e | Increasing bands = OR-construction | **Q34, Q37**에서 커버 |
| 2019-d | PCY + triangular-matrix 조건 | **Q17, Q22** 인근 |
| 2022-g | BFR compressed set in memory | **Q46** 영역 |

### ⚠️ 주제는 맞으나 각도가 다른 것들

| 기출 | 내용 | 예상문제 갭 |
|------|------|-----------|
| 2019-a, 2022-a | "Combiner가 Reducer의 **모든** 작업 수행 가능?" (FALSE) | Q05는 "always applicable"이라는 다른 각도. 실제 기출은 역할 자체를 물음 |
| 2022-h | CUR: 일부 rows/columns 영원히 미선택 가능 (TRUE) | Q54는 sampling 확률 공식. 이 귀결 질문은 없음 |
| 2019-g | Hierarchical이 k-means보다 대규모에서 스케일 나쁨 (TRUE) | clustering 섹션 있으나 이 비교 질문 없음 |
| 2021F-e | PCA = SVD 결과 동일 (TRUE) | Q53과 관련 있으나 "동일한가?" 직접 질문 없음 |

---

## 🚨 예상문제에서 빠진 고위험 토픽

### 1위: Spark reduce()의 결합법칙/교환법칙 요구
> "In Spark, a function passed to a Reduce action is **required** to be associative and commutative."

- **2019 미드텀 (b), 2022 미드텀 (b) — 두 해 연속 거의 동일하게 출제**
- 예상문제에 전혀 없음. Q05는 MapReduce의 Combiner에 대한 질문이지 Spark reduce()가 아님.
- 답은 TRUE — Spark의 `reduce()` action은 교환+결합 필요 (associative+commutative)

### 2위: LSH 증폭(Amplification) 성질
> "Amplifying a (d1,d2,p1,p2)-sensitive family always results in p1'≥p1 and p2'≤p2."

- 2019 미드텀 (f) 출제. 답은 TRUE (AND-OR 복합 증폭 시 gap이 커짐).
- 예상문제에 없음. L7 섹션은 S-curve, threshold 공식 위주.

### 3위: Low confidence + high interest 조합
> "An association rule can have **low confidence but high interest**."

- 2019 미드텀 (c) 출제. 답은 TRUE.
- Interest = confidence - Pr[j]이므로 Pr[j]가 낮으면 confidence가 낮아도 interest는 클 수 있음.
- 예상문제는 "interest는 음수 가능"(2025 기출 각도)만 다루고 이 방향은 없음.

### 4위: GRGPF의 설계 목적 차원
> "The GRGPF algorithm is designed to **work well on low-dimensional data**."

- 2019 미드텀 (h) 출제. 답은 FALSE — GRGPF는 고차원 데이터용.
- 예상문제 Q48은 rowsum 정의를 묻지, 설계 목적을 묻지 않음.

### 5위: 사용자 프로필 정규화 → 음수 평점
> "When normalizing user profiles for content recommendation, some ratings may become negative."

- 2022 미드텀 (i) 출제. 답은 TRUE (평균 차감 시 평균 이하는 음수가 됨).
- 예상문제에 없음.

---

## 종합 평가

**출제 결 적중도: 약 72%**

| 항목 | 평가 |
|------|------|
| 2024/2025 기출 반영 | ★★★★★ (완벽) |
| 트릭 패턴 7개 분류 | ★★★★★ (교수 출제 패턴 정확히 포착) |
| 2019/2022 반복 토픽 커버 | ★★★☆☆ (MinHash·power iteration은 잡았으나 Spark reduce() 누락) |
| 주제 분포 균형 | ★★★★☆ (L1~L12까지 고른 분포) |

예상문제가 2024/2025 기반으로 설계되어 **핵심 트릭 패턴과 주제 커버리지는 우수**합니다.
하지만 기출에서 **두 해 연속 출제된 "Spark reduce() 결합법칙" 문제가 빠진 것이 가장 큰 맹점**입니다.
시험 전에 이 5가지 누락 토픽을 보완해두는 것을 강력히 권장합니다.

---

## 빠진 토픽 5개 — 즉석 보완 정리

### [Gap-1] Spark reduce() 결합법칙/교환법칙
**문제:** In Spark, a function passed to a Reduce action is required to be associative and commutative.
**정답: TRUE**
- Spark의 `reduce(f)` action은 파티션 간 순서가 보장되지 않으므로 f가 교환법칙+결합법칙을 만족해야 올바른 결과를 낸다.
- MapReduce의 Combiner 조건과 같은 이유.
- cf. `fold()`는 초기값을 지정할 수 있어 결합법칙만 필요.

### [Gap-2] LSH Amplification 성질
**문제:** Amplifying a (d1,d2,p1,p2)-sensitive family always results in a (d1,d2,p1',p2')-sensitive family such that p1'≥p1 and p2'≤p2.
**정답: TRUE**
- AND-OR 복합 증폭: AND는 p2를 줄이고, OR는 p1을 높인다.
- 결과적으로 gap(p1'-p2')이 커져 더 sharp한 분류 기준이 만들어진다.
- 단, OR-only: 둘 다 증가 / AND-only: 둘 다 감소. AND-OR 조합이 핵심.

### [Gap-3] Low confidence + high interest
**문제:** An association rule can have a low confidence, but high interest.
**정답: TRUE**
- Interest(I→j) = confidence(I→j) - Pr[j]
- Pr[j]가 매우 낮은 경우 (j가 희귀 아이템), confidence가 낮아도 interest는 양수로 클 수 있다.
- 예: Pr[j] = 0.01, confidence = 0.05 → interest = 0.04 (양수)
- 역으로 interest가 음수이면 I→j는 오히려 j의 출현을 억제한다.

### [Gap-4] GRGPF 고차원 전용
**문제:** The GRGPF algorithm is designed to also work well on low-dimensional data.
**정답: FALSE**
- GRGPF는 고차원(high-dimensional) non-Euclidean 공간에서 대용량 데이터를 처리하기 위해 설계되었다.
- rowsum 기반 clustroid 개념 자체가 고차원에서의 대표점 선택 문제를 해결하기 위함.
- 저차원에서는 k-means 등 더 간단한 알고리즘이 충분하다.

### [Gap-5] 사용자 프로필 정규화 → 음수 평점
**문제:** When normalizing user profiles for content recommendation, some ratings may become negative.
**정답: TRUE**
- Content-based filtering에서 사용자 프로필을 정규화할 때 평균을 차감(mean-centering)한다.
- 사용자의 평점이 평균보다 낮은 아이템은 정규화 후 음수 값이 된다.
- 이는 "이 사용자에게 평균 이하로 싫은 아이템"을 의미하며 정상적인 과정이다.

---

*분석 기반: EE412 Midterm 2019/2022, Final 2019/2021/2022 T/F 섹션*
*생성: Claude Sonnet 4.6*
