/* ---------- page shell ---------- */
const SLUGS={timecard:'time-card-calculator',hours:'hours-calculator',salary:'hourly-to-salary-calculator',tip:'tip-calculator',percent:'percentage-calculator',loan:'mortgage-calculator',bmi:'bmi-calculator',sleep:'sleep-calculator',age:'age-calculator',days:'days-between-dates',convert:'unit-converter',calorie:'calorie-calculator',gpa:'gpa-calculator',autoloan:'auto-loan-calculator',dice:'dice-roller',lcm:'lcm-calculator',gcf:'gcf-calculator',sqft:'square-footage-calculator'};
let cur=null,lastText='';
function update(){if(!cur)return;try{lastText=cur.calc()||''}catch(e){lastText=''}
  const c=$('#copyRes');if(c)c.onclick=()=>{const done=()=>{c.textContent='Copied';setTimeout(()=>c.textContent='Copy result',1400)};try{navigator.clipboard.writeText(lastText).then(done,()=>{c.textContent=lastText})}catch(e){c.textContent=lastText}}}
function open(id){const t=TOOLS.find(x=>x.id===id),body=$('#toolBody');if(!t||!body)return;cur=t;
  body.innerHTML=t.render();body.querySelectorAll('input,select').forEach(e=>e.addEventListener('input',update));
  t.after&&t.after.call(t);update()}

/* search */
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const q=$('#q'),qres=$('#qres');
function find(s){s=s.trim().toLowerCase();return s?TOOLS.filter(t=>(t.name+' '+t.kw+' '+t.desc+' '+t.cat).toLowerCase().includes(s)):[]}
if(q&&qres){
  q.addEventListener('input',()=>{if(!q.value.trim()){qres.hidden=true;return}const h=find(q.value);
    qres.innerHTML=h.length?h.map(t=>`<a href="/${SLUGS[t.id]}/"><b>${esc(t.name)}</b><span>${esc(t.desc)}</span></a>`).join(''):'<p>No calculator matches that. Try “hours”, “mortgage” or “cups”.</p>';qres.hidden=false});
  q.addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();const h=find(q.value);if(h[0])location.href='/'+SLUGS[h[0].id]+'/'}else if(e.key==='Escape'){qres.hidden=true;q.blur()}});
  document.addEventListener('click',e=>{if(!e.target.closest('.search'))qres.hidden=true});
}

/* region */
const reg=$('#region');
if(reg){reg.value=region;reg.addEventListener('change',()=>{region=reg.value;store.set('region',region);
  const tc=store.get('tc',null);if(tc){tc.ot=null;store.set('tc',tc)}
  TOOLS.forEach(t=>{if(t.state){if('sys' in t.state)t.state.sys=null;if('unit' in t.state)t.state.unit=null}});
  if(cur)open(cur.id)})}

/* theme */
const root=document.documentElement,tb=$('#themeBtn');
const isDark=()=>{const a=root.getAttribute('data-theme');return a?a==='dark':matchMedia('(prefers-color-scheme: dark)').matches};
function paint(){if(!tb)return;const d=isDark();tb.dataset.mode=d?'dark':'light';$('#themeLabel').textContent=d?'Dark':'Light';tb.setAttribute('aria-pressed',String(d))}
if(tb){tb.addEventListener('click',()=>{const t=isDark()?'light':'dark';root.setAttribute('data-theme',t);store.set('theme',t);paint()});paint();
  try{matchMedia('(prefers-color-scheme: dark)').addEventListener('change',paint)}catch(e){}}

const tbody=$('#toolBody');if(tbody)open(tbody.dataset.tool);
})();
