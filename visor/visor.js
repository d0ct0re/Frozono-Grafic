// Visor de presentaciones semanales. Lee slides.json de la carpeta de la semana.
// slides.json: {"titulo":"…","slides":[{"img":"img/01.jpg"},{"img":"img/18.jpg","live":"live/x.html"},{"img":"img/05.jpg","anim":"zoom"}]}
(async function(){
const base=document.currentScript?document.currentScript.src:"";
const res=await fetch("slides.json",{cache:"no-cache"}); const cfg=await res.json();
document.title=cfg.titulo||document.title;
document.body.innerHTML=`<div id="stage"></div><div id="bar"><span class="ttl"></span>
<a href="../../" title="Todas las presentaciones">☰ Semanas</a><button id="prev" title="Anterior (←)">‹</button><span id="num"></span>
<button id="next" title="Siguiente (→)">›</button><button id="gbtn" title="Ver todas (G)">▦</button><button id="full" title="Pantalla completa (F)">⛶</button>
<span id="help">← → avanzar · G índice · F pantalla completa</span></div><div id="prog"></div><div id="grid"><div class="g"></div></div>`;
document.querySelector(".ttl").textContent=cfg.titulo||"";
const S=cfg.slides, stage=document.getElementById("stage"), els=[];
S.forEach((s,i)=>{const d=document.createElement("div");d.className="slide"+(s.anim?" anim-"+s.anim:"");
  const im=new Image();im.alt="Diapositiva "+(i+1);im.decoding="async";if(i<3)im.src=s.img;else im.dataset.src=s.img;d.appendChild(im);
  if(s.live){d.dataset.live=s.live;const t=document.createElement("span");t.className="tag";t.textContent="Interactiva";d.appendChild(t)}
  stage.appendChild(d);els.push(d)});
let cur=-1;
const load=k=>{const d=els[k];if(!d)return;const im=d.querySelector("img");if(im&&im.dataset.src){im.src=im.dataset.src;delete im.dataset.src}};
function hook(f){try{f.contentWindow.document.addEventListener("keydown",key)}catch(e){}}
function go(n){
  n=Math.max(0,Math.min(S.length-1,n)); if(n===cur)return;
  if(cur>=0)els[cur].classList.remove("on"); cur=n; const d=els[cur]; load(cur);load(cur+1);load(cur+2);load(cur-1);
  if(d.dataset.live){let f=d.querySelector("iframe");
    if(!f){f=document.createElement("iframe");f.src=d.dataset.live;f.title="Gráfica interactiva";
      f.onload=()=>{hook(f);f.contentWindow.postMessage("play","*");setTimeout(()=>{const im=d.querySelector("img");if(im)im.style.visibility="hidden"},150)};d.insertBefore(f,d.querySelector(".tag"))}
    else f.contentWindow.postMessage("play","*");}
  d.classList.remove("on");void d.offsetWidth;d.classList.add("on");
  document.getElementById("num").textContent=(cur+1)+" / "+S.length;
  document.getElementById("prog").style.width=((cur+1)/S.length*100)+"%";
  history.replaceState(null,"","#"+(cur+1));
  document.querySelectorAll("#grid .t").forEach((t,k)=>t.classList.toggle("cur",k===cur));
}
const grid=document.getElementById("grid"), g=grid.querySelector(".g");
S.forEach((s,i)=>{const t=document.createElement("div");t.className="t";t.innerHTML=`<img loading="lazy" src="${s.thumb||s.img}"><span>${i+1}</span>${s.live?"<b>Interactiva</b>":""}`;
  t.onclick=()=>{grid.classList.remove("on");go(i)};g.appendChild(t)});
const toggleGrid=()=>grid.classList.toggle("on");
function key(e){
  if(grid.classList.contains("on")){if(e.key==="Escape"||e.key==="g"||e.key==="G")toggleGrid();return}
  if(["ArrowRight","PageDown"," ","Enter","ArrowDown"].includes(e.key)){e.preventDefault();go(cur+1)}
  else if(["ArrowLeft","PageUp","Backspace","ArrowUp"].includes(e.key)){e.preventDefault();go(cur-1)}
  else if(e.key==="Home")go(0);else if(e.key==="End")go(S.length-1);
  else if(e.key==="f"||e.key==="F")full();else if(e.key==="g"||e.key==="G")toggleGrid();
}
function full(){if(!document.fullscreenElement)document.documentElement.requestFullscreen().catch(()=>{});else document.exitFullscreen()}
document.addEventListener("fullscreenchange",()=>document.body.classList.toggle("fs",!!document.fullscreenElement));
document.addEventListener("keydown",key);
document.getElementById("prev").onclick=()=>go(cur-1);document.getElementById("next").onclick=()=>go(cur+1);
document.getElementById("full").onclick=full;document.getElementById("gbtn").onclick=toggleGrid;
let tx=null;stage.addEventListener("touchstart",e=>tx=e.touches[0].clientX,{passive:true});
stage.addEventListener("touchend",e=>{if(tx===null)return;const dx=e.changedTouches[0].clientX-tx;if(Math.abs(dx)>50)go(cur+(dx<0?1:-1));tx=null});
go((parseInt(location.hash.slice(1))||1)-1);
})();
