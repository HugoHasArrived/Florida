import os
from flask import Flask, render_template_string

app = Flask(**name**)

GAME = r"""

<!DOCTYPE html>

<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Florida Shadows | State Trooper Horror Files</title>
<style>
*{box-sizing:border-box}
body{margin:0;background:#030509;color:#e5e9ed;font-family:Consolas,monospace}
button{background:#101923;color:#e9eff5;border:1px solid #526878;
padding:12px 18px;cursor:pointer;font-family:inherit;letter-spacing:1px}
button:hover{background:#40151e;border-color:#ed4051}
#screen{max-width:1100px;margin:auto;padding:16px}
header{text-align:center;border-bottom:1px solid #293643;padding:12px}
h1{font-size:clamp(30px,6vw,62px);letter-spacing:7px;margin:5px;color:#e8edf2}
h1 span{color:#dc3348}
.sub{color:#7b9cac;letter-spacing:3px;font-size:12px}
#game{width:100%;display:block;background:#050b10;border:1px solid #3b505f;image-rendering:pixelated}
#menu{position:relative;text-align:center;padding:22px 10px}
#menu p{color:#91a2ae;line-height:1.7}
#buttons{display:flex;justify-content:center;gap:8px;flex-wrap:wrap;margin:20px}
#hud{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;
font-size:12px;padding:10px;border:1px solid #273b48;background:#080e15}
#message{min-height:32px;color:#f0bd80;padding:9px 4px;font-size:13px}
#objectives{display:none;background:#080e15;border:1px solid #526878;padding:15px;margin-top:10px}
#objectives h3{color:#df4351}
#notice{color:#718692;font-size:11px;line-height:1.6}
#mobile{display:none;justify-content:space-between;margin-top:10px;gap:8px}
.pad{display:grid;grid-template-columns:repeat(3,45px);gap:4px}
.pad button{padding:10px 0}
@media(max-width:650px){#mobile{display:flex}#screen{padding:5px}#buttons button{padding:10px}}
</style>
</head>
<body>
<div id="screen">
<header>
<h1>FLORIDA <span>SHADOWS</span></h1>
<div class="sub">STATE TROOPER HORROR FILES</div>
</header>

<section id="menu">
<h2 id="menutitle">THE LAST CALL CAME FROM A DEAD OFFICER.</h2>
<p id="description">A fictional pixel-art detective horror experience.<br>
Choose your detective. Investigate the abandoned highway. Find out what happened to Unit 12.</p>
<div id="buttons">
<button onclick="showCharacters()">START CASE</button>
<button onclick="showControls()">FIELD MANUAL</button>
<button onclick="showCredits()">CREDITS</button>
</div>
<p id="privacy">PRIVACY NOTICE: This game does not access your IP address, camera, microphone, or precise location.</p>
</section>

<canvas id="game" width="800" height="450" style="display:none"></canvas>

<div id="hud" style="display:none">
<span id="health">HEALTH: 100%</span>
<span id="ammo">AMMO: 8</span>
<span id="area">HIGHWAY 9</span>
<span id="evidence">EVIDENCE: 0/5</span>
</div>
<div id="message"></div>
<div id="objectives">
<h3>ACTIVE CASE FILE</h3>
<p id="objectiveText"></p>
<button onclick="toggleObjectives()">CLOSE [TAB]</button>
</div>
<div id="mobile">
<div class="pad">
<span></span><button data-key="w">▲</button><span></span>
<button data-key="a">◀</button><button data-key="s">▼</button><button data-key="d">▶</button>
</div>
<div>
<button onclick="interact()">INSPECT</button>
<button onclick="shoot()">FIRE</button>
<button onclick="toggleFlashlight()">LIGHT</button>
</div>
</div>
<p id="notice">CONTROLS: WASD move · SHIFT sprint · E inspect · SPACE fire · F flashlight · TAB objectives · ESC pause.</p>
</div>

<script>
const canvas=document.getElementById('game'),ctx=canvas.getContext('2d');
ctx.imageSmoothingEnabled=false;
const menu=document.getElementById('menu'),hud=document.getElementById('hud');
const objectives=document.getElementById('objectives');
let state='menu',hero='HUGO',tick=0,last=0,keys={},message='',messageTime=0;
let player={x:85,y:300,hp:100,ammo:8,stamina:100,light:true,face:1};
let items=[],monsters=[],evidence=new Set(),found=new Set(),kills=0;
let room='HIGHWAY 9',paused=false,scare=0,scareNext=900;
function say(s){message=s;messageTime=240;document.getElementById('message').textContent=s}
function showCharacters(){
 document.getElementById('menutitle').textContent='CHOOSE YOUR DETECTIVE';
 document.getElementById('description').innerHTML='Two officers. One missing unit. Something is watching.<br><br><button onclick="choose(\'HUGO\')">HUGO — DETECTIVE</button> <button onclick="choose(\'YUMI\')">YUMI — DETECTIVE</button>';
}
function showControls(){
 document.getElementById('menutitle').textContent='FIELD MANUAL';
 document.getElementById('description').innerHTML='WASD: Move · SHIFT: Sprint<br>E: Inspect / enter · SPACE: Fire<br>F: Flashlight · TAB: Case objectives · ESC: Pause<br><br><button onclick="resetMenu()">BACK</button>';
}
function showCredits(){
 document.getElementById('menutitle').textContent='CASE CREDITS';
 document.getElementById('description').innerHTML='FLORIDA SHADOWS<br>A fictional browser horror game built with HTML Canvas.<br>No real police affiliation or endorsement.<br><br><button onclick="resetMenu()">BACK</button>';
}
function resetMenu(){
 document.getElementById('menutitle').textContent='THE LAST CALL CAME FROM A DEAD OFFICER.';
 document.getElementById('description').innerHTML='A fictional pixel-art detective horror experience.<br>Choose your detective. Investigate the abandoned highway. Find out what happened to Unit 12.<br><br><button onclick="showCharacters()">START CASE</button> <button onclick="showControls()">FIELD MANUAL</button> <button onclick="showCredits()">CREDITS</button>';
}
function choose(name){
 hero=name;player={x:85,y:300,hp:100,ammo:8,stamina:100,light:true,face:1};
 evidence=new Set();found=new Set();kills=0;room='HIGHWAY 9';paused=false;
 items=[
 {name:'patrol car',x:110,y:300,type:'car'},
 {name:'dispatch radio',x:145,y:286,type:'evidence'},
 {name:'bloody footprints',x:275,y:330,type:'evidence'},
 {name:'abandoned motel',x:440,y:215,type:'building'},
 {name:'torn uniform patch',x:520,y:190,type:'evidence'},
 {name:'relay tower',x:700,y:130,type:'tower'},
 {name:'witness',x:355,y:360,type:'witness'}
 ];
 monsters=[
 {x:590,y:310,alive:true,cool:0},
 {x:735,y:250,alive:true,cool:2}
 ];
 menu.style.display='none';canvas.style.display='block';hud.style.display='flex';
 state='game';say('DISPATCH: Trooper '+hero+', respond to a missing officer.');
 updateObjectives();requestAnimationFrame(loop);
}
function updateObjectives(){
 document.getElementById('objectiveText').innerHTML=[
 ['Inspect patrol car',found.has('patrol car')],
 ['Recover dispatch radio',found.has('dispatch radio')],
 ['Investigate the motel',found.has('abandoned motel')],
 ['Collect three evidence items',evidence.size>=3],
 ['Find the missing witness',found.has('witness')],
 ['Investigate the relay tower',found.has('relay tower')]
 ].map(([s,done])=>(done?'☑ ':'☐ ')+s).join('<br><br>');
 document.getElementById('evidence').textContent='EVIDENCE: '+evidence.size+'/5';
}
function toggleObjectives(){
 objectives.style.display=objectives.style.display==='block'?'none':'block';
 updateObjectives();
}
function interact(){
 if(state!=='game')return;
 let nearest=null,d=35;
 for(const item of items){
 if(found.has(item.name))continue;
 let dist=Math.hypot(player.x-item.x,player.y-item.y);
 if(dist<d){nearest=item;d=dist}
 }
 if(!nearest){say('Nothing nearby. Search the roadside.');return}
 const n=nearest.name;
 if(n==='patrol car'){
 found.add(n);evidence.add('Blood on patrol car handle');
 say('PATROL CAR: blood on the handle. No officer in sight.');
 }else if(n==='dispatch radio'){
 found.add(n);evidence.add('Corrupted dispatch recording');
 say('RADIO: "Unit 12, do NOT approach the tower. Repeat—"');
 }else if(n==='bloody footprints'||n==='torn uniform patch'){
 found.add(n);evidence.add(n);
 say('Evidence logged. The rain is washing it away.');
 }else if(n==='witness'){
 found.add(n);say('WITNESS: "It wore a trooper uniform. It had no face."');
 }else if(n==='abandoned motel'){
 if(!found.has('patrol car')){say('Search the patrol car before entering.');return}
 found.add(n);room='BAYLIGHT MOTEL';player.x=80;player.y=350;
 items.push({name:'case file',x:250,y:250,type:'evidence'},
 {name:'relay keycard',x:390,y:330,type:'evidence'},
 {name:'inside scratches',x:530,y:260,type:'evidence'});
 say('The motel door creaks open. Something moves upstairs.');
 }else if(n==='relay tower'){
 if(evidence.size<3){say('The tower access panel needs three evidence items.');return}
 found.add(n);say('The relay activates. A voice answers in your own voice.');
 state='ending';drawEnding();return;
 }else{
 found.add(n);evidence.add(n);say('EVIDENCE LOGGED: '+n.toUpperCase());
 }
 updateObjectives();
}
function shoot(){
 if(state!=='game'||paused)return;
 if(player.ammo<=0){say('CLICK. Sidearm empty.');return}
 player.ammo--;
 let target=null,dist=45;
 for(const m of monsters){let d=Math.hypot(player.x-m.x,player.y-m.y);if(m.alive&&d<dist){target=m;dist=d}}
 if(target){target.alive=false;kills++;say('THREAT DOWN. You hope it was human.')}
 else {say('The shot echoes through the swamp. Something answers.')}
 document.getElementById('ammo').textContent='AMMO: '+player.ammo;
}
function toggleFlashlight(){player.light=!player.light;say('FLASHLIGHT '+(player.light?'ON':'OFF'))}
function drawWorld(){
 ctx.fillStyle='#07110f';ctx.fillRect(0,0,800,450);
 // swamp, trees and wet road
 for(let i=0;i<180;i++){
 let x=(i*71)%800,y=(i*43)%450;
 ctx.fillStyle=i%2?'#0d2921':'#10251f';ctx.fillRect(x,y,3,5);
 }
 ctx.fillStyle='#222b32';ctx.beginPath();ctx.moveTo(0,280);ctx.lineTo(150,245);ctx.lineTo(300,275);ctx.lineTo(500,225);ctx.lineTo(800,195);ctx.lineTo(800,260);ctx.lineTo(500,290);ctx.lineTo(300,340);ctx.lineTo(150,310);ctx.lineTo(0,340);ctx.closePath();ctx.fill();
 ctx.strokeStyle='#596166';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(0,280);ctx.lineTo(150,245);ctx.lineTo(300,275);ctx.lineTo(500,225);ctx.lineTo(800,195);ctx.stroke();
 for(const it of items){
 if(found.has(it.name))continue;
 if(it.type==='building'){
 ctx.fillStyle='#28262b';ctx.fillRect(it.x-35,it.y-30,70,60);
 ctx.fillStyle='#57443c';ctx.fillRect(it.x-40,it.y-36,80,9);
 ctx.fillStyle='#07090d';ctx.fillRect(it.x-8,it.y+3,16,27);
 ctx.fillStyle='#8e413c';ctx.fillRect(it.x-25,it.y-15,9,8);ctx.fillRect(it.x+16,it.y-15,9,8);
 }else if(it.type==='tower'){
 ctx.strokeStyle='#717b80';ctx.lineWidth=4;ctx.beginPath();ctx.moveTo(it.x,it.y+30);ctx.lineTo(it.x,it.y-70);ctx.moveTo(it.x-18,it.y-20);ctx.lineTo(it.x+18,it.y-20);ctx.stroke();
 }else if(it.type==='car'){
 ctx.fillStyle='#090d13';ctx.fillRect(it.x-30,it.y-14,60,28);
 ctx.fillStyle='#9ca9ae';ctx.fillRect(it.x-22,it.y-10,44,20);
 ctx.fillStyle=tick%30<15?'#e43749':'#347fff';ctx.fillRect(it.x-8,it.y-18,16,5);
 }else{
 ctx.fillStyle=it.type==='witness'?'#b77b52':'#d33b48';
 ctx.fillRect(it.x-4,it.y-4,8,8);
 }
 }
 for(const m of monsters){
 if(!m.alive)continue;
 ctx.fillStyle='#020306';ctx.fillRect(m.x-10,m.y-23,20,35);
 ctx.fillRect(m.x-13,m.y-34,26,16);
 ctx.fillStyle='#ff243e';ctx.fillRect(m.x-7,m.y-28,5,4);ctx.fillRect(m.x+3,m.y-28,5,4);
 }
 // player sprite
 ctx.fillStyle='#030508';ctx.fillRect(player.x-8,player.y-17,16,27);
 ctx.fillStyle=hero==='HUGO'?'#314c5b':'#51435c';ctx.fillRect(player.x-7,player.y-13,14,20);
 ctx.fillStyle='#b98464';ctx.fillRect(player.x-5,player.y-25,10,12);
 ctx.fillStyle='#14171c';ctx.fillRect(player.x-7,player.y-29,14,6);
 ctx.fillStyle='#e5b35e';ctx.fillRect(player.x-5,player.y-8,4,4);
 // flashlight darkness and visible cone
 ctx.fillStyle=player.light?'rgba(0,0,0,.64)':'rgba(0,0,0,.87)';
 ctx.fillRect(0,0,800,450);
 let light=ctx.createRadialGradient(player.x,player.y,12,player.x,player.y,player.light?150:48);
 light.addColorStop(0,'rgba(0,0,0,0)');light.addColorStop(1,'rgba(0,0,0,.96)');
 ctx.globalCompositeOperation='destination-out';ctx.fillStyle=light;ctx.beginPath();ctx.arc(player.x,player.y,player.light?150:48,0,Math.PI*2);ctx.fill();ctx.globalCompositeOperation='source-over';
 // rain
 ctx.strokeStyle='rgba(126,157,177,.25)';ctx.lineWidth=1;
 for(let i=0;i<90;i++){let x=(i*83+tick*4)%800,y=(i*37+tick*7)%450;ctx.beginPath();ctx.moveTo(x,y);ctx.lineTo(x-4,y+10);ctx.stroke()}
 if(scare>0)drawScare();
}
function drawScare(){
 ctx.fillStyle='#100008';ctx.fillRect(0,0,800,450);
 ctx.fillStyle='#010103';ctx.beginPath();ctx.ellipse(400,235,120,165,0,0,Math.PI*2);ctx.fill();
 ctx.fillStyle='#e3233c';ctx.fillRect(350,190,35,15);ctx.fillRect(415,190,35,15);
 ctx.fillStyle='#f3ece5';ctx.fillRect(355,193,17,7);ctx.fillRect(420,193,17,7);
 ctx.fillStyle='#020103';ctx.fillRect(350,235,100,40);
 ctx.fillStyle='#f1d8ca';for(let i=0;i<8;i++)ctx.fillRect(357+i*11,240,5,20);
 ctx.fillStyle='#ff3049';ctx.font='bold 34px monospace';ctx.textAlign='center';ctx.fillText('OFFICER DOWN',400,85);
}
function drawEnding(){
 drawWorld();ctx.fillStyle='rgba(0,0,0,.9)';ctx.fillRect(40,90,720,260);
 ctx.strokeStyle='#bd3445';ctx.strokeRect(40,90,720,260);
 ctx.fillStyle='#e8edf2';ctx.textAlign='center';ctx.font='bold 32px monospace';ctx.fillText('CASE FILE: OPEN',400,145);
 ctx.fillStyle='#d83a4b';ctx.font='18px monospace';ctx.fillText('THE RELAY IS STILL TRANSMITTING.',400,195);
 ctx.fillStyle='#9caeb9';ctx.font='14px monospace';ctx.fillText('YOU WERE NEVER THE FIRST TROOPER HERE.',400,230);
 ctx.fillText('Refresh the page to investigate again.',400,285);
}
function loop(now){
 if(state!=='game')return;
 const dt=Math.min((now-last)/16.67||1,2);last=now;tick++;
 if(!paused){
 let speed=keys.shift?2.8:1.8;
 let dx=(keys.d||keys.arrowright?1:0)-(keys.a||keys.arrowleft?1:0);
 let dy=(keys.s||keys.arrowdown?1:0)-(keys.w||keys.arrowup?1:0);
 if(dx&&dy){dx*=.707;dy*=.707}
 player.x=Math.max(18,Math.min(782,player.x+dx*speed*dt));
 player.y=Math.max(35,Math.min(430,player.y+dy*speed*dt));
 player.stamina=Math.max(0,Math.min(100,player.stamina+(keys.shift?-0.8:0.3)*dt));
 for(const m of monsters){
 if(!m.alive)continue;
 let vx=player.x-m.x,vy=player.y-m.y,d=Math.hypot(vx,vy);
 if(d<190&&d>1){m.x+=vx/d*.45*dt;m.y+=vy/d*.45*dt}
 if(d<20&&tick%50===0){player.hp=Math.max(0,player.hp-10);say('IT GRABS YOU! RUN!')}
 }
 if(player.hp<=0){
 ctx.fillStyle='#030207';ctx.fillRect(0,0,800,450);ctx.fillStyle='#dc3448';ctx.textAlign='center';ctx.font='bold 38px monospace';ctx.fillText('OFFICER DOWN',400,205);ctx.fillStyle='#ddd';ctx.font='16px monospace';ctx.fillText('Refresh to try again.',400,245);return;
 }
 if(--scareNext<=0){scare=22;scareNext=1100+Math.random()*600}
 if(scare>0)scare--;
 }
 drawWorld();
 document.getElementById('health').textContent='HEALTH: '+player.hp+'%';
 document.getElementById('area').textContent=room;
 document.getElementById('ammo').textContent='AMMO: '+player.ammo;
 if(messageTime>0)messageTime--;else document.getElementById('message').textContent='';
 requestAnimationFrame(loop);
}
window.addEventListener('keydown',e=>{
 const k=e.key.toLowerCase();keys[k]=true;
 if([' ','tab','arrowup','arrowdown','arrowleft','arrowright'].includes(k))e.preventDefault();
 if(k==='e')interact();if(k===' ')shoot();if(k==='f')toggleFlashlight();
 if(k==='tab'&&state==='game'){toggleObjectives()}
 if(k==='escape'&&state==='game'){paused=!paused;say(paused?'INVESTIGATION PAUSED':'BACK ON DUTY')}
});
window.addEventListener('keyup',e=>keys[e.key.toLowerCase()]=false);
document.querySelectorAll('[data-key]').forEach(b=>{
 const k=b.dataset.key;
 b.addEventListener('pointerdown',e=>{e.preventDefault();keys[k]=true});
 ['pointerup','pointerleave','pointercancel'].forEach(ev=>b.addEventListener(ev,()=>keys[k]=false));
});
</script>

</body>
</html>
"""

@app.route("/")
def home():
return render_template_string(GAME)

if **name** == "**main**":
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
