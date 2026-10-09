
import os
from flask import Flask, Response, jsonify

app = Flask(__name__)

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Florida Shadows — State Trooper Horror Files</title>
<style>
*{box-sizing:border-box}
body{margin:0;background:#050807;color:#e6e8dc;font-family:Consolas,monospace}
canvas{display:block;width:100%;height:100%;position:fixed;inset:0;image-rendering:pixelated}
#menu{position:fixed;inset:0;display:grid;place-items:center;background:#050807d9;padding:20px}
.card{max-width:650px;width:100%;padding:30px;background:#0b100df2;border:1px solid #455147;box-shadow:0 0 70px #000}
.tag{color:#c34b4b;letter-spacing:4px;font-size:12px}
h1{font-size:clamp(38px,8vw,68px);line-height:.95;margin:18px 0;text-shadow:4px 4px #541b20}
h2{color:#d2b878}
p{line-height:1.6;color:#bdc5bc}
button{background:#202a22;color:#fff;border:1px solid #677568;padding:13px 20px;font:inherit;cursor:pointer;margin:5px 5px 5px 0}
button:hover{background:#374738}
.primary{background:#76272d;border-color:#bd5a5a}
#hud{display:none;position:fixed;inset:0;pointer-events:none}
.box{position:absolute;top:12px;left:12px;background:#080c0be0;padding:12px;border:1px solid #4c584e;font-size:12px;line-height:1.7}
#objectives{left:auto;right:12px;max-width:250px}
#hint{position:absolute;bottom:18px;left:50%;transform:translateX(-50%);background:#080c0be8;padding:12px;text-align:center;max-width:95%;font-size:12px}
#message{position:absolute;top:25%;left:10%;right:10%;text-align:center;color:#f1d9a3;text-shadow:2px 2px #000}
</style>
</head>
<body>
<canvas id="game"></canvas>
<div id="menu"><div class="card">
<div class="tag">FLORIDA • INCIDENT REPORT 09-17</div>
<h1>FLORIDA<br>SHADOWS</h1>
<h2>STATE TROOPER HORROR FILES</h2>
<p>One abandoned highway. One unanswered radio call. Something in the swamp knows your name.</p>
<p>Investigate the abandoned patrol car, explore the roadside motel, collect evidence, restore the radio tower, and reach the checkpoint before the darkness finds you.</p>
<button class="primary" onclick="start()">▶ BEGIN PATROL</button>
<button onclick="help()">FIELD MANUAL</button>
<p style="font-size:11px">Fictional horror game. No real location, camera, microphone, or IP data is accessed by this game.</p>
</div></div>
<div id="hud">
<div class="box" id="status">UNIT 07 — NIGHT SHIFT<br>CONDITION: <span id="hp">100</span>%<br>FLASHLIGHT: <span id="battery">100</span>%<br>AMMO: <span id="ammo">6</span></div>
<div class="box" id="objectives">CASE OBJECTIVES<div id="tasks"></div></div>
<div id="message"></div>
<div id="hint">WASD MOVE • E INVESTIGATE • F FLASHLIGHT • SPACE FIRE • SHIFT SPRINT</div>
</div>
<script>
const c=document.getElementById('game'),ctx=c.getContext('2d');
let W,H,active=false,flash=true,hp=100,battery=100,ammo=6,evidence=0,radio=false,car=false,won=false;
let p={x:200,y:200,face:0},cam={x:0,y:0},time=0,keys={},last=0,msg='';
const map={w:2200,h:1600};
const things=[
{x:300,y:250,w:100,h:55,type:'car',name:'Abandoned patrol car'},
{x:510,y:370,w:48,h:40,type:'evidence',name:'Bloody footprints'},
{x:820,y:290,w:110,h:85,type:'motel',name:'Roadside motel'},
{x:990,y:420,w:48,h:40,type:'evidence',name:'Guest ledger'},
{x:1420,y:670,w:70,h:70,type:'tower',name:'Emergency relay tower'},
{x:1720,y:1130,w:90,h:65,type:'exit',name:'County checkpoint'},
{x:690,y:970,w:48,h:40,type:'evidence',name:'Field recorder'}
];
let monster={x:1050,y:800,awake:false};
function resize(){W=innerWidth;H=innerHeight;c.width=W*devicePixelRatio;c.height=H*devicePixelRatio;c.style.width=W+'px';c.style.height=H+'px';ctx.setTransform(devicePixelRatio,0,0,devicePixelRatio,0,0)}
onresize=resize;resize();
function start(){document.getElementById('menu').style.display='none';document.getElementById('hud').style.display='block';active=true;last=performance.now();message('Dispatch: Unit 07, investigate the abandoned motel. Do you copy?')}
function help(){alert('WASD or arrow keys: move\\nSHIFT: sprint\\nE: investigate\\nF: flashlight\\nSPACE: fire\\nR: reload\\nTAB: objectives\\nESC: pause')}
function message(s){msg=s;document.getElementById('message').textContent=s}
function nearest(){let best=null,dmin=90;for(const o of things){if(o.done)continue;let d=Math.hypot(p.x-o.x-o.w/2,p.y-o.y-o.h/2);if(d<dmin){best=o;dmin=d}}return best}
function interact(){
 const o=nearest();if(!o){message('Nothing nearby. Follow the road and search for evidence.');return}
 if(o.type==='car'){car=true;ammo=Math.min(12,ammo+3);o.done=true;message('The patrol car radio crackles. A torn report says: DO NOT ENTER THE TREE LINE.');}
 else if(o.type==='evidence'){evidence++;o.done=true;message(o.name+' collected. Evidence: '+evidence+'/3');}
 else if(o.type==='motel'){o.done=true;battery=Math.min(100,battery+15);message('The motel office is abandoned. Scratches cover the inside of the locked door.');}
 else if(o.type==='tower'){radio=true;o.done=true;monster.awake=true;message('RADIO RESTORED. Dispatch answers — then another voice whispers your name.');}
 else if(o.type==='exit'){if(radio&&evidence>=3){won=true;active=false;message('YOU SURVIVED — dispatch has received your transmission. Refresh to play again.')}else message('Checkpoint locked. Restore the radio and collect 3 evidence items.')}
 updateTasks()
}
function updateTasks(){document.getElementById('tasks').innerHTML=[['Inspect patrol car',car],['Collect 3 evidence',evidence>=3],['Restore radio tower',radio],['Reach checkpoint',won]].map(x=>'<div style="margin-top:6px">'+(x[1]?'[✓] ':'[ ] ')+x[0]+'</div>').join('')}
function shoot(){if(!active)return;if(ammo<=0){message('Out of ammunition. Press R to reload.');return}ammo--;if(Math.hypot(p.x-monster.x,p.y-monster.y)<280){monster.awake=false;monster.x=-500;message('The shadow collapses into the swamp.')}else message('BANG! The sound echoes through the trees.')}
onkeydown=e=>{let k=e.key.toLowerCase();keys[k]=true;if([' ','tab','arrowup','arrowdown','arrowleft','arrowright'].includes(k))e.preventDefault();if(k==='e')interact();if(k==='f')flash=!flash;if(k===' ')shoot();if(k==='r'){ammo=6;message('Magazine reloaded.')}if(k==='tab')message('Objectives: patrol car, 3 evidence items, relay tower, checkpoint.');if(k==='escape'&&active){active=false;message('PAUSED — press ENTER to resume.')}if(k==='enter'&&!active&&!won){active=true;last=performance.now()}};
onkeyup=e=>keys[e.key.toLowerCase()]=false;
function blocked(x,y){if(x<20||y<20||x>map.w-20||y>map.h-20)return true;return things.some(o=>['car','motel','tower','exit'].includes(o.type)&&x>o.x-15&&x<o.x+o.w+15&&y>o.y-15&&y<o.y+o.h+15)}
function update(dt){
 if(!active)return;time+=dt;
 let dx=0,dy=0;if(keys.w||keys.arrowup)dy--;if(keys.s||keys.arrowdown)dy++;if(keys.a||keys.arrowleft)dx--;if(keys.d||keys.arrowright)dx++;
 let l=Math.hypot(dx,dy)||1,speed=keys.shift?210:135;dx=dx/l*speed*dt;dy=dy/l*speed*dt;
 if(dx||dy)p.face=Math.atan2(dy,dx);
 if(!blocked(p.x+dx,p.y))p.x+=dx;if(!blocked(p.x,p.y+dy))p.y+=dy;
 if(flash)battery=Math.max(0,battery-dt);else battery=Math.min(100,battery+dt*2);if(!battery)flash=false;
 if(monster.awake){let d=Math.hypot(p.x-monster.x,p.y-monster.y);if(d<500){let a=Math.atan2(p.y-monster.y,p.x-monster.x);monster.x+=Math.cos(a)*40*dt;monster.y+=Math.sin(a)*40*dt;if(d<30)hp=Math.max(0,hp-dt*18);if(hp<=0){active=false;message('OFFICER DOWN — refresh to restart the patrol.')}}}
 cam.x=Math.max(0,Math.min(map.w-W,p.x-W/2));cam.y=Math.max(0,Math.min(map.h-H,p.y-H/2));
 document.getElementById('hp').textContent=Math.round(hp);document.getElementById('battery').textContent=Math.round(battery);document.getElementById('ammo').textContent=ammo;
 document.getElementById('hint').textContent=nearest()?'E — INVESTIGATE: '+nearest().name:'WASD MOVE • SHIFT SPRINT • E INVESTIGATE • F FLASHLIGHT • SPACE FIRE';
}
function rect(x,y,w,h,col){ctx.fillStyle=col;ctx.fillRect(x,y,w,h)}
function draw(){
 rect(0,0,W,H,'#101711');ctx.save();ctx.translate(-cam.x,-cam.y);
 for(let y=0;y<map.h;y+=32)for(let x=0;x<map.w;x+=32){rect(x,y,30,30,((x*7+y*11)%5)?'#111a13':'#172019')}
 ctx.strokeStyle='#303532';ctx.lineWidth=95;ctx.beginPath();ctx.moveTo(50,60);ctx.lineTo(350,300);ctx.lineTo(720,420);ctx.lineTo(1030,650);ctx.lineTo(1300,850);ctx.lineTo(1720,1160);ctx.stroke();
 ctx.strokeStyle='#9b9477';ctx.lineWidth=2;ctx.setLineDash([22,22]);ctx.stroke();ctx.setLineDash([]);
 for(let i=0;i<150;i++){let x=(i*137+30)%map.w,y=(i*223+60)%map.h;rect(x-12,y-18,24,27,'#17251a');rect(x-7,y-24,14,12,'#223023')}
 for(const o of things){rect(o.x,o.y,o.w,o.h,o.type==='evidence'?'#66302d':o.type==='motel'?'#39352b':o.type==='tower'?'#596158':o.type==='exit'?'#6b6042':'#26322d');rect(o.x+5,o.y+5,o.w-10,5,'#737a6d');if(o.type==='car'){rect(o.x+15,o.y+12,o.w-30,22,'#526158');rect(o.x+10,o.y+o.h-5,20,10,'#080a09');rect(o.x+o.w-30,o.y+o.h-5,20,10,'#080a09')}if(o.type==='motel'){for(let i=0;i<3;i++)rect(o.x+12+i*30,o.y+28,18,18,'#98825a')}if(o.type==='tower'){rect(o.x+o.w/2-3,o.y-80,6,150,'#737e72');for(let i=0;i<4;i++)rect(o.x+8,o.y-60+i*30,o.w-16,3,'#737e72')}if(!o.done)rect(o.x+o.w/2-2,o.y-8,5,5,'#e6cb77');}
 if(monster.x>0){rect(monster.x-10,monster.y-25,20,42,'#050606');rect(monster.x-13,monster.y-35,26,18,'#070908');rect(monster.x-7,monster.y-28,4,3,'#bd2525');rect(monster.x+4,monster.y-28,4,3,'#bd2525')}
 rect(p.x-6,p.y-8,12,17,'#c0c1ae');rect(p.x-5,p.y-16,10,10,'#343b35');rect(p.x-8,p.y-4,16,5,'#607263');
 ctx.restore();
 ctx.fillStyle=flash&&battery>0?'rgba(0,0,0,.72)':'rgba(0,0,0,.94)';ctx.fillRect(0,0,W,H);
 if(flash&&battery>0){let x=p.x-cam.x,y=p.y-cam.y,g=ctx.createRadialGradient(x,y,10,x,y,270);g.addColorStop(0,'rgba(0,0,0,0)');g.addColorStop(1,'rgba(0,0,0,.98)');ctx.globalCompositeOperation='destination-out';ctx.fillStyle=g;ctx.fillRect(0,0,W,H);ctx.globalCompositeOperation='source-over'}
 ctx.strokeStyle='#9aada8';ctx.lineWidth=1;for(let i=0;i<65;i++){let x=(i*91+time*160)%W,y=(i*53+time*260)%H;ctx.beginPath();ctx.moveTo(x,y);ctx.lineTo(x-4,y+9);ctx.stroke()}
}
function loop(t){let dt=Math.min((t-last)/1000||0,.04);last=t;update(dt);draw();requestAnimationFrame(loop)}
updateTasks();requestAnimationFrame(loop);
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
