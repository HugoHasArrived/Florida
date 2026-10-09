
import os
from flask import Flask, Response, jsonify

app = Flask(__name__)

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Florida Shadows</title>
<style>
*{box-sizing:border-box}
body{margin:0;background:#020609;color:#e5faff;font:14px Consolas,monospace;overflow:hidden}
canvas{width:100vw;height:100vh;display:block;image-rendering:pixelated}
#hud{position:fixed;inset:0;pointer-events:none;text-shadow:0 2px 3px #000}
.panel{background:#041019e8;border:1px solid #5b879b;padding:12px;box-shadow:0 0 18px #092737}
#brand{position:absolute;top:15px;left:20px;font-size:clamp(20px,4vw,38px);font-weight:bold;letter-spacing:2px}
#brand span{color:#ff304b}
#sub{font-size:10px;letter-spacing:3px;color:#9bbac6}
#stats{position:absolute;top:95px;left:20px;width:230px;font-size:12px}
.bar{height:10px;background:#18252b;border:1px solid #6b8995;margin:5px 0 10px}
.fill{height:100%;width:100%}.hp{background:#ff304b}.battery{background:#26dfff}
#map{position:absolute;right:18px;top:18px;width:160px;height:105px;border:1px solid #83a5b3;background:#071812}
#objectives{position:absolute;right:18px;top:138px;width:220px;line-height:1.8;font-size:12px}
#dispatch{position:absolute;left:20px;bottom:20px;width:min(450px,calc(100vw - 40px));line-height:1.5;font-size:12px}
#dispatch b{color:#ffc75b}
#controls{position:absolute;right:18px;bottom:18px;line-height:1.8;text-align:right;font-size:11px}
#prompt{position:absolute;bottom:22%;left:50%;transform:translateX(-50%);background:#06131dee;border:1px solid #72eaff;padding:10px;display:none}
#overlay{position:fixed;inset:0;z-index:5;display:flex;align-items:center;justify-content:center;background:radial-gradient(ellipse,#0a1b26d9,#010306f7)}
.card{width:min(580px,92vw);padding:30px;text-align:center;background:#030b12f5;border:1px solid #6b94a5;box-shadow:0 0 60px #123746}
.kicker{font-size:11px;letter-spacing:3px;color:#9acbdb}
.title{font-size:clamp(38px,8vw,70px);font-weight:1000;line-height:.95;margin:20px 0;text-shadow:0 0 20px #244c60}
.title span{color:#ff304b}
.desc{color:#b6c9d2;line-height:1.8;margin:20px 0}
button{pointer-events:auto;background:#0b3545;color:white;border:1px solid #9defff;padding:14px 24px;font:bold 13px Consolas;letter-spacing:2px;cursor:pointer}
button:hover{background:#17637a}
.small{font-size:10px;color:#829ba7;line-height:1.8;margin-top:20px}
#toast{position:absolute;left:50%;top:43%;transform:translate(-50%,-50%);color:#ffe3a0;font-weight:bold;text-align:center;opacity:0}
@media(max-width:600px){#stats{top:90px;width:175px;font-size:10px}#map{width:110px;height:75px}#objectives{top:105px;width:140px;font-size:10px}#controls{display:none}}
</style>
</head>
<body>
<canvas id="game"></canvas>
<div id="hud">
 <div id="brand">FLORIDA <span>SHADOWS</span><div id="sub">STATE TROOPER HORROR FILES</div></div>
 <div id="stats" class="panel">UNIT 07 / NIGHT SHIFT
 <div style="margin-top:12px">HEALTH <span id="hpnum" style="float:right">100%</span>
 <div class="bar"><div id="hp" class="fill hp"></div></div>
 FLASHLIGHT <span id="batnum" style="float:right">100%</span>
 <div class="bar"><div id="bat" class="fill battery"></div></div>
 AMMO <span id="ammo" style="float:right">6 / 12</span></div></div>
 <canvas id="map" width="160" height="105"></canvas>
 <div id="objectives" class="panel"><b>CASE OBJECTIVES</b><div id="objtext"></div></div>
 <div id="dispatch" class="panel"><b>DISPATCH:</b> Unit 07, radio check. Reports of an abandoned patrol car near Cypress Mile. Proceed with caution.</div>
 <div id="controls" class="panel">WASD / ARROWS — MOVE<br>SHIFT — SPRINT<br>E — INVESTIGATE<br>F — FLASHLIGHT<br>SPACE / CLICK — FIRE<br>R — RELOAD</div>
 <div id="prompt"></div><div id="toast"></div>
</div>
<div id="overlay"><div class="card">
 <div class="kicker">FLORIDA HIGHWAY PATROL • CASE 07-113</div>
 <div class="title">FLORIDA<br><span>SHADOWS</span></div>
 STATE TROOPER HORROR FILES
 <div class="desc">02:13 AM. A patrol unit has disappeared on Cypress Mile.<br><br>Your radio is receiving a signal from somewhere deep inside the swamp.<br><b>If you see lights between the trees, do not assume they belong to a car.</b></div>
 <button id="start">BEGIN NIGHT PATROL</button>
 <div class="small">WASD TO MOVE • E TO INVESTIGATE • F TOGGLE FLASHLIGHT<br>HEADPHONES RECOMMENDED</div>
</div></div>
<script>
(()=>{
const canvas=document.getElementById('game'),ctx=canvas.getContext('2d');
const map=document.getElementById('map'),mc=map.getContext('2d');
let W,H,dpr,camX=0,camY=0,time=0,last=0,running=false,dead=false,won=false;
function resize(){W=innerWidth;H=innerHeight;dpr=Math.min(devicePixelRatio||1,2);canvas.width=W*dpr;canvas.height=H*dpr;ctx.setTransform(dpr,0,0,dpr,0,0)}
addEventListener('resize',resize);resize();
const WORLD={w:2600,h:1900},keys={};
const p={x:540,y:840,a:0,hp:100,bat:100,ammo:6,flash:true,inv:0};
let seed=123456;function rand(){seed=(seed*1664525+1013904223)>>>0;return seed/4294967296}
const trees=[],puddles=[],rain=[];
for(let i=0;i<320;i++)trees.push({x:rand()*WORLD.w,y:rand()*WORLD.h,r:12+rand()*30,c:rand()});
for(let i=0;i<100;i++)puddles.push({x:rand()*WORLD.w,y:rand()*WORLD.h,w:10+rand()*65,h:3+rand()*11});
for(let i=0;i<200;i++)rain.push({x:rand()*W,y:rand()*H,l:8+rand()*18,s:250+rand()*450});
const buildings=[
{x:330,y:730,w:135,h:60,type:'car'},
{x:1030,y:530,w:340,h:170,type:'motel'},
{x:1550,y:420,w:100,h:150,type:'tower'},
{x:2110,y:950,w:150,h:90,type:'checkpoint'},
{x:770,y:1190,w:180,h:120,type:'shed'},
{x:1900,y:1290,w:210,h:135,type:'house'}
];
const clues=[
{x:590,y:820,name:'Bloodied dash camera',got:false},
{x:1200,y:625,name:'Motel room key',got:false},
{x:1780,y:1060,name:'Torn uniform patch',got:false}
];
let carChecked=false,towerFixed=false,checkpoint=false;
const monster={x:2050,y:770,active:false,stun:0};
function box(x,y,w,h,c){ctx.fillStyle=c;ctx.fillRect(x,y,w,h)}
function label(s,x,y,size,c){ctx.fillStyle=c;ctx.font=size+'px Consolas';ctx.fillText(s,x,y)}
function dist(x,y,a,b){return Math.hypot(x-a,y-b)}
function camera(){camX=Math.max(0,Math.min(WORLD.w-W,p.x-W/2));camY=Math.max(0,Math.min(WORLD.h-H,p.y-H/2))}
function drawWorld(){
 camera();ctx.save();ctx.translate(-camX,-camY);
 box(0,0,WORLD.w,WORLD.h,'#071712');
 for(let i=0;i<700;i++){let x=(i*137)%WORLD.w,y=(i*241)%WORLD.h;box(x,y,2+i%4,1,'#10271d')}
 // Main wet highway
 box(0,900,WORLD.w,142,'#151c1e');box(0,900,WORLD.w,3,'#77715a');box(0,1039,WORLD.w,3,'#615d49');
 for(let x=0;x<WORLD.w;x+=100)box(x,968,48,4,'#b6a979');
 // Side road
 ctx.strokeStyle='#202728';ctx.lineWidth=60;ctx.beginPath();ctx.moveTo(1330,970);ctx.bezierCurveTo(1400,1100,1500,1220,1770,1320);ctx.stroke();
 ctx.strokeStyle='#77715a';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(1330,938);ctx.bezierCurveTo(1400,1068,1500,1188,1770,1288);ctx.stroke();
 for(const q of puddles){box(q.x,q.y,q.w,q.h,'#09252a');box(q.x+3,q.y+q.h/2,q.w*.6,1,'#20505a')}
 // Layered swamp trees
 for(const t of trees){
 if(t.x<camX-60||t.x>camX+W+60||t.y<camY-60||t.y>camY+H+60)continue;
 box(t.x-4,t.y,8,t.r,'#211e18');
 ctx.fillStyle=t.c>.5?'#09251b':'#0b3022';ctx.beginPath();ctx.arc(t.x,t.y-t.r*.3,t.r,0,7);ctx.fill();
 ctx.fillStyle='#153b2b';ctx.beginPath();ctx.arc(t.x-t.r*.3,t.y-t.r*.5,t.r*.6,0,7);ctx.fill();
 ctx.fillStyle='#06170f';ctx.beginPath();ctx.arc(t.x+t.r*.28,t.y-t.r*.2,t.r*.65,0,7);ctx.fill();
 }
 for(const b of buildings){
 if(b.type==='motel'){
 box(b.x-12,b.y+135,b.w+24,18,'#04090b');box(b.x,b.y,b.w,b.h,'#37342c');box(b.x+8,b.y+8,b.w-16,30,'#544936');
 for(let i=0;i<5;i++){let x=b.x+14+i*63;box(x,b.y+52,48,65,'#171e20');box(x+5,b.y+58,38,48,i%3===0?'#d99a45':'#9e572d');box(x+8,b.y+62,32,40,'#302f26');box(x+4,b.y+122,40,8,'#9a784a')}
 box(b.x+80,b.y-18,180,25,'#171d1e');box(b.x+86,b.y-16,168,20,'#ad2030');
 ctx.shadowColor='#ff244b';ctx.shadowBlur=20;box(b.x+88,b.y-14,164,3,'#ff6571');ctx.shadowBlur=0;label('CYPRESS MILE',b.x+98,b.y-1,13,'#ffe1d7');
 }else if(b.type==='car'){
 box(b.x,b.y+13,b.w,35,'#070b0d');box(b.x+17,b.y,b.w-35,50,'#c9d3d0');box(b.x+42,b.y+4,42,22,'#182e39');box(b.x+91,b.y+4,24,22,'#182e39');box(b.x+5,b.y+2,22,8,'#ff244b');box(b.x+95,b.y+2,22,8,'#28dfff');box(b.x+44,b.y+27,55,12,'#101719');label('FHP',b.x+49,b.y+37,9,'#fff');
 }else if(b.type==='tower'){
 box(b.x+42,b.y+5,8,140,'#414b49');
 for(let i=0;i<5;i++){let y=b.y+20+i*25;ctx.strokeStyle='#64716d';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(b.x+10,y);ctx.lineTo(b.x+80,y+18);ctx.stroke()}
 ctx.strokeStyle='#626d69';ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(b.x+46,b.y+5);ctx.lineTo(b.x+5,b.y+140);ctx.moveTo(b.x+46,b.y+5);ctx.lineTo(b.x+91,b.y+140);ctx.stroke();
 ctx.shadowColor='#ff263d';ctx.shadowBlur=20;box(b.x+42,b.y-5,8,10,'#ff273d');ctx.shadowBlur=0;
 }else if(b.type==='checkpoint'){
 box(b.x,b.y,b.w,75,'#30332a');box(b.x+12,b.y+10,b.w-24,25,'#14291f');label('COUNTY',b.x+43,b.y+27,12,'#c0d2b7');label('CHECKPOINT',b.x+20,b.y+43,10,'#c0d2b7');box(b.x+8,b.y+76,b.w-16,7,'#d1b95b');
 }else{
 box(b.x,b.y,b.w,b.h,'#302e29');box(b.x+12,b.y+12,b.w-24,24,'#131d20');box(b.x+25,b.y+45,35,42,'#b47a43');box(b.x+95,b.y+45,35,42,'#7d5637');box(b.x+b.w/2-12,b.y+b.h-37,25,37,'#17191a');
 }}
 for(const c of clues)if(!c.got){let pulse=.5+.5*Math.sin(time*4+c.x);ctx.fillStyle='rgba(255,190,65,'+(.3+pulse*.6)+')';ctx.beginPath();ctx.arc(c.x,c.y,9+pulse*5,0,7);ctx.fill();label('!',c.x-3,c.y+4,12,'#fff1b4')}
 if(monster.active){
 let bob=Math.sin(time*5)*4;ctx.fillStyle='#020406';ctx.beginPath();ctx.ellipse(monster.x,monster.y,18,32+bob,0,0,7);ctx.fill();box(monster.x-12,monster.y+15,8,32,'#020406');box(monster.x+6,monster.y+15,8,32,'#020406');
 ctx.shadowColor='#ff002b';ctx.shadowBlur=15;box(monster.x-8,monster.y-14,4,3,'#ff243b');box(monster.x+5,monster.y-14,4,3,'#ff243b');ctx.shadowBlur=0;
 }
 // Player sprite
 ctx.save();ctx.translate(p.x,p.y);ctx.rotate(p.a);
 ctx.fillStyle='#020507';ctx.beginPath();ctx.ellipse(2,7,13,17,0,0,7);ctx.fill();
 box(-9,-9,18,18,'#263d49');box(-8,-13,16,8,'#aab9b9');box(-10,-16,20,4,'#17232b');box(-3,-7,6,5,'#d4a66c');box(7,-3,18,5,'#b9d2d6');ctx.restore();
 // Flashlight beam
 if(p.flash){let g=ctx.createRadialGradient(p.x,p.y,10,p.x+Math.cos(p.a)*160,p.y+Math.sin(p.a)*160,225);g.addColorStop(0,'rgba(210,238,210,.20)');g.addColorStop(1,'rgba(210,238,210,0)');ctx.fillStyle=g;ctx.beginPath();ctx.moveTo(p.x,p.y);ctx.arc(p.x,p.y,245,p.a-.42,p.a+.42);ctx.closePath();ctx.fill()}
 ctx.restore();
 // Night vignette
 let v=ctx.createRadialGradient(W/2,H/2,Math.min(W,H)*.15,W/2,H/2,Math.max(W,H)*.72);v.addColorStop(0,'rgba(0,4,8,.03)');v.addColorStop(1,'rgba(0,2,7,.82)');ctx.fillStyle=v;ctx.fillRect(0,0,W,H);
 // Rain overlay
 ctx.strokeStyle='rgba(151,202,224,.28)';ctx.lineWidth=1;
 for(const r of rain){r.y+=r.s*.016;r.x-=r.s*.003;if(r.y>H){r.y=-20;r.x=rand()*W}ctx.beginPath();ctx.moveTo(r.x,r.y);ctx.lineTo(r.x-3,r.y+r.l);ctx.stroke()}
}
function drawMap(){
 mc.fillStyle='#071511';mc.fillRect(0,0,160,105);
 mc.strokeStyle='#374c3f';mc.lineWidth=8;mc.beginPath();mc.moveTo(0,52);mc.lineTo(160,52);mc.stroke();
 mc.strokeStyle='#514d3a';mc.lineWidth=2;mc.beginPath();mc.moveTo(85,0);mc.lineTo(85,105);mc.stroke();
 for(const b of buildings){mc.fillStyle=b.type==='motel'?'#c38b44':'#587b70';mc.fillRect(b.x/WORLD.w*160,b.y/WORLD.h*105,Math.max(3,b.w/WORLD.w*160),Math.max(3,b.h/WORLD.h*105))}
 for(const c of clues)if(!c.got){mc.fillStyle='#ffce54';mc.fillRect(c.x/WORLD.w*160,c.y/WORLD.h*105,3,3)}
 mc.fillStyle='#fff';mc.fillRect(p.x/WORLD.w*160-2,p.y/WORLD.h*105-2,5,5)
}
function toast(s){const t=document.getElementById('toast');t.textContent=s;t.style.opacity=1;clearTimeout(toast.timer);toast.timer=setTimeout(()=>t.style.opacity=0,2200)}
function dispatch(s){document.getElementById('dispatch').innerHTML='<b>DISPATCH:</b> '+s}
function hud(){
 document.getElementById('hp').style.width=p.hp+'%';document.getElementById('hpnum').textContent=Math.ceil(p.hp)+'%';
 document.getElementById('bat').style.width=p.bat+'%';document.getElementById('batnum').textContent=Math.ceil(p.bat)+'%';
 document.getElementById('ammo').textContent=p.ammo+' / 12';
 let n=clues.filter(c=>c.got).length;
 document.getElementById('objtext').innerHTML=(carChecked?'☑':'□')+' Inspect patrol car<br>'+(n===3?'☑':'□')+' Collect evidence ('+n+'/3)<br>'+(towerFixed?'☑':'□')+' Restore radio tower<br>'+(checkpoint?'☑':'□')+' Reach checkpoint';
}
function nearest(){
 let out=null,best=95;
 for(const b of buildings){let d=dist(p.x,p.y,b.x+b.w/2,b.y+b.h/2);if(d<best){best=d;out={type:b.type,b}}}
 for(const c of clues){let d=dist(p.x,p.y,c.x,c.y);if(!c.got&&d<best){best=d;out={type:'clue',c}}}
 return out;
}
function interact(){
 const n=nearest();if(!n){toast('Nothing nearby to investigate.');return}
 if(n.type==='clue'){n.c.got=true;toast('EVIDENCE: '+n.c.name);dispatch('Evidence secured. I do not like what this implies.');if(clues.every(c=>c.got)){monster.active=true;dispatch('Something just came online near the tower. Get out of there.')}hud();return}
 if(n.type==='car'){carChecked=true;toast('PATROL CAR: blood on the seat. Dash camera missing.');dispatch('This is not the first unit to disappear here.')}
 else if(n.type==='motel'){toast('MOTEL: room six is chained from the outside.');dispatch('Motel owner is missing. Do not enter room six.')}
 else if(n.type==='tower'){towerFixed=true;monster.active=true;toast('RADIO TOWER RESTORED');dispatch('...DO NOT TRUST THE PERSON WALKING BESIDE YOU...')}
 else if(n.type==='checkpoint'){if(clues.filter(c=>c.got).length>=2){checkpoint=true;toast('CHECKPOINT REACHED. CASE TRANSMITTED.');dispatch('Copy, Unit 07. We have your coordinates.')}else toast('Checkpoint locked. Find at least two evidence items.')}
 else toast('Locked. Check the surrounding area.');
 hud();
}
function shoot(){
 if(p.ammo<=0){toast('EMPTY — PRESS R TO RELOAD');return}
 p.ammo--;if(monster.active){let d=dist(p.x,p.y,monster.x,monster.y),a=Math.atan2(monster.y-p.y,monster.x-p.x),diff=Math.atan2(Math.sin(a-p.a),Math.cos(a-p.a));if(d<360&&Math.abs(diff)<.35){monster.stun=2;toast('HIT! IT IS STILL MOVING.')}else toast('Your shot vanishes into the swamp.')}else toast('The gunshot echoes through the trees.');hud();
}
function endGame(win){
 running=false;document.getElementById('overlay').style.display='flex';
 document.querySelector('.kicker').textContent=win?'CASE FILE TRANSMITTED':'SIGNAL LOST';
 document.querySelector('.title').innerHTML=win?'CASE <span>FILED</span>':'UNIT <span>LOST</span>';
 document.querySelector('.desc').innerHTML=win?'Evidence transmitted. Dispatch confirms receipt. The radio is still whispering your name.':'Your radio continues to transmit after your body stops moving. Somewhere in the swamp, another unit receives your call sign.';
 document.getElementById('start').textContent='RESTART NIGHT PATROL';
}
function update(dt){
 time+=dt;p.inv=Math.max(0,p.inv-dt);
 let dx=0,dy=0;
 if(keys.w||keys.ArrowUp)dy--;if(keys.s||keys.ArrowDown)dy++;if(keys.a||keys.ArrowLeft)dx--;if(keys.d||keys.ArrowRight)dx++;
 if(dx||dy){let l=Math.hypot(dx,dy);dx/=l;dy/=l;p.a=Math.atan2(dy,dx);let speed=keys.Shift?220:145;p.x=Math.max(15,Math.min(WORLD.w-15,p.x+dx*speed*dt));p.y=Math.max(15,Math.min(WORLD.h-15,p.y+dy*speed*dt))}
 p.bat=p.flash?Math.max(0,p.bat-dt*.65):Math.min(100,p.bat+dt*.35);if(p.bat<=0)p.flash=false;
 if(monster.active&&monster.stun<=0){let d=dist(p.x,p.y,monster.x,monster.y);if(d<650){monster.x+=(p.x-monster.x)/d*45*dt;monster.y+=(p.y-monster.y)/d*45*dt;if(d<35&&p.inv<=0){p.hp-=13;p.inv=1.2;dispatch('IT IS RIGHT BEHIND YOU. MOVE!');if(p.hp<=0){endGame(false)}}}}else monster.stun=Math.max(0,monster.stun-dt);
 hud();drawMap();if(checkpoint&&clues.every(c=>c.got)&&towerFixed)endGame(true);
}
function loop(ts){let dt=Math.min(.035,(ts-last)/1000||0);last=ts;if(running)update(dt);drawWorld();requestAnimationFrame(loop)}
addEventListener('keydown',e=>{
 let k=e.key.length===1?e.key.toLowerCase():e.key;
 if(['ArrowUp','ArrowDown','ArrowLeft','ArrowRight',' '].includes(e.key))e.preventDefault();keys[k]=true;
 if(!running)return;
 if(k==='e')interact();if(k==='f')p.flash=!p.flash;
 if(k===' '||k==='Spacebar')shoot();if(k==='r'){p.ammo=6;toast('MAGAZINE RELOADED')}
 if(k==='Tab'){e.preventDefault();let o=document.getElementById('objectives');o.style.display=o.style.display==='none'?'block':'none'}
});
addEventListener('keyup',e=>{keys[e.key.length===1?e.key.toLowerCase():e.key]=false});
canvas.addEventListener('mousemove',e=>{if(running)p.a=Math.atan2(e.clientY+camY-p.y,e.clientX+camX-p.x)});
canvas.addEventListener('click',()=>{if(running)shoot()});
document.getElementById('start').addEventListener('click',()=>{
 p.x=540;p.y=840;p.hp=100;p.bat=100;p.ammo=6;p.flash=true;p.inv=0;
 clues.forEach(c=>c.got=false);carChecked=false;towerFixed=false;checkpoint=false;monster.active=false;monster.stun=0;
 running=true;document.getElementById('overlay').style.display='none';
 dispatch('Unit 07, radio check. Abandoned patrol car near Cypress Mile. Proceed with caution.');hud();
});
hud();requestAnimationFrame(loop);
})();
</script>
</body>
</html>"""

@app.route("/")
def home():
    return Response(HTML, mimetype="text/html")

@app.route("/health")
def health():
    return jsonify({"status": "online", "game": "Florida Shadows"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=False)
