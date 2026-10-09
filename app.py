```python
from flask import Flask, Response

app = Flask(__name__)

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Florida Shadows | State Trooper Horror Files</title>
<style>
*{box-sizing:border-box}
html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#050907;color:#e4e8dd;font-family:Consolas,monospace}
canvas{display:block;width:100%;height:100%;image-rendering:pixelated}
#overlay{position:fixed;inset:0;z-index:5;display:flex;align-items:center;justify-content:center;overflow:auto;background:radial-gradient(ellipse at center,#243027,#070b09 70%)}
#overlay:before{content:"";position:fixed;inset:0;pointer-events:none;background:repeating-linear-gradient(0deg,transparent 0 3px,#fff06 4px)}
.screen{position:relative;width:min(720px,94vw);padding:32px 24px;text-align:center}
.eyebrow{font-size:11px;letter-spacing:5px;color:#a4b09f;margin-bottom:20px}
h1{font-family:Georgia,serif;font-size:clamp(42px,9vw,82px);line-height:.91;letter-spacing:2px;margin:0;color:#e2e3d7;text-shadow:0 5px #171d18,0 0 35px #8b9d7a25}
.subtitle{font-size:11px;letter-spacing:4px;color:#b35b51;margin:22px 0 28px}
.description{max-width:520px;margin:0 auto 25px;color:#b0b9ac;font-size:12px;line-height:2}
button{display:block;width:min(350px,90%);margin:10px auto;padding:15px;background:#111915;border:1px solid #627166;color:#e4e8dc;font:12px Consolas,monospace;letter-spacing:2px;cursor:pointer;transition:.15s}
button:hover{background:#28372c;border-color:#d0d8c6;transform:translateY(-2px)}
button.primary{background:#652322;border-color:#a64d46}
button.primary:hover{background:#8c2c29}
.small{margin-top:23px;font-size:10px;line-height:1.9;color:#859083}
.content{text-align:left;max-width:590px;margin:24px auto;font-size:13px;line-height:2;color:#c8d0c3}
.content h2{font-size:12px;letter-spacing:3px;color:#c6ac7c;margin-top:20px}
.content strong{color:#f0ebdc}
.quote{text-align:center;font-family:Georgia,serif;font-style:italic;color:#a7b39e;margin-top:24px}
#hud{display:none;position:fixed;inset:0;pointer-events:none}
.panel{padding:10px 12px;background:#070b09d9;border:1px solid #4d5c50;box-shadow:0 4px 18px #0008}
#top{position:absolute;top:14px;left:14px;right:14px;display:flex;justify-content:space-between;align-items:flex-start;gap:8px}
#brand{font-size:10px;letter-spacing:2px;color:#b8c2b2}
#objective{font-size:11px;line-height:1.7;margin-top:8px;max-width:310px}
#stats{text-align:right;font-size:11px;line-height:1.9;min-width:130px}
#healthbar{height:5px;background:#462927;margin-top:3px}
#healthfill{height:100%;width:100%;background:#b4473d}
#bottom{position:absolute;bottom:12px;left:12px;right:12px;display:flex;justify-content:space-between;align-items:end;gap:8px}
#radio{max-width:460px;font-size:10px;line-height:1.7;color:#c6cebf}
#controls{text-align:right;font-size:9px;line-height:1.8;color:#aab5a7}
#prompt{position:absolute;bottom:85px;left:50%;transform:translateX(-50%);display:none;background:#050807e8;border:1px solid #8b9a8c;padding:12px;font-size:11px;white-space:nowrap}
#message{position:absolute;top:27%;left:50%;transform:translateX(-50%);width:90%;max-width:600px;text-align:center;font-size:14px;line-height:1.9;text-shadow:0 2px 5px #000}
#crosshair{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);color:#eee;font-size:20px}
#mini{position:absolute;right:16px;top:118px;width:100px;height:100px;background:#06100bd9;border:1px solid #5b6a5c}
#scare{display:none;position:fixed;inset:0;z-index:8;background:#000;align-items:center;justify-content:center;flex-direction:column;text-align:center}
#scare .face{font-size:min(45vw,250px);color:#b52622;text-shadow:0 0 45px #f00}
#scare p{font-size:11px;letter-spacing:4px}
@media(max-width:600px){#controls{display:none}#mini{width:75px;height:75px;top:105px}#objective{max-width:220px;font-size:10px}#stats{font-size:10px;min-width:105px}.panel{padding:8px}#radio{max-width:75%;font-size:9px}}
</style>
</head>
<body>
<canvas id="game"></canvas>

<div id="hud">
 <div id="top">
  <div class="panel">
   <div id="brand">FLORIDA HIGHWAY PATROL // CASE 07-19</div>
   <div id="objective">OBJECTIVE: Investigate the abandoned checkpoint.</div>
  </div>
  <div class="panel" id="stats">
   <div id="clock">02:13 AM</div>
   <div>HEALTH <span id="health">100</span>%</div>
   <div id="healthbar"><div id="healthfill"></div></div>
   <div>AMMO <span id="ammo">6</span> / <span id="reserve">18</span></div>
   <div>CLUES <span id="clues">0</span>/5</div>
  </div>
 </div>
 <canvas id="mini" width="100" height="100"></canvas>
 <div id="crosshair">+</div>
 <div id="message"></div>
 <div id="prompt"></div>
 <div id="bottom">
  <div class="panel" id="radio">RADIO: Dispatch, do you copy? ... Dispatch?</div>
  <div class="panel" id="controls">WASD / ARROWS — MOVE<br>SHIFT — SPRINT<br>E — INVESTIGATE<br>F — FLASHLIGHT<br>R — RELOAD<br>CLICK / SPACE — FIRE</div>
 </div>
</div>

<div id="overlay"><div class="screen" id="screen"></div></div>
<div id="scare"><div class="face">☠</div><p>YOU SHOULD NOT HAVE LOOKED BACK.</p></div>

<script>
"use strict";
const canvas=document.getElementById("game"),ctx=canvas.getContext("2d");
const mini=document.getElementById("mini"),mctx=mini.getContext("2d");
let W=innerWidth,H=innerHeight,DPR=1;
function resize(){W=innerWidth;H=innerHeight;DPR=Math.min(devicePixelRatio||1,2);canvas.width=W*DPR;canvas.height=H*DPR;ctx.setTransform(DPR,0,0,DPR,0,0)}
addEventListener("resize",resize);resize();

const overlay=document.getElementById("overlay"),screen=document.getElementById("screen");
const world={w:3200,h:2600};
let mode="menu",keys={},elapsed=0,last=0,now=0,noticeTime=0,scareTime=0,shootFlash=0;
let mouse={x:W/2,y:H/2};
let player={x:450,y:420,hp:100,ammo:6,reserve:18,clues:0,angle:0,flash:true,invuln:0};
let camera={x:0,y:0};
let monster={x:2350,y:1750,active:false,stalk:0,seen:0};
let radio="RADIO: Dispatch, do you copy? ... Dispatch?";
let notice="";
let seed=91823;
function rand(){seed=(seed*1664525+1013904223)>>>0;return seed/4294967296}
const trees=[];
for(let i=0;i<440;i++)trees.push({x:rand()*world.w,y:rand()*world.h,r:12+rand()*23,c:Math.floor(rand()*4)});
const puddles=[];
for(let i=0;i<95;i++)puddles.push({x:rand()*world.w,y:rand()*world.h,w:10+rand()*50,h:3+rand()*12});
const buildings=[
 {x:760,y:340,w:330,h:230,name:"CHECKPOINT",color:"#46483c"},
 {x:1250,y:650,w:430,h:300,name:"CYPRESS MOTEL",color:"#51443a"},
 {x:2010,y:1000,w:300,h:240,name:"PATROL SHED",color:"#354039"},
 {x:2500,y:1840,w:270,h:300,name:"RADIO TOWER",color:"#3b4840"},
 {x:470,y:1500,w:360,h:270,name:"RANGER CABIN",color:"#4c4033"}
];
const clues=[
 {x:1000,y:490,name:"Bloodied Incident Report",found:false},
 {x:1500,y:800,name:"Damaged Body Camera",found:false},
 {x:2160,y:1150,name:"Missing Trooper's Badge",found:false},
 {x:720,y:1700,name:"Motel Guest Ledger",found:false},
 {x:2670,y:2010,name:"Transmission Recording",found:false}
];
const objectives=[
 "OBJECTIVE: Investigate the abandoned checkpoint.",
 "OBJECTIVE: Search the roadside motel.",
 "OBJECTIVE: Find the remaining evidence.",
 "OBJECTIVE: Locate the missing trooper's patrol car.",
 "OBJECTIVE: Reach the radio tower and call for help."
];

function menu(which="menu"){
 mode="menu";overlay.style.display="flex";
 if(which==="how"){
  screen.innerHTML=`<div class="eyebrow">FIELD MANUAL // REVISION 04</div><h1 style="font-size:48px">HOW TO PLAY</h1><div class="content">
  <h2>CONTROLS</h2><strong>WASD / ARROWS</strong> — Move through the swamp.<br><strong>SHIFT</strong> — Sprint, but noise attracts attention.<br><strong>E</strong> — Inspect evidence and search structures.<br><strong>F</strong> — Toggle flashlight.<br><strong>R</strong> — Reload your service weapon.<br><strong>LEFT CLICK / SPACE</strong> — Fire your weapon.<br>
  <h2>YOUR ASSIGNMENT</h2>Investigate the checkpoint, search the buildings, collect five pieces of evidence, and reach the radio tower. Your flashlight helps you see, but it may reveal things you would rather not see.<h2>FIELD WARNING</h2>Something is moving between the trees. It does not always chase you. Sometimes it simply watches.</div><button class="primary" onclick="menu('menu')">BACK TO MENU</button>`;
 }else if(which==="credits"){
  screen.innerHTML=`<div class="eyebrow">CASE FILE // ACKNOWLEDGEMENTS</div><h1 style="font-size:52px">CREDITS</h1><div class="content" style="text-align:center"><h2>SPECIAL THANKS</h2><p>Special thanks to <strong>Mayumi Alingarog (Yumi, Mimi, Yumimi)</strong>, my classmate and fellow developer, for being very helpful, kind, and respectful throughout the journey.</p><p>Thank you for the support, inspiration, and encouragement that helped make this project possible.</p><h2>CREATED FOR SCREAM JAM 2026</h2><div class="quote">Every mystery leaves a trace. Every crime leaves a shadow. And some shadows are always watching.</div></div><button class="primary" onclick="menu('menu')">BACK TO MENU</button>`;
 }else if(which==="dead"){
  screen.innerHTML=`<div class="eyebrow">OFFICER DOWN // FILE SEALED</div><h1 style="font-size:60px">NO<br>RESPONSE</h1><p class="description">The radio kept transmitting after your body camera stopped.</p><button class="primary" onclick="startGame()">TRY AGAIN</button><button onclick="menu('credits')">CREDITS</button><button onclick="menu('menu')">MAIN MENU</button>`;
 }else if(which==="win"){
  screen.innerHTML=`<div class="eyebrow">TRANSMISSION SENT</div><h1 style="font-size:60px">CASE<br>UNSEALED</h1><p class="description">The tower answers. Through the static, you hear a second voice—using your own call sign.</p><button class="primary" onclick="menu('credits')">CREDITS</button><button onclick="menu('menu')">MAIN MENU</button>`;
 }else{
  screen.innerHTML=`<div class="eyebrow">FLORIDA HIGHWAY PATROL PRESENTS</div><h1>FLORIDA<br>SHADOWS</h1><div class="subtitle">STATE TROOPER HORROR FILES</div><p class="description">A routine midnight welfare check becomes an investigation into something the official reports refuse to acknowledge.</p><button class="primary" onclick="startGame()">BEGIN NIGHT PATROL</button><button onclick="menu('how')">HOW TO PLAY</button><button onclick="menu('credits')">CREDITS</button><div class="small">FICTIONAL HORROR EXPERIENCE · SCREAM JAM 2026<br>HEADPHONES RECOMMENDED · YOU ARE NOT ALONE</div>`;
 }
}
menu();

function startGame(){
 player={x:450,y:420,hp:100,ammo:6,reserve:18,clues:0,angle:0,flash:true,invuln:0};
 monster={x:2350,y:1750,active:false,stalk:0,seen:0};
 clues.forEach(c=>c.found=false);
 elapsed=0;now=0;notice="";noticeTime=0;scareTime=0;shootFlash=0;
 radio="RADIO: Dispatch, do you copy? ... Dispatch?";
 document.getElementById("radio").textContent=radio;
 document.getElementById("clues").textContent="0";
 document.getElementById("ammo").textContent="6";
 document.getElementById("reserve").textContent="18";
 document.getElementById("health").textContent="100";
 document.getElementById("healthfill").style.width="100%";
 document.getElementById("objective").textContent=objectives[0];
 document.getElementById("hud").style.display="block";
 overlay.style.display="none";mode="playing";last=performance.now();
}
function setRadio(s){radio=s;document.getElementById("radio").textContent=s}
function say(s,d=3){notice=s;noticeTime=d;document.getElementById("message").textContent=s}
function finish(win){mode=win?"win":"dead";document.getElementById("hud").style.display="none";menu(win?"win":"dead")}
function reload(){
 const n=Math.min(6-player.ammo,player.reserve);
 if(n>0){player.ammo+=n;player.reserve-=n;document.getElementById("ammo").textContent=player.ammo;document.getElementById("reserve").textContent=player.reserve;setRadio("RADIO: Magazine seated. Keep moving.")}
}
function shoot(){
 if(mode!=="playing")return;
 if(player.ammo<=0){say("CLICK. EMPTY.",1);return}
 player.ammo--;shootFlash=.1;document.getElementById("ammo").textContent=player.ammo;
 let d=Math.hypot(monster.x-player.x,monster.y-player.y);
 if(monster.active&&d<420){
  let a=Math.atan2(monster.y-player.y,monster.x-player.x);
  let diff=Math.abs(Math.atan2(Math.sin(a-player.angle),Math.cos(a-player.angle)));
  if(diff<.4){monster.stalk++;say("The shape recoils into the rain.",1.4);if(monster.stalk>=4){monster.x+=Math.cos(a+2)*260;monster.y+=Math.sin(a+2)*260;monster.stalk=0}}
 }else if(Math.random()<.12)say("The shot disappears into the trees.",1.3);
}
function interact(){
 let best=null,dist=110;
 for(const c of clues)if(!c.found){let d=Math.hypot(c.x-player.x,c.y-player.y);if(d<dist){best=c;dist=d}}
 if(best){
  best.found=true;player.clues++;document.getElementById("clues").textContent=player.clues;
  say("EVIDENCE LOGGED: "+best.name.toUpperCase(),3);
  setRadio("RADIO: Evidence logged. Dispatch is not responding.");
  if(player.clues===1){monster.active=true;setRadio("RADIO: ...Officer? There is someone behind you.")}
  if(player.clues===5){setRadio("RADIO: Tower coordinates received. Get there now.");}
  return;
 }
 for(const b of buildings){
  const d=Math.hypot(b.x+b.w/2-player.x,b.y+b.h/2-player.y);
  if(d<Math.max(b.w,b.h)*.65+70){
   if(b.name==="RADIO TOWER"&&player.clues>=5){finish(true);return}
   say(b.name+": The door is jammed. Search the perimeter for evidence.",3);
   setRadio("RADIO: No entry. Check the surrounding area.");return;
  }
 }
 say("Nothing useful nearby. Check the roadside and structures.",2);
}
addEventListener("keydown",e=>{
 keys[e.key.toLowerCase()]=true;
 if(["ArrowUp","ArrowDown","ArrowLeft","ArrowRight"," "].includes(e.key))e.preventDefault();
 if(mode==="playing"){
  if(e.key.toLowerCase()==="f")player.flash=!player.flash;
  if(e.key.toLowerCase()==="r")reload();
  if(e.key.toLowerCase()==="e")interact();
  if(e.code==="Space")shoot();
 }
});
addEventListener("keyup",e=>keys[e.key.toLowerCase()]=false);
canvas.addEventListener("mousemove",e=>{mouse.x=e.clientX;mouse.y=e.clientY});
canvas.addEventListener("mousedown",shoot);
let mouse={x:W/2,y:H/2};

function update(dt){
 if(mode!=="playing")return;
 elapsed+=dt;now+=dt;shootFlash=Math.max(0,shootFlash-dt);
 let vx=0,vy=0;
 if(keys.w||keys.arrowup)vy--;if(keys.s||keys.arrowdown)vy++;
 if(keys.a||keys.arrowleft)vx--;if(keys.d||keys.arrowright)vx++;
 const len=Math.hypot(vx,vy)||1;vx/=len;vy/=len;
 const speed=155*(keys.shift?1.55:1);
 player.x=Math.max(25,Math.min(world.w-25,player.x+vx*speed*dt));
 player.y=Math.max(25,Math.min(world.h-25,player.y+vy*speed*dt));
 if(vx||vy)player.angle=Math.atan2(vy,vx);
 if(Math.abs(mouse.x-W/2)>5||Math.abs(mouse.y-H/2)>5)player.angle=Math.atan2(mouse.y-H/2,mouse.x-W/2);
 camera.x=Math.max(0,Math.min(world.w-W,player.x-W/2));
 camera.y=Math.max(0,Math.min(world.h-H,player.y-H/2));
 if(monster.active){
  monster.seen+=dt;
  const dx=player.x-monster.x,dy=player.y-monster.y,d=Math.hypot(dx,dy)||1;
  const target=d<260?105:320;
  if(d>target){monster.x+=dx/d*Math.min(d-target,48*dt);monster.y+=dy/d*Math.min(d-target,48*dt)}
  if(d<100&&player.invuln<=0){
   player.hp-=15;player.invuln=1.2;say("IT FOUND YOU.",1);
   setRadio("RADIO: [SCREAMING STATIC]");
   if(Math.random()<.35)jumpscare();
  }
  if(d>900&&monster.seen>12){monster.x=player.x+(Math.random()<.5?-1:1)*(320+Math.random()*180);monster.y=player.y+(Math.random()<.5?-1:1)*(280+Math.random()*180)}
  if(d<340&&Math.random()<dt*.12)say("You hear wet footsteps behind you.",2);
 }
 player.invuln=Math.max(0,player.invuln-dt);
 noticeTime-=dt;if(noticeTime<=0)document.getElementById("message").textContent="";
 scareTime=Math.max(0,scareTime-dt);
 if(player.hp<=0){finish(false);return}
 document.getElementById("health").textContent=Math.max(0,Math.ceil(player.hp));
 document.getElementById("healthfill").style.width=Math.max(0,player.hp)+"%";
 document.getElementById("clock").textContent="02:"+String(Math.floor((13+elapsed/3)%60)).padStart(2,"0")+" AM";
 let objectiveIndex=player.clues===0?0:player.clues===1?1:player.clues<5?2:4;
 document.getElementById("objective").textContent=objectives[objectiveIndex];
 let nearest=null,nd=120;
 for(const c of clues)if(!c.found){let d=Math.hypot(c.x-player.x,c.y-player.y);if(d<nd){nearest=c;nd=d}}
 const prompt=document.getElementById("prompt");
 if(nearest){prompt.style.display="block";prompt.textContent="[ E ] INVESTIGATE: "+nearest.name}
 else if(buildings.some(b=>Math.hypot(b.x+b.w/2-player.x,b.y+b.h/2-player.y)<180)){prompt.style.display="block";prompt.textContent="[ E ] SEARCH STRUCTURE"}
 else prompt.style.display="none";
}

function jumpscare(){
 if(scareTime>0)return;
 scareTime=1;
 const s=document.getElementById("scare");s.style.display="flex";
 setTimeout(()=>{s.style.display="none"},450);
}
function draw(){
 ctx.fillStyle="#101913";ctx.fillRect(0,0,W,H);
 // Pixelated swamp ground
 for(let y=-10;y<H+20;y+=30)for(let x=-10;x<W+20;x+=36){
  let wx=x+camera.x,wy=y+camera.y,n=Math.sin(wx*.03+wy*.021);
  ctx.fillStyle=n>.65?"#1b291e":n<-.55?"#0c1510":"#132017";
  ctx.fillRect(x,y,18+Math.abs(n)*12,2);
 }
 // Winding wet road
 ctx.beginPath();
 for(let y=0;y<=world.h;y+=35){
  let x=1500+Math.sin(y*.0017)*380+Math.sin(y*.004)*85-camera.x;
  if(y===0)ctx.moveTo(x,y-camera.y);else ctx.lineTo(x,y-camera.y);
 }
 ctx.strokeStyle="#2d322e";ctx.lineWidth=145;ctx.stroke();
 ctx.strokeStyle="#5a6057";ctx.lineWidth=2;ctx.setLineDash([24,30]);ctx.stroke();ctx.setLineDash([]);
 for(const p of puddles){
  const x=p.x-camera.x,y=p.y-camera.y;if(x<-70||y<-40||x>W+70||y>H+40)continue;
  ctx.fillStyle="#273a35";ctx.beginPath();ctx.ellipse(x,y,p.w,p.h,0,0,Math.PI*2);ctx.fill();
  ctx.strokeStyle="#4a5d53";ctx.lineWidth=1;ctx.stroke();
 }
 for(const t of trees){
  const x=t.x-camera.x,y=t.y-camera.y;if(x<-65||y<-65||x>W+65||y>H+65)continue;
  ctx.fillStyle="#070c09";ctx.beginPath();ctx.ellipse(x+5,y+9,t.r*1.35,t.r*.8,0,0,Math.PI*2);ctx.fill();
  ctx.fillStyle=["#17251b","#1b2b20","#213024","#18251d"][t.c];
  ctx.beginPath();ctx.arc(x,y,t.r,0,Math.PI*2);ctx.fill();
  ctx.fillStyle="#2d3b2a";ctx.fillRect(x-2,y-t.r*.5,4,t.r);
 }
 for(const b of buildings){
  const x=b.x-camera.x,y=b.y-camera.y;
  if(x<-b.w-40||y<-b.h-40||x>W+40||y>H+40)continue;
  ctx.fillStyle="#050706";ctx.fillRect(x+10,y+14,b.w,b.h);
  ctx.fillStyle=b.color;ctx.fillRect(x,y,b.w,b.h);
  ctx.fillStyle="#252d27";ctx.fillRect(x-8,y-8,b.w+16,20);
  ctx.fillStyle="#626e60";ctx.fillRect(x,y,b.w,4);
  for(let wx=x+22;wx<x+b.w-15;wx+=65){
   ctx.fillStyle="#101a18";ctx.fillRect(wx,y+47,28,38);
   ctx.fillStyle=Math.sin(now*2+wx)>.7?"#a17e47":"#263a33";
   ctx.fillRect(wx+4,y+51,20,29);
   ctx.fillStyle="#1c2520";ctx.fillRect(wx,y+b.h-32,25,32);
  }
  ctx.fillStyle="#c2bca0";ctx.font="10px monospace";ctx.fillText(b.name,x+12,y+25);
  if(b.name==="RADIO TOWER"){
   ctx.strokeStyle="#637568";ctx.lineWidth=3;ctx.beginPath();
   ctx.moveTo(x+b.w/2,y);ctx.lineTo(x+b.w/2-20,y-150);
   ctx.lineTo(x+b.w/2+20,y-150);ctx.closePath();ctx.stroke();
   ctx.fillStyle="#ba3029";ctx.fillRect(x+b.w/2-3,y-157,6,7);
  }
 }
 // Abandoned patrol car
 const carx=1100-camera.x,cary=1100-camera.y;
 ctx.fillStyle="#070a09";ctx.fillRect(carx-29,cary-16,62,34);
 ctx.fillStyle="#202925";ctx.fillRect(carx-25,cary-19,55,28);
 ctx.fillStyle="#a1a79a";ctx.fillRect(carx-12,cary-16,24,4);
 ctx.fillStyle="#a22e2a";ctx.fillRect(carx+1,cary-23,10,5);
 ctx.fillStyle="#293e41";ctx.fillRect(carx-18,cary-11,14,8);ctx.fillRect(carx+9,cary-11,14,8);
 ctx.fillStyle="#090a09";ctx.fillRect(carx-20,cary+11,12,5);ctx.fillRect(carx+17,cary+11,12,5);
 // Evidence markers
 for(const c of clues)if(!c.found){
  const x=c.x-camera.x,y=c.y-camera.y;
  ctx.fillStyle="#d5bc7a";ctx.fillRect(x-3,y-3,6,6);
  ctx.fillStyle="#d5bc7840";ctx.beginPath();ctx.arc(x,y,12+Math.sin(now*3)*3,0,Math.PI*2);ctx.fill();
 }
 // The Smiler
 if(monster.active){
  const x=monster.x-camera.x,y=monster.y-camera.y,d=Math.hypot(player.x-monster.x,player.y-monster.y);
  if(x>-100&&y>-100&&x<W+100&&y<H+100){
   const scale=Math.max(.65,Math.min(1.5,440/Math.max(d,1)));
   ctx.save();ctx.translate(x,y);ctx.scale(scale,scale);
   ctx.fillStyle="#050605";ctx.beginPath();ctx.ellipse(0,0,18,39,0,0,Math.PI*2);ctx.fill();
   ctx.fillRect(-13,-6,26,53);
   ctx.beginPath();ctx.ellipse(0,-38,13,17,0,0,Math.PI*2);ctx.fill();
   ctx.fillStyle="#bb2821";ctx.fillRect(-7,-42,4,3);ctx.fillRect(4,-42,4,3);
   ctx.strokeStyle="#070807";ctx.lineWidth=7;ctx.beginPath();
   ctx.moveTo(-12,2);ctx.lineTo(-25,36);ctx.moveTo(12,2);ctx.lineTo(23,36);ctx.stroke();
   ctx.restore();
  }
 }
 // Player character
 const px=player.x-camera.x,py=player.y-camera.y;
 ctx.fillStyle="#050606";ctx.beginPath();ctx.ellipse(px,py+9,13,7,0,0,Math.PI*2);ctx.fill();
 ctx.fillStyle=player.invuln>0&&Math.floor(now*12)%2?"#a64b43":"#809184";
 ctx.fillRect(px-7,py-10,14,20);
 ctx.fillStyle="#c7bea5";ctx.fillRect(px-5,py-18,10,10);
 ctx.strokeStyle="#090c0a";ctx.lineWidth=4;ctx.beginPath();
 ctx.moveTo(px-4,py+8);ctx.lineTo(px-6,py+16);ctx.moveTo(px+4,py+8);ctx.lineTo(px+6,py+16);ctx.stroke();
 // Flashlight beam and darkness
 ctx.save();
 ctx.fillStyle="#020504";ctx.fillRect(0,0,W,H);
 ctx.globalCompositeOperation="destination-out";
 const glow=ctx.createRadialGradient(px,py,25,px,py,player.flash?Math.max(W,H)*.65:180);
 glow.addColorStop(0,"rgba(0,0,0,1)");glow.addColorStop(.6,"rgba(0,0,0,.84)");glow.addColorStop(1,"rgba(0,0,0,0)");
 ctx.fillStyle=glow;ctx.fillRect(0,0,W,H);
 if(player.flash){
  ctx.translate(px,py);ctx.rotate(player.angle);
  const beam=ctx.createRadialGradient(0,0,10,0,0,410);
  beam.addColorStop(0,"rgba(0,0,0,.94)");beam.addColorStop(1,"rgba(0,0,0,0)");
  ctx.fillStyle=beam;ctx.beginPath();ctx.moveTo(0,0);ctx.arc(0,0,410,-.42,.42);ctx.closePath();ctx.fill();
 }
 ctx.restore();
 // Atmospheric fog and rain
 const fog=ctx.createLinearGradient(0,0,0,H);
 fog.addColorStop(0,"rgba(17,28,21,.12)");fog.addColorStop(1,"rgba(2,6,4,.5)");
 ctx.fillStyle=fog;ctx.fillRect(0,0,W,H);
 ctx.strokeStyle="#b8c5bd36";ctx.lineWidth=1;
 for(let i=0;i<95;i++){
  let rx=(i*137+now*95)%W,ry=(i*79+now*230)%(H+20);
  ctx.beginPath();ctx.moveTo(rx,ry);ctx.lineTo(rx-4,ry+11);ctx.stroke();
 }
 if(shootFlash>0){ctx.fillStyle="#e6dfbb";ctx.fillRect(W/2-3,H/2-3,6,6)}
 drawMini();
}
function drawMini(){
 mctx.fillStyle="#07100b";mctx.fillRect(0,0,100,100);
 mctx.strokeStyle="#4b554b";mctx.lineWidth=5;mctx.beginPath();
 for(let y=0;y<=world.h;y+=40){let x=(1500+Math.sin(y*.0017)*380+Math.sin(y*.004)*85)/world.w*100; if(y===0)mctx.moveTo(x,y/world.h*100);else mctx.lineTo(x,y/world.h*100)}
 mctx.stroke();
 for(const b of buildings){mctx.fillStyle="#7d806d";mctx.fillRect(b.x/world.w*100,b.y/world.h*100,3,3)}
 for(const c of clues)if(!c.found){mctx.fillStyle="#d9bb70";mctx.fillRect(c.x/world.w*100,c.y/world.h*100,2,2)}
 if(monster.active){mctx.fillStyle="#c32c26";mctx.fillRect(monster.x/world.w*100-1,monster.y/world.h*100-1,3,3)}
 mctx.fillStyle="#f1eee0";mctx.fillRect(player.x/world.w*100-2,player.y/world.h*100-2,4,4);
}

function frame(ts){
 const dt=Math.min(.04,(ts-(last||ts))/1000||0);last=ts;
 if(mode==="playing")update(dt);
 if(mode==="playing")draw();else drawMenuBackground();
 requestAnimationFrame(frame);
}
function drawMenuBackground(){
 ctx.fillStyle="#080e0a";ctx.fillRect(0,0,W,H);
 for(let i=0;i<80;i++){
  const x=(i*197+now*8)%W,y=(i*83+now*19)%H;
  ctx.fillStyle=i%3?"#111d14":"#1c291c";ctx.fillRect(x,y,2,2);
 }
 ctx.strokeStyle="#202c22";ctx.lineWidth=2;
 for(let i=0;i<18;i++){
  const x=i*W/17;
  ctx.beginPath();ctx.moveTo(x,H);ctx.lineTo(x+Math.sin(i)*25,H*.25);ctx.stroke();
 }
 ctx.fillStyle="#0b120d";ctx.fillRect(0,H*.78,W,H*.22);
}
requestAnimationFrame(frame);
</script>
</body>
</html>"""

@app.route("/")
def index():
    return Response(HTML, mimetype="text/html")

@app.route("/health")
def health():
    return {"status": "online", "game": "Florida Shadows"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
```
