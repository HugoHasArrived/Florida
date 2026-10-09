from flask import Flask, Response, jsonify
import os

app = Flask(__name__)

HTML = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<meta name="theme-color" content="#050907">
<title>Florida Shadows | State Trooper Horror Files</title>
<style>
:root {
  color-scheme: dark;
  --ink: #e9e6d6;
  --muted: #9ba99a;
  --red: #b83d40;
  --red-hot: #ef5c54;
  --gold: #d4bc80;
  --green: #92a789;
  --panel: rgba(5, 10, 8, .95);
  --line: #536253;
  --gap: 12px;
}
* {
  box-sizing: border-box;
  -webkit-tap-highlight-color: transparent;
}
html,
body {
  width: 100%;
  height: 100%;
  margin: 0;
  overflow: hidden;
  background: #030605;
  color: var(--ink);
  font-family: Consolas, Monaco, "Courier New", monospace;
}
body {
  user-select: none;
}
button,
input {
  font: inherit;
}
button {
  color: var(--ink);
  border: 1px solid #667563;
  background: linear-gradient(180deg, #253027, #111713);
  padding: 12px 15px;
  text-transform: uppercase;
  letter-spacing: 1px;
  cursor: pointer;
  transition: border-color .12s ease, background .12s ease, transform .12s ease;
}
button:hover,
button:focus-visible {
  border-color: var(--gold);
  background: linear-gradient(180deg, #49302a, #211715);
  outline: 1px solid #b89d60;
}
button:active {
  transform: translateY(1px);
}
button.selected {
  border-color: var(--gold);
  background: linear-gradient(180deg, #3d3b28, #20251a);
  box-shadow: inset 0 0 0 1px #928052, 0 0 14px #d6b56a18;
}
button:disabled {
  opacity: .35;
  cursor: not-allowed;
}
#game {
  position: fixed;
  inset: 0;
  width: 100%;
  height: 100%;
  display: block;
  image-rendering: pixelated;
  background: #09110d;
  cursor: crosshair;
}
#hud {
  display: none;
  position: fixed;
  inset: 0;
  z-index: 2;
  pointer-events: none;
  text-shadow: 0 2px 4px #000;
}
#topbar {
  position: absolute;
  top: 13px;
  left: 13px;
  right: 13px;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 10px;
}
.hudbox {
  max-width: min(350px, 54vw);
  padding: 10px 12px;
  background: rgba(4, 8, 6, .82);
  border: 1px solid #536253;
  box-shadow: 0 4px 18px #0008;
  font-size: 11px;
  line-height: 1.55;
}
.hudbox b {
  font-size: 10px;
  color: #e0d4b4;
  letter-spacing: 1.6px;
}
.micro {
  color: #879589;
  font-size: 9px;
  letter-spacing: .8px;
  line-height: 1.55;
}
#objective {
  max-width: 330px;
  color: #e5d19a;
  margin-top: 6px;
}
#status {
  color: #e18a81;
  margin-top: 4px;
}
#healthbar,
#staminabar {
  width: 152px;
  height: 7px;
  background: #171d17;
  border: 1px solid #79816e;
  margin-top: 5px;
}
#healthfill {
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, #79282a, #d04a42);
}
#staminafill {
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, #667c4a, #b7c77e);
}
#bottom {
  position: absolute;
  left: 13px;
  right: 13px;
  bottom: 13px;
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 12px;
}
#prompt {
  color: #e6d49f;
  min-height: 17px;
  margin-bottom: 5px;
}
#minimap {
  width: 132px;
  height: 132px;
  flex: 0 0 auto;
  border: 1px solid #82907c;
  background: #07100bde;
  box-shadow: 0 0 18px #0009;
}
#objectiveToggle {
  pointer-events: auto;
  position: absolute;
  top: 50%;
  right: 0;
  writing-mode: vertical-rl;
  border-right: 0;
  padding: 13px 8px;
  font-size: 10px;
  background: #09100cdb;
}
#toast {
  display: none;
  position: fixed;
  z-index: 12;
  left: 50%;
  top: 21%;
  transform: translateX(-50%);
  width: max-content;
  max-width: 90vw;
  padding: 12px 17px;
  background: #080c09f5;
  border: 1px solid var(--gold);
  box-shadow: 0 0 32px #000;
  color: #f0dda8;
  font-size: 12px;
  line-height: 1.5;
  letter-spacing: .5px;
  text-align: center;
}
.overlay {
  position: fixed;
  z-index: 5;
  inset: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: auto;
  padding: clamp(10px, 3vw, 30px);
  background: radial-gradient(ellipse at 48% 42%, rgba(15, 33, 24, .58), rgba(0, 0, 0, .87) 61%, rgba(0, 0, 0, .98));
}
.panel {
  position: relative;
  width: min(900px, 97vw);
  max-height: 94vh;
  overflow: auto;
  padding: clamp(20px, 4vw, 42px);
  background: linear-gradient(135deg, rgba(13, 22, 16, .98), rgba(4, 8, 6, .99));
  border: 1px solid #697966;
  box-shadow: 0 0 0 5px #000b, 0 0 76px #000;
  scrollbar-color: #54624f #101610;
}
.panel::before {
  content: "";
  position: absolute;
  inset: 7px;
  border: 1px solid #3a493b;
  pointer-events: none;
  opacity: .7;
}
.panel > * {
  position: relative;
}
.hidden {
  display: none !important;
}
.kicker {
  color: #b6c2b0;
  font-size: 10px;
  letter-spacing: 4px;
  text-transform: uppercase;
}
.logo {
  margin: 19px 0 15px;
  color: #e9e5d7;
  font-size: clamp(42px, 8vw, 84px);
  font-weight: 900;
  line-height: .82;
  letter-spacing: clamp(1px, .4vw, 5px);
  text-shadow: 4px 4px #41181b, 7px 7px #020403;
}
.logo span {
  color: #c34749;
}
.subtitle {
  color: #c8b886;
  font-size: clamp(10px, 1.7vw, 14px);
  letter-spacing: clamp(1px, .35vw, 4px);
}
.intro {
  max-width: 630px;
  color: #b9c3b6;
  font-size: 13px;
  line-height: 1.8;
}
.menu-layout {
  display: grid;
  grid-template-columns: minmax(0, 1.15fr) minmax(220px, .85fr);
  align-items: center;
  gap: 26px;
}
.menu-actions {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 9px;
  margin-top: 23px;
}
.menu-actions button:first-child {
  grid-column: 1 / -1;
  padding: 16px;
  font-weight: bold;
  background: linear-gradient(#632c30, #291719);
  border-color: #b28c68;
}
.menu-art canvas {
  display: block;
  width: 100%;
  max-height: 400px;
  image-rendering: pixelated;
}
.info-card {
  padding: 14px;
  background: #090f0b;
  border: 1px solid #3c4a3d;
  color: #b9c5b8;
  font-size: 11px;
  line-height: 1.8;
}
.info-card b {
  color: #e0d2ad;
}
.danger {
  color: #e18a7e;
}
.pc-hint {
  margin-top: 13px;
  color: #8e9a8e;
  font-size: 9px;
  letter-spacing: 1px;
}
.section-title {
  margin: 7px 0 12px;
  color: #e8e2ce;
  font-size: clamp(22px, 4vw, 30px);
}
.selection-strip {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px;
  margin: 18px 0;
}
.character {
  min-width: 0;
  padding: 12px 8px;
  text-align: center;
  text-transform: none;
  letter-spacing: 0;
  border-color: #475548;
}
.avatar {
  display: flex;
  height: 76px;
  justify-content: center;
  align-items: center;
  margin-bottom: 8px;
}
.avatar canvas {
  width: 68px;
  height: 68px;
  image-rendering: pixelated;
}
.character strong {
  display: block;
  font-size: 11px;
}
.character small {
  display: block;
  margin-top: 6px;
  color: #aeb9ac;
  font-size: 9px;
  line-height: 1.55;
}
.choice-row {
  display: flex;
  flex-wrap: wrap;
  gap: 9px;
  margin: 12px 0 18px;
}
.choice-row button {
  flex: 1;
  min-width: 140px;
}
.two-col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 13px;
}
.page-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 9px;
  margin-top: 22px;
}
.page-buttons button {
  min-width: 130px;
}
.credits-lines {
  margin: 18px 0;
  padding: 6px 0 6px 16px;
  border-left: 2px solid #963d40;
  color: #c4cebf;
  line-height: 1.8;
}
.rule-list {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 9px;
  margin: 17px 0;
}
.rule {
  padding: 11px 12px;
  border: 1px solid #344335;
  background: #0b120d;
  color: #b8c4b7;
  font-size: 11px;
  line-height: 1.65;
}
.rule b {
  display: block;
  margin-bottom: 3px;
  color: #e0d0a5;
  letter-spacing: .5px;
}
.badge {
  display: inline-block;
  padding: 4px 7px;
  margin: 3px 3px 0 0;
  border: 1px solid #695b3d;
  color: #dfcc98;
  font-size: 9px;
  letter-spacing: 1px;
}
#objectivePanel,
#inventoryPanel,
#pausePanel,
#endingPanel,
#radioPanel {
  z-index: 8;
}
.task-row {
  display: flex;
  gap: 10px;
  padding: 10px 2px;
  border-bottom: 1px solid #263328;
  color: #c3cbbb;
  font-size: 12px;
  line-height: 1.6;
}
.task-mark {
  flex: 0 0 18px;
  color: #d3bb7d;
}
.task-row.done .task-mark {
  color: #9cbf85;
}
.task-row.done .task-copy {
  color: #829283;
  text-decoration: line-through;
}
.inventory-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
  margin: 18px 0;
}
.inventory-slot {
  min-height: 85px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 7px;
  border: 1px solid #455243;
  background: #0b120e;
  color: #d1d6c7;
  text-align: center;
  font-size: 10px;
}
.inventory-slot span {
  color: #8f9b8d;
  font-size: 18px;
}
#touchControls {
  display: none;
  position: fixed;
  inset: 0;
  z-index: 3;
  pointer-events: none;
}
#dpad {
  position: absolute;
  left: 16px;
  bottom: 18px;
  width: 144px;
  height: 144px;
  pointer-events: auto;
}
#dpad button {
  position: absolute;
  width: 45px;
  height: 45px;
  padding: 0;
  background: #101911d9;
  border-color: #7f8a78;
  font-size: 19px;
  touch-action: none;
}
#up {
  left: 49px;
  top: 0;
}
#down {
  left: 49px;
  bottom: 0;
}
#left {
  left: 0;
  top: 49px;
}
#right {
  right: 0;
  top: 49px;
}
#touchActions {
  position: absolute;
  right: 15px;
  bottom: 18px;
  display: grid;
  grid-template-columns: repeat(2, 61px);
  gap: 8px;
  pointer-events: auto;
}
#touchActions button {
  width: 61px;
  height: 49px;
  padding: 2px;
  background: #101911e8;
  border-color: #7f8a78;
  font-size: 9px;
  touch-action: none;
}
body.game-active.mobile-mode #touchControls {
  display: block;
}
body.game-active.mobile-mode #bottom {
  bottom: 178px;
}
body.game-active.mobile-mode #minimap {
  width: 85px;
  height: 85px;
}
#damageFlash {
  position: fixed;
  inset: 0;
  z-index: 1;
  pointer-events: none;
  opacity: 0;
  background: radial-gradient(ellipse, transparent 35%, rgba(155, 16, 22, .55));
}
#interactNotice {
  position: fixed;
  left: 50%;
  bottom: 18%;
  z-index: 2;
  transform: translateX(-50%);
  color: #e7d5a1;
  text-shadow: 0 2px 5px black;
  font-size: 10px;
  letter-spacing: 1px;
  pointer-events: none;
}
@media (max-width: 700px) {
  .menu-layout {
    grid-template-columns: 1fr;
    gap: 5px;
  }
  .menu-art {
    display: none;
  }
  .logo {
    margin-top: 13px;
  }
  .menu-actions {
    margin-top: 13px;
  }
  .panel {
    padding: 23px;
  }
  .intro {
    font-size: 11px;
  }
  .selection-strip {
    gap: 5px;
  }
  .character {
    padding: 8px 4px;
  }
  .avatar {
    height: 55px;
  }
  .avatar canvas {
    width: 51px;
    height: 51px;
  }
  .two-col,
  .rule-list {
    grid-template-columns: 1fr;
  }
  .hudbox {
    padding: 7px 8px;
    font-size: 9px;
  }
  .hudbox b {
    font-size: 9px;
  }
  #topbar {
    top: 7px;
    left: 7px;
    right: 7px;
  }
  #bottom {
    left: 7px;
    right: 7px;
    bottom: 7px;
  }
  #minimap {
    width: 78px;
    height: 78px;
  }
  .menu-actions button {
    padding: 11px 6px;
    font-size: 10px;
  }
  .inventory-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
</head>
<body>
<canvas id="game"></canvas>
<div id="damageFlash"></div>
<div id="hud">
  <div id="topbar">
    <div class="hudbox">
      <b>FLORIDA STATE PATROL</b>
      <div class="micro">CASE FS-07 / NIGHT SHIFT</div>
      <div id="health">CONDITION: STABLE</div>
      <div id="healthbar"><div id="healthfill"></div></div>
      <div class="micro">STAMINA</div>
      <div id="staminabar"><div id="staminafill"></div></div>
    </div>
    <div class="hudbox">
      <b>ACTIVE CASE</b>
      <div id="objective">Locate the abandoned checkpoint.</div>
      <div id="status">RADIO: STANDBY</div>
      <div class="micro">OFFICER <span id="officerName">REYES</span> · <span id="timeReadout">02:17 AM</span></div>
    </div>
  </div>
  <div id="bottom">
    <div class="hudbox">
      <div id="prompt">WASD move · Shift sprint · E investigate · F flashlight</div>
      <div class="micro">AMMO <span id="ammo">6</span>/<span id="reserve">24</span> · EVIDENCE <span id="evidence">0/5</span> · SURVIVORS <span id="survivors">0/2</span> · LIGHT <span id="battery">100%</span></div>
    </div>
    <canvas id="minimap" width="132" height="132"></canvas>
  </div>
  <button id="objectiveToggle">CASE FILE [J]</button>
</div>
<div id="touchControls">
  <div id="dpad">
    <button id="up" aria-label="Move up">▲</button>
    <button id="left" aria-label="Move left">◀</button>
    <button id="right" aria-label="Move right">▶</button>
    <button id="down" aria-label="Move down">▼</button>
  </div>
  <div id="touchActions">
    <button id="touchInteract">SEARCH</button>
    <button id="touchShoot">FIRE</button>
    <button id="touchLight">LIGHT</button>
    <button id="touchReload">RELOAD</button>
    <button id="touchRun">SPRINT</button>
    <button id="touchBag">BAG</button>
  </div>
</div>
<div id="toast"></div>
<div id="interactNotice"></div>
<div id="menu" class="overlay">
  <div class="panel">
    <div class="menu-layout">
      <div>
        <div class="kicker">A pixelated detective horror</div>
        <h1 class="logo">FLORIDA<br><span>SHADOWS</span></h1>
        <div class="subtitle">STATE TROOPER HORROR FILES</div>
        <p class="intro">A midnight call. A forgotten road. A missing deputy. Something deep in the marsh is copying the voices on your radio.</p>
        <div class="menu-actions">
          <button id="start">▶ Begin patrol</button>
          <button id="characterBtn">Choose character</button>
          <button id="controlsBtn">Control mode</button>
          <button id="howBtn">How to play</button>
          <button id="creditsBtn">Credits</button>
        </div>
        <div class="pc-hint">VERSION 2.0 · SCREAM JAM 2026 · HEADPHONES RECOMMENDED</div>
      </div>
      <div class="menu-art">
        <canvas id="artCanvas" width="320" height="390"></canvas>
        <div class="info-card"><b>INCIDENT REPORT / 02:17 AM</b><br>Last transmission: “It's standing between the trees.”<br><span class="danger">UNIT 14 — SIGNAL LOST</span></div>
      </div>
    </div>
  </div>
</div>
<div id="characterPanel" class="overlay hidden">
  <div class="panel">
    <div class="kicker">Personnel records</div>
    <h2 class="section-title">Choose your officer</h2>
    <p class="intro">Each officer has a different field specialty. Your choice changes movement, resilience, and starting equipment.</p>
    <div class="selection-strip">
      <button class="character selected" data-char="reyes"><div class="avatar"><canvas id="charArt0" width="64" height="64"></canvas></div><strong>OFFICER REYES</strong><small>Balanced field kit<br>Reliable and steady</small></button>
      <button class="character" data-char="morgan"><div class="avatar"><canvas id="charArt1" width="64" height="64"></canvas></div><strong>DEPUTY MORGAN</strong><small>Extra health<br>Hard to take down</small></button>
      <button class="character" data-char="blake"><div class="avatar"><canvas id="charArt2" width="64" height="64"></canvas></div><strong>TROOPER BLAKE</strong><small>Fast response<br>Quick on their feet</small></button>
    </div>
    <div class="info-card" id="characterDetails"><b>OFFICER REYES</b><br>Experienced patrol officer. Balanced speed, stamina, and health.</div>
    <div class="page-buttons"><button id="confirmCharacter">Confirm selection</button><button id="backCharacter">Back to menu</button></div>
  </div>
</div>
<div id="controlsPanel" class="overlay hidden">
  <div class="panel">
    <div class="kicker">Input settings</div>
    <h2 class="section-title">Choose control mode</h2>
    <p class="intro">Choose the controls that match your device. You can switch this later from the main menu.</p>
    <div class="choice-row"><button id="desktopMode" class="selected">Desktop / Laptop</button><button id="mobileMode">Mobile / Touchscreen</button></div>
    <div class="two-col">
      <div class="info-card"><b>DESKTOP</b><br>WASD or arrows to move<br>Shift to sprint<br>E to investigate<br>F to toggle flashlight<br>R to reload<br>Space or left-click to fire<br>J for case file · I for inventory · Esc to pause</div>
      <div class="info-card"><b>MOBILE</b><br>Use the directional pad to move<br>Tap SEARCH to investigate<br>Tap FIRE to shoot<br>Tap LIGHT to use the flashlight<br>Tap SPRINT to run<br>Tap BAG for inventory<br>Touch buttons stay visible during play</div>
    </div>
    <div class="page-buttons"><button id="saveControls">Save control mode</button><button id="backControls">Back to menu</button></div>
  </div>
</div>
<div id="howPanel" class="overlay hidden">
  <div class="panel">
    <div class="kicker">Field manual</div>
    <h2 class="section-title">Survive the night shift</h2>
    <div class="rule-list">
      <div class="rule"><b>01 / INVESTIGATE</b>Recover five pieces of evidence. Stand near glowing objects and press E or tap SEARCH.</div>
      <div class="rule"><b>02 / RESCUE</b>Find two missing people. They will follow you once you help them.</div>
      <div class="rule"><b>03 / STAY ALIVE</b>The Smiler stalks noisy officers. Sprinting and gunshots draw its attention.</div>
      <div class="rule"><b>04 / FIGHT SMART</b>Shots can interrupt the creature but will not kill it. Smaller marsh crawlers can be killed.</div>
      <div class="rule"><b>05 / SEARCH BUILDINGS</b>Press E at doors to enter rooms. Investigate interiors for supplies and clues.</div>
      <div class="rule"><b>06 / ESCAPE</b>Find the truck keys, collect enough evidence, rescue both survivors, and reach extraction.</div>
    </div>
    <p class="intro">Search sheds for ammunition, bandages, batteries, and notes. The flashlight helps you spot details, but it also reveals your position. Watch the minimap: red marks danger, gold marks evidence, and green marks survivors.</p>
    <div class="page-buttons"><button id="backHow">Return to menu</button></div>
  </div>
</div>
<div id="creditsPanel" class="overlay hidden">
  <div class="panel">
    <div class="kicker">Case contributors</div>
    <h2 class="section-title">Credits</h2>
    <div class="credits-lines"><b>FLORIDA SHADOWS — STATE TROOPER HORROR FILES</b><br>Original browser-based pixel horror project<br>Created for Scream Jam 2026</div>
    <div class="credits-lines"><b>Special thanks to Mayumi Alingarog (Yumi, Mimi, Yumimi)</b><br>My classmate and fellow developer, for being very helpful, kind, and respectful throughout the journey.</div>
    <div class="info-card">“Every mystery leaves a trace. Every crime leaves a shadow. And some shadows are always watching.”</div>
    <div class="page-buttons"><button id="backCredits">Return to menu</button></div>
  </div>
</div>
<div id="objectivePanel" class="overlay hidden">
  <div class="panel">
    <div class="kicker">Incident FS-07</div>
    <h2 class="section-title">Case file and objectives</h2>
    <div id="taskList"></div>
    <div class="page-buttons"><button id="closeObjectives">Close case file</button></div>
  </div>
</div>
<div id="inventoryPanel" class="overlay hidden">
  <div class="panel">
    <div class="kicker">Field kit</div>
    <h2 class="section-title">Inventory</h2>
    <div id="inventorySummary" class="info-card"></div>
    <div class="inventory-grid">
      <div class="inventory-slot"><span>▣</span>Ammo boxes<br><b id="invAmmo">24</b></div>
      <div class="inventory-slot"><span>✚</span>Medical packs<br><b id="invMed">0</b></div>
      <div class="inventory-slot"><span>ϟ</span>Battery cells<br><b id="invBat">0</b></div>
      <div class="inventory-slot"><span>⌑</span>Truck keys<br><b id="invKeys">Missing</b></div>
    </div>
    <div class="page-buttons"><button id="useMed">Use medical pack</button><button id="closeInventory">Close inventory</button></div>
  </div>
</div>
<div id="pausePanel" class="overlay hidden">
  <div class="panel">
    <div class="kicker">Patrol interrupted</div>
    <h2 class="section-title">Paused</h2>
    <p class="intro">The swamp is still there when you return.</p>
    <div class="page-buttons"><button id="resume">Resume patrol</button><button id="pauseObjectives">Case file</button><button id="pauseMenu">Abandon patrol</button></div>
  </div>
</div>
<div id="endingPanel" class="overlay hidden">
  <div class="panel">
    <div class="kicker">Incident report finalized</div>
    <h2 id="endingTitle" class="section-title">Case closed</h2>
    <p id="endingText" class="intro"></p>
    <div id="endingStats" class="info-card"></div>
    <div class="page-buttons"><button id="again">Start another patrol</button><button id="toMenu">Main menu</button></div>
  </div>
</div>
<div id="radioPanel" class="overlay hidden">
  <div class="panel">
    <div class="kicker">Encrypted dispatch channel</div>
    <h2 class="section-title">Radio transcript</h2>
    <div id="radioText" class="info-card"></div>
    <div class="page-buttons"><button id="closeRadio">Return to patrol</button></div>
  </div>
</div>
<script>
(()=>{
"use strict";
const $=id=>document.getElementById(id);
const canvas=$('game');
const ctx=canvas.getContext('2d',{alpha:false});
const mini=$('minimap');
const mctx=mini.getContext('2d');
const WORLD={w:3200,h:2500};
const TILE=32;
const specs={
  reyes:{name:'Officer Reyes',color:'#29372d',shirt:'#777650',speed:158,hp:100,stamina:100,ammo:6,reserve:24},
  morgan:{name:'Deputy Morgan',color:'#2e3f37',shirt:'#555b4a',speed:145,hp:125,stamina:112,ammo:7,reserve:28},
  blake:{name:'Trooper Blake',color:'#263c32',shirt:'#8a7952',speed:178,hp:90,stamina:120,ammo:5,reserve:30}
};
const state={
  screen:'menu',
  selectedCharacter:'reyes',
  pendingCharacter:'reyes',
  controlMode:'desktop',
  pendingMode:'desktop',
  options:{shake:true,subtitles:true},
  running:false,
  paused:false,
  gameOver:false,
  won:false,
  floor:'outside',
  room:null,
  elapsed:0,
  missionClock:137,
  lastFrame:0,
  toastTimer:0,
  radioTimer:0,
  lightning:0,
  lightningNext:10,
  screenShake:0,
  damageFlash:0,
  noise:0,
  intensity:0,
  deathFade:0,
  victoryFade:0,
  discovered:0,
  rescued:0,
  keysFound:false,
  exploredRooms:0,
  kills:0,
  shots:0,
  saves:0,
  currentWeapon:'service pistol',
  audioReady:false,
  mute:false
};
let W=innerWidth;
let H=innerHeight;
let dpr=1;
let player=null;
let monster=null;
let crawlers=[];
let survivors=[];
let objects=[];
let bullets=[];
let particles=[];
let trees=[];
let wetPatches=[];
let reeds=[];
let raindrops=[];
let fireflies=[];
let decals=[];
let interiorProps=[];
let camera={x:0,y:0};
let keys={};
let pointer={x:W/2,y:H/2,down:false};
let touchRun=false;
let ammo=6;
let reserve=24;
let evidence=0;
let medkits=0;
let batteryCells=1;
let flashlightBattery=100;
let flashlight=true;
let stamina=100;
let health=100;
let footstepTimer=0;
let attackTimer=0;
let shootTimer=0;
let reloadTimer=0;
let interactCooldown=0;
let damageCooldown=0;
let growlTimer=4;
let ambientTimer=0;
let shakeX=0;
let shakeY=0;
let audioContext=null;
let masterGain=null;
let ambientOsc=null;
let rainGain=null;
let rainSource=null;
let uiStack=[];
let objectivePageOpen=false;
let inventoryPageOpen=false;
let lastSafe={x:260,y:260};
function clamp(v,min,max){return Math.max(min,Math.min(max,v))}
function lerp(a,b,t){return a+(b-a)*t}
function dist(ax,ay,bx,by){return Math.hypot(bx-ax,by-ay)}
function angleTo(ax,ay,bx,by){return Math.atan2(by-ay,bx-ax)}
function seeded(x,y){let n=Math.sin(x*127.1+y*311.7+17.17)*43758.5453;return n-Math.floor(n)}
function choose(list){return list[Math.floor(Math.random()*list.length)]}
function resize(){
  dpr=Math.min(window.devicePixelRatio||1,2);
  W=innerWidth;
  H=innerHeight;
  canvas.width=Math.floor(W*dpr);
  canvas.height=Math.floor(H*dpr);
  canvas.style.width=W+'px';
  canvas.style.height=H+'px';
  ctx.setTransform(dpr,0,0,dpr,0,0);
}
window.addEventListener('resize',resize);
resize();
function setScreen(name){
  state.screen=name;
  const mapping={
    menu:'menu',
    character:'characterPanel',
    controls:'controlsPanel',
    how:'howPanel',
    credits:'creditsPanel',
    objectives:'objectivePanel',
    inventory:'inventoryPanel',
    pause:'pausePanel',
    ending:'endingPanel',
    radio:'radioPanel'
  };
  for(const id of Object.values(mapping))$(id).classList.add('hidden');
  if(mapping[name])$(mapping[name]).classList.remove('hidden');
  if(name==='menu'||name==='character'||name==='controls'||name==='how'||name==='credits'){
    state.running=false;
    document.body.classList.remove('game-active');
  }
  if(name==='menu')drawMenuArt();
}
function toast(message,duration=2.5){
  $('toast').textContent=message;
  $('toast').style.display='block';
  state.toastTimer=duration;
}
function hideToast(){
  $('toast').style.display='none';
  state.toastTimer=0;
}
function audioStart(){
  if(state.audioReady)return;
  try{
    const AC=window.AudioContext||window.webkitAudioContext;
    if(!AC)return;
    audioContext=new AC();
    masterGain=audioContext.createGain();
    masterGain.gain.value=.18;
    masterGain.connect(audioContext.destination);
    ambientOsc=audioContext.createOscillator();
    const lowFilter=audioContext.createBiquadFilter();
    const ambientGain=audioContext.createGain();
    ambientOsc.type='sawtooth';
    ambientOsc.frequency.value=38;
    lowFilter.type='lowpass';
    lowFilter.frequency.value=115;
    ambientGain.gain.value=.09;
    ambientOsc.connect(lowFilter);
    lowFilter.connect(ambientGain);
    ambientGain.connect(masterGain);
    ambientOsc.start();
    rainGain=audioContext.createGain();
    rainGain.gain.value=.018;
    const buffer=audioContext.createBuffer(1,audioContext.sampleRate*2,audioContext.sampleRate);
    const data=buffer.getChannelData(0);
    for(let i=0;i<data.length;i++)data[i]=(Math.random()*2-1)*.25;
    rainSource=audioContext.createBufferSource();
    rainSource.buffer=buffer;
    rainSource.loop=true;
    const rainFilter=audioContext.createBiquadFilter();
    rainFilter.type='lowpass';
    rainFilter.frequency.value=950;
    rainSource.connect(rainFilter);
    rainFilter.connect(rainGain);
    rainGain.connect(masterGain);
    rainSource.start();
    state.audioReady=true;
  }catch(error){state.audioReady=false}
}
function tone(freq,duration,type='sine',volume=.12,slide=0){
  if(!audioContext||!masterGain||state.mute)return;
  try{
    const now=audioContext.currentTime;
    const osc=audioContext.createOscillator();
    const gain=audioContext.createGain();
    osc.type=type;
    osc.frequency.setValueAtTime(Math.max(25,freq),now);
    osc.frequency.exponentialRampToValueAtTime(Math.max(25,freq+slide),now+duration);
    gain.gain.setValueAtTime(volume,now);
    gain.gain.exponentialRampToValueAtTime(.001,now+duration);
    osc.connect(gain);
    gain.connect(masterGain);
    osc.start(now);
    osc.stop(now+duration+.03);
  }catch(error){}
}
function sound(name){
  if(name==='shot'){
    tone(115,.12,'sawtooth',.42,-75);
    tone(45,.19,'triangle',.25,-20);
  }
  if(name==='reload'){
    tone(480,.04,'square',.08,-180);
    setTimeout(()=>tone(310,.06,'square',.08,-90),150);
    setTimeout(()=>tone(540,.05,'square',.07,-260),370);
  }
  if(name==='pickup'){
    tone(620,.09,'sine',.12,130);
    setTimeout(()=>tone(880,.12,'sine',.1,80),75);
  }
  if(name==='hurt'){
    tone(80,.24,'sawtooth',.26,-45);
    tone(53,.3,'triangle',.16,-15);
  }
  if(name==='radio'){
    tone(750,.035,'square',.04,-340);
    setTimeout(()=>tone(510,.045,'square',.035,-400),65);
  }
  if(name==='scare'){
    tone(50,.8,'sawtooth',.28,-25);
    tone(110,.6,'square',.12,-70);
  }
  if(name==='step'){
    tone(65,.045,'triangle',.025,-22);
  }
  if(name==='door'){
    tone(95,.2,'triangle',.12,-35);
    setTimeout(()=>tone(210,.13,'square',.07,-120),110);
  }
  if(name==='roar'){
    tone(64,.6,'sawtooth',.22,-48);
    tone(39,.8,'triangle',.22,-12);
  }
}
function initializeAssets(){
  trees=[];
  wetPatches=[];
  reeds=[];
  raindrops=[];
  fireflies=[];
  decals=[];
  for(let x=35;x<WORLD.w;x+=63){
    for(let y=35;y<WORLD.h;y+=67){
      const n=seeded(x,y);
      const onRoad=nearRoad(x,y);
      const nearBuilding=buildingAt(x,y,110);
      if(n>.57&&!onRoad&&!nearBuilding){
        trees.push({x:x+(n*31),y:y+seeded(y,x)*29,s:.62+seeded(x+4,y+7)*.92,shade:Math.floor(seeded(x+7,y+3)*3),phase:seeded(y,x)*6.28,solid:true});
      }
      if(n<.09&&!onRoad){
        wetPatches.push({x:x+10,y:y+14,w:18+seeded(x+2,y)*42,h:5+seeded(x,y+8)*10});
      }
      if(n>.86&&!onRoad){
        reeds.push({x:x+12,y:y+8,h:9+seeded(y+1,x)*17,phase:seeded(x+5,y)*6});
      }
    }
  }
  for(let i=0;i<55;i++){
    fireflies.push({x:seeded(i*7,2)*WORLD.w,y:seeded(i*11,4)*WORLD.h,phase:seeded(i,4)*7,speed:.5+seeded(i,9)});
  }
  for(let i=0;i<160;i++){
    raindrops.push({x:Math.random()*W,y:Math.random()*H,speed:190+Math.random()*460,length:7+Math.random()*8});
  }
}
function roadPoints(){
  return [
    {x:120,y:-80},
    {x:320,y:280},
    {x:560,y:520},
    {x:850,y:790},
    {x:1150,y:945},
    {x:1520,y:1120},
    {x:1900,y:1390},
    {x:2240,y:1620},
    {x:2580,y:1960},
    {x:3080,y:2440}
  ];
}
function pointSegmentDistance(px,py,a,b){
  const dx=b.x-a.x;
  const dy=b.y-a.y;
  const l=dx*dx+dy*dy||1;
  const t=clamp(((px-a.x)*dx+(py-a.y)*dy)/l,0,1);
  return dist(px,py,a.x+dx*t,a.y+dy*t);
}
function nearRoad(x,y){
  const points=roadPoints();
  for(let i=0;i<points.length-1;i++){
    if(pointSegmentDistance(x,y,points[i],points[i+1])<84)return true;
  }
  return false;
}
function roadDistance(x,y){
  const points=roadPoints();
  let result=Infinity;
  for(let i=0;i<points.length-1;i++)result=Math.min(result,pointSegmentDistance(x,y,points[i],points[i+1]));
  return result;
}
function buildingAt(x,y,padding=0){
  const list=[
    {x:375,y:390,w:145,h:112},
    {x:930,y:735,w:170,h:132},
    {x:1480,y:470,w:164,h:120},
    {x:1690,y:1300,w:170,h:132},
    {x:2390,y:1740,w:178,h:136}
  ];
  return list.some(b=>x>b.x-b.w/2-padding&&x<b.x+b.w/2+padding&&y>b.y-b.h/2-padding&&y<b.y+b.h/2+padding);
}
function makeObjects(){
  objects=[
    {id:'log',x:460,y:328,type:'evidence',name:'Waterlogged patrol log',detail:'A page from Unit 14. The time is scratched out.',found:false,icon:'▤'},
    {id:'radio',x:690,y:605,type:'evidence',name:'Cracked dispatch radio',detail:'A second voice can be heard under the static.',found:false,icon:'▣'},
    {id:'cloth',x:1040,y:360,type:'evidence',name:'Torn uniform patch',detail:'The fabric is wet, but there has been no rain indoors.',found:false,icon:'▧'},
    {id:'prints',x:1425,y:970,type:'evidence',name:'Oversized footprints',detail:'The prints lead into the black water. None lead back.',found:false,icon:'⌁'},
    {id:'badge',x:1990,y:1450,type:'evidence',name:'Deputy Harlow’s badge',detail:'The metal is warm. Someone recently held it.',found:false,icon:'★'},
    {id:'shack',x:375,y:390,type:'building',name:'Checkpoint shack',detail:'A roadside patrol hut with a jammed window.',room:'checkpoint',w:145,h:112},
    {id:'station',x:930,y:735,type:'building',name:'Ranger station',detail:'A ranger station with a working generator.',room:'station',w:170,h:132},
    {id:'gas',x:1480,y:470,type:'building',name:'Swamp gas stop',detail:'A shut-down gas stop with an office in back.',room:'gas',w:164,h:120},
    {id:'cabin',x:1690,y:1300,type:'building',name:'Leaning cabin',detail:'A cabin with fresh light underneath the door.',room:'cabin',w:170,h:132},
    {id:'tower',x:2390,y:1740,type:'building',name:'Radio relay hut',detail:'The emergency relay is still receiving something.',room:'tower',w:178,h:136},
    {id:'medkit1',x:500,y:430,type:'loot',name:'First-aid pouch',loot:'medkit',found:false,icon:'+'},
    {id:'ammo1',x:1010,y:805,type:'loot',name:'Ammunition box',loot:'ammo',found:false,icon:'▪'},
    {id:'battery1',x:1525,y:520,type:'loot',name:'Flashlight batteries',loot:'battery',found:false,icon:'ϟ'},
    {id:'keys',x:2120,y:1480,type:'loot',name:'Truck keys',loot:'keys',found:false,icon:'⌑'},
    {id:'ammo2',x:2225,y:1590,type:'loot',name:'Emergency ammo pouch',loot:'ammo',found:false,icon:'▪'},
    {id:'exit',x:2920,y:2300,type:'exit',name:'Patrol truck extraction',detail:'A unit is waiting on the county road.',icon:'▰'}
  ];
  survivors=[
    {id:'ana',x:1020,y:792,name:'Mara',found:false,following:false,delivered:false,hp:1,dialogue:'Please, please get me out of here. It keeps calling from the trees.'},
    {id:'wade',x:1815,y:1360,name:'Eli',found:false,following:false,delivered:false,hp:1,dialogue:'I heard my partner on the radio. He was standing right in front of me when it spoke.'}
  ];
}
function makeRoom(name){
  const rooms={
    checkpoint:{title:'CHECKPOINT SHACK',w:700,h:480,spawn:{x:350,y:392},exit:{x:350,y:435},color:'#453f30',props:[{x:205,y:150,w:110,h:52,t:'desk'},{x:500,y:150,w:80,h:75,t:'cabinet'},{x:440,y:310,w:120,h:40,t:'bed'}],items:[{x:220,y:175,type:'note',name:'Incident memo',detail:'“Do not answer a voice if it uses your badge number.”',found:false},{x:505,y:270,type:'loot',name:'Small ammo stash',loot:'ammo',found:false}]},
    station:{title:'RANGER STATION',w:820,h:570,spawn:{x:410,y:474},exit:{x:410,y:526},color:'#3b4032',props:[{x:150,y:140,w:150,h:56,t:'desk'},{x:400,y:130,w:90,h:80,t:'shelves'},{x:660,y:160,w:70,h:140,t:'cabinet'},{x:220,y:350,w:145,h:55,t:'table'},{x:570,y:390,w:110,h:45,t:'bed'}],items:[{x:160,y:170,type:'note',name:'Missing person report',detail:'Three hikers disappeared near the drainage ditch.',found:false},{x:660,y:300,type:'loot',name:'Medical supplies',loot:'medkit',found:false},{x:416,y:180,type:'note',name:'Generator log',detail:'The generator starts when the relay is powered.',found:false}]},
    gas:{title:'SWAMP GAS STOP',w:760,h:500,spawn:{x:380,y:412},exit:{x:380,y:458},color:'#3d3b2d',props:[{x:145,y:130,w:100,h:150,t:'shelves'},{x:300,y:130,w:100,h:150,t:'shelves'},{x:560,y:120,w:130,h:70,t:'desk'},{x:520,y:320,w:115,h:45,t:'table'}],items:[{x:560,y:155,type:'note',name:'Receipt with a warning',detail:'“Do not follow the headlights past mile marker 9.”',found:false},{x:320,y:310,type:'loot',name:'Battery pack',loot:'battery',found:false}]},
    cabin:{title:'LEANING CABIN',w:760,h:520,spawn:{x:380,y:432},exit:{x:380,y:478},color:'#41372d',props:[{x:180,y:140,w:120,h:75,t:'bed'},{x:540,y:145,w:100,h:100,t:'cabinet'},{x:350,y:160,w:100,h:50,t:'desk'},{x:530,y:330,w:130,h:46,t:'table'}],items:[{x:350,y:190,type:'note',name:'Handwritten warning',detail:'It stands perfectly still until you use the flashlight.',found:false},{x:550,y:270,type:'loot',name:'Truck keys',loot:'keys',found:false}]},
    tower:{title:'RADIO RELAY HUT',w:800,h:560,spawn:{x:400,y:472},exit:{x:400,y:520},color:'#30392f',props:[{x:170,y:130,w:110,h:70,t:'desk'},{x:400,y:140,w:200,h:100,t:'console'},{x:650,y:170,w:75,h:120,t:'cabinet'},{x:380,y:340,w:180,h:50,t:'table'}],items:[{x:400,y:190,type:'note',name:'Final dispatch tape',detail:'The voice on the recording says your next line before you speak it.',found:false},{x:650,y:300,type:'loot',name:'Emergency medical pack',loot:'medkit',found:false}]}
  };
  return structuredClone(rooms[name]||rooms.checkpoint);
}
function resetGame(){
  const spec=specs[state.selectedCharacter];
  player={x:260,y:260,r:10,angle:0,speed:spec.speed,hp:spec.hp,maxHp:spec.hp,stamina:spec.stamina,maxStamina:spec.stamina,step:0,moving:false,hidden:false,invulnerable:0,flash:0,footstep:0};
  health=player.hp;
  stamina=player.stamina;
  ammo=spec.ammo;
  reserve=spec.reserve;
  evidence=0;
  medkits=1;
  batteryCells=1;
  flashlightBattery=100;
  flashlight=true;
  bullets=[];
  particles=[];
  crawlers=[];
  for(let i=0;i<5;i++){
    crawlers.push({x:760+i*410,y:420+(i%3)*450,r:9,hp:2,speed:70+Math.random()*15,phase:Math.random()*8,alert:false,attack:0,dead:false});
  }
  monster={x:2800,y:2080,r:15,stun:0,phase:0,active:false,spotted:false,attack:0,lastMove:0,warpCooldown:0};
  makeObjects();
  state.elapsed=0;
  state.missionClock=137;
  state.toastTimer=0;
  state.radioTimer=0;
  state.lightning=0;
  state.lightningNext=9;
  state.screenShake=0;
  state.damageFlash=0;
  state.noise=0;
  state.intensity=0;
  state.deathFade=0;
  state.victoryFade=0;
  state.discovered=0;
  state.rescued=0;
  state.keysFound=false;
  state.exploredRooms=0;
  state.kills=0;
  state.shots=0;
  state.saves=0;
  state.floor='outside';
  state.room=null;
  state.gameOver=false;
  state.reloadActive=false;
  state.won=false;
  state.paused=false;
  state.running=true;
  stamina=player.stamina;
  health=player.hp;
  camera={x:0,y:0};
  lastSafe={x:player.x,y:player.y};
  footstepTimer=0;
  attackTimer=0;
  shootTimer=0;
  reloadTimer=0;
  interactCooldown=0;
  damageCooldown=0;
  growlTimer=5;
  ambientTimer=0;
  initializeAssets();
  $('officerName').textContent=spec.name.toUpperCase();
  $('hud').style.display='block';
  document.body.classList.add('game-active');
  applyControlMode();
  setScreen('game');
  updateHUD();
  updateObjectives();
  audioStart();
  tone(280,.15,'sine',.08,160);
  toast('DISPATCH: Check the checkpoint. Unit 14 has gone silent.',3.5);
  state.lastFrame=performance.now();
  requestAnimationFrame(loop);
}
function applyControlMode(){
  document.body.classList.toggle('mobile-mode',state.controlMode==='mobile');
  $('desktopMode').classList.toggle('selected',state.pendingMode==='desktop');
  $('mobileMode').classList.toggle('selected',state.pendingMode==='mobile');
}
function activeOverlay(){
  return ['menu','character','controls','how','credits','objectives','inventory','pause','ending','radio'].includes(state.screen);
}
function worldCoordinates(screenX,screenY){
  return {x:screenX+camera.x,y:screenY+camera.y};
}
function nearestInteractable(){
  if(state.floor!=='outside')return nearestInteriorObject();
  let found=null;
  let best=76;
  for(const o of objects){
    if(o.type==='evidence'&&o.found)continue;
    if(o.type==='loot'&&o.found)continue;
    const d=dist(player.x,player.y,o.x,o.y);
    if(d<best){best=d;found=o;}
  }
  for(const s of survivors){
    if(s.delivered)continue;
    const d=dist(player.x,player.y,s.x,s.y);
    if(d<best){best=d;found=s;}
  }
  return found;
}
function nearestInteriorObject(){
  if(!state.room)return null;
  let nearest=null;
  let best=67;
  for(const item of state.room.items){
    if(item.found)continue;
    const d=dist(player.x,player.y,item.x,item.y);
    if(d<best){best=d;nearest=item;}
  }
  const exit=state.room.exit;
  const exitDist=dist(player.x,player.y,exit.x,exit.y);
  if(exitDist<best)return {type:'exitRoom',name:'Exit building',x:exit.x,y:exit.y};
  return nearest;
}
function interact(){
  if(!state.running||state.paused||state.gameOver||interactCooldown>0)return;
  interactCooldown=.22;
  audioStart();
  const target=nearestInteractable();
  if(!target){
    toast(state.floor==='outside'?'Nothing close enough to investigate.':'Nothing useful within reach.',1.2);
    return;
  }
  if(target.type==='evidence'||target.type==='note'){
    target.found=true;
    evidence++;
    state.discovered++;
    state.noise=Math.max(state.noise,.2);
    state.intensity=Math.min(1,state.intensity+.12);
    sound('pickup');
    showRadioText(target.name,target.detail||'The evidence may be useful later.');
    toast('EVIDENCE LOGGED: '+target.name.toUpperCase()+' — '+(target.detail||'Added to case file.'),3.1);
    updateHUD();
    updateObjectives();
    if(evidence===5)toast('FIVE CLUES RECOVERED. FIND THE SURVIVORS AND TRUCK KEYS.',3.2);
    activateMonster();
    return;
  }
  if(target.type==='building'){
    enterBuilding(target);
    return;
  }
  if(target.type==='exitRoom'){
    leaveBuilding();
    return;
  }
  if(target.type==='loot'){
    collectLoot(target);
    return;
  }
  if(target.type==='exit'){
    tryExtraction();
    return;
  }
  if(target.following===false&&target.found===false&&typeof target.dialogue==='string'){
    target.found=true;
    target.following=true;
    state.noise=.15;
    sound('pickup');
    toast(target.name.toUpperCase()+': “'+target.dialogue+'”',4);
    updateHUD();
    updateObjectives();
    activateMonster();
    return;
  }
}
function collectLoot(target){
  target.found=true;
  sound('pickup');
  if(target.loot==='ammo'){
    reserve+=12;
    toast('AMMUNITION SECURED: +12 ROUNDS.');
  }
  if(target.loot==='medkit'){
    medkits++;
    toast('FIRST-AID SUPPLIES ADDED TO YOUR KIT.');
  }
  if(target.loot==='battery'){
    batteryCells++;
    flashlightBattery=Math.min(100,flashlightBattery+22);
    toast('FLASHLIGHT BATTERIES RECOVERED.');
  }
  if(target.loot==='keys'){
    state.keysFound=true;
    toast('PICKED UP THE PATROL TRUCK KEYS. EXTRACTION IS AVAILABLE.');
  }
  updateHUD();
  updateInventory();
  updateObjectives();
}
function enterBuilding(target){
  if(state.floor!=='outside')return;
  state.floor='inside';
  state.room=makeRoom(target.room);
  player.x=state.room.spawn.x;
  player.y=state.room.spawn.y;
  player.angle=-Math.PI/2;
  player.speed=specs[state.selectedCharacter].speed*.84;
  state.exploredRooms++;
  bullets=[];
  sound('door');
  toast('ENTERED: '+state.room.title+'. LISTEN BEFORE MOVING.',2.4);
  camera={x:0,y:0};
  updateHUD();
}
function leaveBuilding(){
  if(state.floor!=='inside'||!state.room)return;
  const exitName=state.room.title;
  state.floor='outside';
  state.room=null;
  player.speed=specs[state.selectedCharacter].speed;
  player.x=clamp(player.x+0,50,WORLD.w-50);
  player.y=clamp(player.y+0,50,WORLD.h-50);
  if(exitName==='CHECKPOINT SHACK'){player.x=375;player.y=470;}
  if(exitName==='RANGER STATION'){player.x=930;player.y=815;}
  if(exitName==='SWAMP GAS STOP'){player.x=1480;player.y=545;}
  if(exitName==='LEANING CABIN'){player.x=1690;player.y=1380;}
  if(exitName==='RADIO RELAY HUT'){player.x=2390;player.y=1820;}
  camera={x:clamp(player.x-W/2,0,WORLD.w-W),y:clamp(player.y-H/2,0,WORLD.h-H)};
  sound('door');
  toast('BACK OUTSIDE. THE RAIN HAS NOT STOPPED.',1.8);
  updateHUD();
}
function showRadioText(title,detail){
  $('radioText').innerHTML='<b>'+escapeHTML(title.toUpperCase())+'</b><br><br>'+escapeHTML(detail)+'<br><br><span style="color:#8b9a8b">EVIDENCE LOG UPDATED</span>';
  if(state.options.subtitles){
    state.radioTimer=7;
    state.radioLine=title+': '+detail;
  }
}
function escapeHTML(value){
  return String(value).replace(/[&<>"']/g,char=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
}
function activateMonster(){
  if(monster.active)return;
  monster.active=true;
  monster.x=player.x+choose([-1,1])*650;
  monster.y=player.y+choose([-1,1])*500;
  monster.x=clamp(monster.x,100,WORLD.w-100);
  monster.y=clamp(monster.y,100,WORLD.h-100);
  monster.spotted=false;
  sound('scare');
  toast('THE RADIO CUTS OUT. SOMETHING IS MOVING THROUGH THE TREES.',3.3);
  state.screenShake=.4;
}
function currentTasks(){
  return [
    {done:evidence>=5,text:'Recover five evidence items ('+evidence+'/5).'},
    {done:survivors.filter(s=>s.delivered).length>=2,text:'Find and escort two missing people ('+survivors.filter(s=>s.delivered).length+'/2).'},
    {done:state.keysFound,text:'Locate the patrol truck keys.'},
    {done:state.exploredRooms>=2,text:'Search at least two buildings ('+state.exploredRooms+'/2).'},
    {done:state.won,text:'Reach the extraction point alive.'}
  ];
}
function updateObjectives(){
  const tasks=currentTasks();
  $('taskList').innerHTML=tasks.map(t=>'<div class="task-row '+(t.done?'done':'')+'"><div class="task-mark">'+(t.done?'✓':'□')+'</div><div class="task-copy">'+escapeHTML(t.text)+'</div></div>').join('');
}
function updateHUD(){
  if(!player)return;
  $('health').textContent=player.hp>70?'CONDITION: STABLE':player.hp>35?'CONDITION: WOUNDED':'CONDITION: CRITICAL';
  $('healthfill').style.width=clamp(player.hp/player.maxHp*100,0,100)+'%';
  $('staminafill').style.width=clamp(stamina/player.maxStamina*100,0,100)+'%';
  $('ammo').textContent=ammo;
  $('reserve').textContent=reserve;
  $('evidence').textContent=evidence+'/5';
  $('survivors').textContent=survivors.filter(s=>s.delivered).length+'/2';
  $('battery').textContent=Math.floor(flashlightBattery)+'%';
  $('officerName').textContent=specs[state.selectedCharacter].name.toUpperCase();
  const minutes=Math.floor(state.missionClock/60);
  const seconds=Math.floor(state.missionClock%60);
  $('timeReadout').textContent=String(2+Math.floor(minutes/60)).padStart(2,'0')+':'+String(minutes%60).padStart(2,'0')+' AM';
  $('status').textContent=monster&&monster.active?'RADIO: SIGNAL LOST':'RADIO: DISPATCH STANDBY';
  const completeSurvivors=survivors?survivors.filter(s=>s.delivered).length:0;
  if(evidence<5){$('objective').textContent='Collect evidence '+evidence+'/5. Search the buildings.';}
  else if(completeSurvivors<2){$('objective').textContent='Find the missing people '+completeSurvivors+'/2.';}
  else if(!state.keysFound){$('objective').textContent='Find the patrol truck keys.';}
  else{$('objective').textContent='Reach the roadside extraction point.';}
  const near=player&&state.running?nearestInteractable():null;
  if(near){
    $('prompt').textContent='E / SEARCH — '+String(near.name||'Investigate').toUpperCase();
    $('interactNotice').textContent='[ E ]  '+String(near.name||'INVESTIGATE').toUpperCase();
  }else{
    $('prompt').textContent=state.floor==='inside'?'WASD MOVE · E SEARCH · F FLASHLIGHT · ESC PAUSE':'WASD MOVE · SHIFT SPRINT · E SEARCH · F FLASHLIGHT · CLICK FIRE';
    $('interactNotice').textContent='';
  }
}
function updateInventory(){
  $('inventorySummary').innerHTML='<b>'+escapeHTML(specs[state.selectedCharacter].name.toUpperCase())+'</b><br>Health: '+Math.ceil(player.hp)+' / '+player.maxHp+'<br>Stamina: '+Math.ceil(stamina)+' / '+player.maxStamina+'<br>Loaded magazine: '+ammo+' rounds<br>Spare ammunition: '+reserve+' rounds<br>Flashlight: '+Math.floor(flashlightBattery)+'%';
  $('invAmmo').textContent=reserve;
  $('invMed').textContent=medkits;
  $('invBat').textContent=batteryCells;
  $('invKeys').textContent=state.keysFound?'Found':'Missing';
  $('useMed').disabled=medkits<=0||player.hp>=player.maxHp;
}
function useMedkit(){
  if(medkits<=0){toast('NO MEDICAL PACKS LEFT.');return;}
  if(player.hp>=player.maxHp){toast('YOU ARE ALREADY IN GOOD CONDITION.');return;}
  medkits--;
  player.hp=Math.min(player.maxHp,player.hp+42);
  health=player.hp;
  sound('pickup');
  toast('FIELD DRESSING APPLIED. HEALTH RESTORED.');
  updateHUD();
  updateInventory();
}
function tryExtraction(){
  const delivered=survivors.filter(s=>s.delivered).length;
  if(evidence<5){toast('DISPATCH REFUSES TO CLEAR EXTRACTION. EVIDENCE '+evidence+'/5.',2.7);return;}
  if(delivered<2){toast('YOU CANNOT LEAVE THEM BEHIND. SURVIVORS '+delivered+'/2.',2.7);return;}
  if(!state.keysFound){toast('THE TRUCK IS LOCKED. FIND THE KEYS.',2.7);return;}
  state.won=true;
  finishGame(true);
}
function finishGame(success){
  state.gameOver=true;
  state.running=false;
  state.won=success;
  state.screen='ending';
  $('hud').style.display='none';
  document.body.classList.remove('game-active');
  $('endingTitle').textContent=success?'CASE FILE: SURVIVORS RECOVERED':'OFFICER LOST IN THE MARSH';
  $('endingText').textContent=success?'You got the survivors out and brought back the evidence. Dispatch never explains the extra voice on the recording. On the final playback, it sounds exactly like you.':'Your radio keeps transmitting after your pulse stops. The rescue team finds your patrol car empty and the flashlight still on.';
  $('endingStats').innerHTML='TIME IN FIELD: '+Math.floor(state.elapsed/60)+' MINUTES<br>EVIDENCE RECOVERED: '+evidence+'/5<br>SURVIVORS EXTRACTED: '+survivors.filter(s=>s.delivered).length+'/2<br>CRAWLERS NEUTRALIZED: '+state.kills+'<br>SHOTS FIRED: '+state.shots+'<br>BUILDINGS SEARCHED: '+state.exploredRooms;
  setScreen('ending');
  if(success)tone(460,.4,'sine',.1,180);else sound('scare');
}
function enterScreen(name){
  if(!state.running)return;
  state.running=false;
  state.paused=true;
  setScreen(name);
}
function closeOverlay(){
  state.paused=false;
  state.running=true;
  state.screen='game';
  for(const id of ['objectivePanel','inventoryPanel','pausePanel','radioPanel'])$(id).classList.add('hidden');
  $('hud').style.display='block';
  document.body.classList.add('game-active');
  state.lastFrame=performance.now();
  requestAnimationFrame(loop);
}
function pauseGame(){
  if(!state.running||state.gameOver)return;
  state.paused=true;
  state.running=false;
  setScreen('pause');
}
function openObjectives(){
  if(!state.running)return;
  updateObjectives();
  enterScreen('objectives');
}
function openInventory(){
  if(!state.running)return;
  updateInventory();
  enterScreen('inventory');
}
function reloadWeapon(){
  if(reloadTimer>0)return;
  if(ammo>=6){toast('MAGAZINE ALREADY FULL.',1.2);return;}
  if(reserve<=0){toast('NO SPARE AMMUNITION.',1.5);return;}
  reloadTimer=.78;
  state.reloadActive=true;
  sound('reload');
  toast('RELOADING...',.9);
}
function shoot(){
  if(!state.running||state.paused||state.gameOver||state.floor==='inside')return;
  if(shootTimer>0||reloadTimer>0)return;
  if(ammo<=0){toast('CLICK. RELOAD WITH R.',1.1);tone(180,.05,'square',.04,-80);return;}
  audioStart();
  shootTimer=.27;
  ammo--;
  state.shots++;
  state.noise=1;
  state.intensity=Math.min(1,state.intensity+.14);
  sound('shot');
  state.screenShake=state.options.shake?.10:0;
  const target=worldCoordinates(pointer.x,pointer.y);
  const a=angleTo(player.x,player.y,target.x,target.y);
  player.angle=a;
  bullets.push({x:player.x+Math.cos(a)*17,y:player.y+Math.sin(a)*17,vx:Math.cos(a)*620,vy:Math.sin(a)*620,life:.72,owner:'player',r:3});
  for(let i=0;i<9;i++){
    particles.push({x:player.x+Math.cos(a)*16,y:player.y+Math.sin(a)*16,vx:Math.cos(a+Math.random()-.5)*(60+Math.random()*150),vy:Math.sin(a+Math.random()-.5)*(60+Math.random()*150),life:.15+Math.random()*.18,color:choose(['#f6daa2','#c7ab69','#f5e9c7']),size:1+Math.random()*2});
  }
  updateHUD();
}
function damagePlayer(amount,source){
  if(player.invulnerable>0||state.gameOver)return;
  player.hp=Math.max(0,player.hp-amount);
  health=player.hp;
  player.invulnerable=.65;
  state.damageFlash=.7;
  state.screenShake=state.options.shake?.25:0;
  state.noise=1;
  sound('hurt');
  toast(source==='smiler'?'IT IS RIGHT BEHIND YOU.':'SOMETHING BITES THROUGH YOUR UNIFORM.',1.6);
  updateHUD();
  if(player.hp<=0)finishGame(false);
}
function movePlayer(dt){
  if(state.floor==='inside'){
    moveInteriorPlayer(dt);
    return;
  }
  let dx=(keys.d||keys.arrowright?1:0)-(keys.a||keys.arrowleft?1:0);
  let dy=(keys.s||keys.arrowdown?1:0)-(keys.w||keys.arrowup?1:0);
  if(Math.abs(dx)+Math.abs(dy)>0){
    const len=Math.hypot(dx,dy)||1;
    dx/=len;
    dy/=len;
    player.moving=true;
    const wantsRun=keys.shift||touchRun;
    const running=wantsRun&&stamina>2;
    const speed=player.speed*(running?1.55:1);
    if(running){
      stamina=Math.max(0,stamina-26*dt);
      state.noise=Math.max(state.noise,.58);
    }else{
      stamina=Math.min(player.maxStamina,stamina+17*dt);
      state.noise=Math.max(state.noise,.15);
    }
    const nx=player.x+dx*speed*dt;
    const ny=player.y+dy*speed*dt;
    if(!blockedAt(nx,player.y,player.r))player.x=nx;
    if(!blockedAt(player.x,ny,player.r))player.y=ny;
    player.angle=angleTo(0,0,dx,dy);
    player.step+=dt*(running?13:8);
    footstepTimer+=dt*(running?1.6:1);
    if(footstepTimer>(running?.28:.52)){
      footstepTimer=0;
      if(Math.random()<.6)sound('step');
    }
    if(running)state.intensity=Math.min(1,state.intensity+dt*.03);
  }else{
    player.moving=false;
    stamina=Math.min(player.maxStamina,stamina+21*dt);
    state.noise=Math.max(0,state.noise-dt*.5);
  }
  player.x=clamp(player.x,22,WORLD.w-22);
  player.y=clamp(player.y,22,WORLD.h-22);
}
function blockedAt(x,y,r){
  for(const t of trees){
    if(Math.abs(t.x-x)>r+12||Math.abs(t.y-y)>r+15)continue;
    if(dist(x,y,t.x,t.y)<r+9*t.s)return true;
  }
  for(const o of objects){
    if(o.type!=='building')continue;
    if(Math.abs(o.x-x)<o.w/2+r&&Math.abs(o.y-y)<o.h/2+r)return true;
  }
  return false;
}
function moveInteriorPlayer(dt){
  if(!state.room)return;
  const dx=(keys.d||keys.arrowright?1:0)-(keys.a||keys.arrowleft?1:0);
  const dy=(keys.s||keys.arrowdown?1:0)-(keys.w||keys.arrowup?1:0);
  const len=Math.hypot(dx,dy)||1;
  if(dx||dy){
    const nx=player.x+dx/len*player.speed*dt;
    const ny=player.y+dy/len*player.speed*dt;
    if(!insideBlocked(nx,player.y))player.x=nx;
    if(!insideBlocked(player.x,ny))player.y=ny;
    player.angle=Math.atan2(dy,dx);
    player.moving=true;
    player.step+=dt*8;
  }else player.moving=false;
  player.x=clamp(player.x,32,state.room.w-32);
  player.y=clamp(player.y,32,state.room.h-32);
}
function insideBlocked(x,y){
  if(!state.room)return false;
  if(x<27||y<27||x>state.room.w-27||y>state.room.h-27)return true;
  for(const p of state.room.props){
    if(x>p.x-p.w/2-15&&x<p.x+p.w/2+15&&y>p.y-p.h/2-15&&y<p.y+p.h/2+15)return true;
  }
  return false;
}
function updateSurvivors(dt){
  for(const s of survivors){
    if(!s.following||s.delivered)continue;
    const d=dist(player.x,player.y,s.x,s.y);
    if(state.floor==='outside'&&d>58){
      const a=angleTo(s.x,s.y,player.x,player.y);
      const speed=d>220?105:70;
      const nx=s.x+Math.cos(a)*speed*dt;
      const ny=s.y+Math.sin(a)*speed*dt;
      if(!blockedAt(nx,s.y,7))s.x=nx;
      if(!blockedAt(s.x,ny,7))s.y=ny;
    }
    if(state.floor==='outside'&&dist(s.x,s.y,2920,2300)<115){
      s.delivered=true;
      s.following=false;
      state.rescued++;
      sound('pickup');
      toast(s.name.toUpperCase()+' REACHED THE SAFE ZONE.',2.3);
      updateObjectives();
      updateHUD();
    }
  }
}
function updateCrawlers(dt){
  if(state.floor==='inside')return;
  for(const c of crawlers){
    if(c.dead)continue;
    c.phase+=dt;
    c.attack=Math.max(0,c.attack-dt);
    const d=dist(player.x,player.y,c.x,c.y);
    const range=state.floor==='inside'?0:270;
    if(d<range){
      c.alert=true;
      const a=angleTo(c.x,c.y,player.x,player.y);
      const speed=c.speed*(d<100?1.2:1);
      const nx=c.x+Math.cos(a)*speed*dt;
      const ny=c.y+Math.sin(a)*speed*dt;
      if(!blockedAt(nx,c.y,c.r))c.x=nx;
      if(!blockedAt(c.x,ny,c.r))c.y=ny;
      if(d<c.r+player.r+5&&c.attack<=0){
        c.attack=1.3;
        damagePlayer(9,'crawler');
      }
    }else if(Math.sin(c.phase*.7)>.94){
      c.x+=Math.cos(c.phase)*18*dt;
      c.y+=Math.sin(c.phase*.8)*18*dt;
    }
  }
}
function updateMonster(dt){
  if(!monster.active)return;
  monster.phase+=dt;
  monster.stun=Math.max(0,monster.stun-dt);
  monster.attack=Math.max(0,monster.attack-dt);
  monster.warpCooldown=Math.max(0,monster.warpCooldown-dt);
  const d=dist(player.x,player.y,monster.x,monster.y);
  if(d<390)monster.spotted=true;
  if(state.floor==='inside'){
    if(d<200&&monster.warpCooldown<=0){
      monster.warpCooldown=9;
      monster.x=clamp(player.x+choose([-1,1])*430,70,WORLD.w-70);
      monster.y=clamp(player.y+choose([-1,1])*350,70,WORLD.h-70);
      showRadioText('UNKNOWN TRANSMISSION','You can hear footsteps outside the building.');
      toast('SOMETHING MOVES OUTSIDE THE WALLS.',2.3);
    }
    return;
  }
  if(monster.stun>0)return;
  let speed=d<280?111:state.noise>.3?88:62;
  if(d>780&&state.noise<.2){
    monster.lastMove+=dt;
    if(monster.lastMove>7&&monster.warpCooldown<=0){
      const angle=angleTo(player.x,player.y,monster.x,monster.y);
      monster.x=clamp(player.x+Math.cos(angle)*620,80,WORLD.w-80);
      monster.y=clamp(player.y+Math.sin(angle)*620,80,WORLD.h-80);
      monster.lastMove=0;
      monster.warpCooldown=7;
    }
  }
  const a=angleTo(monster.x,monster.y,player.x,player.y);
  monster.x+=Math.cos(a)*speed*dt;
  monster.y+=Math.sin(a)*speed*dt;
  if(d<43&&monster.attack<=0){
    monster.attack=1.45;
    damagePlayer(21,'smiler');
    monster.x=clamp(monster.x-Math.cos(a)*44,30,WORLD.w-30);
    monster.y=clamp(monster.y-Math.sin(a)*44,30,WORLD.h-30);
  }
  if(d<160&&growlTimer<=0){
    sound('roar');
    growlTimer=7+Math.random()*7;
    if(Math.random()<.55)toast('YOU HEAR WET BREATHING OVER YOUR SHOULDER.',1.8);
  }
}
function updateBullets(dt){
  for(const b of bullets){
    b.x+=b.vx*dt;
    b.y+=b.vy*dt;
    b.life-=dt;
    if(b.owner!=='player')continue;
    for(const c of crawlers){
      if(c.dead)continue;
      if(dist(b.x,b.y,c.x,c.y)<c.r+4){
        c.hp--;
        b.life=0;
        spawnBlood(c.x,c.y);
        if(c.hp<=0){
          c.dead=true;
          state.kills++;
          state.noise=Math.max(state.noise,.7);
          toast('MARSH CRAWLER NEUTRALIZED.',1.2);
        }
        break;
      }
    }
    if(monster.active&&b.life>0&&dist(b.x,b.y,monster.x,monster.y)<monster.r+5){
      monster.stun=Math.max(monster.stun,1.4);
      b.life=0;
      spawnSparks(monster.x,monster.y);
      toast('THE SHAPE STAGGERS. IT DOES NOT FALL.',1.2);
    }
  }
  bullets=bullets.filter(b=>b.life>0);
  for(const p of particles){
    p.x+=p.vx*dt;
    p.y+=p.vy*dt;
    p.life-=dt;
    p.vx*=Math.pow(.07,dt);
    p.vy*=Math.pow(.07,dt);
  }
  particles=particles.filter(p=>p.life>0);
}
function spawnBlood(x,y){
  for(let i=0;i<7;i++)particles.push({x,y,vx:(Math.random()-.5)*160,vy:(Math.random()-.5)*160,life:.18+Math.random()*.4,color:choose(['#76302b','#a53b37','#47201d']),size:2+Math.random()*3});
}
function spawnSparks(x,y){
  for(let i=0;i<12;i++)particles.push({x,y,vx:(Math.random()-.5)*240,vy:(Math.random()-.5)*240,life:.12+Math.random()*.26,color:choose(['#d9c58e','#a2b28b','#efdfb2']),size:1+Math.random()*3});
}
function updateWeather(dt){
  state.lightningNext-=dt;
  if(state.lightningNext<=0){
    state.lightning=.15+Math.random()*.35;
    state.lightningNext=7+Math.random()*15;
    if(Math.random()<.5){
      setTimeout(()=>{state.lightning=Math.max(state.lightning,.08);},110);
    }
    if(Math.random()<.3)tone(40,.7,'triangle',.08,-8);
  }
  state.lightning=Math.max(0,state.lightning-dt*.7);
  state.damageFlash=Math.max(0,state.damageFlash-dt*1.8);
  $('damageFlash').style.opacity=state.damageFlash;
  state.screenShake=Math.max(0,state.screenShake-dt*.8);
  state.intensity=Math.max(0,state.intensity-dt*.035);
  for(const r of raindrops){
    r.y+=r.speed*dt;
    r.x-=r.speed*.16*dt;
    if(r.y>H+15){r.y=-15;r.x=Math.random()*W;}
    if(r.x<-15)r.x=W+10;
  }
  for(const f of fireflies)f.phase+=dt*f.speed;
}
function update(dt){
  state.elapsed+=dt;
  state.missionClock+=dt;
  growlTimer-=dt;
  shootTimer=Math.max(0,shootTimer-dt);
  reloadTimer=Math.max(0,reloadTimer-dt);
  interactCooldown=Math.max(0,interactCooldown-dt);
  damageCooldown=Math.max(0,damageCooldown-dt);
  if(reloadTimer===0&&reloadTimer!==-1&&ammo<6&&reserve>0&&state.reloadActive){
    const need=6-ammo;
    const take=Math.min(need,reserve);
    ammo+=take;
    reserve-=take;
    state.reloadActive=false;
    updateHUD();
    toast('MAGAZINE READY.',1.0);
  }
  if(reloadTimer===0&&ammo<6&&reserve>0&&!state.reloadActive)state.reloadActive=false;
  if(keys.r&&reloadTimer<=0&&!state.reloadActive){
    state.reloadActive=true;
    reloadWeapon();
    keys.r=false;
  }
  if(state.floor==='outside'){
    const onReed=trees.some(t=>Math.abs(t.x-player.x)<25&&Math.abs(t.y-player.y)<25);
    player.hidden=onReed&&!keys.shift&&state.noise<.2;
  }else player.hidden=false;
  movePlayer(dt);
  updateSurvivors(dt);
  updateCrawlers(dt);
  updateMonster(dt);
  updateBullets(dt);
  updateWeather(dt);
  if(flashlight&&flashlightBattery>0){
    flashlightBattery=Math.max(0,flashlightBattery-dt*(state.floor==='inside'?1.0:.34));
    if(flashlightBattery<=0){flashlight=false;toast('FLASHLIGHT BATTERY EXHAUSTED.',2);}
  }
  if(state.floor==='outside'){
    camera.x=clamp(player.x-W/2,0,WORLD.w-W);
    camera.y=clamp(player.y-H/2,0,WORLD.h-H);
  }else if(state.room){
    camera.x=clamp(player.x-W/2,0,Math.max(0,state.room.w-W));
    camera.y=clamp(player.y-H/2,0,Math.max(0,state.room.h-H));
  }
  if(state.toastTimer>0){
    state.toastTimer-=dt;
    if(state.toastTimer<=0)hideToast();
  }
  state.radioTimer=Math.max(0,state.radioTimer-dt);
  updateHUD();
  if(pointer.down&&state.controlMode==='desktop')shoot();
}
function screenJitter(){
  if(state.options.shake&&state.screenShake>0){
    shakeX=(Math.random()-.5)*state.screenShake*22;
    shakeY=(Math.random()-.5)*state.screenShake*22;
  }else{
    shakeX=0;
    shakeY=0;
  }
}
function px(x,y,w,h,color){
  ctx.fillStyle=color;
  ctx.fillRect(Math.round(x),Math.round(y),Math.max(1,Math.round(w)),Math.max(1,Math.round(h)));
}
function worldPx(x,y,w,h,color){
  px(x-camera.x+shakeX,y-camera.y+shakeY,w,h,color);
}
function drawGround(){
  px(0,0,W,H,'#101a13');
  const startX=Math.floor(camera.x/TILE)*TILE;
  const startY=Math.floor(camera.y/TILE)*TILE;
  for(let wy=startY;wy<camera.y+H+TILE;wy+=TILE){
    for(let wx=startX;wx<camera.x+W+TILE;wx+=TILE){
      const x=wx-camera.x+shakeX;
      const y=wy-camera.y+shakeY;
      const n=seeded(Math.floor(wx/TILE),Math.floor(wy/TILE));
      const color=n>.79?'#1b291b':n>.57?'#162319':n>.3?'#122018':'#101b14';
      px(x,y,TILE,TILE,color);
      if(n>.91){
        px(x+5,y+7,9,2,'#35412c');
        px(x+9,y+11,4,2,'#28382a');
      }
      if(n<.06){
        px(x+13,y+20,8,4,'#27352a');
        px(x+16,y+21,3,1,'#536151');
      }
      if(n>.48&&n<.52)px(x+23,y+6,2,7,'#202f22');
    }
  }
}
function drawRoad(){
  const p=roadPoints();
  ctx.save();
  ctx.beginPath();
  ctx.moveTo(p[0].x-camera.x+shakeX,p[0].y-camera.y+shakeY);
  for(let i=1;i<p.length;i++)ctx.lineTo(p[i].x-camera.x+shakeX,p[i].y-camera.y+shakeY);
  ctx.lineCap='square';
  ctx.lineJoin='round';
  ctx.lineWidth=98;
  ctx.strokeStyle='#090e0b';
  ctx.stroke();
  ctx.lineWidth=88;
  ctx.strokeStyle='#35372d';
  ctx.stroke();
  ctx.lineWidth=75;
  ctx.strokeStyle='#414235';
  ctx.stroke();
  ctx.lineWidth=2;
  ctx.strokeStyle='#817a60';
  ctx.setLineDash([19,24]);
  ctx.stroke();
  ctx.setLineDash([]);
  ctx.restore();
  for(let i=0;i<15;i++){
    const wx=225+i*170;
    const wy=190+i*142;
    if(roadDistance(wx,wy)<50){
      const x=wx-camera.x;
      const y=wy-camera.y;
      if(x>-30&&x<W+30&&y>-30&&y<H+30){
        px(x,y,18,3,'#292f26');
        px(x+5,y+1,5,1,'#77745e');
      }
    }
  }
}
function drawTree(t){
  const x=t.x-camera.x+shakeX;
  const y=t.y-camera.y+shakeY;
  const s=t.s;
  if(x<-85||y<-100||x>W+85||y>H+100)return;
  const palette=[
    ['#0a110c','#17271b','#263928','#39462e'],
    ['#0b130d','#1d2b1e','#2b3a29','#424b32'],
    ['#0e140e','#202b20','#30382a','#4a4b34']
  ][t.shade];
  const wind=Math.sin(state.elapsed*.75+t.phase)*1.7;
  px(x-13*s,y-4*s,26*s,12*s,'#080e0a');
  px(x-4*s,y-1*s,8*s,18*s,'#29281e');
  px(x-14*s+wind,y-20*s,28*s,20*s,palette[0]);
  px(x-12*s+wind,y-31*s,24*s,18*s,palette[1]);
  px(x-8*s+wind,y-41*s,16*s,15*s,palette[2]);
  px(x-4*s+wind,y-46*s,8*s,9*s,palette[3]);
  px(x-20*s+wind,y-13*s,10*s,12*s,palette[0]);
  px(x+10*s+wind,y-15*s,10*s,13*s,palette[0]);
  px(x-8*s+wind,y-28*s,5*s,4*s,'#405037');
  if(t.s>.95){
    px(x-2*s,y-37*s,3*s,2*s,'#566041');
    px(x+5*s,y-18*s,2*s,4*s,'#48523a');
  }
}
function drawReeds(){
  for(const r of reeds){
    const x=r.x-camera.x;
    const y=r.y-camera.y;
    if(x<-20||y<-25||x>W+20||y>H+20)continue;
    const swing=Math.sin(state.elapsed*2+r.phase)*2;
    px(x,y-r.h,2,r.h,'#263a28');
    px(x+swing-2,y-r.h+3,3,5,'#45523a');
    px(x+4,y-r.h*.7,2,r.h*.7,'#31442d');
  }
}
function drawPuddles(){
  for(const p of wetPatches){
    const x=p.x-camera.x;
    const y=p.y-camera.y;
    if(x<-80||y<-30||x>W+80||y>H+30)continue;
    px(x,y,p.w,p.h,'#0d1b18');
    px(x+3,y+2,p.w*.47,2,'#314c42');
    px(x+p.w*.63,y+p.h-3,p.w*.2,1,'#263e35');
  }
}
function drawBuilding(o){
  const x=o.x-camera.x+shakeX;
  const y=o.y-camera.y+shakeY;
  const w=o.w;
  const h=o.h;
  if(x<-w-50||y<-h-75||x>W+w+50||y>H+h+75)return;
  px(x-w/2-7,y-h/2+8,w+14,h+17,'#080e0a');
  px(x-w/2,y-h/2,w,h,'#494737');
  px(x-w/2+5,y-h/2+5,w-10,h-10,'#34382c');
  px(x-w/2-4,y-h/2-8,w+8,11,'#25291f');
  px(x-w/2-2,y-h/2-10,w+4,5,'#774336');
  px(x-w/2+5,y-h/2+11,w-10,3,'#595540');
  px(x-w/2+10,y-h/2+18,24,18,'#151d17');
  px(x-w/2+13,y-h/2+21,18,12,'#807c5c');
  px(x+w/2-35,y-h/2+18,24,18,'#131b15');
  px(x+w/2-32,y-h/2+21,18,12,'#736e52');
  px(x-12,y-h/2+h*.49,24,h*.38,'#0c100c');
  px(x-8,y-h/2+h*.49+5,16,h*.36,'#1c2119');
  px(x+4,y-h/2+h*.49+20,2,3,'#c2a46a');
  px(x-w/2-2,y+h/2-7,w+4,8,'#171d16');
  ctx.fillStyle='#d4c9a1';
  ctx.textAlign='center';
  ctx.font='9px monospace';
  ctx.fillText(o.name.toUpperCase(),x,y-h/2-17);
  if(Math.sin(state.elapsed*1.8+o.x)>-.3){
    px(x-w*.28,y-h/2+24,5,3,'#d4b979');
  }
}
function drawEvidence(o){
  const x=o.x-camera.x+shakeX;
  const y=o.y-camera.y+shakeY;
  if(x<-20||y<-20||x>W+20||y>H+20)return;
  if(o.found){
    px(x-5,y-4,10,8,'#313b2e');
    return;
  }
  const pulse=.5+.5*Math.sin(state.elapsed*4+o.x);
  ctx.fillStyle='rgba(212,185,108,'+(.08+pulse*.12)+')';
  ctx.beginPath();
  ctx.arc(x,y,16+pulse*9,0,Math.PI*2);
  ctx.fill();
  px(x-8,y-8,16,16,'#5a4c2d');
  px(x-5,y-5,10,10,pulse>.5?'#e2ca86':'#a48c56');
  px(x-2,y-2,4,4,'#f6edc2');
  px(x-12,y-1,3,2,'#c9aa68');
}
function drawLoot(o){
  if(o.found)return;
  const x=o.x-camera.x;
  const y=o.y-camera.y;
  if(x<-20||y<-20||x>W+20||y>H+20)return;
  const pulse=Math.sin(state.elapsed*3+o.y)>0;
  px(x-8,y-6,16,12,'#354134');
  px(x-6,y-7,12,2,'#7e815a');
  px(x-5,y-4,10,7,'#b09b67');
  px(x-3,y-2,6,3,pulse?'#e8d49b':'#7e764f');
}
function drawExit(o){
  const x=o.x-camera.x;
  const y=o.y-camera.y;
  px(x-32,y-18,64,36,'#858776');
  px(x-25,y-11,50,16,'#28362d');
  px(x-24,y+9,12,5,'#a72d30');
  px(x+12,y+9,12,5,'#a72d30');
  px(x-19,y-8,13,8,'#6e8172');
  px(x+6,y-8,13,8,'#6e8172');
  px(x-7,y-24,14,7,'#cfc7a5');
  ctx.fillStyle='#efdda8';
  ctx.font='10px monospace';
  ctx.textAlign='center';
  ctx.fillText('EXTRACTION',x,y-33);
  if(!state.keysFound||evidence<5||survivors.filter(s=>s.delivered).length<2){
    px(x-18,y+20,36,3,'#a34740');
  }
}
function drawSurvivors(){
  for(const s of survivors){
    if(s.delivered)continue;
    const x=s.x-camera.x;
    const y=s.y-camera.y;
    if(x<-30||y<-30||x>W+30||y>H+30)continue;
    px(x-7,y-7,14,15,'#242a25');
    px(x-5,y-12,10,8,'#8a7560');
    px(x-5,y-2,10,8,s.following?'#65785a':'#726c56');
    px(x-5,y+6,4,6,'#272b25');
    px(x+1,y+6,4,6,'#272b25');
    if(!s.found){
      ctx.strokeStyle='rgba(173,206,148,.45)';
      ctx.strokeRect(x-12,y-17,24,32);
    }
    if(s.following){
      ctx.fillStyle='#a8c88e';
      ctx.font='9px monospace';
      ctx.textAlign='center';
      ctx.fillText('FOLLOWING',x,y-20);
    }
  }
}
function drawCrawler(c){
  if(c.dead)return;
  const x=c.x-camera.x+shakeX;
  const y=c.y-camera.y+shakeY;
  if(x<-45||y<-45||x>W+45||y>H+45)return;
  const step=Math.sin(c.phase*8)*3;
  px(x-9,y-5,18,11,'#10120f');
  px(x-7,y-8+step,14,7,'#26271e');
  px(x-4,y-10+step,8,5,'#37382a');
  px(x-11,y-2,5,4,'#10120f');
  px(x+6,y-2,5,4,'#10120f');
  px(x-7,y+3,4,5,'#0d100d');
  px(x+4,y+3,4,5,'#0d100d');
  px(x-3,y-7+step,2,2,'#d54d40');
  px(x+2,y-7+step,2,2,'#d54d40');
  if(c.alert){
    ctx.fillStyle='rgba(188,56,51,.25)';
    ctx.beginPath();
    ctx.arc(x,y,19,0,Math.PI*2);
    ctx.fill();
  }
}
function drawMonster(){
  if(!monster.active)return;
  const x=monster.x-camera.x+shakeX;
  const y=monster.y-camera.y+shakeY;
  if(x<-110||y<-110||x>W+110||y>H+110)return;
  const bob=Math.sin(monster.phase*4.5)*3;
  const stretched=monster.stun>0?0:Math.sin(monster.phase*7)*1.5;
  px(x-13,y-23+bob,26,44,'#060807');
  px(x-10,y-41+bob,20,23,'#050706');
  px(x-7,y-46+bob,14,9,'#080a08');
  px(x-16,y-17+bob,6,29,'#070907');
  px(x+10,y-18+bob,6,30,'#070907');
  px(x-15,y+11,7,23,'#050706');
  px(x+7,y+11,7,23,'#050706');
  px(x-9,y-37+bob,18,5,'#0c0e0b');
  px(x-6,y-34+bob,3,2,'#d33a35');
  px(x+3,y-34+bob,3,2,'#d33a35');
  px(x-7,y-18+bob,14,2,'#1b1a16');
  px(x-19,y-10+bob,5,18,'#0a0b09');
  px(x+14,y-10+bob,5,18,'#0a0b09');
  if(monster.stun>0){
    px(x-19,y-52,38,2,'#dfc789');
    px(x-11,y-50,22,2,'#9e8a56');
  }
  if(dist(player.x,player.y,monster.x,monster.y)<240){
    ctx.strokeStyle='rgba(174,38,35,.12)';
    ctx.beginPath();
    ctx.arc(x,y,26+stretched,0,Math.PI*2);
    ctx.stroke();
  }
}
function drawPlayer(){
  const x=player.x-camera.x+shakeX;
  const y=player.y-camera.y+shakeY;
  const spec=specs[state.selectedCharacter];
  const leg=player.moving?Math.sin(player.step)*3:0;
  ctx.save();
  ctx.translate(Math.round(x),Math.round(y));
  ctx.rotate(player.angle);
  if(player.invulnerable>0&&Math.floor(state.elapsed*24)%2===0)ctx.globalAlpha=.5;
  px(-9,-8,18,17,'#080d0a');
  px(-7,-7,14,14,spec.color);
  px(-11,-6,5,11,spec.color);
  px(6,-6,5,11,spec.color);
  px(-7,-13,14,6,'#20261d');
  px(-6,-15,12,5,spec.shirt);
  px(-5,-16,10,3,'#c1b180');
  px(-7,7+leg,5,7,'#2b2c24');
  px(2,7-leg,5,7,'#2b2c24');
  px(2,-3,17,4,'#0b0e0b');
  px(15,-4,5,3,'#c9c5ac');
  px(-3,-2,4,3,'#e4d0a0');
  if(state.selectedCharacter==='morgan'){
    px(-2,-9,5,5,'#6c7162');
  }
  if(state.selectedCharacter==='blake'){
    px(-4,-13,8,2,'#d2b56e');
  }
  ctx.restore();
}
function drawFireflies(){
  for(const f of fireflies){
    const x=f.x-camera.x+Math.sin(f.phase)*12;
    const y=f.y-camera.y+Math.cos(f.phase*.7)*9;
    if(x<0||y<0||x>W||y>H)continue;
    const alpha=.2+.45*(.5+.5*Math.sin(f.phase*2));
    ctx.fillStyle='rgba(182,202,119,'+alpha+')';
    ctx.fillRect(x,y,2,2);
    if(alpha>.45){
      ctx.fillStyle='rgba(151,177,104,.09)';
      ctx.fillRect(x-4,y-4,10,10);
    }
  }
}
function drawBulletEffects(){
  for(const b of bullets){
    const x=b.x-camera.x;
    const y=b.y-camera.y;
    px(x-2,y-2,5,5,'#f7daa0');
    px(x-1,y-1,2,2,'#fff7d9');
  }
  for(const p of particles){
    const x=p.x-camera.x;
    const y=p.y-camera.y;
    ctx.globalAlpha=clamp(p.life/.4,0,1);
    px(x,y,p.size||2,p.size||2,p.color||'#e4c78b');
    ctx.globalAlpha=1;
  }
}
function drawRain(){
  ctx.strokeStyle='rgba(154,179,173,.27)';
  ctx.lineWidth=1;
  ctx.beginPath();
  for(const r of raindrops){
    ctx.moveTo(r.x,r.y);
    ctx.lineTo(r.x-4,r.y+r.length);
  }
  ctx.stroke();
  ctx.fillStyle='rgba(141,164,156,.035)';
  ctx.fillRect(0,0,W,H);
}
function drawLighting(){
  const x=player.x-camera.x+shakeX;
  const y=player.y-camera.y+shakeY;
  ctx.save();
  ctx.fillStyle=flashlight&&flashlightBattery>0?'rgba(0,4,4,.79)':'rgba(0,0,0,.66)';
  ctx.fillRect(0,0,W,H);
  ctx.globalCompositeOperation='destination-out';
  const haloRadius=flashlight&&flashlightBattery>0?102:38;
  const halo=ctx.createRadialGradient(x,y,5,x,y,haloRadius);
  halo.addColorStop(0,'rgba(0,0,0,1)');
  halo.addColorStop(.65,'rgba(0,0,0,.75)');
  halo.addColorStop(1,'rgba(0,0,0,0)');
  ctx.fillStyle=halo;
  ctx.beginPath();
  ctx.arc(x,y,haloRadius,0,Math.PI*2);
  ctx.fill();
  if(flashlight&&flashlightBattery>0){
    const target=worldCoordinates(pointer.x,pointer.y);
    const a=angleTo(player.x,player.y,target.x,target.y);
    const beam=ctx.createRadialGradient(x,y,13,x,y,365);
    beam.addColorStop(0,'rgba(0,0,0,.98)');
    beam.addColorStop(.62,'rgba(0,0,0,.76)');
    beam.addColorStop(1,'rgba(0,0,0,0)');
    ctx.fillStyle=beam;
    ctx.beginPath();
    ctx.moveTo(x,y);
    ctx.arc(x,y,365,a-.34,a+.34);
    ctx.closePath();
    ctx.fill();
  }
  ctx.restore();
  if(state.lightning>0){
    ctx.fillStyle='rgba(191,211,204,'+state.lightning*.36+')';
    ctx.fillRect(0,0,W,H);
  }
  const vignette=ctx.createRadialGradient(W/2,H/2,Math.min(W,H)*.13,W/2,H/2,Math.max(W,H)*.76);
  vignette.addColorStop(0,'rgba(0,0,0,0)');
  vignette.addColorStop(.65,'rgba(0,0,0,.17)');
  vignette.addColorStop(1,'rgba(0,0,0,.81)');
  ctx.fillStyle=vignette;
  ctx.fillRect(0,0,W,H);
}
function drawWorld(){
  screenJitter();
  if(state.floor==='inside'){
    drawInterior();
    drawSurvivors();
    drawPlayer();
    drawBulletEffects();
    drawLightingInterior();
    drawMini();
    return;
  }
  drawGround();
  drawPuddles();
  drawRoad();
  drawReeds();
  for(const t of trees)drawTree(t);
  for(const o of objects){
    if(o.type==='building')drawBuilding(o);
    if(o.type==='evidence')drawEvidence(o);
    if(o.type==='loot')drawLoot(o);
    if(o.type==='exit')drawExit(o);
  }
  drawSurvivors();
  for(const c of crawlers)drawCrawler(c);
  drawMonster();
  drawPlayer();
  drawBulletEffects();
  drawFireflies();
  drawLighting();
  drawRain();
  drawMini();
}
function drawInterior(){
  if(!state.room)return;
  const room=state.room;
  px(0,0,W,H,'#131811');
  const sx=-camera.x+shakeX;
  const sy=-camera.y+shakeY;
  px(sx,sy,room.w,room.h,room.color);
  for(let y=0;y<room.h;y+=32){
    for(let x=0;x<room.w;x+=32){
      const n=seeded(x,y);
      px(x+sx,y+sy,32,32,n>.5?'#4a4634':'#454131');
      px(x+sx+2,y+sy+2,28,28,n>.5?'#3f3e2f':'#393a2c');
      if(n>.82)px(x+sx+5,y+sy+12,18,2,'#55513b');
    }
  }
  px(sx,sy,room.w,24,'#171d15');
  px(sx,sy,24,room.h,'#171d15');
  px(sx+room.w-24,sy,24,room.h,'#171d15');
  px(sx,sy+room.h-24,room.w,24,'#171d15');
  for(const p of room.props)drawFurniture(p,sx,sy);
  for(const item of room.items){
    if(item.found)continue;
    const x=item.x+sx;
    const y=item.y+sy;
    const pulse=Math.sin(state.elapsed*4)>0;
    if(item.type==='note'){
      px(x-8,y-6,16,12,'#a59a70');
      px(x-5,y-3,10,2,'#514c38');
      px(x-5,y,8,2,'#6c6143');
      if(pulse)px(x-10,y-8,20,2,'#d1b96f');
    }else{
      px(x-8,y-5,16,10,'#7f7959');
      px(x-4,y-2,8,4,'#c9b57a');
    }
  }
  const ex=room.exit.x+sx;
  const ey=room.exit.y+sy;
  px(ex-35,ey-20,70,18,'#171c14');
  px(ex-24,ey-13,48,12,'#5e5942');
  ctx.fillStyle='#d4c38e';
  ctx.font='10px monospace';
  ctx.textAlign='center';
  ctx.fillText('EXIT',ex,ey-25);
  for(let i=0;i<10;i++){
    const x=(i*89+35+state.elapsed*5)%room.w+sx;
    const y=(i*41+70)%room.h+sy;
    px(x,y,1,1,'#9e966b');
  }
  const textY=27;
  px(32,sy+32,room.w-64,1,'#6a6248');
  ctx.fillStyle='#d4c69d';
  ctx.textAlign='center';
  ctx.font='11px monospace';
  ctx.fillText(room.title,W/2,30);
  drawRainAtWindows(sx,sy,room);
}
function drawFurniture(p,sx,sy){
  const x=p.x+sx;
  const y=p.y+sy;
  if(p.t==='desk'){
    px(x-p.w/2,y-p.h/2+5,p.w,p.h,'#241f18');
    px(x-p.w/2+3,y-p.h/2,p.w-6,p.h-8,'#6c5337');
    px(x-p.w/2+8,y-p.h/2+5,p.w-16,p.h-18,'#886745');
    px(x-p.w/2+10,y+p.h/2-3,9,14,'#3c3021');
    px(x+p.w/2-19,y+p.h/2-3,9,14,'#3c3021');
    px(x-12,y-5,22,13,'#aaa58a');
    px(x-10,y-3,18,2,'#4c4b3b');
  }
  if(p.t==='cabinet'){
    px(x-p.w/2,y-p.h/2,p.w,p.h,'#25281e');
    px(x-p.w/2+4,y-p.h/2+4,p.w-8,p.h-8,'#63543a');
    px(x-2,y-p.h/2+6,3,p.h-12,'#2a2e22');
    px(x-p.w/2+9,y,3,5,'#c6b279');
    px(x+5,y,3,5,'#c6b279');
  }
  if(p.t==='shelves'){
    px(x-p.w/2,y-p.h/2,p.w,p.h,'#33291e');
    for(let yy=y-p.h/2+10;yy<y+p.h/2-5;yy+=25){
      px(x-p.w/2+3,yy,p.w-6,4,'#90704b');
      for(let xx=x-p.w/2+7;xx<x+p.w/2-9;xx+=19){
        px(xx,yy-9,9,9,choose(['#3d4e38','#595540','#4f3430','#5c5c45']));
      }
    }
  }
  if(p.t==='bed'){
    px(x-p.w/2,y-p.h/2,p.w,p.h,'#27251e');
    px(x-p.w/2+5,y-p.h/2+5,p.w-10,p.h-10,'#766c52');
    px(x-p.w/2+9,y-p.h/2+8,p.w-18,p.h-16,'#494d3a');
    px(x-p.w/2+9,y-p.h/2+8,p.w-18,14,'#a39a7e');
  }
  if(p.t==='table'){
    px(x-p.w/2,y-p.h/2,p.w,p.h,'#25251c');
    px(x-p.w/2+3,y-p.h/2+3,p.w-6,p.h-7,'#7b6140');
    px(x-p.w/2+7,y+p.h/2-1,7,15,'#332a1e');
    px(x+p.w/2-14,y+p.h/2-1,7,15,'#332a1e');
  }
  if(p.t==='console'){
    px(x-p.w/2,y-p.h/2,p.w,p.h,'#1b241e');
    px(x-p.w/2+6,y-p.h/2+6,p.w-12,p.h-12,'#35443a');
    for(let i=0;i<8;i++)px(x-p.w/2+12+i*21,y-p.h/2+17,7,6,choose(['#b4423c','#a8b079','#647d9c']));
    px(x-p.w/2+10,y+12,p.w-20,4,'#0d110e');
  }
}
function drawRainAtWindows(sx,sy,room){
  const windows=[{x:room.w*.22,y:28,w:34,h:8},{x:room.w*.76,y:28,w:34,h:8}];
  for(const w of windows){
    px(w.x+sx,w.y+sy,w.w,w.h,'#141d19');
    px(w.x+sx+3,w.y+sy+2,w.w-6,w.h-4,'#4d6b61');
    if(Math.sin(state.elapsed*2)>0)px(w.x+sx+5,w.y+sy+2,2,w.h-4,'#a3b9a6');
  }
}
function drawLightingInterior(){
  const x=player.x-camera.x+shakeX;
  const y=player.y-camera.y+shakeY;
  ctx.save();
  ctx.fillStyle=flashlight&&flashlightBattery>0?'rgba(0,4,4,.72)':'rgba(0,0,0,.74)';
  ctx.fillRect(0,0,W,H);
  ctx.globalCompositeOperation='destination-out';
  const rad=flashlight&&flashlightBattery>0?150:42;
  const g=ctx.createRadialGradient(x,y,4,x,y,rad);
  g.addColorStop(0,'rgba(0,0,0,.99)');
  g.addColorStop(.62,'rgba(0,0,0,.73)');
  g.addColorStop(1,'rgba(0,0,0,0)');
  ctx.fillStyle=g;
  ctx.beginPath();
  ctx.arc(x,y,rad,0,Math.PI*2);
  ctx.fill();
  ctx.restore();
  const vignette=ctx.createRadialGradient(W/2,H/2,50,W/2,H/2,Math.max(W,H)*.75);
  vignette.addColorStop(0,'rgba(0,0,0,0)');
  vignette.addColorStop(1,'rgba(0,0,0,.72)');
  ctx.fillStyle=vignette;
  ctx.fillRect(0,0,W,H);
}
function drawMini(){
  const mw=mini.width;
  const mh=mini.height;
  mctx.fillStyle='#07100a';
  mctx.fillRect(0,0,mw,mh);
  if(state.floor==='inside'&&state.room){
    mctx.fillStyle='#33382b';
    mctx.fillRect(5,5,mw-10,mh-10);
    mctx.strokeStyle='#827d60';
    mctx.strokeRect(5,5,mw-10,mh-10);
    mctx.fillStyle='#e8dfbb';
    mctx.fillRect(mw/2-2,mh/2-2,5,5);
    return;
  }
  mctx.fillStyle='#152319';
  mctx.fillRect(2,2,mw-4,mh-4);
  mctx.strokeStyle='#5e604d';
  mctx.lineWidth=4;
  mctx.beginPath();
  const points=roadPoints();
  mctx.moveTo(points[0].x/WORLD.w*mw,points[0].y/WORLD.h*mh);
  for(let i=1;i<points.length;i++)mctx.lineTo(points[i].x/WORLD.w*mw,points[i].y/WORLD.h*mh);
  mctx.stroke();
  for(const o of objects){
    const x=o.x/WORLD.w*mw;
    const y=o.y/WORLD.h*mh;
    let color='#77826d';
    if(o.type==='evidence'&&!o.found)color='#e1be65';
    if(o.type==='loot'&&!o.found)color='#93c68c';
    if(o.type==='exit')color='#d5d0ad';
    mctx.fillStyle=color;
    mctx.fillRect(x-2,y-2,4,4);
  }
  for(const s of survivors){
    if(s.delivered)continue;
    mctx.fillStyle=s.following?'#9ac58a':'#6d9b83';
    mctx.fillRect(s.x/WORLD.w*mw-2,s.y/WORLD.h*mh-2,4,4);
  }
  mctx.fillStyle='#fff0bc';
  mctx.fillRect(player.x/WORLD.w*mw-2,player.y/WORLD.h*mh-2,5,5);
  if(monster&&monster.active){
    mctx.fillStyle='#e4413d';
    mctx.fillRect(monster.x/WORLD.w*mw-2,monster.y/WORLD.h*mh-2,5,5);
  }
  for(const c of crawlers){
    if(c.dead)continue;
    if(dist(player.x,player.y,c.x,c.y)<460){
      mctx.fillStyle='#bf4d47';
      mctx.fillRect(c.x/WORLD.w*mw-1,c.y/WORLD.h*mh-1,3,3);
    }
  }
}
function drawMenuArt(){
  const c=$('artCanvas');
  if(!c)return;
  const g=c.getContext('2d');
  const cw=c.width;
  const ch=c.height;
  g.clearRect(0,0,cw,ch);
  g.fillStyle='#070e0a';
  g.fillRect(0,0,cw,ch);
  for(let y=0;y<ch;y+=10){
    g.fillStyle=y<160?'#0b1810':y<260?'#112016':'#17221a';
    g.fillRect(0,y,cw,10);
  }
  for(let i=0;i<24;i++){
    const x=(i*67)%cw;
    const h=70+(i*31)%170;
    g.fillStyle=i%3===0?'#1b2d20':'#14251a';
    g.fillRect(x,180-h*.4,9,h);
    g.fillRect(x-16,210-h*.23,42,10);
    g.fillRect(x-10,170-h*.2,31,12);
  }
  g.fillStyle='#080d09';
  g.beginPath();
  g.moveTo(0,290);
  g.lineTo(93,230);
  g.lineTo(230,248);
  g.lineTo(320,292);
  g.lineTo(320,390);
  g.lineTo(0,390);
  g.fill();
  g.fillStyle='#34372d';
  g.beginPath();
  g.moveTo(72,390);
  g.lineTo(130,260);
  g.lineTo(191,260);
  g.lineTo(278,390);
  g.fill();
  g.strokeStyle='#817760';
  g.lineWidth=3;
  g.setLineDash([13,16]);
  g.beginPath();
  g.moveTo(175,390);
  g.lineTo(160,276);
  g.stroke();
  g.setLineDash([]);
  g.fillStyle='#050706';
  g.fillRect(197,180,27,87);
  g.fillRect(201,152,20,33);
  g.fillRect(194,200,6,34);
  g.fillRect(221,200,6,34);
  g.fillStyle='#b83d3c';
  g.fillRect(205,164,3,2);
  g.fillRect(215,164,3,2);
  g.fillStyle='#4f422e';
  g.fillRect(192,187,35,4);
  for(let i=0;i<38;i++){
    const x=(i*71)%cw;
    const y=(i*47)%ch;
    g.fillStyle=i%4===0?'#d6d0a6':'#7d9666';
    g.fillRect(x,y,1,1);
  }
  const fog=g.createLinearGradient(0,210,0,ch);
  fog.addColorStop(0,'rgba(9,16,10,0)');
  fog.addColorStop(1,'rgba(6,10,7,.94)');
  g.fillStyle=fog;
  g.fillRect(0,210,cw,ch-210);
}
function drawPortraits(){
  const ids=['charArt0','charArt1','charArt2'];
  const keys=['reyes','morgan','blake'];
  ids.forEach((id,index)=>{
    const c=$(id);
    const g=c.getContext('2d');
    const spec=specs[keys[index]];
    g.clearRect(0,0,64,64);
    g.fillStyle='#0a120c';
    g.fillRect(0,0,64,64);
    g.fillStyle='#1b2d20';
    g.fillRect(5,4,54,56);
    g.fillStyle=spec.color;
    g.fillRect(18,31,28,25);
    g.fillStyle=spec.shirt;
    g.fillRect(17,21,30,16);
    g.fillStyle='#d0c18e';
    g.fillRect(16,18,32,7);
    g.fillStyle='#171b15';
    g.fillRect(21,29,6,5);
    g.fillRect(37,29,6,5);
    g.fillStyle='#b8b9a5';
    g.fillRect(26,36,12,3);
    g.fillStyle='#171b15';
    g.fillRect(25,42,14,7);
    g.fillStyle='#d2b975';
    g.fillRect(12,36,5,10);
    g.fillRect(47,36,5,10);
    if(index===1){
      g.fillStyle='#626e58';
      g.fillRect(22,14,20,6);
      g.fillRect(20,19,24,4);
    }
    if(index===2){
      g.fillStyle='#d4bb76';
      g.fillRect(21,20,22,3);
      g.fillStyle='#6b7858';
      g.fillRect(17,25,30,4);
    }
  });
}
function bindEvents(){
  $('start').addEventListener('click',()=>{audioStart();resetGame();});
  $('characterBtn').addEventListener('click',()=>{
    state.pendingCharacter=state.selectedCharacter;
    setScreen('character');
    updateCharacterSelection();
  });
  $('controlsBtn').addEventListener('click',()=>{
    state.pendingMode=state.controlMode;
    applyControlMode();
    setScreen('controls');
  });
  $('howBtn').addEventListener('click',()=>setScreen('how'));
  $('creditsBtn').addEventListener('click',()=>setScreen('credits'));
  $('backCharacter').addEventListener('click',()=>setScreen('menu'));
  $('confirmCharacter').addEventListener('click',()=>{
    state.selectedCharacter=state.pendingCharacter;
    setScreen('menu');
    toast('PERSONNEL FILE UPDATED: '+specs[state.selectedCharacter].name.toUpperCase(),1.6);
  });
  for(const btn of document.querySelectorAll('[data-char]')){
    btn.addEventListener('click',()=>{
      state.pendingCharacter=btn.dataset.char;
      updateCharacterSelection();
      tone(420,.07,'sine',.06,70);
    });
  }
  $('desktopMode').addEventListener('click',()=>{state.pendingMode='desktop';applyControlMode();});
  $('mobileMode').addEventListener('click',()=>{state.pendingMode='mobile';applyControlMode();});
  $('saveControls').addEventListener('click',()=>{
    state.controlMode=state.pendingMode;
    applyControlMode();
    setScreen('menu');
    toast('CONTROL MODE SAVED: '+state.controlMode.toUpperCase(),1.7);
  });
  $('backControls').addEventListener('click',()=>setScreen('menu'));
  $('backHow').addEventListener('click',()=>setScreen('menu'));
  $('backCredits').addEventListener('click',()=>setScreen('menu'));
  $('objectiveToggle').addEventListener('click',openObjectives);
  $('closeObjectives').addEventListener('click',closeOverlay);
  $('closeInventory').addEventListener('click',closeOverlay);
  $('useMed').addEventListener('click',useMedkit);
  $('resume').addEventListener('click',closeOverlay);
  $('pauseObjectives').addEventListener('click',()=>{
    updateObjectives();
    setScreen('objectives');
  });
  $('pauseMenu').addEventListener('click',()=>{
    state.gameOver=true;
    state.running=false;
    $('hud').style.display='none';
    document.body.classList.remove('game-active');
    setScreen('menu');
  });
  $('again').addEventListener('click',()=>{audioStart();resetGame();});
  $('toMenu').addEventListener('click',()=>{
    $('hud').style.display='none';
    document.body.classList.remove('game-active');
    setScreen('menu');
  });
  $('closeRadio').addEventListener('click',closeOverlay);
  $('touchInteract').addEventListener('pointerdown',e=>{e.preventDefault();interact();});
  $('touchShoot').addEventListener('pointerdown',e=>{e.preventDefault();shoot();});
  $('touchLight').addEventListener('pointerdown',e=>{e.preventDefault();toggleFlashlight();});
  $('touchReload').addEventListener('pointerdown',e=>{e.preventDefault();reloadWeapon();});
  $('touchRun').addEventListener('pointerdown',e=>{e.preventDefault();touchRun=true;});
  for(const eventName of ['pointerup','pointercancel','pointerleave'])$('touchRun').addEventListener(eventName,()=>touchRun=false);
  $('touchBag').addEventListener('pointerdown',e=>{e.preventDefault();openInventory();});
  const directionIds={up:'w',down:'s',left:'a',right:'d'};
  for(const [id,key] of Object.entries(directionIds)){
    const btn=$(id);
    btn.addEventListener('pointerdown',e=>{e.preventDefault();keys[key]=true;btn.setPointerCapture(e.pointerId);});
    for(const eventName of ['pointerup','pointercancel','pointerleave'])btn.addEventListener(eventName,()=>keys[key]=false);
  }
  canvas.addEventListener('pointermove',e=>{
    const rect=canvas.getBoundingClientRect();
    pointer.x=e.clientX-rect.left;
    pointer.y=e.clientY-rect.top;
  });
  canvas.addEventListener('pointerdown',e=>{
    if(state.controlMode==='desktop'&&e.button===0){
      pointer.down=true;
      shoot();
    }
  });
  window.addEventListener('pointerup',()=>pointer.down=false);
  canvas.addEventListener('contextmenu',e=>e.preventDefault());
  window.addEventListener('keydown',onKeyDown);
  window.addEventListener('keyup',onKeyUp);
  window.addEventListener('blur',()=>{
    keys={};
    pointer.down=false;
    touchRun=false;
    if(state.running)pauseGame();
  });
  document.addEventListener('visibilitychange',()=>{
    if(document.hidden&&state.running)pauseGame();
  });
}
function updateCharacterSelection(){
  for(const btn of document.querySelectorAll('[data-char]'))btn.classList.toggle('selected',btn.dataset.char===state.pendingCharacter);
  const spec=specs[state.pendingCharacter];
  const messages={
    reyes:'Experienced patrol officer. Balanced speed, stamina, and health.',
    morgan:'A seasoned deputy who can take more damage and carries extra rounds.',
    blake:'A fast-moving trooper who can sprint longer, but has less starting health.'
  };
  $('characterDetails').innerHTML='<b>'+escapeHTML(spec.name.toUpperCase())+'</b><br>'+escapeHTML(messages[state.pendingCharacter])+'<br><br>Speed: '+spec.speed+' · Max health: '+spec.hp+' · Starting ammo: '+spec.ammo+' + '+spec.reserve+' spare';
}
function toggleFlashlight(){
  if(flashlightBattery<=0){toast('FLASHLIGHT BATTERY EMPTY. SEARCH FOR CELLS.');return;}
  flashlight=!flashlight;
  sound('radio');
  toast(flashlight?'FLASHLIGHT ON. STAY ALERT.':'FLASHLIGHT OFF. MOVE QUIETLY.',1.3);
}
function onKeyDown(e){
  const key=e.key.toLowerCase();
  keys[key]=true;
  if([' ','arrowup','arrowdown','arrowleft','arrowright'].includes(key))e.preventDefault();
  if(e.repeat)return;
  if(key==='escape'){
    if(state.screen==='game')pauseGame();
    else if(['objectives','inventory','radio'].includes(state.screen))closeOverlay();
    else if(state.screen==='pause')closeOverlay();
    else if(state.screen!=='menu')setScreen('menu');
    return;
  }
  if(!state.running)return;
  if(key==='e')interact();
  if(key==='f')toggleFlashlight();
  if(key==='r'){
    state.reloadActive=true;
    reloadWeapon();
  }
  if(key==='j'||key==='tab'){
    e.preventDefault();
    openObjectives();
  }
  if(key==='i')openInventory();
  if(key===' '&&state.floor==='outside')shoot();
  if(key==='q'){
    if(batteryCells>0){
      batteryCells--;
      flashlightBattery=Math.min(100,flashlightBattery+55);
      toast('BATTERY CELL USED. LIGHT RESTORED.',1.5);
      updateHUD();
      updateInventory();
    }else toast('NO BATTERY CELLS LEFT.',1.2);
  }
}
function onKeyUp(e){
  keys[e.key.toLowerCase()]=false;
}
function menuFrame(){
  if(state.running)return;
  drawMenuArt();
  requestAnimationFrame(menuFrame);
}
function loop(now){
  if(!state.running)return;
  const dt=Math.min(.035,Math.max(.001,(now-state.lastFrame)/1000));
  state.lastFrame=now;
  if(!state.paused&&!state.gameOver)update(dt);
  drawWorld();
  if(state.running)requestAnimationFrame(loop);
}
function boot(){
  initializeAssets();
  drawPortraits();
  drawMenuArt();
  bindEvents();
  applyControlMode();
  updateCharacterSelection();
  updateObjectives();
  menuFrame();
}
boot();
})();
</script>
</body>
</html>'''

@app.get('/')
def index():
    return Response(HTML, mimetype='text/html')

@app.get('/health')
def health():
    return jsonify(status='ok', game='Florida Shadows — State Trooper Horror Files', version='2.0')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', '5000'))
    app.run(host='0.0.0.0', port=port, debug=False)
