# -*- coding: utf-8 -*-
import json, sys, io, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from creatures import CREATURES

SP   = os.path.dirname(os.path.abspath(__file__))       # tools/
ROOT = os.path.dirname(SP)                              # 레포 루트
OUT  = os.path.join(ROOT, "index.html")

# 국가 데이터·소개문은 원작(둘기마요, RandomReincarnation)에서 가져온 UN WPP 2024 자료다.
COUNTRY_JS = io.open(f"{SP}/data/countries.js", encoding="utf-8").read().rstrip("\n")
PROFILE_JS = io.open(f"{SP}/data/profiles.js",  encoding="utf-8").read().rstrip("\n")
assert COUNTRY_JS.startswith("const COUNTRIES = ["), COUNTRY_JS[:40]
assert PROFILE_JS.startswith("const profileData = "), PROFILE_JS[:40]

# 원본 CSS(레이아웃·지도·버튼 스타일)는 tools/data/base.css 로 떼어 두었다.
ORIG_CSS = io.open(f"{SP}/data/base.css", encoding="utf-8").read().rstrip("\n")

sil = json.load(open(f"{SP}/silhouettes.json"))
SIL_JS = "const SIL = " + json.dumps(
    {k: {"vb": v["viewBox"], "tr": v["transform"], "d": v["paths"]} for k, v in sil.items()},
    ensure_ascii=False, separators=(",", ":")) + ";"

CREDITS = sorted({(v["contributor"] or v["attribution"] or "unknown") for v in sil.values()})

for c in CREATURES:
    s = sil[c["id"]]
    c["silTaxon"] = s["taxon"]
    c["silExact"] = s["exact"]
CREATURE_JS = "const CREATURES = " + json.dumps(CREATURES, ensure_ascii=False, separators=(",", ":")) + ";"

EXTRA_CSS = r"""
  /* ===== 생명 전체판 추가 스타일 ===== */
  .subtitle { word-break: keep-all; }

  .oddsNote {
    margin: -8px 0 16px;
    padding: 10px 13px;
    border-radius: 12px;
    background: #eef2ff;
    border: 1px solid #c7d2fe;
    color: #3730a3;
    font-size: 14px;
    line-height: 1.6;
    word-break: keep-all;
    overflow-wrap: anywhere;
  }

  .oddsNote b { font-weight: 700; }

  #creatureCard {
    display: none;
    gap: 18px;
    margin-bottom: 12px;
    padding: 18px;
    background: white;
    border: 1px solid #ddd;
    border-radius: 16px;
  }

  #creatureCard.shown { display: flex; }

  .silBox {
    flex: 0 0 190px;
    display: flex;
    align-items: center;
    justify-content: center;
    aspect-ratio: 1 / 1;
    padding: 14px;
    border-radius: 14px;
    background: #f3f4f6;
    color: #334155;
  }

  .silBox svg {
    display: block;
    width: 100%;
    height: 100%;
  }

  .creatureMeta { flex: 1 1 auto; min-width: 0; }

  .creatureName {
    font-size: 26px;
    font-weight: 700;
    line-height: 1.25;
    word-break: keep-all;
  }

  .creatureSci {
    margin-top: 2px;
    color: #888;
    font-size: 14px;
    font-style: italic;
  }

  .badges {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-top: 9px;
  }

  .badge {
    padding: 4px 9px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 700;
    white-space: nowrap;
  }

  .badge.ev-msr-pass    { background: #dcfce7; color: #166534; }
  .badge.ev-msr-debate  { background: #fef3c7; color: #92400e; }
  .badge.ev-msr-partial { background: #e0f2fe; color: #075985; }
  .badge.ev-ny          { background: #ede9fe; color: #5b21b6; }
  .badge.cnt-measured   { background: #e5e7eb; color: #4b5563; }
  .badge.cnt-estimated  { background: #ffe4e6; color: #9f1239; }

  .creatureBlurb {
    margin: 11px 0 0;
    color: #444;
    line-height: 1.72;
    word-break: keep-all;
    overflow-wrap: anywhere;
  }

  .creatureFacts {
    margin-top: 10px;
    color: #555;
    font-size: 14px;
    line-height: 1.7;
  }

  .creatureFacts span {
    display: block;
    word-break: keep-all;
    overflow-wrap: anywhere;
  }

  .srcLine {
    margin-top: 10px;
    padding-top: 9px;
    border-top: 1px dashed #e5e7eb;
    color: #999;
    font-size: 12px;
    line-height: 1.6;
    word-break: keep-all;
    overflow-wrap: anywhere;
  }

  #humanSection { display: none; }
  #humanSection.shown { display: block; }

  .humanBanner {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 10px;
    padding: 12px 14px;
    border-radius: 12px;
    background: #fff7d6;
    border: 1px solid #e8ca58;
    font-weight: 700;
    word-break: keep-all;
  }

  .mapSwitchRow {
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 10px;
  }

  .mapSwitchRow .label { margin: 0; }

  #mapError {
    display: none;
    padding: 16px;
    border-radius: 12px;
    background: #fef2f2;
    border: 1px solid #fecaca;
    color: #991b1b;
    font-size: 14px;
    line-height: 1.6;
  }

  .sources {
    margin-top: 14px;
    padding: 14px;
    background: white;
    border: 1px solid #ddd;
    border-radius: 14px;
    color: #666;
    font-size: 13px;
    line-height: 1.7;
  }

  .sources summary {
    cursor: pointer;
    font-weight: 700;
    color: #333;
  }

  .sources ul { margin: 10px 0 0; padding-left: 20px; }
  .sources li { margin-bottom: 6px; word-break: keep-all; overflow-wrap: anywhere; }
  .sources a { color: #2563eb; }

  /* ===== 모바일 대응 ===== */
  @media (max-width: 700px) {
    .wrap { padding: 18px 13px calc(40px + env(safe-area-inset-bottom)); }

    h1 { font-size: clamp(20px, 5.6vw, 26px); }

    .modeSwitch {
      width: 100%;
      display: flex;
    }

    .modeSwitch button {
      flex: 1 1 0;
      min-height: 44px;
      padding: 10px 8px;
    }

    #creatureCard { flex-direction: column; align-items: center; }

    .silBox {
      flex: 0 0 auto;
      width: min(56vw, 220px);
    }

    .creatureMeta { width: 100%; }

    .creatureName { font-size: 22px; text-align: center; }
    .creatureSci  { text-align: center; }
    .badges       { justify-content: center; }

    #rebirthBtn { min-height: 52px; font-size: 17px; }

    #supportBtn, #creatorXLink { flex: 1 1 140px; min-width: 0; min-height: 44px; }

    .actionRow { flex-direction: column; }
    .secondaryBtn { flex: 1 1 auto; min-height: 48px; }
    .keyHint { display: none; }          /* 물리 키보드가 없는 환경 */

    .statPanel { padding: 14px; }
    .heroValue { font-size: 38px; }

    /* 막대 행을 2단으로 접는다: 이름 위, 막대+숫자 아래 */
    .barRow {
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 3px 8px;
      padding: 6px 4px;
    }
    .barName { grid-column: 1 / -1; white-space: normal; word-break: keep-all; }
    .barTrack { grid-column: 1; }
    .barNums  { grid-column: 2; }
  }

  @media (max-width: 430px) {
    .stats { grid-template-columns: 1fr; }
    .card  { padding: 12px; }
    .value { font-size: 18px; }
    .silBox { width: min(68vw, 200px); }
  }


  /* ===== 액션 버튼 행 ===== */
  .actionRow {
    display: flex;
    gap: 10px;
    margin-top: 12px;
  }

  .secondaryBtn {
    flex: 1 1 0;
    min-width: 0;
    border: 1px solid #cbd5e1;
    border-radius: 14px;
    padding: 15px 12px;
    background: #fff;
    color: #334155;
    font: inherit;
    font-size: 15px;
    font-weight: 700;
    cursor: pointer;
    word-break: keep-all;
  }

  .secondaryBtn:hover { background: #f1f5f9; }
  .secondaryBtn:active { transform: translateY(1px); }
  .secondaryBtn[disabled] { opacity: .55; cursor: progress; }

  .keyHint {
    margin-top: 8px;
    color: #999;
    font-size: 13px;
    text-align: center;
    word-break: keep-all;
  }

  .keyHint kbd {
    display: inline-block;
    min-width: 20px;
    padding: 1px 6px;
    border: 1px solid #d1d5db;
    border-bottom-width: 2px;
    border-radius: 5px;
    background: #fff;
    color: #444;
    font-family: inherit;
    font-size: 12px;
    font-weight: 700;
    text-align: center;
  }

  /* ===== 통계 패널 (샘플링 · 인간 될 때까지) ===== */
  .statPanel {
    display: none;
    margin-top: 12px;
    padding: 18px;
    background: white;
    border: 1px solid #ddd;
    border-radius: 16px;
  }

  .statPanel.shown { display: block; }

  .sampleHead {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 8px;
  }

  .sampleTitle {
    font-size: 17px;
    font-weight: 700;
    word-break: keep-all;
  }

  .sampleSub {
    color: #888;
    font-size: 13px;
    word-break: keep-all;
  }

  .heroBox {
    margin: 14px 0 4px;
    padding: 15px 16px;
    border-radius: 14px;
    background: #eef2ff;
    border: 1px solid #c7d2fe;
  }

  .heroLabel {
    color: #4338ca;
    font-size: 13px;
    margin-bottom: 2px;
  }

  .heroValue {
    font-size: 48px;
    font-weight: 600;
    line-height: 1.05;
    color: #312e81;
  }

  .heroFoot {
    margin-top: 5px;
    color: #4338ca;
    font-size: 13px;
    line-height: 1.6;
    word-break: keep-all;
    overflow-wrap: anywhere;
  }

  /* 범례 — 막대(실측)와 눈금(기대)은 색이 아니라 모양으로 구분된다 */
  .chartLegend {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 14px;
    margin: 16px 0 10px;
    color: #666;
    font-size: 13px;
  }

  .legendItem { display: flex; align-items: center; gap: 6px; }

  .legendBar {
    width: 22px;
    height: 11px;
    border-radius: 0 4px 4px 0;
    background: #2563eb;
  }

  .legendTick {
    width: 2px;
    height: 15px;
    border-radius: 1px;
    background: #1e293b;
    box-shadow: 0 0 0 2px #fff;
  }

  /* ===== 순위 막대 목록 ===== */
  .barList { display: grid; gap: 7px; }

  .barRow {
    display: grid;
    grid-template-columns: 148px minmax(0, 1fr) 178px;
    align-items: center;
    gap: 10px;
    padding: 3px 4px;
    border-radius: 8px;
  }

  .barRow:hover { background: #f8fafc; }

  .barName {
    font-size: 13px;
    color: #171717;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .barTrack {
    position: relative;
    height: 14px;
    border-radius: 3px;
    background: #f3f4f6;
  }

  .barFill {
    height: 100%;
    min-width: 0;
    border-radius: 0 4px 4px 0;
    background: #2563eb;
  }

  .barTick {
    position: absolute;
    top: -2px;
    width: 2px;
    height: 18px;
    margin-left: -1px;
    border-radius: 1px;
    background: #1e293b;
    box-shadow: 0 0 0 2px #fff;
  }

  .barNums {
    color: #555;
    font-size: 12px;
    font-variant-numeric: tabular-nums;
    text-align: right;
    white-space: nowrap;
  }

  .barNums b { color: #171717; font-weight: 700; }
  .barNums .barExp { color: #999; }

  .barTail {
    margin-top: 4px;
    padding: 8px 4px 0;
    border-top: 1px solid #e5e7eb;
    color: #999;
    font-size: 12px;
    word-break: keep-all;
  }

  /* 인간 될 때까지 — 횟수가 주제라 히어로 색을 달리한다 */
  #questPanel .heroBox   { background: #fff7d6; border-color: #e8ca58; }
  #questPanel .heroLabel,
  #questPanel .heroFoot  { color: #8a6d0b; }
  #questPanel .heroValue { color: #6b5307; }

  .statNote {
    margin-top: 12px;
    color: #999;
    font-size: 12px;
    line-height: 1.65;
    word-break: keep-all;
    overflow-wrap: anywhere;
  }


  /* ===== 결과 등장 이펙트 ===== */
  /* 리롤할 때마다 결과가 "새로 도착했다"는 신호를 준다.
     재생을 다시 트리거하려면 JS에서 클래스를 떼고 reflow 후 다시 붙인다. */
  @keyframes resultPop {
    from { opacity: 0; transform: translateY(12px) scale(.985); }
    to   { opacity: 1; transform: none; }
  }

  @keyframes silPop {
    0%   { opacity: 0; transform: scale(.62) rotate(-7deg); }
    65%  { opacity: 1; transform: scale(1.07) rotate(2.5deg); }
    100% { opacity: 1; transform: scale(1) rotate(0); }
  }

  @keyframes glowRing {
    from { box-shadow: 0 0 0 0 rgba(37, 99, 235, .38); }
    to   { box-shadow: 0 0 0 14px rgba(37, 99, 235, 0); }
  }

  .pop { animation: resultPop .4s cubic-bezier(.2, .8, .2, 1) both; }

  #creatureCard.pop { animation: resultPop .4s cubic-bezier(.2, .8, .2, 1) both; }
  #creatureCard.pop .silBox     { animation: glowRing .7s ease-out both; }
  #creatureCard.pop .silBox svg { animation: silPop .52s cubic-bezier(.2, .9, .2, 1) both; }

  /* 맨 위로 올릴 때 화면 끝에 붙지 않도록 */
  #statsRow, .statPanel { scroll-margin-top: 12px; }

  @media (prefers-reduced-motion: reduce) {
    .pop,
    #creatureCard.pop,
    #creatureCard.pop .silBox,
    #creatureCard.pop .silBox svg { animation: none; }
  }

  #rebirthBtn, .secondaryBtn, .modeSwitch button, #supportBtn {
    -webkit-tap-highlight-color: transparent;
    touch-action: manipulation;
  }
"""

BODY = r"""
<div class="wrap">

  <div class="titleRow">
    <h1>🧬 랜덤 다시 태어나기 · 생명 전체판</h1>

    <div class="modeSwitch" role="group" aria-label="추첨 기준 선택">
      <button type="button" class="active" data-cmode="real" aria-pressed="true">실제 개체수</button>
      <button type="button" data-cmode="log" aria-pressed="false">로그 보정</button>
    </div>
  </div>

  <div class="subtitle" id="subtitle"></div>

  <div class="oddsNote" id="oddsNote"></div>

  <div class="stats" id="statsRow">
    <div class="card">
      <div class="label" id="totalLabel">후보 개체수 총합</div>
      <div class="value" id="totalValue">—</div>
    </div>

    <div class="card">
      <div class="label">이번 생</div>
      <div class="value" id="resultCreature">?</div>
    </div>

    <div class="card">
      <div class="label" id="chanceLabel">이번 생 확률</div>
      <div class="value" id="resultChance">—</div>
    </div>

    <div class="card">
      <div class="label">환생 횟수</div>
      <div class="value" id="rollCount">0</div>
    </div>
  </div>

  <div id="creatureCard">
    <div class="silBox" id="silBox"></div>

    <div class="creatureMeta">
      <div class="creatureName" id="creatureName"></div>
      <div class="creatureSci" id="creatureSci"></div>
      <div class="badges" id="creatureBadges"></div>
      <p class="creatureBlurb" id="creatureBlurb"></p>
      <div class="creatureFacts" id="creatureFacts"></div>
      <div class="srcLine" id="creatureSrc"></div>
    </div>
  </div>

  <div id="humanSection">
    <div class="humanBanner">🎉 인간으로 태어났습니다 — 이제 어느 나라에서 태어날지 뽑습니다.</div>

    <div class="mapSwitchRow">
      <div class="label" id="countrySubtitle"></div>

      <div class="modeSwitch" role="group" aria-label="국가 추첨 기준 선택">
        <button type="button" class="active" data-mode="births" aria-pressed="true">출생아 기준</button>
        <button type="button" data-mode="population" aria-pressed="false">인구 기준</button>
      </div>
    </div>

    <div id="mapBox">
      <div id="loading">세계지도 불러오는 중…</div>
      <div id="mapError"></div>
      <svg id="worldMap" viewBox="0 0 960 500" role="img" aria-label="랜덤 환생 세계지도" style="display:none"></svg>
    </div>

    <div id="result">
      당신은 <strong id="bigCountry"></strong>에서 다시 태어났습니다.
      <div id="detail"></div>
    </div>
  </div>

  <button id="rebirthBtn" type="button">🎲 랜덤으로 다시 태어나기</button>

  <div class="actionRow">
    <button id="questBtn" class="secondaryBtn" type="button">🔁 인간 될 때까지 뽑기</button>
    <button id="sampleBtn" class="secondaryBtn" type="button">📊 1,000번 샘플링</button>
  </div>

  <div class="keyHint"><kbd>R</kbd> 키를 누르면 바로 다시 태어납니다.</div>

  <div id="questPanel" class="statPanel">
    <div class="sampleHead">
      <div class="sampleTitle" id="questTitle"></div>
      <div class="sampleSub" id="questSub"></div>
    </div>

    <div class="heroBox">
      <div class="heroLabel">인간이 되기까지 뽑은 횟수</div>
      <div class="heroValue" id="questHero">—</div>
      <div class="heroFoot" id="questHeroFoot"></div>
    </div>

    <div class="chartLegend">
      <div class="legendItem"><span class="legendBar"></span>실측 (인간이 되기 전까지 뽑힌 횟수)</div>
      <div class="legendItem"><span class="legendTick"></span>기대 확률</div>
    </div>

    <div class="barList" id="questBars"></div>
    <div class="barTail" id="questTail"></div>

    <div class="statNote" id="questNote"></div>
  </div>

  <div id="samplePanel" class="statPanel">
    <div class="sampleHead">
      <div class="sampleTitle" id="sampleTitle"></div>
      <div class="sampleSub" id="sampleSub"></div>
    </div>

    <div class="heroBox">
      <div class="heroLabel">1,000번 중 인간으로 태어난 횟수</div>
      <div class="heroValue" id="sampleHero">—</div>
      <div class="heroFoot" id="sampleHeroFoot"></div>
    </div>

    <div class="chartLegend">
      <div class="legendItem"><span class="legendBar"></span>실측 (1,000회 중 뽑힌 횟수)</div>
      <div class="legendItem"><span class="legendTick"></span>기대 확률</div>
    </div>

    <div class="barList" id="sampleBars"></div>
    <div class="barTail" id="sampleTail"></div>

    <div class="statNote">
      막대(실측)와 눈금(기대)은 하나의 같은 축 위에 있습니다 — 실측·기대 중 큰 값이 축의 100%입니다.
      막대가 눈금보다 짧으면 기대보다 덜 나온 것, 길면 더 나온 것입니다. 모든 값은 오른쪽에 숫자로도 적어 두었습니다.
      1,000회는 표본이 작아 드문 종이 0회로 나오는 것은 정상입니다.
    </div>
  </div>

  <div class="bottom">
    <div class="card">
      <div class="label">최근 환생</div>
      <div class="history" id="history">아직 없음</div>
    </div>
  </div>

  <details class="sources">
    <summary>📚 후보 선정 기준과 개체수 출처 (꼭 읽어주세요)</summary>

    <p style="margin-top:10px"><b>후보를 어떻게 골랐나</b> — 거울 자기인식(mirror self-recognition) 실험에서 통과·논쟁·준통과 기록이 있는 종과,
    2024년 <a href="https://sites.google.com/nyu.edu/nydeclaration/declaration" target="_blank" rel="noopener noreferrer">뉴욕 동물 의식 선언</a>이
    “의식 경험의 현실적 가능성”을 인정한 분류군(모든 척추동물 · 두족류 · 십각류 · 곤충)에서 대표 종을 뽑았습니다.
    총 33종/분류군입니다.</p>

    <p><b>⚠️ 개체수의 한계</b> — 종별 전 세계 개체수가 실제로 <u>출판된</u> 것은 조류(Callaghan 2021), 가축(FAOSTAT), 대형 포유류(IUCN) 정도입니다.
    청줄청소놀래기 · 유령게 · 뿔개미 · 문어 · 가재 등은 <b>전 세계 개체수 추정치가 존재하지 않습니다.</b>
    이 종들은 자릿수(order of magnitude) 추정치를 넣고 <span class="badge cnt-estimated">개체수 추정</span> 배지를 붙였습니다.
    확률의 절대값이 아니라 자릿수의 차이를 보시면 됩니다.</p>

    <ul>
      <li>인구·출생아 — <a href="https://population.un.org/wpp/" target="_blank" rel="noopener noreferrer">UN World Population Prospects 2024</a> 2026년 중위 추계, 195개 국가·지역</li>
      <li>가축·벌통 — <a href="https://www.fao.org/faostat/" target="_blank" rel="noopener noreferrer">FAOSTAT</a> Production/Live Animals, 2024년 세계 합계</li>
      <li>조류 종별 개체수 — <a href="https://www.pnas.org/doi/10.1073/pnas.2023170118" target="_blank" rel="noopener noreferrer">Callaghan, Nakagawa &amp; Cornwell (2021) PNAS</a>, 9,700종 추정치</li>
      <li>개미 총량 — <a href="https://www.pnas.org/doi/10.1073/pnas.2201550119" target="_blank" rel="noopener noreferrer">Schultheiss et al. (2022) PNAS</a>, 전 세계 개미 2×10¹⁶마리</li>
      <li>분류군별 개체수 자릿수 — <a href="https://www.pnas.org/doi/10.1073/pnas.1711842115" target="_blank" rel="noopener noreferrer">Bar-On, Phillips &amp; Milo (2018) PNAS</a> SI Table S1</li>
      <li>야생 개체수·보전등급 — <a href="https://www.iucnredlist.org/" target="_blank" rel="noopener noreferrer">IUCN Red List</a></li>
      <li>거울 테스트 종별 결과 — <a href="https://en.wikipedia.org/wiki/Mirror_test" target="_blank" rel="noopener noreferrer">Mirror test (Wikipedia)</a> 및 각 원논문</li>
      <li>실루엣 그림 — <a href="https://www.phylopic.org/" target="_blank" rel="noopener noreferrer">PhyloPic</a>, 퍼블릭도메인(CC0/PDM) 이미지만 사용 · 기여자: __CREDITS__</li>
    </ul>

    <p><b>원본</b> — 국가별 추첨 부분은 둘기마요(<a href="https://x.com/oters1225" target="_blank" rel="noopener noreferrer">@oters1225</a>)의
    <a href="https://oters1117-art.github.io/RandomReincarnation/" target="_blank" rel="noopener noreferrer">랜덤 다시 태어나기</a>의 데이터와 로직을 그대로 사용했습니다.</p>
  </details>

  <div class="note">
    이 페이지는 통계 데이터로 만든 사고 실험입니다. 어떤 생물의 의식 유무에 대한 확정된 과학적 결론이 아닙니다.
    <div class="updatedAt">개체수 기준: FAOSTAT 2024 · UN WPP 2024(2026년 추계) · IUCN · 각 원논문</div>
  </div>

</div>
"""
BODY = BODY.replace("__CREDITS__", ", ".join(CREDITS))

SCRIPT = r"""
/* ===================== 데이터 ===================== */
__COUNTRY_JS__

__PROFILE_JS__
const profilesById = new Map(profileData.map(profile => [profile.id, profile]));

__SIL_JS__

__CREATURE_JS__

const EV_LABEL = {
  "msr-pass":    "🪞 거울 자기인식 통과",
  "msr-debate":  "🪞 거울 자기인식 (논쟁)",
  "msr-partial": "🪞 거울 자기인식 준통과",
  "ny":          "🧠 의식 가능성 · 뉴욕선언 2024"
};

const sum = (arr, fn) => arr.reduce((acc, item) => acc + fn(item), 0);

const totalBirths     = sum(COUNTRIES, d => d.births);
const totalPopulation = sum(COUNTRIES, d => d.population);

const realWeight = c => c.count;
const logWeight  = c => Math.log10(c.count);

const totalReal = sum(CREATURES, realWeight);
const totalLog  = sum(CREATURES, logWeight);
const human     = CREATURES.find(c => c.id === "human");

let creatureMode = "real";   // "real" | "log"
let countryMode  = "births"; // "births" | "population"

/* ===================== 표기 헬퍼 ===================== */
const KO_UNITS = [
  [1e16, "경"],
  [1e12, "조"],
  [1e8,  "억"],
  [1e4,  "만"]
];

function formatBigCount(n) {
  for (const [size, unit] of KO_UNITS) {
    if (n >= size) {
      const scaled = n / size;
      const digits = scaled >= 100 ? 0 : scaled >= 10 ? 1 : 2;
      return Number(scaled.toFixed(digits)).toLocaleString("ko-KR") + unit;
    }
  }
  return Math.round(n).toLocaleString("ko-KR");
}

function formatCount(n) {
  if (n >= 100000000) return (n / 100000000).toFixed(2) + "억";
  if (n >= 10000)     return Math.round(n / 10000).toLocaleString("ko-KR") + "만";
  return Math.round(n).toLocaleString("ko-KR");
}

function formatProbability(p) {
  const percent = p * 100;
  if (percent >= 1)    return percent.toFixed(2) + "%";
  if (percent >= 0.01) return percent.toFixed(3) + "%";
  return percent.toFixed(5) + "%";
}

function formatOdds(probability) {
  return "약 " + Math.round(1 / probability).toLocaleString("ko-KR") + "번 중 1번";
}

function secureRandom() {
  const values = new Uint32Array(1);
  crypto.getRandomValues(values);
  return values[0] / 4294967296;
}

/* items 중 하나를 weightFn 비례로 뽑는다 (원본 weightedPick의 일반화) */
function weightedPick(items, weightFn, totalWeight) {
  let random = secureRandom() * totalWeight;
  for (const item of items) {
    random -= weightFn(item);
    if (random < 0) return item;
  }
  return items[items.length - 1];
}

const creatureWeight = () => (creatureMode === "real" ? realWeight : logWeight);
const creatureTotal  = () => (creatureMode === "real" ? totalReal : totalLog);
const creatureChance = c => creatureWeight()(c) / creatureTotal();

/* ===================== 세계지도 (실패해도 1단계는 동작) ===================== */
let mapReady = false;
let countries = null, projection = null, svg = null, pinLayer = null;

async function initMap() {
  const [d3, topojson, world] = await Promise.all([
    import("https://cdn.jsdelivr.net/npm/d3@7.9.0/+esm"),
    import("https://cdn.jsdelivr.net/npm/topojson-client@3.1.0/+esm"),
    import("https://cdn.jsdelivr.net/npm/world-atlas@2.0.2/countries-110m.json/+esm")
  ]);

  const atlas = world.default ?? world;
  countries = topojson.feature(atlas, atlas.objects.countries);

  projection = d3.geoNaturalEarth1()
    .fitExtent([[10, 10], [950, 490]], countries);

  const path = d3.geoPath(projection);
  svg = d3.select("#worldMap");

  svg.append("g")
    .selectAll("path")
    .data(countries.features)
    .join("path")
    .attr("class", "country")
    .attr("data-id", d => String(+d.id))
    .attr("d", path);

  pinLayer = svg.append("g");
  window.__d3 = d3;

  document.getElementById("loading").style.display = "none";
  document.getElementById("worldMap").style.display = "block";
  mapReady = true;
}

initMap().catch(error => {
  console.error("세계지도 로딩 실패:", error);
  document.getElementById("loading").style.display = "none";
  const box = document.getElementById("mapError");
  box.style.display = "block";
  box.textContent = "세계지도를 불러오지 못했습니다(오프라인 또는 CDN 차단). "
    + "국가 추첨과 설명은 그대로 동작하고, 지도만 표시되지 않습니다.";
});

/* ===================== 1단계: 어떤 생물로 태어나는가 ===================== */
function renderSilhouette(id) {
  const box = document.getElementById("silBox");
  const data = SIL[id];
  box.replaceChildren();
  if (!data) return;

  const NS = "http://www.w3.org/2000/svg";
  const svgEl = document.createElementNS(NS, "svg");
  svgEl.setAttribute("viewBox", data.vb);
  svgEl.setAttribute("preserveAspectRatio", "xMidYMid meet");
  svgEl.setAttribute("aria-hidden", "true");

  const g = document.createElementNS(NS, "g");
  if (data.tr) g.setAttribute("transform", data.tr);
  g.setAttribute("fill", "currentColor");
  g.setAttribute("stroke", "none");

  for (const d of data.d) {
    const p = document.createElementNS(NS, "path");
    p.setAttribute("d", d);
    g.appendChild(p);
  }
  svgEl.appendChild(g);
  box.appendChild(svgEl);
}

function renderCreature(c) {
  renderSilhouette(c.id);

  document.getElementById("creatureName").textContent = c.emoji + " " + c.ko;
  document.getElementById("creatureSci").textContent  = c.sci;

  const badges = [
    { cls: "ev-" + c.evidence, text: EV_LABEL[c.evidence] },
    c.measured
      ? { cls: "cnt-measured",  text: "개체수 측정치" }
      : { cls: "cnt-estimated", text: "개체수 추정" },
    { cls: "cnt-measured", text: c.group }
  ];
  document.getElementById("creatureBadges").replaceChildren(...badges.map(b => {
    const span = document.createElement("span");
    span.className = "badge " + b.cls;
    span.textContent = b.text;
    return span;
  }));

  document.getElementById("creatureBlurb").textContent = c.blurb;

  const chance = creatureChance(c);
  const facts = [
    ...c.facts,
    "🔢 개체수 약 " + formatBigCount(c.count) + " · 이 모드에서 "
      + formatProbability(chance) + " (" + formatOdds(chance) + ")"
  ];
  document.getElementById("creatureFacts").replaceChildren(...facts.map(text => {
    const span = document.createElement("span");
    span.textContent = text;
    return span;
  }));

  const silNote = c.silExact
    ? ""
    : " · 실루엣은 상위 분류군(" + c.silTaxon + ")";
  document.getElementById("creatureSrc").textContent =
    "개체수 출처: " + c.countSrc + " · 그림 PhyloPic(CC0)" + silNote;

  document.getElementById("creatureCard").classList.add("shown");
}

/* ===================== 2단계: 인간이면 어느 나라인가 (원본 로직) ===================== */
function renderCountry() {
  const result = weightedPick(
    COUNTRIES,
    countryMode === "births" ? (d => d.births) : (d => d.population),
    countryMode === "births" ? totalBirths : totalPopulation
  );

  const birthProbability      = result.births / totalBirths;
  const populationProbability = result.population / totalPopulation;

  document.getElementById("bigCountry").textContent = result.name;

  const profile = profilesById.get(result.id);
  const populationOdds = countryMode === "population" ? ", " + formatOdds(populationProbability) : "";
  const birthOdds      = countryMode === "births"     ? ", " + formatOdds(birthProbability)      : "";

  const detailLines = [
    profile?.introduction,
    ...(profile?.statistics || []).map(statistic => "📊 " + statistic),
    "👥 인구 약 " + formatCount(result.population) + "명 (세계의 "
      + formatProbability(populationProbability) + populationOdds + ")",
    "👶 연간 출생아 약 " + formatCount(result.births) + "명 (세계의 "
      + formatProbability(birthProbability) + birthOdds + ")"
  ].filter(Boolean);

  document.getElementById("detail").replaceChildren(...detailLines.map(text => {
    const line = document.createElement("span");
    line.className = "detailLine";
    line.textContent = text;
    return line;
  }));

  document.getElementById("result").style.display = "block";

  if (mapReady) {
    svg.selectAll(".country")
      .classed("selected", d => String(+d.id) === String(+result.id));

    pinLayer.selectAll("*").remove();

    const countryFeature = countries.features.find(
      d => String(+d.id) === String(+result.id)
    );

    if (countryFeature) {
      const centroid = projection(window.__d3.geoCentroid(countryFeature));
      const scale = window.matchMedia("(max-width: 700px)").matches ? 1.6 : 1;

      if (centroid && Number.isFinite(centroid[0]) && Number.isFinite(centroid[1])) {
        pinLayer.append("circle").attr("class", "pinOuter")
          .attr("cx", centroid[0]).attr("cy", centroid[1]).attr("r", 10 * scale);
        pinLayer.append("circle").attr("class", "pinInner")
          .attr("cx", centroid[0]).attr("cy", centroid[1]).attr("r", 4 * scale);
      }
    }
  }

  return result;
}

function clearCountry() {
  document.getElementById("result").style.display = "none";
  document.getElementById("humanSection").classList.remove("shown");
  if (mapReady) {
    svg.selectAll(".country").classed("selected", false);
    pinLayer.selectAll("*").remove();
  }
}

/* ===================== 모드 전환 ===================== */
function setCreatureMode(mode) {
  creatureMode = mode;
  const isReal = mode === "real";

  document.querySelectorAll("[data-cmode]").forEach(button => {
    const isActive = button.dataset.cmode === mode;
    button.classList.toggle("active", isActive);
    button.setAttribute("aria-pressed", String(isActive));
  });

  document.getElementById("subtitle").textContent = isReal
    ? "지금 지구에 살아 있는 '자기 인식이 가능한 정도의 지능'을 가진 개체 하나를 실제 개체수 비례로 뽑습니다."
    : "개체수의 자릿수(log₁₀)를 가중치로 써서, 33종을 골고루 구경하는 모드입니다. 실제 확률이 아닙니다.";

  document.getElementById("totalLabel").textContent = isReal
    ? "후보 개체수 총합" : "후보 종·분류군";

  document.getElementById("totalValue").textContent = isReal
    ? formatBigCount(totalReal) + "마리"
    : CREATURES.length + "종";

  const humanChance = isReal
    ? human.count / totalReal
    : Math.log10(human.count) / totalLog;

  document.getElementById("oddsNote").innerHTML = isReal
    ? "이 모드에서 <b>인간</b>으로 태어날 확률은 <b>" + formatProbability(humanChance)
      + "</b> — " + formatOdds(humanChance)
      + "입니다. 후보를 자기인식 근거가 있는 33종으로 좁혀도 이 정도입니다."
    : "이 모드에서 <b>인간</b>이 나올 확률은 <b>" + formatProbability(humanChance)
      + "</b>입니다. 실제 개체수를 반영하지 않은 <b>구경용 모드</b>라는 점을 기억하세요.";

  document.getElementById("chanceLabel").textContent = "이번 생 확률";
  document.getElementById("resultCreature").textContent = "?";
  document.getElementById("resultChance").textContent = "—";
  document.getElementById("creatureCard").classList.remove("shown");
  hidePanels();
  clearCountry();
}

function setCountryMode(mode) {
  countryMode = mode;
  const isBirth = mode === "births";

  document.querySelectorAll("[data-mode]").forEach(button => {
    const isActive = button.dataset.mode === mode;
    button.classList.toggle("active", isActive);
    button.setAttribute("aria-pressed", String(isActive));
  });

  document.getElementById("countrySubtitle").textContent = isBirth
    ? "2026년 전 세계에서 태어나는 아기 한 명 기준"
    : "2026년 세계 인구 한 명 기준";
}


/* ===================== 결과 강조: 이펙트 + 맨 위로 스크롤 ===================== */
const PANEL_IDS = ["questPanel", "samplePanel"];

function hidePanels(...keep) {
  for (const id of PANEL_IDS) {
    if (!keep.includes(id)) document.getElementById(id).classList.remove("shown");
  }
}

const prefersReducedMotion = () =>
  typeof window.matchMedia === "function" &&
  window.matchMedia("(prefers-reduced-motion: reduce)").matches;

/* 같은 애니메이션을 다시 재생시키려면 클래스를 떼고 reflow를 강제한 뒤 다시 붙여야 한다. */
function playPop(el) {
  if (prefersReducedMotion()) return;
  el.classList.remove("pop");
  void el.offsetWidth;
  el.classList.add("pop");
}

function scrollToTop(el) {
  if (typeof el.scrollIntoView !== "function") return;
  el.scrollIntoView({
    behavior: prefersReducedMotion() ? "auto" : "smooth",
    block: "start"
  });
}

/* 이펙트를 재생하고 화면 맨 위로 올린다.
   리롤에서는 이펙트는 생물 카드에, 스크롤은 그 위의 통계 행에 걸린다. */
function highlight(popEl, scrollEl = popEl) {
  playPop(popEl);
  scrollToTop(scrollEl);
}

/* ===================== 환생 ===================== */
let rolls = 0;
const history = [];

/* 뽑힌 생물을 화면에 반영한다.
   attempts는 이 결과에 실제로 소모된 추첨 횟수 (인간 될 때까지 모드에서 1보다 커진다). */
function showResult(creature, attempts = 1, note = "") {
  rolls += attempts;

  const chance = creatureChance(creature);

  document.getElementById("resultCreature").textContent = creature.emoji + " " + creature.ko;
  document.getElementById("resultChance").textContent   = formatProbability(chance);
  document.getElementById("rollCount").textContent      = rolls.toLocaleString("ko-KR");

  clearCountry();
  renderCreature(creature);

  let label = creature.emoji + " " + creature.ko;

  if (creature.id === "human") {
    document.getElementById("humanSection").classList.add("shown");
    const country = renderCountry();
    label += "(" + country.name + ")";
  }

  history.push(label + note);
  if (history.length > 15) history.shift();
  document.getElementById("history").textContent = history.join(" → ");

  /* 이펙트는 생물 카드에, 스크롤은 그 바로 위의 통계 행(이번 생·확률·환생 횟수)에.
     리롤과 "인간 될 때까지" 모두 동일하게 동작한다. */
  highlight(document.getElementById("creatureCard"),
            document.getElementById("statsRow"));
}

function rebirth() {
  /* 새로 뽑으면 이전 통계 패널은 더 이상 이번 생과 무관하므로 치운다 */
  hidePanels();
  showResult(weightedPick(CREATURES, creatureWeight(), creatureTotal()));
}

document.getElementById("rebirthBtn").addEventListener("click", rebirth);
/* ===================== 1,000번 샘플링 통계 ===================== */
const SAMPLE_N = 1000;

function runSampling(n = SAMPLE_N) {
  const weightFn = creatureWeight();
  const total    = creatureTotal();
  const hits     = new Map(CREATURES.map(c => [c.id, 0]));
  const countryHits = new Map();

  for (let i = 0; i < n; i++) {
    const c = weightedPick(CREATURES, weightFn, total);
    hits.set(c.id, hits.get(c.id) + 1);

    if (c.id === "human") {
      const country = weightedPick(
        COUNTRIES,
        countryMode === "births" ? (d => d.births) : (d => d.population),
        countryMode === "births" ? totalBirths : totalPopulation
      );
      countryHits.set(country.name, (countryHits.get(country.name) || 0) + 1);
    }
  }

  const rows = CREATURES
    .map(c => ({ c, hits: hits.get(c.id), expected: creatureChance(c) }))
    .sort((a, b) => b.hits - a.hits || b.expected - a.expected);

  return { n, rows, countryHits };
}

function renderSampling(result) {
  const { n, rows, countryHits } = result;
  const isReal = creatureMode === "real";

  document.getElementById("sampleTitle").textContent =
    "📊 " + n.toLocaleString("ko-KR") + "번 샘플링 결과 — 많이 뽑힌 순";

  document.getElementById("sampleSub").textContent =
    (isReal ? "실제 개체수 기준" : "로그 보정 기준")
    + " · 국가는 " + (countryMode === "births" ? "출생아" : "인구") + " 기준";

  /* 히어로 — 이 앱이 말하려는 단 하나의 숫자 */
  const humanRow = rows.find(r => r.c.id === "human");
  document.getElementById("sampleHero").textContent =
    humanRow.hits.toLocaleString("ko-KR") + "회";

  const expectedHumans = humanRow.expected * n;
  const countryText = countryHits.size
    ? " 태어난 나라: " + [...countryHits]
        .sort((a, b) => b[1] - a[1])
        .map(([name, count]) => count > 1 ? name + " " + count + "회" : name)
        .join(", ")
    : " 이번 표본에서는 한 번도 인간이 되지 못했습니다.";

  document.getElementById("sampleHeroFoot").textContent =
    "기대값 " + expectedHumans.toFixed(2) + "회 (" + formatProbability(humanRow.expected) + ")."
    + countryText;

  renderBarList("sampleBars", "sampleTail", rows, n);

  /* "인간 될 때까지" 결과는 이번 샘플링과 무관하므로 치우고, 샘플링 결과를 맨 위로 */
  hidePanels("samplePanel");
  const panel = document.getElementById("samplePanel");
  panel.classList.add("shown");
  highlight(panel);
}

/* 순위 막대 목록 — 실측(막대)과 기대(눈금)를 하나의 축에 함께 올린다.
   축 최댓값을 둘 중 큰 값으로 잡아야 1위 막대가 기대치보다 낮을 때도 눈금이 축 안에 남는다. */
function renderBarList(barsId, tailId, rows, n) {
  const maxExpected = Math.max(...rows.map(r => r.expected * n));
  const axisMax     = Math.max(1, rows[0].hits, maxExpected);
  const shown       = rows.filter(r => r.hits > 0);
  const zeroed      = rows.filter(r => r.hits === 0);

  document.getElementById(barsId).replaceChildren(...shown.map(r => {
    const row = document.createElement("div");
    row.className = "barRow";

    const name = document.createElement("div");
    name.className = "barName";
    name.textContent = r.c.emoji + " " + r.c.ko;

    const track = document.createElement("div");
    track.className = "barTrack";

    const fill = document.createElement("div");
    fill.className = "barFill";
    fill.style.width = (r.hits / axisMax * 100).toFixed(3) + "%";
    track.appendChild(fill);

    /* 기대값 눈금 — 막대와 완전히 같은 축 위에 놓는다 */
    const tick = document.createElement("div");
    tick.className = "barTick";
    tick.style.left = (r.expected * n / axisMax * 100).toFixed(3) + "%";
    track.appendChild(tick);

    const nums = document.createElement("div");
    nums.className = "barNums";
    const strong = document.createElement("b");
    strong.textContent = r.hits.toLocaleString("ko-KR") + "회";
    const obs = document.createTextNode(
      " · " + (r.hits / n * 100).toFixed(1) + "% ");
    const exp = document.createElement("span");
    exp.className = "barExp";
    exp.textContent = "(기대 " + formatProbability(r.expected) + ")";
    nums.append(strong, obs, exp);

    row.append(name, track, nums);
    return row;
  }));

  /* 0회 종은 한 줄로 접는다 */
  const tail = document.getElementById(tailId);
  if (zeroed.length) {
    tail.style.display = "block";
    tail.textContent = "0회 " + zeroed.length + "종 — "
      + zeroed.map(r => r.c.ko).join(", ");
  } else {
    tail.style.display = "none";
    tail.textContent = "";
  }
}

const sampleBtn = document.getElementById("sampleBtn");

function sample() {
  sampleBtn.disabled = true;
  sampleBtn.textContent = "샘플링 중…";

  /* 버튼 상태가 먼저 그려지도록 한 프레임 넘긴다 */
  requestAnimationFrame(() => {
    try {
      renderSampling(runSampling());
    } finally {
      sampleBtn.disabled = false;
      sampleBtn.textContent = "📊 1,000번 샘플링";
    }
  });
}

sampleBtn.addEventListener("click", sample);

/* ===================== 인간이 나올 때까지 뽑기 ===================== */
/* 실제 개체수 기준 인간 확률은 0.064% — 기대 1,558번.
   상한 없이 돌리면 최악의 경우 브라우저가 멈추므로 안전 상한을 둔다.
   5만 번에서 못 찾을 확률은 (1-p)^50000 ≈ 3×10⁻¹⁴ 로 사실상 0이다. */
const QUEST_CAP = 50000;

function runQuest(cap = QUEST_CAP) {
  const weightFn = creatureWeight();
  const total    = creatureTotal();
  const hits     = new Map(CREATURES.map(c => [c.id, 0]));

  let attempts = 0;
  let found = null;

  while (attempts < cap) {
    const c = weightedPick(CREATURES, weightFn, total);
    attempts++;
    hits.set(c.id, hits.get(c.id) + 1);
    if (c.id === "human") { found = c; break; }
  }

  const rows = CREATURES
    .map(c => ({ c, hits: hits.get(c.id), expected: creatureChance(c) }))
    .sort((a, b) => b.hits - a.hits || b.expected - a.expected);

  return { attempts, found, rows, cap };
}

function renderQuest(result) {
  const { attempts, found, rows, cap } = result;
  const isReal = creatureMode === "real";
  const p = creatureChance(human);

  document.getElementById("questTitle").textContent = found
    ? "🔁 인간이 될 때까지 — " + attempts.toLocaleString("ko-KR") + "번 걸렸습니다"
    : "🔁 인간이 될 때까지 — 상한까지 실패";

  document.getElementById("questSub").textContent =
    (isReal ? "실제 개체수 기준" : "로그 보정 기준")
    + " · 국가는 " + (countryMode === "births" ? "출생아" : "인구") + " 기준";

  document.getElementById("questHero").textContent =
    attempts.toLocaleString("ko-KR") + "번" + (found ? "" : "+");

  /* 기하분포: 평균 1/p, 중앙값 ln2/p. 둘을 같이 보여야 "운이 좋았나"를 판단할 수 있다. */
  const mean   = 1 / p;
  const median = Math.log(2) / Math.log(1 / (1 - p));

  document.getElementById("questHeroFoot").textContent = found
    ? "인간 확률 " + formatProbability(p) + " · 평균 "
      + Math.round(mean).toLocaleString("ko-KR") + "번, 중앙값 "
      + Math.round(median).toLocaleString("ko-KR") + "번 걸립니다. "
      + (attempts <= median
          ? "중앙값보다 빨랐습니다 — 운이 좋은 절반에 속합니다."
          : "중앙값보다 오래 걸렸습니다.")
    : cap.toLocaleString("ko-KR") + "번을 뽑아도 인간이 나오지 않았습니다. "
      + "안전 상한에서 멈췄습니다 — 다시 눌러보세요.";

  document.getElementById("questNote").textContent = found
    ? "인간이 되기 직전까지 당신은 위의 것들이었습니다. 막대(실측)와 눈금(기대)은 "
      + attempts.toLocaleString("ko-KR") + "번을 기준으로 같은 축 위에 있습니다. "
      + "인간은 마지막 1회로 끝나므로 기대 눈금도 1 근처에 놓입니다."
    : "안전 상한(" + cap.toLocaleString("ko-KR") + "번)에 걸려 중단했습니다.";

  renderBarList("questBars", "questTail", rows, attempts);

  /* 샘플링 결과는 이번 추첨과 무관하므로 치운다 */
  hidePanels("questPanel");
  const panel = document.getElementById("questPanel");
  panel.classList.add("shown");

  /* 마지막 결과를 메인 카드에 반영 — 소모한 추첨 횟수 전부를 환생 횟수에 더한다.
     showResult가 생물 카드를 맨 위로 올리므로 여기서 별도 스크롤은 하지 않는다. */
  if (found) {
    showResult(found, attempts, " [" + attempts.toLocaleString("ko-KR") + "번째]");
  } else {
    highlight(panel);   /* 상한 실패 시엔 카드가 안 바뀌므로 패널을 올린다 */
  }
}

const questBtn = document.getElementById("questBtn");

function quest() {
  questBtn.disabled = true;
  questBtn.textContent = "인간을 찾는 중…";

  /* 버튼 상태가 먼저 그려지도록 한 프레임 넘긴다 */
  requestAnimationFrame(() => {
    try {
      renderQuest(runQuest());
    } finally {
      questBtn.disabled = false;
      questBtn.textContent = "🔁 인간 될 때까지 뽑기";
    }
  });
}

questBtn.addEventListener("click", quest);

/* ===================== 키보드 단축키 ===================== */
document.addEventListener("keydown", event => {
  if (event.key !== "r" && event.key !== "R") return;
  if (event.ctrlKey || event.metaKey || event.altKey) return;   // 새로고침(Ctrl+R) 등 보존

  const el = event.target;
  const tag = el && el.tagName;
  if (tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT" || (el && el.isContentEditable)) return;

  event.preventDefault();
  rebirth();
});


document.querySelectorAll("[data-cmode]").forEach(button => {
  button.addEventListener("click", () => {
    if (button.dataset.cmode !== creatureMode) setCreatureMode(button.dataset.cmode);
  });
});

document.querySelectorAll("[data-mode]").forEach(button => {
  button.addEventListener("click", () => {
    if (button.dataset.mode !== countryMode) {
      setCountryMode(button.dataset.mode);
      if (document.getElementById("humanSection").classList.contains("shown")) renderCountry();
    }
  });
});

setCountryMode("births");
setCreatureMode("real");

/* 콘솔 검증용 */
window.__mc = (n = 100000) => {
  const tally = new Map();
  for (let i = 0; i < n; i++) {
    const c = weightedPick(CREATURES, creatureWeight(), creatureTotal());
    tally.set(c.ko, (tally.get(c.ko) || 0) + 1);
  }
  return [...tally].map(([ko, hits]) => {
    const c = CREATURES.find(x => x.ko === ko);
    return { ko, observed: hits / n, expected: creatureChance(c) };
  }).sort((a, b) => b.observed - a.observed);
};
"""
SCRIPT = (SCRIPT
  .replace("__COUNTRY_JS__", COUNTRY_JS)
  .replace("__PROFILE_JS__", PROFILE_JS)
  .replace("__SIL_JS__", SIL_JS)
  .replace("__CREATURE_JS__", CREATURE_JS))

html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>랜덤 다시 태어나기 · 생명 전체판</title>
<style>
{ORIG_CSS}
{EXTRA_CSS}
</style>
</head>
<body>
{BODY}
<script type="module">
{SCRIPT}
</script>
</body>
</html>
"""
io.open(OUT, "w", encoding="utf-8").write(html)
print(f"wrote {OUT}  ({len(html.encode('utf-8')):,} bytes)")
