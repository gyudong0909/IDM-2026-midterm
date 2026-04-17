# IDM 중간고사 완전정복 패키지
**서울대학교 데이터마이닝개론 (26-1) | 2026-04-23 중간고사**

> **2026: Closed-book** (2024·2025는 오픈북) | T/F 오답 -1점 | 범위: L1~L13

---

## 파일 구조

```
DM/
├── prompts/                      ← Claude MAX 요청용 프롬프트
│   ├── prompt_A1a_L1to5.txt           ← HTML 헤더 + JS 데이터 + L1~L5  (~159K)
│   ├── prompt_A1b_L6to10.txt          ← L6~L10                          (~144K)
│   ├── prompt_A1c_L11to13.txt         ← L11~L13 + 집계 섹션 + 닫기      (~107K)
│   ├── prompt_B1_react_tf_trainer.txt
│   ├── prompt_B2_react_code_blanks.txt
│   └── prompt_B3_react_hw_solutions.txt
├── lecture notes/                ← 강의 슬라이드 PDF (1~13강)
├── lecture script/               ← 강의 스크립트 (영한 교차)
├── lecture video/                ← 강의 영상 (학습용, 프롬프트에서 제외)
├── IDM_previous_midterm/         ← 기출문제 (2024, 2025)
├── hw0~hw2/                      ← 과제
├── book_chapters/                ← MMDS 챕터별 분리본 (A1 프롬프트용)
│   ├── mmds_ch1.pdf  (20p)
│   ├── mmds_ch2.pdf  (52p)
│   ├── mmds_ch3.pdf  (58p)
│   ├── mmds_ch6.pdf  (40p)
│   ├── mmds_ch7.pdf  (40p)
│   ├── mmds_ch9.pdf  (36p)
│   └── mmds_ch11.pdf (34p)
└── study_guide.html              ← 메인 학습서 (브라우저에서 열기, A1 출력물)
```

---

## prompts/ 사용 방법

### ⚙️ 사전 준비 (최초 1회)

A1, B1, B2, B4는 로컬 PDF 파일을 읽는다. Claude Code에서 PDF를 읽으려면
`poppler-utils`가 시스템에 설치되어 있어야 한다.

```bash
sudo apt-get install poppler-utils
```

설치 확인:
```bash
pdftotext -v
```

> B3는 PDF 읽기 없음 → poppler-utils 불필요.

### 공통 원칙
- **각 프롬프트는 반드시 별도 대화(새 대화창)에서 실행**
- 한 대화에 여러 프롬프트 넣으면 출력 절단 발생
- 프롬프트 파일 내용을 전체 복사 → claude.ai 대화창에 붙여넣기

---

### A1: HTML 전체 재작성 (3개 세션)

토큰 한도(200K) 때문에 3개의 독립 세션으로 분리. 각 세션은 별개 대화창.

**작업 흐름:**

```
① [새 대화창 #1] prompt_A1a_L1to5.txt 붙여넣고 전송
   → 자료 읽음: L1~L5 PDF/스크립트 + MMDS ch1,2,6 + 기출 전체
   → 출력: HTML 헤더 + JS 데이터 레이어 + L1~L5
   → <!-- PART A1b CONTINUES HERE --> 로 끝남
   → 출력 전체 복사 저장 (Part_A.html)

② [새 대화창 #2] prompt_A1b_L6to10.txt 붙여넣고 전송
   → 자료 읽음: L6~L10 PDF/스크립트 + MMDS ch3,7,11 + 기출 전체
   → 출력: mmdsExamples_mid[] + L6~L10 섹션
   → <!-- PART A1c CONTINUES HERE --> 로 끝남
   → 출력 전체 복사 저장 (Part_B.html)

③ [새 대화창 #3] prompt_A1c_L11to13.txt 붙여넣고 전송
   → 자료 읽음: L11~L13 PDF/스크립트 + MMDS ch9,11 + HW + 기출
   → 출력: mmdsExamples_late[] + 병합 + L11~L13 + 집계 섹션 + </body></html>
   → 출력 전체 복사 저장 (Part_C.html)

④ Part_A.html + Part_B.html + Part_C.html 텍스트 합치기
   → study_guide.html 로 저장 → 브라우저에서 열기
```

> 각 세션은 독립적 — 순서대로 실행하되 같은 대화창일 필요 없음.

---

### B1: T/F 트레이너 (React)

**사용할 파일:** `prompt_B1_react_tf_trainer.txt`

**작업 흐름 (같은 대화창에서 2번 입력):**

```
① 새 대화창 열기
② prompt_B1_react_tf_trainer.txt 내용 전체 붙여넣고 전송
   → MAX가 기출 + 강의 자료 읽고 T/F 문제 목록(80~100개) 텍스트 출력
   → React 앱 코드는 아직 작성 안 함
③ 문제 목록 검토 후, 같은 대화창에서:
   "STEP 2 진행해줘"
   → React Artifact로 T/F 트레이너 앱 구현
```

---

### B2: 코드/슈도코드 빈칸 채우기 (React)

**사용할 파일:** `prompt_B2_react_code_blanks.txt`

```
① 새 대화창 열기
② 프롬프트 붙여넣고 전송 → React Artifact 한 번에 출력
   탭별 구성: MinHash | SGD for UV | Spark Quantile | BFR/SON
   슬라이드에서 추가 코드 발견 시 탭 자동 추가
```

---

### B3: 과제 해설 (React)

**사용할 파일:** `prompt_B3_react_hw_solutions.txt`

```
① 새 대화창 열기
② 프롬프트 붙여넣고 전송 → React Artifact 한 번에 출력
   탭 구성: HW1 | HW2
   각 문제 카드: 원문 + 단계별 풀이 + 시험 관련성 태그(🔴🟡⚪)
   뼈대 코드 TODO 해설 포함 (Q1 k-means, Q3 CF)
   필터: 전체 / 시험 직결만 / 진행 체크박스
```

---

## 기출 핵심 패턴

### 매년 출제 (2024, 2025 공통)
- **T/F 20점**: 전 범위에서 20문항, 오답 -1점
- **MapReduce/Spark**: combiner 조건, 워커 실패 원리, 분산 계산 구현
- **빈발 아이템셋**: Toivonen 실습, Association rules
- **LSH**: banding 계산, 유사도별 hash 방법 매칭
- **클러스터링**: k-means++ 계산, BFR N/SUM/SUMQ
- **차원 축소**: SVD 에너지 %, CUR 분해

### 2026 신규 범위
- **L12-13 추천 시스템**: 과거 기출 없음

### 출제 트렌드
- 2024: 계산형 중심 (오픈북)
- 2025: 이론/증명형 증가 + **Novel Variant** — A-CURE, Dω 등 시험장 정의 후 풀기 (오픈북)
- 2026 예상: **Closed-book으로 변경** → 공식·알고리즘 단계 암기 필수
  - Novel Variant 강도 낮아질 수 있음 (closed-book에서 너무 가혹)
  - 대신 T/F 세밀한 개념 구분, 표준 계산 문제 비중 증가 예상
  - 공식 없이 풀 수 있는 수준까지 이해 + 암기 병행 필요

---

## 교수 출제 철학

> *"I personally don't like memorizing. I want to ask your understanding skills —  
> how you understood the content and how well you can use the knowledge to solve other problems."*

공식 암기보다 **왜 그 공식이 존재하는지** 이해하는 것이 핵심.

---

## 빠른 복습 체크리스트

시험 전날 확인용:

- [ ] k-means++ 확률 계산 (D(p)² / ΣD(q)²)
- [ ] CURE: 대표점 선택 → shrink → 신규 점 배정
- [ ] BFR: N/SUM/SUMQ → centroid/σ → Mahalanobis 거리
  - centroid = SUM/N, σ² = SUMSQ/N - (SUM/N)², mahal = √Σ((x_d - c_d)/σ_d)²
- [ ] SVD: 에너지 = Σσᵢ², 상위 k개 보존율 계산
- [ ] CUR: 샘플링 확률 = ||col||²F / ||M||²F, 스케일 보정
- [ ] LSH S-curve: P = 1-(1-s^r)^b, 임계값 t ≈ (1/b)^(1/r)
  - r↑ (b↓, k=r×b 고정): S-curve 더 steep → precision↑, recall↓
  - b↑ (r↓, k=r×b 고정): 임계값 낮아짐 → recall↑, precision↓
- [ ] Toivonen: 샘플 → 빈발 집합 + Negative Border → 전체 검증
- [ ] UV Decomposition: SSE = Σ(r_xi - u_x·v_i)² (관측값만)
- [ ] UV vs SVD: 직교성 없음, blank 무시, gradient descent, k 과적합
- [ ] Pearson correlation: 유저 평균 빼고 공분산 / 표준편차 곱
- [ ] SGD 업데이트: ε=2(r-û), u←u+η(εv-λu), v←v+η(εu-λv)
- [ ] BPR: J = Σ -log σ(u_x^T v_i - u_x^T v_j)
- [ ] Novel Variant 대비: 각 알고리즘의 핵심 파라미터 역할 설명 가능한가?

---

*Generated with Claude Code | claude-sonnet-4-6*
