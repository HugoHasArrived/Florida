
import os
from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

PAGE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<title>Florida Shadows | State Trooper Horror Files</title>
<style>
:root{--red:#b82e35;--gold:#d6b66d;--panel:#101411;--muted:#89928b}
*{box-sizing:border-box}
body{margin:0;background:#050706;color:#e6e7df;font-family:Consolas,monospace;overflow:hidden}
button{font:inherit;cursor:pointer;color:#eee;background:#171d19;border:1px solid #59645a;padding:12px 18px}
button:hover{background:#29372c;border-color:#d6b66d}
#game{position:fixed;inset:0;width:100%;height:100%;image-rendering:pixelated;background:#080b09}
.overlay{position:fixed;inset:0;display:flex;align-items:center;justify-content:center;background:radial-gradient(ellipse,#121a15d9,#020303f5);z-index:3;padding:18px}
.card{width:min(700px,96vw);max-height:94vh;overflow:auto;background:#090d0bf2;border:1px solid #414b42;padding:clamp(18px,4vw,36px);box-shadow:0 0 55px #000}
.kicker{color:var(--red);letter-spacing:4px;font-size:12px}
h1{font-size:clamp(35px,8vw,70px);line-height:.95;margin:15px 0;color:#eee;text-shadow:4px 4px #552124}
h2{color:var(--gold);margin-top:0}
p{line-height:1.65;color:#b8c0b8}
.small{font-size:12px;color:#8d978e;line-height:1.7}
.actions{display:flex;gap:10px;flex-wrap:wrap;margin-top:22px}
.primary{background:#77272c;border-color:#bd5555}
#hud{position:fixed;inset:0;pointer-events:none;display:none}
.hudbox{position:absolute;background:#090d0bd9;border:1px solid #354038;padding:10px 13px;font-size:12px;line-height:1.7}
#status{left:14px;top:14px;min-width:185px}
#objectives{right:14px;top:14px;width:min(270px,48vw)}
#hint{position:absolute;left:50%;bottom:12%;transform:translateX(-50%);background:#070908e8;border:1px solid #68736a;padding:12px 18px;text-align:center;min-width:220px}
#message{position:absolute;left:50%;top:20%;transform:translateX(-50%);max-width:85vw;color:#f1dca4;text-shadow:1px 2px #000;text-align:center}
.bar{height:6px;background:#333;margin-top:4px;width:150px}
.bar span{display:block;height:100%;background:#a83b3f;width:100%}
#touch{display:none;position:fixed;bottom:18px;left:16px;right:16px;z-index:2;justify-content:space-between;pointer-events:none}
.pad{display:grid;grid-template-columns:repeat(3,44px);gap:4px;pointer-events:auto}
.pad button,.touchactions button{background:#101611bb;padding:12px 0;min-width:42px}
.touchactions{display:flex;align-items:end;gap:5px;pointer-events:auto}
#crosshair{position:absolute;left:50%;top:50%;width:8px;height:8px;border:1px solid #d9dfc4;border-radius:50%;opacity:.65}
@media(max-width:700px){#touch{display:flex}#objectives{top:auto;bottom:12px;right:10px;width:145px;font-size:10px}#status{font-size:10px}#hint{bottom:100px}}
</style>
</head>
<body>
<canvas id="game"></canvas>

<div class="overlay" id="menu">
 <div class="card">
  <div class="kicker">FLORIDA • INCIDENT REPORT 09-17</div>
  <h1>FLORIDA<br>SHADOWS</h1>
  <h2>STATE TROOPER HORROR FILES</h2>
  <p>One abandoned highway. One unanswered radio call. Something in the swamp knows your name.</p>
  <p class="small">A fictional pixel-art survival horror game. Explore the roadside, investigate evidence, manage your flashlight, and survive whatever is following you.</p>
  <div class="actions">
   <button class="primary" onclick="startGame()">▶ BEGIN PATROL</button>
   <button onclick="showHelp()">FIELD MANUAL</button>
   <button onclick="showCredits()">CREDITS</button>
  </div>
  <p class="small">FICTIONAL GAME • No real location, camera, microphone, or IP data is accessed or transmitted by this game.</p>
 </div>
</div>

<div class="overlay" id="panel" style="display:none">
 <div class="card">
  <div id="panelcontent"></div>
  <div class="actions"><button class="primary" onclick="closePanel()">RETURN TO GAME</button></div>
 </div>
</div>

<div id="hud">
 <div class="hudbox" id="status">
  <div>UNIT 07 — NIGHT SHIFT</div>
  <div id="healthlabel">CONDITION: STABLE</div>
  <div class="bar"><span id="healthbar"></span></div>
  <div id="flashlabel">FLASHLIGHT: 100%</div>
  <div class="bar"><span id="flashbar" style="background:#d6b66d"></span></div>
  <div id="ammo">AMMO: 6</div>
 </div>
 <div class="hudbox" id="objectives"><b style="color:#d6b66d">CASE OBJECTIVES</b><div id="objectiveList"></div></div>
 <div id="hint">WASD to move • E to investigate</div>
 <div id="message"></div><div id="crosshair"></div>
</div>

<div id="touch">
 <div class="pad">
  <span></span><button data-key="w">▲</button><span></span>
  <button data-key="a">◀</button><button data-key="s">▼</button><button data-key="d">▶</button>
 </div>
 <div class="touchactions">
  <button onclick="interact()">INSPECT</button>
  <button onclick="shoot()">FIRE</button>
  <button onclick="toggleFlash()">LIGHT</button>
 </div>
</div>

<script>
"use strict";
const canvas=document.getElementById("game");
const ctx=canvas.getContext("2d");
let W=innerWidth,H=innerHeight,dpr=1;
function resize(){
 dpr=Math.min(devicePixelRatio||1,2);
 W=innerWidth;H=innerHeight;
 canvas.width=Math.floor(W*dpr);canvas.height=Math.floor(H*dpr);
 canvas.style.width=W+"px";canvas.style.height=H+"px";
 ctx.setTransform(dpr,0,0,dpr,0,0);
}
addEventListener("resize",resize);resize();

const keys={};
let state="menu",last=0,elapsed=0,flashOn=true,messageTimer=0;
let health=100,battery=100,ammo=6,evidence=0,radioFound=false,carFound=false,escaped=false;
let player={x:210,y:210,speed:125,face:0};
let world={w:2400,h:1800};
let camera={x:0,y:0};
let objects=[],monsters=[],particles=[];
let objectiveText=[];
const rand=(a,b)=>a+Math.random()*(b-a);
const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
const dist=(a,b)=>Math.hypot(a.x-b.x,a.y-b.y);

function buildWorld(){
 objects=[
  {x:250,y:210,w:100,h:60,type:"patrol",name:"Abandoned patrol car",desc:"Unit 07 is here. The driver door is open. The radio is still receiving a signal.",done:false},
  {x:510,y:360,w:55,h:45,type:"evidence",name:"Bloody footprints",desc:"Fresh footprints lead away from the highway and into the trees.",done:false},
  {x:870,y:280,w:90,h:70,type:"building",name:"Closed roadside motel",desc:"The office door hangs open. A generator rattles behind the building.",done:false},
  {x:1010,y:410,w:50,h:45,type:"evidence",name:"Motel guest ledger",desc:"Several names have been scratched out. The final entry reads: 'DON'T ANSWER THE RADIO.'",done:false},
  {x:1450,y:650,w:75,h:65,type:"tower",name:"Emergency relay tower",desc:"The relay tower could restore your radio. Something is moving below the stairs.",done:false},
  {x:1790,y:1160,w:80,h:65,type:"exit",name:"County road checkpoint",desc:"The road is blocked. You need the radio evidence before calling for help.",done:false},
  {x:680,y:990,w:55,h:45,type:"evidence",name:"Discarded field recorder",desc:"A recording plays: 'Trooper, if you hear this, it is already behind you.'",done:false},
  {x:1220,y:1150,w:65,h:55,type:"evidence",name:"Mud-covered boot print",desc:"The print is much larger than a human boot. It points toward the tower.",done:false}
 ];
 monsters=[
  {x:700,y:500,speed:40,awake:true,phase:rand(0,6),hit:0},
  {x:1300,y:850,speed:34,awake:false,phase:rand(0,6),hit:0},
  {x:1770,y:990,speed:48,awake:false,phase:rand(0,6),hit:0}
 ];
}
buildWorld();

function startGame(){
 document.getElementById("menu").style.display="none";
 document.getElementById("panel").style.display="none";
 document.getElementById("hud").style.display="block";
 state="playing";last=performance.now();
 say("Dispatch: Unit 07, report to the roadside motel. Do you copy?");
 updateObjectives();
}
function showHelp(){
 showPanel("<div class='kicker'>FIELD MANUAL</div><h2>Controls & Survival</h2><p><b>W A S D / Arrow keys</b> — Move<br><b>Shift</b> — Sprint<br><b>E</b> — Investigate nearby objects<br><b>F</b> — Toggle flashlight<br><b>Space / Click</b> — Fire service weapon<br><b>R</b> — Reload<br><b>Tab</b> — Show objectives<br><b>Esc</b> — Pause</p><p>Your flashlight drains while on. Evidence is more important than ammunition. If the thing finds you, keep moving.</p>");
}
function showCredits(){
 showPanel("<div class='kicker'>CASE FILE FOOTER</div><h2>Credits</h2><p>Florida Shadows — State Trooper Horror Files</p><p>Created as a fictional pixel-art horror experience. All locations, incidents, and characters are fictional.</p><p class='small'>No real emergency service is contacted. This game does not request your device location or access your camera or microphone.</p>");
}
function showPanel(html){
 state="panel";document.getElementById("panelcontent").innerHTML=html;
 document.getElementById("panel").style.display="flex";
}
function closePanel(){
 document.getElementById("panel").style.display="none";
 if(state==="panel")state="playing";
}
function say(text,time=4){
 document.getElementById("message").textContent=text;messageTimer=time;
}
function updateObjectives(){
 const list=[
  [carFound,"Inspect the abandoned patrol car"],
  [evidence>=1,"Find roadside evidence"],
  [radioFound,"Restore the emergency radio"],
  [evidence>=3,"Collect 3 pieces of evidence"],
  [escaped,"Reach the county road checkpoint"]
 ];
 document.getElementById("objectiveList").innerHTML=list.map(([done,t])=>
  `<div style="margin-top:5px;color:${done?"#9eaa91":"#c1c7bf"}">${done?"[✓]":"[ ]"} ${t}</div>`).join("");
}
function nearestObject(){
 let best=null,bd=Infinity;
 for(const o of objects){
  if(o.done)continue;
  let d=dist(player,{x:o.x+o.w/2,y:o.y+o.h/2});
  if(d<bd){bd=d;best=o;}
 }
 return bd<85?best:null;
}
function interact(){
 if(state!=="playing")return;
 const o=nearestObject();
 if(!o){say("Nothing nearby. Listen to the radio and follow the evidence.");return;}
 if(o.type==="patrol"){
  carFound=true;
  showPanel("<div class='kicker'>EVIDENCE LOG 001</div><h2>Abandoned patrol car</h2><p>The engine is cold, but the radio is warm. There are scratches on the inside of the windshield.</p><p>The glove compartment contains a spare magazine and a torn incident report.</p><p><b>Radio:</b> A broken signal repeats from somewhere near the motel and relay tower.</p>");
  if(!o.done){ammo=Math.min(12,ammo+3);o.done=true;}
 }else if(o.type==="evidence"){
  evidence++;o.done=true;
  showPanel(`<div class='kicker'>EVIDENCE LOG ${String(evidence).padStart(3,"0")}</div><h2>${o.name}</h2><p>${o.desc}</p><p>Evidence collected: ${evidence}/3</p>`);
 }else if(o.type==="building"){
  showPanel("<div class='kicker'>LOCATION REPORT</div><h2>Roadside motel</h2><p>The building is silent. A room key is on the counter. The guest ledger may explain why every room was abandoned.</p><p>You hear a slow dragging sound upstairs. There are no safe rooms here.</p>");
  if(!o.done){o.done=true;battery=Math.min(100,battery+12);}
 }else if(o.type==="tower"){
  radioFound=true;o.done=true;
  showPanel("<div class='kicker'>RADIO LINK RESTORED</div><h2>Emergency relay tower</h2><p>The receiver crackles back to life.</p><p><b>Dispatch:</b> Unit 07, your transmission is breaking up. Do not approach the tree line. Repeat, do not—</p><p>A second voice whispers your name through the static.</p>");
  for(const m of monsters)m.awake=true;
 }else if(o.type==="exit"){
  if(radioFound&&evidence>=3){
   escaped=true;state="won";
   showPanel("<div class='kicker'>CASE STATUS: SURVIVED</div><h2>Transmission Received</h2><p>Your emergency call finally reaches dispatch. Headlights appear beyond the barricade.</p><p>As the rescue vehicle stops, your radio whispers: 'This was only the first county.'</p><p><b>Evidence collected:</b> "+evidence+"</p><div class='actions'><button class='primary' onclick='location.reload()'>PLAY AGAIN</button></div>");
  }else{
   say("Checkpoint locked. Restore the relay and collect at least 3 evidence items.");
  }
 }
 updateObjectives();
}
function toggleFlash(){
 if(state==="playing")flashOn=!flashOn;
}
function shoot(){
 if(state!=="playing"||ammo<=0){say("No ammunition. Press R to reload.");return;}
 ammo--;say("BANG!",0.7);
 let target=null,bd=260;
 for(const m of monsters){
  const d=dist(player,m);
  if(d<bd){let angle=Math.atan2(m.y-player.y,m.x-player.x);
   let diff=Math.atan2(Math.sin(angle-player.face),Math.cos(angle-player.face));
   if(Math.abs(diff)<0.38){target=m;bd=d;}
  }
 }
 if(target){target.hit=1.2;target.awake=false;say("The shape collapses into the darkness.");}
}
function reload(){if(state==="playing"){ammo=6;say("Magazine changed.");}}
addEventListener("keydown",e=>{
 const k=e.key.toLowerCase();keys[k]=true;
 if([" ","arrowup","arrowdown","arrowleft","arrowright","tab"].includes(k))e.preventDefault();
 if(k==="e")interact();
 if(k==="f")toggleFlash();
 if(k===" " )shoot();
 if(k==="r")reload();
 if(k==="escape"&&state==="playing"){
  showPanel("<div class='kicker'>PAUSED</div><h2>Patrol Suspended</h2><p>Listen carefully before moving again.</p><button onclick='closePanel()'>RESUME PATROL</button>");
 }
 if(k==="tab"&&state==="playing"){
  say("Objectives: investigate the patrol car, collect 3 evidence items, restore the relay, then reach the checkpoint.",5);
 }
});
addEventListener("keyup",e=>keys[e.key.toLowerCase()]=false);
canvas.addEventListener("click",()=>{if(state==="playing")shoot();});
document.querySelectorAll("[data-key]").forEach(b=>{
 const k=b.dataset.key;
 b.addEventListener("pointerdown",e=>{e.preventDefault();keys[k]=true;});
 ["pointerup","pointerleave","pointercancel"].forEach(ev=>b.addEventListener(ev,()=>keys[k]=false));
});

function blocked(x,y){
 if(x<20||y<20||x>world.w-20||y>world.h-20)return true;
 for(const o of objects){
  if(["patrol","building","tower","exit"].includes(o.type)){
   if(x>o.x-16&&x<o.x+o.w+16&&y>o.y-16&&y<o.y+o.h+16)return true;
  }
 }
 return false;
}
function update(dt){
 if(state!=="playing")return;
 elapsed+=dt;
 if(messageTimer>0){messageTimer-=dt;if(messageTimer<=0)document.getElementById("message").textContent="";}
 let dx=0,dy=0;
 if(keys.w||keys.arrowup)dy--;
 if(keys.s||keys.arrowdown)dy++;
 if(keys.a||keys.arrowleft)dx--;
 if(keys.d||keys.arrowright)dx++;
 const len=Math.hypot(dx,dy)||1;
 const moving=dx!==0||dy!==0;
 const sprint=keys.shift&&moving;
 const speed=player.speed*(sprint?1.55:1);
 dx=dx/len*speed*dt;dy=dy/len*speed*dt;
 if(moving)player.face=Math.atan2(dy,dx);
 if(!blocked(player.x+dx,player.y))player.x+=dx;
 if(!blocked(player.x,player.y+dy))player.y+=dy;
 if(flashOn)battery=Math.max(0,battery-dt*1.25);
 else battery=Math.min(100,battery+dt*2);
 if(battery<=0)flashOn=false;

 for(const m of monsters){
  if(m.hit>0){m.hit-=dt;continue;}
  const d=dist(player,m);
  if(d<390)m.awake=true;
  if(m.awake&&d<520){
   const a=Math.atan2(player.y-m.y,player.x-m.x);
   const sp=m.speed*(d<130?1.18:1);
   const mx=Math.cos(a)*sp*dt,my=Math.sin(a)*sp*dt;
   if(!blocked(m.x+mx,m.y))m.x+=mx;
   if(!blocked(m.x,m.y+my))m.y+=my;
   if(d<28){health-=dt*19;if(health<=0){
    health=0;state="dead";
    showPanel("<div class='kicker'>UNIT 07 — NO RESPONSE</div><h2>Officer Down</h2><p>The radio keeps transmitting long after the flashlight goes out.</p><button class='primary' onclick='location.reload()'>RESTART SHIFT</button>");
   }}
  }
 }
 camera.x=clamp(player.x-W/2,0,world.w-W);
 camera.y=clamp(player.y-H/2,0,world.h-H);
 const o=nearestObject();
 document.getElementById("hint").textContent=o?"[E] INVESTIGATE: "+o.name:"WASD MOVE • SHIFT SPRINT • E INVESTIGATE • F FLASHLIGHT • SPACE FIRE";
 document.getElementById("healthbar").style.width=health+"%";
 document.getElementById("healthlabel").textContent="CONDITION: "+(health>65?"STABLE":health>30?"INJURED":"CRITICAL");
 document.getElementById("flashbar").style.width=battery+"%";
 document.getElementById("flashlabel").textContent="FLASHLIGHT: "+Math.round(battery)+"% "+(flashOn?"ON":"OFF");
 document.getElementById("ammo").textContent="AMMO: "+ammo+" | EVIDENCE: "+evidence+"/3";
}
function rect(x,y,w,h,c){ctx.fillStyle=c;ctx.fillRect(Math.round(x),Math.round(y),w,h);}
function text(t,x,y,c="#b7bcae",size=12){ctx.fillStyle=c;ctx.font=size+"px Consolas,monospace";ctx.fillText(t,x,y);}
function drawWorld(){
 ctx.fillStyle="#080c09";ctx.fillRect(0,0,W,H);
 ctx.save();ctx.translate(-camera.x,-camera.y);
 rect(0,0,world.w,world.h,"#111812");
 // Ground tiles and wet swamp patches
 for(let y=0;y<world.h;y+=32)for(let x=0;x<world.w;x+=32){
  const n=(Math.sin(x*12.9+y*3.7)*43758.5)%1;
  rect(x,y,30,30,n>.3?"#121a13":"#101610");
  if((x*3+y*7)%11===0)rect(x+7,y+11,2,2,"#293327");
 }
 // Winding highway
 ctx.strokeStyle="#303431";ctx.lineWidth=95;ctx.beginPath();
 ctx.moveTo(70,80);ctx.lineTo(360,300);ctx.lineTo(720,410);ctx.lineTo(1030,650);ctx.lineTo(1270,880);ctx.lineTo(1630,1020);ctx.lineTo(1900,1320);ctx.stroke();
 ctx.strokeStyle="#9b9477";ctx.lineWidth=2;ctx.setLineDash([25,25]);ctx.beginPath();
 ctx.moveTo(70,80);ctx.lineTo(360,300);ctx.lineTo(720,410);ctx.lineTo(1030,650);ctx.lineTo(1270,880);ctx.lineTo(1630,1020);ctx.lineTo(1900,1320);ctx.stroke();ctx.setLineDash([]);
 // Tree line
 for(let i=0;i<180;i++){
  const x=(i*137+43)%world.w,y=(i*223+79)%world.h;
  if(Math.abs(y-(80+x*.62))<95)continue;
  rect(x-9,y-5,18,19,"#0a100c");rect(x-13,y-18,26,25,"#17241a");
  rect(x-8,y-24,16,13,"#1c2b1e");
 }
 // Water
 rect(0,1450,world.w,350,"#091a1a");
 for(let i=0;i<80;i++)rect((i*91)%world.w,1480+(i*53)%300,rand(10,35),1,"#1b3430");
 // Buildings and interactables
 for(const o of objects){
  const colors={patrol:"#222c2b",evidence:"#382b29",building:"#40372d",tower:"#333e3a",exit:"#4a4030"};
  rect(o.x,o.y,o.w,o.h,colors[o.type]);
  rect(o.x+4,o.y+4,o.w-8,5,"#677066");
  if(o.type==="patrol"){
   rect(o.x+10,o.y+8,o.w-20,o.h-16,"#202a2b");
   rect(o.x+18,o.y+13,24,12,"#52635c");rect(o.x+o.w-38,o.y+13,20,12,"#52635c");
   rect(o.x+7,o.y+o.h-4,16,8,"#080a09");rect(o.x+o.w-23,o.y+o.h-4,16,8,"#080a09");
   text("UNIT 07",o.x+17,o.y+o.h+17,"#d7d8c9",10);
  }else if(o.type==="building"){
   rect(o.x+10,o.y+12,o.w-20,o.h-15,"#292721");
   for(let i=0;i<3;i++)rect(o.x+12+i*22,o.y+23,13,15,"#817452");
   rect(o.x+o.w/2-8,o.y+o.h-21,16,21,"#151612");
  }else if(o.type==="tower"){
   rect(o.x+o.w/2-3,o.y-70,6,135,"#657067");
   for(let j=0;j<4;j++)rect(o.x+o.w/2-24,o.y-50+j*27,48,3,"#657067");
   rect(o.x+o.w/2-9,o.y-75,18,8,"#a14b45");
  }else if(o.type==="evidence"){
   rect(o.x+12,o.y+10,o.w-24,o.h-20,"#a13d37");
   rect(o.x+18,o.y+16,8,3,"#d5bdb0");
  }else if(o.type==="exit"){
   rect(o.x+8,o.y+8,o.w-16,9,"#b3a16e");text("CHECKPOINT",o.x-3,o.y+o.h+17,"#d7c79a",9);
  }
  if(!o.done){
   ctx.fillStyle="#d9c17a";ctx.fillRect(o.x+o.w/2-2,o.y-9,4,4);
  }
 }
 // Monsters
 for(const m of monsters){
  if(m.hit>0)continue;
  const flicker=Math.sin(elapsed*5+m.phase)>-.25;
  rect(m.x-9,m.y-20,18,32,"#080909");
  rect(m.x-12,m.y-29,24,17,"#090b0a");
  if(flicker){rect(m.x-6,m.y-23,4,3,"#b83232");rect(m.x+3,m.y-23,4,3,"#b83232");}
  rect(m.x-8,m.y+10,5,10,"#050605");rect(m.x+3,m.y+10,5,10,"#050605");
 }
 // Player
 const bob=Math.sin(elapsed*11)*(keys.w||keys.a||keys.s||keys.d?2:0);
 rect(player.x-6,player.y-7+bob,12,15,"#b9b9a7");
 rect(player.x-5,player.y-15+bob,10,9,"#333a34");
 rect(player.x-7,player.y+7+bob,5,8,"#424941");rect(player.x+2,player.y+7+bob,5,8,"#424941");
 rect(player.x-8,player.y-5+bob,16,5,"#5b6d5d");
 ctx.restore();

 // Darkness and flashlight
 ctx.fillStyle="rgba(0,0,0,"+(flashOn&&battery>0?".86":".95")+")";
 ctx.fillRect(0,0,W,H);
 if(flashOn&&battery>0){
  const px=player.x-camera.x,py=player.y-camera.y;
  const radius=220+battery*.7;
  const grad=ctx.createRadialGradient(px,py,15,px,py,radius);
  grad.addColorStop(0,"rgba(0,0,0,0)");
  grad.addColorStop(.55,"rgba(0,0,0,.15)");
  grad.addColorStop(1,"rgba(0,0,0,.95)");
  ctx.globalCompositeOperation="destination-out";
  ctx.fillStyle=grad;ctx.fillRect(0,0,W,H);
  ctx.globalCompositeOperation="source-over";
  // Directional flashlight cone
  ctx.save();ctx.translate(px,py);ctx.rotate(player.face);
  const cone=ctx.createRadialGradient(0,0,12,0,0,420);
  cone.addColorStop(0,"rgba(0,0,0,0)");
  cone.addColorStop(1,"rgba(0,0,0,.85)");
  ctx.globalCompositeOperation="destination-out";
  ctx.fillStyle=cone;ctx.beginPath();ctx.moveTo(0,0);ctx.arc(0,0,420,-.42,.42);ctx.closePath();ctx.fill();
  ctx.globalCompositeOperation="source-over";ctx.restore();
 }
 // Rain
 ctx.strokeStyle="rgba(155,177,174,.18)";ctx.lineWidth=1;
 for(let i=0;i<70;i++){
  let x=(i*97+elapsed*180)%W,y=(i*61+elapsed*300)%H;
  ctx.beginPath();ctx.moveTo(x,y);ctx.lineTo(x-4,y+10);ctx.stroke();
 }
 // Screen interference
 if(Math.random()<.12){rect(0,Math.random()*H,W,1,"#c0d0c020");}
 if(health<35&&Math.random()<.3)rect(0,0,W,H,"#7e111116");
}

function loop(t){
 const dt=Math.min((t-last)/1000||0,.04);last=t;
 update(dt);
 if(state!=="menu"&&state!=="panel"&&state!=="dead"&&state!=="won")drawWorld();
 else if(state==="menu"){
  drawWorld();
  // keep menu visible over the live title screen
 }
 else drawWorld();
 requestAnimationFrame(loop);
}
requestAnimationFrame(loop);
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(PAGE)

@app.route("/health")
def health():
    return jsonify({"status": "online", "game": "Florida Shadows"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=False)
