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
body.prologue-mode #hud { display: none !important; }
body.prologue-mode.prologue-call #touchControls,
body.prologue-mode.prologue-arrival #touchControls { display: none !important; }
body.prologue-mode.prologue-drive.mobile-mode #touchControls { display: block; }
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
  grid-template-columns: repeat(2, minmax(0, 1fr));
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
.credits-panel {
  background: linear-gradient(145deg, rgba(10, 18, 13, .98), rgba(5, 8, 7, .98));
  border-color: #76664a;
}
.credits-hero {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px;
  margin: 18px 0 22px;
  background: linear-gradient(110deg, #17221a, #0a100c);
  border: 1px solid #485544;
}
.credits-mark {
  display: grid;
  flex: 0 0 58px;
  height: 58px;
  place-items: center;
  border: 2px solid #9b4644;
  background: #160e0e;
  color: #e4c98d;
  font-size: 22px;
  font-weight: 900;
  text-shadow: 2px 2px #4d1b1d;
}
.credits-hero b, .credits-hero span, .credits-hero small {
  display: block;
}
.credits-hero b {
  color: #e8dfc7;
  font-size: 17px;
  letter-spacing: 2px;
}
.credits-hero span {
  margin-top: 5px;
  color: #c5b487;
  font-size: 10px;
  letter-spacing: 1px;
}
.credits-hero small {
  margin-top: 7px;
  color: #96a293;
  font-size: 10px;
}
.credit-name {
  display: inline-block;
  margin-top: 8px;
  color: #f0d7a0;
  font-size: 20px;
  letter-spacing: .5px;
}
.credit-alias {
  color: #b7a57f;
  font-size: 11px;
}
.credits-lines p {
  margin: 11px 0 0;
}
.credits-quote {
  border-color: #65563a;
  color: #e0d2ac;
  font-style: italic;
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
    <p class="intro">Choose one playable lead: one boy officer or one girl officer. Your choice changes movement, resilience, and starting equipment.</p>
    <div class="selection-strip">
      <button class="character selected" data-char="hugo"><div class="avatar"><canvas id="charArt0" width="64" height="64"></canvas></div><strong>BOY · OFFICER HUGO</strong><small>Male playable character<br>Steady aim · Balanced field kit</small></button>
      <button class="character" data-char="yumi"><div class="avatar"><canvas id="charArt1" width="64" height="64"></canvas></div><strong>GIRL · OFFICER YUMI</strong><small>Female playable character<br>Quick response · Longer stamina</small></button>
    </div>
    <div class="info-card" id="characterDetails"><b>BOY · OFFICER HUGO</b><br>Experienced male patrol officer with a balanced field kit.</div>
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
      <div class="rule"><b>01 / ANSWER THE CALL</b>Begin inside your patrol car. Press E or tap the screen to accept dispatch.</div>
      <div class="rule"><b>02 / DRIVE TO MILE MARKER 9</b>Hold W / Up to accelerate, A / D or arrows to steer, and S / Down to brake. Mobile players use the direction pad.</div>
      <div class="rule"><b>03 / YOU ARE ALONE</b>Arrive at the roadside and press E or SEARCH to leave the car. Backup is unavailable.</div>
      <div class="rule"><b>04 / INVESTIGATE</b>Recover five pieces of evidence. Stand near glowing objects and press E or tap SEARCH.</div>
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
  <div class="panel credits-panel">
    <div class="kicker">The people behind the case file</div>
    <h2 class="section-title">Credits & Appreciation</h2>
    <div class="credits-hero">
      <div class="credits-mark">FS</div>
      <div><b>FLORIDA SHADOWS</b><span>STATE TROOPER HORROR FILES</span><small>Pixel horror project · Scream Jam 2026</small></div>
    </div>
    <div class="credits-lines"><b>WITH APPRECIATION TO</b><br><strong class="credit-name">Mayumi Alingarog</strong><br><span class="credit-alias">Also known as Yumi, Mimi, and Yumimi</span><p>To Mayumi Alingarog, my classmate and fellow developer: thank you for being such a helpful, kind, and respectful person. Your support, encouragement, and willingness to share this creative journey mean a lot. Your kindness makes collaboration better, and I am grateful to have you as a classmate and fellow developer.</p><p>This project is a little more special because of the people who offer encouragement along the way. Thank you for being one of them.</p></div>
    <div class="credits-lines"><b>TO EVERYONE WHO PLAYS</b><br>Thank you for stepping into the swamp, investigating the case, and helping bring this horror story to life. Keep exploring, keep creating, and never ignore strange sounds on the radio.</div>
    <div class="info-card credits-quote">“Every mystery leaves a trace. Every crime leaves a shadow. And some shadows are always watching.”</div>
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
const lightCanvas=document.createElement('canvas');
const lightCtx=lightCanvas.getContext('2d');
const mini=$('minimap');
const mctx=mini.getContext('2d');
const WORLD={w:3200,h:2500};
const TILE=32;
const specs={
  hugo:{name:'Officer Hugo',color:'#29372d',shirt:'#777650',speed:158,hp:110,stamina:105,ammo:6,reserve:24,gender:'male',hair:'#29231c'},
  yumi:{name:'Officer Yumi',color:'#303d36',shirt:'#817552',speed:174,hp:95,stamina:125,ammo:6,reserve:26,gender:'female',hair:'#201a18'}
};
const state={
  screen:'menu',
  selectedCharacter:'hugo',
  pendingCharacter:'hugo',
  controlMode:'desktop',
  pendingMode:'desktop',
  options:{shake:true,subtitles:true},
  running:false,
  paused:false,
  prologueStage:'call',
  prologueTimer:0,
  driveProgress:0,
  driveSpeed:0,
  driveLane:0,
  driveScroll:0,
  driveShake:0,
  driveSirenPhase:0,
  driveNearMissTimer:0,
  drivePassedCars:0,
  driveCollisionCooldown:0,
  driveCrashTimer:0,
  driveDamage:0,
  driveCollisionCount:0,
  lastBuildingExit:null,
  sceneFade:0,
  horrorBeat:0,
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
  lightCanvas.width=canvas.width;
  lightCanvas.height=canvas.height;
  canvas.style.width=W+'px';
  canvas.style.height=H+'px';
  ctx.setTransform(dpr,0,0,dpr,0,0);
  lightCtx.setTransform(dpr,0,0,dpr,0,0);
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
  if(name!=='game'){
    document.body.classList.remove('prologue-mode','prologue-call','prologue-drive','prologue-arrival');
  }
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
function roadNetworks(){
  return [
    roadPoints(),
    [{x:320,y:280},{x:170,y:430},{x:125,y:690},{x:205,y:970},{x:410,y:1130}],
    [{x:560,y:520},{x:370,y:665},{x:360,y:850},{x:505,y:1035},{x:690,y:1130}],
    [{x:850,y:790},{x:1050,y:660},{x:1340,y:650},{x:1570,y:790},{x:1710,y:980}],
    [{x:1150,y:945},{x:1060,y:1180},{x:1110,y:1430},{x:1330,y:1610},{x:1650,y:1720}],
    [{x:1520,y:1120},{x:1740,y:970},{x:2020,y:1000},{x:2270,y:1180},{x:2510,y:1190}],
    [{x:1900,y:1390},{x:2030,y:1600},{x:2260,y:1760},{x:2520,y:1800},{x:2760,y:2020}],
    [{x:410,y:1130},{x:450,y:1500},{x:740,y:1670},{x:980,y:1840},{x:1290,y:1920}],
    [{x:1710,y:980},{x:1850,y:760},{x:2130,y:710},{x:2410,y:780},{x:2630,y:920}],
    [{x:2520,y:1800},{x:2790,y:1740},{x:3050,y:1840}]
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
  for(const points of roadNetworks()){
    for(let i=0;i<points.length-1;i++){
      if(pointSegmentDistance(x,y,points[i],points[i+1])<84)return true;
    }
  }
  return false;
}
function roadDistance(x,y){
  let result=Infinity;
  for(const points of roadNetworks()){
    for(let i=0;i<points.length-1;i++)result=Math.min(result,pointSegmentDistance(x,y,points[i],points[i+1]));
  }
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
  for(const o of objects){
    if(o.type==='building')list.push({x:o.x,y:o.y,w:o.w,h:o.h});
  }
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
    {id:'tower',x:2390,y:1740,type:'building',name:'Radio relay hut',detail:'The emergency relay is still receiving something.',room:'tower',w:178,h:136,style:'relay'},
    {id:'motel',x:110,y:1100,type:'building',name:'Pine Rest Motel',detail:'A roadside motel with a vacancy sign that keeps switching off.',room:'motel',w:188,h:144,style:'motel'},
    {id:'diner',x:720,y:900,type:'building',name:'Last Stop Diner',detail:'The counter is empty, but one coffee is still steaming.',room:'diner',w:196,h:138,style:'diner'},
    {id:'clinic',x:1210,y:445,type:'building',name:'County Clinic',detail:'The emergency lights are on. Nobody answers the door.',room:'clinic',w:184,h:142,style:'clinic'},
    {id:'depot',x:2700,y:1080,type:'building',name:'Road Maintenance Depot',detail:'A maintenance depot with a broken gate and abandoned tools.',room:'depot',w:196,h:150,style:'depot'},
    {id:'church',x:2180,y:1870,type:'building',name:'St. Mercy Chapel',detail:'Candles glow inside although the power is gone.',room:'church',w:174,h:160,style:'chapel'},
    {id:'warehouse',x:1370,y:2110,type:'building',name:'Flood Control Warehouse',detail:'The warehouse doors are chained from the inside.',room:'warehouse',w:210,h:158,style:'warehouse'},
    {id:'farmhouse',x:2820,y:1570,type:'building',name:'Cypress Farmhouse',detail:'A farmhouse with a light moving behind its upstairs window.',room:'farmhouse',w:182,h:146,style:'farmhouse'},
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
  rooms.motel=structuredClone(rooms.cabin);
  rooms.motel.title='PINE REST MOTEL';
  rooms.motel.w=920;rooms.motel.h=620;rooms.motel.spawn={x:460,y:520};rooms.motel.exit={x:460,y:574};
  rooms.motel.props=[{x:170,y:145,w:118,h:70,t:'bed'},{x:390,y:140,w:120,h:55,t:'desk'},{x:700,y:155,w:90,h:115,t:'cabinet'},{x:230,y:355,w:150,h:48,t:'table'},{x:650,y:390,w:100,h:55,t:'bed'}];
  rooms.motel.items=[{x:395,y:170,type:'loot',name:'Motel first-aid kit',loot:'medkit',found:false},{x:700,y:300,type:'loot',name:'Motel ammunition tin',loot:'ammo',found:false}];
  rooms.diner=structuredClone(rooms.gas);
  rooms.diner.title='LAST STOP DINER';
  rooms.diner.w=900;rooms.diner.h=600;rooms.diner.spawn={x:450,y:500};rooms.diner.exit={x:450,y:554};
  rooms.diner.props=[{x:185,y:155,w:180,h:42,t:'table'},{x:420,y:155,w:180,h:42,t:'table'},{x:660,y:155,w:140,h:42,t:'table'},{x:180,y:340,w:220,h:46,t:'desk'},{x:685,y:350,w:85,h:130,t:'shelves'}];
  rooms.diner.items=[{x:180,y:370,type:'loot',name:'Diner medical bag',loot:'medkit',found:false},{x:685,y:300,type:'loot',name:'Diner spare batteries',loot:'battery',found:false}];
  rooms.clinic=structuredClone(rooms.station);
  rooms.clinic.title='COUNTY CLINIC';
  rooms.clinic.w=900;rooms.clinic.h=620;rooms.clinic.spawn={x:450,y:520};rooms.clinic.exit={x:450,y:574};
  rooms.clinic.props=[{x:175,y:145,w:125,h:65,t:'desk'},{x:390,y:150,w:90,h:135,t:'cabinet'},{x:660,y:150,w:110,h:65,t:'table'},{x:220,y:365,w:130,h:55,t:'bed'},{x:600,y:365,w:130,h:55,t:'bed'}];
  rooms.clinic.items=[{x:175,y:185,type:'loot',name:'Clinic medical supplies',loot:'medkit',found:false},{x:660,y:185,type:'loot',name:'Clinic battery crate',loot:'battery',found:false}];
  rooms.depot=structuredClone(rooms.station);
  rooms.depot.title='ROAD MAINTENANCE DEPOT';
  rooms.depot.w=900;rooms.depot.h=620;rooms.depot.spawn={x:450,y:520};rooms.depot.exit={x:450,y:574};
  rooms.depot.props=[{x:170,y:160,w:180,h:65,t:'desk'},{x:440,y:145,w:145,h:110,t:'cabinet'},{x:700,y:160,w:100,h:145,t:'shelves'},{x:250,y:390,w:155,h:70,t:'table'},{x:650,y:390,w:155,h:70,t:'table'}];
  rooms.depot.items=[{x:440,y:280,type:'loot',name:'Road crew ammunition',loot:'ammo',found:false},{x:700,y:335,type:'loot',name:'Road crew batteries',loot:'battery',found:false}];
  rooms.church=structuredClone(rooms.cabin);
  rooms.church.title='ST. MERCY CHAPEL';
  rooms.church.w=860;rooms.church.h=620;rooms.church.spawn={x:430,y:520};rooms.church.exit={x:430,y:574};
  rooms.church.props=[{x:430,y:150,w:190,h:60,t:'table'},{x:200,y:250,w:70,h:120,t:'cabinet'},{x:660,y:250,w:70,h:120,t:'cabinet'},{x:430,y:360,w:220,h:45,t:'table'}];
  rooms.church.items=[{x:430,y:185,type:'loot',name:'Chapel first-aid kit',loot:'medkit',found:false},{x:660,y:315,type:'loot',name:'Chapel emergency batteries',loot:'battery',found:false}];
  rooms.warehouse=structuredClone(rooms.gas);
  rooms.warehouse.title='FLOOD CONTROL WAREHOUSE';
  rooms.warehouse.w=960;rooms.warehouse.h=640;rooms.warehouse.spawn={x:480,y:540};rooms.warehouse.exit={x:480,y:594};
  rooms.warehouse.props=[{x:170,y:150,w:130,h:120,t:'shelves'},{x:380,y:150,w:130,h:120,t:'shelves'},{x:610,y:150,w:130,h:120,t:'shelves'},{x:800,y:150,w:90,h:120,t:'cabinet'},{x:480,y:370,w:180,h:65,t:'table'}];
  rooms.warehouse.items=[{x:800,y:300,type:'loot',name:'Warehouse ammunition',loot:'ammo',found:false},{x:480,y:400,type:'loot',name:'Warehouse medical crate',loot:'medkit',found:false}];
  rooms.farmhouse=structuredClone(rooms.cabin);
  rooms.farmhouse.title='CYPRESS FARMHOUSE';
  rooms.farmhouse.w=900;rooms.farmhouse.h=620;rooms.farmhouse.spawn={x:450,y:520};rooms.farmhouse.exit={x:450,y:574};
  rooms.farmhouse.props=[{x:190,y:155,w:120,h:75,t:'bed'},{x:420,y:150,w:120,h:55,t:'desk'},{x:690,y:160,w:95,h:115,t:'cabinet'},{x:230,y:370,w:150,h:50,t:'table'},{x:670,y:380,w:120,h:50,t:'bed'}];
  rooms.farmhouse.items=[{x:420,y:180,type:'loot',name:'Farmhouse emergency kit',loot:'medkit',found:false},{x:690,y:300,type:'loot',name:'Farmhouse spare ammo',loot:'ammo',found:false}];
  return structuredClone(rooms[name]||rooms.checkpoint);
}
function resetGame(){
  const spec=specs[state.selectedCharacter];
  player={x:310,y:330,r:10,angle:0,speed:spec.speed,hp:spec.hp,maxHp:spec.hp,stamina:spec.stamina,maxStamina:spec.stamina,step:0,moving:false,hidden:false,invulnerable:0,flash:0,footstep:0};
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
    crawlers.push({x:760+i*410,y:420+(i%3)*450,r:9,hp:2,speed:70+Math.random()*15,phase:Math.random()*8,alert:false,attack:0,dead:false,hiddenUntil:14});
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
  state.prologueStage='call';
  state.prologueTimer=0;
  state.driveProgress=0;
  state.driveSpeed=0;
  state.driveLane=0;
  state.driveScroll=0;
  state.driveShake=0;
  state.driveSirenPhase=0;
  state.driveNearMissTimer=0;
  state.drivePassedCars=0;
  state.driveCollisionCooldown=0;
  state.driveCrashTimer=0;
  state.driveDamage=0;
  state.driveCollisionCount=0;
  state.lastBuildingExit=null;
  state.sceneFade=0;
  state.horrorBeat=0;
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
  document.body.classList.add('game-active','prologue-mode','prologue-call');
  applyControlMode();
  setScreen('game');
  updateHUD();
  updateObjectives();
  audioStart();
  tone(280,.15,'sine',.08,160);
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
function setPrologueStage(stage){
  state.prologueStage=stage;
  state.prologueTimer=0;
  document.body.classList.toggle('prologue-call',stage==='call');
  document.body.classList.toggle('prologue-drive',stage==='drive');
  document.body.classList.toggle('prologue-arrival',stage==='arrival');
  document.body.classList.toggle('prologue-mode',stage!=='swamp');
  if(stage==='drive'){state.driveProgress=0;state.driveSpeed=0;state.driveLane=0;state.driveScroll=0;state.driveShake=0;state.driveSirenPhase=0;state.driveNearMissTimer=0;state.drivePassedCars=0;state.driveCollisionCooldown=1.2;state.driveCrashTimer=0;state.driveDamage=0;state.driveCollisionCount=0;tone(540,.18,'sawtooth',.06,-210);toast('DISPATCH: Proceed to mile marker nine. You are the only available unit.',4);}
  if(stage==='arrival'){state.driveSpeed=0;sound('radio');tone(76,.75,'triangle',.08,-34);}
}
function acceptDispatch(){
  if(state.prologueStage!=='call')return;
  audioStart();
  setPrologueStage('drive');
}
function exitPatrolCar(){
  if(state.prologueStage!=='arrival')return;
  keys={};
  touchRun=false;
  pointer.down=false;
  setPrologueStage('swamp');
  const safeSpawns=[{x:520,y:500},{x:500,y:480},{x:550,y:520},{x:470,y:465},{x:560,y:545},{x:430,y:450}];
  let spawn=safeSpawns.find(point=>!blockedAt(point.x,point.y,player.r));
  if(!spawn)spawn={x:520,y:500};
  player.x=spawn.x;player.y=spawn.y;player.angle=.9;player.moving=false;player.step=0;
  camera.x=clamp(player.x-W/2,0,WORLD.w-W);
  camera.y=clamp(player.y-H/2,0,WORLD.h-H);
  lastSafe={x:player.x,y:player.y};
  state.elapsed=0;state.horrorBeat=0;state.lightningNext=3.2;state.sceneFade=.78;
  updateHUD();updateObjectives();
  toast('SCENE LOG: No backup. No witnesses. WASD / ARROWS TO MOVE. E SEARCHES. F FLASHLIGHT.',4);
  tone(58,.8,'triangle',.07,-25);
}
function updatePrologue(dt){
  state.prologueTimer+=dt;
  if(state.prologueStage==='drive'){
    const forward=keys.w||keys.arrowup;
    const brake=keys.s||keys.arrowdown;
    const steer=(keys.d||keys.arrowright?1:0)-(keys.a||keys.arrowleft?1:0);
    if(forward)state.driveSpeed=Math.min(100,state.driveSpeed+31*dt);
    else state.driveSpeed=Math.max(0,state.driveSpeed-8*dt);
    if(brake)state.driveSpeed=Math.max(0,state.driveSpeed-72*dt);
    const handling=Math.max(.54,1-state.driveDamage*.0035);
    state.driveLane=clamp(state.driveLane+steer*dt*(.78+state.driveSpeed*.009)*handling,-1.15,1.15);
    state.driveScroll+=dt*(13+state.driveSpeed*2.35);
    state.driveSirenPhase+=dt;
    state.driveNearMissTimer=Math.max(0,state.driveNearMissTimer-dt);
    state.driveShake=Math.max(0,state.driveShake-dt*2.8);
    if(Math.abs(state.driveLane)>.83){
      state.driveSpeed=Math.max(18,state.driveSpeed-24*dt);
      state.driveShake=Math.min(1,state.driveShake+dt*.8);
      if(Math.random()<dt*.9)tone(90,.08,'square',.025,-20);
    }
    state.driveCollisionCooldown=Math.max(0,state.driveCollisionCooldown-dt);
    state.driveCrashTimer=Math.max(0,state.driveCrashTimer-dt);
    const playerLane=state.driveLane*.49;
    for(let i=0;i<12;i++){
      const direction=i%3===0?1:-1;
      const phase=((i*.137+state.driveScroll*(direction>0?.00052:-.00031))%1+1)%1;
      const z=.035+phase*.91;
      const lane=[-.22,.18,-.38,.42,-.08,.31,-.30,.12,.39,-.15,.25,-.43][i];
      if(z>.77&&z<.99&&Math.abs(lane-playerLane)<.17&&state.driveCollisionCooldown<=0&&state.driveSpeed>16){
        state.driveCollisionCooldown=3.8;
        state.driveCrashTimer=1.7;
        state.driveCollisionCount++;
        state.driveDamage=Math.min(100,state.driveDamage+Math.max(18,state.driveSpeed*.38));
        state.driveSpeed=Math.max(0,state.driveSpeed-42);
        state.driveProgress=Math.max(0,state.driveProgress-1.4);
        state.driveShake=1;
        state.driveNearMissTimer=0;
        sound('hurt');
        tone(52,.46,'sawtooth',.2,-20);
        if(Math.random()<.5)tone(990,.07,'square',.05,-650);
        toast(state.driveCollisionCount===1?'COLLISION! You clipped a car. Steer clear of traffic.':'CRASH! The patrol car is taking serious damage.',3.2);
      }
    }
    if(Math.abs(state.driveLane)>1.03&&state.driveCollisionCooldown<=0&&state.driveSpeed>22){
      state.driveCollisionCooldown=3.2;
      state.driveCrashTimer=1.1;
      state.driveCollisionCount++;
      state.driveDamage=Math.min(100,state.driveDamage+15);
      state.driveSpeed=Math.max(12,state.driveSpeed-30);
      state.driveShake=1;
      sound('hurt');
      toast('CURB IMPACT! Steer back onto the road.',2.7);
    }
    if(state.driveDamage>65&&Math.random()<dt*.28&&state.driveSpeed>68)state.driveSpeed=Math.max(35,state.driveSpeed-10);
    state.driveProgress+=dt*(.40+state.driveSpeed*.046)*(Math.abs(state.driveLane)>.9?.58:1);
    const trafficCycle=Math.floor(state.driveScroll/245);
    if(trafficCycle>state.drivePassedCars&&state.driveSpeed>35){
      state.drivePassedCars=trafficCycle;
      if(Math.random()<.58){
        state.driveShake=Math.max(state.driveShake,.12);
        tone(Math.random()<.5?125:185,.12,'triangle',.025,-45);
        if(Math.random()<.32)toast(choose(['A SEMI ROARS PAST IN THE RAIN.','HEADLIGHTS FLASH FROM AN ONCOMING CAR.','THE TIRES SKIM THROUGH DEEP WATER.','A DRIVER STARES AT YOU WITHOUT BLINKING.']),1.7);
      }
    }
    if(state.prologueTimer>7&&state.prologueTimer<7.08)sound('radio');
    if(state.driveDamage>=85&&state.prologueTimer%7<dt)toast('VEHICLE CRITICAL: AVOID MORE IMPACTS.',2.2);
    if(state.driveProgress>=100){state.driveProgress=100;setPrologueStage('arrival');}
  }
  for(const r of raindrops){r.y+=r.speed*dt*.65;r.x-=r.speed*.16*dt;if(r.y>H+15){r.y=-15;r.x=Math.random()*W;}if(r.x<-15)r.x=W+10;}
  state.sceneFade=Math.max(0,state.sceneFade-dt*1.7);
}
function poly(points,color){ctx.fillStyle=color;ctx.beginPath();ctx.moveTo(points[0][0],points[0][1]);for(let i=1;i<points.length;i++)ctx.lineTo(points[i][0],points[i][1]);ctx.closePath();ctx.fill();}
function strokePoly(points,color,width=1){ctx.strokeStyle=color;ctx.lineWidth=width;ctx.beginPath();ctx.moveTo(points[0][0],points[0][1]);for(let i=1;i<points.length;i++)ctx.lineTo(points[i][0],points[i][1]);ctx.closePath();ctx.stroke();}
function drawRadioScreen(x,y,w,h,active){
  px(x,y,w,h,'#070c09');px(x+3,y+3,w-6,h-6,'#17271c');px(x+7,y+7,w-14,h-14,'#09150e');
  ctx.fillStyle=active?'#b9c9a0':'#7a8876';ctx.font='bold 10px monospace';ctx.textAlign='left';ctx.fillText(active?'FSP DISPATCH':'NO SIGNAL',x+10,y+17);
  for(let i=0;i<14;i++){const hh=2+Math.abs(Math.sin(state.prologueTimer*5+i*1.4))*(active?12:3);px(x+10+i*5,y+h-11-hh,3,hh,active?'#789d72':'#354437');}
  px(x+w-18,y+9,4,4,active?'#bf5149':'#3a463b');
}
function drawPrologueCall(){
  px(0,0,W,H,'#050907');
  const sky=ctx.createLinearGradient(0,0,0,H*.7);sky.addColorStop(0,'#080f13');sky.addColorStop(.55,'#182324');sky.addColorStop(1,'#0e1513');ctx.fillStyle=sky;ctx.fillRect(0,0,W,H*.72);
  const horizon=H*.38;
  for(let i=0;i<24;i++){const bw=22+(i*37)%66,bh=55+(i*53)%Math.max(70,H*.34),x=(i*91-state.prologueTimer*3)%(W+bw)-bw;const y=horizon-bh;px(x,y,bw,bh,i%4===0?'#1a282a':'#101d20');px(x+3,y+6,bw-6,3,'#2a3735');for(let wy=y+14;wy<horizon-9;wy+=13)for(let wx=x+6;wx<x+bw-5;wx+=12)if(seeded(Math.floor(wx),Math.floor(wy))>.48)px(wx,wy,4,5,Math.sin(state.prologueTimer*2+wx)>.88?'#b5a06e':'#39483e');}
  poly([[0,horizon],[W*.32,horizon-8],[W*.69,horizon-3],[W,horizon+10],[W,H*.73],[0,H*.73]],'#18211d');
  ctx.strokeStyle='rgba(175,199,194,.34)';ctx.lineWidth=1;for(const r of raindrops){ctx.beginPath();ctx.moveTo(r.x,r.y);ctx.lineTo(r.x-5,r.y+15);ctx.stroke();}
  poly([[0,H*.77],[W*.16,H*.57],[W*.84,H*.57],[W,H*.77],[W,H],[0,H]],'#101613');
  poly([[0,H*.79],[W*.27,H*.65],[W*.73,H*.65],[W,H*.79],[W,H],[0,H]],'#202620');
  px(0,H*.77,W,H*.23,'#090d0b');
  for(let i=0;i<8;i++){const x=W*.12+i*W*.11;px(x,H*.78,2,H*.08,'#26302a');px(x-13,H*.81,28,3,'#3c4035');}
  const dashY=H*.70;poly([[0,dashY],[W*.19,H*.64],[W*.81,H*.64],[W,dashY],[W,H],[0,H]],'#171d19');poly([[0,H*.78],[W*.22,H*.68],[W*.78,H*.68],[W,H*.78],[W,H],[0,H]],'#252a23');
  px(W*.1,H*.76,W*.8,4,'#454639');px(W*.13,H*.79,W*.74,2,'#111612');
  ctx.save();ctx.translate(W*.50,H*.91);ctx.strokeStyle='#050706';ctx.lineWidth=Math.max(11,W*.018);ctx.beginPath();ctx.arc(0,0,Math.min(W,H)*.16,Math.PI*1.05,Math.PI*1.95);ctx.stroke();ctx.strokeStyle='#596052';ctx.lineWidth=3;ctx.beginPath();ctx.arc(0,0,Math.min(W,H)*.16,Math.PI*1.05,Math.PI*1.95);ctx.stroke();ctx.restore();
  drawRadioScreen(W*.065,H*.755,W*.23,H*.10,true);
  px(W*.72,H*.76,W*.19,H*.11,'#050706');px(W*.73,H*.77,W*.17,H*.075,'#121b14');ctx.fillStyle='#a7b492';ctx.font='bold '+Math.max(10,Math.floor(W*.012))+'px monospace';ctx.textAlign='center';ctx.fillText('02:17 AM',W*.815,H*.80);ctx.fillStyle='#cb5a50';ctx.fillText('UNIT 14 / LOST',W*.815,H*.825);
  px(W*.39,H*.77,W*.22,H*.075,'#0a0d0b');px(W*.405,H*.79,W*.19,H*.012,'#455047');px(W*.405,H*.81,W*.13,H*.008,'#262f27');
  px(0,0,W,Math.max(4,H*.012),'#060908');
  const pw=Math.min(690,W-34),ph=Math.min(220,H*.34),bx=(W-pw)/2,by=H*.09;
  px(bx-3,by-3,pw+6,ph+6,'#0a0d0b');px(bx,by,pw,ph,'rgba(5,10,8,.94)');strokePoly([[bx,by],[bx+pw,by],[bx+pw,by+ph],[bx,by+ph]],'#75816b',1);
  px(bx+17,by+17,4,ph-34,'#ad4a43');ctx.textAlign='left';ctx.fillStyle='#b8c5a8';ctx.font='bold 12px monospace';ctx.fillText('INCOMING DISPATCH // PRIORITY CALL',bx+34,by+31);
  ctx.fillStyle='#e9e6d6';ctx.font='bold '+Math.max(16,Math.min(24,W*.026))+'px monospace';ctx.fillText('MILE MARKER 9 — OFFICER NEEDS ASSISTANCE',bx+34,by+67);
  ctx.fillStyle='#aab4a3';ctx.font=Math.max(11,Math.min(15,W*.015))+'px monospace';ctx.fillText('Unit 14 abandoned its patrol vehicle. One deputy missing.',bx+34,by+98);ctx.fillText('No backup units available. Weather is getting worse.',bx+34,by+120);
  ctx.fillStyle='#d6b87a';ctx.font='bold '+Math.max(11,Math.min(14,W*.014))+'px monospace';ctx.fillText('DISPATCH: “Respond alone. Keep your radio open.”',bx+34,by+154);
  const blink=Math.floor(state.prologueTimer*2)%2===0;ctx.textAlign='center';ctx.fillStyle=blink?'#f0dfb4':'#89927e';ctx.font='bold '+Math.max(12,Math.min(16,W*.017))+'px monospace';ctx.fillText('PRESS E / ENTER OR TAP TO ACCEPT CALL',W/2,by+ph-18);
  drawVignette();
}
function drawTrafficCars(horizon,roadCenter,topHalf,bottomHalf,city){
  for(let i=0;i<12;i++){
    const direction=i%3===0?1:-1;
    const phase=((i*.137+state.driveScroll*(direction>0?.00052:-.00031))%1+1)%1;
    const z=.035+phase*.91;
    const y=horizon+z*z*(H-horizon);
    const roadMid=roadCenter+(W*.5-roadCenter)*z;
    const half=topHalf+(bottomHalf-topHalf)*z;
    const lane=[-.22,.18,-.38,.42,-.08,.31,-.30,.12,.39,-.15,.25,-.43][i];
    const x=roadMid+lane*half;
    const scale=.18+z*1.22;
    const cw=(city?13:11)+z*(i%4===0?62:48);
    const ch=5+z*(i%4===0?31:24);
    if(y<H*.41||y>H+ch)continue;
    ctx.save();
    ctx.globalAlpha=.46+z*.54;
    ctx.fillStyle='rgba(0,0,0,.5)';
    ctx.beginPath();ctx.ellipse(x,y+ch*.45,cw*.66,ch*.55,0,0,Math.PI*2);ctx.fill();
    const body=i%4===0?'#343a37':i%3===0?'#555148':i%2===0?'#28363a':'#4b5149';
    poly([[x-cw*.48,y-ch*.25],[x-cw*.37,y-ch*.68],[x-cw*.2,y-ch*.92],[x+cw*.2,y-ch*.92],[x+cw*.38,y-ch*.64],[x+cw*.49,y-ch*.24],[x+cw*.43,y+ch*.42],[x-cw*.43,y+ch*.42]],body);
    poly([[x-cw*.27,y-ch*.58],[x-cw*.16,y-ch*.82],[x+cw*.16,y-ch*.82],[x+cw*.29,y-ch*.58]],direction>0?'#172326':'#7c918e');
    ctx.fillStyle='#151b1a';ctx.fillRect(x-cw*.32,y-ch*.19,cw*.64,ch*.43);
    if(direction>0){
      const glow=ctx.createRadialGradient(x,y+ch*.35,1,x,y+ch*.35,cw*.42);
      glow.addColorStop(0,'rgba(255,62,47,.33)');glow.addColorStop(1,'rgba(255,45,35,0)');ctx.fillStyle=glow;ctx.fillRect(x-cw*.55,y-ch*.05,cw*1.1,ch*1.1);
      px(x-cw*.38,y+ch*.12,Math.max(2,cw*.13),Math.max(2,ch*.18),'#ef5548');px(x+cw*.25,y+ch*.12,Math.max(2,cw*.13),Math.max(2,ch*.18),'#ef5548');
    }else{
      const glow=ctx.createRadialGradient(x,y+ch*.08,1,x,y+ch*.08,cw*.85);
      glow.addColorStop(0,'rgba(234,239,205,.30)');glow.addColorStop(1,'rgba(226,239,209,0)');ctx.fillStyle=glow;ctx.fillRect(x-cw,y-ch*.5,cw*2,ch*1.6);
      px(x-cw*.38,y+ch*.1,Math.max(2,cw*.14),Math.max(2,ch*.2),'#deddb4');px(x+cw*.24,y+ch*.1,Math.max(2,cw*.14),Math.max(2,ch*.2),'#deddb4');
    }
    if(i%4===0){px(x-cw*.47,y+ch*.18,cw*.94,Math.max(2,ch*.13),'#a2a49a');px(x-cw*.12,y-ch*.95,cw*.24,Math.max(2,ch*.1),'#121918');}
    ctx.restore();
  }
}
function drawDrivingPoliceLights(){
  const phase=Math.sin(state.driveSirenPhase*17);
  const redOn=phase>0;
  ctx.save();
  const red=ctx.createRadialGradient(W*.08,H*.42,0,W*.08,H*.42,W*.42);
  red.addColorStop(0,redOn?'rgba(255,28,34,.28)':'rgba(255,28,34,.035)');red.addColorStop(1,'rgba(255,28,34,0)');
  ctx.fillStyle=red;ctx.fillRect(0,H*.15,W*.55,H*.62);
  const blue=ctx.createRadialGradient(W*.92,H*.42,0,W*.92,H*.42,W*.42);
  blue.addColorStop(0,!redOn?'rgba(40,105,255,.30)':'rgba(40,105,255,.035)');blue.addColorStop(1,'rgba(40,105,255,0)');
  ctx.fillStyle=blue;ctx.fillRect(W*.45,H*.15,W*.55,H*.62);
  ctx.globalAlpha=.28+.32*Math.abs(phase);
  ctx.fillStyle=redOn?'#b52c33':'#305eab';ctx.beginPath();ctx.moveTo(W*.05,H*.5);ctx.lineTo(W*.32,H*.62);ctx.lineTo(W*.48,H*.74);ctx.lineTo(W*.18,H*.69);ctx.closePath();ctx.fill();
  ctx.fillStyle=redOn?'#294e9e':'#c03739';ctx.beginPath();ctx.moveTo(W*.95,H*.5);ctx.lineTo(W*.68,H*.62);ctx.lineTo(W*.52,H*.74);ctx.lineTo(W*.82,H*.69);ctx.closePath();ctx.fill();
  const barY=H*.69;px(W*.435,barY,W*.052,H*.012,redOn?'#ed4c47':'#315fc0');px(W*.513,barY,W*.052,H*.012,redOn?'#315fc0':'#ed4c47');
  ctx.restore();
}
function drawDriveRainAndGlass(){
  ctx.strokeStyle='rgba(185,202,197,.28)';ctx.lineWidth=1;ctx.beginPath();
  for(let i=0;i<105;i++){
    const x=(i*137+state.driveScroll*3.4)%W;
    const y=(i*71+state.driveScroll*5.2)%(H*.72);
    ctx.moveTo(x,y);ctx.lineTo(x-5,y+14+(i%5)*2);
  }
  ctx.stroke();
  ctx.strokeStyle='rgba(192,207,196,.11)';ctx.lineWidth=2;
  for(let i=0;i<5;i++){const x=(i*W*.24+state.driveScroll*.2)%W;ctx.beginPath();ctx.moveTo(x,H*.13);ctx.quadraticCurveTo(x-W*.03,H*.32,x-W*.07,H*.57);ctx.stroke();}
}
function drawDriveSideStreets(horizon,roadCenter,topHalf,bottomHalf,city){
  const ground=city?'#272d2a':'#162119';
  for(let i=0;i<(city?4:2);i++){
    let z=((i*.29+state.driveScroll*.00043+.12)%1);
    if(z<.12)z+=.12;
    const y=horizon+z*z*(H-horizon);
    const cx=roadCenter+(W*.5-roadCenter)*z;
    const half=topHalf+(bottomHalf-topHalf)*z;
    const thick=5+z*38;
    const spread=W*(city?.09:.05)+z*W*(city?.29:.16);
    for(const side of [-1,1]){
      const edge=cx+side*half;
      const far=edge+side*spread;
      poly([[edge,y-thick*.48],[far,y-thick*1.3],[far+side*(7+z*12),y+thick*1.4],[edge,y+thick*.48]],'#0b100e');
      poly([[edge+side*2,y-thick*.35],[far-side*2,y-thick],[far-side*2,y+thick],[edge+side*2,y+thick*.35]],ground);
      if(city&&z>.31){
        for(let k=0;k<5;k++){
          const sx=edge+side*(spread*(.24+k*.12));
          const sy=y+Math.sin(k*2+i)*thick*.22;
          px(sx,sy,Math.max(2,z*5),Math.max(2,z*3),'#a4a18a');
        }
        if(i%2===0){
          const poleX=far-side*(z*3+2);px(poleX,y-thick*2.3,Math.max(2,z*3),thick*2.3,'#161e1b');
          px(poleX-side*4,y-thick*2.5,Math.max(4,z*9),Math.max(3,z*7),i%4===0?'#a5423d':'#a8b08c');
          const glow=ctx.createRadialGradient(poleX,y-thick*2.5,1,poleX,y-thick*2.5,15+z*65);glow.addColorStop(0,'rgba(198,176,112,.22)');glow.addColorStop(1,'rgba(198,176,112,0)');ctx.fillStyle=glow;ctx.fillRect(poleX-55,y-thick*2.5-55,110,110);
        }
      }
    }
    if(city&&z>.45&&z<.98){
      const crossY=y-thick*.12;
      for(let k=-3;k<=3;k++){
        const sx=cx+k*(5+z*10);
        px(sx,crossY,Math.max(2,z*4),Math.max(2,z*4),'#aaa68e');
      }
    }
  }
  if(city){
    for(const side of [-1,1]){
      for(let i=0;i<5;i++){
        const z=((i*.23+state.driveScroll*.00031+.07)%1);
        const y=horizon+z*z*(H-horizon);
        const cx=roadCenter+(W*.5-roadCenter)*z;
        const half=topHalf+(bottomHalf-topHalf)*z;
        const x=cx+side*(half+W*(.08+z*.14));
        const lampY=y-z*H*.045;
        if(x>-25&&x<W+25){
          px(x,y-z*45,Math.max(2,z*3),z*45,'#151d1a');px(x-side*z*8,lampY,Math.max(5,z*15),Math.max(2,z*5),'#9d9b80');
          const glow=ctx.createRadialGradient(x-side*z*6,lampY,1,x-side*z*6,lampY,8+z*45);glow.addColorStop(0,'rgba(218,193,133,.3)');glow.addColorStop(1,'rgba(218,193,133,0)');ctx.fillStyle=glow;ctx.fillRect(x-z*48,lampY-z*45,z*96,z*90);
        }
      }
    }
  }
}
function drawDriveScene(){
  const t=state.driveProgress/100;const city=t<.62;
  const sky=ctx.createLinearGradient(0,0,0,H*.58);sky.addColorStop(0,city?'#070f18':'#020604');sky.addColorStop(.58,city?'#202d31':'#111d14');sky.addColorStop(1,city?'#344039':'#1a281b');
  ctx.fillStyle='#111713';ctx.fillRect(0,0,W,H);ctx.fillStyle=sky;ctx.fillRect(0,0,W,H*.59);
  const horizon=H*.38+Math.sin(state.driveScroll*.006)*3;
  ctx.fillStyle=city?'#252c29':'#172219';ctx.fillRect(0,horizon,W,H-horizon);
  for(let i=0;i<(city?42:34);i++){
    const speed=.38+(i%6)*.13;
    let layer=(i*83-state.driveScroll*speed)%(W+180);if(layer<0)layer+=W+180;
    const x=layer-90;const bw=24+(i*19)%84;const hh=32+(i*43)%Math.max(65,H*.37);const y=horizon-hh;
    if(city){
      const base=i%5===0?'#1b282b':i%3===0?'#111f22':'#142124';
      px(x-3,y-3,bw+6,hh+6,'#0a1113');px(x,y,bw,hh,base);px(x+3,y+4,bw-6,3,'#303c3b');
      if(i%4===0){px(x+bw*.62,y-9,bw*.25,10,'#293536');px(x+bw*.7,y-17,2,8,'#3c4a47');}
      for(let wy=y+10;wy<horizon-5;wy+=11){
        px(x+4,wy,bw-8,1,'#1e2b2b');
        for(let wx=x+6;wx<x+bw-5;wx+=11){
          const lit=seeded(i,Math.floor(wy+wx))>.48;
          if(lit){const flick=Math.sin(state.driveScroll*.027+i+wx*.3)>.86;px(wx,wy,4,5,flick?'#d1b67a':((i+Math.floor(wx/11))%4===0?'#7b9b98':'#8e9675'));}
        }
      }
      if(i%7===0){px(x+bw*.17,y+hh*.66,bw*.66,hh*.19,'#07100e');px(x+bw*.21,y+hh*.69,bw*.58,hh*.1,'#4a5545');px(x+bw*.28,y+hh*.71,bw*.42,hh*.035,'#c1a76d');}
      if(i%9===0){px(x+bw*.25,y-12,bw*.5,8,'#070b09');px(x+bw*.27,y-10,bw*.46,3,'#c2463f');}
    }else{
      px(x+10,horizon-35,6,35,'#151d14');px(x,horizon-65,bw,37,'#101a12');px(x+5,horizon-80,bw-10,24,'#0b150e');px(x+13,horizon-94,bw-26,17,'#111c13');
      px(x+bw*.25,horizon-50,3,7,'#b99d62');
    }
  }
  const roadCenter=W*.5-state.driveLane*W*.24+Math.sin(state.driveScroll*.004)*W*.025;const topHalf=W*.075,bottomHalf=W*.49;
  drawDriveSideStreets(horizon,roadCenter,topHalf,bottomHalf,city);
  poly([[roadCenter-topHalf,horizon],[roadCenter+topHalf,horizon],[W*.5+bottomHalf,H],[W*.5-bottomHalf,H]],'#090d0c');
  poly([[roadCenter-topHalf+3,horizon],[roadCenter+topHalf-3,horizon],[W*.5+bottomHalf-14,H],[W*.5-bottomHalf+14,H]],'#282d29');
  strokePoly([[roadCenter-topHalf,horizon],[W*.5-bottomHalf,H],[W*.5+bottomHalf,H],[roadCenter+topHalf,horizon]],'#4e5147',2);
  for(let i=0;i<11;i++){const z=((i/11+state.driveScroll*.011)%1);const y=horizon+z*z*(H-horizon);const width=1+z*5;const h=4+z*40;const cx=roadCenter+(W*.5-roadCenter)*z;const len=width+z*4;px(cx-len/2,y,len,h,'#8b856d');}
  for(const side of [-1,1]){for(let i=0;i<5;i++){const z=((i/5+state.driveScroll*.004)%1);const y=horizon+z*z*(H-horizon);const x=roadCenter+side*(topHalf+z*(bottomHalf+25));if(city){px(x-2,y-35*z-2,4*z+2,38*z+2,'#30362d');px(x-8*z,y-38*z,16*z+4,4*z+2,'#b3a16d');if(z>.45){px(x-13*z,y-36*z,26*z,4*z,'#4f5748');}}else{px(x-2-z*3,y-38*z,4+z*6,42*z,'#0a100c');px(x-12*z,y-45*z,24*z,13*z,'#132117');px(x-15*z,y-36*z,30*z,11*z,'#17261a');}}}
  drawTrafficCars(horizon,roadCenter,topHalf,bottomHalf,city);
  drawDrivingPoliceLights();
  drawDriveRainAndGlass();
  const shake=state.driveShake*4;ctx.save();ctx.translate((Math.random()-.5)*shake,(Math.random()-.5)*shake);
  poly([[0,H*.79],[W*.18,H*.68],[W*.82,H*.68],[W,H*.79],[W,H],[0,H]],'#090d0b');poly([[0,H*.82],[W*.23,H*.72],[W*.77,H*.72],[W,H*.82],[W,H],[0,H]],'#20251f');
  px(W*.07,H*.83,W*.25,H*.08,'#0b100c');px(W*.68,H*.83,W*.25,H*.08,'#0b100c');
  ctx.save();ctx.translate(W*.5,H*.93);ctx.strokeStyle='#050706';ctx.lineWidth=Math.max(10,W*.02);ctx.beginPath();ctx.arc(0,0,Math.min(W,H)*.15,Math.PI*1.08,Math.PI*1.92);ctx.stroke();ctx.strokeStyle='#4b5248';ctx.lineWidth=3;ctx.beginPath();ctx.arc(0,0,Math.min(W,H)*.15,Math.PI*1.08,Math.PI*1.92);ctx.stroke();ctx.restore();
  drawRadioScreen(W*.055,H*.755,W*.20,H*.085,state.driveProgress<75);
  px(W*.72,H*.765,W*.20,H*.09,'#070a08');px(W*.735,H*.778,W*.17,H*.055,'#131e17');ctx.textAlign='center';ctx.fillStyle='#b6c9a6';ctx.font='bold '+Math.max(12,Math.min(20,W*.024))+'px monospace';ctx.fillText(Math.round(state.driveSpeed)+' MPH',W*.82,H*.81);ctx.fillStyle='#c6c7ae';ctx.font='10px monospace';ctx.fillText('CRUISE / MILE 9',W*.82,H*.832);
  ctx.restore();
  const barW=Math.min(500,W*.54),barX=(W-barW)/2,barY=H*.09;px(barX-8,barY-10,barW+16,69,'rgba(3,7,5,.88)');ctx.fillStyle='#bfc8b3';ctx.font='bold 12px monospace';ctx.textAlign='left';ctx.fillText('DESTINATION: MILE MARKER 9',barX,barY+8);px(barX,barY+20,barW,9,'#263129');px(barX+2,barY+22,(barW-4)*t,5,t>.82?'#b34a43':'#b6b17a');ctx.fillStyle='#e5e2d4';ctx.textAlign='right';ctx.fillText(Math.floor(state.driveProgress)+'%',barX+barW,barY+8);
  ctx.textAlign='center';ctx.fillStyle='#ddd6c0';ctx.font='bold '+Math.max(12,Math.min(16,W*.017))+'px monospace';ctx.fillText(Math.abs(state.driveLane)>.83?'WARNING: TIRES LEAVING ROAD':state.driveSpeed<10?'HOLD W / UP TO ACCELERATE':'A / D OR ← / → TO STEER',W/2,H*.61);
  const integrity=Math.max(0,100-state.driveDamage);
  px(W*.72,H*.86,W*.20,6,'#090e0b');px(W*.72+2,H*.86+2,W*.196*(integrity/100),2,integrity<35?'#d34a42':integrity<65?'#c2a65e':'#829b76');
  ctx.textAlign='left';ctx.fillStyle=integrity<35?'#ef7268':'#b6c3a8';ctx.font='bold 9px monospace';ctx.fillText('VEHICLE INTEGRITY '+Math.round(integrity)+'%',W*.72,H*.855);
  if(state.driveCrashTimer>0){
    const alpha=Math.min(.46,state.driveCrashTimer*.32);ctx.fillStyle='rgba(150,12,16,'+alpha+')';ctx.fillRect(0,0,W,H);
    ctx.strokeStyle='rgba(229,232,219,'+Math.min(.8,state.driveCrashTimer*.7)+')';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(W*.82,H*.15);ctx.lineTo(W*.73,H*.29);ctx.lineTo(W*.78,H*.37);ctx.lineTo(W*.67,H*.52);ctx.moveTo(W*.73,H*.29);ctx.lineTo(W*.59,H*.23);ctx.moveTo(W*.78,H*.37);ctx.lineTo(W*.9,H*.44);ctx.moveTo(W*.67,H*.52);ctx.lineTo(W*.61,H*.7);ctx.stroke();
    px(W*.29,H*.34,W*.42,58,'rgba(3,6,5,.91)');ctx.strokeStyle='#b94742';ctx.strokeRect(W*.29,H*.34,W*.42,58);ctx.textAlign='center';ctx.fillStyle='#f0c4a5';ctx.font='bold '+Math.max(16,Math.min(24,W*.027))+'px monospace';ctx.fillText('COLLISION — REGAIN CONTROL',W*.5,H*.34+24);ctx.fillStyle='#d9d8c7';ctx.font='12px monospace';ctx.fillText('Brake, steer away from traffic, and keep the car on the road.',W*.5,H*.34+44);
  }
  drawVignette();
}
function drawArrivalScene(){
  px(0,0,W,H,'#040706');const grad=ctx.createLinearGradient(0,0,0,H);grad.addColorStop(0,'#07100d');grad.addColorStop(.68,'#0d1710');grad.addColorStop(1,'#030504');ctx.fillStyle=grad;ctx.fillRect(0,0,W,H);
  for(let i=0;i<22;i++){const x=(i*79)%W;const ht=H*(.18+((i*17)%47)/100);px(x,H*.53-ht*.4,8+(i%5)*7,ht,'#0a120c');px(x-8,H*.48-ht*.25,24+(i%4)*8,10,'#0b150e');px(x-4,H*.41-ht*.2,18,12,'#0e1a11');}
  poly([[W*.37,H*.4],[W*.63,H*.4],[W*.95,H],[W*.05,H]],'#090d0a');poly([[W*.46,H*.4],[W*.54,H*.4],[W*.68,H],[W*.32,H]],'#171d17');ctx.setLineDash([18,22]);ctx.strokeStyle='#655f4a';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(W*.5,H*.41);ctx.lineTo(W*.5,H);ctx.stroke();ctx.setLineDash([]);
  const cx=W*.35,cy=H*.66;const sirenRed=Math.sin(state.prologueTimer*13)>0;ctx.save();ctx.translate(cx,cy);ctx.rotate(-.10);px(-W*.12,-H*.06,W*.24,H*.13,'#080a08');px(-W*.105,-H*.055,W*.21,H*.105,'#a6aaa0');px(-W*.082,-H*.047,W*.164,H*.085,'#263a36');px(-W*.07,-H*.04,W*.14,H*.07,'#111e1b');px(-W*.04,-H*.035,W*.08,H*.06,'#07100d');px(-W*.1,-H*.055,W*.05,H*.014,'#c9c8b5');px(W*.05,-H*.055,W*.05,H*.014,'#c9c8b5');px(-W*.025,-H*.048,W*.05,H*.018,'#eee8d0');px(-W*.105,H*.03,W*.036,H*.018,'#c8443b');px(W*.069,H*.03,W*.036,H*.018,'#c8443b');px(-W*.045,-H*.069,W*.035,H*.012,sirenRed?'#fb4844':'#255bd4');px(W*.01,-H*.069,W*.035,H*.012,sirenRed?'#255bd4':'#fb4844');ctx.restore();
  const patrolGlow=ctx.createRadialGradient(cx,H*.68,2,cx,H*.68,W*.48);patrolGlow.addColorStop(0,sirenRed?'rgba(226,34,42,.20)':'rgba(35,82,213,.20)');patrolGlow.addColorStop(1,'rgba(0,0,0,0)');ctx.fillStyle=patrolGlow;ctx.fillRect(0,H*.3,W,H*.65);
  const flashX=sirenRed?W*.17:W*.79;const flashGlow=ctx.createRadialGradient(flashX,H*.64,2,flashX,H*.64,W*.32);flashGlow.addColorStop(0,sirenRed?'rgba(240,50,47,.22)':'rgba(45,100,230,.22)');flashGlow.addColorStop(1,'rgba(0,0,0,0)');ctx.fillStyle=flashGlow;ctx.fillRect(0,H*.35,W,H*.65);
  ctx.strokeStyle='rgba(163,180,177,.30)';ctx.lineWidth=1;ctx.beginPath();for(const drop of raindrops){ctx.moveTo(drop.x,drop.y);ctx.lineTo(drop.x-4,drop.y+11);}ctx.stroke();
  const ox=W*.62,oy=H*.64;px(ox-8,oy-42,16,18,'#101511');px(ox-11,oy-23,22,37,'#1f2c23');px(ox-18,oy-21,7,27,'#151e18');px(ox+11,oy-21,7,27,'#151e18');px(ox-8,oy+10,7,22,'#121813');px(ox+2,oy+10,7,22,'#121813');px(ox-9,oy-45,18,6,'#756b49');
  ctx.save();ctx.globalAlpha=.7;ctx.strokeStyle='#d9ddbd';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(ox+8,oy-17);ctx.lineTo(W*.84,H*.4);ctx.lineTo(W*.91,H*.22);ctx.stroke();ctx.restore();
  ctx.fillStyle='rgba(192,208,195,.24)';ctx.font='12px monospace';ctx.textAlign='left';ctx.fillText('MILE MARKER 9',W*.07,H*.18);ctx.fillStyle='#d8ddcc';ctx.font='bold '+Math.max(18,Math.min(34,W*.04))+'px monospace';ctx.fillText('NO BACKUP ON SCENE',W*.07,H*.24);ctx.fillStyle='#abb7a6';ctx.font=Math.max(11,Math.min(16,W*.017))+'px monospace';ctx.fillText('One patrol car. One officer. No movement in the trees.',W*.07,H*.29);ctx.fillText('The radio is receiving a transmission from your own unit.',W*.07,H*.32);
  px(W*.07,H*.37,W*.005,H*.09,'#b34b43');ctx.fillStyle='#d4bb7e';ctx.font='bold 13px monospace';ctx.fillText('PRESS E / TAP SEARCH TO STEP OUT',W*.09,H*.415);drawVignette();
}
function drawVignette(){const v=ctx.createRadialGradient(W*.5,H*.48,Math.min(W,H)*.16,W*.5,H*.48,Math.max(W,H)*.8);v.addColorStop(0,'rgba(0,0,0,0)');v.addColorStop(.7,'rgba(0,0,0,.18)');v.addColorStop(1,'rgba(0,0,0,.72)');ctx.fillStyle=v;ctx.fillRect(0,0,W,H);}
function drawPrologue(){
  screenJitter();
  if(state.prologueStage==='call')drawPrologueCall();
  else if(state.prologueStage==='drive')drawDriveScene();
  else drawArrivalScene();
}
function drawPatrolCarWorld(){
  const x=245-camera.x+shakeX,y=278-camera.y+shakeY;
  if(x<-100||y<-100||x>W+100||y>H+100)return;
  ctx.save();ctx.translate(x,y);ctx.rotate(.78);
  px(-25,-44,50,88,'#070b08');px(-22,-40,44,80,'#a6aaa0');px(-18,-35,36,70,'#343b36');px(-17,-29,34,23,'#15221e');px(-17,7,34,20,'#15221e');px(-14,-4,28,12,'#202925');px(-21,-23,42,4,'#b4b5a4');px(-21,20,42,4,'#c2c0af');px(-19,-13,8,15,'#090d0b');px(11,-13,8,15,'#090d0b');px(-20,-38,10,5,'#d8c79c');px(10,-38,10,5,'#d8c79c');px(-19,34,9,5,'#ce433b');px(10,34,9,5,'#ce433b');px(-7,-6,14,12,'#111a16');px(-4,-2,8,4,'#c3b77d');px(-15,-2,11,5,Math.sin(state.elapsed*9)>0?'#d44a42':'#284b85');px(4,-2,11,5,Math.sin(state.elapsed*9)>0?'#284b85':'#d44a42');ctx.restore();
}

function worldCoordinates(screenX,screenY){
  return {x:screenX+camera.x,y:screenY+camera.y};
}
function nearestInteractable(){
  if(state.floor!=='outside')return nearestInteriorObject();
  let found=null;
  let best=Infinity;
  for(const o of objects){
    if(o.type==='evidence'&&o.found)continue;
    if(o.type==='loot'&&o.found)continue;
    const d=dist(player.x,player.y,o.x,o.y);
    const reach=o.type==='building'?Math.max(98,Math.max(o.w,o.h)*.5+29):76;
    if(d<reach&&d<best){best=d;found=o;}
  }
  for(const s of survivors){
    if(s.delivered)continue;
    const d=dist(player.x,player.y,s.x,s.y);
    if(d<76&&d<best){best=d;found=s;}
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
  if(state.prologueStage==='call'){acceptDispatch();return;}
  if(state.prologueStage==='arrival'){exitPatrolCar();return;}
  if(state.prologueStage==='drive'){toast('KEEP MOVING. MILE MARKER 9 IS AHEAD.',1.2);return;}
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
  state.lastBuildingExit={x:target.x,y:target.y+target.h/2+16};
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
  if(state.lastBuildingExit){
    player.x=state.lastBuildingExit.x;
    player.y=state.lastBuildingExit.y;
    state.lastBuildingExit=null;
  }else{
    if(exitName==='CHECKPOINT SHACK'){player.x=375;player.y=470;}
    if(exitName==='RANGER STATION'){player.x=930;player.y=815;}
    if(exitName==='SWAMP GAS STOP'){player.x=1480;player.y=545;}
    if(exitName==='LEANING CABIN'){player.x=1690;player.y=1380;}
    if(exitName==='RADIO RELAY HUT'){player.x=2390;player.y=1820;}
  }
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
  if(state.prologueStage==='swamp'&&dist(x,y,245,278)<43+r)return true;
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
    monster.frozenByLight=false;
    if(d<200&&monster.warpCooldown<=0){
      monster.warpCooldown=9;
      monster.x=clamp(player.x+choose([-1,1])*430,70,WORLD.w-70);
      monster.y=clamp(player.y+choose([-1,1])*350,70,WORLD.h-70);
      showRadioText('UNKNOWN TRANSMISSION','You can hear footsteps outside the building.');
      toast('SOMETHING MOVES OUTSIDE THE WALLS.',2.3);
    }
    return;
  }
  const towardMonster=angleTo(player.x,player.y,monster.x,monster.y);
  const beamDelta=Math.atan2(Math.sin(towardMonster-flashlightAngle()),Math.cos(towardMonster-flashlightAngle()));
  monster.frozenByLight=flashlight&&flashlightBattery>0&&d<505&&Math.abs(beamDelta)<.235;
  if(monster.frozenByLight&&d>58&&monster.stun<=0){
    monster.lastMove=0;
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
  if(d<250&&growlTimer<=0){
    sound('roar');
    growlTimer=5+Math.random()*6;
    if(Math.random()<.72)toast(choose(['YOU HEAR WET BREATHING OVER YOUR SHOULDER.','RADIO: DO NOT TURN AROUND.','SOMETHING SCRAPES ALONG THE TREES.','YOUR FLASHLIGHT JUST CAUGHT A SHAPE MOVING.']),1.8);
    state.intensity=Math.min(1,state.intensity+.18);
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
  if(state.prologueStage!=='swamp'){updatePrologue(dt);return;}
  state.sceneFade=Math.max(0,state.sceneFade-dt*1.7);
  state.elapsed+=dt;
  state.missionClock+=dt;
  if(state.horrorBeat===0&&state.elapsed>4.8){state.horrorBeat=1;sound('radio');toast('RADIO: “Officer… I can see you beside the car.” DISPATCH DENIES SENDING THAT TRANSMISSION.',4.2);state.intensity=.7;state.screenShake=.15;}
  if(state.horrorBeat===1&&state.elapsed>10.5){state.horrorBeat=2;activateMonster();toast('SOMETHING BETWEEN THE TREES JUST MOVED.',3.1);}
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
  ctx.save();
  ctx.lineCap='round';
  ctx.lineJoin='round';
  for(const p of roadNetworks()){
    ctx.beginPath();
    ctx.moveTo(p[0].x-camera.x+shakeX,p[0].y-camera.y+shakeY);
    for(let i=1;i<p.length;i++)ctx.lineTo(p[i].x-camera.x+shakeX,p[i].y-camera.y+shakeY);
    ctx.lineWidth=106;ctx.strokeStyle='#080d0a';ctx.stroke();
    ctx.lineWidth=96;ctx.strokeStyle='#272c24';ctx.stroke();
    ctx.lineWidth=84;ctx.strokeStyle='#353a30';ctx.stroke();
    ctx.lineWidth=78;ctx.strokeStyle='#414337';ctx.stroke();
    ctx.lineWidth=2;ctx.strokeStyle='#8f8567';ctx.setLineDash([18,23]);ctx.stroke();ctx.setLineDash([]);
  }
  ctx.restore();
  for(let i=0;i<60;i++){
    const wx=130+(i*173)%3000;
    const wy=75+(i*197)%2350;
    if(roadDistance(wx,wy)<49){
      const x=wx-camera.x+shakeX;
      const y=wy-camera.y+shakeY;
      if(x>-40&&x<W+40&&y>-30&&y<H+30){
        px(x-10,y,22,3,'#222920');px(x-5,y+1,12,1,'#716c55');
        if(i%3===0){px(x+7,y-4,2,8,'#343c2f');px(x+4,y-7,8,4,'#a6a085');}
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
  if(o.style==='motel'){
    px(x-w*.43,y-h/2+4,w*.86,10,'#673b32');px(x-w*.36,y-h/2+7,w*.72,3,'#b48e63');
    px(x-w*.12,y-h/2-27,w*.24,13,'#111a14');px(x-w*.105,y-h/2-24,w*.21,7,Math.sin(state.elapsed*7)>0?'#d45f4b':'#7d342d');
    ctx.fillStyle='#e0b876';ctx.font='bold 8px monospace';ctx.fillText('VACANCY',x,y-h/2-18);
  }
  if(o.style==='diner'){
    px(x-w*.48,y-h/2+5,w*.96,13,'#5d302a');px(x-w*.44,y-h/2+8,w*.88,4,'#c4a66c');
    for(let i=0;i<5;i++)px(x-w*.36+i*w*.18,y+h*.04,Math.max(6,w*.065),h*.12,'#a46d43');
    ctx.fillStyle='#e2c17b';ctx.font='bold 8px monospace';ctx.fillText('LAST STOP',x,y-h/2-17);
  }
  if(o.style==='clinic'){
    px(x-5,y-h/2-25,10,32,'#a8b6a3');px(x-16,y-h/2-15,32,10,'#a8b6a3');
    px(x-w*.34,y+h*.06,w*.19,h*.18,'#172c2c');px(x-w*.31,y+h*.09,w*.13,h*.12,'#688a81');
  }
  if(o.style==='depot'||o.style==='warehouse'){
    px(x-w*.34,y-h/2+18,w*.68,h*.44,'#171e18');px(x-w*.29,y-h/2+23,w*.58,h*.35,'#29362c');
    for(let i=0;i<5;i++)px(x-w*.26+i*w*.105,y-h/2+23,2,h*.35,'#4e5947');
    px(x-w*.38,y-h/2+3,w*.76,5,'#8a7652');
  }
  if(o.style==='chapel'){
    poly([[x-w*.28,y-h/2+5],[x,y-h/2-29],[x+w*.28,y-h/2+5]],'#35392d');
    px(x-4,y-h/2-21,8,19,'#b1aa89');px(x-2,y-h/2-18,4,13,'#343a2c');
    px(x-4,y-h/2-13,8,3,'#b7aa81');
  }
  if(o.style==='farmhouse'){
    poly([[x-w*.52,y-h/2+7],[x,y-h/2-23],[x+w*.52,y-h/2+7]],'#4f342b');
    px(x-18,y-h/2+3,36,7,'#6c4937');px(x+16,y-h/2-17,9,24,'#342e25');
    if(Math.sin(state.elapsed*2.1+o.x)>.75)px(x+w*.18,y-h/2+17,15,13,'#c99c55');
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
  if(x<-140||y<-150||x>W+140||y>H+150)return;
  const bob=monster.frozenByLight?0:Math.sin(monster.phase*3.7)*3;
  const twitch=monster.frozenByLight?0:Math.sin(monster.phase*15)*1.8;
  const lurch=monster.stun>0||monster.frozenByLight?0:Math.sin(monster.phase*8)*2;
  ctx.save();
  ctx.globalAlpha=monster.stun>0?.72:1;
  ctx.fillStyle='rgba(0,0,0,.6)';
  ctx.beginPath();
  ctx.ellipse(x,y+28,29,8,0,0,Math.PI*2);
  ctx.fill();
  px(x-17,y-28+bob,34,50,'#040504');
  px(x-14,y-47+bob,28,25,'#070807');
  px(x-10,y-61+bob,20,18,'#050605');
  px(x-7,y-65+bob,14,7,'#080908');
  px(x-20,y-24+bob,7,37,'#050605');
  px(x+13,y-25+bob,7,38,'#050605');
  px(x-24-twitch,y-3+bob,6,25,'#060706');
  px(x+18+twitch,y-1+bob,6,27,'#060706');
  px(x-15,y+17,10,28,'#050605');
  px(x+5,y+17,10,28,'#050605');
  px(x-12,y+40,10,5,'#090a08');
  px(x+4,y+40,10,5,'#090a08');
  px(x-12,y-43+bob,24,7,'#10120f');
  px(x-9,y-38+bob,18,4,'#1c1c17');
  px(x-8,y-38+bob,5,3,monster.frozenByLight?'#fff4cf':'#f4d5a3');
  px(x+3,y-38+bob,5,3,monster.frozenByLight?'#fff4cf':'#f4d5a3');
  px(x-7,y-37+bob,3,2,monster.frozenByLight?'#ff4b43':'#b8322b');
  px(x+4,y-37+bob,3,2,monster.frozenByLight?'#ff4b43':'#b8322b');
  px(x-5,y-29+bob,10,3,'#4b2220');
  px(x-7,y-27+bob,14,3,'#ddd1b7');
  px(x-4,y-27+bob,2,3,'#161512');
  px(x+1,y-27+bob,2,3,'#161512');
  px(x-9,y-19+bob,18,2,'#28231e');
  px(x-6,y-14+bob,12,2,'#191a15');
  px(x-16,y-4+bob,4,11,'#28221b');
  px(x+12,y-3+bob,4,11,'#28221b');
  for(let i=0;i<4;i++){
    px(x-25+i*2+twitch,y+18+i%2*3,2,7,'#0a0b09');
    px(x+20+i*2-twitch,y+18+i%2*3,2,7,'#0a0b09');
  }
  ctx.globalAlpha=1;
  if(monster.stun>0){
    px(x-22,y-72,44,2,'#dfc789');
    px(x-11,y-69,22,2,'#9e8a56');
  }
  const d=dist(player.x,player.y,monster.x,monster.y);
  if(d<300){
    ctx.strokeStyle='rgba(174,38,35,'+(.08+.06*(.5+.5*Math.sin(monster.phase*9)))+')';
    ctx.lineWidth=2;
    ctx.beginPath();
    ctx.ellipse(x,y+2,23+lurch,39,0,0,Math.PI*2);
    ctx.stroke();
  }
  ctx.restore();
}
function drawPatrolSirenWorldGlow(){
  const x=245-camera.x+shakeX;
  const y=278-camera.y+shakeY;
  if(x<-140||y<-140||x>W+140||y>H+140)return;
  const redOn=Math.sin(state.elapsed*13)>0;
  const lights=[{x:x-3,y:y-18,color:redOn?'rgba(247,43,50,.46)':'rgba(36,80,228,.12)'},{x:x+3,y:y-18,color:redOn?'rgba(36,80,228,.12)':'rgba(247,43,50,.46)'}];
  ctx.save();ctx.globalCompositeOperation='screen';
  for(const light of lights){
    const g=ctx.createRadialGradient(light.x,light.y,0,light.x,light.y,75);
    g.addColorStop(0,light.color);g.addColorStop(1,'rgba(0,0,0,0)');
    ctx.fillStyle=g;ctx.fillRect(light.x-75,light.y-75,150,150);
  }
  ctx.restore();
}
function drawPlayer(){
  const x=player.x-camera.x+shakeX;
  const y=player.y-camera.y+shakeY;
  const spec=specs[state.selectedCharacter];
  const leg=player.moving?Math.sin(player.step)*4:0;
  const bob=player.moving?Math.abs(Math.sin(player.step*2))*1.65:Math.sin(state.elapsed*1.7)*.45;
  const lean=player.moving?Math.sin(player.step)*.035:0;
  ctx.save();
  ctx.translate(Math.round(x),Math.round(y-bob));
  ctx.rotate(lean);
  ctx.rotate(player.angle);
  if(player.invulnerable>0&&Math.floor(state.elapsed*24)%2===0)ctx.globalAlpha=.5;
  px(-9,-8,18,17,'#080d0a');
  px(-7,-7,14,14,spec.color);
  px(-11,-6+leg*.22,5,11,spec.color);
  px(6,-6-leg*.22,5,11,spec.color);
  px(-7,-13,14,6,'#20261d');
  px(-6,-15,12,5,spec.shirt);
  px(-5,-16,10,3,'#c1b180');
  px(-7,7+leg,5,7,'#2b2c24');
  px(2,7-leg,5,7,'#2b2c24');
  px(2,-3,17,4,'#0b0e0b');
  px(15,-4,5,3,'#c9c5ac');
  px(-3,-2,4,3,'#e4d0a0');
  if(state.selectedCharacter==='hugo'){
    px(-6,-17,12,3,'#28241c');
    px(-5,-14,10,2,'#b5a16e');
    px(-2,-3,3,3,'#d4c7a5');
  }
  if(state.selectedCharacter==='yumi'){
    px(-8,-17,16,5,'#201816');
    px(-9,-13,3,12,'#201816');
    px(6,-13,3,12,'#201816');
    px(-4,-14,8,3,'#b8a5a0');
    px(-2,-3,3,3,'#d4c7a5');
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
function flashlightAngle(){
  if(!player)return 0;
  if(state.controlMode==='mobile')return player.angle||0;
  const target=worldCoordinates(pointer.x,pointer.y);
  const dx=target.x-player.x;
  const dy=target.y-player.y;
  if(Math.hypot(dx,dy)<24)return player.angle||0;
  return angleTo(player.x,player.y,target.x,target.y);
}
function drawMaskCone(x,y,angle,reach,halfAngle,ambientAlpha,haloRadius){
  const l=lightCtx;
  l.save();
  l.setTransform(dpr,0,0,dpr,0,0);
  l.clearRect(0,0,W,H);
  l.globalCompositeOperation='source-over';
  l.fillStyle='rgba(0,0,0,'+ambientAlpha+')';
  l.fillRect(0,0,W,H);
  l.globalCompositeOperation='destination-out';
  const halo=l.createRadialGradient(x,y,0,x,y,haloRadius);
  halo.addColorStop(0,'rgba(0,0,0,.96)');
  halo.addColorStop(.50,'rgba(0,0,0,.83)');
  halo.addColorStop(1,'rgba(0,0,0,0)');
  l.fillStyle=halo;
  l.beginPath();
  l.arc(x,y,haloRadius,0,Math.PI*2);
  l.fill();
  if(flashlight&&flashlightBattery>0){
    l.save();
    l.beginPath();
    l.moveTo(x,y);
    l.arc(x,y,reach,angle-halfAngle,angle+halfAngle);
    l.closePath();
    l.clip();
    const beam=l.createRadialGradient(x,y,5,x,y,reach);
    beam.addColorStop(0,'rgba(0,0,0,1)');
    beam.addColorStop(.61,'rgba(0,0,0,1)');
    beam.addColorStop(.79,'rgba(0,0,0,.995)');
    beam.addColorStop(.92,'rgba(0,0,0,.83)');
    beam.addColorStop(1,'rgba(0,0,0,0)');
    l.fillStyle=beam;
    l.fillRect(x-reach,y-reach,reach*2,reach*2);
    l.restore();
    l.save();
    l.globalCompositeOperation='source-over';
    l.beginPath();
    l.moveTo(x,y);
    l.arc(x,y,reach,angle-halfAngle,angle+halfAngle);
    l.closePath();
    l.clip();
    const glow=l.createRadialGradient(x,y,9,x,y,reach);
    glow.addColorStop(0,'rgba(216,230,191,.12)');
    glow.addColorStop(.17,'rgba(197,218,180,.075)');
    glow.addColorStop(.55,'rgba(177,202,158,.04)');
    glow.addColorStop(.86,'rgba(159,186,146,.018)');
    glow.addColorStop(1,'rgba(159,186,146,0)');
    l.fillStyle=glow;
    l.fillRect(x-reach,y-reach,reach*2,reach*2);
    l.restore();
  }
  l.restore();
  ctx.save();
  ctx.globalCompositeOperation='source-over';
  ctx.drawImage(lightCanvas,0,0,W,H);
  ctx.restore();
}
function drawLighting(){
  const x=player.x-camera.x+shakeX;
  const y=player.y-camera.y+shakeY;
  const working=flashlight&&flashlightBattery>0;
  const angle=flashlightAngle();
  const flicker=working&&state.intensity>.38&&((state.elapsed%8)<.065||((state.elapsed%8)>1.1&&(state.elapsed%8)<1.16));
  drawMaskCone(x,y,angle,flicker?92:510,.245,state.lightning>0?.16:.997,working?23:5);
  if(state.lightning>0){
    ctx.fillStyle='rgba(191,211,204,'+Math.min(.84,state.lightning*1.15)+')';
    ctx.fillRect(0,0,W,H);
    ctx.fillStyle='rgba(0,0,0,.22)';
    ctx.fillRect(0,0,W,H);
  }
  const vignette=ctx.createRadialGradient(W/2,H/2,Math.min(W,H)*.18,W/2,H/2,Math.max(W,H)*.78);
  vignette.addColorStop(0,'rgba(0,0,0,0)');
  vignette.addColorStop(.63,'rgba(0,0,0,.09)');
  vignette.addColorStop(1,'rgba(0,0,0,.58)');
  ctx.fillStyle=vignette;
  ctx.fillRect(0,0,W,H);
  if(monster&&monster.active){
    const d=dist(player.x,player.y,monster.x,monster.y);
    if(d<285){
      const panic=.035+.045*(.5+.5*Math.sin(state.elapsed*10));
      ctx.fillStyle='rgba(112,4,7,'+panic+')';
      ctx.fillRect(0,0,W,H);
      if(d<145&&Math.sin(state.elapsed*18)>.92){
        ctx.fillStyle='rgba(210,220,196,.035)';
        ctx.fillRect(0,0,W,H);
      }
    }
  }
}

function drawWorld(){
  if(state.prologueStage!=='swamp'){drawPrologue();return;}
  screenJitter();
  if(state.floor==='inside'){
    drawInterior();
    drawSurvivors();
    drawPlayer();
    drawBulletEffects();
    drawLightingInterior();
    drawMini();
    if(state.sceneFade>0){ctx.fillStyle='rgba(0,0,0,'+state.sceneFade+')';ctx.fillRect(0,0,W,H);}
    return;
  }
  drawGround();
  drawPuddles();
  drawRoad();
  drawReeds();
  for(const t of trees)drawTree(t);
  drawPatrolCarWorld();
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
  drawRain();
  drawLighting();
  drawPatrolSirenWorldGlow();
  drawMini();
  if(state.sceneFade>0){ctx.fillStyle='rgba(0,0,0,'+state.sceneFade+')';ctx.fillRect(0,0,W,H);}
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
  const working=flashlight&&flashlightBattery>0;
  const angle=flashlightAngle();
  drawMaskCone(x,y,angle,working?355:1,.26,.998,working?18:4);
  const flicker=working&&state.intensity>.38&&((state.elapsed%8)<.065||((state.elapsed%8)>1.1&&(state.elapsed%8)<1.16));
  if(flicker){
    ctx.fillStyle='rgba(0,0,0,.62)';
    ctx.fillRect(0,0,W,H);
  }
  if(monster&&monster.active){
    const d=dist(player.x,player.y,monster.x,monster.y);
    if(d<260){
      ctx.fillStyle='rgba(100,0,5,'+(0.025+.035*(.5+.5*Math.sin(state.elapsed*11)))+')';
      ctx.fillRect(0,0,W,H);
    }
  }
  const vignette=ctx.createRadialGradient(W/2,H/2,Math.min(W,H)*.18,W/2,H/2,Math.max(W,H)*.8);
  vignette.addColorStop(0,'rgba(0,0,0,0)');
  vignette.addColorStop(.62,'rgba(0,0,0,.08)');
  vignette.addColorStop(1,'rgba(0,0,0,.56)');
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
  mctx.lineWidth=3;
  for(const points of roadNetworks()){
    mctx.beginPath();
    mctx.moveTo(points[0].x/WORLD.w*mw,points[0].y/WORLD.h*mh);
    for(let i=1;i<points.length;i++)mctx.lineTo(points[i].x/WORLD.w*mw,points[i].y/WORLD.h*mh);
    mctx.stroke();
  }
  for(const o of objects){
    if(o.type!=='building')continue;
    const bx=o.x/WORLD.w*mw,by=o.y/WORLD.h*mh;
    mctx.fillStyle='#a0a18a';mctx.fillRect(bx-2,by-2,4,4);
  }
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
  const ids=['charArt0','charArt1'];
  const keys=['hugo','yumi'];
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
    if(spec.gender==='male'){
      g.fillStyle=spec.hair;
      g.fillRect(21,10,22,7);
      g.fillRect(19,14,5,8);
      g.fillRect(40,14,5,8);
      g.fillStyle='#b5a16e';
      g.fillRect(21,18,22,3);
      g.fillStyle='#d2b975';
    }else{
      g.fillStyle=spec.hair;
      g.fillRect(20,9,24,9);
      g.fillRect(18,14,6,23);
      g.fillRect(40,14,6,23);
      g.fillRect(23,8,18,4);
      g.fillStyle='#c7b5a1';
      g.fillRect(22,18,20,3);
      g.fillStyle='#d2b975';
    }
    g.fillStyle='#d2b975';
    g.fillRect(12,36,5,10);
    g.fillRect(47,36,5,10);
    if(index===0){
      g.fillStyle='#d4bb76';
      g.fillRect(21,20,22,3);
      g.fillStyle='#6b7858';
      g.fillRect(17,25,30,4);
      g.fillStyle='#d6c18b';
      g.fillRect(29,32,6,5);
    }
    if(index===1){
      g.fillStyle='#626e58';
      g.fillRect(22,14,20,6);
      g.fillRect(20,19,24,4);
      g.fillStyle='#c9b6a0';
      g.fillRect(22,24,20,3);
      g.fillStyle='#d6c18b';
      g.fillRect(29,32,6,5);
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
    if(state.prologueStage==='call'){acceptDispatch();return;}
    if(state.prologueStage==='arrival'){exitPatrolCar();return;}
    if(state.prologueStage==='drive')return;
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
    hugo:'Boy character. Officer Hugo is a dependable male state trooper with balanced speed, health, and stamina.',
    yumi:'Girl character. Officer Yumi is a quick female investigator with faster movement and longer stamina.'
  };
  $('characterDetails').innerHTML='<b>'+(state.pendingCharacter==='hugo'?'BOY · ':'GIRL · ')+escapeHTML(spec.name.toUpperCase())+'</b><br>'+escapeHTML(messages[state.pendingCharacter])+'<br><br>Speed: '+spec.speed+' · Max health: '+spec.hp+' · Starting ammo: '+spec.ammo+' + '+spec.reserve+' spare';
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
  if(state.prologueStage==='call'&&(key==='e'||key==='enter')){acceptDispatch();return;}
  if(state.prologueStage==='arrival'&&(key==='e'||key==='enter')){exitPatrolCar();return;}
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
