from flask import Flask, render_template_string, request, jsonify
import os, json, sqlite3
from datetime import datetime

app = Flask(__name__)

PAGE = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>SKYLINE TOWER | 자동 이동 편의 분석</title>
<style>
*{box-sizing:border-box}
body{margin:0;overflow:hidden;background:#dce5ec;color:#20384b;font-family:Arial,"Malgun Gothic",sans-serif}
#view{position:fixed;inset:0}
#titleIntro{position:fixed;inset:0;z-index:20;display:grid;place-items:center;background:radial-gradient(ellipse at center,#183347f2 0%,#07131df7 72%);color:#f5fbff;pointer-events:none;animation:introFade 2.9s ease forwards}
#titleIntro:before{content:"";position:absolute;width:min(70vw,680px);height:1px;background:linear-gradient(90deg,transparent,#74d9ee,transparent);transform:translateY(68px);opacity:.75}
#titleIntro h1{margin:0;padding:24px;text-align:center;font-size:clamp(28px,5vw,58px);letter-spacing:.045em;font-weight:800;text-shadow:0 0 26px #65cbe877;opacity:0;animation:titleRise .8s ease .18s forwards}
#titleIntro p{position:absolute;top:calc(50% + 62px);margin:0;color:#a9c7d6;font-size:11px;letter-spacing:.32em;opacity:0;animation:titleRise .7s ease .55s forwards}
@keyframes titleRise{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}
@keyframes introFade{0%,72%{opacity:1;visibility:visible}100%{opacity:0;visibility:hidden}}
@media(prefers-reduced-motion:reduce){#titleIntro{animation-duration:.6s}#titleIntro h1,#titleIntro p{animation-duration:.2s}}
canvas{display:block}
.panel{position:fixed;z-index:3;left:14px;top:14px;width:300px;max-height:calc(100vh - 28px);overflow:auto;padding:17px;background:#f8fbf2ed;border:1px solid #bacbd8;border-radius:13px;box-shadow:0 8px 28px #24384925}
h2{margin:0 0 4px;font-size:20px}
.sub{font-size:10px;letter-spacing:1.3px;color:#6c8191}
p{font-size:12px;line-height:1.65;color:#526b7e}
label{display:block;margin-top:12px;font-size:12px;font-weight:bold}
select,button{width:100%;padding:10px;margin-top:6px;border:1px solid #c2d0dc;border-radius:7px;background:white;color:#20384b;font-size:12px}
button{cursor:pointer}
button:hover{background:#e1f2f8}
.buttons{display:flex;gap:6px}
.buttons button{flex:1}
#info{margin-top:12px;padding:10px;background:#e5f1f7;border-radius:8px}
#info strong{font-size:13px;color:#087c99}
#info p{margin:5px 0 0}
#accessPanel{margin-top:12px;padding:10px;background:#fff;border:1px solid #c8d6df;border-radius:9px}
#accessPanel h3{font-size:13px;margin:0 0 7px;color:#173e58}
#accessPanel select,#accessPanel button,#accessPanel textarea{font-size:11px;padding:8px;margin-top:5px}
#accessPanel textarea{width:100%;min-height:48px;border:1px solid #c2d0dc;border-radius:6px;resize:vertical}
#accessSummary{font-size:11px;line-height:1.55;color:#526b7e;margin:7px 0}
#accessLegend{display:flex;flex-wrap:wrap;gap:5px;font-size:10px;margin:6px 0}
.legendChip{padding:3px 5px;border-radius:4px;background:#eef3f6}
#safetyPanel{position:fixed;z-index:4;right:14px;top:56px;width:290px;max-height:56vh;overflow:auto;padding:12px;background:#f8fbf2f2;border:1px solid #b8cbd7;border-radius:11px;box-shadow:0 8px 24px #24384922;font-size:11px}
#safetyPanel h3{margin:0 0 7px;font-size:14px;color:#173e58}
#evidencePanel{margin:0 0 10px;padding:9px;background:#fff;border:1px solid #c9d8e0;border-radius:8px}
#evidencePanel h4{margin:0 0 5px;font-size:13px;color:#173e58}
#evidenceAnalyze{width:100%;padding:8px;margin:5px 0;background:#145b7a;color:#fff;border:0;border-radius:6px;font-weight:bold;cursor:pointer}
#evidenceResults{max-height:235px;overflow:auto;margin-top:6px}
.evidenceCard{padding:7px;margin:5px 0;border:1px solid #d5e0e6;border-left:3px solid #8aa0ad;border-radius:5px;background:#fbfdfe;line-height:1.5;overflow-wrap:anywhere}
.evidenceCard strong{display:block;margin-bottom:2px;color:#20384b}
.evidenceMeta{font-size:10px;color:#526b7e}
#safetyScore{font-size:24px;font-weight:800;margin:3px 0}
#safetyMeta{line-height:1.6;color:#526b7e}
#riskFloors{display:grid;grid-template-columns:repeat(4,1fr);gap:4px;margin:7px 0}
.riskFloorBtn{padding:5px 2px!important;margin:0!important;font-size:10px!important}
#riskList{max-height:105px;overflow:auto;line-height:1.5}
#safetyPanel select,#safetyPanel input,#safetyPanel button{font-size:10px;padding:6px;margin-top:4px}
#safetyPanel input[type=checkbox]{width:auto}
.riskRow{padding:5px;margin:4px 0;background:#fff;border-radius:5px;border-left:3px solid #94a3b8}

#autoPanel button{width:100%;padding:9px;margin-top:5px;border-radius:6px;font-size:11px;cursor:pointer}
.autoFinding{padding:8px;margin:6px 0;border:1px solid #d3e0e7;border-left:4px solid #d39a16;border-radius:7px;background:#fff;font-size:11px;line-height:1.5}
.autoFinding button{width:auto!important;padding:5px 7px!important;margin:4px 4px 0 0!important}
#mobilityPanel{margin-top:12px;padding:10px;background:#f2f8fb;border:1px solid #b9d2df;border-radius:9px}
#mobilityPanel h3{font-size:13px;margin:0 0 6px;color:#173e58}
#mobilityPanel input,#mobilityPanel select,#mobilityPanel button{width:100%;font-size:11px;padding:7px;margin-top:4px;border:1px solid #c2d0dc;border-radius:6px;background:#fff;color:#20384b}
#mobilityPanel input[type=checkbox]{width:auto}
.mobGrid{display:grid;grid-template-columns:1fr 1fr;gap:5px}
.mobField label{margin-top:4px;font-size:10px}
.mobResult{padding:8px;background:#fff;border-radius:7px;margin-top:7px;border:1px solid #d3e0e7}
#mobScore{font-size:24px;font-weight:800;line-height:1.3}
#mobDetails{font-size:10px;line-height:1.55;white-space:pre-line;color:#435b6b}
.mobBar{height:7px;background:#e6edf1;border-radius:8px;overflow:hidden;margin-top:5px}
#mobBarFill{height:100%;width:0;background:#18845b}
.mobSmall{font-size:10px;color:#536b7a;line-height:1.45;margin-top:5px}
.mobSetting{border-top:1px solid #d3e0e7;margin-top:8px;padding-top:7px}
#mobSavedList{font-size:10px}
@media print{body{overflow:visible;background:#fff}#view,canvas,#safetyPanel,#hint,#toplabel{display:none!important}.panel{display:block!important;position:static;width:auto;max-height:none;overflow:visible;padding:0;border:0;box-shadow:none;background:#fff}.panel>*{display:none!important}#mobilityPanel{display:block!important;position:static;width:auto;max-height:none;overflow:visible;padding:0;border:0;background:#fff}#mobilityPanel>*:not(#mobilityPrint){display:none!important}#mobilityPrint{display:block!important}}

#toplabel{position:fixed;right:14px;top:14px;background:#173e58;color:#fff;padding:10px 13px;border-radius:8px;font-size:11px}
#hint{position:fixed;right:14px;bottom:14px;background:#f8fbf2ed;padding:11px 14px;border-radius:9px;font-size:11px;line-height:1.8;max-width:230px}
@media(max-width:650px){
.panel{left:7px;top:7px;width:240px;padding:11px;max-height:70vh}
h2{font-size:17px}
#toplabel{right:7px;top:7px;font-size:9px}
#hint{right:7px;bottom:7px;font-size:10px;max-width:180px}
#safetyPanel{right:7px;top:42px;width:230px;max-height:42vh;padding:8px}
#riskFloors{grid-template-columns:repeat(5,1fr)}
}
</style>
</head>
<body>
<div id="titleIntro" aria-label="안전 점수 계산 시스템 시작 화면"><div><h1>안전 점수 계산 시스템</h1><p>SPATIAL ACCESSIBILITY · MODEL REVIEW</p></div></div>
<div id="view"></div>

<section class="panel">
<h2>SKYLINE TOWER</h2>
<div class="sub">INTERACTIVE ARCHITECTURE</div>
<p>층을 선택해 내부 평면을 확인하세요. 건물의 외벽은 보기 쉽게 열려 있으며, 카메라만 움직입니다.</p>
<label for="floor">층 선택 · 용도</label>
<select id="floor">
<option value="all">건물 전체</option>
</select>
<div class="buttons">
<button id="in">＋ 확대</button>
<button id="out">－ 축소</button>
</div>
<div class="buttons">
<button id="inside">내부 보기</button>
<button id="outside">외관 보기</button>
</div>
<button id="reset">시점 초기화</button>
<div id="info">
<strong id="title">건물 안내</strong>
<p id="description">드래그로 카메라를 움직이고, 층을 선택하거나 내부 공간을 클릭해 보세요.</p>
</div>
<div id="autoPanel" style="margin-top:12px;padding:11px;background:#fff;border:1px solid #b9d2df;border-radius:9px">
<h3 style="margin:0 0 5px;font-size:14px;color:#173e58">자동 이동 편의 분석</h3>
<p style="margin:4px 0 8px">3D 모델의 구조와 객체를 자동 확인합니다. 현장 측정이 필요한 항목은 임의로 채우지 않습니다.</p>
<button id="autoAnalyze" style="background:#145b7a;color:white;font-weight:bold;border:0">자동 분석 및 점수 계산</button>
<button id="peopleToggle">인물 시뮬레이션 일시정지</button>
<button id="waterRegenerate">가상 물기 배치 다시 생성</button>
<div style="margin-top:8px;padding:8px;background:#f2f7fa;border-radius:7px"><label for="luxAdjust" style="margin:0 0 4px">조도 시뮬레이션 보정 <span id="luxAdjustLabel">0 lux</span></label><input id="luxAdjust" type="range" min="-180" max="180" step="10" value="0" style="width:100%"><div style="font-size:10px;color:#526b7e">실측값이 아닌 시뮬레이션 값입니다. 변경 후 자동 분석을 다시 실행하세요.</div></div>
<div style="margin-top:8px;padding:9px;background:#eef6fb;border:1px solid #c8dce8;border-radius:7px">
<strong style="font-size:12px">층별 조도 설정 (시뮬레이션)</strong>
<label for="floorLuxSelect" style="margin-top:6px">조정할 층</label><select id="floorLuxSelect" style="width:100%;padding:6px"><option value="1">1층</option></select>
<label for="floorLuxRange" style="margin-top:6px">조도 <span id="floorLuxValue">400 lux</span></label><input id="floorLuxRange" type="range" min="0" max="1500" step="10" value="400" style="width:100%">
<input id="floorLuxNumber" type="number" min="0" max="1500" step="10" value="400" style="width:100%;padding:6px;box-sizing:border-box">
<div id="floorLuxComparison" style="font-size:11px;line-height:1.6;margin-top:7px">층별 조도 설정을 변경하면 점수를 다시 계산합니다.</div>
<div style="font-size:10px;line-height:1.5;color:#526b7e;margin-top:5px">사용자 입력 시뮬레이션값이며 실측 조도가 아닙니다. 조도 점수·가중치(초기 20%)는 비교용 모델이며 법적 기준이 아닙니다.</div>
<button id="floorLuxReset" type="button" style="margin-top:6px">선택 층 조도 초기화</button><button id="floorLuxResetAll" type="button" style="margin-top:6px">전체 층 기본값 복원</button>
</div>
<div id="gardenStatus" style="font-size:11px;line-height:1.5;margin-top:7px;color:#31566c">스카이 가든: 자동 분석 대상에 포함됩니다.</div>
<div id="autoProgress" aria-live="polite" style="font-size:11px;line-height:1.55;margin-top:7px;color:#526b7e">분석 전 · 버튼을 눌러 모델 분석을 시작하세요.</div>
<div id="autoSummary" style="display:none;margin-top:8px;padding:9px;border-radius:7px;background:#f2f7fa">
<div id="autoScore" style="font-size:24px;font-weight:800;color:#173e58">평가 대기</div>
<div id="autoCounts" style="font-size:11px;line-height:1.6"></div>
<div id="autoLimit" style="font-size:10px;line-height:1.5;color:#526b7e;margin-top:5px"></div><div id="floorScoreGrid"></div><div id="floorScoreNote"></div>
</div>
<div id="autoFindings" style="margin-top:7px"></div>
<div class="buttons" style="margin-top:7px"><button id="autoSave">결과 저장</button><button id="autoReport">보고서 인쇄 / PDF</button></div>
<label for="autoSaved" style="margin-top:8px">저장된 분석</label><select id="autoSaved"><option value="">저장 기록 선택</option></select>
<button id="autoLoad">저장 결과 불러오기</button>
<details style="margin-top:8px"><summary style="cursor:pointer;font-size:11px;font-weight:bold">계산 방식 보기</summary><p style="margin:5px 0">모델 내 기하학적 후보를 탐색하고, 확인 가능한 형상 정보만으로 잠정 위험을 평가합니다. 단위·축척이 검증되지 않은 치수는 법적 기준과 직접 비교하지 않습니다. 실제 조도, 바닥 마찰, 문턱, 시간대별 밀집도는 모델만으로 알 수 없어 미측정으로 표시합니다.</p><p style="margin:5px 0">초기 점수식: S = 100 × exp(−D − λI). 계수는 프로젝트 비교용 초기값이며 검증된 안전 인증 점수가 아닙니다.</p></details>
</div>
<details id="legacyTools"><summary style="cursor:pointer;font-size:12px;font-weight:bold;color:#31566c;margin:10px 0">고급 설정 · 기존 50개 점검표 / 수동 측정</summary>
<div id="accessPanel">
<h3>접근성 불편 요소 50개</h3>
<div id="accessLegend"><span class="legendChip">A 이동·공간</span><span class="legendChip">B 조작·도달</span><span class="legendChip">C 화장실</span><span class="legendChip">D 정보·의사소통</span><span class="legendChip">E 비상·환경</span></div>
<select id="accessFilter"><option value="all">전체 분류 · 50개</option><option value="A">A · 이동 및 공간 이용</option><option value="B">B · 시설 조작 및 도달 범위</option><option value="C">C · 화장실 및 위생시설</option><option value="D">D · 정보 인식 및 의사소통</option><option value="E">E · 비상 상황 및 실내 환경</option></select>
<select id="accessItem"><option value="">항목 선택 또는 3D 마커 클릭</option></select>
<div id="accessSummary">번호 마커를 선택하면 위치와 영향 분석이 표시됩니다. 마커 위치는 모델에서 확인 가능한 시설 또는 제안 위치이며, 현장 실측을 대신하지 않습니다.</div>
<select id="accessRating" aria-label="접근성 평가"><option value="확인 필요">평가: 확인 필요</option><option>양호</option><option>경미</option><option>보통</option><option>심각</option><option>위험</option></select>
<textarea id="accessEvidence" placeholder="평가 근거 또는 측정값 기록 (확인되지 않은 값은 추정하지 마세요)"></textarea>
<button id="accessSave">평가 기록 저장</button>
<button id="accessImprove">개선안 제안 / 상태 전환</button>
<div id="accessCompare" class="legendChip">개선 전후: 아직 기록 없음</div>
</div>
<div id="mobilityPanel">
<h3>통합 이동 편의 평가</h3>
<div class="mobSmall">측정·관찰 데이터를 입력하면 100점에서 개별 위험과 복합 위험을 반영합니다. 점수는 비교용 프로젝트 지표이며 사고 확률·법적 인증 점수가 아닙니다.</div>
<label for="mobSpace">평가 공간</label><select id="mobSpace"><option value="">공간 선택</option></select>
<div class="mobGrid">
 <div class="mobField"><label for="mobWidth">유효 통로 폭 (m)</label><input id="mobWidth" type="number" min="0" max="20" step="0.01" placeholder="미측정"></div>
 <div class="mobField"><label for="mobThreshold">문턱·단차 (cm)</label><input id="mobThreshold" type="number" min="0" max="100" step="0.1" placeholder="미측정"></div>
 <div class="mobField"><label for="mobDensity">밀집도 (명/m²)</label><input id="mobDensity" type="number" min="0" max="100" step="0.01" placeholder="미측정"></div>
 <div class="mobField"><label for="mobLux">조도 (lux)</label><input id="mobLux" type="number" min="0" max="100000" step="1" placeholder="미측정"></div>
</div>
<label for="mobFloorState">바닥 상태 (관찰 기반, 미끄럼 시험 대체 불가)</label>
<select id="mobFloorState"><option value="">미조사</option><option value="dry">건조 상태 관찰(성능 미검증)</option><option value="wet">젖음 확인</option><option value="ice">결빙 확인</option><option value="tested">미끄럼 성능 시험으로 위험 없음 확인</option></select>
<div class="mobGrid">
 <div class="mobField"><label for="mobMaterial">바닥 재질</label><input id="mobMaterial" placeholder="예: 타일(재질만으로 판정 안 함)"></div>
 <div class="mobField"><label for="mobMeasureTime">측정 일시</label><input id="mobMeasureTime" type="datetime-local"></div>
</div>
<label for="mobSource">자료 출처 / 증빙</label><input id="mobSource" placeholder="현장 측정, 도면명, 사진 파일명 등">
<label for="mobMethod">측정 방법 및 조건</label><input id="mobMethod" placeholder="측정 위치·기기·측정 조건">
<label style="display:flex;gap:5px;align-items:center;font-weight:normal"><input id="mobVerified" type="checkbox"> 입력값과 증빙을 확인함</label>
<label style="display:flex;gap:5px;align-items:center;font-weight:normal"><input id="mobExtreme" type="checkbox"> 사전 정의된 극단 위험 조건이 실제로 확인됨</label>
<input id="mobExtremeReason" placeholder="극단 위험 근거 (필수, 예: 실제 통로 완전 차단)">
<div class="mobResult"><div id="mobScore">평가 자료 부족</div><div id="mobStatus" class="mobSmall">미조사 항목은 정상(위험 0)으로 간주하지 않습니다.</div><div class="mobBar"><div id="mobBarFill"></div></div><div id="mobDetails">필수 측정값을 입력하세요.</div></div>
<div class="mobGrid">
 <button id="mobCalculate">점수 계산</button><button id="mobSave">평가 저장</button>
 <button id="mobLoad">선택 평가 불러오기</button><button id="mobReport">인쇄용 보고서</button>
</div>
<label for="mobSavedList">저장된 평가</label><select id="mobSavedList"><option value="">저장 기록 선택</option></select>
<div class="mobSetting">
 <strong style="font-size:11px">평가 기준·계수 설정</strong>
 <div class="mobGrid">
  <div class="mobField"><label for="cfgWidth">통로 폭 기준 (m)</label><input id="cfgWidth" type="number" min="0.1" max="5" step="0.05" value="1.2"></div>
  <div class="mobField"><label for="cfgNarrow">좁은 폭 참고 (m)</label><input id="cfgNarrow" type="number" min="0.1" max="3" step="0.05" value="0.9"></div>
  <div class="mobField"><label for="cfgThreshold">단차 비교 기준 (cm)</label><input id="cfgThreshold" type="number" min="0.1" max="20" step="0.1" value="2"></div>
  <div class="mobField"><label for="cfgLux">조도 기준 (lux)</label><input id="cfgLux" type="number" min="1" max="10000" step="10" value="400"></div>
  <div class="mobField"><label for="cfgDensity">밀집도 기준 (명/m²)</label><input id="cfgDensity" type="number" min="0.1" max="20" step="0.1" value="1"></div>
  <div class="mobField"><label for="cfgLambda">복합 영향 λ</label><input id="cfgLambda" type="number" min="0" max="5" step="0.05" value="0.8"></div>
  <div class="mobField"><label for="wWidth">폭 가중치</label><input id="wWidth" type="number" min="0" max="5" step="0.05" value="0.7"></div>
  <div class="mobField"><label for="wThreshold">단차 가중치</label><input id="wThreshold" type="number" min="0" max="5" step="0.05" value="0.45"></div>
  <div class="mobField"><label for="wFloor">바닥 가중치</label><input id="wFloor" type="number" min="0" max="5" step="0.05" value="0.5"></div>
  <div class="mobField"><label for="wDensity">밀집도 가중치</label><input id="wDensity" type="number" min="0" max="5" step="0.05" value="0.5"></div>
  <div class="mobField"><label for="wLux">조도 가중치</label><input id="wLux" type="number" min="0" max="5" step="0.05" value="0.35"></div>
  <div class="mobField"><label for="cfgInteraction">쌍별 상호작용 cᵢⱼ</label><input id="cfgInteraction" type="number" min="0" max="5" step="0.05" value="0.3"></div>
 </div>
 <div class="mobSmall">초기 계수는 검증된 통계값이 아닌 프로젝트 시작값입니다. 1.2m는 복도·통로의 비교 기준으로, 0.9m는 좁은 폭 참고값으로 둡니다. 적용 법령은 시설 종류·용도·신축/기존 여부에 따라 확인해야 합니다. 2cm와 400lux 역시 조건별 기준 확인이 필요하며, 400lux는 프로젝트 비교값입니다.</div>
 <button id="mobRecalc">기준 변경 반영 및 재계산</button>
</div>
<div id="mobilityPrint" style="display:none"></div>
</div>
</details>
</section>

<div id="toplabel">31 FLOORS · SPACED INTERIOR · REALISTIC INTERIOR</div>
<section id="safetyPanel" aria-label="층별 안전도">
<h3 id="safetyTitle">평가 자료 분석</h3>
<div id="floorHazardOverview" style="margin:10px 0 14px;padding:12px;background:#f7fafc;border:1px solid #d6e0e8;border-radius:12px">
 <h4 style="margin:0 0 5px;font-size:15px">층별 위험 물체·위험 요소와 안전도</h4>
 <p style="font-size:11px;line-height:1.55;color:#5c6f7c;margin:4px 0 10px">각 층에 등록된 시설·위험 후보의 우선순위를 점수로 환산합니다. 안전도 = 100 − 층별 위험 점수 합계(최대 100점 감점). 아래는 현재 3D 모델의 시설 설명과 제안 위치를 이용한 잠정 평가이며, 실제 현장 확인이 아닌 항목은 ‘후보’로 표시됩니다.</p>
 <div id="floorHazardSummary" style="font-size:12px;font-weight:700;margin-bottom:8px">층별 자료를 계산하는 중입니다.</div>
 <div id="floorHazardCards"></div>
</div>
<div id="evidencePanel">
 <h4 id="evidenceFloorTitle">현재 선택 공간 · 전체 건물</h4>
 <div id="evidenceStatus" class="evidenceMeta">분석 전 · 선택한 층의 등록 자료를 확인할 수 있습니다.</div>
 <button id="evidenceAnalyze" type="button">분석하기</button>
 <div id="evidenceResults" aria-live="polite"><div class="evidenceMeta">분석하기를 누르면 등록된 자료와 미확인 항목이 표시됩니다.</div></div>
</div>
<div id="safetyScore">평가 대기</div>
<div id="safetyMeta">등록된 위험 요소 중 근거가 확인된 항목만 점수에 반영합니다. 아직 조사하지 않은 층은 안전하다고 간주하지 않습니다.</div>
<div id="riskFloors"></div>
<div id="riskList"></div>
<hr style="border:0;border-top:1px solid #d6e0e6;margin:8px 0">
<strong>위험 요소 등록</strong>
<select id="riskItemSelect" aria-label="위험 요소 시설 선택"></select>
<select id="riskSeverity" aria-label="위험 수준"><option value="경미">경미 · -2</option><option value="주의">주의 · -5</option><option value="심각">심각 · -10</option><option value="긴급">긴급 · -20</option></select>
<input id="riskCause" placeholder="발생 원인·확인 근거 입력" aria-label="발생 원인 및 근거">
<label style="display:flex;align-items:center;gap:5px;font-weight:normal;margin-top:5px"><input id="riskVerified" type="checkbox"> 현장 또는 자료로 위험 확인됨</label>
<button id="riskAdd">위험 요소 등록</button>
<button id="markFloorSurveyed">선택 층 조사 완료 표시</button>
<div style="color:#657786;line-height:1.45;margin-top:5px">확인하지 않은 항목은 등록되지만 점수에는 반영되지 않습니다. 모델 좌표는 관련 시설의 기준 위치이며 실측 좌표가 아닐 수 있습니다.</div>
</section>
<div id="hint">
드래그: 시점 회전<br>
휠: 확대 / 축소<br>
층 선택: 해당 층 확대<br>
방 클릭: 공간 정보 확인
</div>

<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>
<script>
(() => {
const host=document.getElementById('view');
if(!window.THREE){
document.getElementById('description').textContent='3D 라이브러리를 불러오지 못했습니다. 인터넷 연결을 확인하세요.';
return;
}

const scene=new THREE.Scene();
scene.background=new THREE.Color(0xdce5ec);
scene.fog=new THREE.Fog(0xe6e7e4,85,190);

const camera=new THREE.PerspectiveCamera(39.6,innerWidth/innerHeight,.1,500) // 50mm full-frame equivalent field of view;
const renderer=new THREE.WebGLRenderer({antialias:true});
renderer.setPixelRatio(Math.min(devicePixelRatio,2));
renderer.setSize(innerWidth,innerHeight);
renderer.shadowMap.enabled=true;
renderer.shadowMap.type=THREE.PCFSoftShadowMap;
renderer.shadowMap.enabled=true;
renderer.setPixelRatio(Math.min(devicePixelRatio,2));
renderer.shadowMap.autoUpdate=true;
renderer.toneMappingExposure=1.12;
renderer.outputColorSpace=THREE.SRGBColorSpace;
renderer.physicallyCorrectLights=true;
renderer.setClearColor(0xdce5ec,1);
renderer.toneMapping=THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure=1.0;
renderer.outputColorSpace=THREE.SRGBColorSpace;
host.appendChild(renderer.domElement);

scene.add(new THREE.HemisphereLight(0xf3f8ff,0x77736a,1.25));
const ambientFill=new THREE.AmbientLight(0xffffff,0.28);
scene.add(ambientFill);

const sun=new THREE.DirectionalLight(0xfff0dc,2.7);
sun.position.set(22,48,26);
sun.castShadow=true;
sun.shadow.mapSize.set(3072,3072);
sun.shadow.camera.left=-35; sun.shadow.camera.right=35; sun.shadow.camera.top=65; sun.shadow.camera.bottom=-35;
sun.shadow.bias=-0.00015; sun.shadow.normalBias=0.025;
scene.add(sun);

const fill=new THREE.DirectionalLight(0xa4d6ff,1.1);
fill.position.set(-20,18,-20);
scene.add(fill);

// Procedural surface maps: subtle photographic grain without external image assets.
// Canvas textures are intentionally low-contrast to avoid a cartoon-like tiled appearance.
function surfaceTexture(type, repeatX=2, repeatY=2){
  const c=document.createElement('canvas'); c.width=512; c.height=512;
  const ctx=c.getContext('2d');
  if(type==='tile'){
    ctx.fillStyle='#bdbbb4'; ctx.fillRect(0,0,512,512);
    const step=64;
    for(let y=0;y<512;y+=step){ for(let x=0;x<512;x+=step){
      const v=184+Math.floor(Math.random()*15);
      ctx.fillStyle=`rgb(${v},${v-1},${v-5})`; ctx.fillRect(x+1,y+1,step-2,step-2);
      ctx.strokeStyle='rgba(255,255,255,.22)'; ctx.lineWidth=1; ctx.strokeRect(x+2,y+2,step-4,step-4);
    }}
  } else if(type==='wood'){
    ctx.fillStyle='#9b7959'; ctx.fillRect(0,0,512,512);
    for(let y=0;y<512;y+=32){
      const v=105+Math.floor(Math.random()*35);
      ctx.fillStyle=`rgb(${v+45},${v+20},${v})`; ctx.fillRect(0,y,512,30);
      ctx.strokeStyle='rgba(48,31,18,.22)'; ctx.lineWidth=1; ctx.beginPath(); ctx.moveTo(0,y+4); ctx.lineTo(512,y+4); ctx.stroke();
      for(let i=0;i<24;i++){
        const x=Math.random()*512, len=10+Math.random()*70;
        ctx.strokeStyle=`rgba(55,35,20,${.04+Math.random()*.1})`; ctx.beginPath(); ctx.moveTo(x,y+Math.random()*27); ctx.lineTo(Math.min(512,x+len),y+Math.random()*27); ctx.stroke();
      }
    }
  } else if(type==='concrete'){
    ctx.fillStyle='#c5c4bf'; ctx.fillRect(0,0,512,512);
    for(let i=0;i<15000;i++){
      const x=Math.random()*512, y=Math.random()*512, a=.015+Math.random()*.07;
      ctx.fillStyle=Math.random()>.5?`rgba(255,255,255,${a})`:`rgba(45,45,42,${a})`;
      ctx.fillRect(x,y,1+Math.random()*2,1+Math.random()*2);
    }
  } else if(type==='carpet'){
    ctx.fillStyle='#858783'; ctx.fillRect(0,0,512,512);
    for(let i=0;i<24000;i++){
      const v=Math.random()>.5?255:0;
      ctx.fillStyle=`rgba(${v},${v},${v},${.015+Math.random()*.035})`;
      ctx.fillRect(Math.random()*512,Math.random()*512,1,1);
    }
  }
  const tex=new THREE.CanvasTexture(c);
  tex.wrapS=THREE.RepeatWrapping; tex.wrapT=THREE.RepeatWrapping;
  tex.repeat.set(repeatX,repeatY); tex.colorSpace=THREE.SRGBColorSpace;
  tex.anisotropy=8;
  return tex;
}
const tileMap=surfaceTexture('tile',3,3);
const woodMap=surfaceTexture('wood',2,3);
const concreteMap=surfaceTexture('concrete',2,2);
const carpetMap=surfaceTexture('carpet',2,2);

const mats={
concrete:new THREE.MeshStandardMaterial({color:0xd7d6d0,roughness:.96,map:concreteMap}),
wall:new THREE.MeshStandardMaterial({color:0xe8e3d9,roughness:.94, bumpMap:concreteMap, bumpScale:.035}),
wall2:new THREE.MeshStandardMaterial({color:0xc9c9c2,roughness:.9}),
floor:new THREE.MeshStandardMaterial({color:0xaaa9a4,roughness:.92,map:tileMap}),
wood:new THREE.MeshStandardMaterial({color:0x9b704b,roughness:.62,map:woodMap}),
darkwood:new THREE.MeshStandardMaterial({color:0x594638,roughness:.82,map:woodMap}),
glass:new THREE.MeshPhysicalMaterial({color:0x8dbbd0,metalness:.25,roughness:.2,transparent:true,opacity:.48}),
frame:new THREE.MeshStandardMaterial({color:0x263746,metalness:.5,roughness:.32}),
blue:new THREE.MeshStandardMaterial({color:0x164e91,roughness:.65}),
black:new THREE.MeshStandardMaterial({color:0x252a30,roughness:.72}),
white:new THREE.MeshStandardMaterial({color:0xf7f5ef,roughness:.68}),
green:new THREE.MeshStandardMaterial({color:0x477b58,roughness:.9}),
plantpot:new THREE.MeshStandardMaterial({color:0xb7a28a,roughness:.8}),
metal:new THREE.MeshStandardMaterial({color:0xb7c4cc,metalness:.72,roughness:.24}),
highlight:new THREE.MeshStandardMaterial({color:0x19c5df,emissive:0x075568,roughness:.6})
};

const root=new THREE.Group();
scene.add(root);

const floorGroups=[];
const pickables=[];
const roomMeshes=[];

const FLOOR_H=3.25;
const FLOORS=31;
const W=22;
const D=17;

function box(parent,x,y,z,w,h,d,material,meta){
const mesh=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),material);
mesh.position.set(x,y,z);
mesh.castShadow=true;
mesh.receiveShadow=true;
if(meta){
mesh.userData={...meta,originalMaterial:material};
pickables.push(mesh);
}
parent.add(mesh);
return mesh;
}

function cylinder(parent,x,y,z,r,h,material,segments=12){
const m=new THREE.Mesh(new THREE.CylinderGeometry(r,r,h,segments),material);
m.position.set(x,y,z);
m.castShadow=true;
parent.add(m);
return m;
}

function addTrashCan(parent,x,z){
  const bodyMat=new THREE.MeshStandardMaterial({color:0x343a3d,metalness:.42,roughness:.38});
  const rimMat=new THREE.MeshStandardMaterial({color:0x8e9698,metalness:.78,roughness:.24});
  const innerMat=new THREE.MeshStandardMaterial({color:0x181c1e,roughness:.8});
  // small, floor-standing commercial waste bin with a rolled rim and visible opening
  cylinder(parent,x,.34,z,.22,.62,bodyMat,24);
  cylinder(parent,x,.655,z,.235,.055,rimMat,24);
  cylinder(parent,x,.688,z,.177,.012,innerMat,24);
  cylinder(parent,x,.055,z,.205,.055,bodyMat,24);
  const label=new THREE.Mesh(new THREE.PlaneGeometry(.10,.055),new THREE.MeshStandardMaterial({color:0xb9c3c4,metalness:.3,roughness:.35}));
  label.position.set(x,.42,z+.222); parent.add(label);
}

function room(parent,name,desc,x,z,w,d,opts={}){
const y=opts.y ?? 0;
const floorMat=opts.floorMat || mats.floor;
const fm=box(parent,x,y+.045,z,w,.09,d,floorMat,{
kind:'room',
name,
desc,
floor:opts.floor
});
fm.userData.room=true;
roomMeshes.push(fm);
return fm;
}

let chairSequence=1;
const chairSeats=[];
function chair(parent,x,y,z,rot=0){
const g=new THREE.Group();
g.position.set(x,y,z);
g.rotation.y=rot;
let floor=1,ancestor=parent;
while(ancestor){if(Number.isFinite(ancestor.userData?.floor)){floor=ancestor.userData.floor;break;}ancestor=ancestor.parent;}
g.userData={kind:'chair-seat',seatId:chairSequence++,floor,seatAvailable:true,canSit:true,approachYaw:rot,occupiedBy:null};
parent.add(g);
chairSeats.push(g);

box(g,0,.38,0,.42,.12,.42,mats.black);
box(g,0,.58,-.17,.42,.38,.09,mats.black);
cylinder(g,0,.17,0,.045,.28,mats.metal,8);

for(const dx of [-.14,.14]){
for(const dz of [-.14,.14]){
box(g,dx,.055,dz,.035,.11,.035,mats.black);
}
}
}

function desk(parent,x,y,z,w=1.5,d=.72){
box(parent,x,y+.72,z,w,.09,d,mats.white);

for(const dx of [-w*.42,w*.42]){
for(const dz of [-d*.35,d*.35]){
box(parent,x+dx,y+.35,z+dz,.055,.7,.055,mats.metal);
}
}

box(parent,x,y+.82,z-.12,.36,.28,.035,mats.black);
box(parent,x,y+.79,z+.17,.3,.025,.13,mats.wall2);
}

function sofa(parent,x,y,z,w=1.8){
box(parent,x,y+.32,z,w,.35,.72,mats.darkwood);
box(parent,x,y+.58,z-.28,w,.25,.16,mats.darkwood);
box(parent,x,y+.51,z,w-.12,.12,.55,mats.white);
}

function plant(parent,x,y,z,scale=1){
cylinder(parent,x,y+.18*scale,z,.19*scale,.36*scale,mats.plantpot);

const crown=new THREE.Mesh(
new THREE.IcosahedronGeometry(.43*scale,1),
mats.green
);
crown.position.set(x,y+.72*scale,z);
crown.castShadow=true;
parent.add(crown);

for(let i=0;i<4;i++){
const leaf=new THREE.Mesh(
new THREE.IcosahedronGeometry(.22*scale,0),
mats.green
);
leaf.position.set(
x+Math.cos(i*Math.PI/2)*.28*scale,
y+.65*scale,
z+Math.sin(i*Math.PI/2)*.28*scale
);
parent.add(leaf);
}
}

function meetingTable(parent,x,y,z,w=2.8,d=1.15,seats=8){
box(parent,x,y+.76,z,w,.11,d,mats.white);

for(let dx of [-w*.38,w*.38]){
box(parent,x+dx,y+.38,z,.08,.72,.08,mats.metal);
}

for(let i=0;i<seats/2;i++){
let px=x-w*.36+i*(w*.72/Math.max(1,seats/2-1));
chair(parent,px,y,z-d*.72,0);
chair(parent,px,y,z+d*.72,Math.PI);
}
}

function roomWall(parent,x,y,z,w,h,d,doorGap=false){
if(!doorGap){
box(parent,x,y+h/2,z,w,h,d,mats.wall);
}else{
const gap=1.05;
const side=(w-gap)/2;

if(side>0.05){
box(parent,x-(gap+side)/2,y+h/2,z,side,h,d,mats.wall);
box(parent,x+(gap+side)/2,y+h/2,z,side,h,d,mats.wall);
}

box(parent,x,y+h-.12,z,gap,.24,d,mats.wall);
}
}

const ground=new THREE.Mesh(
new THREE.PlaneGeometry(200,200),
new THREE.MeshStandardMaterial({color:0xb9c5cb,roughness:1})
);
ground.rotation.x=-Math.PI/2;
ground.position.y=-.16;
ground.receiveShadow=true;
scene.add(ground);

box(root,0,-.02,0,W+.5,.3,D+.5,mats.concrete);

const themes={
2:['레스토랑 · 메인 키친 & 커피 바','메인 키친 · 커피 바 · 공용 테이블 · 소파석 · 팔레트석 · 테라스'],
3:['회의·협업 센터','중형 회의실 · 프레젠테이션 공간'],
4:['창의 스튜디오','프로젝트 테이블 · 아이디어 보드'],
5:['디지털 연구실','컴퓨터 워크스테이션 · 장비실'],
6:['교육·세미나 층','강의형 좌석 · 발표 공간'],
7:['도서·자료 라운지','열람 테이블 · 서가'],
8:['스타트업 허브','공용 업무석 · 팀룸'],
9:['디자인 스튜디오','작업대 · 샘플 보관실'],
10:['미디어 제작실','편집 데스크 · 방음 부스'],
11:['기술 연구실','실험 작업대 · 장비 보관'],
12:['프로젝트 오피스','팀별 업무 공간 · 소회의실'],
13:['비즈니스 라운지','응접 소파 · 미팅 테이블'],
14:['교육·세미나 층','강의형 좌석 · 발표 공간'],
15:['디지털 연구실','컴퓨터 워크스테이션 · 장비실'],
16:['회의·협업 센터','중형 회의실 · 프레젠테이션 공간'],
17:['창의 스튜디오','프로젝트 테이블 · 아이디어 보드'],
18:['도서·자료 라운지','열람 테이블 · 서가'],
19:['스타트업 허브','공용 업무석 · 팀룸'],
20:['디자인 스튜디오','작업대 · 샘플 보관실'],
21:['미디어 제작실','편집 데스크 · 방음 부스'],
22:['기술 연구실','실험 작업대 · 장비 보관'],
23:['프로젝트 오피스','팀별 업무 공간 · 소회의실'],
24:['비즈니스 라운지','응접 소파 · 미팅 테이블'],
25:['교육·세미나 층','강의형 좌석 · 발표 공간'],
26:['디지털 연구실','컴퓨터 워크스테이션 · 장비실'],
27:['회의·협업 센터','중형 회의실 · 프레젠테이션 공간'],
28:['창의 스튜디오','프로젝트 테이블 · 아이디어 보드'],
29:['도서·자료 라운지','열람 테이블 · 서가'],
30:['임원 업무층','개인 사무실 · 회의실'],
31:['전망 라운지','소파 · 카페 테이블 · 파노라마 창']
};

function buildFloor(f){
const g=new THREE.Group();
g.position.y=(f-1)*FLOOR_H;
g.userData.floor=f;
root.add(g);
floorGroups.push(g);

const floorMat=f===1
?new THREE.MeshStandardMaterial({color:0xb6b0a5,roughness:.88,map:tileMap})
:(f%3===0
?new THREE.MeshStandardMaterial({color:0x8f9699,roughness:.92,map:carpetMap})
:mats.floor);

box(g,0,0,0,W,.16,D,floorMat);

// 2층은 일반 사무실 구조를 먼저 생성하면 벽과 코어가 식당 가구를 가리므로
// 전용 레이아웃을 먼저 구성하고 반환합니다. 외곽 벽은 컷어웨이 형태로 낮게 둡니다.
if(f===2){
  const tile=new THREE.MeshStandardMaterial({color:0xc9c6bd,roughness:.96,map:tileMap});
  const woodFloor=new THREE.MeshStandardMaterial({color:0x9b7655,roughness:.86});
  const darkTile=new THREE.MeshStandardMaterial({color:0x777b7a,roughness:.9});
  // 밝은 타일 바닥과 후면 주방 바닥
  box(g,0,.105,0,W-.3,.055,D-.3,tile);
  box(g,-6.9,.145,-5.0,6.5,.07,5.7,woodFloor);
  box(g,8.8,.145,1.0,3.8,.07,7.5,woodFloor);
  // 외곽 벽: 후면과 좌우 일부만 두어 위에서 내부가 잘 보이게 함
  box(g,0,1.35,-D/2+.12,W,2.7,.22,mats.wall2);
  // Left-side restroom extension entrance: split the original wall to leave a real opening.
  box(g,-W/2+.12,1.15,(-D/2-2.35)/2,.22,2.3,(-2.35+D/2),mats.wall2);
  box(g,-W/2+.12,1.15,( -0.95+D/2)/2,.22,2.3,(D/2+0.95),mats.wall2);
  box(g,W/2-.12,1.15,-4.6,.22,2.3,7.0,mats.wall2);
  // 후면 왼쪽 메인 키친: 조리대, 싱크, 냉장고, 조리기구
  box(g,-6.9,.22,-5.0,6.4,.12,5.5,darkTile);
  box(g,-6.8,.72,-6.8,5.5,.95,.72,mats.white);
  box(g,-6.8,1.22,-6.8,5.6,.08,.76,mats.metal);
  for(let i=0;i<4;i++){
    const x=-8.9+i*1.4;
    box(g,x,1.28,-6.8,.72,.07,.5,mats.black);
    box(g,x,1.33,-6.8,.48,.035,.3,mats.metal);
  }
  for(let i=0;i<3;i++){
    const x=-9.0+i*2.0;
    box(g,x,.75,-3.25,1.55,1.15,.65,mats.wall2);
  }
  // 위 블록은 단순한 수납장으로 교체: 높이/좌표를 명시해 렌더링 오류 방지
  for(let i=0;i<3;i++){
    const x=-9.0+i*2.0;
    box(g,x,.75,-3.25,1.55,1.15,.65,mats.wall2);
    box(g,x,1.35,-3.25,1.6,.08,.7,mats.metal);
  }
  // 주방과 홀 사이 파티션 및 서빙 통로
  box(g,-3.35,1.0,-4.9,.12,1.8,4.4,mats.frame);
  box(g,-3.35,1.75,-4.9,.18,.08,4.4,mats.metal);
  // 커피 바: 긴 카운터, 상판, 머신과 컵
  box(g,-6.4,.62,-1.25,6.4,1.0,.95,mats.darkwood);
  box(g,-6.4,1.15,-1.25,6.55,.12,1.05,mats.black);
  box(g,-6.4,1.22,-1.25,6.25,.045,.86,mats.wood);
  for(let i=0;i<4;i++){
    const x=-8.7+i*1.55;
    box(g,x,1.48,-1.25,.48,.38,.42,mats.metal);
    cylinder(g,x,1.7,-1.25,.12,.07,mats.black,12);
  }
  // 오른쪽 저장고와 화장실: 낮은 파티션으로 분리
  box(g,4.2,1.15,-6.5,5.7,2.3,.14,mats.wall);
  box(g,1.45,1.15,-5.4,.14,2.3,2.8,mats.wall);
  box(g,4.0,.72,-5.25,1.8,1.35,.7,mats.wood);
  box(g,6.25,.72,-5.25,1.45,1.35,.7,mats.wall2);
  box(g,2.0,.72,-6.65,.8,1.35,.7,mats.white);
  // 다이닝 존: 3열의 긴 테이블과 의자
  for(let row=0;row<3;row++){
    const z=.0+row*2.15;
    box(g,1.2,.78,z,4.8,.12,.92,mats.white);
    box(g,1.2,.39,z,.12,.68,.12,mats.metal);
    for(let col=0;col<4;col++){
      const x=-.35+col*1.05;
      chair(g,x,0,z-.68,0);
      chair(g,x,0,z+.68,Math.PI);
    }
  }
  // 음식 접시·트레이는 식탁 표면에 고정해 레스토랑 용도를 명확히 보여 줍니다.
  const plateMat=new THREE.MeshStandardMaterial({color:0xf6f4ee,roughness:.32});
  const foodMat=new THREE.MeshStandardMaterial({color:0xc9783e,roughness:.7});
  const greenFoodMat=new THREE.MeshStandardMaterial({color:0x6e9b56,roughness:.8});
  for(let row=0;row<3;row++){
    const z=row*2.15;
    for(let col=0;col<3;col++){
      const x=-.15+col*1.25;
      cylinder(g,x,.86,z,.17,.025,plateMat,20);
      cylinder(g,x,.885,z,.075,.025,foodMat,14);
      cylinder(g,x+.07,.90,z+.035,.025,.015,greenFoodMat,10);
    }
  }
  // A small procedural chef stands inside the kitchen work zone; it is a visual simulation, not a scanned human model.
  const chef=new THREE.Group();chef.userData={kind:'restaurant-chef',floor:2,zone:'주방',synthetic:true};chef.position.set(-8.6,0,-4.8);chef.rotation.y=Math.PI;
  const chefSkin=new THREE.MeshStandardMaterial({color:0xb98260,roughness:.85});
  const chefCoat=new THREE.MeshStandardMaterial({color:0xf0eee7,roughness:.82});
  const chefPants=new THREE.MeshStandardMaterial({color:0x303942,roughness:.9});
  const chefHatMat=new THREE.MeshStandardMaterial({color:0xffffff,roughness:.7});
  function chefPart(geo,mat,x,y,z,sx=1,sy=1,sz=1){const m=new THREE.Mesh(geo,mat);m.position.set(x,y,z);m.scale.set(sx,sy,sz);m.castShadow=true;m.receiveShadow=true;chef.add(m);return m;}
  chefPart(new THREE.CapsuleGeometry(.15,.32,4,8),chefCoat,0,1.08,0,.92,1,.72);
  chefPart(new THREE.CapsuleGeometry(.105,.28,3,8),chefPants,-.075,.48,0,.8,1,.8);
  chefPart(new THREE.CapsuleGeometry(.105,.28,3,8),chefPants,.075,.48,0,.8,1,.8);
  chefPart(new THREE.SphereGeometry(.12,16,12),chefSkin,0,1.48,0,1,1.12,.95);
  chefPart(new THREE.CylinderGeometry(.12,.13,.14,16),chefHatMat,0,1.68,0);
  chefPart(new THREE.SphereGeometry(.105,14,10),chefHatMat,0,1.77,0,1,1,.85);
  const chefArmL=chefPart(new THREE.CapsuleGeometry(.045,.28,3,7),chefCoat,-.20,1.13,-.02,1,1,1);chefArmL.rotation.z=-.62;
  const chefArmR=chefPart(new THREE.CapsuleGeometry(.045,.28,3,7),chefCoat,.20,1.13,-.02,1,1,1);chefArmR.rotation.z=.62;
  chef.userData.animatedArms=[chefArmL,chefArmR];g.add(chef);

  // 왼쪽 창가 그룹석: 원형 테이블과 네 좌석씩
  for(let i=0;i<3;i++){
    const z=.2+i*2.25;
    cylinder(g,-9.0,.78,z,.72,.12,mats.white,24);
    cylinder(g,-9.0,.39,z,.09,.68,mats.metal,12);
    for(let a=0;a<4;a++){
      const ang=a*Math.PI/2;
      chair(g,-9.0+Math.cos(ang)*.95,0,z+Math.sin(ang)*.95,ang);
    }
  }
  // 오른쪽 소파 라운지와 낮은 테이블
  sofa(g,7.0,0,-.2,2.4); sofa(g,7.0,0,1.0,2.4);
  box(g,7.0,.42,.4,1.15,.09,.65,mats.wood);
  sofa(g,7.0,0,4.0,2.0); sofa(g,8.3,0,5.1,1.8);
  box(g,7.7,.42,4.65,1.0,.09,.62,mats.wood);
  // 테라스 가장자리, 난간, 화분
  box(g,9.0,.12,1.0,3.2,.08,7.2,woodFloor);
  box(g,10.55,.65,1.0,.08,1.05,7.1,mats.frame);
  for(let z=-2.0;z<=4.5;z+=1.3) box(g,10.55,.62,z,.08,.95,.05,mats.metal);
  for(let z=-2.0;z<=4.8;z+=2.1) plant(g,9.55,0,z,.7);
  // 입구와 안내/픽업 카운터
  box(g,-2.8,.58,7.55,2.6,1.0,.55,mats.darkwood);
  box(g,-2.8,1.1,7.55,2.65,.08,.6,mats.white);
  box(g,-2.8,1.35,7.55,1.2,.32,.07,mats.blue);
  // 조명과 안내 표지
  for(let x=-9;x<=9;x+=3) box(g,x,2.38,7.7,.55,.035,.12,new THREE.MeshStandardMaterial({color:0xffe7b0,emissive:0x59401b}));
  const sign=box(g,0,2.05,-8.35,4.0,.42,.08,mats.blue);
  sign.userData={kind:'room',floor:2,name:'2층 레스토랑',desc:'메인 키친 · 커피 바 · 공용 다이닝 · 그룹석 · 소파 라운지 · 테라스'};
  pickables.push(sign);
  return g;
}

const wallH=2.45;
const t=.16;

// Left exterior wall is split at the shared doorway to the restroom wing.
const leftDoorCenterZ=-1.65, leftDoorWidth=1.4;
const leftDoorStart=leftDoorCenterZ-leftDoorWidth/2, leftDoorEnd=leftDoorCenterZ+leftDoorWidth/2;
box(g,-W/2,wallH/2,(-D/2+leftDoorStart)/2,t,wallH,leftDoorStart+D/2,mats.wall);
box(g,-W/2,wallH/2,(leftDoorEnd+D/2)/2,t,wallH,D/2-leftDoorEnd,mats.wall);
box(g,-W/2,wallH-.18,leftDoorCenterZ,t,.36,leftDoorWidth,mats.wall);
// 본관 오른쪽 외벽은 확장 구역 연결문 위치를 비워 두어 통로가 실제로 뚫리도록 분할합니다.
const connectorCenterZ=-1.65;
const connectorOpening=1.4;
const rightWallStart=-D/2, rightWallEnd=D/2;
const openingStart=connectorCenterZ-connectorOpening/2;
const openingEnd=connectorCenterZ+connectorOpening/2;
box(g,W/2,wallH/2,(rightWallStart+openingStart)/2,t,wallH,openingStart-rightWallStart,mats.wall);
box(g,W/2,wallH/2,(openingEnd+rightWallEnd)/2,t,wallH,rightWallEnd-openingEnd,mats.wall);
box(g,W/2,wallH-.18,connectorCenterZ,t,.36,connectorOpening,mats.wall); // 문 위쪽 벽만 유지
box(g,0,wallH/2,-D/2,W,wallH,t,mats.wall);

for(let x=-W/2+1;x<W/2;x+=1.4){
box(g,x,1.25,D/2-.04,.055,2.35,.07,mats.frame);
}

box(g,0,2.43,D/2-.02,W,.07,.12,mats.frame);
box(g,-5.5,.6,D/2,.12,1.2,.12,mats.wall);
box(g,5.5,.6,D/2,.12,1.2,.12,mats.wall);
box(g,0,.08,D/2,11,.12,.16,mats.frame);

// 기존 본관 내부의 엘리베이터 문·프레임·호출 버튼은 제거했습니다.

const label=f===1?'로비':themes[f][0];
const detail=f===1
?'리셉션 · 대기 라운지 · 방문객 안내 · 엘리베이터 코어'
:themes[f][1];

const floorInfo={
kind:'floor',
floor:f,
name:f+'층 · '+label,
desc:detail
};

// 중앙을 가로지르며 떠 있는 것처럼 보이던 긴 선택용 막대는 제거했습니다.

if(f===1){
// 1층 고급 로비: 대리석 리셉션, 미디어 월, 라운지, 한쪽으로 치운 엘리베이터 코어
const marble=new THREE.MeshStandardMaterial({color:0xd9d5cd,roughness:.24,metalness:.02,map:tileMap});
const marbleDark=new THREE.MeshStandardMaterial({color:0x383633,roughness:.24,metalness:.08});
const warmWood=new THREE.MeshStandardMaterial({color:0x806044,roughness:.52,metalness:.02,map:woodMap});
const brushedGold=new THREE.MeshStandardMaterial({color:0xb49a70,roughness:.32,metalness:.72});
const glassDoor=new THREE.MeshPhysicalMaterial({color:0x9bb8c0,roughness:.12,metalness:.18,transparent:true,opacity:.32,side:THREE.DoubleSide,depthWrite:false});
const screenMat=new THREE.MeshStandardMaterial({color:0x101820,roughness:.18,metalness:.08,emissive:0x152b3b,emissiveIntensity:.42});
const warmGlow=new THREE.MeshStandardMaterial({color:0xffe5b5,emissive:0xffd18a,emissiveIntensity:.38,roughness:.4});

// 로비 바닥: 큰 규격의 밝은 석재 타일과 짙은 대리석 인레이
box(g,0,.115,0,W-.22,.055,D-.22,marble);
for(let z=-7;z<=7;z+=3.5) box(g,0,.147,z,W-.45,.018,.025,new THREE.MeshStandardMaterial({color:0xaaa59c,roughness:.5}));
for(let x=-9;x<=9;x+=3.6) box(g,x,.148,0,.022,.018,D-.45,new THREE.MeshStandardMaterial({color:0xaaa59c,roughness:.5}));
for(const z of [-5.7,5.7]) box(g,0,.16,z,W-1.1,.025,.24,marbleDark);
for(const x of [-8.6,8.6]) box(g,x,.16,0,.22,.025,D-1.2,marbleDark);

// 왼쪽 리셉션 배경: 석재 패널, 세로 목재 루버, 간접 조명
box(g,-7.25,1.45,-3.7,7.1,2.65,.18,marble);
for(let i=0;i<8;i++) box(g,-10.45+i*.9,1.42,-3.57,.045,2.35,.055,brushedGold);
box(g,-7.25,2.72,-3.53,6.6,.055,.12,warmGlow);
// 리셉션 데스크의 두꺼운 석재 전면과 상판
box(g,-6.2,.68,-1.35,4.9,1.05,1.18,marble);
box(g,-6.2,1.22,-1.35,5.05,.13,1.28,marbleDark);
box(g,-6.2,1.30,-1.35,4.88,.055,1.13,new THREE.MeshStandardMaterial({color:0xe8e2d7,roughness:.22}));
box(g,-6.2,.72,-.745,4.25,.72,.035,warmWood);
box(g,-6.2,.76,-.71,2.6,.035,.04,brushedGold);
// 리셉션 모니터, 키보드, 작은 장식
for(const x of [-7.0,-5.35]){
  box(g,x,1.52,-1.58,.72,.43,.055,mats.black);
  box(g,x,1.53,-1.545,.64,.34,.018,new THREE.MeshStandardMaterial({color:0x253e4b,emissive:0x0a2029,emissiveIntensity:.6,roughness:.25}));
  box(g,x,1.29,-1.35,.22,.035,.22,mats.black);
}

// 오른쪽 후면의 미디어 월: TV는 벽에 밀착, 주변에 목재 패널과 얇은 프레임
box(g,1.35,1.42,-7.25,7.0,2.55,.22,warmWood);
for(let i=0;i<13;i++) box(g,-1.85+i*.52,1.42,-7.105,.025,2.35,.035,brushedGold);
box(g,2.0,1.62,-7.02,3.45,1.92,.10,marbleDark);
box(g,2.0,1.62,-6.955,3.28,1.75,.035,mats.black);
box(g,2.0,1.62,-6.925,3.17,1.64,.018,screenMat);
// TV 화면의 추상적인 풍경/브랜드 그래픽
box(g,1.55,1.88,-6.91,1.95,.035,.012,new THREE.MeshStandardMaterial({color:0x567a83,emissive:0x102d38,emissiveIntensity:.5,roughness:.4}));
box(g,2.45,1.38,-6.908,2.0,.025,.012,new THREE.MeshStandardMaterial({color:0xc0a67c,emissive:0x49331a,emissiveIntensity:.45,roughness:.45}));
box(g,2.0,.62,-6.98,3.6,.10,.28,marbleDark);

// 기존 본관 1층의 엘리베이터 문·프레임·호출 버튼은 제거했습니다.

// 중앙의 넓은 동선은 비워 두고 오른쪽/왼쪽 가장자리에만 라운지 좌석 배치
box(g,.8,.17,.0,4.5,.035,5.7,new THREE.MeshStandardMaterial({color:0xb5a58e,roughness:.9}));
sofa(g,6.5,0,2.15,2.4);
sofa(g,8.45,0,2.15,2.2);
box(g,7.45,.42,2.15,1.05,.09,.68,warmWood);
sofa(g,6.45,0,4.15,2.0);
box(g,6.45,.42,4.15,.82,.08,.58,marbleDark);
// 대기 라운지의 실제 비례에 가까운 안락의자와 테이블
for(const x of [-1.5,1.0]){
  sofa(g,x,0,3.9,1.45);
  cylinder(g,x,.42,2.75,.42,.09,marbleDark,32);
  cylinder(g,x,.48,2.75,.34,.035,new THREE.MeshStandardMaterial({color:0xd9c9ad,roughness:.25}),32);
}

// 큰 화분과 관엽식물, 로비 양 끝에 배치
plant(g,-9.45,0,3.65,1.35);
plant(g,9.25,0,5.65,1.15);
plant(g,-1.0,0,-5.4,.95);

// 외벽 유리 출입문과 금속 손잡이: 기존 커튼월 앞쪽에 겹치지 않도록 안쪽에 설치
for(const x of [-3.0,-1.0,1.0,3.0]){
  box(g,x,1.22,D/2-.42,1.88,2.28,.045,glassDoor);
  box(g,x-.94,1.22,D/2-.38,.045,2.36,.065,mats.frame);
  box(g,x+.94,1.22,D/2-.38,.045,2.36,.065,mats.frame);
  box(g,x+.58,1.22,D/2-.34,.035,.72,.045,brushedGold);
}
box(g,0,2.42,D/2-.37,9.0,.08,.12,marbleDark);

// 천장 없는 컷어웨이 화면에서도 어색하지 않은 벽면 간접광 라인
for(const x of [-9.7,-4.0,4.2,9.4]) box(g,x,2.54,-3.7,.055,.025,4.8,warmGlow);

// 선택/클릭 가능한 안내 오브젝트
const lobbySign=box(g,-6.2,1.75,-2.05,1.35,.22,.045,mats.blue,{
  kind:'room',floor:1,name:'1층 · 프리미엄 리셉션',desc:'대리석 리셉션 · 미디어 월 · 대기 라운지 · 관엽식물'
});
lobbySign.userData.room=true; roomMeshes.push(lobbySign);

room(g,'1층 · 메인 로비','고급 석재 바닥과 대리석 리셉션, 벽면 미디어 디스플레이, 대기 라운지로 구성된 메인 로비.',-1.0,0.0,4.5,5.4,{floor:f,floorMat:marble});
room(g,'관리·안내실','로비 운영과 방문객 응대를 위한 지원 공간.',-4.6,2.4,3.1,2.6,{floor:f,floorMat:warmWood});

}else if(f!==2){
// 출입구가 불필요한 개방형 층에서는 문틀/아치형 파티션을 만들지 않습니다.
// 소회의실 용도가 있는 층(f % 6 === 4)에만 출입구가 있는 파티션을 둡니다.
if(f%6===4){
  roomWall(g,-4.7,0,-3.0,3.1,2.35,.12,true);
  roomWall(g,4.7,0,-3.0,3.1,2.35,.12,true);
  roomWall(g,-4.7,0,3.0,3.1,2.35,.12,true);
  roomWall(g,4.7,0,3.0,2.35,.12,true);
}

room(g,f+'층 · '+themes[f][0]+' A','주요 업무 공간: '+themes[f][1],-4.7,-3.0,3.0,2.7,{floor:f,floorMat:f%2?mats.floor:new THREE.MeshStandardMaterial({color:0xaaa69d})});
room(g,f+'층 · 팀룸 B','소규모 협업과 집중 작업을 위한 별도 공간.',4.7,-3.0,3.0,2.7,{floor:f,floorMat:mats.floor});
room(g,f+'층 · 지원실 C','수납 및 지원 업무를 위한 보조 공간.',-4.7,3.0,3.0,2.7,{floor:f,floorMat:mats.floor});
room(g,f+'층 · 미팅룸 D','짧은 회의와 프로젝트 논의를 위한 공간.',4.7,3.0,3.0,2.7,{floor:f,floorMat:mats.floor});

if(f===31||f===32){
plant(g,-5.2,0,-3.2,1.1);
plant(g,5.2,0,3.1,1.1);
sofa(g,-4.7,0,0,1.6);
sofa(g,4.7,0,0,1.6);
cylinder(g,0,.5,3.1,.48,.12,mats.white,24);

}else if(f%5===0||f%5===3){
meetingTable(g,-4.7,0,-3.0,2.0,.9,4);
meetingTable(g,4.7,0,3.0,2.0,.9,4);
plant(g,5.4,0,-4.7,.8);

}else if(f%5===1){
for(let z=-3.5;z<=3.6;z+=2.2){
desk(g,-4.8,0,z,1.6,.7);
chair(g,-4.8,0,z+.65);
}
for(let z=-3.5;z<=3.6;z+=2.2){
desk(g,4.8,0,z,1.6,.7);
chair(g,4.8,0,z+.65);
}
plant(g,-5.5,0,4.7,.8);

}else if(f%5===2){
for(let z=-3.6;z<=3.7;z+=1.35){
box(g,-5.6,.95,z,.35,1.9,.95,mats.wood);
for(let y=.4;y<1.8;y+=.42){
box(g,-5.39,y,z,.08,.035,.83,mats.blue);
}
}
desk(g,4.7,0,-3.0,1.8,.85);
chair(g,4.7,0,-2.2);
plant(g,5.4,0,4.7,.8);

}else{
meetingTable(g,-4.7,0,-3.0,2.0,.9,4);
desk(g,4.7,0,3.0,1.7,.8);
chair(g,4.7,0,3.7);
}

// Removed legacy freestanding divider posts that appeared as unexplained floating black bars.

// 넓어진 평면을 활용한 층별 특화 인테리어: 협업석, 포커스룸, 라운지, 교육 공간
// 기존 방 배치와 겹치지 않도록 중앙 통로(z=0) 주변을 비워 두고 좌우 구역에 배치합니다.
if(f===2){
  // 2층 레스토랑: 레퍼런스의 주방-커피바-다이닝-라운지 동선을 반영
  const tile=new THREE.MeshStandardMaterial({color:0xc9c7bd,roughness:.96,map:tileMap});
  box(g,0,.10,0,W-.35,.06,D-.35,tile);
  const woodFloor=new THREE.MeshStandardMaterial({color:0x9a704d,roughness:.82});
  // 후면 왼쪽 메인 키친과 조리대
  box(g,-6.7,.13,-5.0,7.0,.08,6.0,woodFloor);
  box(g,-6.7,1.0,-7.45,7.0,1.8,.18,mats.wall2);
  box(g,-6.7,.62,-4.6,5.7,.12,1.0,mats.metal);
  box(g,-6.7,.95,-4.6,5.7,.55,.85,mats.white);
  for(let i=0;i<4;i++){
    box(g,-8.9+i*1.45,1.25,-4.6,.9,.06,.58,mats.black);
    box(g,-8.9+i*1.45,1.31,-4.6,.55,.035,.35,mats.metal);
  }
  // 싱크대, 냉장/보관 캐비닛, 조리 기구
  for(let i=0;i<3;i++){
    box(g,-9.3+i*2.25,.72,-6.5,1.7,1.25,.65,mats.wall);
    box(g,-9.3+i*2.25,1.38,-6.5,1.72,.08,.68,mats.metal);
  }
  // 커피 바: 주방 앞쪽을 따라 길게 배치
  box(g,-6.4,.62,-1.2,7.4,1.15,1.0,mats.darkwood);
  box(g,-6.4,1.22,-1.2,7.55,.12,1.08,mats.black);
  box(g,-6.4,1.30,-1.2,7.2,.05,.82,mats.wood);
  for(let i=0;i<4;i++){
    box(g,-9.0+i*1.75,1.52,-1.15,.52,.35,.42,mats.metal);
    cylinder(g,-9.0+i*1.75,1.73,-1.15,.12,.08,mats.black,12);
  }
  // 후면 오른쪽 저장고와 화장실 구역을 낮은 파티션으로 구분
  box(g,4.2,1.1,-6.6,5.7,2.1,.16,mats.wall);
  box(g,1.35,1.1,-5.2,.16,2.1,3.0,mats.wall);
  box(g,4.2,.65,-5.25,2.0,1.25,.7,mats.wood);
  box(g,6.25,.65,-5.25,1.4,1.25,.7,mats.wall2);
  box(g,1.9,.65,-6.8,.75,1.25,.65,mats.white);
  // 공용 다이닝: 3열의 긴 테이블과 양쪽 의자
  for(let row=0;row<3;row++){
    const zz=1.0+row*2.05;
    box(g,1.3,.78,zz,5.0,.12,.92,mats.white);
    for(let col=0;col<4;col++){
      const xx=-.45+col*1.15;
      chair(g,xx,0,zz-.72,0); chair(g,xx,0,zz+.72,Math.PI);
    }
    box(g,1.3,.39,zz, .12,.68,.12,mats.metal);
  }
  // 왼쪽 창가 그룹석: 원형 테이블과 의자
  for(let i=0;i<3;i++){
    const zz=1.0+i*2.15;
    cylinder(g,-9.2,.78,zz,.78,.12,mats.white,24);
    for(let a=0;a<4;a++){
      const ang=a*Math.PI/2; chair(g,-9.2+Math.cos(ang)*1.05,0,zz+Math.sin(ang)*1.05,ang);
    }
  }
  // 오른쪽 소파석과 팔레트 스타일 좌석
  sofa(g,7.2,0,1.0,3.1); sofa(g,7.2,0,2.0,3.1);
  box(g,7.2,.43,3.35,1.25,.1,.72,mats.wood);
  sofa(g,6.8,0,5.2,2.3); sofa(g,8.4,0,6.0,2.0);
  box(g,7.7,.42,5.7,1.0,.08,.65,mats.wood);
  // 테라스 느낌의 목재 바닥과 화분
  box(g,8.8,.08,-.1,2.5,.08,7.8,woodFloor);
  for(let z=-2.8;z<=6.0;z+=2.2) plant(g,9.65,0,z,.75);
  // 입구와 안내 카운터
  box(g,-3.0,.55,7.9,2.8,1.0,.55,mats.wood);
  box(g,-3.0,1.08,7.9,2.85,.08,.6,mats.white);
  box(g,-3.0,1.35,7.9,1.3,.35,.08,mats.blue);
  // 동선 유도용 바닥 표시와 조명
  for(let x=-1.5;x<=5.0;x+=1.3) box(g,x,.145,-.05,.72,.025,.045,mats.metal);
  for(let x=-9;x<=9;x+=3) box(g,x,2.35,7.9,.65,.035,.12,new THREE.MeshStandardMaterial({color:0xffe7b0,emissive:0x59401b}));
}else if(f%6===0){
  // 교육/세미나 층: 강의형 테이블과 전면 발표 보드
  box(g,0,1.35,-7.45,7.2,2.5,.16,mats.wall2);
  box(g,0,1.75,-7.34,4.8,.65,.05,mats.blue);
  for(let row=0;row<3;row++){
    for(let col=0;col<4;col++){
      const xx=-6.8+col*4.5, zz=-4.4+row*2.0;
      desk(g,xx,0,zz,2.4,.72);
      chair(g,xx,0,zz+.68);
      chair(g,xx,0,zz-.68,Math.PI);
    }
  }
}else if(f%6===1){
  // 개방형 오피스: 넓은 데스크 열과 개별 의자
  for(let row=0;row<3;row++){
    for(let col=0;col<5;col++){
      const xx=-9+col*4.5, zz=-6+row*5.4;
      box(g,xx,0.76,zz,3.0,.1,1.35,mats.white);
      box(g,xx,0.91,zz-.28,.65,.3,.035,mats.black);
      chair(g,xx-1.0,0,zz+1.0);
      chair(g,xx+1.0,0,zz+1.0);
    }
  }
}else if(f%6===2){
  // 프로젝트 협업 구역: 큰 공용 테이블과 식재
  for(let i=0;i<3;i++){
    meetingTable(g,-7.2+i*7.2,0,-5.8,4.2,1.45,8);
    meetingTable(g,-7.2+i*7.2,0,5.7,4.2,1.45,8);
  }
  plant(g,-10.0,0,7.0,.9); plant(g,10.0,0,-7.0,.9);
}else if(f%6===3){
  // 도서/자료 라운지: 양쪽 서가와 중앙 열람 테이블
  for(let side of [-1,1]){
    for(let i=0;i<5;i++){
      const zz=-6.2+i*3.0;
      box(g,side*9.4,1.05,zz,1.0,2.1,2.35,mats.wood);
      for(let shelf=0;shelf<4;shelf++) box(g,side*8.87,.35+shelf*.43,zz,.06,.035,2.1,mats.blue);
    }
  }
  for(let i=0;i<3;i++){
    meetingTable(g,-3.6+i*3.6,0,0,2.5,1.0,6);
  }
}else if(f%6===4){
  // 소회의실: 유리 파티션 느낌의 낮은 프레임과 회의 테이블
  for(let side of [-1,1]){
    for(let i=0;i<2;i++){
      const xx=side*6.8;
      const zz=-4.3+i*8.6;
      box(g,xx,1.2,zz,5.0,.08,.08,mats.frame);
      box(g,xx-2.45,1.2,zz+1.6,.08,2.4,3.2,mats.glass);
      meetingTable(g,xx,0,zz,2.7,1.15,6);
    }
  }
}else{
  // 휴게/비즈니스 라운지: 소파 그룹, 낮은 테이블, 화분
  for(let side of [-1,1]){
    sofa(g,side*7.4,0,-4.6,2.7);
    sofa(g,side*7.4,0,-2.9,2.7);
    box(g,side*7.4,0.42,-3.75,1.2,.08,.75,mats.wood);
    plant(g,side*10.1,0,5.8,.95);
    for(let i=0;i<2;i++){
      cylinder(g,side*(4.5+i*2.0),.42,5.8,.48,.1,mats.white,20);
      chair(g,side*(4.5+i*2.0),0,6.55);
    }
  }
}
}

// 층별 개성을 분명히 하는 마감·가구·사인 디테일
// 기존 평면 틀과 주요 가구는 유지하고, 용도에 맞는 시각적 단서를 추가합니다.
const accentColors={
  1:0x315f75,2:0x9a6848,3:0x426c88,4:0x9a6e43,5:0x3d8c91,6:0x496fa3,
  7:0x76583f,8:0x3d7d72,9:0x9b6d4b,10:0x343b4d,11:0x3c7e8a,12:0x536b80,
  13:0x8b725a,14:0x496fa3,15:0x3d8c91,16:0x426c88,17:0x9a6e43,18:0x76583f,
  19:0x3d7d72,20:0x9b6d4b,21:0x343b4d,22:0x3c7e8a,23:0x536b80,24:0x8b725a,
  25:0x496fa3,26:0x3d8c91,27:0x426c88,28:0x9a6e43,29:0x76583f,30:0x343b4d,31:0x4b7c8a
};
const accent=new THREE.MeshStandardMaterial({color:accentColors[f]||0x426c88,roughness:.62,metalness:.08});
const trim=new THREE.MeshStandardMaterial({color:0xd8d3c8,roughness:.55,metalness:.12});
const rugColors={3:0x536f83,4:0x9a704e,5:0x597e80,6:0x536f9a,7:0x7a624d,8:0x4d8075,9:0x9b7658,10:0x353d4e,11:0x5c7b80,12:0x687a89,13:0x8b7967,30:0x343c47,31:0x557e87};
if(f!==2){
  // 층마다 다른 러그/구역 표식으로 반복적인 평면 느낌을 줄입니다.
  if(rugColors[f]){
    const rug=new THREE.Mesh(new THREE.PlaneGeometry(f===30?5.8:4.2,f===30?3.2:2.4),new THREE.MeshStandardMaterial({color:rugColors[f],roughness:.96}));
    rug.rotation.x=-Math.PI/2; rug.position.set(f%2?-5.0:5.0,.155,f%3===0?3.9:-3.9); rug.receiveShadow=true; g.add(rug);
    box(g,f%2?-5.0:5.0,.17,f%3===0?3.9:-3.9,f===30?5.4:3.8,.025,f===30?2.8:2.0,trim);
  }
  // 벽면의 층별 사인, 얇은 몰딩과 조명 라인
  box(g,0,2.18,-8.32,5.4,.48,.10,accent);
  box(g,0,2.18,-8.255,4.95,.035,.025,mats.white);
  for(let x=-9.6;x<=9.6;x+=3.2){
    box(g,x,2.28,7.82,.72,.045,.12,new THREE.MeshStandardMaterial({color:0xffe6b5,emissive:0x70532c,emissiveIntensity:.45}));
  }
  // 창가의 실제 유리 패널과 얇은 알루미늄 멀리언
  const facadeGlass=new THREE.MeshPhysicalMaterial({color:f%2?0x9fc8d8:0xb3d4df,metalness:.22,roughness:.18,transparent:true,opacity:.27,side:THREE.DoubleSide,depthWrite:false});
  for(let i=0;i<12;i++){
    const x=-10.0+i*(20/11);
    box(g,x,1.28,D/2-.095,1.48,2.12,.035,facadeGlass);
    box(g,x-.75,1.28,D/2-.06,.045,2.22,.07,mats.frame);
    if(i%2===0) box(g,x,1.28,D/2-.055,.025,2.1,.055,trim);
  }
  box(g,0,.20,D/2-.02,W,.055,.09,accent);
  // 용도별로 식별되는 특징 오브젝트
  if([3,12,16,23,27].includes(f)){
    box(g,0,1.55,-7.12,5.8,1.55,.16,mats.black);
    box(g,0,1.55,-7.02,5.45,1.22,.035,new THREE.MeshStandardMaterial({color:0x244b64,emissive:0x102b3b,roughness:.28}));
    for(let i=0;i<5;i++) box(g,-2.0+i,0.22,-5.75,.72,.035,.12,accent);
  }else if([5,11,15,22,26].includes(f)){
    // 연구층: 실험대, 수납 모듈, 장비 표시등
    for(let i=0;i<4;i++){
      const x=-7.2+i*4.8;
      box(g,x,.86,-6.0,2.3,1.35,.82,mats.white);
      box(g,x,.88,-5.56,2.18,.06,.05,accent);
      for(let j=0;j<3;j++) box(g,x-.65+j*.65,1.58,-6.0,.16,.22,.16,mats.metal);
    }
  }else if([6,14,25].includes(f)){
    // 교육층: 전면 발표 보드와 강의실 단상
    box(g,0,.28,-6.7,4.8,.18,1.05,mats.darkwood);
    box(g,0,1.55,-7.65,6.2,1.5,.12,accent);
    box(g,0,1.55,-7.57,5.8,1.18,.025,mats.black);
  }else if([7,18,29].includes(f)){
    // 자료층: 라벨이 붙은 서가와 열람 조명
    for(let side of [-1,1]) for(let i=0;i<4;i++){
      const x=side*(8.6-i*.45), z=-5.3+i*3.2;
      box(g,x,1.02,z,.62,1.95,2.45,mats.wood);
      for(let j=0;j<4;j++) box(g,x,0.38+j*.4,z,.66,.035,2.25,accent);
      box(g,x,1.72,z-1.18,.45,.12,.025,trim);
    }
  }else if([10,21].includes(f)){
    // 미디어층: 흡음 부스와 편집 장비
    for(let side of [-1,1]) for(let i=0;i<2;i++){
      const x=side*7.5, z=-4.0+i*7.0;
      box(g,x,1.15,z,3.3,2.2,.10,mats.black);
      box(g,x,1.15,z+.07,2.9,1.85,.035,new THREE.MeshStandardMaterial({color:0x303947,roughness:.95}));
      box(g,x,1.85,z+.12,1.05,.52,.04,accent);
    }
  }else if([13,24,31].includes(f)){
    // 라운지/전망층: 따뜻한 목재 패널, 낮은 조명, 녹지
    box(g,-8.4,1.25,-1.0,.12,2.25,5.5,mats.wood);
    for(let i=0;i<7;i++) box(g,-8.31,.45+i*.25,-3.25+i*.75,.035,.025,.55,trim);
    plant(g,-8.0,0,5.4,.82); plant(g,8.0,0,-5.4,.82);
  }else if([4,9,17,20,28].includes(f)){
    // 창작/디자인층: 샘플 보드와 색상 패널
    for(let i=0;i<6;i++){
      const colors=[0xd7b18a,0x9bb9b3,0xc5cbd0,0xb4a0bd,0xd2c47e,0x7d9cb1];
      box(g,-4.5+i*1.8,1.48,-7.65,1.25,1.55,.08,new THREE.MeshStandardMaterial({color:colors[(i+f)%colors.length],roughness:.75}));
      box(g,-4.5+i*1.8,.45,6.6,1.2,.08,.7,mats.darkwood);
    }
  }else if(f===30){
    // 임원층: 프라이빗 미팅 테이블과 목재 패널
    box(g,0,1.28,-7.55,7.0,2.35,.12,mats.darkwood);
    meetingTable(g,0,0,-1.0,4.8,1.55,8);
  }else if(f===8||f===19){
    // 스타트업 층: 컬러 협업 포드와 화이트보드
    for(let i=0;i<4;i++){
      const x=-7.5+i*5.0;
      box(g,x,1.0,5.6,3.2,1.85,.12,accent);
      box(g,x,1.0,5.51,2.85,1.48,.035,mats.white);
      desk(g,x,0,3.7,2.0,.72); chair(g,x,0,4.4);
    }
  }
}

// Removed stray corner marker that repeated as disconnected floating bars on every floor.

return g;
}

for(let f=1;f<=FLOORS;f++)buildFloor(f);

// Floor/space lighting is explicitly a visual simulation. It is not a lux-meter reading.
const simulatedLuxByFloor={};
// User-controlled per-floor simulated illuminance; persisted locally in this browser.
const FLOOR_LUX_STORAGE_KEY='skyline_tower_floor_lux_v1';
let floorLuxOverrides={};
let floorLuxPreviousSnapshot=null;
try{floorLuxOverrides=JSON.parse(localStorage.getItem(FLOOR_LUX_STORAGE_KEY)||'{}')||{};}catch(_e){floorLuxOverrides={};}
function floorLuxDefault(f){if(f===32)return 370;const variation=((f*37)%11)-5;return Math.max(220,390+variation*8-35);}
function getFloorLux(f){const v=Number(floorLuxOverrides[String(f)]);return Number.isFinite(v)&&v>=0?Math.min(1500,v):floorLuxDefault(f);}
function setFloorLux(f,value){const v=Math.max(0,Math.min(1500,Number(value)||0));floorLuxOverrides[String(f)]=v;try{localStorage.setItem(FLOOR_LUX_STORAGE_KEY,JSON.stringify(floorLuxOverrides));}catch(_e){};if(simulatedLuxByFloor[f]){const key=f===32?'통로':'복도';simulatedLuxByFloor[f].spaces[key]=v;simulatedLuxByFloor[f].source='사용자 입력 시뮬레이션값';}}
function luxDetailScore(lux,reference){const ratio=reference>0?lux/reference:0;return ratio>=1?100:ratio>=.75?85:ratio>=.5?65:ratio>=.25?40:15;}
function initFloorLuxControls(){const sel=document.getElementById('floorLuxSelect');if(!sel)return;sel.innerHTML='';for(let f=1;f<=FLOORS;f++){const o=document.createElement('option');o.value=String(f);o.textContent=f+'층';sel.appendChild(o);}const roof=document.createElement('option');roof.value='32';roof.textContent='32층 · 스카이 가든';sel.appendChild(roof);const update=()=>{const f=Number(sel.value||1),lux=getFloorLux(f);document.getElementById('floorLuxRange').value=String(lux);document.getElementById('floorLuxNumber').value=String(lux);document.getElementById('floorLuxValue').textContent=lux+' lux';};sel.addEventListener('change',update);const change=v=>{const f=Number(sel.value||1);if(autoLatest){const old=autoLatest.floorScores?.find(x=>x.floor===f);floorLuxPreviousSnapshot={floor:f,lux:old?.lux,detail:old?.luxScore,floorScore:old?.score,buildingScore:autoLatest.score};}setFloorLux(f,v);update();if(autoLatest)autoModelAnalysis();};document.getElementById('floorLuxRange').addEventListener('input',e=>change(e.target.value));document.getElementById('floorLuxNumber').addEventListener('change',e=>change(e.target.value));document.getElementById('floorLuxReset').addEventListener('click',()=>{delete floorLuxOverrides[sel.value];try{localStorage.setItem(FLOOR_LUX_STORAGE_KEY,JSON.stringify(floorLuxOverrides));}catch(_e){};const f=Number(sel.value);if(simulatedLuxByFloor[f])simulatedLuxByFloor[f].spaces[f===32?'통로':'복도']=floorLuxDefault(f);update();if(autoLatest)autoModelAnalysis();});document.getElementById('floorLuxResetAll').addEventListener('click',()=>{floorLuxOverrides={};try{localStorage.removeItem(FLOOR_LUX_STORAGE_KEY);}catch(_e){};update();if(autoLatest)autoModelAnalysis();});update();}

let luxSimulationOffset=0;
function installFloorLighting(){
 for(let f=1;f<=FLOORS;f++){
  const g=floorGroups[f-1], variation=((f*37)%11)-5;
  const baseLux=390+variation*8+luxSimulationOffset; // project-only simulated lux, intentionally not presented as a measurement
  simulatedLuxByFloor[f]={base:baseLux,source:'시뮬레이션 조도',spaces:{복도:Math.max(220,baseLux-35),교실:Math.max(260,baseLux+25),화장실:Math.max(180,baseLux-90),계단:Math.max(190,baseLux-75),출입구:baseLux+45}};
  const lumMat=new THREE.MeshStandardMaterial({color:0xffefcf,emissive:0xffd99b,emissiveIntensity:.55+(variation+5)*.018,roughness:.4});
  // Existing floor model is preserved; ceiling fixtures and subtle local lights make level variation visible.
  for(let x of [-6,0,6]){
   const fixture=box(g,x,2.78,-1.6,.62,.035,.18,lumMat);
   fixture.userData={kind:'simulated-light-fixture',floor:f,simulatedLux:baseLux};
  }
  const light=new THREE.PointLight(0xffe8c4,.30+(variation+5)*.055,13,1.7);
  light.position.set((f%3-1)*3,2.68,0);light.castShadow=false;light.userData={kind:'simulated-floor-light',floor:f,simulatedLux:baseLux};g.add(light);
 }
}
installFloorLighting();
simulatedLuxByFloor[32]={base:395,source:'시뮬레이션 조도',spaces:{'스카이 가든':395,통로:370,휴식공간:410}};
function applyLuxSimulationOffset(offset){
 luxSimulationOffset=Number(offset)||0;
 for(let f=1;f<=FLOORS;f++){
  const v=((f*37)%11)-5, baseLux=390+v*8+luxSimulationOffset;
  simulatedLuxByFloor[f]={base:baseLux,source:'시뮬레이션 조도',spaces:{복도:Math.max(80,baseLux-35),교실:Math.max(80,baseLux+25),화장실:Math.max(80,baseLux-90),계단:Math.max(80,baseLux-75),출입구:Math.max(80,baseLux+45)}};
  const g=floorGroups[f-1];g.traverse(o=>{if(o.userData?.kind==='simulated-floor-light'){o.intensity=Math.max(.03,.30+(v+5)*.055+luxSimulationOffset/300);o.userData.simulatedLux=baseLux;}if(o.userData?.kind==='simulated-light-fixture'){o.userData.simulatedLux=baseLux;if(o.material?.emissiveIntensity!==undefined)o.material.emissiveIntensity=Math.max(.12,.35+(v+5)*.035+luxSimulationOffset/500);}});
 }
 const gardenBase=395+luxSimulationOffset;
 simulatedLuxByFloor[32]={base:gardenBase,source:'시뮬레이션 조도',spaces:{'스카이 가든':gardenBase,통로:Math.max(80,gardenBase-25),휴식공간:Math.max(80,gardenBase+15)}};
 if(autoLatest)autoModelAnalysis();
}
initFloorLuxControls();
Object.keys(floorLuxOverrides).filter(k=>/^\d+$/.test(k)).forEach(k=>setFloorLux(Number(k),floorLuxOverrides[k]));
document.getElementById('luxAdjust').addEventListener('input',e=>{document.getElementById('luxAdjustLabel').textContent=(Number(e.target.value)>0?'+':'')+e.target.value+' lux';applyLuxSimulationOffset(e.target.value);if(autoLatest)autoModelAnalysis();});
initFloorLuxControls();

// 기존 내부 구조물은 원본 레이아웃으로 복원하고, 오른쪽 확장 코어만 별도 그룹으로 추가합니다.
function addVerticalCirculationCore(g,f){
const extFloor=new THREE.MeshStandardMaterial({color:0x9d9f9b,roughness:.82,map:tileMap});
  const coreWall=new THREE.MeshStandardMaterial({color:0x4b5154,roughness:.78,map:concreteMap});
  const brushed=new THREE.MeshStandardMaterial({color:0xb7c0c4,metalness:.82,roughness:.22});
  const elevatorDoor=new THREE.MeshStandardMaterial({color:0x64757d,metalness:.8,roughness:.23});
  const stairTread=new THREE.MeshStandardMaterial({color:0x777d80,metalness:.28,roughness:.7});
  const handrail=new THREE.MeshStandardMaterial({color:0xaeb8bb,metalness:.84,roughness:.2});
  // Expanded floor plate and short connector corridor. Main building remains unchanged.
  box(g,14.55,.015,0,7.1,.13,D,extFloor);
  box(g,11.55,.018,0,3.2,.13,3.0,extFloor);
  // Outer perimeter walls of the extension.
  box(g,18.05,1.52,0,.18,3.04,D,mats.wall2);
  box(g,14.55,1.52,-8.38,7.1,3.04,.18,mats.wall2);
  box(g,14.55,1.52,8.38,7.1,3.04,.18,mats.wall2);
  // Elevator shaft: same footprint on every floor, open toward the landing.
  const liftX=12.95, liftZ=-5.15;
  box(g,liftX,1.56,liftZ,2.45,3.12,.16,coreWall); // rear wall
  box(g,liftX-1.22,1.56,liftZ+.72,.16,3.12,1.55,coreWall);
  box(g,liftX+1.22,1.56,liftZ+.72,.16,3.12,1.55,coreWall);
  // Lift car is visible through the open shaft; repeated in exact vertical alignment.
  if(f===1) box(g,liftX,1.48,liftZ+.38,2.05,2.78,1.72,elevatorDoor);
  box(g,liftX-.50,1.49,liftZ+.38,.94,2.68,.035,brushed);
  box(g,liftX+.50,1.49,liftZ+.38,.94,2.68,.035,brushed);
  box(g,liftX,2.85,liftZ+.36,.045,.025,1.45,mats.metal);
  // Landing surround, split doors and illuminated floor indicator.
  box(g,liftX-1.13,1.52,liftZ+1.23,.12,3.0,.12,brushed);
  box(g,liftX+1.13,1.52,liftZ+1.23,.12,3.0,.12,brushed);
  box(g,liftX-.48,1.5,liftZ+1.22,.94,2.88,.07,elevatorDoor);
  box(g,liftX+.48,1.5,liftZ+1.22,.94,2.88,.07,elevatorDoor);
  box(g,liftX+1.48,1.58,liftZ+1.12,.22,.52,.10,mats.black);
  box(g,liftX+1.48,1.73,liftZ+1.055,.13,.12,.025,mats.highlight);
  box(g,liftX+1.48,1.39,liftZ+1.055,.08,.08,.025,brushed);
  // Stairwell occupies the adjacent half of the extension. Two switchback flights per floor.
  const stairXs=[14.05,15.75];
  const zStarts=[5.45,1.25];
  for(let flight=0;flight<2;flight++){
    const sx=stairXs[flight], z0=zStarts[flight], dir=flight===0?-1: -1;
    const steps=8, rise=.205, tread=.30;
    for(let i=0;i<steps;i++){
      const zz=z0-(i+.5)*tread;
      const hh=.18+i*rise+(flight===1?1.62:0);
      box(g,sx,hh/2,zz,1.22,hh,tread,stairTread);
      box(g,sx,hh+.025,zz,1.24,.045,tread+.015,brushed);
    }
    // Inclined handrails on both sides of each flight.
    const rail=new THREE.Mesh(new THREE.BoxGeometry(.055,.055,3.05),handrail);
    rail.position.set(sx-.68,1.02+(flight===1?1.62:0),z0-1.2); rail.rotation.x=-.36; g.add(rail);
    const rail2=new THREE.Mesh(new THREE.BoxGeometry(.055,.055,3.05),handrail);
    rail2.position.set(sx+.68,1.02+(flight===1?1.62:0),z0-1.2); rail2.rotation.x=-.36; g.add(rail2);
    for(let j=0;j<5;j++){
      const zz=z0-.38-j*.58;
      for(const dx of [-.68,.68]) box(g,sx+dx,.58+j*.19+(flight===1?1.62:0),zz,.045,.9,.045,handrail);
    }
  }
  // Landing between the two flights and a clear connector to the original floor.
  box(g,14.9,1.63,2.25,3.0,.16,1.85,extFloor); // 계단 1구간 끝과 2구간 시작을 잇는 중간 계단참
  box(g,11.75,.12,-.05,2.0,.12,2.2,extFloor);
  // Doorway connecting the original main building to the new stair/elevator extension.
  // Keep the same wall line, but leave a clear 1.25 m opening centered on the connector.
  const connX=11.15, connZ=-1.65, connWall=mats.wall2;
  box(g,connX,1.35,connZ-1.0,.16,2.7,.6,connWall);
  box(g,connX,1.35,connZ+1.0,.16,2.7,.6,connWall);
  box(g,connX,2.52,connZ,.16,.36,1.4,connWall);
  // Slim metallic door frame and threshold.
  box(g,connX-.02,1.34,connZ-.66,.10,2.62,.075,brushed);
  box(g,connX-.02,1.34,connZ+.66,.10,2.62,.075,brushed);
  box(g,connX-.02,2.63,connZ,.10,.075,1.38,brushed);
  box(g,connX,.095,connZ, .38,.035,1.28,brushed);
  // Partially open glazed door leaf, hinged on the near jamb so the passage remains visible.
  const connectorGlass=new THREE.MeshPhysicalMaterial({color:0x8bb6c4,roughness:.16,metalness:.22,transparent:true,opacity:.42,side:THREE.DoubleSide});
  const connectorLeaf=new THREE.Mesh(new THREE.BoxGeometry(.055,2.42,.61),connectorGlass);
  connectorLeaf.position.set(connX-.10,1.31,connZ-.32);
  connectorLeaf.rotation.y=-.48;
  g.add(connectorLeaf);
  box(g,connX-.14,1.34,connZ-.52,.035,.18,.035,brushed); // handle
  // 층별 쓰레기통은 원래 배치와 가구를 피해 공용 코너에 둡니다.
  if(f!==2) addTrashCan(g,9.45,6.7);
}
// 전 층에 사람과 소규모 생활 소품을 추가합니다. 기존 레스토랑 배치는 변경하지 않습니다.
// Build the right-side stair/elevator extension on every floor.
// Identical floor offsets keep the shaft aligned from level 1 through level 31.
for(let f=1;f<=FLOORS;f++){
  addVerticalCirculationCore(floorGroups[f-1],f);
}

// Left-side restroom wing: built as real meshes on each existing floor group,
// so floor selection and floor separation automatically include the toilets.
function addLeftRestroomWing(g,f){
  const tile=new THREE.MeshStandardMaterial({color:0xd8d7d1,roughness:.86,map:tileMap});
  const tileWall=new THREE.MeshStandardMaterial({color:0xe7e9e7,roughness:.8});
  const darkTile=new THREE.MeshStandardMaterial({color:0x737d80,roughness:.8});
  const porcelain=new THREE.MeshStandardMaterial({color:0xf5f5f0,roughness:.22,metalness:.02});
  const chrome=new THREE.MeshStandardMaterial({color:0xaeb9bf,metalness:.88,roughness:.18});
  const stallMat=new THREE.MeshStandardMaterial({color:0x9aa9ae,roughness:.58});
  const signMat=new THREE.MeshStandardMaterial({color:0x174f75,roughness:.55});
  const lightMat=new THREE.MeshStandardMaterial({color:0xffedc4,emissive:0x8c7343,emissiveIntensity:.65});
  // Wing footprint lies to the left of the original building, sharing its floor elevation.
  box(g,-14.55,.015,0,7.1,.13,D-.1,tile);
  box(g,-18.05,1.52,0,.18,3.04,D,mats.wall2);
  box(g,-14.55,1.52,-8.38,7.1,3.04,.18,mats.wall2);
  box(g,-14.55,1.52,8.38,7.1,3.04,.18,mats.wall2);
  // Open central access corridor from the main building door, then three restroom suites.
  box(g,-12.1,.10,-1.65,1.9,.08,1.4,tile);
  // Divider walls between suites; doors are left open toward the shared corridor.
  box(g,-15.25,1.42,-2.75,5.35,2.84,.12,tileWall);
  box(g,-15.25,1.42,3.05,5.35,2.84,.12,tileWall);
  // Far-side wall behind fixtures; front wall has three door openings aligned with suite centers.
  box(g,-17.7,1.42,0,.12,2.84,16.45,tileWall);
  const suiteCenters=[-5.45,.15,5.95];
  const frontX=-12.62, roomBackX=-17.62;
  // Side walls with 0.95 m gaps at each suite entry.
  const spans=[[-8.25,-5.95],[-4.95,-.45],[.85,5.25],[6.65,8.25]];
  for(const [a,b] of spans) box(g,frontX,1.42,(a+b)/2,.12,2.84,b-a,tileWall);
  // Men / women / accessible suite interior tile zones and fixtures.
  suiteCenters.forEach((cz,idx)=>{
    const isAccessible=idx===2;
    const suiteDepth=idx===1?5.55:5.45;
    box(g,-15.18,.105,cz,4.95,.055,suiteDepth,tile);
    // Sign panel above each entrance, facing the shared corridor.
    const sign=box(g,-12.48,2.18,cz,.06,.38,1.05,signMat);
    sign.userData={kind:'room',floor:f,name:f+'층 '+(idx===0?'남자 화장실':idx===1?'여자 화장실':'장애인 화장실'),desc:isAccessible?'넓은 출입구 · 휠체어 회전 공간 · 안전 손잡이 · 세면대':'타일 마감 · 변기 칸 · 세면대 · 수도꼭지'};
    pickables.push(sign);
    // Toilet bowls: tank, pedestal, oval-like bowl and flush button.
    const toiletPositions=idx===0?[-6.55,-4.45]:idx===1?[-1.0,1.0]:[6.0];
    toiletPositions.forEach((zj,k)=>{
      box(g,-16.55,.53,zj,.48,.72,.20,porcelain);
      cylinder(g,-16.35,.25,zj+.02,.26,.12,porcelain,20);
      cylinder(g,-16.35,.34,zj+.02,.29,.10,porcelain,20);
      box(g,-16.82,.62,zj,.12,.82,.40,porcelain);
      cylinder(g,-16.82,.94,zj,.045,.025,chrome,12);
    });
    // Sink counter, ceramic basins and visible faucets.
    const sinkZ=cz+(idx===0?1.45:idx===1?-1.55:0);
    box(g,-13.65,.83,sinkZ,1.15,.14,.72,stallMat);
    cylinder(g,-13.65,.94,sinkZ,.29,.09,porcelain,24);
    cylinder(g,-13.65,.99,sinkZ,.20,.045,porcelain,24);
    cylinder(g,-13.65,1.12,sinkZ-.18,.035,.22,chrome,12);
    cylinder(g,-13.65,1.22,sinkZ-.10,.035,.16,chrome,12);
    // Stall partitions and partially open doors for the multi-stall suites.
    if(idx<2){
      const partitionZ=cz+.45;
      box(g,-15.35,1.12,partitionZ,3.75,2.15,.07,stallMat);
      const door=new THREE.Mesh(new THREE.BoxGeometry(.055,1.95,1.0),stallMat);
      door.position.set(-13.48,1.02,cz-.48); door.rotation.y=-.18; g.add(door);
      box(g,-13.42,1.02,cz-.80,.05,.13,.05,chrome);
    }else{
      // Wheelchair turning zone marked on floor (clear circle, not a solid obstacle).
      const ring=new THREE.Mesh(new THREE.RingGeometry(0.72,.79,40),new THREE.MeshBasicMaterial({color:0x2788a5,side:THREE.DoubleSide}));
      ring.rotation.x=-Math.PI/2; ring.position.set(-14.65,.145,cz+.25); g.add(ring);
      // Grab rails beside toilet and at the back wall.
      box(g,-15.95,1.02,cz-.55,.62,.055,.055,chrome);
      box(g,-15.62,1.02,cz-.92,.055,.055,.62,chrome);
      box(g,-13.35,1.02,cz+.95,.72,.055,.055,chrome);
    }
    // Ceiling light fixture and wall tile seams as visible 3D elements.
    box(g,-15.1,2.78,cz,.72,.045,.24,lightMat);
    for(let xx=-17.0;xx<=-13.0;xx+=1.0) box(g,xx,2.72,cz+(idx===0?1.85:idx===1?-1.85:1.7),.018,.035,.018,chrome);
  });
  // Short threshold at the main-building opening; leave its center walkable.
  box(g,-11.15,.075,-1.65,.32,.04,1.22,chrome);
}

for(let f=1;f<=FLOORS;f++) addLeftRestroomWing(floorGroups[f-1],f);

// Human-scale articulated procedural people. These are synthetic figures, not captured people or a rigged external asset.
const walkingPeople=[];
const skinMats=[0xc98e68,0xe0b18c,0x9a674b,0xf0c9a7].map(color=>new THREE.MeshStandardMaterial({color,roughness:.82}));
const shirtColors=[0x2c5576,0x6c7d54,0x8b4b45,0xded9cf,0x4d4d58,0x8b704f,0x315c5a];
const hairColors=[0x2b2421,0x42362e,0x5a4638,0x191b20];
function makeWalkingPerson(parent,f,index){
 const g=new THREE.Group();g.userData={kind:'person',floor:f,personIndex:index};
 const skin=skinMats[(f+index)%skinMats.length];
 const shirt=new THREE.MeshStandardMaterial({color:shirtColors[(f*3+index)%shirtColors.length],roughness:.86});
 const pants=new THREE.MeshStandardMaterial({color:[0x303a45,0x4a4b50,0x344b60,0x5a5148][(f+index)%4],roughness:.9});
 const shoe=new THREE.MeshStandardMaterial({color:0x25282a,roughness:.7});
 const hair=new THREE.MeshStandardMaterial({color:hairColors[(f+index)%hairColors.length],roughness:.95});
 function mesh(geo,mat,parentObj,x,y,z){const m=new THREE.Mesh(geo,mat);m.position.set(x,y,z);m.castShadow=true;m.receiveShadow=true;parentObj.add(m);return m;}
 function ellipsoid(parentObj,x,y,z,sx,sy,sz,mat){const m=mesh(new THREE.SphereGeometry(1,16,12),mat,parentObj,x,y,z);m.scale.set(sx,sy,sz);return m;}
 function limb(parentObj,mat,r1,r2,len){const pivot=new THREE.Group();parentObj.add(pivot);const m=mesh(new THREE.CapsuleGeometry((r1+r2)/2,Math.max(.02,len-r1-r2),4,8),mat,pivot,0,-len/2,0);return {pivot,mesh:m,len};}
 // Adult proportions, layered clothes, separate joint pivots and shoes.
 const pelvis=mesh(new THREE.CapsuleGeometry(.145,.12,3,8),pants,g,0,.83,0);pelvis.scale.set(1,.85,.9);
 const torso=mesh(new THREE.CapsuleGeometry(.18,.43,5,10),shirt,g,0,1.13,0);torso.scale.set(1,.95,.78);
 const neck=mesh(new THREE.CylinderGeometry(.055,.065,.09,10),skin,g,0,1.43,0);
 const head=ellipsoid(g,0,1.56,0,.12,.145,.115,skin);
 ellipsoid(g,0,1.66,-.012,.122,.065,.119,hair);
 // ears and nose help the face silhouette read as human at building scale.
 ellipsoid(g,-.122,1.56,0,.022,.035,.025,skin);ellipsoid(g,.122,1.56,0,.022,.035,.025,skin);
 ellipsoid(g,0,1.545,.108,.022,.026,.027,skin);
 const arms=[],legs=[],feet=[];
 for(const side of [-1,1]){
   const shoulder=new THREE.Group();shoulder.position.set(side*.205,1.31,0);g.add(shoulder);
   const upper=limb(shoulder,shirt,.05,.055,.29);upper.pivot.position.set(0,-.04,0);
   const elbow=new THREE.Group();elbow.position.set(0,-.28,0);shoulder.add(elbow);
   const fore=limb(elbow,shirt,.042,.047,.26);fore.pivot.position.set(0,0,0);
   ellipsoid(elbow,0,-.25,0,.045,.045,.045,skin);
   arms.push({shoulder,elbow,side});
   const hip=new THREE.Group();hip.position.set(side*.083,.78,0);g.add(hip);
   const thigh=limb(hip,pants,.067,.07,.39);
   const knee=new THREE.Group();knee.position.set(0,-.36,0);hip.add(knee);
   const calf=limb(knee,pants,.048,.055,.36);
   const foot=mesh(new THREE.BoxGeometry(.105,.065,.20),shoe,knee,0,-.34,.045);feet.push(foot);
   legs.push({hip,knee,side,thigh,calf});
 }
 // The route is local to the floor. Each person is assigned a lane and cycles through nearby waypoints.
 const lanes=[-1.05,-.5,0,.5,1.05];
 const route=[{x:-9,z:lanes[index]},{x:-4.5,z:lanes[index]},{x:0,z:lanes[index]},{x:4.5,z:lanes[index]},{x:9,z:lanes[index]},{x:4.5,z:lanes[index]+.22},{x:0,z:lanes[index]+.22},{x:-4.5,z:lanes[index]+.22}];
 const person={group:g,arms,legs,feet,floor:f,index,route,waypoint:(f+index)%route.length,phase:(f*1.71+index*1.27),state:'walk',stateTime:((f*7+index*13)%19)*.13,speed:.62+((f*3+index*7)%5)*.085,radius:.24,baseY:0,blockedTime:0,replanCooldown:((f*5+index*3)%7)*.07,pauseDuration:0,path:null,pathIndex:0,role:'walker',seatCooldown:((f+index)%4)*2.5,seatTarget:null};
 g.traverse(o=>{o.userData={...(o.userData||{}),kind:'person',floor:f,personIndex:index};});
 const initial=route[person.waypoint];g.position.set(initial.x,0,initial.z);parent.add(g);walkingPeople.push(person);
}
for(let f=1;f<=FLOORS;f++)for(let i=0;i<5;i++)makeWalkingPerson(floorGroups[f-1],f,i);

// A simulation-only hazard registry. Puddles are visualized on selected restroom floors and are fed into the analyzer.
const simulatedWaterHazards=[];
function makeWaterPatch(parent,f,index,x,z,rx,rz){
 const shape=new THREE.Shape();shape.moveTo(-rx*.92,-rz*.1);shape.bezierCurveTo(-rx*1.12,-rz*.75,-rx*.38,-rz*1.05,0,-rz*.75);shape.bezierCurveTo(rx*.68,-rz*1.08,rx*1.12,-rz*.42,rx*.84,rz*.12);shape.bezierCurveTo(rx*.98,rz*.7,rx*.28,rz*1.03,-rx*.18,rz*.74);shape.bezierCurveTo(-rx*.82,rz*.92,-rx*1.08,rz*.35,-rx*.92,-rz*.1);
 const geom=new THREE.ShapeGeometry(shape,20);
 const mat=new THREE.MeshPhysicalMaterial({color:0x77b9c8,metalness:.12,roughness:.12,transparent:true,opacity:.62,clearcoat:1,clearcoatRoughness:.08,side:THREE.DoubleSide,depthWrite:false});
 const patch=new THREE.Mesh(geom,mat);patch.rotation.x=-Math.PI/2;patch.position.set(x,.173,z);patch.renderOrder=3;patch.receiveShadow=true;patch.userData={kind:'simulated-water',floor:f,hazardId:'water-'+f+'-'+index};parent.add(patch);
 // A faint irregular highlight adds a readable wet edge without pretending to be a physical fluid simulation.
 const edge=new THREE.LineLoop(new THREE.EdgesGeometry(geom),new THREE.LineBasicMaterial({color:0xbfeaf1,transparent:true,opacity:.48}));edge.rotation.x=-Math.PI/2;edge.position.set(x,.176,z);parent.add(edge);
 const data={id:patch.userData.hazardId,type:'바닥 물기(시뮬레이션)',spaceType:'화장실(모델 위치 기반 추정)',floor:f,x,z,y:.173,area:Math.PI*rx*rz,rx,rz,mesh:patch,createdAt:new Date().toISOString(),source:'가상 시뮬레이션 생성',routeOverlap:null};
 data.edge=edge;simulatedWaterHazards.push(data);
}
function generateSimulatedWater(){
 // Remove prior run's patches first; generated positions remain fixed until this function is called again.
 for(const h of simulatedWaterHazards){h.mesh.parent?.remove(h.mesh);h.mesh.parent?.remove(h.edge);}
 simulatedWaterHazards.length=0;
 const rng=(seed)=>{let x=seed>>>0;return()=>{x=(1664525*x+1013904223)>>>0;return x/4294967296;};};
 const rand=rng((Date.now()^Math.floor(Math.random()*0xffffffff))>>>0);
 const eligible=[];for(let f=1;f<=FLOORS;f++)eligible.push(f);
 // Select a subset of floors; locations stay inside the modeled left-side restroom wing.
 const count=5+Math.floor(rand()*4);
 for(let n=0;n<count&&eligible.length;n++){
   const pick=Math.floor(rand()*eligible.length),f=eligible.splice(pick,1)[0];
   const zOptions=[-5.15,-1.0,3.0,5.9];const z=zOptions[Math.floor(rand()*zOptions.length)]+(rand()-.5)*.45;
   const x=-14.45+(rand()-.5)*.7,rx=.38+rand()*.42,rz=.28+rand()*.42;
   makeWaterPatch(floorGroups[f-1],f,n,x,z,rx,rz);
 }
}
generateSimulatedWater();

// Static collision candidates are derived from transformed mesh bounds; floors, people, and water surfaces are excluded.
let collisionByFloor=null;
function buildCollisionCache(){
 // Collision data is built from each mesh's world-transformed bounds, so nested group transforms
 // and rotations are included. Bounds are conservative AABBs, not exact mesh/triangle collision.
 const out=Array.from({length:FLOORS+1},()=>[]);scene.updateMatrixWorld(true);
 root.traverse(o=>{
   if(!o.isMesh||!o.geometry||o.userData?.kind==='person'||o.userData?.kind==='simulated-water'||o.userData?.kind==='simulated-light-fixture'||o.userData?.kind==='accessMarker')return;
   const b=new THREE.Box3().setFromObject(o);if(b.isEmpty())return;
   const size=b.getSize(new THREE.Vector3());
   // Discard tiny decorative flecks and broad floor/ceiling slabs; retain chairs, desks, counters,
   // cabinets, planters, rails, columns and wall pieces that overlap human body height.
   if(size.y<.16||size.x<.075||size.z<.075)return;
   if(size.x>38&&size.z>24&&size.y<.45)return;
   const midY=(b.min.y+b.max.y)*.5;const f=midY>totalH+.02?32:Math.max(1,Math.min(FLOORS,Math.floor(midY/FLOOR_H)+1));
   const floorY=(f-1)*FLOOR_H;const lo=b.min.y-floorY,hi=b.max.y-floorY;
   if(hi<.16||lo>1.82)return;
   let ancestor=o.parent,chairGroup=null;
   while(ancestor){if(ancestor.userData?.kind==='chair-seat'||/chair|seat/i.test(ancestor.name||'')){chairGroup=ancestor;break;}ancestor=ancestor.parent;}
   const name=((o.name||'')+' '+(o.userData?.name||'')+' '+(o.userData?.kind||'')).toLowerCase();
   let kind='model-object';if(chairGroup)kind='chair';else if(/desk|table|counter|cabinet|shelf|sofa|책상|테이블|카운터|수납|소파/.test(name))kind='furniture';else if(/wall|벽/.test(name))kind='wall';else if(/column|pillar|기둥/.test(name))kind='column';else if(/door|문틀|출입/.test(name))kind='door-frame';else if(/plant|planter|화분|화단/.test(name))kind='planter';
   out[f-1].push({minX:b.min.x,maxX:b.max.x,minZ:b.min.z,maxZ:b.max.z,minY:lo,maxY:hi,obj:o,chairGroup,kind});
 });
 // Deduplicate nearly identical mesh bounds from layered decorative meshes. Keep distinct chair parts
 // where their bounds materially differ, because seat/back/legs collectively occupy space.
 for(let f=0;f<out.length;f++){
   const seen=new Set();out[f]=out[f].filter(b=>{const k=[b.minX,b.maxX,b.minZ,b.maxZ,b.minY,b.maxY].map(v=>Math.round(v*20)).join(':');if(seen.has(k))return false;seen.add(k);return true;});
 }
 collisionByFloor=out;
}
function staticPersonCollides(p,x,z){
 if(!collisionByFloor)buildCollisionCache();
 const obstacles=collisionByFloor[p.floor-1]||[];
 for(const b of obstacles){
  // Broad-phase AABB with a circular body footprint. Bounds are world-transformed, but complex mesh openings remain approximate.
  if(b.maxY<.18||b.minY>1.72)continue;
  const qx=Math.max(b.minX,Math.min(x,b.maxX)),qz=Math.max(b.minZ,Math.min(z,b.maxZ));
  const dx=x-qx,dz=z-qz;const clearance=(b.kind==='furniture'||b.kind==='chair'||b.kind==='wall'||b.kind==='column')?.09:0;
  const r=p.radius+clearance;
  if(dx*dx+dz*dz<r*r)return true;
 }
 return false;
}
function personCollides(p,x,z){
 if(staticPersonCollides(p,x,z))return true;
 for(const q of walkingPeople){
  if(q===p||q.floor!==p.floor)continue;
  const dx=x-q.group.position.x,dz=z-q.group.position.z;
  const gap=p.radius+q.radius+.055;
  if(dx*dx+dz*dz<gap*gap)return true;
 }
 return false;
}
function movementSegmentClear(p,x0,z0,x1,z1){
 const distance=Math.hypot(x1-x0,z1-z0),samples=Math.max(2,Math.ceil(distance/.12));
 for(let i=1;i<=samples;i++){const t=i/samples;const x=x0+(x1-x0)*t,z=z0+(z1-z0)*t;if(personCollides(p,x,z))return false;}
 return true;
}
function findPersonPath(p,start,goal){
 // A* uses body-radius collision tests and explicitly forbids diagonal corner cutting.
 // Route bounds match the modeled public circulation area; each person still replans independently.
 const step=.35,minX=-10.2,maxX=10.2,minZ=-7.0,maxZ=7.0;
 const clampCell=v=>Math.max(0,Math.min(v,Math.round((maxX-minX)/step)));
 const nxMax=Math.round((maxX-minX)/step),nzMax=Math.round((maxZ-minZ)/step);
 const toCell=(x,z)=>({i:Math.max(0,Math.min(nxMax,Math.round((x-minX)/step))),j:Math.max(0,Math.min(nzMax,Math.round((z-minZ)/step)))});
 const toPos=(i,j)=>({x:minX+i*step,z:minZ+j*step});
 const a=toCell(start.x,start.z),b=toCell(goal.x,goal.z),key=(i,j)=>i+','+j;
 const open=[{...a,g:0,f:Math.hypot(a.i-b.i,a.j-b.j)}],came=new Map(),cost=new Map([[key(a.i,a.j),0]]),closed=new Set();
 const dirs=[[1,0],[-1,0],[0,1],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]];let loops=0;
 while(open.length&&loops++<4200){open.sort((u,v)=>u.f-v.f);const cur=open.shift(),ck=key(cur.i,cur.j);if(closed.has(ck))continue;closed.add(ck);
  if(Math.abs(cur.i-b.i)<=1&&Math.abs(cur.j-b.j)<=1){const path=[];let k=ck;while(came.has(k)){const [i,j]=k.split(',').map(Number);path.push(toPos(i,j));k=came.get(k);}path.reverse();return path;}
  for(const [di,dj] of dirs){const ni=cur.i+di,nj=cur.j+dj;if(ni<0||ni>nxMax||nj<0||nj>nzMax)continue;const pos=toPos(ni,nj);if(personCollides(p,pos.x,pos.z))continue;
   if(di&&dj){const sideA=toPos(cur.i+di,cur.j),sideB=toPos(cur.i,cur.j+dj);if(personCollides(p,sideA.x,sideA.z)||personCollides(p,sideB.x,sideB.z))continue;}
   const nk=key(ni,nj),ng=cur.g+((di&&dj)?1.414:1);if(ng>=(cost.get(nk)??Infinity))continue;cost.set(nk,ng);came.set(nk,ck);open.push({i:ni,j:nj,g:ng,f:ng+Math.hypot(ni-b.i,nj-b.j)});
  }
 }
 return null;
}
function findSeatForPerson(p){
 if(p.role!=='seat-seeker'||p.seatCooldown>0||p.seatTarget)return null;
 let best=null;
 for(const seat of chairSeats){
  if(!seat.userData?.canSit||!seat.userData.seatAvailable||seat.userData.floor!==p.floor)continue;
  const center=seat.localToWorld(new THREE.Vector3(0,0,0));
  const approach=seat.localToWorld(new THREE.Vector3(0,0,.68));
  const d=Math.hypot(approach.x-p.group.position.x,approach.z-p.group.position.z);
  if(d>3.4||d<.45||staticPersonCollides(p,approach.x,approach.z))continue;
  const path=findPersonPath(p,{x:p.group.position.x,z:p.group.position.z},{x:approach.x,z:approach.z});
  if(!path||!path.length)continue;
  if(!best||d<best.distance)best={seat,center,approach,path,distance:d};
 }
 if(best){best.seat.userData.seatAvailable=false;best.seat.userData.occupiedBy=p.index+'-'+p.floor;p.seatTarget=best; p.path=best.path;p.pathIndex=0;p.blockedTime=0;return best;}
 return null;
}
function releasePersonSeat(p){
 if(p.seatTarget?.seat){p.seatTarget.seat.userData.seatAvailable=true;p.seatTarget.seat.userData.occupiedBy=null;}
 p.seatTarget=null;p.seatCooldown=18+((p.floor*7+p.index*11)%13);p.group.position.y=0;
 p.legs.forEach(l=>{l.hip.rotation.x=0;l.knee.rotation.x=0;});
}
function advancePerson(p,dt,t){
 // Each agent owns its own state clock, route cursor, speed response and replanning cooldown.
 p.stateTime=(p.stateTime||0)+dt;
 p.replanCooldown=Math.max(0,(p.replanCooldown||0)-dt);p.seatCooldown=Math.max(0,(p.seatCooldown||0)-dt);
 if(p.state==='sit'){
   if(p.stateTime>p.sitDuration){releasePersonSeat(p);p.state='walk';p.stateTime=0;p.currentSpeed=0;p.path=null;p.pathIndex=0;p.waypoint=(p.waypoint+1)%p.route.length;}
 }else if(p.state==='pause'){
   if(p.stateTime>p.pauseDuration){p.state='walk';p.stateTime=0;p.pauseDuration=0;p.currentSpeed=0;p.path=null;p.pathIndex=0;p.waypoint=(p.waypoint+1)%p.route.length;}
 }else if(p.state==='walk'){
   let goal=p.path&&p.pathIndex<p.path.length?p.path[p.pathIndex]:(p.seatTarget?{x:p.seatTarget.approach.x,z:p.seatTarget.approach.z}:p.route[p.waypoint]);
   let dx=goal.x-p.group.position.x,dz=goal.z-p.group.position.z,dist=Math.hypot(dx,dz);
   if(dist<.24){
     if(p.path&&p.pathIndex<p.path.length-1){p.pathIndex++;}
     else if(p.path){p.path=null;p.pathIndex=0;p.blockedTime=0;}
     else if(p.seatTarget){
       p.group.position.x=p.seatTarget.center.x;p.group.position.z=p.seatTarget.center.z;
       p.group.rotation.y=p.seatTarget.seat.rotation.y;p.group.position.y=-.12;
       p.state='sit';p.stateTime=0;p.sitDuration=3.2+((p.floor*3+p.index*5)%7)*.65;p.currentSpeed=0;
       p.legs.forEach((l,i)=>{l.hip.rotation.x=i===0?-.8:-.72;l.knee.rotation.x=1.0;});
       p.arms.forEach(a=>{a.shoulder.rotation.x=.18;a.elbow.rotation.x=.28;});
     }else if(p.role==='seat-seeker'&&p.seatCooldown<=0&&findSeatForPerson(p)){
       // Seat approach has become the new individual goal; do not advance the walking route yet.
     }else if(p.waypoint===p.route.length-1){
       // A brief destination dwell occurs only at the route end, not at every waypoint.
       p.state='pause';p.stateTime=0;p.pauseDuration=.25+((p.index*17+p.floor*11)%9)*.11;p.currentSpeed=0;
     }else{p.waypoint=(p.waypoint+1)%p.route.length;}
   }else{
     const targetSpeed=p.speed*Math.min(1,dist/1.0);
     p.currentSpeed??=0;
     p.currentSpeed+=(targetSpeed-p.currentSpeed)*(1-Math.exp(-4.8*dt));
     const step=Math.min(dist,p.currentSpeed*dt),nx=p.group.position.x+dx/dist*step,nz=p.group.position.z+dz/dist*step;
     const sx=p.group.position.x,sz=p.group.position.z;
     let next=null;
     // Never sidestep by arbitrary offsets every frame: that creates wall jitter and diagonal clipping.
     // First validate the complete swept segment; if blocked, stop and let A* choose a stable detour.
     if(movementSegmentClear(p,sx,sz,nx,nz))next={x:nx,z:nz};
     if(next){
       p.group.position.x=next.x;p.group.position.z=next.z;p.blockedTime=0;
       const mdx=next.x-sx,mdz=next.z-sz;
       if(Math.hypot(mdx,mdz)>.0001){const yaw=Math.atan2(mdx,mdz);let yd=((yaw-p.group.rotation.y+Math.PI*3)%(Math.PI*2))-Math.PI;p.group.rotation.y+=yd*(1-Math.exp(-6.5*dt));}
     }else{
       p.blockedTime=(p.blockedTime||0)+dt;p.currentSpeed*=Math.exp(-7*dt);
       if(p.blockedTime>.18&&p.replanCooldown<=0){
         const routeGoal=p.seatTarget?{x:p.seatTarget.approach.x,z:p.seatTarget.approach.z}:p.route[p.waypoint];
         const path=findPersonPath(p,{x:p.group.position.x,z:p.group.position.z},routeGoal);
         if(path&&path.length){p.path=path;p.pathIndex=0;p.blockedTime=0;p.replanCooldown=.45;}
         else{p.replanCooldown=.65; p.path=null; p.pathIndex=0;
         // Try alternate individual waypoints that have a collision-free path; never keep pushing into a table/chair.
         for(let attempt=1;attempt<p.route.length;attempt++){const wi=(p.waypoint+attempt)%p.route.length;const alt=p.route[wi];if(staticPersonCollides(p,alt.x,alt.z))continue;const altPath=findPersonPath(p,{x:p.group.position.x,z:p.group.position.z},alt);if(altPath&&altPath.length){p.waypoint=wi;p.path=altPath;p.pathIndex=0;p.blockedTime=0;break;}}
       }
       }
       // If the destination is unreachable after retries, select another waypoint instead of oscillating.
       if(p.blockedTime>2.2){p.path=null;p.pathIndex=0;p.blockedTime=0;p.waypoint=(p.waypoint+1+((p.index+p.floor)%2))%p.route.length;p.replanCooldown=.35;}
     }
   }
 }
 const moving=p.state==='walk'&&p.currentSpeed>.08;
 if(p.state==='sit')p.currentSpeed=0;
 const stride=moving?Math.sin(t*5.8+p.phase):0;
 const idle=Math.sin(t*1.4+p.phase)*.025;
 if(p.state==='sit'){
  p.legs.forEach((l,i)=>{l.hip.rotation.x=i===0?-.8:-.72;l.knee.rotation.x=1.0;l.thigh.mesh.rotation.x=0;l.calf.mesh.rotation.x=0;});
  p.arms.forEach(a=>{a.shoulder.rotation.x=.18;a.shoulder.rotation.z=a.side*.08;a.elbow.rotation.x=.28;});
 }else{
  p.legs.forEach((l,i)=>{const side=i===0?1:-1;l.hip.rotation.x=stride*.38*side;l.knee.rotation.x=Math.max(0,-stride*side)*.48;l.thigh.mesh.rotation.x=0;l.calf.mesh.rotation.x=0;});
  p.arms.forEach((a,i)=>{const side=i===0?1:-1;a.shoulder.rotation.x=moving?-stride*.22*side:idle;a.shoulder.rotation.z=a.side*.08;a.elbow.rotation.x=moving?.08+Math.max(0,stride*side)*.12:.12;});
 }
}
// Accessibility audit catalogue: 50 unique items across A-E. Coordinates refer to this
// model's local floor plan. Existing facilities use approximate anchor points; unverified
// locations are explicitly labelled as proposal locations, not measured defects.
const accessItems=[
{id:1,cat:'A',name:'좁은 출입구 폭',loc:'주출입구 / 출입문',floor:1,x:0,z:8.05,users:'휠체어 이용자, 보행 보조기 이용자, 유아차 이용자',impact:'통과 폭이 부족하면 출입과 교행이 어려울 수 있습니다.',effect:'건물 진입 및 실별 이동 접근성 저하',fix:'유효 통과 폭을 실측하고 문짝·가구 간섭을 제거한 뒤 필요한 폭을 확보합니다.',priority:'높음',status:'확인 필요',basis:'도면·현장 치수 미확인',proposal:false},
{id:2,cat:'A',name:'출입구 턱·단차',loc:'주출입구 문턱',floor:1,x:1.2,z:8.0,users:'휠체어 이용자, 보행 보조기 이용자, 고령자, 어린이',impact:'바퀴 이동이 막히거나 걸려 넘어질 수 있습니다.',effect:'진입·이동 안전 저하',fix:'단차 높이를 측정하고 문턱 제거 또는 적절한 경사 연결을 검토합니다.',priority:'높음',status:'확인 필요',basis:'단차 실측 미실시',proposal:true},
{id:3,cat:'A',name:'긴 복도 및 이동 거리',loc:'층별 주 복도',floor:2,x:0,z:0,users:'휠체어 이용자, 보행 보조기 이용자, 고령자, 임산부',impact:'휴식 없이 긴 거리를 이동하면 피로가 증가할 수 있습니다.',effect:'주요 시설까지의 이동 부담 증가',fix:'주요 목적지까지 경로를 확인하고 휴식 지점과 안내를 보강합니다.',priority:'보통',status:'확인 필요',basis:'실제 이동 거리 미측정',proposal:true},
{id:4,cat:'A',name:'미끄러운 바닥',loc:'현관·복도 바닥',floor:1,x:3,z:6.8,users:'고령자, 보행 보조기 이용자, 어린이, 임산부',impact:'물기나 표면 마찰 부족으로 미끄러질 가능성이 있습니다.',effect:'낙상 위험 증가',fix:'바닥 상태와 젖은 상태의 미끄럼 저항을 점검하고 미끄럼 방지 마감·매트를 검토합니다.',priority:'높음',status:'확인 필요',basis:'바닥 성능 시험 미실시',proposal:true},
{id:5,cat:'A',name:'엘리베이터 내부 폭·공간',loc:'오른쪽 확장부 엘리베이터',floor:1,x:12.95,z:-5.15,users:'휠체어 이용자, 보행 보조기 이용자, 고령자',impact:'내부 회전이나 동반 탑승이 어려울 수 있습니다.',effect:'수직 이동의 독립성 저하',fix:'카 내부 유효 치수와 문 유효 폭을 측정하고 회전·조작 공간을 확인합니다.',priority:'높음',status:'확인 필요',basis:'모델 치수와 실측 일치 여부 미확인',proposal:false},
{id:6,cat:'A',name:'계단만 있는 동선',loc:'오른쪽 확장부 계단',floor:1,x:14.05,z:3.8,users:'휠체어 이용자, 보행 보조기 이용자, 고령자, 임산부',impact:'계단은 일부 이용자의 층간 이동을 제한합니다.',effect:'대체 가능한 수직 동선의 필요성',fix:'엘리베이터 등 계단을 이용하지 않는 대체 경로의 연속성을 확인합니다.',priority:'높음',status:'확인 필요',basis:'오른쪽 엘리베이터 모델 존재; 실제 운행·접근성 미확인',proposal:false},
{id:7,cat:'A',name:'복잡한 통로 구조',loc:'복도 교차·연결부',floor:1,x:10.8,z:-1.65,users:'시각장애인, 인지장애가 있는 이용자, 방문객, 어린이',impact:'갈림길을 빠르게 파악하지 못해 길을 잃을 수 있습니다.',effect:'목적지 탐색 부담 증가',fix:'주요 분기점에 일관된 방향 표지와 명확한 시야를 확보합니다.',priority:'보통',status:'확인 필요',basis:'실제 길찾기 관찰 미실시',proposal:true},
{id:8,cat:'A',name:'낮은 천장 높이',loc:'복도 천장 제안 위치',floor:2,x:4,z:-6.5,users:'키가 큰 이용자, 시각장애인',impact:'머리 충돌 또는 돌출물 충돌 위험이 생길 수 있습니다.',effect:'이동 안전 저하',fix:'천장고와 돌출 설비 높이를 실측하고 위험 구간을 표시합니다.',priority:'보통',status:'확인 필요',basis:'현장 천장고 미측정',proposal:true},
{id:9,cat:'A',name:'안내 동선 부족',loc:'로비 및 층별 갈림길',floor:1,x:0,z:3.5,users:'시각장애인, 고령자, 어린이, 방문객',impact:'주요 시설 방향을 찾기 어려울 수 있습니다.',effect:'독립적인 길찾기 저하',fix:'입구·교차점·엘리베이터 앞에 일관된 방향 안내를 배치합니다.',priority:'보통',status:'확인 필요',basis:'안내 체계 현장 조사 미실시',proposal:true},
{id:10,cat:'A',name:'긴급 대피 동선 부족',loc:'주요 복도와 출구 연결부',floor:1,x:-1,z:7.5,users:'모든 이용자, 특히 이동·감각 장애인',impact:'피난 경로가 막히거나 불명확하면 대피가 지연될 수 있습니다.',effect:'비상 시 인명 안전에 영향',fix:'피난 경로의 연속성·폭·장애물과 대체 경로를 전문가가 점검합니다.',priority:'긴급',status:'확인 필요',basis:'소방·피난 도면 미확인',proposal:true},
{id:11,cat:'A',name:'자동문 미설치 또는 조작 불편',loc:'주출입구',floor:1,x:-1.5,z:8.0,users:'휠체어 이용자, 보행 보조기 이용자, 손 사용이 제한된 이용자',impact:'문을 당기거나 미는 동작이 어려울 수 있습니다.',effect:'독립적인 출입 저하',fix:'문 여닫는 힘과 접근 공간을 확인하고 자동문 또는 쉬운 조작 장치를 검토합니다.',priority:'보통',status:'확인 필요',basis:'실제 문 하드웨어 미확인',proposal:true},
{id:12,cat:'A',name:'계단 손잡이 부재·연속성',loc:'오른쪽 계단 난간',floor:1,x:15.0,z:2.8,users:'고령자, 보행 보조기 이용자, 시각장애인, 임산부',impact:'계단 오르내릴 때 지지와 방향 확인이 어려울 수 있습니다.',effect:'균형 유지와 이동 안전 저하',fix:'양측 손잡이의 연속성·고정 상태·끝단 처리를 점검합니다.',priority:'높음',status:'확인 필요',basis:'실물 손잡이 치수 미검증',proposal:false},
{id:13,cat:'A',name:'경사로 폭 협소',loc:'주출입구 경사로 제안 위치',floor:1,x:-2.5,z:8.3,users:'휠체어 이용자, 보행 보조기 이용자',impact:'통과·회전·교행이 어려울 수 있습니다.',effect:'대체 진입 경로의 이용성 저하',fix:'경사로 유효 폭과 회전 공간을 실측합니다.',priority:'높음',status:'확인 필요',basis:'경사로 현장 위치·치수 미확인',proposal:true},
{id:14,cat:'A',name:'바닥 요철·파손',loc:'외부 연결 보행로 제안 위치',floor:1,x:-4,z:8.3,users:'휠체어 이용자, 고령자, 보행 보조기 이용자, 시각장애인',impact:'바퀴가 걸리거나 걸려 넘어질 수 있습니다.',effect:'이동 안전 및 연속성 저하',fix:'보행면을 점검하고 파손부를 보수합니다.',priority:'높음',status:'확인 필요',basis:'외부 보행로 현장 확인 미실시',proposal:true},
{id:15,cat:'A',name:'복도 조명 부족',loc:'복도·계단 연결부',floor:3,x:7.5,z:0,users:'저시력자, 고령자, 청각장애인(시각적 경보 인지)',impact:'경계와 표지판을 식별하기 어려울 수 있습니다.',effect:'이동·정보 인식 저하',fix:'조도를 측정하고 눈부심을 줄이면서 균일한 조명을 확보합니다.',priority:'보통',status:'확인 필요',basis:'조도 측정 미실시',proposal:true},
{id:16,cat:'B',name:'조명 스위치 위치 높음',loc:'실내 벽면 스위치 제안 위치',floor:1,x:8.8,z:-6.5,users:'휠체어 이용자, 키가 작은 이용자, 어린이',impact:'스위치에 손이 닿지 않거나 접근 자세가 불편할 수 있습니다.',effect:'설비 독립 조작 저하',fix:'도달 범위와 접근 공간을 확인해 조작 가능한 위치로 조정합니다.',priority:'보통',status:'확인 필요',basis:'스위치 좌표·높이 미확인',proposal:true},
{id:17,cat:'B',name:'자동문 버튼 위치 불량',loc:'주출입구 버튼 제안 위치',floor:1,x:-2,z:7.2,users:'휠체어 이용자, 손 사용이 제한된 이용자',impact:'버튼에 접근하거나 누르기 어려울 수 있습니다.',effect:'출입의 독립성 저하',fix:'문짝 회전 범위를 피하고 정면 접근 공간과 도달 높이를 확인합니다.',priority:'보통',status:'확인 필요',basis:'버튼 설치 여부 미확인',proposal:true},
{id:18,cat:'B',name:'출입 키패드 높이',loc:'출입 통제 장치 제안 위치',floor:1,x:8.7,z:7.2,users:'휠체어 이용자, 키가 작은 이용자, 시각장애인',impact:'입력·화면 확인이 어려울 수 있습니다.',effect:'보안 출입 접근성 저하',fix:'조작 높이·화면 대비·촉각 피드백과 전면 접근 공간을 확인합니다.',priority:'보통',status:'확인 필요',basis:'키패드 현장 설치 위치 미확인',proposal:true},
{id:19,cat:'B',name:'수도꼭지 조작 어려움',loc:'왼쪽 확장부 화장실 세면대',floor:1,x:-13.65,z:-5.45,users:'손 기능이 제한된 이용자, 고령자, 휠체어 이용자',impact:'손목을 돌리거나 강하게 쥐어야 하면 조작이 어려울 수 있습니다.',effect:'위생시설 독립 이용 저하',fix:'레버형·센서형 등 적은 힘으로 조작 가능한 수전을 검토합니다.',priority:'보통',status:'확인 필요',basis:'모델에 세면대·수전 오브젝트 존재; 실제 작동성 미확인',proposal:false},
{id:20,cat:'B',name:'비상벨 위치 불량',loc:'화장실·공용 공간 비상벨 제안 위치',floor:1,x:-14.2,z:1.0,users:'휠체어 이용자, 고령자, 어린이, 부상자',impact:'넘어지거나 앉은 상태에서 손이 닿지 않을 수 있습니다.',effect:'도움 요청 지연 가능성',fix:'앉은 자세와 바닥 가까운 위치에서도 접근 가능한 호출 장치를 검토합니다.',priority:'높음',status:'확인 필요',basis:'비상벨 모델·실제 설치 여부 미확인',proposal:true},
{id:21,cat:'B',name:'장애인용 설비 미비',loc:'왼쪽 확장부 장애인 화장실',floor:1,x:-14.65,z:5.95,users:'휠체어 이용자, 보행 보조기 이용자',impact:'회전·옮겨 앉기·문 조작 공간이 부족할 수 있습니다.',effect:'위생시설 접근성 저하',fix:'회전 공간, 문 유효 폭, 손잡이와 세면대 하부 공간을 실측합니다.',priority:'높음',status:'확인 필요',basis:'모델에 관련 오브젝트 존재; 실측 및 법규 적합성 미확인',proposal:false},
{id:22,cat:'B',name:'엘리베이터 버튼 높이',loc:'오른쪽 엘리베이터 조작 패널',floor:1,x:14.45,z:-4.0,users:'휠체어 이용자, 키가 작은 이용자, 시각장애인',impact:'버튼에 닿거나 층 정보를 확인하기 어려울 수 있습니다.',effect:'수직 이동 조작의 독립성 저하',fix:'버튼 높이·촉각 표기·대비·음성 안내를 점검합니다.',priority:'높음',status:'확인 필요',basis:'모델 패널 위치 존재; 실제 치수 미검증',proposal:false},
{id:23,cat:'C',name:'화장실 출입구 폭 협소',loc:'왼쪽 확장부 화장실 입구',floor:1,x:-12.48,z:-5.45,users:'휠체어 이용자, 보행 보조기 이용자',impact:'문을 통과하거나 회전하기 어려울 수 있습니다.',effect:'화장실 접근성 저하',fix:'문 유효 폭과 접근 공간을 실측하고 장애물을 제거합니다.',priority:'높음',status:'확인 필요',basis:'모델 출입구가 존재하나 실제 치수 미확인',proposal:false},
{id:24,cat:'C',name:'세면대 높이·하부 공간',loc:'왼쪽 확장부 화장실 세면대',floor:1,x:-13.65,z:-5.45,users:'휠체어 이용자, 어린이, 키가 작은 이용자',impact:'무릎 공간이 부족하거나 수도꼭지에 닿기 어려울 수 있습니다.',effect:'세면대 사용성 저하',fix:'상판 높이와 하부 무릎 공간, 접근 방향을 확인합니다.',priority:'높음',status:'확인 필요',basis:'3D 세면대 존재; 실제 규격 미확인',proposal:false},
{id:25,cat:'C',name:'손 건조기·비누 디스펜서 높이',loc:'화장실 세면대 주변 제안 위치',floor:1,x:-13.1,z:-4.8,users:'휠체어 이용자, 키가 작은 이용자, 어린이',impact:'손이 닿지 않거나 조작부를 보기 어려울 수 있습니다.',effect:'위생 절차의 독립성 저하',fix:'사용 가능한 도달 높이와 전면 접근 공간을 확인합니다.',priority:'보통',status:'확인 필요',basis:'디스펜서 오브젝트·치수 미확인',proposal:true},
{id:26,cat:'C',name:'변기 주변 손잡이·휴지걸이 위치',loc:'장애인 화장실 변기 주변',floor:1,x:-16.35,z:5.95,users:'휠체어 이용자, 보행 보조기 이용자, 고령자',impact:'옮겨 앉기와 휴지 사용이 불편하거나 균형을 잡기 어려울 수 있습니다.',effect:'화장실 이용 안전 저하',fix:'손잡이 고정·위치와 휴지걸이 도달 범위를 점검합니다.',priority:'높음',status:'확인 필요',basis:'모델 손잡이 오브젝트 존재; 실측 미확인',proposal:false},
{id:27,cat:'C',name:'비상호출 버튼 높이',loc:'장애인 화장실 내부 제안 위치',floor:1,x:-15.0,z:6.8,users:'휠체어 이용자, 고령자, 부상자',impact:'긴급 상황에서 호출 장치에 손이 닿지 않을 수 있습니다.',effect:'도움 요청 지연 가능성',fix:'변기와 바닥 가까운 위치에서 접근 가능한 호출 장치를 설치·시험합니다.',priority:'높음',status:'확인 필요',basis:'실제 호출 장치 설치 여부 미확인',proposal:true},
{id:28,cat:'C',name:'화장실 내부 회전 공간 협소',loc:'왼쪽 확장부 장애인 화장실',floor:1,x:-14.65,z:6.0,users:'휠체어 이용자, 보행 보조기 이용자',impact:'휠체어 회전과 설비 접근이 어려울 수 있습니다.',effect:'독립적인 시설 이용 저하',fix:'실제 유효 공간을 측정하고 회전 영역 내 장애물을 제거합니다.',priority:'높음',status:'확인 필요',basis:'모델에 회전 표시 존재; 치수 검증 필요',proposal:false},
{id:29,cat:'C',name:'바닥 물기·미끄럼',loc:'화장실 세면대 주변',floor:1,x:-13.5,z:-4.9,users:'고령자, 시각장애인, 보행 보조기 이용자, 어린이',impact:'물기와 배수 불량은 미끄러짐 위험을 높일 수 있습니다.',effect:'낙상 위험 증가',fix:'배수·누수·미끄럼 저항을 점검하고 젖은 구역을 관리합니다.',priority:'높음',status:'확인 필요',basis:'실제 물기·바닥 성능 미확인',proposal:true},
{id:30,cat:'C',name:'화장실 환기 부족',loc:'화장실 환기 설비 제안 위치',floor:2,x:-16.8,z:0,users:'천식 등 냄새·공기질에 민감한 이용자, 모든 이용자',impact:'환기가 부족하면 냄새와 습기가 쌓일 수 있습니다.',effect:'실내 환경 쾌적성 저하',fix:'환기 설비 운전과 환기량을 점검합니다.',priority:'보통',status:'확인 필요',basis:'환기량·공기질 측정 미실시',proposal:true},
{id:31,cat:'D',name:'안내 표지판 글씨가 작음',loc:'로비 안내판',floor:1,x:2.0,z:2.5,users:'저시력자, 고령자, 인지장애가 있는 이용자',impact:'거리에서 글자를 읽거나 정보를 빠르게 찾기 어려울 수 있습니다.',effect:'시설 정보 인식 저하',fix:'글자 크기·대비·읽는 거리와 설치 높이를 점검합니다.',priority:'보통',status:'확인 필요',basis:'실제 표지판 규격 미확인',proposal:true},
{id:32,cat:'D',name:'층 안내 색상 구분 부족',loc:'엘리베이터 앞 층 안내판',floor:1,x:11.4,z:-4.3,users:'저시력자, 인지장애가 있는 이용자, 방문객',impact:'층이나 방향을 빠르게 구분하기 어려울 수 있습니다.',effect:'길찾기 오류 가능성 증가',fix:'색상만으로 정보를 구분하지 말고 글자·기호·대비를 함께 사용합니다.',priority:'보통',status:'확인 필요',basis:'표지판 디자인·대비 미검토',proposal:true},
{id:33,cat:'D',name:'다국어 표기 부족',loc:'주출입구 안내판',floor:1,x:0,z:7.2,users:'한국어에 익숙하지 않은 방문객, 외국인 이용자',impact:'주요 시설과 안전 안내를 이해하기 어려울 수 있습니다.',effect:'정보 접근성 저하',fix:'주요 목적지와 비상 안내에 적절한 다국어 표기를 검토합니다.',priority:'보통',status:'확인 필요',basis:'현장 안내판 내용 미확인',proposal:true},
{id:34,cat:'D',name:'시각장애인 유도블록 부족',loc:'현관에서 엘리베이터까지의 동선',floor:1,x:4.5,z:1.5,users:'시각장애인, 저시력자',impact:'주요 시설까지 안전하게 방향을 찾기 어려울 수 있습니다.',effect:'독립 이동 및 충돌 예방 저하',fix:'동선과 장애물을 조사해 유도블록의 연속성과 목적지 연결을 검토합니다.',priority:'높음',status:'확인 필요',basis:'유도블록 실물·도면 미확인',proposal:true},
{id:35,cat:'D',name:'청각 안내·시각 경보 미비',loc:'엘리베이터 및 비상 안내 설비',floor:1,x:12.95,z:-4.0,users:'청각장애인, 난청 고령자',impact:'음성 안내만 있으면 중요한 정보를 놓칠 수 있습니다.',effect:'이동·비상 정보 접근성 저하',fix:'시각 표시·문자 정보와 음성 안내가 함께 제공되는지 확인합니다.',priority:'높음',status:'확인 필요',basis:'실제 경보·안내 기능 미검증',proposal:true},
{id:36,cat:'E',name:'비상구 위치 확인 어려움',loc:'주요 출구 및 복도',floor:1,x:-1.0,z:7.8,users:'모든 이용자, 특히 방문객·시각장애인·인지장애가 있는 이용자',impact:'비상 시 출구 방향을 찾는 시간이 길어질 수 있습니다.',effect:'대피 지연 가능성',fix:'출구 표지의 시인성과 경로 연속성을 현장 점검합니다.',priority:'긴급',status:'확인 필요',basis:'실제 피난 계획 미확인',proposal:true},
{id:37,cat:'E',name:'피난 유도등 부족',loc:'복도와 계단 피난 경로',floor:1,x:14.0,z:0.5,users:'모든 이용자, 특히 정전·연기 상황의 이용자',impact:'정전이나 연기 속에서 진행 방향을 파악하기 어려울 수 있습니다.',effect:'피난 경로 인식 저하',fix:'유도등 설치 위치·작동·시야 가림을 전문가가 점검합니다.',priority:'긴급',status:'확인 필요',basis:'실제 유도등 설비 미확인',proposal:true},
{id:38,cat:'E',name:'화재 경보 인지 방식 부족',loc:'공용 공간 경보 장치 제안 위치',floor:2,x:0,z:0,users:'청각장애인, 난청 고령자, 모든 이용자',impact:'경보가 소리만으로 제공되면 일부 이용자가 인지하지 못할 수 있습니다.',effect:'비상 대응 지연 가능성',fix:'시각·진동 등 보완 경보와 청각 신호의 작동을 확인합니다.',priority:'긴급',status:'확인 필요',basis:'경보 설비 실제 구성 미확인',proposal:true},
{id:39,cat:'E',name:'연기 감지기 설치·작동 확인',loc:'층별 천장 감지 구역',floor:2,x:5.0,z:-3.0,users:'모든 이용자',impact:'감지 설비가 없거나 작동하지 않으면 화재 인지가 늦어질 수 있습니다.',effect:'초기 대응과 대피 안전에 영향',fix:'감지기 배치·점검 기록·작동 상태를 관련 전문가가 확인합니다.',priority:'긴급',status:'확인 필요',basis:'실제 설비와 소방 기록 미확인',proposal:true},
{id:40,cat:'E',name:'대피 대기 공간·피난 시설 부족',loc:'로비 또는 피난 안전 구역 제안 위치',floor:1,x:3.0,z:3.0,users:'휠체어 이용자, 보행 보조기 이용자, 고령자, 모든 이용자',impact:'즉시 계단을 이용하기 어려운 사람이 안전하게 대기할 장소가 부족할 수 있습니다.',effect:'비상 대피 지원 저하',fix:'건축·소방 계획에 따라 안전 대기 공간과 구조 요청 수단을 확인합니다.',priority:'긴급',status:'확인 필요',basis:'실제 피난 계획·공간 지정 미확인',proposal:true},
{id:41,cat:'E',name:'소방 설비 위치 확인 어려움',loc:'소화기·소화전 위치 제안 지점',floor:1,x:9.0,z:5.0,users:'모든 이용자, 시설 관리자',impact:'설비를 급히 찾아야 할 때 시간이 지연될 수 있습니다.',effect:'초기 대응 지연 가능성',fix:'설비 접근을 막는 물건을 치우고 표지·가시성을 확인합니다.',priority:'높음',status:'확인 필요',basis:'실제 소방 설비 위치 미확인',proposal:true},
{id:42,cat:'E',name:'실내 온도 조절 불편',loc:'공용 공간 온도조절기 제안 위치',floor:3,x:8.8,z:-6.0,users:'고령자, 어린이, 임산부, 온도에 민감한 이용자',impact:'온도 편차나 조작 어려움으로 불쾌감이 생길 수 있습니다.',effect:'실내 환경 쾌적성 저하',fix:'실내 온도 분포와 조절기 접근성을 확인합니다.',priority:'보통',status:'확인 필요',basis:'온도 측정·조절기 위치 미확인',proposal:true},
{id:43,cat:'E',name:'실내 소음 문제',loc:'기계실 인접 공용 공간 제안 위치',floor:2,x:9.0,z:6.0,users:'청각장애인, 난청 고령자, 감각 과민 이용자',impact:'안내 방송과 대화가 묻히거나 집중이 어려울 수 있습니다.',effect:'의사소통·이용 쾌적성 저하',fix:'소음 수준을 측정하고 소음원 차단과 안내 신호의 명료성을 개선합니다.',priority:'보통',status:'확인 필요',basis:'소음 측정 미실시',proposal:true},
{id:44,cat:'E',name:'디지털 정보 접근성 부족',loc:'키오스크·디지털 안내기 제안 위치',floor:1,x:3.5,z:2.0,users:'시각장애인, 청각장애인, 고령자, 인지장애가 있는 이용자',impact:'화면 읽기·대비·음성·물리 조작이 충분하지 않으면 정보를 이용하기 어렵습니다.',effect:'디지털 서비스 접근성 저하',fix:'화면 낭독, 키보드·촉각 조작, 자막과 충분한 대비를 점검합니다.',priority:'보통',status:'확인 필요',basis:'웹사이트·앱 자체는 3D 건물 좌표에 배치할 수 없어 키오스크 제안 위치만 표시',proposal:true},
{id:45,cat:'E',name:'환기 부족',loc:'밀폐된 실내 공간 제안 위치',floor:4,x:-5.0,z:-5.5,users:'공기질에 민감한 이용자, 모든 이용자',impact:'환기가 부족하면 이산화탄소·냄새·습기가 쌓일 수 있습니다.',effect:'실내 환경과 쾌적성 저하',fix:'환기 운전과 실내 공기질을 측정하고 설비를 점검합니다.',priority:'보통',status:'확인 필요',basis:'환기량·공기질 측정 미실시',proposal:true},
{id:46,cat:'E',name:'비상 상황 안내 부족',loc:'비상구·피난 경로 안내판',floor:1,x:14.0,z:7.2,users:'모든 이용자, 특히 방문객·외국인·시각장애인',impact:'비상 시 행동과 대피 방향을 이해하기 어려울 수 있습니다.',effect:'대피 판단 지연 가능성',fix:'쉽고 큰 글씨, 그림 기호, 다국어 및 시각·음성 정보를 함께 제공합니다.',priority:'긴급',status:'확인 필요',basis:'실제 비상 안내판 미확인',proposal:true},
{id:47,cat:'E',name:'화재 대피 시설 부족',loc:'계단·피난 경로 제안 위치',floor:1,x:15.5,z:0.0,users:'모든 이용자, 특히 이동장애인',impact:'대체 피난 방법이나 보호 구역이 부족하면 대피가 어려울 수 있습니다.',effect:'비상 시 안전 확보 저하',fix:'건물 용도와 관련 기준에 따라 피난 계획을 소방 전문가와 검토합니다.',priority:'긴급',status:'확인 필요',basis:'실제 소방·피난 도면 미확인',proposal:true},
{id:48,cat:'D',name:'안내 표지판 혼동',loc:'층별 복도 교차점',floor:3,x:0,z:0,users:'인지장애가 있는 이용자, 어린이, 방문객, 저시력자',impact:'표현이 일관되지 않으면 잘못된 방향으로 이동할 수 있습니다.',effect:'길찾기 부담과 이동 지연',fix:'명칭·화살표·색상 체계를 건물 전체에서 일관되게 사용합니다.',priority:'보통',status:'확인 필요',basis:'현장 표지판 일관성 조사 미실시',proposal:true},
{id:49,cat:'B',name:'문 손잡이 조작 불편',loc:'공용 출입문 손잡이 제안 위치',floor:1,x:8.8,z:7.3,users:'손 기능이 제한된 이용자, 고령자, 휠체어 이용자',impact:'강한 쥐기·비틀기 동작이 필요하면 문을 열기 어려울 수 있습니다.',effect:'출입 독립성 저하',fix:'레버형 손잡이와 낮은 조작력, 손 접근 공간을 검토합니다.',priority:'보통',status:'확인 필요',basis:'실제 손잡이 형태·조작력 미확인',proposal:true},
{id:50,cat:'C',name:'화장실 청결·위생용품 관리',loc:'왼쪽 확장부 화장실 내부',floor:1,x:-15.0,z:0.2,users:'모든 이용자, 특히 면역 취약자·고령자',impact:'청결이나 소모품 부족은 위생적인 시설 이용을 방해할 수 있습니다.',effect:'위생·쾌적성 저하',fix:'청소 점검표와 소모품 보충 주기를 정하고 비치 상태를 확인합니다.',priority:'보통',status:'확인 필요',basis:'실제 청결 상태는 3D 모델로 판단할 수 없어 현장 확인 필요',proposal:true}
];

const accessColors={A:0xe0a126,B:0x2584c7,C:0x2c9c70,D:0x8b61c2,E:0xd94b4b};
const accessMarkerGroup=new THREE.Group(); root.add(accessMarkerGroup);
const accessMarkerMeshes=[];
let selectedAccessId=null;
const accessRecords={};
accessItems.forEach(item=>{accessRecords[item.id]={rating:'확인 필요',evidence:item.basis,improved:false};});
function makeMarkerLabel(item){
 const c=document.createElement('canvas'); c.width=128;c.height=128;const ctx=c.getContext('2d');
 ctx.fillStyle='#ffffff';ctx.beginPath();ctx.arc(64,64,57,0,Math.PI*2);ctx.fill();
 ctx.lineWidth=9;ctx.strokeStyle='#'+accessColors[item.cat].toString(16).padStart(6,'0');ctx.stroke();
 ctx.fillStyle='#183348';ctx.font='bold 48px Arial';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(String(item.id),64,66);
 const tex=new THREE.CanvasTexture(c);tex.colorSpace=THREE.SRGBColorSpace;
 const sprite=new THREE.Sprite(new THREE.SpriteMaterial({map:tex,depthTest:false,transparent:true}));sprite.scale.set(.85,.85,1);sprite.renderOrder=999;
 return sprite;
}
accessItems.forEach(item=>{
 const marker=new THREE.Group();marker.position.set(item.x,(item.floor-1)*FLOOR_H+2.45,item.z);marker.userData={kind:'accessMarker',itemId:item.id};
 const dot=new THREE.Mesh(new THREE.SphereGeometry(.18,16,12),new THREE.MeshStandardMaterial({color:accessColors[item.cat],emissive:accessColors[item.cat],emissiveIntensity:.25}));dot.position.y=-.42;dot.userData={kind:'accessMarker',itemId:item.id};marker.add(dot);
 const label=makeMarkerLabel(item);label.position.y=.12;label.userData={kind:'accessMarker',itemId:item.id};marker.add(label);
 accessMarkerGroup.add(marker);accessMarkerMeshes.push(dot,label);item.marker=marker;
});
function updateAccessVisibility(){
 accessItems.forEach(item=>{const cat=document.getElementById('accessFilter').value;item.marker.visible=(selectedFloor===null||selectedFloor===item.floor)&& (cat==='all'||cat===item.cat);});
}
function accessScore(){
 const points={'양호':0,'경미':1,'보통':2,'심각':3,'위험':4};
 const rated=Object.values(accessRecords).filter(r=>r.rating!=='확인 필요');
 if(!rated.length)return null;
 return (rated.reduce((sum,r)=>sum+points[r.rating],0)/rated.length).toFixed(2);
}
function updateAccessCompare(){
 const rated=Object.values(accessRecords).filter(r=>r.rating!=='확인 필요').length;
 const proposed=Object.values(accessRecords).filter(r=>r.improved).length;
 const score=accessScore();
 document.getElementById('accessCompare').textContent='평가 완료 '+rated+'/50 · 평가 심각도 평균 '+(score===null?'계산 불가(평가 입력 필요)':score+'/4')+' · 개선안 제안 '+proposed+'개 · 실제 해결 완료 0개';
}
function renderAccessItem(item){
 if(!item)return;
 selectedAccessId=item.id;document.getElementById('accessItem').value=String(item.id);
 const rec=accessRecords[item.id];
 document.getElementById('accessSummary').innerHTML='<b>#'+item.id+' · '+item.name+'</b><br>분류 '+item.cat+' · '+item.loc+' · '+item.floor+'층'+(item.proposal?' <b>(제안 위치)</b>':' <b>(모델 시설 기준, 실측 미확인)</b>')+'<br><b>영향 이용자:</b> '+item.users+'<br><b>불편·위험:</b> '+item.impact+'<br><b>접근성 영향:</b> '+item.effect+'<br><b>개선 방법:</b> '+item.fix+'<br><b>우선순위:</b> '+item.priority+'<br><b>상태:</b> '+(rec.improved?'개선안 제안됨 — 실제 구조 변경 전':'평가 기록 '+rec.rating)+'<br><b>근거:</b> '+rec.evidence;
 document.getElementById('accessRating').value=rec.rating;document.getElementById('accessEvidence').value=rec.evidence;
 targetLookY=(item.floor-1)*FLOOR_H+1.2;targetDist=20;targetAz=item.x<0?-0.7:0.7;
 if(selectedFloor!==item.floor){selector.value=String(item.floor);applyFloor(String(item.floor));}
}
const accessFilter=document.getElementById('accessFilter'), accessSelect=document.getElementById('accessItem');
function rebuildAccessSelect(){
 const prior=accessSelect.value;accessSelect.innerHTML='<option value="">항목 선택 또는 3D 마커 클릭</option>';
 accessItems.filter(i=>accessFilter.value==='all'||i.cat===accessFilter.value).forEach(i=>{const o=document.createElement('option');o.value=i.id;o.textContent=String(i.id).padStart(2,'0')+' · '+i.name;accessSelect.appendChild(o);});
 if(prior&&accessSelect.querySelector('option[value="'+prior+'"]'))accessSelect.value=prior;
}
accessFilter.addEventListener('change',()=>{rebuildAccessSelect();updateAccessVisibility();});
accessSelect.addEventListener('change',()=>{const item=accessItems.find(i=>i.id===Number(accessSelect.value));if(item)renderAccessItem(item);});
document.getElementById('accessSave').addEventListener('click',()=>{
 if(!selectedAccessId){document.getElementById('accessSummary').textContent='먼저 목록 또는 3D 마커에서 항목을 선택하세요.';return;}
 const rec=accessRecords[selectedAccessId];rec.rating=document.getElementById('accessRating').value;rec.evidence=document.getElementById('accessEvidence').value.trim()||'확인 필요';
 updateAccessCompare();renderAccessItem(accessItems.find(i=>i.id===selectedAccessId));
});
document.getElementById('accessImprove').addEventListener('click',()=>{
 if(!selectedAccessId){document.getElementById('accessSummary').textContent='먼저 항목을 선택하세요.';return;}
 const rec=accessRecords[selectedAccessId];rec.improved=!rec.improved;
 updateAccessCompare();renderAccessItem(accessItems.find(i=>i.id===selectedAccessId));
});
rebuildAccessSelect();updateAccessCompare();

function addPerson(parent,x,z,variant=0,rot=0){
  const human=new THREE.Group(); human.position.set(x,0,z); human.rotation.y=rot; human.userData={kind:'person',floor:parent.userData?.floor||Math.max(1,Math.min(FLOORS,Math.round(parent.position.y/FLOOR_H)+1)),personIndex:variant}; parent.add(human);
  const shirts=[0x315f75,0x8b5d45,0x557b62,0x4b536c,0xb7a17b,0x6f8793,0x6b493f,0x4d6669];
  const pants=[0x30363c,0x424d57,0x5d5146,0x343b4d,0x282d32];
  const skinMats=[0xc99673,0xd8ad8c,0x9e6e50,0xe0b99a];
  const shirt=new THREE.MeshStandardMaterial({color:shirts[variant%shirts.length],roughness:.78});
  const trouser=new THREE.MeshStandardMaterial({color:pants[(variant*3)%pants.length],roughness:.84});
  const skin=new THREE.MeshStandardMaterial({color:skinMats[variant%skinMats.length],roughness:.82});
  const shoe=new THREE.MeshStandardMaterial({color:variant%3===0?0x202326:0x393632,roughness:.72});
  const hair=new THREE.MeshStandardMaterial({color:[0x30251f,0x4b382c,0x1e2021,0x6b5140][variant%4],roughness:.9});
  const addMesh=(geo,mat,px,py,pz,rx=0,ry=0,rz=0)=>{const m=new THREE.Mesh(geo,mat);m.position.set(px,py,pz);m.rotation.set(rx,ry,rz);m.castShadow=true;m.receiveShadow=true;human.add(m);return m;};
  // Shoes and slightly separated legs, with tapered trousers.
  for(const dx of [-.105,.105]){
    addMesh(new THREE.CylinderGeometry(.065,.085,.47,9),trouser,dx,.49,0,0,0,dx<0?-.025:.025);
    addMesh(new THREE.BoxGeometry(.145,.085,.235),shoe,dx,.255,.045,0,0,dx<0?-.035:.035);
  }
  // Torso with a subtle shoulder taper and waist, plus a collar.
  addMesh(new THREE.CylinderGeometry(.205,.17,.56,12),shirt,0,1.055,0);
  addMesh(new THREE.SphereGeometry(.19,12,8),shirt,0,1.31,0);
  addMesh(new THREE.CylinderGeometry(.055,.06,.105,10),skin,0,1.385,0);
  addMesh(new THREE.SphereGeometry(.128,16,12),skin,0,1.545,0);
  // Hair cap and a small nose give the silhouette more human-like definition.
  addMesh(new THREE.SphereGeometry(.131,14,8,0,Math.PI*2,0,Math.PI*.53),hair,0,1.585,-.008);
  addMesh(new THREE.SphereGeometry(.025,8,6),skin,0,1.535,.122);
  // Arms angle naturally at the elbows; hands stay close to the hips to avoid props.
  for(const side of [-1,1]){
    addMesh(new THREE.CylinderGeometry(.052,.068,.31,9),shirt,side*.235,1.105,.012,0,0,side*.12);
    addMesh(new THREE.CylinderGeometry(.043,.05,.19,8),skin,side*.27,.88,.035,0,0,side*.10);
    addMesh(new THREE.SphereGeometry(.043,8,6),skin,side*.285,.775,.04);
  }
  human.traverse(o=>{o.userData={...(o.userData||{}),kind:'person',floor:human.userData.floor};});
  human.userData.isPerson=true;
  // These legacy figures were decorative/static. Register them with the same independent
  // collision-aware movement controller while preserving their original appearance.
  const f=human.userData.floor,idx=walkingPeople.length;
  const lane=((idx%7)-3)*.34;
  const agent={group:human,arms:[],legs:[],feet:[],floor:f,index:idx,
    route:[{x:x,z:z},{x:Math.max(-9.4,Math.min(9.4,x+2.2)),z:z+lane},{x:Math.max(-9.4,Math.min(9.4,x-1.8)),z:z+lane+.45}],
    waypoint:1,phase:idx*1.31,state:'walk',stateTime:0,speed:.38+(idx%4)*.09,radius:.25,
    blockedTime:0,replanCooldown:.2,path:null,pathIndex:0,role:'walker',seatCooldown:99,seatTarget:null,currentSpeed:0};
  walkingPeople.push(agent);
  return human;
}
function isPersonSpotClear(parent,x,z){
  // Inspect nested furniture meshes in world space; the old direct-child/local-bounds test
  // missed objects inside groups and allowed people to spawn inside tables and chairs.
  scene.updateMatrixWorld(true);
  const probe=new THREE.Vector3(x,0,z);let clear=true;
  parent.traverse(obj=>{
    if(!clear||!obj.isMesh||!obj.geometry||obj.userData?.kind==='person'||obj.userData?.kind==='simulated-water')return;
    const b=new THREE.Box3().setFromObject(obj);if(b.isEmpty())return;
    const size=b.getSize(new THREE.Vector3());
    if(size.y<.12||size.x<.06||size.z<.06)return;
    if(size.x>38&&size.z>24&&size.y<.45)return;
    if(b.max.y<.18||b.min.y>1.72)return;
    const qx=Math.max(b.min.x,Math.min(x,b.max.x)),qz=Math.max(b.min.z,Math.min(z,b.max.z));
    if((x-qx)**2+(z-qz)**2<.48*.48)clear=false;
  });
  return clear;
}
function addRealisticFloorPeople(g,f,count=4){
  const candidates=[
    [-8.4,-1.1],[-8.3,2.2],[-6.2,5.9],[-3.7,5.8],[-1.0,4.8],
    [1.6,5.9],[4.1,5.8],[6.5,4.8],[8.2,1.8],[7.7,-1.6],
    [5.5,-5.4],[2.8,-5.6],[-1.5,-5.4],[-4.6,-5.5],[-7.5,-4.9],
    [-5.7,1.6],[-2.7,1.9],[.2,2.1],[3.0,2.2],[5.8,1.2]
  ];
  let placed=0;
  for(let i=0;i<candidates.length && placed<count;i++){
    const [x,z]=candidates[(i*7+f*3)%candidates.length];
    if(isPersonSpotClear(g,x,z)){
      addPerson(g,x,z,(f+placed*2)%8,((f+placed)%4)*Math.PI/2);
      placed++;
    }
  }
  // If furniture occupies most candidate spots, use a wider perimeter search while still checking collisions.
  for(let z=-6.2;z<=6.3 && placed<count;z+=1.35){
    for(let x=-9.2;x<=9.2 && placed<count;x+=1.55){
      if(isPersonSpotClear(g,x,z)){
        addPerson(g,x,z,(f+placed*3)%8,((f+placed)%4)*Math.PI/2);
        placed++;
      }
    }
  }
}

function addFloorLifeAndDetails(g,f){
  // Keep all original room layouts and the redesigned second-floor restaurant intact.
  // Place four people per floor only where the approximate floor-level collision test finds clearance.
  if(f===2){
    addRealisticFloorPeople(g,f,4);
    plant(g,10.1,0,-6.7,.62);
    return;
  }
  addRealisticFloorPeople(g,f,4);
  if(f%4===0){
    plant(g,9.5,0,-6.5,.7);
  }else if(f%4===1 && f!==1){
    plant(g,9.5,0,6.4,.7);
  }else if(f%4===2){
    plant(g,-9.7,0,-6.8,.72);
  }else{
    plant(g,9.5,0,6.4,.7);
  }
}

// 층마다 끊겨 보이던 외곽 모서리 기둥은 제거했습니다.

// 32층 스카이 가든에도 이용객을 배치해 최상층이 비어 보이지 않도록 합니다.
const totalH=FLOORS*FLOOR_H;

box(root,0,totalH+.12,0,W+.25,.24,D+.25,mats.concrete);
box(root,0,totalH+.55,-3.6,3.4,.8,2.5,mats.wall2);

for(let i=0;i<3;i++){
box(root,-4.5+i*.85,totalH+.95,-3.6,.55,.12,.65,mats.metal);
}

// 32층 스카이 가든: 유리 아트리움 + 실내 정원 + 라운지
// 기존 32층 구조와 층 선택 체계는 유지하고, 옥상 영역만 교체합니다.
const roofGarden=new THREE.Group();
roofGarden.name='32층 스카이 가든';
addPerson(roofGarden,-5.0,2.0,2,Math.PI/2);
addPerson(roofGarden,4.8,3.8,4,-Math.PI/2);
addPerson(roofGarden,-1.8,5.2,1,Math.PI);
addPerson(roofGarden,2.0,-5.1,6,0);
plant(roofGarden,8.8,0,-5.8,.8);
root.add(roofGarden);
const roofY=totalH+.28;
const gardenW=W-1.0, gardenD=D-1.0;
// Top landing for the right-side stair/elevator core, aligned with the floors below.
box(roofGarden,14.55,roofY+.08,0,7.1,.16,D-0.2,mats.concrete);
box(roofGarden,12.95,roofY+1.42,-3.95,2.45,2.8,.16,mats.wall2);
box(roofGarden,12.95,roofY+1.40,-2.95,2.05,2.55,.06,mats.metal);
box(roofGarden,14.05,roofY+.70,2.3,1.22,.10,1.0,mats.metal);
box(roofGarden,15.75,roofY+1.48,2.3,1.22,.10,1.0,mats.metal);
const roofGlass=new THREE.MeshPhysicalMaterial({color:0xb9dbe5,metalness:.12,roughness:.18,transparent:true,opacity:.22,side:THREE.DoubleSide,depthWrite:false});
const leafMats=[0x2f7048,0x438653,0x639b58,0x8aa85a,0x24583d].map(c=>new THREE.MeshStandardMaterial({color:c,roughness:.9}));
const bloomMats=[0xe8d6c7,0xe6b8c8,0xf0d77b,0xffffff].map(c=>new THREE.MeshStandardMaterial({color:c,roughness:.8}));
const soilMat=new THREE.MeshStandardMaterial({color:0x514638,roughness:1});
const grassMat=new THREE.MeshStandardMaterial({color:0x56864b,roughness:1});
const pathMat=new THREE.MeshStandardMaterial({color:0xb9b8ae,roughness:.9});

// 바닥 데크와 넓은 밝은 산책로
const deck=new THREE.Mesh(new THREE.PlaneGeometry(gardenW,gardenD),new THREE.MeshStandardMaterial({color:0xc8c8bd,roughness:.88}));
deck.rotation.x=-Math.PI/2; deck.position.set(0,roofY,0); deck.receiveShadow=true; roofGarden.add(deck);
box(roofGarden,0,roofY+.035,0,2.05,.07,gardenD-.25,pathMat);
box(roofGarden,0,roofY+.04,0,gardenW-.25,.08,1.85,mats.wood);
// 목재 데크 라운지 쪽으로 이어지는 보조 산책로
box(roofGarden,-5.0,roofY+.045,3.4,5.2,.08,1.45,mats.wood);
box(roofGarden,5.0,roofY+.045,-3.5,5.2,.08,1.45,mats.wood);

// 높은 유리 외벽: 창틀이 보이는 온실형 스카이 가든
const roofWallH=7.1, wallY=roofY+roofWallH/2;
for(const z of [-gardenD/2,gardenD/2]){
  box(roofGarden,0,wallY,z,gardenW,roofWallH,.12,roofGlass);
  box(roofGarden,0,roofY+roofWallH,z,gardenW,.16,.18,mats.frame);
  for(let x=-gardenW/2;x<=gardenW/2+.01;x+=1.65) box(roofGarden,x,wallY,z,.075,roofWallH,.16,mats.frame);
  box(roofGarden,0,roofY+2.35,z-.005,gardenW,.07,.18,mats.frame);
  box(roofGarden,0,roofY+4.8,z-.005,gardenW,.055,.18,mats.metal);
}
for(const x of [-gardenW/2,gardenW/2]){
  box(roofGarden,x,wallY,0,.12,roofWallH,gardenD,roofGlass);
  box(roofGarden,x,roofY+roofWallH,0,.18,.16,gardenD,mats.frame);
  for(let z=-gardenD/2;z<=gardenD/2+.01;z+=1.55) box(roofGarden,x,wallY,z,.16,roofWallH,.075,mats.frame);
  box(roofGarden,x,roofY+2.35,0,.18,.07,gardenD,mats.frame);
  box(roofGarden,x,roofY+4.8,0,.18,.055,gardenD,mats.metal);
}
// 유리 지붕 패널과 아치형 구조 프레임
for(let z=-gardenD/2+1.0;z<gardenD/2;z+=2.15){
  const points=[];
  for(let i=0;i<=20;i++){
    const x=-gardenW/2+(gardenW*i/20);
    const y=roofY+roofWallH+1.35*Math.sin(Math.PI*i/20);
    points.push(new THREE.Vector3(x,y,z));
  }
  const curve=new THREE.CatmullRomCurve3(points);
  const rib=new THREE.Mesh(new THREE.TubeGeometry(curve,40,.055,7,false),mats.frame);
  rib.castShadow=true; roofGarden.add(rib);
}
// 유리 지붕의 투명 패널은 빛을 통과시키도록 얇은 패널로 구성
for(let i=0;i<8;i++){
  const x=-gardenW/2+1.0+i*(gardenW-2)/7;
  const pane=new THREE.Mesh(new THREE.PlaneGeometry(1.25,gardenD-.5),roofGlass);
  pane.rotation.x=-Math.PI/2; pane.position.set(x,roofY+roofWallH+.55,0); roofGarden.add(pane);
}

// 화단: 직사각형만 반복하지 않고 길게 이어지는 녹지 섬으로 구성
function gardenBed(x,z,w,d,count=18){
  box(roofGarden,x,roofY+.16,z,w,.28,d,mats.plantpot);
  box(roofGarden,x,roofY+.315,z,w-.16,.08,d-.16,soilMat);
  box(roofGarden,x,roofY+.36,z,w-.24,.035,d-.24,grassMat);
  for(let i=0;i<count;i++){
    const cols=Math.max(2,Math.floor(Math.sqrt(count)));
    const px=x-w*.43+(i%cols)*(w*.86/(cols-1));
    const row=Math.floor(i/Math.max(2,Math.floor(Math.sqrt(count))));
    const rows=Math.ceil(count/Math.max(2,Math.floor(Math.sqrt(count))));
    const pz=z-d*.38+row*(d*.76/Math.max(1,rows-1));
    const sc=.22+(i%4)*.055;
    const shrub=new THREE.Mesh(new THREE.IcosahedronGeometry(sc,1),leafMats[i%leafMats.length]);
    shrub.position.set(px,roofY+.48+sc*.5,pz); shrub.castShadow=true; roofGarden.add(shrub);
    if(i%4===0){
      const flower=new THREE.Mesh(new THREE.SphereGeometry(.09,8,6),bloomMats[i%bloomMats.length]);
      flower.position.set(px+.12,roofY+.58+sc*.5,pz+.08); roofGarden.add(flower);
    }
  }
}
gardenBed(-7.1,-4.7,4.4,2.7,24);
gardenBed(7.1,-4.7,4.4,2.7,24);
gardenBed(-7.1,4.55,4.4,2.65,24);
gardenBed(7.1,4.55,4.4,2.65,24);
// 중앙 종단 보행 경로가 화단에 의해 가로막히지 않도록 양끝 중앙 화단은 생성하지 않습니다.
// 중앙 종방향 주 통로(x≈0)는 연속 보행 폭을 확보하기 위해 식재 섬을 두지 않습니다.
// 가장자리 화단은 유지하고, 시각 객체와 충돌 객체가 동시에 생성되지 않도록 중앙 식재 생성을 생략합니다.

// 실내 수목과 큰 플랜터
function indoorTree(x,z,scale=1){
  cylinder(roofGarden,x,roofY+.75*scale,z,.13*scale,1.45*scale,mats.darkwood,10);
  for(const [dx,dy,dz,r] of [[0,1.65,0,.78],[.38,1.85,.12,.56],[-.35,1.78,-.12,.58],[.08,2.12,-.2,.5]]){
    const crown=new THREE.Mesh(new THREE.IcosahedronGeometry(r*scale,1),leafMats[(Math.round(x+z)+4+Math.round(r*10))%leafMats.length]);
    crown.position.set(x+dx*scale,roofY+dy*scale,z+dz*scale); crown.castShadow=true; roofGarden.add(crown);
  }
  cylinder(roofGarden,x,roofY+.2,z,.58*scale,.38,mats.plantpot,18);
}
[[-8.6,-1.6,1.05],[8.6,-1.4,1.0],[-9.0,2.5,.8],[9.0,2.5,.8]].forEach(v=>indoorTree(...v));

// 소파형 라운지 좌석과 낮은 테이블
function gardenSofa(x,z,rot=0){
  const g=new THREE.Group(); g.position.set(x,roofY+.08,z); g.rotation.y=rot; roofGarden.add(g);
  box(g,0,.28,0,2.15,.3,.72,mats.darkwood);
  box(g,0,.49,-.25,2.15,.36,.18,mats.darkwood);
  box(g,0,.46,.02,1.98,.13,.52,mats.white);
  for(const dx of [-.82,0,.82]) box(g,dx,.57,-.245,.58,.12,.12,mats.white);
}
function lowTable(x,z){
  box(roofGarden,x,roofY+.42,z,1.05,.09,.62,mats.wood);
  for(const dx of [-.38,.38]) for(const dz of [-.2,.2]) box(roofGarden,x+dx,roofY+.23,z+dz,.055,.38,.055,mats.darkwood);
}
gardenSofa(-4.7,-1.0,Math.PI/2); gardenSofa(-4.7,1.0,Math.PI/2); lowTable(-3.45,0);
gardenSofa(4.7,-1.0,-Math.PI/2); gardenSofa(4.7,1.0,-Math.PI/2); lowTable(3.45,0);
// 개별 라운지 의자와 작은 원형 테이블
for(const [x,z] of [[-2.8,4.1],[-1.1,4.1],[1.1,4.1],[2.8,4.1]]){
  cylinder(roofGarden,x,roofY+.43,z,.42,.09,mats.white,20);
  cylinder(roofGarden,x,roofY+.22,z,.055,.36,mats.metal,10);
  chair(roofGarden,x-.62,roofY,z+.12,Math.PI/2);
}
// 퍼걸러는 한쪽 코너의 포인트 휴게 공간으로 배치
const pergola=new THREE.Group(); pergola.position.set(0,0,-.1); roofGarden.add(pergola);
for(const x of [-2.3,2.3]) for(const z of [-5.0,-1.8]) box(pergola,x,roofY+1.45,z,.13,2.7,.13,mats.darkwood);
for(let x=-2.35;x<=2.35;x+=.48) box(pergola,x,roofY+2.8,-3.4,.09,.12,3.3,mats.wood);
box(pergola,0,roofY+2.7,-5.0,4.8,.12,.12,mats.darkwood);
box(pergola,0,roofY+2.7,-1.8,4.8,.12,.12,mats.darkwood);
// 조명 기둥과 따뜻한 발광 조명
for(const [x,z] of [[-5,-2.8],[5,-2.8],[-5,2.8],[5,2.8],[0,-5.5],[0,5.5]]){
  cylinder(roofGarden,x,roofY+.62,z,.045,1.15,mats.frame,8);
  const lamp=new THREE.MeshStandardMaterial({color:0xffedbf,emissive:0x8a6a2c,emissiveIntensity:.55});
  box(roofGarden,x,roofY+1.22,z,.2,.13,.2,lamp);
}
// 스카이 가든에는 엘리베이터 구조물을 배치하지 않습니다.

// 공간 선택용 투명 클릭 영역
box(roofGarden,0,roofY+.025,0,gardenW,.035,gardenD,
 new THREE.MeshStandardMaterial({color:0xffffff,transparent:true,opacity:0.001,depthWrite:false}),
 {kind:'roof',name:'32층 스카이 가든',desc:'높은 유리 아트리움과 자연광, 실내 수목, 계절 화단, 산책로, 라운지 좌석을 갖춘 개방형 스카이 가든입니다.'});

let az=0.72;
let targetAz=0.72;
let el=0.68;
let targetEl=0.68;
let dist=66;
let targetDist=66;
let lookY=totalH*.48;
let targetLookY=lookY;
let drag=false;
let px=0;
let py=0;

const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
const canvas=renderer.domElement;

canvas.addEventListener('pointerdown',e=>{
if(e.button!==0)return;
drag=true;
px=e.clientX;
py=e.clientY;
canvas.setPointerCapture(e.pointerId);
});

canvas.addEventListener('pointermove',e=>{
if(!drag)return;
targetAz-=(e.clientX-px)*.006;
targetEl=clamp(targetEl+(e.clientY-py)*.004,-.05,1.25);
px=e.clientX;
py=e.clientY;
});

function endDrag(){drag=false;}
canvas.addEventListener('pointerup',endDrag);
canvas.addEventListener('pointercancel',endDrag);

canvas.addEventListener('wheel',e=>{
e.preventDefault();
targetDist=clamp(targetDist+e.deltaY*.045,10,155);
},{passive:false});

const selector=document.getElementById('floor');
const names={
1:'로비',
...Object.fromEntries(Object.entries(themes).map(([k,v])=>[k,v[0]]))
};

for(let f=FLOORS;f>=1;f--){
const o=document.createElement('option');
o.value=f;
o.textContent=f+'층 · '+names[f];
selector.appendChild(o);
}
const roofOption=document.createElement('option');
roofOption.value='roof';
roofOption.textContent='32층 · 스카이 가든';
selector.insertBefore(roofOption,selector.options[1]||null);

let selectedFloor=null;

function applyFloor(f){
selectedFloor=f==='all'?null:(f==='roof'?'roof':Number(f));

floorGroups.forEach(g=>{
g.visible=selectedFloor===null||(typeof selectedFloor==='number'&&g.userData.floor===selectedFloor);
});
roofGarden.visible=selectedFloor===null||selectedFloor==='roof';

if(selectedFloor==='roof'){
 targetLookY=totalH+1.6; targetDist=27; targetEl=.85;
 document.getElementById('title').textContent='32층 · 스카이 가든';
 document.getElementById('description').textContent='유리 아트리움 · 실내 수목 · 계절 화단 · 산책로 · 라운지 좌석 · 퍼걸러 쉼터';
 document.getElementById('toplabel').textContent='32F · SKY GARDEN';
}else if(selectedFloor!==null){
targetLookY=(selectedFloor-1)*FLOOR_H+1.25;
targetDist=18;

const label=names[selectedFloor]||'업무 공간';
document.getElementById('title').textContent=selectedFloor+'층 · '+label;

const d=selectedFloor===1
?'리셉션 · 대기 라운지 · 방문객 안내'
:themes[selectedFloor][1];

document.getElementById('description').textContent=d+' — 공간을 클릭하면 개별 공간 설명을 확인할 수 있습니다.';
document.getElementById('toplabel').textContent=selectedFloor+'F · '+label;

}else{
targetLookY=totalH*.48;
targetDist=82;
document.getElementById('title').textContent='건물 전체';
document.getElementById('description').textContent='지상 31개 층과 32층 스카이 가든으로 구성된 가상 복합 업무 빌딩입니다. 층을 선택하면 해당 층의 내부를 자세히 볼 수 있습니다.';
document.getElementById('toplabel').textContent='31 FLOORS + 32F SKY GARDEN';
}
updateAccessVisibility();
if(typeof renderFloorEvidenceAnalysis==='function')renderFloorEvidenceAnalysis();
if(typeof updateSafetyPanel==='function')updateSafetyPanel();
}


// Floor safety scoring: only manually registered items with explicit evidence confirmation affect scores.
const safetyDeductions={경미:2,주의:5,심각:10,긴급:20};
const safetyRisks=[]; const surveyedFloors=new Set(); let nextRiskId=1; const riskMarkerGroup=new THREE.Group();root.add(riskMarkerGroup);
const riskMarkerMeshes=[];
function safetyFloorOfCurrent(){return selectedFloor==='roof'?32:(typeof selectedFloor==='number'?selectedFloor:null);}
function createRiskMarker(r){
 const item=accessItems.find(a=>a.id===r.itemId); if(!item)return;
 const group=new THREE.Group(); group.position.set(item.x,(item.floor-1)*FLOOR_H+3.35,item.z);group.userData={kind:'riskMarker',riskId:r.id};
 const col=r.severity==='긴급'||r.severity==='심각'?0xe03131:(r.severity==='주의'?0xf28c28:0xe4c542);
 const c=document.createElement('canvas');c.width=128;c.height=128;const ctx=c.getContext('2d');
 ctx.fillStyle='#'+col.toString(16).padStart(6,'0');ctx.beginPath();ctx.arc(64,64,57,0,Math.PI*2);ctx.fill();
 ctx.strokeStyle=r.severity==='긴급'?'#7f0000':'#ffffff';ctx.lineWidth=8;ctx.stroke();ctx.fillStyle='#ffffff';ctx.font='bold 68px Arial';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(r.severity==='긴급'?'⚠':'!',64,66);
 const tex=new THREE.CanvasTexture(c);tex.colorSpace=THREE.SRGBColorSpace;
 const sprite=new THREE.Sprite(new THREE.SpriteMaterial({map:tex,depthTest:false,transparent:true}));sprite.scale.set(1.0,1.0,1);sprite.renderOrder=1000;sprite.userData={kind:'riskMarker',riskId:r.id,itemId:r.itemId};group.add(sprite);
 group.userData={kind:'riskMarker',riskId:r.id,itemId:r.itemId};riskMarkerGroup.add(group);riskMarkerMeshes.push(sprite);r.marker=group;
}
function scoreFloor(f){
 const registered=safetyRisks.filter(r=>r.floor===f);
 const confirmed=registered.filter(r=>r.verified&&r.evidence.trim());
 const by={경미:0,주의:0,심각:0,긴급:0};let deduction=0;
 confirmed.forEach(r=>{by[r.severity]++;deduction+=safetyDeductions[r.severity];});
 return {registered,confirmed,by,deduction,score:Math.max(0,100-deduction),assessed:surveyedFloors.has(f)||confirmed.length>0};
}
function scoreColor(score){return score>=85?'#18845b':score>=70?'#2584c7':score>=50?'#d39a16':'#d74735';}
function updateRiskVisibility(){
 safetyRisks.forEach(r=>{if(r.marker)r.marker.visible=(selectedFloor===null||(typeof selectedFloor==='number'&&selectedFloor===r.floor));});
}
function goToRisk(r){
 const item=accessItems.find(a=>a.id===r.itemId);if(!item)return;
 selector.value=String(item.floor);applyFloor(String(item.floor));
 targetLookY=(item.floor-1)*FLOOR_H+1.2;targetDist=17;targetAz=item.x<0?-0.7:0.7;
 renderAccessItem(item);
 const el=document.getElementById('safetyMeta');el.textContent='위험 #'+r.id+' · '+item.name+' · '+r.floor+'층 · '+r.severity+' · '+(r.verified?'확인됨':'확인 필요')+' · 감점 '+(r.verified&&r.evidence.trim()?'-'+safetyDeductions[r.severity]+'점':'점수 미반영');
}
function renderFloorEvidenceAnalysis(){
 const title=document.getElementById('evidenceFloorTitle'),status=document.getElementById('evidenceStatus'),results=document.getElementById('evidenceResults');
 if(!title||!status||!results)return;
 const f=selectedFloor==='roof'?32:(typeof selectedFloor==='number'?selectedFloor:null);
 title.textContent=f===32?'32층 · 스카이 가든':(f?f+'층 · '+(names[f]||'업무 공간'):'전체 건물 · 층별 자료');
 const cards=[];let missing=[];
 const add=(name,value,source,state,detail='')=>cards.push({name,value,source,state,detail});
 const relevantItems=accessItems.filter(a=>f===null||a.floor===f);
 const relevantRecords=relevantItems.map(a=>({item:a,record:accessRecords[a.id]}));
 relevantRecords.forEach(({item,record})=>{
  if(record&&(record.rating!=='확인 필요'||(record.evidence&&record.evidence!==item.basis&&record.evidence!=='확인 필요'))){
   add(item.name,record.evidence&&record.evidence!=='확인 필요'?record.evidence:'평가 상태: '+record.rating,'사용자 입력 · 접근성 점검표',record.rating==='위험'||record.rating==='심각'?'추가 확인 필요':'등록 자료 있음','위치: '+item.loc+' · 상태: '+record.rating);
  }
 });
 const risks=safetyRisks.filter(r=>f===null||r.floor===f);
 risks.forEach(r=>{const item=accessItems.find(a=>a.id===r.itemId);add('위험 등록: '+(item?.name||'시설 위험'),r.evidence||'근거 미입력',r.source||'사용자 입력',r.verified&&String(r.evidence||'').trim()?'확인된 위험':'추가 확인 필요','층: '+r.floor+' · 심각도: '+r.severity+' · 점수 반영: '+(r.verified&&String(r.evidence||'').trim()?'예':'아니요'))});
 const water=simulatedWaterHazards.filter(h=>f===null||h.floor===f);
 water.forEach(h=>add('바닥 물기 후보',`면적 약 ${h.area.toFixed(2)} (모델 단위²)`,h.source||'시뮬레이션', '추가 확인 필요','가상 배치이며 실제 관찰 자료가 아님'));
 if(typeof autoLatest!=='undefined'&&autoLatest?.findings){
  autoLatest.findings.filter(item=>f===null||item.floor===f).forEach(item=>add('자동 모델 분석 후보 · '+(item.title||item.type||'객체 후보'),item.reason||('위험 후보값 '+Number(item.risk||0).toFixed(2)),'3D 모델 형상 분석 · 잠정','추가 확인 필요','후보 탐지 결과이며 현장 위험 확정이 아님 · '+item.floor+'층'));
 }
 const luxFloors=f===null?Object.keys(simulatedLuxByFloor).map(Number):[f];
 luxFloors.filter(n=>simulatedLuxByFloor[n]).forEach(n=>{const data=simulatedLuxByFloor[n];const spaces=data.spaces||{};Object.entries(spaces).forEach(([space,value])=>add('조도 · '+space,Number.isFinite(value)?value+' lux':'미입력',data.source||'시뮬레이션','시뮬레이션 자료','실측 조도가 아님 · '+(n===32?'32층 스카이 가든':n+'층')))});
 const mobility=mobilityEvaluations.filter(rec=>{
  const d=rec.payload||rec;const recFloor=Number(d.floor??d.data?.floor??d.values?.floor??NaN);
  return f===null||recFloor===f;
 });
 mobility.forEach(rec=>{const d=rec.payload||rec;const values=d.values||{};const present=Object.entries({통로폭:values.width,문턱:values.threshold,밀집도:values.density,조도:values.lux,바닥상태:values.floorState}).filter(([,v])=>v!==null&&v!==undefined&&v!=='');
  present.forEach(([name,value])=>add('이동 편의 측정 · '+name,String(value),d.metadata?.source||'사용자 입력',d.metadata?.verified?'증빙 정보 등록':'증빙 확인 필요','기록 #'+rec.id+' · 공간: '+(d.space||rec.space||'미지정')));
 });
 try{
  const active=typeof currentMobData==='function'?currentMobData():null;
  if(active&&(f===null||active.floor===f)){
   const values=active.values||{};const present=Object.entries({통로폭:values.width,문턱:values.threshold,밀집도:values.density,조도:values.lux,바닥상태:values.floorState,바닥재질:values.material}).filter(([,v])=>v!==null&&v!==undefined&&v!=='');
   present.forEach(([name,value])=>add('현재 입력(미저장) · '+name,String(value),active.metadata?.source||'사용자 입력 폼','미저장 · 분석에 참고 가능','공간: '+active.space));
  }
 }catch(_e){}
 if(f!==null){
  let meshCount=0;const modelRoot=f===32?roofGarden:floorGroups[f-1];if(modelRoot)modelRoot.traverse(o=>{if(o.isMesh)meshCount++;});
  add('3D 모델 객체',meshCount+'개 메시','모델 구조','모델 기반','메시 수는 실측·접근성 판정이 아니라 모델 객체 수');
 }
 const sourceCount=cards.length;
 const knownMeasurements=cards.filter(c=>/실측|측정/.test(c.source)&&!/시뮬레이션/.test(c.source)).length;
 status.textContent=sourceCount+'개 자료 항목 확인 · 사용자 입력/점검표/모델/시뮬레이션을 구분합니다. '+(knownMeasurements?'측정 관련 자료 '+knownMeasurements+'개':'실측값으로 확인된 자료 없음');
 results.innerHTML='';
 if(!cards.length){const empty=document.createElement('div');empty.className='evidenceCard';empty.innerHTML='<strong>등록 자료 없음</strong><div class="evidenceMeta">현재 선택 범위에서 입력된 점검 기록·위험 등록·이동 편의 측정 기록을 찾지 못했습니다. 모델 정보와 시뮬레이션 정보는 별도 항목으로 표시됩니다.</div>';results.appendChild(empty);}
 cards.forEach(c=>{const el=document.createElement('div');el.className='evidenceCard';const strong=document.createElement('strong');strong.textContent=c.name;el.appendChild(strong);const val=document.createElement('div');val.textContent='현재 자료: '+c.value;el.appendChild(val);const meta=document.createElement('div');meta.className='evidenceMeta';meta.textContent='자료 유형: '+c.source+' · 상태: '+c.state+(c.detail?' · '+c.detail:'');el.appendChild(meta);results.appendChild(el)});
 // Missing items are listed as missing, never interpreted as zero risk or as a safe result.
 const hasWidth=mobility.some(rec=>{const d=rec.payload||rec;return d.values?.width!==null&&d.values?.width!==undefined&&d.values?.width!==''});
 const hasThreshold=mobility.some(rec=>{const d=rec.payload||rec;return d.values?.threshold!==null&&d.values?.threshold!==undefined&&d.values?.threshold!==''});
 const hasFloor=mobility.some(rec=>{const d=rec.payload||rec;return !!d.values?.floorState});
 const hasDensity=mobility.some(rec=>{const d=rec.payload||rec;return d.values?.density!==null&&d.values?.density!==undefined&&d.values?.density!==''});
 const hasLux=mobility.some(rec=>{const d=rec.payload||rec;return d.values?.lux!==null&&d.values?.lux!==undefined&&d.values?.lux!==''});
 if(!hasWidth)missing.push('유효 통로 폭 실측/입력값');if(!hasThreshold)missing.push('문턱·단차 실측/입력값');if(!hasFloor)missing.push('바닥 상태 관찰/시험 기록');if(!hasDensity)missing.push('시간대별 밀집도');if(!hasLux)missing.push('실측 조도');
 const miss=document.createElement('div');miss.className='evidenceCard';miss.style.borderLeftColor='#9aabb6';const mh=document.createElement('strong');mh.textContent='추가 자료 필요';miss.appendChild(mh);const mp=document.createElement('div');mp.className='evidenceMeta';mp.textContent=missing.join(' · ')+' — 미입력은 0이나 안전으로 간주하지 않습니다.';miss.appendChild(mp);results.appendChild(miss);
}
function renderFloorHazardOverview(){
 const cards=document.getElementById('floorHazardCards');
 const summary=document.getElementById('floorHazardSummary');
 if(!cards||!summary)return;
 cards.innerHTML='';
 const floorRows=Array.from({length:FLOORS+1},(_,i)=>{
  const floor=i+1;
  const items=accessItems.filter(item=>item.floor===floor);
  const risks=items.map(item=>{
   const points=item.priority==='긴급'?20:(item.priority==='높음'?10:(item.priority==='보통'?5:2));
   return {...item,points};
  });
  const total=risks.reduce((sum,item)=>sum+item.points,0);
  const deduction=Math.min(100,total);
  return {floor,risks,total,deduction,score:Math.max(0,100-deduction)};
 });
 const known=floorRows.filter(row=>row.risks.length);
 summary.textContent='평가 대상 '+floorRows.length+'개 층 · 위험 후보가 등록된 층 '+known.length+'개 · 안전도 계산식: 100 − min(위험 점수 합계, 100)';
 floorRows.forEach(row=>{
  const card=document.createElement('details');
  card.style.cssText='background:white;border:1px solid #dbe3ef;border-radius:10px;margin:7px 0;padding:9px 10px';
  const head=document.createElement('summary');
  head.style.cssText='display:flex;align-items:center;justify-content:space-between;gap:8px;list-style:none;cursor:pointer;font-size:12px';
  const left=document.createElement('span');
  left.textContent=row.floor===32?'32층 · 스카이 가든':row.floor+'층';
  const right=document.createElement('strong');
  right.style.color=scoreColor(row.score);
  right.textContent=row.score+' / 100점'+(row.risks.length?'':' · 미검증');
  head.append(left,right);card.appendChild(head);
  const bar=document.createElement('div');bar.style.cssText='height:6px;background:#e5eaf0;border-radius:10px;overflow:hidden;margin:8px 0';
  const fill=document.createElement('div');fill.style.cssText='height:100%;width:'+row.score+'%;background:'+scoreColor(row.score);
  bar.appendChild(fill);card.appendChild(bar);
  const expl=document.createElement('p');expl.style.cssText='font-size:11px;line-height:1.55;color:#5c6f7c;margin:5px 0';
  expl.textContent=row.risks.length
   ?'등록된 위험 후보 '+row.risks.length+'개 · 원점수 합계 '+row.total+'점 · 적용 감점 '+row.deduction+'점. 점수는 모델에 등록된 후보를 기준으로 한 비교용 값입니다.'
   :'현재 모델 자료에서 이 층에 배정된 위험 후보를 찾지 못했습니다. 위험이 없다는 뜻이 아니므로 안전도 100점으로 확정하지 않습니다.';
  card.appendChild(expl);
  row.risks.forEach(item=>{
   const box=document.createElement('div');box.style.cssText='border-top:1px solid #edf1f6;padding:8px 0';
   const title=document.createElement('div');title.style.cssText='font-size:12px;font-weight:700';title.textContent=item.name+' · '+item.points+'점';box.appendChild(title);
   const reason=document.createElement('p');reason.style.cssText='font-size:11px;line-height:1.5;color:#526675;margin:4px 0';
   reason.textContent='위치: '+item.loc+'. 위험 이유: '+(item.impact||item.effect||'이동·이용에 불편을 줄 가능성')+' 점수 기준: '+item.priority+' 우선순위에 따라 '+item.points+'점을 부여했습니다.';
   box.appendChild(reason);
   const fix=document.createElement('p');fix.style.cssText='font-size:11px;line-height:1.5;color:#315b48;margin:3px 0';fix.textContent='개선·확인 방법: '+(item.fix||'현장 상태와 실제 치수를 확인합니다.');box.appendChild(fix);
   const source=document.createElement('p');source.style.cssText='font-size:10px;line-height:1.45;color:#87939b;margin:3px 0';source.textContent='근거 상태: '+(item.status||'확인 필요')+' · '+(item.basis||'현장 확인 전')+'. 이 항목은 실제 확인 전까지 잠정 후보입니다.';box.appendChild(source);
   card.appendChild(box);
  });
  const jump=document.createElement('button');jump.type='button';jump.textContent='이 층 보기';jump.style.cssText='margin-top:7px;padding:7px 10px;border:0;border-radius:8px;background:#eaf0ff;color:#1d4ed8;font-weight:700;font-size:11px';
  jump.onclick=()=>{if(row.floor===32){selector.value='roof';applyFloor('roof');}else{selector.value=String(row.floor);applyFloor(String(row.floor));}targetDist=17;};card.appendChild(jump);
  cards.appendChild(card);
 });
}

function updateSafetyPanel(){
 renderFloorHazardOverview();
 const current=safetyFloorOfCurrent();
 const floorScores=Array.from({length:FLOORS+1},(_,i)=>({floor:i+1,...scoreFloor(i+1)}));
 const overall= safetyRisks.filter(r=>r.verified&&r.evidence.trim());
 const selected=current?scoreFloor(current):null;
 const title=document.getElementById('safetyTitle'),scoreEl=document.getElementById('safetyScore'),meta=document.getElementById('safetyMeta');
 if(selected){
  title.textContent='평가 자료 분석';
  scoreEl.textContent=selected.assessed?selected.score+' / 100점':'평가 자료 부족';scoreEl.style.color=selected.assessed?scoreColor(selected.score):'#687b89';
  meta.textContent=(current+'층 안전 점수 요약 · 등록 위험 '+selected.registered.length+'개 · 확인된 위험 '+selected.confirmed.length+'개 · 총 감점 -'+selected.deduction+'점'+(selected.assessed?'':' · 미조사 층은 100점으로 간주하지 않습니다.'));
 }else{
  title.textContent='평가 자료 분석';
  const assessedFloors=floorScores.filter(x=>x.assessed);if(assessedFloors.length){const avg=Math.round(assessedFloors.reduce((a,x)=>a+x.score,0)/assessedFloors.length);scoreEl.textContent='평균 '+avg+' / 100점';scoreEl.style.color=scoreColor(avg);const lowest=assessedFloors.slice().sort((a,b)=>a.score-b.score)[0];meta.textContent='전체 건물 안전 점수 요약 · 평가 완료 '+assessedFloors.length+'/'+(FLOORS+1)+'개 평가 단위 · 확인된 위험 '+overall.length+'개 · 가장 낮은 평가 층 '+lowest.floor+'층';}
  else{scoreEl.textContent='평가 자료 부족';scoreEl.style.color='#687b89';meta.textContent='전체 건물 안전 점수 요약 · 확인된 위험 요소가 없습니다. 이는 위험이 없다는 뜻이 아니라 아직 확인된 데이터가 없다는 뜻입니다.';}
 }
 const floorsEl=document.getElementById('riskFloors');floorsEl.innerHTML='';
 floorScores.forEach(d=>{const b=document.createElement('button');b.className='riskFloorBtn';b.textContent=d.floor+'F'+(d.registered.length?' !':'');b.title=d.assessed?d.score+'점, 확인 위험 '+d.confirmed.length+'개':'미조사';b.textContent=d.floor+'F'+(d.registered.length?' !':'')+(d.assessed?' '+d.score:' ?');b.style.borderColor=d.assessed?scoreColor(d.score):'#9aa9b3';b.style.color=d.assessed?scoreColor(d.score):'#687b89';b.onclick=()=>{if(d.floor===32){selector.value='roof';applyFloor('roof');}else{selector.value=String(d.floor);applyFloor(String(d.floor));}};floorsEl.appendChild(b);});
 const list=document.getElementById('riskList');list.innerHTML='';
 let shown=(current? safetyRisks.filter(r=>r.floor===current):safetyRisks.slice()).sort((a,b)=>(b.verified?1:0)-(a.verified?1:0)||safetyDeductions[b.severity]-safetyDeductions[a.severity]).slice(0,5);
 if(!shown.length){list.textContent='등록된 위험 요소 없음 · 각 층의 시설을 조사하고 확인된 항목을 등록하세요.';}
 shown.forEach(r=>{const item=accessItems.find(a=>a.id===r.itemId);const row=document.createElement('div');row.className='riskRow';row.style.borderLeftColor=(r.severity==='긴급'||r.severity==='심각')?'#d74735':(r.severity==='주의'?'#f28c28':'#e4c542');const text=document.createElement('div');text.textContent='#'+r.id+' · '+r.floor+'층 · '+(item?item.name:'시설')+' · '+r.severity+' · '+(r.verified&&r.evidence.trim()?'-'+safetyDeductions[r.severity]+'점':'확인 필요, 점수 미반영');row.appendChild(text);const btn=document.createElement('button');btn.textContent='위치 보기';btn.onclick=()=>goToRisk(r);row.appendChild(btn);list.appendChild(row);});
 updateRiskVisibility();
}
const riskItemSelect=document.getElementById('riskItemSelect');
accessItems.forEach(item=>{const o=document.createElement('option');o.value=item.id;o.textContent='#'+item.id+' · '+item.floor+'층 · '+item.name;riskItemSelect.appendChild(o);});
document.getElementById('markFloorSurveyed').addEventListener('click',()=>{
 if(typeof selectedFloor!=='number'){document.getElementById('safetyMeta').textContent='먼저 층 선택 메뉴에서 조사할 층을 선택하세요.';return;}
 surveyedFloors.add(selectedFloor);updateSafetyPanel();
 document.getElementById('safetyMeta').textContent=selectedFloor+'층을 조사 완료로 표시했습니다. 확인된 위험 요소의 감점은 계속 반영됩니다.';
});
document.getElementById('riskAdd').addEventListener('click',()=>{
 const item=accessItems.find(a=>a.id===Number(riskItemSelect.value));if(!item)return;
 const severity=document.getElementById('riskSeverity').value;const evidence=document.getElementById('riskCause').value.trim();const verified=document.getElementById('riskVerified').checked;
 const existing=safetyRisks.find(r=>r.itemId===item.id);
 if(existing){existing.severity=severity;existing.evidence=evidence;existing.verified=verified;existing.floor=item.floor;}
 else{safetyRisks.push({id:nextRiskId++,itemId:item.id,floor:item.floor,severity,evidence,verified,source:'사용자 입력',marker:null});createRiskMarker(safetyRisks[safetyRisks.length-1]);}
 document.getElementById('riskCause').value='';document.getElementById('riskVerified').checked=false;
 updateSafetyPanel();
});

document.getElementById('evidenceAnalyze').addEventListener('click',renderFloorEvidenceAnalysis);
selector.addEventListener('change',()=>applyFloor(selector.value));

document.getElementById('in').onclick=()=>targetDist=clamp(targetDist-5,10,155);
document.getElementById('out').onclick=()=>targetDist=clamp(targetDist+5,10,155);
document.getElementById('inside').onclick=()=>{
targetEl=1.05;
targetDist=24;
};
document.getElementById('outside').onclick=()=>{
targetEl=.24;
targetDist=92;
};
document.getElementById('reset').onclick=()=>{
selector.value='all';
applyFloor('all');
targetAz=.72;
targetEl=.68;
targetDist=66;
};

const ray=new THREE.Raycaster();
const pointer=new THREE.Vector2();

canvas.addEventListener('click',e=>{
pointer.x=e.clientX/innerWidth*2-1;
pointer.y=-(e.clientY/innerHeight)*2+1;

ray.setFromCamera(pointer,camera);
const riskHits=ray.intersectObjects(riskMarkerMeshes.filter(m=>{let p=m;while(p){if(!p.visible)return false;p=p.parent;}return true;}),false);
if(riskHits.length){const rid=riskHits[0].object.userData.riskId;const risk=safetyRisks.find(r=>r.id===rid);if(risk){goToRisk(risk);return;}}
const accessHits=ray.intersectObjects(accessMarkerMeshes.filter(m=>{let p=m;while(p){if(!p.visible)return false;p=p.parent;}return true;}),false);
if(accessHits.length){const aid=accessHits[0].object.userData.itemId;if(aid){renderAccessItem(accessItems.find(i=>i.id===aid));return;}}

const visible=pickables.filter(m=>{
let p=m;
while(p){
if(!p.visible)return false;
p=p.parent;
}
return true;
});

const hits=ray.intersectObjects(visible,false);
if(!hits.length)return;

const obj=hits[0].object;
const data=obj.userData;

if(data.kind==='roof'){
 document.getElementById('title').textContent=data.name;
 document.getElementById('description').textContent=data.desc;
 selector.value='roof'; applyFloor('roof');
 return;
}
if(data.kind==='room'||data.kind==='floor'){
const floor=data.floor||1;

document.getElementById('title').textContent=data.name||floor+'층 공간';
document.getElementById('description').textContent=data.desc||'선택한 공간입니다.';

if(selector.value==='all'){
selector.value=String(floor);
applyFloor(String(floor));
}

targetLookY=(floor-1)*FLOOR_H+1.2;
}
});

let repairedPersonStarts=false;
function repairPersonStarts(){
  if(repairedPersonStarts)return;repairedPersonStarts=true;
  collisionByFloor=null;buildCollisionCache();
  for(const p of walkingPeople){
    const x0=p.group.position.x,z0=p.group.position.z;
    if(!staticPersonCollides(p,x0,z0)&&!walkingPeople.some(q=>q!==p&&q.floor===p.floor&&Math.hypot(q.group.position.x-x0,q.group.position.z-z0)<p.radius+q.radius+.08))continue;
    let found=null;
    // Search outward in a deterministic grid; never invent an obstacle-free spot without checking it.
    for(let r=1;r<=18&&!found;r++){
      for(let k=0;k<24&&!found;k++){
        const a=2*Math.PI*k/24, x=x0+Math.cos(a)*r*.28,z=z0+Math.sin(a)*r*.28;
        if(x < -9.7||x>9.7||z < -6.7||z>6.7)continue;
        if(!staticPersonCollides(p,x,z)&&!walkingPeople.some(q=>q!==p&&q.floor===p.floor&&Math.hypot(q.group.position.x-x,q.group.position.z-z)<p.radius+q.radius+.08))found={x,z};
      }
    }
    if(found){p.group.position.x=found.x;p.group.position.z=found.z;}
    else {p.state='pause';p.pauseDuration=1.2;p.stateTime=0;}
    p.path=null;p.pathIndex=0;p.currentSpeed=0;p.blockedTime=0;
    // Give every person a distinct set of nearby reachable waypoints instead of shared straight lanes.
    const candidates=[];
    for(let rr=1;rr<=7;rr++)for(let k=0;k<16;k++){
      const a=2*Math.PI*k/16,x=p.group.position.x+Math.cos(a)*rr*.62,z=p.group.position.z+Math.sin(a)*rr*.62;
      if(x < -9.5||x>9.5||z < -6.5||z>6.5||staticPersonCollides(p,x,z))continue;
      if(!candidates.some(c=>Math.hypot(c.x-x,c.z-z)<.55))candidates.push({x,z});
    }
    if(candidates.length>=2)p.route=[p.group.position.clone().setY(0)].map(v=>({x:v.x,z:v.z})).concat(candidates.slice((p.index*3)%Math.max(1,candidates.length), (p.index*3)%Math.max(1,candidates.length)+3));
    if(p.route.length<2)p.route=[{x:p.group.position.x,z:p.group.position.z},{x:Math.max(-9.2,Math.min(9.2,p.group.position.x+1)),z:p.group.position.z}];
    p.waypoint=1%p.route.length;
  }
}
function animate(){
requestAnimationFrame(animate);
repairPersonStarts();
const now=performance.now()*.001;
const dt=Math.min(.04,Math.max(.001,(now-(animate._lastTime||now))));animate._lastTime=now;
if(!peoplePaused)walkingPeople.forEach(p=>advancePerson(p,dt,now));
if(!peoplePaused){root.traverse(o=>{if(o.userData?.kind==='restaurant-chef'&&o.userData.animatedArms){const a=o.userData.animatedArms;a[0].rotation.z=-.62+Math.sin(now*1.8)*.12;a[1].rotation.z=.62+Math.cos(now*1.8)*.12;}});}

az+=(targetAz-az)*.1;
el+=(targetEl-el)*.1;
dist+=(targetDist-dist)*.1;
lookY+=(targetLookY-lookY)*.1;

const target=new THREE.Vector3(0,lookY,0);

camera.position.set(
target.x+Math.sin(az)*dist*Math.cos(el),
target.y+Math.sin(el)*dist,
target.z+Math.cos(az)*dist*Math.cos(el)
);

camera.lookAt(target);
renderer.render(scene,camera);
}


// Integrated mobility convenience score: only entered variables participate; missing != safe.
const mobFields=['mobWidth','mobThreshold','mobDensity','mobLux','mobFloorState','mobMaterial','mobMeasureTime','mobSource','mobMethod','mobVerified','mobExtreme','mobExtremeReason'];
const mobWeights={width:'wWidth',threshold:'wThreshold',floor:'wFloor',density:'wDensity',lux:'wLux'};
let mobilityEvaluations=[]; let currentMobilityResult=null; let loadedMobilityId=null;
const mobSpace=document.getElementById('mobSpace');
accessItems.forEach(it=>{const o=document.createElement('option');o.value=it.id;o.textContent=it.floor+'층 · '+it.loc+' · '+it.name;mobSpace.appendChild(o);});
function num(id){const v=document.getElementById(id).value;return v===''?null:Number(v);}
function cfg(id, fallback){const v=num(id);return v===null?fallback:Math.max(0,v);}
function clamp01(v){return Math.max(0,Math.min(1,v));}
function currentMobData(){
 const item=accessItems.find(x=>x.id===Number(mobSpace.value));
 return {itemId:item?item.id:null,space:item?item.loc+' · '+item.name:'미선택',floor:item?item.floor:null,values:{width:num('mobWidth'),threshold:num('mobThreshold'),density:num('mobDensity'),lux:num('mobLux'),floorState:document.getElementById('mobFloorState').value,material:document.getElementById('mobMaterial').value.trim()},metadata:{measureTime:document.getElementById('mobMeasureTime').value,source:document.getElementById('mobSource').value.trim(),method:document.getElementById('mobMethod').value.trim(),verified:document.getElementById('mobVerified').checked},extreme:{confirmed:document.getElementById('mobExtreme').checked,reason:document.getElementById('mobExtremeReason').value.trim()}};
}
function calculateMobility(data){
 const v=data.values, cWidth=cfg('cfgWidth',1.2), cNarrow=cfg('cfgNarrow',.9), cStep=cfg('cfgThreshold',2), cLux=cfg('cfgLux',400), cDensity=cfg('cfgDensity',1);
 const risks={}, missing=[];
 if(v.width!==null){if(v.width<0||v.width>20)throw Error('통로 폭은 0~20m 범위로 입력하세요.');risks.width=v.width>=cWidth?0:(v.width>=cNarrow?0.6*(cWidth-v.width)/Math.max(.001,cWidth-cNarrow):Math.min(1,0.6+0.4*(cNarrow-v.width)/Math.max(.001,cNarrow)));}else missing.push('통로 폭');
 if(v.threshold!==null){if(v.threshold<0||v.threshold>100)throw Error('문턱·단차는 0~100cm 범위로 입력하세요.');risks.threshold=clamp01(Math.max(0,v.threshold-cStep)/Math.max(1,10-cStep));}else missing.push('문턱·단차');
 if(v.floorState){risks.floor=({dry:.15,wet:.65,ice:1,tested:0})[v.floorState];}else missing.push('바닥 상태');
 if(v.density!==null){if(v.density<0||v.density>100)throw Error('밀집도는 0~100명/m² 범위로 입력하세요.');risks.density=clamp01(v.density/(2*cDensity));}else missing.push('밀집도');
 if(v.lux!==null){if(v.lux<0||v.lux>100000)throw Error('조도는 0~100000lux 범위로 입력하세요.');risks.lux=clamp01(Math.max(0,cLux-v.lux)/cLux);}else missing.push('조도');
 const present=Object.keys(risks);if(!present.length)return {score:null,risks,missing,D:null,I:null,detail:[],coverage:0,verified:false,extreme:false};
 const weights={};Object.keys(mobWeights).forEach(k=>weights[k]=cfg(mobWeights[k],0));
 let D=0;const detail=[];present.forEach(k=>{const d=weights[k]*risks[k];D+=d;detail.push({key:k,r:risks[k],weight:weights[k],deduction:d});});
 const pairs=[];for(let i=0;i<present.length;i++)for(let j=i+1;j<present.length;j++){const impact=cfg('cfgInteraction',.3)*risks[present[i]]*risks[present[j]];pairs.push({a:present[i],b:present[j],impact});}
 const I=pairs.reduce((sum,p)=>sum+p.impact,0),lambda=cfg('cfgLambda',.8);
 const evidenceComplete=!!(data.metadata.verified&&data.metadata.source&&data.metadata.method&&data.metadata.measureTime);
 const extreme=data.extreme.confirmed&&evidenceComplete&&data.extreme.reason.length>0;
 const score=extreme?0:Math.max(0,Math.min(100,100*Math.exp(-D-lambda*I)));
 const verified=evidenceComplete&&present.length===5&&missing.length===0;
 return {score,risks,missing,D,I,lambda,pairs,detail,coverage:present.length,verified,evidenceComplete,extreme,weights,settings:{cWidth,cNarrow,cStep,cLux,cDensity,lambda,interaction:cfg('cfgInteraction',.3)},data};
}
function mobilityColor(s){return s>=80?'#18845b':s>=60?'#2584c7':s>=40?'#d39a16':'#d74735';}
function renderMobility(result,data){
 currentMobilityResult=result;const score=document.getElementById('mobScore'),status=document.getElementById('mobStatus'),details=document.getElementById('mobDetails'),bar=document.getElementById('mobBarFill');
 if(result.score===null){score.textContent='평가 자료 부족';score.style.color='#687b89';bar.style.width='0%';status.textContent='입력값이 없어 점수를 계산할 수 없습니다. 미측정은 위험 0으로 처리되지 않습니다.';details.textContent='미조사 항목: '+result.missing.join(', ');return;}
 score.textContent=(result.verified?'':'잠정 ') +(result.score.toFixed(1))+' / 100점';score.style.color=mobilityColor(result.score);bar.style.width=result.score+'%';bar.style.background=mobilityColor(result.score);
 status.textContent=(result.extreme?'긴급 경고: 확인된 극단 위험 조건으로 0점 처리':result.score<20?'진입 주의 필요 · 매우 낮은 이동 편의 점수':result.score<50?'이동 편의 저하 · 개선 검토 필요':result.score<75?'일부 불편 가능 · 개선 검토':'입력된 항목 기준 이동 편의 비교 결과')+' · '+(result.verified?'5개 변수·증빙 확인됨':(result.evidenceComplete?'일부 변수 미조사 — 잠정 결과':'증빙 또는 일부 변수 미완료 — 잠정 결과'))+' · 입력 '+result.coverage+'/5개 변수';
 const names={width:'통로 폭',threshold:'문턱·단차',floor:'바닥 상태',density:'밀집도',lux:'조도'};
 let lines=['공간: '+data.space+' ('+(data.floor||'?')+'층)','기본 점수: 100','개별 위험 감점량 D = Σ(wᵢrᵢ): '+result.D.toFixed(3),'복합 위험값 I = Σ(cᵢⱼrᵢrⱼ): '+result.I.toFixed(3),'최종식: S = 100 × exp(-D - λI), λ='+result.lambda+' → '+result.score.toFixed(1)+'점'];
 result.detail.forEach(d=>lines.push(names[d.key]+': 위험값 '+d.r.toFixed(2)+' × 가중치 '+d.weight.toFixed(2)+' = D 기여 '+d.deduction.toFixed(3)));
 if(result.pairs)result.pairs.filter(p=>p.impact>0).forEach(p=>lines.push('복합 '+names[p.a]+' × '+names[p.b]+': I 기여 '+p.impact.toFixed(3)));
 lines.push('미조사 항목: '+(result.missing.length?result.missing.join(', '):'없음'));
 lines.push('바닥 위험값은 관찰 기반 프로젝트 설정값이며 미끄럼 시험을 대체하지 않음.');
 lines.push('자료 출처: '+(data.metadata.source||'미입력')+' · 측정 방법: '+(data.metadata.method||'미입력')+' · 측정 일시: '+(data.metadata.measureTime||'미입력'));
 if(data.extreme.confirmed&&!result.extreme)lines.push('극단 위험 체크는 증빙·출처·방법·일시·사유가 모두 있어야 0점 조건에 반영됨.');
 details.textContent=lines.join('\n');
}
function runMobility(){try{const d=currentMobData();const r=calculateMobility(d);renderMobility(r,d);return {d,r};}catch(e){document.getElementById('mobStatus').textContent=e.message;return null;}}
function populateMobSaved(){const sel=document.getElementById('mobSavedList');const old=sel.value;sel.innerHTML='<option value="">저장 기록 선택</option>';mobilityEvaluations.forEach(x=>{const o=document.createElement('option');o.value=x.id;o.textContent='#'+x.id+' · '+(x.space||'공간 미지정')+' · '+(x.savedAt||'');sel.appendChild(o);});if(old)sel.value=old;}
async function refreshMobSaved(){try{const res=await fetch('/api/evaluations');if(!res.ok)throw Error('서버 저장소 응답 오류');mobilityEvaluations=await res.json();populateMobSaved();if(typeof renderFloorEvidenceAnalysis==='function')renderFloorEvidenceAnalysis();}catch(e){document.getElementById('mobStatus').textContent='저장 목록을 불러오지 못했습니다: '+e.message;}}
function loadMobRecord(rec){if(!rec)return;loadedMobilityId=rec.id||null;const d=rec.payload||rec;const v=d.values||{},m=d.metadata||{},ex=d.extreme||{};if(d.itemId)mobSpace.value=String(d.itemId);document.getElementById('mobWidth').value=v.width??'';document.getElementById('mobThreshold').value=v.threshold??'';document.getElementById('mobDensity').value=v.density??'';document.getElementById('mobLux').value=v.lux??'';document.getElementById('mobFloorState').value=v.floorState||'';document.getElementById('mobMaterial').value=v.material||'';document.getElementById('mobMeasureTime').value=m.measureTime||'';document.getElementById('mobSource').value=m.source||'';document.getElementById('mobMethod').value=m.method||'';document.getElementById('mobVerified').checked=!!m.verified;document.getElementById('mobExtreme').checked=!!ex.confirmed;document.getElementById('mobExtremeReason').value=ex.reason||'';if(d.settings){Object.entries(d.settings).forEach(([k,val])=>{const ids={cWidth:'cfgWidth',cNarrow:'cfgNarrow',cStep:'cfgThreshold',cLux:'cfgLux',cDensity:'cfgDensity',lambda:'cfgLambda',interaction:'cfgInteraction'};if(ids[k])document.getElementById(ids[k]).value=val;});}if(d.weights){Object.entries(d.weights).forEach(([k,val])=>{if(mobWeights[k])document.getElementById(mobWeights[k]).value=val;});}runMobility();}
async function saveMobRecord(){const result=runMobility();if(!result)return;const {d,r}=result;if(!d.itemId){document.getElementById('mobStatus').textContent='평가 공간을 선택하세요.';return;}if(!d.metadata.source||!d.metadata.method||!d.metadata.measureTime)document.getElementById('mobStatus').textContent+=' · 출처·방법·측정 일시가 빠져 있어 저장 결과는 증빙 미완료로 유지됩니다.';
 const payload={...d,score:r.score,scoreStatus:r.verified?'증빙 확인됨':'잠정',risks:r.risks,missing:r.missing,D:r.D,I:r.I,lambda:r.lambda,weights:r.weights,settings:r.settings,formula:'층별 점수=0.8×(통행 격자 연결성·점유율·추정 최소 폭 점수-모델 장애물 감점)+0.2×조도 세부 점수; 조도 구간점수 100/85/65/40/15; 전체=32개 평가 단위 동일 가중 평균' ,updatedAt:new Date().toISOString()};
 try{const res=await fetch('/api/evaluations',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:loadedMobilityId,payload})});const out=await res.json();if(!res.ok)throw Error(out.error||'저장 실패');loadedMobilityId=out.id;await refreshMobSaved();document.getElementById('mobStatus').textContent+=' · 서버 저장 완료 (기록 #'+out.id+')';}catch(e){document.getElementById('mobStatus').textContent+=' · 서버 저장 실패: '+e.message+' (성공으로 처리하지 않았습니다)';}}
function reportMobility(){const result=runMobility();if(!result)return;const {d,r}=result;const area=document.getElementById('mobilityPrint');area.style.display='block';area.innerHTML='<h1>교통약자 이동 편의 평가 보고서</h1><p>공간: '+escapeHtml(d.space)+' · 층: '+(d.floor||'미지정')+'</p><h2>결과: '+(r.score===null?'평가 자료 부족':r.score.toFixed(1)+' / 100점 ('+(r.verified?'증빙 확인':'잠정')+')')+'</h2><p>공식: S = 100 × exp(-D - λI). D='+ (r.D===null?'미계산':r.D.toFixed(4))+'; I='+(r.I===null?'미계산':r.I.toFixed(4))+'; λ='+(r.lambda??'미계산')+'</p><pre>'+escapeHtml(document.getElementById('mobDetails').textContent)+'</pre><h3>입력 데이터 및 증빙</h3><pre>'+escapeHtml(JSON.stringify(d,null,2))+'</pre><p>이 점수는 프로젝트 내 이동 편의 비교 지표이며, 사고 확률이나 법적 안전 인증·전문가 진단을 의미하지 않습니다. 계수는 초기 설정값이며 검증 자료를 통해 조정해야 합니다.</p><p>법령 확인: <a href="https://www.law.go.kr/법령/장애인ㆍ노인ㆍ임산부등의편의증진보장에관한법률시행규칙">국가법령정보센터 - 장애인등편의법 시행규칙</a></p>';window.print();setTimeout(()=>area.style.display='none',1000);}
function escapeHtml(s){return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
document.getElementById('mobCalculate').onclick=runMobility;document.getElementById('mobRecalc').onclick=runMobility;document.getElementById('mobSave').onclick=saveMobRecord;document.getElementById('mobLoad').onclick=()=>{const rec=mobilityEvaluations.find(x=>String(x.id)===document.getElementById('mobSavedList').value);if(rec)loadMobRecord(rec);};document.getElementById('mobReport').onclick=reportMobility;
document.getElementById('mobSpace').addEventListener('change',()=>{const it=accessItems.find(x=>x.id===Number(mobSpace.value));if(it){selector.value=String(it.floor);applyFloor(String(it.floor));targetLookY=(it.floor-1)*FLOOR_H+1.2;targetDist=20;}});
['cfgWidth','cfgNarrow','cfgThreshold','cfgLux','cfgDensity','cfgLambda','wWidth','wThreshold','wFloor','wDensity','wLux','cfgInteraction'].forEach(id=>document.getElementById(id).addEventListener('change',()=>{if(currentMobilityResult)runMobility();}));

// Automatic model inspection: only reports geometry-derived candidates and clearly separates unknown field data.
let autoLatest=null, autoRecords=[];
const autoKnownUnknown=['실측 통로·출입구 유효 폭','문 상태(개방/폐쇄)와 각 실-복도 연결 그래프','문턱·단차 높이와 형상','바닥 마찰계수·습윤 상태','실제 조도(lux)','시간대별 인원 밀집도','중앙 복도 외 각 실 내부의 목적지 간 완전 경로 검증'];
function autoClassify(obj,b){
 const n=((obj.name||'')+' '+(obj.userData?.name||'')+' '+(obj.userData?.kind||'')).toLowerCase();
 if(/person|human|walker/.test(n)||obj.userData?.kind==='person')return '사람(시각화)';
 if(/door|문틀|출입/.test(n))return '문·출입구';if(/stair|계단/.test(n))return '계단';if(/elevator|lift|엘리베이터/.test(n))return '엘리베이터';
 if(/column|pillar|기둥/.test(n))return '기둥';if(/wall|벽/.test(n))return '벽';if(/floor|바닥/.test(n))return '바닥';if(/desk|table|책상|테이블/.test(n))return '가구';if(/chair|의자/.test(n))return '의자';if(/cabinet|shelf|수납|서가/.test(n))return '수납장';
 const size=new THREE.Vector3();b.getSize(size);
 if(size.y>2.45&&size.x<.5&&size.z<.5)return '기둥 후보';
 if(size.y<.22&&size.x>4&&size.z>4)return '바닥 후보';
 return '미분류 객체';
}
function auditFloorCorridor(floor){
 // Geometry-derived walkability estimate for the main modeled circulation band.
 // It deliberately reports model units (not metres) until the model scale is verified.
 if(!collisionByFloor)buildCollisionCache();
 const p={floor,radius:.24};const step=.4;
 const garden=floor===32;
 const bounds=garden?{minX:-1.6,maxX:1.6,minZ:-7.6,maxZ:7.6,axis:'z'}:{minX:-10,maxX:10,minZ:-2.4,maxZ:2.4,axis:'x'};
 const xs=[];for(let x=bounds.minX;x<=bounds.maxX+.001;x+=step)xs.push(Number(x.toFixed(3)));
 const zs=[];for(let z=bounds.minZ;z<=bounds.maxZ+.001;z+=step)zs.push(Number(z.toFixed(3)));
 const free=zs.map(z=>xs.map(x=>!staticPersonCollides(p,x,z)));
 const H=zs.length,W=xs.length,idx=(i,j)=>j*W+i;
 let freeCount=0;for(let j=0;j<H;j++)for(let i=0;i<W;i++)if(free[j][i])freeCount++;
 // Find the largest connected walkable component (8-neighbour with corner cutting prohibited).
 const seen=new Uint8Array(W*H);let largest=0,components=0;
 for(let j=0;j<H;j++)for(let i=0;i<W;i++)if(free[j][i]&&!seen[idx(i,j)]){
  components++;let count=0;const q=[[i,j]];seen[idx(i,j)]=1;
  for(let h=0;h<q.length;h++){const [ci,cj]=q[h];count++;for(const [di,dj] of [[1,0],[-1,0],[0,1],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]]){const ni=ci+di,nj=cj+dj;if(ni<0||ni>=W||nj<0||nj>=H||!free[nj][ni]||seen[idx(ni,nj)])continue;if(di&&dj&&(!free[cj][ni]||!free[nj][ci]))continue;seen[idx(ni,nj)]=1;q.push([ni,nj]);}}
  if(count>largest)largest=count;
 }
 // Test whether a walkable route joins the opposite ends of the main circulation band.
 const starts=[],targets=new Set();if(bounds.axis==='x'){for(let j=0;j<H;j++){if(free[j][0])starts.push([0,j]);if(free[j][W-1])targets.add(idx(W-1,j));}}else{for(let i=0;i<W;i++){if(free[0][i])starts.push([i,0]);if(free[H-1][i])targets.add(idx(i,H-1));}}
 const visited=new Uint8Array(W*H),queue=[];for(const [i,j] of starts){visited[idx(i,j)]=1;queue.push([i,j]);}
 let connected=false;for(let h=0;h<queue.length&&!connected;h++){const [ci,cj]=queue[h];if(targets.has(idx(ci,cj))){connected=true;break;}for(const [di,dj] of [[1,0],[-1,0],[0,1],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]]){const ni=ci+di,nj=cj+dj;if(ni<0||ni>=W||nj<0||nj>=H||!free[nj][ni]||visited[idx(ni,nj)])continue;if(di&&dj&&(!free[cj][ni]||!free[nj][ci]))continue;visited[idx(ni,nj)]=1;queue.push([ni,nj]);}}
 let minBand=Infinity;for(let i=0;i<W;i++){let best=0,run=0;for(let j=0;j<H;j++){if(free[j][i]){run++;best=Math.max(best,run);}else run=0;}minBand=Math.min(minBand,best*step);}
 if(!Number.isFinite(minBand))minBand=0;
 const freeRatio=freeCount/Math.max(1,W*H),componentRatio=largest/Math.max(1,freeCount);
 // A connected end-to-end path is the dominant factor; width and walkable area are secondary.
 const continuity=connected?1:Math.min(.35,componentRatio*.35);
 const widthFactor=Math.max(0,Math.min(1,minBand/1.6));
 const score=Math.max(0,Math.min(100,45*continuity+30*widthFactor+25*freeRatio));
 const issues=[];
 if(!connected)issues.push('주요 통행 영역의 양 끝을 잇는 연속 경로를 모델 격자에서 찾지 못함');
 if(minBand<1.2)issues.push('추정 최소 유효 폭이 1.2 모델 단위 미만인 구간이 있음');
 if(freeRatio<.72)issues.push('검사 격자에서 장애물로 판정된 비율이 높음 ('+((1-freeRatio)*100).toFixed(1)+'%)');
 if(components>1)issues.push('통행 가능 영역이 '+components+'개 연결 요소로 분리됨');
 return {floor,score,connected,minClearWidthModelUnits:Number(minBand.toFixed(2)),freeRatio:Number(freeRatio.toFixed(3)),componentCount:components,issues,grid:{step,columns:W,rows:H},scope:garden?'스카이 가든 중앙 통행 영역':'중앙 복도 및 인접 통행 영역',method:'월드 변환 AABB + 보행자 반경 0.24 모델 단위 + 0.4 단위 격자 연결성'};
}

function autoModelAnalysis(){
 const progress=document.getElementById('autoProgress'), findingsEl=document.getElementById('autoFindings');
 progress.textContent='3D 모델 구조 확인 중…';
 return new Promise(resolve=>requestAnimationFrame(async ()=>{
  try{
   await new Promise(requestAnimationFrame);
   scene.updateMatrixWorld(true);
   const meshes=[];let allMeshes=0, named=0, floorCount=0, personCount=0;
   root.traverse(o=>{if(o.isGroup&&o.userData?.kind==='person')personCount++;if(!o.isMesh||!o.geometry)return;allMeshes++;if(o.name||o.userData?.name)named++;meshes.push(o);});
   progress.textContent='공간 및 객체 분류 중…';
   await new Promise(requestAnimationFrame);
   const classified={};const floorMeshes=Array.from({length:FLOORS+1},()=>[]);
   const candidates=[];
   for(const obj of meshes){
    if(obj.userData?.kind==='person'||obj.userData?.kind==='accessMarker')continue;
    const box3=new THREE.Box3().setFromObject(obj);if(box3.isEmpty())continue;
    const center=box3.getCenter(new THREE.Vector3()), size=box3.getSize(new THREE.Vector3());
    const cls=autoClassify(obj,box3);classified[cls]=(classified[cls]||0)+1;
    const isGarden=center.y>totalH+.02 || obj.parent===roofGarden || (obj.parent&&obj.parent.name==='32층 스카이 가든');
    const floor=isGarden?32:Math.max(1,Math.min(FLOORS,Math.floor(center.y/FLOOR_H)+1));
    floorMeshes[floor-1].push({obj,box3,center,size,cls});
    // Main circulation corridor candidate zone; geometry is a screening heuristic, not proof of a real obstruction.
    const yLocal=center.y-(floor-1)*FLOOR_H;
    const corridorZone=floor===32 ? (center.x>-1.0&&center.x<1.0&&center.z>-7.6&&center.z<7.6) : (center.x>-10.5&&center.x<10.5&&center.z>-.95&&center.z<1.0);
    const plausibleObstacle=size.x>.18&&size.z>.18&&size.y>.28&&size.y<2.25&&size.x<3.2&&size.z<2.6&&yLocal>.18&&yLocal<2.2;
    const structural=/벽|바닥|기둥|계단|엘리베이터/.test(cls);
    if(corridorZone&&plausibleObstacle&&!structural){
      const footprint=Math.max(.01,size.x*size.z), heightFactor=Math.min(1,size.y/1.5);
      const risk=Math.max(.18,Math.min(.72,.18+Math.min(.32,footprint*.12)+heightFactor*.22));
      candidates.push({floor,x:center.x,y:center.y,z:center.z,size:{x:size.x,y:size.y,z:size.z},type:cls,source:'model-geometry',risk,objectName:obj.name||obj.userData?.name||'이름 없는 3D 객체',reason:'중앙 통행 후보 구역과 객체의 3D 경계 상자가 겹칩니다. 벽·바닥 등 구조물은 제외했지만, 실제 통행 방해 여부는 위치와 용도를 확인해야 합니다.'});
    }
   }
   progress.textContent='통로·장애물 후보 분석 중…';
   await new Promise(requestAnimationFrame);
   // Puddles generated in this same scene are first-class virtual hazards, not inferred from appearance.
   progress.textContent='시뮬레이션 물기와 이동 경로 관계 확인 중…';
   const waterFindings=simulatedWaterHazards.map((h,i)=>{
     const nearby=walkingPeople.filter(p=>p.floor===h.floor&&Math.hypot(p.group.position.x-h.x,p.group.position.z-h.z)<h.rx+h.rz+.5).length;
     const routeOverlap=walkingPeople.some(p=>p.floor===h.floor&&p.route.some(pt=>Math.abs(pt.x-h.x)<h.rx+.28&&Math.abs(pt.z-h.z)<h.rz+.28));
     h.routeOverlap=routeOverlap;
     return {floor:h.floor,x:h.x,y:(h.floor-1)*FLOOR_H+h.y,z:h.z,size:{x:h.rx*2,y:.01,z:h.rz*2},type:h.type,risk:routeOverlap?.72:.28,objectName:h.id,title:'화장실 바닥 물기(가상 위험)',priority:routeOverlap?'높음':'확인 필요',deduction:0,reason:`시뮬레이션에서 생성된 물기 · 면적 약 ${h.area.toFixed(2)} 모델 단위² · 이동 경로 근접/겹침 ${routeOverlap?'확인':'경로 표본상 직접 겹침 미확인'} · 인접 인물 ${nearby}명. 실제 물기나 실제 미끄럼 위험 측정값이 아닙니다.`,source:'virtual-simulation',hazardId:h.id,area:h.area,routeOverlap,createdAt:h.createdAt};
   });
   // Only a model-level screening score: unknown unit scale and missing field observations prevent a verified accessibility score.
   const unique=candidates.filter((c,i,a)=>a.findIndex(x=>x.floor===c.floor&&Math.abs(x.x-c.x)<.12&&Math.abs(x.z-c.z)<.12)===i);
   unique.push(...waterFindings);
   unique.sort((a,b)=>b.risk-a.risk);
   // Deduplicate same-cause overlapping object candidates before scoring.
   const deduped=unique.filter((c,i,a)=>a.findIndex(x=>x.floor===c.floor&&x.source===c.source&&x.type===c.type&&Math.hypot(x.x-c.x,x.z-c.z)<.45)===i);
   const findings=deduped.map((c,i)=>{const baseDeduction=(c.source==='virtual-simulation'?5.5:3.0)*c.risk;return {...c,id:'g'+i,title:c.title|| (c.source==='virtual-simulation'?'화장실 바닥 물기':'통행 구역 내 객체 후보'),baseDeduction,priority:c.risk>=.78?'매우 높음':c.risk>=.55?'높음':c.risk>=.3?'보통':'낮음',sourceType:c.source==='virtual-simulation'?'시뮬레이션':'모델 형상 기반 후보'};});
   // Rebuild once and score actual corridor grid connectivity/clearance, not only a sparse list of objects.
   collisionByFloor=null;buildCollisionCache();
   const floorScores=Array.from({length:FLOORS+1},(_,ix)=>{
    const f=ix+1,ff=findings.filter(x=>x.floor===f),audit=auditFloorCorridor(f);
    const raw=ff.reduce((sum,x)=>sum+x.baseDeduction,0);
    const lux=getFloorLux(f),referenceLux=Math.max(1,Number(document.getElementById('cfgLux')?.value)||400);
    const luxScore=luxDetailScore(lux,referenceLux),luxRisk=100-luxScore;
    // Keep geometry/obstacle penalties in the non-lighting component. Lighting is weighted once at 20%.
    const obstacleDeduction=Math.min(16,raw*.45);
    const nonLuxScore=Math.max(0,Math.min(100,audit.score-obstacleDeduction));
    const score=Math.max(0,Math.min(100,nonLuxScore*.8+luxScore*.2));
    const luxDeduction=(100-luxScore)*.2;
    const deduction=100-score;
    const level=score>=90?'이동 원활(잠정)':score>=75?'일부 제약(잠정)':score>=50?'제약 큼(잠정)':'경로 차단 우려(잠정)';
    const allIssues=[...audit.issues];if(ff.length)allIssues.push('통행 후보 객체/가상 위험 '+ff.length+'건 확인');
    return {floor:f,score,deduction:100-score,baseDeduction:obstacleDeduction,interactionDeduction:0,luxDeduction,lux,luxScore,luxRisk,referenceLux,nonLuxScore,openRatio:audit.freeRatio,findings:ff,count:ff.length,level,audit,issues:allIssues};
   });
   // Equal floor weights unless verified area/use-frequency data is available.
   const score=floorScores.reduce((a,x)=>a+x.score,0)/floorScores.length;
   const D=floorScores.reduce((a,x)=>a+x.baseDeduction,0)/floorScores.length/100;
   const I=floorScores.reduce((a,x)=>a+x.interactionDeduction,0)/floorScores.length/100;
   const criticalFloors=floorScores.filter(x=>x.score<50).map(x=>x.floor);
   const unknownUnit=true;
   autoLatest={kind:'model-screening',score,scoreStatus:'잠정 · 모델 형상/복도 연결성 기반 추정값',D,I,lambda:.8,findings:findings.sort((a,b)=>b.risk-a.risk).slice(0,80),floorScores,criticalFloors,unknown: autoKnownUnknown,meta:{createdAt:new Date().toISOString(),floors:FLOORS+1,meshCount:allMeshes,namedCount:named,personCount,classified,simulatedWaterCount:simulatedWaterHazards.length,simulatedLuxByFloor,unit:'미검증',weighting:'층별 동일 가중치(면적·이용 빈도 실측값 없음)',method:'월드 변환 객체 경계 상자 + 중앙 통행 격자 연결성/폭 추정 + 가상 물기 + 가정 조도',model:'현재 내장된 절차적 3D 모델',gardenIncluded:true,gardenFloor:32,gardenMeshCount:floorMeshes[31].length},limitations:['물기는 실제 관측이 아닌 시뮬레이션용 가상 위험 데이터이며 실제 사고 위험 측정이 아닙니다.','조도는 시각적 연출과 점수 예시를 위한 시뮬레이션값이며 실제 lux 측정이 아닙니다. 400 lux는 프로젝트 기준입니다.','모델 단위·축척이 확인되지 않아 치수 기반 법적 기준 비교를 하지 않았습니다.','객체 이름과 형상 기반 분류는 일부 미분류·오분류가 있을 수 있습니다.','충돌·통로 폭은 월드 변환 경계 상자와 0.4 모델 단위 격자로 추정하며 삼각형 단위 충돌은 아닙니다.','모델 단위·축척이 미검증이므로 추정 통로 폭은 모델 단위이며 미터 실측값이 아닙니다. 문턱, 마찰, 실제 조도, 실제 밀집도는 측정하지 않았습니다. 격자 연결성 평가는 중앙 복도와 스카이 가든 중앙 통행 영역에 한정되며, 각 실의 전체 목적지 경로와 문 개폐 상태는 완전 검증되지 않았습니다.','점수는 모델 내 중앙 통행 영역의 연결성·격자 점유율·추정 최소 폭을 반영한 잠정 비교 지표이며 인증·전문가 판정이 아닙니다.']};
   progress.textContent='점수 계산 및 결과 정리 중…';
   await new Promise(requestAnimationFrame);
   progress.textContent='이동 경로 연결과 회전 공간: 모델에 경로·축척 메타데이터가 없어 정량 판정 보류';
   renderAutoAnalysis(autoLatest);resolve(autoLatest);
  }catch(e){progress.textContent='분석을 완료하지 못했습니다: '+e.message;resolve(null);}
 }));
}
function renderAutoAnalysis(r){
 if(!r)return;const sum=document.getElementById('autoSummary'),score=document.getElementById('autoScore'),counts=document.getElementById('autoCounts'),limit=document.getElementById('autoLimit'),list=document.getElementById('autoFindings');sum.style.display='block';
 score.textContent='잠정 '+r.score.toFixed(1)+' / 100점';counts.textContent='모델 메시 '+r.meta.meshCount+'개 · 이름/메타데이터 확인 '+r.meta.namedCount+'개 · 층 '+r.meta.floors+'개 · 위험 후보 '+r.findings.length+'개 · 추가 측정 필요 '+r.unknown.length+'개';
 limit.textContent='층별 점수는 월드 변환 AABB 기반 장애물 판정, 중앙 통행 격자의 연결성·점유율·추정 최소 폭, 가상 물기 및 가정 조도를 반영한 잠정값입니다. 통로 폭은 미검증 모델 단위이며 미터 실측값이 아닙니다. 400 lux는 프로젝트 기준값이며 실측값이 아닙니다. 층별 동일 가중치로 전체 평균을 계산했습니다.';
 const grid=document.getElementById('floorScoreGrid');grid.innerHTML='';
 const gs=document.getElementById('gardenStatus');if(gs)gs.textContent='스카이 가든 분석 완료 · 32층 독립 평가 단위 · 모델 메시 '+(r.meta.gardenMeshCount??0)+'개 · 발견 위험 후보 '+(r.findings||[]).filter(x=>x.floor===32).length+'개 · 조도는 시뮬레이션값';
 const floors=r.floorScores||[];
 floors.forEach(f=>{const b=document.createElement('button');b.className='floorScoreCard';b.type='button';b.innerHTML='<span>'+(f.floor===32?'32층 · 스카이 가든':f.floor+'층')+' · '+f.level+'</span><strong>'+f.score.toFixed(1)+' / 100</strong><div class="floorScoreBar"><span style="width:'+f.score+'%;background:'+(f.score>=90?'#18845b':f.score>=75?'#2584c7':f.score>=50?'#d39a16':'#d74735')+'"></span></div><span>모델 장애물/위험 후보 '+f.count+'개 · 감점 '+f.deduction.toFixed(1)+'점</span><br><span>추정 최소 폭 '+(f.audit?f.audit.minClearWidthModelUnits:'미계산')+' 모델 단위 · 양끝 연결 '+(f.audit?.connected?'확인':'미확인')+'</span><br><span>검사 격자 통행 가능 '+(f.audit?(f.audit.freeRatio*100).toFixed(1):'미계산')+'% · 조도 시뮬레이션 '+f.lux+' lux · 조도 점수 '+f.luxScore+'/100 · 조도 위험도 '+f.luxRisk+'</span>';b.onclick=()=>{if(f.floor===32){selector.value='roof';applyFloor('roof');}else{selector.value=String(f.floor);applyFloor(String(f.floor));targetLookY=(f.floor-1)*FLOOR_H+1.2;}targetDist=17;};grid.appendChild(b);});
 const note=document.getElementById('floorScoreNote');note.textContent='전체 건물 잠정 이동 편의 지표: '+r.score.toFixed(1)+' / 100점 · 32개 평가 단위 동일 가중 평균(31개 층 + 스카이 가든). 층별 점수는 모델 경계 상자와 통행 격자 연결성·추정 최소 폭을 반영합니다. 폭은 미터가 아닌 미검증 모델 단위입니다.'+(r.criticalFloors?.length?' · 경로 제약 우려: '+r.criticalFloors.map(f=>f===32?'스카이 가든':f+'층').join(', ')+' 점수가 50점 미만입니다.':'')+'. 모델 밖 실제 출입구 상태와 실측 폭은 별도 확인이 필요합니다.';
 const luxSel=document.getElementById('floorLuxSelect');if(luxSel){const f=Number(luxSel.value||1),cur=floors.find(x=>x.floor===f);if(cur){const prevLux=Number(floorLuxOverrides['__previous_'+f]);const cmp=document.getElementById('floorLuxComparison');const snap=floorLuxPreviousSnapshot&&floorLuxPreviousSnapshot.floor===f?floorLuxPreviousSnapshot:null;cmp.textContent=(f===32?'32층 스카이 가든':f+'층')+' · 조도 '+(snap&&snap.lux!==undefined?snap.lux+' → ':'')+cur.lux+' lux · 조도 세부 점수 '+(snap&&snap.detail!==undefined?snap.detail+' → ':'')+cur.luxScore+'/100 · 조도 위험도 '+cur.luxRisk+'/100 · 층 점수 '+(snap&&snap.floorScore!==undefined?snap.floorScore.toFixed(1)+' → ':'')+cur.score.toFixed(1)+'/100 · 전체 점수 '+(snap?snap.buildingScore.toFixed(1)+' → ':'')+r.score.toFixed(1)+'/100. 조도 가중치 20%, 나머지 80%; 조도 위험도는 별도 감점으로 중복 적용하지 않음.';floorLuxPreviousSnapshot=null;}}
 list.innerHTML='';
 if(!r.findings.length){const d=document.createElement('div');d.className='autoFinding';d.textContent='현재 모델의 중앙 통행 후보 구역에서 선별 조건에 맞는 객체를 찾지 못했습니다. 이는 위험 요소가 없다는 뜻이 아닙니다. 아래 미측정 항목은 별도 확인이 필요합니다.';list.appendChild(d);}
 r.findings.forEach(f=>{const card=document.createElement('div');card.className='autoFinding';const title=document.createElement('strong');title.textContent=(f.title||'통행 구역 내 객체 후보')+' · '+f.floor+'층';card.appendChild(title);const p=document.createElement('p');p.style.margin='4px 0';p.textContent='유형: '+f.type+' · 후보 위험값 '+f.risk.toFixed(2)+' · 종합 지표 영향(근사): '+f.deduction.toFixed(2)+'점 · 출처: '+(f.sourceType||'가상 시뮬레이션');card.appendChild(p);const why=document.createElement('p');why.style.margin='4px 0';why.textContent=f.reason;card.appendChild(why);const loc=document.createElement('button');loc.textContent='위치 보기';loc.onclick=()=>{if(f.floor===32){selector.value='roof';applyFloor('roof');targetLookY=totalH+1.6;}else{selector.value=String(f.floor);applyFloor(String(f.floor));targetLookY=(f.floor-1)*FLOOR_H+1.2;}targetDist=17;targetAz=Math.atan2(f.x,f.z);targetLookY=f.y||(f.floor===32?totalH+1.6:(f.floor-1)*FLOOR_H+1.2);if(f.hazardId){const h=simulatedWaterHazards.find(q=>q.id===f.hazardId);if(h){h.mesh.material.emissive=new THREE.Color(0x126879);h.mesh.material.emissiveIntensity=.28;}}};card.appendChild(loc);const improve=document.createElement('p');improve.style.margin='4px 0';improve.textContent='개선 확인: 해당 위치의 실제 통행 폭과 객체 용도를 확인하고, 통로를 침범하는 경우 재배치 또는 통행 공간 확보를 검토합니다.';card.appendChild(improve);list.appendChild(card);});
 const unknown=document.createElement('div');unknown.className='autoFinding';unknown.style.borderLeftColor='#718796';const strong=document.createElement('strong');strong.textContent='추가 확인 필요';unknown.appendChild(strong);const ul=document.createElement('ul');ul.style.paddingLeft='18px';r.unknown.forEach(x=>{const li=document.createElement('li');li.textContent=x;ul.appendChild(li)});unknown.appendChild(ul);list.appendChild(unknown);
}
async function saveAutoAnalysis(){if(!autoLatest){document.getElementById('autoProgress').textContent='먼저 자동 분석을 실행하세요.';return;}try{const payload={space:'건물 전체 · 자동 모델 분석',floor:null,kind:autoLatest.kind,score:autoLatest.score,scoreStatus:autoLatest.scoreStatus,findings:autoLatest.findings,floorScores:autoLatest.floorScores,criticalFloors:autoLatest.criticalFloors,unknown:autoLatest.unknown,meta:autoLatest.meta,limitations:autoLatest.limitations,D:autoLatest.D,I:autoLatest.I,lambda:autoLatest.lambda,formula:'층별 점수=0.8×(통행 격자 연결성·점유율·추정 최소 폭 점수-모델 장애물 감점)+0.2×조도 세부 점수; 조도 구간점수 100/85/65/40/15; 전체=32개 평가 단위 동일 가중 평균' ,updatedAt:new Date().toISOString()};const res=await fetch('/api/evaluations',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({payload})});const out=await res.json();if(!res.ok)throw Error(out.error||'저장 실패');document.getElementById('autoProgress').textContent='분석 결과 저장 완료 · 기록 #'+out.id;await refreshAutoSaved();}catch(e){document.getElementById('autoProgress').textContent='저장 실패: '+e.message;}}
async function refreshAutoSaved(){try{const res=await fetch('/api/evaluations');if(!res.ok)throw Error('목록 조회 실패');autoRecords=await res.json();const sel=document.getElementById('autoSaved');sel.innerHTML='<option value="">저장 기록 선택</option>';autoRecords.filter(x=>x.payload?.kind==='model-screening').forEach(x=>{const o=document.createElement('option');o.value=x.id;o.textContent='#'+x.id+' · '+(x.savedAt||x.createdAt||'')+' · '+Number(x.payload.score||0).toFixed(1)+'점';sel.appendChild(o);});}catch(e){document.getElementById('autoProgress').textContent='저장 목록을 불러오지 못했습니다: '+e.message;}}
function loadAutoSaved(){const rec=autoRecords.find(x=>String(x.id)===document.getElementById('autoSaved').value);if(!rec)return;autoLatest=rec.payload;renderAutoAnalysis(autoLatest);document.getElementById('autoProgress').textContent='저장된 분석 #'+rec.id+' 불러옴 · '+(rec.savedAt||rec.createdAt||'');}
function reportAutoAnalysis(){if(!autoLatest){document.getElementById('autoProgress').textContent='먼저 자동 분석을 실행하세요.';return;}const r=autoLatest;const area=document.getElementById('mobilityPrint');area.style.display='block';area.innerHTML='<h1>3D 건물 자동 이동 편의 분석 보고서</h1><p>분석 시각: '+escapeHtml(r.meta.createdAt||'저장 분석')+'</p><h2>잠정 모델 선별 지표: '+Number(r.score).toFixed(2)+' / 100점</h2><p>계산식: 기본 위험 후보 감점 + 복합 위험 감점 + 시뮬레이션 조도 감점(감점 상한 적용)</p><p>모델 메시 수: '+r.meta.meshCount+' · 통행 구역 겹침 후보: '+r.findings.length+'</p><h3>위험 후보</h3><pre>'+escapeHtml(JSON.stringify(r.findings,null,2))+'</pre><h3>미측정 항목</h3><pre>'+escapeHtml(r.unknown.join('\n'))+'</pre><h3>한계</h3><pre>'+escapeHtml(r.limitations.join('\n'))+'</pre><p>이 보고서는 절차적 3D 모델의 경계 상자 기반 선별 결과입니다. 현장 측정, 실제 단위 확인, 전문가 검토를 대신하지 않습니다.</p>';window.print();setTimeout(()=>area.style.display='none',1200);}
document.getElementById('autoAnalyze').onclick=autoModelAnalysis;document.getElementById('autoSave').onclick=saveAutoAnalysis;document.getElementById('autoLoad').onclick=loadAutoSaved;document.getElementById('autoReport').onclick=reportAutoAnalysis;
let peoplePaused=false;document.getElementById('peopleToggle').onclick=()=>{peoplePaused=!peoplePaused;document.getElementById('peopleToggle').textContent=peoplePaused?'인물 시뮬레이션 재개':'인물 시뮬레이션 일시정지';};document.getElementById('waterRegenerate').onclick=()=>{generateSimulatedWater();collisionByFloor=null;document.getElementById('autoProgress').textContent='가상 물기 배치를 다시 생성했습니다. 다시 분석하면 위험 후보에 반영됩니다.';};
refreshAutoSaved();

refreshMobSaved();

updateAccessVisibility();
updateSafetyPanel();
animate();

window.addEventListener('resize',()=>{
camera.aspect=innerWidth/innerHeight;
camera.updateProjectionMatrix();
renderer.setSize(innerWidth,innerHeight);
});
})();
</script>
</body>
</html>
"""

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mobility_assessments.sqlite3")

def init_db():
    with sqlite3.connect(DB_PATH) as con:
        con.execute("CREATE TABLE IF NOT EXISTS evaluations (id INTEGER PRIMARY KEY AUTOINCREMENT, space TEXT NOT NULL, floor INTEGER, payload TEXT NOT NULL, created_at TEXT NOT NULL, updated_at TEXT NOT NULL)")
        con.commit()

@app.route("/")
def index():
    return PAGE

@app.route("/api/evaluations", methods=["GET", "POST"])
def evaluations_api():
    init_db()
    if request.method == "GET":
        with sqlite3.connect(DB_PATH) as con:
            con.row_factory = sqlite3.Row
            rows = con.execute("SELECT id,space,floor,payload,created_at,updated_at FROM evaluations ORDER BY updated_at DESC").fetchall()
        return jsonify([{"id":r["id"],"space":r["space"],"floor":r["floor"],"payload":json.loads(r["payload"]),"createdAt":r["created_at"],"savedAt":r["updated_at"]} for r in rows])
    body = request.get_json(silent=True) or {}
    payload = body.get("payload")
    if not isinstance(payload, dict):
        return jsonify({"error":"평가 데이터 형식이 올바르지 않습니다."}), 400
    space = str(payload.get("space") or "").strip()
    if not space or len(space) > 500:
        return jsonify({"error":"평가 공간을 선택해야 합니다."}), 400
    floor = payload.get("floor")
    if floor is not None and (not isinstance(floor, int) or floor < 1 or floor > 32):
        return jsonify({"error":"층 값이 올바르지 않습니다."}), 400
    now = datetime.now().isoformat(timespec="seconds")
    encoded = json.dumps(payload, ensure_ascii=False, allow_nan=False)
    with sqlite3.connect(DB_PATH) as con:
        row_id = body.get("id")
        if row_id is not None and (not isinstance(row_id, int) or row_id < 1):
            return jsonify({"error":"저장 기록 ID가 올바르지 않습니다."}), 400
        if row_id:
            cur = con.execute("UPDATE evaluations SET space=?,floor=?,payload=?,updated_at=? WHERE id=?", (space,floor,encoded,now,row_id))
            if cur.rowcount == 0:
                return jsonify({"error":"수정할 저장 기록을 찾지 못했습니다."}), 404
            saved_id = int(row_id)
        else:
            cur = con.execute("INSERT INTO evaluations(space,floor,payload,created_at,updated_at) VALUES(?,?,?,?,?)", (space,floor,encoded,now,now))
            saved_id = cur.lastrowid
        con.commit()
    return jsonify({"ok":True,"id":saved_id,"savedAt":now})

application = app

if __name__ == "__main__":
    app.run(debug=True)