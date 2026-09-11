# 🧬 랜덤 다시 태어나기 · 생명 전체판

**다시 태어난다면 무엇이 될까?** 지금 지구에 살아 있는 개체수를 가중치로 삼아, "자기 인식이 가능한 정도의 지능"을 가진 33종·분류군 중 하나를 무작위로 뽑습니다. **인간이 나오면 어느 나라에서 태어나는지 한 번 더** 뽑아 세계지도에 표시합니다.

▶ **https://fff-2.github.io/randomreincarnation/**

> 실제 개체수 기준으로 인간이 나올 확률은 **0.064%** — 약 1,558번 중 1번입니다.
> 후보를 자기인식 근거가 있는 33종으로 좁혀도 이 정도입니다.

---

## 기능

| | |
|---|---|
| **2단계 추첨** | ① 어떤 생물로 태어나는가 → ② 인간이면 어느 나라에서 태어나는가 |
| **두 가지 확률 모드** | `실제 개체수` (정직한 확률) / `로그 보정` (33종을 골고루 구경하는 모드) |
| **종별 카드** | PhyloPic 실루엣 + 설명 + 거울 테스트 근거 + 개체수와 그 출처 |
| **세계지도** | 인간이 뽑히면 195개 국가·지역 중 출생아/인구 비례로 추첨해 지도에 핀 표시 |
| **인간 될 때까지 뽑기** | 인간이 나올 때까지 반복 추첨 → 몇 번 걸렸는지, 그 전까지 무엇이었는지 보여줍니다 (안전 상한 5만 회) |
| **1,000번 샘플링** | 현재 모드로 1,000회 시뮬레이션 → 순위 막대 차트로 실측 vs 기대 비교 |
| **키보드 단축키** | <kbd>R</kbd> — 바로 다시 태어나기 (<kbd>Ctrl</kbd>+<kbd>R</kbd> 새로고침은 그대로 동작) |
| **결과 포커스** | 세 동작이 각각 자기 결과만 남기고 나머지 패널을 치운 뒤, 등장 이펙트와 함께 결과를 화면 맨 위로 올립니다 (`prefers-reduced-motion` 존중) |
| **모바일 대응** | 320px까지 가로 스크롤 없음, 터치 타깃 48px 이상, safe-area 대응 |

세계지도(d3 + world-atlas)만 CDN에서 불러오고 **나머지는 전부 단일 HTML 파일 안에 들어 있습니다.** 지도 로딩이 실패해도(오프라인·CDN 차단) 생물 추첨과 설명·실루엣은 그대로 동작합니다.

---

## 후보를 어떻게 골랐나

두 가지 근거를 썼고, 각 종마다 어느 근거인지 배지로 표시합니다.

**① 거울 자기인식(mirror self-recognition) 실험 기록** — [Mirror test](https://en.wikipedia.org/wiki/Mirror_test) 및 각 원논문

| 배지 | 뜻 | 종 |
|---|---|---|
| 🪞 **통과** | 마크 테스트를 통과한 기록 | 인간 · 침팬지 · 보노보 · 오랑우탄(보르네오/수마트라) · 큰돌고래 · 범고래 · 말 · 생쥐 · 청줄청소놀래기 · 대서양유령게 · 뿔개미 |
| 🪞 **논쟁** | 통과 보고가 있으나 재현 실패·단일 연구 | 서부/동부고릴라 · 아시아코끼리 · 유라시아까치 · 집까마귀 · 집비둘기 |
| 🪞 **준통과** | 거울을 이해하지만 마크 테스트는 미통과 | 쥐가오리 · 집돼지 · 개(후각 자기인식 STSR 통과) |

**② 의식 가능성** — [뉴욕 동물 의식 선언 (2024)](https://sites.google.com/nyu.edu/nydeclaration/declaration)

> "포유류와 조류의 의식적 경험에는 강력한 과학적 지지가 있다. 그 너머로도 모든 척추동물(파충류·양서류·어류 포함)과 많은 무척추동물(최소한 두족류·십각류·곤충)에서 의식적 경험의 현실적 가능성이 있다."

🧠 닭 · 소 · 아프리카사바나코끼리 · 회색앵무 · 뉴칼레도니아까마귀 · 큰까마귀 · 참문어 · 참갑오징어 · 유럽꼴뚜기 · 서양꿀벌 · 서양뒤영벌 · 가재류

---

## ⚠️ 개체수 데이터의 한계 — 꼭 읽어주세요

종별 전 세계 개체수가 실제로 **출판된** 것은 조류·가축·대형 포유류 정도입니다. 청줄청소놀래기 · 대서양유령게 · 뿔개미 · 문어 · 가재 등은 **전 세계 개체수 추정치가 존재하지 않습니다.** 이 종들은 상위 분류군의 자릿수(order of magnitude)에서 역산한 추정치를 넣고 `개체수 추정` 배지를 붙였습니다.

**확률의 절대값이 아니라 자릿수의 차이를 보시면 됩니다.**

| 출처 | 가져온 값 |
|---|---|
| [FAOSTAT](https://www.fao.org/faostat/) Production/Live Animals, 2024 | 닭 276.8억 · 소 15.79억 · 돼지 9.62억 · 말 5,621만 · 봉군 1억 171만 |
| [Callaghan, Nakagawa & Cornwell (2021) *PNAS*](https://www.pnas.org/doi/10.1073/pnas.2023170118) — 9,700종 조류 개체수 | 까치 3,337만 · 집까마귀 4,106만 · 큰까마귀 4,715만 · 양비둘기 2.86억 · 회색앵무 659만 · 뉴칼레도니아까마귀 22만 (모두 95% CI 포함) |
| [IUCN Red List](https://www.iucnredlist.org/) | 유인원 · 코끼리 · 고래류 야생 개체수 |
| [Schultheiss et al. (2022) *PNAS*](https://www.pnas.org/doi/10.1073/pnas.2201550119) | 전 세계 개미 2×10¹⁶마리 → 뿔개미(Myrmica) 역산의 상한 |
| [Bar-On, Phillips & Milo (2018) *PNAS*](https://www.pnas.org/doi/10.1073/pnas.1711842115) SI Table S1 | 분류군별 개체수 자릿수 (어류 10¹⁵ · 야생조류 10¹¹ · 육상 절지동물 10¹⁸ …) |
| [UN World Population Prospects 2024](https://population.un.org/wpp/) | 195개 국가·지역의 2026년 중위추계 인구·출생아 |

이 페이지는 통계로 만든 **사고 실험**입니다. 어떤 생물의 의식 유무에 대한 확정된 과학적 결론이 아닙니다.

---

## 빌드

`index.html`은 **생성물**입니다. 직접 편집하지 말고 빌더를 고친 뒤 다시 만드세요.

```bash
python3 tools/build.py          # → index.html (외부 의존성 없음)
```

```
tools/
├─ build.py                CSS·HTML·JS를 조립해 index.html 생성
├─ creatures.py            33종 데이터 — 개체수, 근거 등급, 설명, 출처
├─ fetch_silhouettes.py    PhyloPic API에서 퍼블릭도메인 실루엣 수집
├─ pplib.py                PhyloPic API 헬퍼
├─ silhouettes.json        수집된 SVG path (전부 CC0/PDM)
└─ data/
   ├─ countries.js         UN WPP 2024 · 195개 국가·지역
   ├─ profiles.js          국가별 소개문·통계
   └─ base.css             레이아웃·지도·버튼 기본 스타일
```

실루엣을 다시 수집하려면:

```bash
python3 tools/fetch_silhouettes.py tools/silhouettes.json
```

33종 전부 **퍼블릭도메인(CC0/PDM)** 이미지만 쓰도록 골랐습니다. 특정 종에 CC0 이미지가 없으면 상위 분류군 실루엣으로 폴백하고, 카드에 `실루엣은 상위 분류군(...)`이라고 표시합니다.

### 확률 검증

브라우저 콘솔에서 현재 모드의 실측 분포를 바로 확인할 수 있습니다.

```js
__mc(100000)   // 10만 회 몬테카를로 → [{ko, observed, expected}, ...]
```

또는 UI 버튼으로도 확인할 수 있습니다.

- `📊 1,000번 샘플링` — 1,000회의 실측 분포를 기대 확률과 나란히 비교
- `🔁 인간 될 때까지 뽑기` — 인간이 나올 때까지 걸린 횟수를 기하분포의 평균(1/p)·중앙값(ln2/p)과 비교

두 패널 모두 막대(실측)와 눈금(기대)이 **하나의 같은 축** 위에 있습니다 — 실측·기대 중 큰 값이 축의 100%입니다.

검증 결과: `runQuest()`를 반복한 평균 시도 횟수가 이론값 `1/p`와 실제 개체수 모드에서 2.5% 이내(n=300), 로그 보정 모드에서 0.7% 이내(n=20,000)로 일치합니다.

---

## 라이선스·출처

- **국가별 추첨 부분** — 둘기마요([@oters1225](https://x.com/oters1225))의 [랜덤 다시 태어나기](https://oters1117-art.github.io/RandomReincarnation/)에서 UN WPP 데이터와 추첨·지도 로직을 가져와 확장했습니다.
- **실루엣 그림** — [PhyloPic](https://www.phylopic.org/), 퍼블릭도메인(CC0 1.0 / PDM 1.0) 이미지만 사용.
  CC0는 출처 표시 의무가 없지만 기여자를 밝힙니다 — Amanda Kuhlman · Amy Beauvois · Andy Wilson · Cameron Dunn · Ferran Sayol · Guillaume Dera · Ieuan Jones · Jody Taylor · Jonathan Lawley · Margot Michaud · Marie Attard · Mattia Menchetti · Michael Day · Michael Rosenberg · Olesja Bogomaz · Rowan Sherwood · Steven Traver · T. Michael Keesey · Tony Goldberg.
- **개체수·연구 데이터** — 위 "개체수 데이터의 한계" 표의 각 출처를 따릅니다.
- **세계지도** — [world-atlas](https://github.com/topojson/world-atlas) (Natural Earth, 퍼블릭도메인) · [d3](https://d3js.org/) (ISC)
