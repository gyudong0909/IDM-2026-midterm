#!/usr/bin/env python3
"""
Build study_viewer.html — 3-column study interface for IDM midterm prep.

Columns:
  [Left 40%]  PDF lecture slides (iframe)
  [Middle 30%] English lecture script (searchable, highlightable)
  [Right 30%]  Korean explanation + key formulas + traps

Reads:
  lecture notes/*.pdf           (referenced via iframe path)
  lecture script/*.txt          (inlined into HTML as JS data)

Usage: cd IDM-2026-midterm && python3 build_viewer.py
"""

import json
from pathlib import Path

BASE = Path(__file__).parent
SCRIPT_DIR = BASE / "lecture script"

LECTURES = [
    (1,  "Introduction",                    "1-intro.pdf",        "Lecture 1 - Introduction.txt"),
    (2,  "MapReduce",                       "2-mapreduce.pdf",    "Lecture 2 - MapReduce.txt"),
    (3,  "Spark",                           "3-spark.pdf",        "Lecture 3 - Spark.txt"),
    (4,  "Frequent Itemsets 1",             "4-itemsets-1.pdf",   "Lecture 4 - Frequent Itemsets 1.txt"),
    (5,  "Frequent Itemsets 2",             "5-itemsets-2.pdf",   "Lecture 5 - Frequent Itemsets 2.txt"),
    (6,  "Finding Similar Items 1",         "6-lsh-1.pdf",        "Lecture 6 - Finding Similar Items 1.txt"),
    (7,  "Finding Similar Items 2",         "7-lsh-2.pdf",        "Lecture 7 - Finding Similar Items 2.txt"),
    (8,  "Clustering 1",                    "8-clustering-1.pdf", "Lecture 8 - Clustering 1.txt"),
    (9,  "Clustering 2",                    "9-clustering-2.pdf", "Lecture 9 - Clustering 2.txt"),
    (10, "Dimensionality Reduction 1",      "10-dimred-1.pdf",    "Lecture 10 - Dimensionality Reduction 1.txt"),
    (11, "Dimensionality Reduction 2",      "11-dimred-2.pdf",    "Lecture 11 - Dimensionality Reduction 2.txt"),
    (12, "Recommender Systems 1",           "12-recsys-1.pdf",    "Lecture 12 - Recommender Systems 1.txt"),
    (13, "Recommender Systems 2",           "13-recsys-2.pdf",    "Lecture 13 - Recommender Systems 2.txt"),
]

EXPLAIN = {
1: r"""
<h3>L1: Introduction to Data Mining</h3>
<p>데이터 마이닝의 철학 — "왜 ML이 아닌 Data Mining인가". 공식보다 <b>intuition</b>이 핵심.</p>

<h4>핵심 개념</h4>
<ul>
<li><b>Bonferroni's principle</b>: 패턴이 의미 있는지 체크 — 같은 크기의 <em>랜덤 데이터</em>에서 예상 횟수와 비교. <br>예: 23명 중 생일 겹침 → 이미 P &gt; 0.5라 신기하지 않음.</li>
<li><b>TF-IDF</b>: 자주 쓰이지만 모든 문서에 나타나는 흔한 단어는 제외.
<div class="formula">\(\text{TF-IDF}(i,j) = \text{TF}(i,j) \times \log(N/n_i)\)</div></li>
<li><b>Hash function</b>: key → bucket [0, B−1]. 충돌은 피할 수 없음. O(1) lookup의 근간.</li>
<li><b>Power law</b>: log-log 선형. \(y = c x^a\). 20/80 법칙의 수학적 근거.</li>
<li><b>Memory hierarchy</b>: Register → L1/L2/L3 Cache → RAM → SSD/HDD → Cloud. 데이터가 어느 계층에 있느냐가 알고리즘 병목을 결정.</li>
</ul>

<h4>필수 암기</h4>
<ul>
<li>TF-IDF 공식과 각 항의 의미 (TF ↑ but IDF ↓ for common words)</li>
<li>Bonferroni principle 아이디어 (random expectation 대비 유의미성)</li>
<li>Power law의 log-log 선형성</li>
</ul>

<div class="warn"><b>T/F 함정:</b> "Data mining = ML"은 FALSE. ML은 DM의 <em>도구</em>. 명시적 규칙(parsing HTML 등)으로 풀 수 있으면 ML 불필요.</div>
""",

2: r"""
<h3>L2: MapReduce</h3>
<p>분산 컴퓨팅의 기본 패러다임. "<b>연산을 데이터로 가져간다</b>"는 원칙.</p>

<h4>핵심 공식</h4>
<div class="formula">
Map: \((k, v) \to \{(k_i, v_i)\}_i\)<br>
Reduce: \((k, [v_1, \ldots, v_n]) \to (k, v)\)
</div>
<p>Group by Key는 <em>시스템</em>이 처리 — 프로그래머는 Map/Reduce만 작성.</p>

<h4>Combiner 조건</h4>
<p>Reduce 함수가 <b>commutative + associative</b>일 때만 적용. 예: sum ✓, avg ✗ (count/total 분리 필요).</p>

<h4>노드 실패 처리</h4>
<ul>
<li><b>Map worker 실패</b>: 로컬 디스크에 있던 모든 출력 날아감 → 완료된 task까지 <em>전부 재실행</em></li>
<li><b>Reduce worker 실패</b>: 완료된 출력은 DFS에 안전 → 진행 중인 task만 재실행</li>
<li><b>Master 실패</b>: 전체 job 재시작</li>
</ul>

<h4>Matrix-Vector 곱 (v가 메모리에 맞을 때)</h4>
<div class="formula">map((i,j), m_ij) → (i, m_ij × v_j)<br>reduce(i, values) → (i, sum(values))</div>

<div class="warn"><b>T/F 함정:</b> "programmer writes GroupByKey" — FALSE. 시스템이 처리. | "framework checks associativity" — FALSE. 프로그래머 책임.</div>
""",

3: r"""
<h3>L3: Spark</h3>
<p>MapReduce의 상위 호환. DAG 기반 + 인메모리 + lazy evaluation.</p>

<h4>RDD (Resilient Distributed Dataset)</h4>
<ul>
<li>Partitioned, <b>immutable</b> (read-only), 한 타입의 컬렉션</li>
<li>메모리 캐싱 가능 — iterative 알고리즘에서 100x 속도</li>
<li>Lineage로 fault-tolerance (chunk 단위 재계산)</li>
</ul>

<h4>Transformation vs Action</h4>
<p><b>Transformation</b> (lazy): map, flatMap, filter, groupByKey, reduceByKey, join, sort, distinct</p>
<p><b>Action</b> (forces execution): count, collect, reduce, save, take</p>

<h4>Wide vs Narrow Dependency</h4>
<ul>
<li><b>Narrow</b>: 각 파티션이 최대 1개 부모 파티션에 의존 → 병렬 빠름. map, flatMap, filter.</li>
<li><b>Wide</b>: shuffle 필요. <em>groupByKey, join, sort, reduceByKey</em>.</li>
</ul>

<h4>MR vs Spark 용어 매핑</h4>
<p>MR Map ≈ Spark <code>flatMap</code>, MR Reduce ≈ Spark <code>reduceByKey</code>. 이름이 다름에 주의.</p>

<div class="warn"><b>T/F 함정:</b> "RDD is mutable" — FALSE. | "flatMap is wide" — FALSE (narrow). | "Spark always beats MR" — FALSE (메모리 초과 시 아님).</div>
""",

4: r"""
<h3>L4: Frequent Itemsets 1 — A-Priori</h3>
<p>Market-basket model. 핵심: <b>frequent itemset을 찾는 게 어렵고, 그 뒤 association rule은 쉽다</b>.</p>

<h4>핵심 공식</h4>
<div class="formula">
Support(I) = # baskets containing all items in I<br>
Confidence(I→J) = supp(I∪J) / supp(I) = P(J|I)<br>
Interest(I→J) = Conf − P(J)
</div>
<p>Interest는 <em>음수 가능</em> (negative correlation).</p>

<h4>A-Priori 단조성 (Monotonicity)</h4>
<p>I가 frequent이면 모든 subset도 frequent. 대우: item i가 infrequent면 i를 포함하는 어떤 pair도 infrequent. → Pass 1에서 필터 → Pass 2에서 frequent item끼리 pair만 카운트.</p>

<h4>메모리 경계: Triangular vs Triples</h4>
<ul>
<li>Triangular: \(4 \cdot n(n-1)/2\) bytes — dense data(p &gt; 1/3)에 유리</li>
<li>Triples (i, j, count): \(12 p \cdot n(n-1)/2\) — sparse(p &lt; 1/3)에 유리</li>
</ul>

<h4>Closed vs Maximal</h4>
<p><b>모든 maximal은 closed이지만, 역은 성립 안 함.</b> closed = immediate superset이 같은 support 없음. maximal = immediate superset 중 frequent 없음.</p>

<div class="warn"><b>T/F 함정:</b> "A-Priori finds interesting rules" — FALSE (frequent itemset만 찾음). | "Interest is always positive" — FALSE.</div>
""",

5: r"""
<h3>L5: Frequent Itemsets 2 — PCY, Multistage, Toivonen, SON</h3>
<p>A-Priori의 candidate pairs가 메모리 초과할 때. 3가지 개선 + 2가지 샘플링 기법.</p>

<h4>PCY (Park-Chen-Yu)</h4>
<p>Pass 1의 <em>여유 메모리</em>를 hash table에 활용. 각 pair를 bucket에 해시 → Pass 2 전에 bitmap으로 변환 (1/32 공간). Pass 2 candidate = 두 item 모두 frequent AND pair가 frequent bucket에 해시.</p>
<p><b>반드시 triples method 사용</b> (sparsity 활용 목적).</p>

<h4>Multistage</h4>
<p>PCY를 연쇄로 — 각 pass마다 새 hash 함수로 bitmap 추가. <b>이전 bitmap을 <em>버릴 수 없음</em></b> (조건 독립적).</p>

<h4>Toivonen</h4>
<ul>
<li>샘플로 frequent itemset + <b>negative border</b> 찾기</li>
<li>Negative border = 샘플에서 frequent 아니지만 모든 immediate subset은 frequent</li>
<li>전체 데이터에서 둘 다 체크. <em>border item이 전체에서 frequent면 실패 → 재샘플링</em></li>
<li>No false negative 보장 (샘플에 누락된 frequent itemset이 있다면 border에 반드시 존재)</li>
</ul>

<h4>SON (Savasere-Omiecinski-Navathe)</h4>
<p>Pass 1: 청크 단위 A-Priori (threshold ps). Pass 2: union을 전체 데이터에서 검증 (threshold s).</p>
<p><b>No false negative 증명 (pigeonhole)</b>: 전체 support ≥ s면 최소 한 청크에서 support ≥ ps. MapReduce와 궁합.</p>

<div class="warn"><b>T/F 함정:</b> "PCY uses triangular" — FALSE. | "Multistage can drop earlier bitmap" — FALSE. | "Toivonen checks for false negatives by full-data validation" — FALSE (그건 false positive 제거).</div>
""",

6: r"""
<h3>L6: LSH Part 1 — Shingling & MinHashing</h3>
<p>대규모 문서에서 유사 문서 찾기. O(N²) 비교를 O(N)으로 근사.</p>

<h4>3-stage pipeline</h4>
<p>Shingling → Min-Hashing → LSH Banding</p>

<h4>Jaccard + Characteristic Matrix</h4>
<div class="formula">sim(C_1, C_2) = |C_1 ∩ C_2| / |C_1 ∪ C_2|</div>
<p>Rows = shingles, columns = docs. 매우 sparse → 실제로 저장 X, signature로 대체.</p>

<h4>MinHash 핵심 항등식 (증명 가능해야 함)</h4>
<div class="formula">\(\Pr[h_\pi(C_1) = h_\pi(C_2)] = \text{Jaccard}(C_1, C_2)\)</div>
<p><b>증명:</b> permutation 후 "첫 active row"가 공통 원소일 확률 = |교집합|/|합집합|.</p>

<h4>Signature 계산 (streaming)</h4>
<p>n개 hash 함수 → signature 길이 n 벡터. rows를 한 번 스캔하며 각 (column, hash) 칸을 min으로 업데이트.</p>
<div class="formula">for each row r with value(c,r)=1:<br>&nbsp;&nbsp;for each hash i: sig[i][c] = min(sig[i][c], h_i(r))</div>
<p>추정 Jaccard = signature 일치 비율.</p>

<div class="warn"><b>T/F 함정:</b> "MinHash = exact Jaccard" — FALSE (unbiased estimator). | "Must store full characteristic matrix" — FALSE (streaming).</div>
""",

7: r"""
<h3>L7: LSH Part 2 — Banding & Distance</h3>
<p>Signature → 후보 pair 추출. S-curve 튜닝이 핵심.</p>

<h4>Banding</h4>
<p>Signature(길이 n)를 b개 band × r rows로 나눔. 각 band의 r값을 bucket에 해시. <b>한 band이라도 일치</b>하면 candidate pair.</p>

<h4>S-curve (반드시 유도 가능)</h4>
<div class="formula">\(P(\text{candidate}) = 1 - (1 - s^r)^b\)</div>
<p>\(s^r\) = 한 band 일치 확률. \((1-s^r)^b\) = 모든 band 불일치.</p>

<h4>Threshold</h4>
<div class="formula">\(t \approx (1/b)^{1/r}\)</div>
<table style="width:100%;font-size:13px;margin:8px 0">
<tr><th>조절</th><th>효과</th></tr>
<tr><td>r↑ (b↓)</td><td>S-curve steep, t↑, precision↑ <b>recall↓</b></td></tr>
<tr><td>b↑ (r↓)</td><td>S-curve 완만, t↓, <b>recall↑</b> precision↓</td></tr>
</table>

<h4>거리 metric 4공리</h4>
<ol><li>d ≥ 0</li><li>d(x,y)=0 ⇔ x=y</li><li>symmetric</li><li>triangle inequality</li></ol>

<h4>거리 ↔ LSH family 매칭</h4>
<ul>
<li>Jaccard → MinHash</li>
<li>Euclidean (L2) → random projection</li>
<li>Cosine → random hyperplane</li>
<li>Edit distance → ❌ (simple LSH family 없음)</li>
</ul>

<div class="warn"><b>T/F 함정:</b> "r↑ always increases recall" — FALSE (반대). | "Banding removes all FP" — FALSE (verify 필요).</div>
""",

8: r"""
<h3>L8: Clustering 1 — Hierarchical & k-means</h3>
<p>Unsupervised grouping. 두 계열: 계층적(트리) vs 분할적(고정 k).</p>

<h4>Hierarchical (Agglomerative)</h4>
<p>각 점이 cluster에서 시작 → 가장 가까운 두 cluster 병합 반복. <em>거리 정의 4가지</em>:</p>
<ul>
<li><b>Single link</b>: min pairwise → 체인 형성</li>
<li><b>Complete link</b>: max pairwise → round 클러스터</li>
<li><b>Average link</b>: mean pairwise → 균형</li>
<li><b>Centroid/Ward</b>: Euclidean 공간에서만 의미</li>
</ul>
<p><b>Non-Euclidean 공간</b>에서는 centroid 못 씀 → clustroid 또는 link 거리 사용.</p>

<h4>k-means (Lloyd's)</h4>
<ol>
<li>k개 centroid 초기화</li>
<li>각 점 → 가장 가까운 centroid 배정</li>
<li>centroid = 배정 점들의 평균으로 갱신</li>
<li>수렴까지 2-3 반복</li>
</ol>
<p>Local minimum만 보장. Global optimum은 보장 안 됨.</p>

<h4>k-means++ (똑똑한 초기화)</h4>
<div class="formula">\(\Pr[\text{pick } p] = \frac{D(p)^2}{\sum_q D(q)^2}\)</div>
<p>D(p) = 가장 가까운 기존 centroid와의 거리. <b>D²-weighted</b> 샘플링으로 centroid 분산. O(log k)-approximation 이론 보장.</p>

<h4>Silhouette</h4>
<div class="formula">\(s_i = (b_i - a_i) / \max(a_i, b_i)\)</div>
<p>a_i = 자기 cluster 평균 거리, b_i = 다음 가까운 cluster 평균. 높을수록 좋음.</p>

<div class="warn"><b>T/F 함정:</b> "k-means always global optimum" — FALSE. | "k-means++ guarantees optimal" — FALSE (approximation만).</div>
""",

9: r"""
<h3>L9: Clustering 2 — BFR & CURE</h3>
<p>대용량 데이터용 clustering. 메모리에 못 들어가는 경우.</p>

<h4>BFR (Bradley-Fayyad-Reina)</h4>
<p><b>가정:</b> cluster들은 axis-aligned Gaussian. 청크 단위 streaming 처리.</p>
<p>3개 집합 유지:</p>
<ul>
<li><b>DS</b> (Discard): 확실한 cluster 배정 점들의 요약 통계</li>
<li><b>CS</b> (Compression): 미배정 점들의 dense 서브클러스터</li>
<li><b>RS</b> (Retained): 아웃라이어, 실제 저장</li>
</ul>

<h4>Sufficient statistics (차원 d)</h4>
<div class="formula">N, SUM_d = Σx_d, SUMSQ_d = Σx_d²<br>centroid_d = SUM_d/N, σ_d² = SUMSQ_d/N − (SUM_d/N)²</div>

<h4>Mahalanobis 거리</h4>
<div class="formula">\(\text{mahal}(x,c) = \sqrt{\sum_d \left(\frac{x_d - c_d}{\sigma_d}\right)^2}\)</div>
<p>Threshold 보통 \(2\sqrt{D}\). 이 안에 있으면 DS에 배정.</p>

<h4>CURE (non-spherical 대응)</h4>
<ol>
<li>sample 추출 → 계층 clustering</li>
<li>각 cluster에서 <b>k개 representative</b> 선택 (centroid에서 가장 먼 점부터, 그 다음 기존 rep에서 먼 점)</li>
<li><b>Shrink</b>: <span class="formula" style="display:inline-block;padding:4px 10px;margin:0">p' = (1−α)p + αc</span> (α ≈ 0.2)</li>
<li>나머지 점은 가장 가까운 shrunk rep의 cluster로 배정</li>
</ol>
<p>왜 shrink? — rep이 outlier일 위험을 줄이고 robust하게.</p>
<p><b>Novel Variant 예고:</b> 2025 midterm에 A-CURE (α_i = 1/d_i) 출제. 각 알고리즘의 parameter 역할 이해 필수.</p>

<div class="warn"><b>T/F 함정:</b> "BFR needs all data in memory" — FALSE. | "CURE uses one centroid per cluster" — FALSE. | "Shrink moves toward nearest point" — FALSE (centroid 방향).</div>
""",

10: r"""
<h3>L10: Dimensionality Reduction 1 — SVD</h3>
<p>고차원 데이터가 사실 저차원 subspace에 있을 때. Frobenius norm 최적 근사.</p>

<h4>SVD 분해</h4>
<div class="formula">\(M_{m \times n} = U_{m \times r} \, \Sigma_{r \times r} \, V^T_{r \times n}\)</div>
<ul>
<li>r = rank(M)</li>
<li>U, V는 orthonormal columns</li>
<li>Σ는 diagonal, \(\sigma_1 \ge \sigma_2 \ge \cdots \ge 0\)</li>
</ul>

<h4>최적 rank-k 근사 (Eckart-Young)</h4>
<div class="formula">
\(M_k = \sum_{i=1}^{k} \sigma_i u_i v_i^T\)<br>
\(\|M - M_k\|_F^2 = \sum_{i>k} \sigma_i^2\)
</div>
<p>어떤 다른 rank-k 행렬도 이보다 작은 Frobenius 오차 못 만듦.</p>

<h4>Energy</h4>
<div class="formula">Total energy = \(\sum \sigma_i^2 = \|M\|_F^2\)<br>Retained by top-k = \(\sum_{i\le k}\sigma_i^2 / \sum \sigma_i^2\)</div>
<p>보통 <b>90% energy</b> 유지하는 k 선택.</p>

<h4>M^T M 관계</h4>
<p>\(M^T M = V \Sigma^2 V^T\). V의 columns = M^T M의 eigenvectors. eigenvalue = σ_i².</p>

<h4>추천 시스템에서 SVD 쿼리</h4>
<p>new user q를 concept space로: <b>q · V</b>. 그 후 U·Σ 공간에서 nearest user 찾음.</p>

<h4>기출 (2021 Final Q5)</h4>
<p>U5 rating [1, 0, 2, 3], V^T가 주어짐. concept projection = U5 · V = [3, √2/2, 2]. ★</p>

<div class="warn"><b>T/F 함정:</b> "SVD is unique" — FALSE (sign flips). | "SVD ≠ PCA" — TRUE (PCA는 centered data의 SVD).</div>
""",

11: r"""
<h3>L11: Dimensionality Reduction 2 — CUR</h3>
<p>SVD는 dense factor → sparsity 깨짐 + 해석 난해. CUR로 <b>실제 행/열</b>을 사용해 해결.</p>

<h4>CUR 분해</h4>
<div class="formula">\(M \approx C \cdot U \cdot R\)</div>
<ul>
<li>C: M의 실제 <b>열</b>들 (m × r)</li>
<li>R: M의 실제 <b>행</b>들 (r × n)</li>
<li>U: 중간 r × r 행렬 (pseudoinverse로 계산)</li>
</ul>

<h4>샘플링 확률</h4>
<div class="formula">\(p_j = \frac{\|m_{\cdot j}\|^2}{\|M\|_F^2}\)</div>
<p>열 노름의 제곱에 비례. 샘플 후 <b>스케일 \(1/\sqrt{r \cdot p_j}\)</b>로 보정.</p>

<h4>중간 U 구성</h4>
<ol>
<li>W = C와 R의 교집합 (r × r)</li>
<li>W = X Σ Y^T로 SVD</li>
<li>U = Y Σ⁺ X^T (Moore-Penrose pseudoinverse)</li>
</ol>

<h4>보장</h4>
<p>충분히 샘플 (\(r = O(k \log k / \epsilon^2)\)) 시 <b>(1+ε)-approximation</b> to SVD rank-k (expected Frobenius).</p>

<h4>SVD vs CUR</h4>
<table style="width:100%;font-size:13px">
<tr><th></th><th>SVD</th><th>CUR</th></tr>
<tr><td>정확도</td><td>optimal</td><td>(1+ε) of optimal</td></tr>
<tr><td>Sparsity</td><td>dense factors</td><td>sparse (원본 행/열 사용)</td></tr>
<tr><td>해석</td><td>abstract combo</td><td>concrete rows/cols</td></tr>
</table>

<div class="warn"><b>T/F 함정:</b> "CUR samples uniformly" — FALSE. | "CUR exact" — FALSE (approximation).</div>
""",

12: r"""
<h3>L12: Recommender Systems 1 — Content & CF</h3>
<p>개인화 추천. <b>Content-based</b> (아이템 특징 사용) vs <b>Collaborative Filtering</b> (상호작용만 사용).</p>

<h4>Utility matrix</h4>
<p>매우 sparse. 대부분 미평가. Netflix 기준 density &lt; 1%.</p>

<h4>Content-based</h4>
<ol>
<li>item profile (feature 벡터)</li>
<li>user profile (liked item들의 가중 평균)</li>
<li>score = cos(user profile, item profile)</li>
</ol>
<p>장: 새 item OK. 단: feature 필요, 과도 특화 (no serendipity).</p>

<h4>CF — User-User Pearson</h4>
<div class="formula">\(\text{sim}(x,y) = \frac{\sum_i (r_{xi}-\bar r_x)(r_{yi}-\bar r_y)}{\sqrt{\sum(r_{xi}-\bar r_x)^2}\sqrt{\sum(r_{yi}-\bar r_y)^2}}\)</div>
<p>평균 빼는 이유: 사용자별 rating 스케일 보정 (harsh vs lenient).</p>

<h4>Prediction (k-NN weighted)</h4>
<div class="formula">\(\hat r_{xi} = \bar r_x + \frac{\sum_{y \in N} \text{sim}(x,y)(r_{yi}-\bar r_y)}{\sum |\text{sim}(x,y)|}\)</div>

<h4>Item-Item CF (보통 더 좋음)</h4>
<p>아이템 특성은 안정적, 사용자 기분은 변동 → item-item similarity가 더 안정.</p>

<h4>Cold start</h4>
<ul><li>새 item: content-based OK, CF 불가</li><li>새 user: 둘 다 난감 → hybrid</li></ul>

<h4>Long tail</h4>
<p>온라인 스토어는 <em>무한 선반</em>으로 niche 상품 수익 가능 → 추천 시스템의 가치.</p>

<div class="warn"><b>T/F 함정:</b> "Content handles cold start for both" — FALSE (only items). | "Utility matrix dense" — FALSE. | "RMSE = user satisfaction" — FALSE (only numerical error).</div>
""",

13: r"""
<h3>L13: Recommender Systems 2 — Latent Factors, SGD, BPR</h3>
<p>Neighborhood CF → <b>k차원 embedding</b>. 훨씬 scalable + 보통 더 정확.</p>

<h4>UV Decomposition</h4>
<div class="formula">\(R \approx U V^T, \quad \hat r_{xi} = u_x^\top v_i\)</div>
<p><b>핵심:</b> 관측된 entry만 loss에 포함 (SVD와 결정적 차이).</p>

<h4>Objective</h4>
<div class="formula">\(\sum_{(x,i) \in \text{obs}} (r_{xi} - u_x^\top v_i)^2 + \lambda(\|U\|_F^2 + \|V\|_F^2)\)</div>

<h4>SGD Update (암기 필수)</h4>
<div class="formula">
ε = 2(r − u^T v)<br>
u ← u + η(ε v − λu)<br>
v ← v + η(ε u − λv)
</div>

<h4>Bias 포함 모델</h4>
<div class="formula">\(\hat r = \mu + b_x + b_i + u^T v\)</div>

<h4>UV vs SVD 차이</h4>
<table style="width:100%;font-size:13px">
<tr><th>UV</th><th>SVD</th></tr>
<tr><td>직교성 없음</td><td>U, V orthonormal</td></tr>
<tr><td>blank 무시 ✓</td><td>모든 entry (0 imputation)</td></tr>
<tr><td>SGD/ALS</td><td>linear algebra 정확해</td></tr>
</table>

<h4>BPR (Bayesian Personalized Ranking) — implicit feedback</h4>
<div class="formula">\(J = \sum_{(x,i,j)} -\log \sigma(u_x^\top v_i - u_x^\top v_j)\)</div>
<p>관측된 i를 미관측 j보다 <em>높게 랭크</em>하도록 학습. Pairwise loss.</p>

<div class="warn"><b>T/F 함정:</b> "UV has orthogonal factors" — FALSE. | "SGD needs full matrix in memory" — FALSE. | "BPR is pointwise" — FALSE (pairwise). | "SVD on sparse matrix with 0-fill = UV" — FALSE (핵심 함정, 2025 Final Q1(c)).</div>
""",
}

HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>IDM Study Viewer — PPT + Script + 설명</title>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<style>
:root { --toolbar-h: 58px; --border: #dee2e6; --accent: #4361ee; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { height: 100%; font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; color: #1a1a2e; overflow: hidden; }
body { display: flex; flex-direction: column; background: #f8f9fa; }

/* Toolbar */
#toolbar { height: var(--toolbar-h); background: #1a1a2e; color: #fff; display: flex; align-items: center; padding: 0 16px; gap: 12px; flex-shrink: 0; box-shadow: 0 2px 6px rgba(0,0,0,0.15); }
#toolbar strong { font-size: 16px; margin-right: 4px; letter-spacing: 0.3px; }
#toolbar select { padding: 7px 12px; font-size: 14px; border-radius: 5px; border: none; background: #fff; color: #1a1a2e; font-weight: 500; min-width: 240px; cursor: pointer; }
#toolbar .search-wrap { display: flex; align-items: center; background: #fff; border-radius: 5px; padding: 2px 4px; }
#toolbar input[type=text] { width: 200px; padding: 6px 10px; font-size: 13px; border: none; outline: none; }
#toolbar button { padding: 7px 12px; background: #2d2d5e; color: #fff; border: none; border-radius: 5px; cursor: pointer; font-size: 13px; font-weight: 500; transition: 0.15s; }
#toolbar button:hover { background: var(--accent); }
#toolbar .spacer { flex: 1; }
#toolbar .font-adjust { display: flex; align-items: center; gap: 4px; font-size: 12px; color: #ccc; }
#toolbar .font-adjust button { padding: 3px 9px; font-size: 12px; }
#toolbar .match-info { font-size: 12px; color: #aab; min-width: 70px; text-align: right; }

/* Three-column container */
#container { flex: 1; display: grid; grid-template-columns: 40% 30% 30%; gap: 1px; background: #ccc; overflow: hidden; }
.pane { background: #fff; overflow: hidden; display: flex; flex-direction: column; }
.pane-header { padding: 9px 14px; font-size: 12px; font-weight: 700; background: #eef2f7; border-bottom: 1px solid var(--border); flex-shrink: 0; color: #555; letter-spacing: 0.3px; }
.pane-body { flex: 1; overflow-y: auto; padding: 14px 18px; }

/* Left: PDF */
#pdf-frame { width: 100%; height: 100%; border: none; flex: 1; }

/* Middle: Script */
#script { white-space: pre-wrap; line-height: 1.85; font-size: 14px; font-family: 'Segoe UI', system-ui, sans-serif; color: #222; }
#script mark { background: #ffeb3b; padding: 0 3px; border-radius: 3px; font-weight: 500; }
#script mark.current { background: #ff9800; color: #fff; }

/* Right: Explanation */
#explain { font-size: 14px; line-height: 1.75; color: #222; }
#explain h3 { color: var(--accent); margin-bottom: 10px; font-size: 17px; border-bottom: 2px solid var(--accent); padding-bottom: 6px; }
#explain h4 { margin: 14px 0 6px; font-size: 14px; color: #1a1a2e; font-weight: 700; }
#explain p { margin: 6px 0; }
#explain ul, #explain ol { padding-left: 22px; margin: 6px 0; }
#explain li { margin: 4px 0; }
#explain code { background: #eef; padding: 1px 5px; border-radius: 3px; font-size: 13px; font-family: 'Consolas', monospace; }
#explain .formula { background: #f0f4ff; border: 1px solid #c7d2fe; border-radius: 6px; padding: 10px 14px; margin: 10px 0; text-align: center; font-family: 'Cambria Math', Cambria, serif; }
#explain .warn { background: #fff3cd; border: 1px solid #ffc107; border-radius: 6px; padding: 9px 13px; margin: 10px 0; font-size: 13px; }
#explain table { width: 100%; border-collapse: collapse; font-size: 13px; margin: 6px 0; }
#explain th { background: #1a1a2e; color: #fff; padding: 6px 10px; text-align: left; }
#explain td { padding: 6px 10px; border-bottom: 1px solid #e9ecef; }
#explain tr:nth-child(even) { background: #f7f8fa; }
</style>
</head>
<body>

<div id="toolbar">
  <strong>📚 IDM Viewer</strong>
  <select id="lec-select" onchange="loadLecture(this.value)"></select>
  <div class="search-wrap">
    <input type="text" id="search" placeholder="🔍 스크립트 검색..." oninput="searchScript(this.value)">
  </div>
  <span class="match-info" id="match-info"></span>
  <span class="spacer"></span>
  <div class="font-adjust">
    <span>글자</span>
    <button onclick="adjustFont(-1)">A−</button>
    <button onclick="adjustFont(+1)">A+</button>
  </div>
  <button onclick="window.open('study_guide.html','_blank')" title="전체 학습 가이드 새 창에서 열기">📖 Full Guide ↗</button>
</div>

<div id="container">
  <div class="pane">
    <div class="pane-header">📄 강의 슬라이드 (PPT)</div>
    <iframe id="pdf-frame" src="about:blank"></iframe>
  </div>

  <div class="pane">
    <div class="pane-header">📝 강의 스크립트 (English — 브라우저 우클릭 → "한국어로 번역" 가능)</div>
    <div class="pane-body">
      <div id="script"></div>
    </div>
  </div>

  <div class="pane">
    <div class="pane-header">💡 핵심 설명 & 공식 (한국어)</div>
    <div class="pane-body">
      <div id="explain"></div>
    </div>
  </div>
</div>

<script>
const LECTURES = __LECTURES_META__;
const SCRIPTS = __SCRIPTS__;
const EXPLAIN = __EXPLANATIONS__;

let currentFont = 14;

function init(){
  const sel = document.getElementById('lec-select');
  LECTURES.forEach(l => {
    const o = document.createElement('option');
    o.value = l.num;
    o.textContent = `L${l.num}: ${l.name}`;
    sel.appendChild(o);
  });
  const last = Number(localStorage.getItem('idm-viewer-lec') || 1);
  sel.value = String(last);
  loadLecture(last);
}

function loadLecture(n){
  n = Number(n);
  const l = LECTURES.find(x => x.num === n);
  if(!l) return;
  document.getElementById('pdf-frame').src = l.pdf;
  document.getElementById('script').textContent = SCRIPTS[n] || '(Script unavailable)';
  document.getElementById('explain').innerHTML = EXPLAIN[n] || '<p style="color:#999">설명 준비 중</p>';
  document.getElementById('search').value = '';
  document.getElementById('match-info').textContent = '';
  localStorage.setItem('idm-viewer-lec', n);
  if(window.MathJax && MathJax.typesetPromise) MathJax.typesetPromise();
}

function adjustFont(delta){
  currentFont = Math.max(10, Math.min(22, currentFont + delta));
  document.getElementById('script').style.fontSize = currentFont + 'px';
}

function searchScript(q){
  const el = document.getElementById('script');
  const n = Number(document.getElementById('lec-select').value);
  const text = SCRIPTS[n] || '';
  const info = document.getElementById('match-info');
  if(!q){
    el.textContent = text;
    info.textContent = '';
    return;
  }
  const esc = q.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const re = new RegExp(esc, 'gi');
  let count = 0;
  const html = text
    .replace(/[&<>]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]))
    .replace(re, m => { count++; return `<mark>${m}</mark>`; });
  el.innerHTML = html;
  info.textContent = count + ' 개 일치';
  const first = el.querySelector('mark');
  if(first){
    first.classList.add('current');
    first.scrollIntoView({behavior:'smooth', block:'center'});
  }
}

init();
</script>
</body>
</html>"""


def main():
    # Load scripts from filesystem
    scripts = {}
    missing = []
    for num, _, _, script_file in LECTURES:
        path = SCRIPT_DIR / script_file
        if path.exists():
            scripts[num] = path.read_text(encoding="utf-8", errors="replace")
        else:
            scripts[num] = f"(Script file not found: {script_file})"
            missing.append(script_file)

    # Lecture metadata
    meta = [
        {"num": n, "name": name, "pdf": f"lecture notes/{pdf}".replace(" ", "%20")}
        for n, name, pdf, _ in LECTURES
    ]

    # Inject
    html = (
        HTML
        .replace("__LECTURES_META__", json.dumps(meta, ensure_ascii=False))
        .replace("__SCRIPTS__", json.dumps(scripts, ensure_ascii=False))
        .replace("__EXPLANATIONS__", json.dumps(EXPLAIN, ensure_ascii=False))
    )

    out = BASE / "study_viewer.html"
    out.write_text(html, encoding="utf-8")

    size_kb = out.stat().st_size / 1024
    print(f"✓ Written: {out} ({size_kb:.1f} KB)")
    if missing:
        print(f"⚠ Missing scripts: {missing}")
    else:
        print(f"✓ All 13 lecture scripts loaded")
    print(f"✓ {len(EXPLAIN)} explanations embedded")


if __name__ == "__main__":
    main()
