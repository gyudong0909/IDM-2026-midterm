# IDM 중간고사 완전정복 패키지
**서울대학교 데이터마이닝개론 (26-1) | 2026-04-23 중간고사**

> **2026: Closed-book** (2024·2025는 오픈북) | T/F 오답 -1점 | 범위: L1~L13

---

## 파일 구조

```
DM/
├── prompts/                      ← Claude Code 요청용 프롬프트
│   ├── prompt_A1a_L1to5.txt           ← standalone HTML: L1~L5          (→ A1a.html)
│   ├── prompt_A1b_L6to10.txt          ← standalone HTML: L6~L10         (→ A1b.html)
│   ├── prompt_A1c_L11to13.txt         ← standalone HTML: L11~L13 + 집계 (→ A1c.html)
│   ├── prompt_A1d_merge.txt           ← A1a+A1b+A1c 병합               (→ study_guide.html)
│   ├── prompt_B1_tf_trainer.txt       ← T/F 트레이너 섹션 추가 (바닐라 JS)
│   ├── prompt_B2_code_blanks.txt      ← 코드 빈칸 섹션 추가 (바닐라 JS)
│   └── prompt_B3_hw_solutions.txt     ← 과제 해설 섹션 추가 (바닐라 JS)
├── lecture notes/                ← 강의 슬라이드 PDF (1~13강)
├── lecture script/               ← 강의 스크립트 (영한 교차)

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

모든 프롬프트는 로컬 PDF 파일을 읽는다. Claude Code에서 PDF를 읽으려면
`poppler-utils`가 시스템에 설치되어 있어야 한다.

```bash
sudo apt-get install poppler-utils && pdftotext -v
```

### 공통 원칙
- **각 프롬프트는 반드시 별도 대화(새 대화창)에서 실행**
- 한 대화에 여러 프롬프트 넣으면 컨텍스트 초과로 출력 절단 발생
- 프롬프트 파일 내용을 전체 복사 → Claude Code 대화창에 붙여넣기
- 파일 저장 완료 메시지 확인 후 반드시 **exit(대화 종료)** → 새 대화창에서 다음 프롬프트 실행

---

### A1: HTML 전체 생성 (4개 세션)

토큰 한도(200K) 때문에 3개의 독립 세션으로 분리 생성 후 4번째 세션에서 병합.
각 A1x 파일은 완결된 standalone HTML — 단독 브라우저 실행 가능.

**작업 흐름:**

```
① [새 대화창 #1] prompt_A1a_L1to5.txt 붙여넣고 전송
   → 자료 읽음: L1~L5 PDF/스크립트 + MMDS ch1,2,6 + 기출 전체
   → A1a.html 생성 (완결된 standalone HTML: L1~L5)
   → "A1a.html 저장 완료" 확인 → exit

② [새 대화창 #2] prompt_A1b_L6to10.txt 붙여넣고 전송
   → 자료 읽음: L6~L10 PDF/스크립트 + MMDS ch3,7,11 + 기출 전체
   → A1b.html 생성 (완결된 standalone HTML: L6~L10)
   → "A1b.html 저장 완료" 확인 → exit

③ [새 대화창 #3] prompt_A1c_L11to13.txt 붙여넣고 전송
   → 자료 읽음: L11~L13 PDF/스크립트 + MMDS ch9,11 + 기출
   → A1c.html 생성 (완결된 standalone HTML: L11~L13 + 집계 섹션)
   → "A1c.html 저장 완료" 확인 → exit

④ [새 대화창 #4] prompt_A1d_merge.txt 붙여넣고 전송
   → A1a.html + A1b.html + A1c.html 읽기
   → CSS/JS 병합, 섹션 통합, mmdsExamples 배열 합치기
   → study_guide.html 생성
   → "study_guide.html 저장 완료" 확인 → exit → 브라우저에서 열기
```

> ⚠️ 각 세션은 완전 독립 — 반드시 exit 후 새 대화창에서 다음 실행. 같은 대화창에 이어서 실행하면 컨텍스트 초과로 내용 절단.

---

### B1: T/F 트레이너 추가 (A1d 완료 후)

**사용할 파일:** `prompt_B1_tf_trainer.txt`

```
① 새 대화창 열기 (study_guide.html 존재 확인)
② prompt_B1_react_tf_trainer.txt 전체 붙여넣고 전송
   → 기출 + 강의 자료 읽고 T/F 문제 목록(80~100개) 텍스트 출력 (STEP 1)
      문제마다 [기출2024 / 기출2025 / 예상] 라벨 부여 → 카드 배지 + 필터 UI로 구분
③ 문제 목록 검토 후, 같은 대화창에서:
   "STEP 2 진행해줘"
   → study_guide.html에 T/F 트레이너 섹션 추가 + 저장 → exit
```

---

### B2: 코드 빈칸 추가 (B1 완료 후)

**사용할 파일:** `prompt_B2_code_blanks.txt`

```
① 새 대화창 열기
② 프롬프트 붙여넣고 전송
   → 슬라이드 읽기 → study_guide.html에 코드 빈칸 섹션 추가 + 저장 → exit
```

---

### B3: 과제 해설 추가 (B2 완료 후)

**사용할 파일:** `prompt_B3_hw_solutions.txt`

```
① 새 대화창 열기
② 프롬프트 붙여넣고 전송
   → HW PDF + 강의 읽기 → study_guide.html에 과제 해설 섹션 추가 + 저장 → exit
```

---

## 전체 실행 체크리스트

순서를 지켜야 하며, 각 단계는 반드시 **별도 대화창 + exit** 후 다음 진행.

**A 시리즈 — study_guide.html 생성**
- [ ] A1a: `prompt_A1a_L1to5.txt` → `A1a.html` 생성 → exit
- [ ] A1b: `prompt_A1b_L6to10.txt` → `A1b.html` 생성 → exit
- [ ] A1c: `prompt_A1c_L11to13.txt` → `A1c.html` 생성 → exit
- [ ] A1d: `prompt_A1d_merge.txt` → `study_guide.html` 생성 (JS 병합 + `<!-- B_SERIES_ANCHOR -->` 삽입) → exit

**B 시리즈 — study_guide.html에 인터랙티브 섹션 추가**
- [ ] B1: `prompt_B1_tf_trainer.txt` → STEP1 확인 후 "STEP 2 진행해줘" → T/F 트레이너 추가 → exit
- [ ] B2: `prompt_B2_code_blanks.txt` → 코드 빈칸 섹션 추가 → exit
- [ ] B3: `prompt_B3_hw_solutions.txt` → 과제 해설 섹션 추가 → exit

**완료 후**
- [ ] 브라우저에서 `study_guide.html` 열기

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
