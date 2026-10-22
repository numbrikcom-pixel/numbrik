/* Numbrik calculators — numbrik.com */
(function(){
const $=s=>document.querySelector(s);
const store={get(k,d){try{const v=localStorage.getItem('nb_'+k);return v?JSON.parse(v):d}catch(e){return d}},set(k,v){try{localStorage.setItem('nb_'+k,JSON.stringify(v))}catch(e){}}};

const REGIONS={
  US:{cur:'USD',loc:'en-US',imperial:true,ot:40,otNote:'US federal rule: 1.5× pay after 40 hours a week.'},
  CA:{cur:'CAD',loc:'en-CA',imperial:false,ot:44,otNote:'Ontario uses 44 hrs/week. Other provinces differ (BC and Alberta also count daily 8 hrs).'},
  AU:{cur:'AUD',loc:'en-AU',imperial:false,ot:38,otNote:'Most awards pay overtime after 38 ordinary hours. Check your award.'},
  UK:{cur:'GBP',loc:'en-GB',imperial:false,ot:0,otNote:'No legal overtime premium in the UK. Set a threshold if your contract has one.'},
  NL:{cur:'EUR',loc:'nl-NL',imperial:false,ot:0,otNote:'No statutory overtime premium. Your CAO may set one.'}
};
let region=store.get('region',null)||(()=>{const l=(navigator.language||'').toUpperCase();if(l.endsWith('CA'))return'CA';if(l.endsWith('AU'))return'AU';if(l.endsWith('GB'))return'UK';if(l.startsWith('NL'))return'NL';return'US'})();
const R=()=>REGIONS[region];
const money=(n,d=2)=>isFinite(n)?new Intl.NumberFormat(R().loc,{style:'currency',currency:R().cur,minimumFractionDigits:d,maximumFractionDigits:d}).format(n):'—';
const num=(n,d=2)=>isFinite(n)?new Intl.NumberFormat(R().loc,{maximumFractionDigits:d}).format(n):'—';
const hm=h=>{if(!isFinite(h))return'—';const m=Math.round(h*60);return Math.floor(m/60)+'h '+String(m%60).padStart(2,'0')+'m'};
const toMin=t=>{if(!t)return null;const[a,b]=t.split(':').map(Number);return a*60+b};
const fmtClock=min=>{min=((min%1440)+1440)%1440;const d=new Date(2000,0,1,Math.floor(min/60),min%60);return d.toLocaleTimeString(R().loc,{hour:'numeric',minute:'2-digit'})};
const v=id=>{const e=document.getElementById(id);return e?parseFloat(e.value):NaN};

function field(id,label,val,opts={}){
  const t=opts.type||'number';
  const inp=`<input id="${id}" type="${t}" value="${val}" ${opts.step?`step="${opts.step}"`:t==='number'?'step="any"':''} inputmode="${t==='number'?'decimal':'text'}">`;
  return `<div class="field"><label for="${id}">${label}</label>${opts.unit?`<div class="unit">${inp}<span>${opts.unit}</span></div>`:inp}</div>`;
}
function kv(pairs){return '<dl class="kv">'+pairs.map(([k,v])=>`<div><dt>${k}</dt><dd>${v}</dd></div>`).join('')+'</dl>'}
function seg(id,opts,cur){return `<div class="seg" id="${id}" role="group">`+opts.map(([val,lab])=>`<button type="button" data-v="${val}" aria-pressed="${val===cur}">${lab}</button>`).join('')+'</div>'}
function bindSeg(id,cb){const el=document.getElementById(id);el.addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;el.querySelectorAll('button').forEach(x=>x.setAttribute('aria-pressed',x===b));cb(b.dataset.v)})}
const copyBtn='<button class="copy" type="button" id="copyRes">Copy result</button>';

/* ---------- TOOLS ---------- */
const DAYS=['Mon','Tue','Wed','Thu','Fri','Sat','Sun'];
const SAMPLE=[['09:00','17:30',30],['09:00','17:30',30],['08:30','18:00',45],['09:00','17:30',30],['09:00','16:00',30],['10:00','14:00',0],['','',0]];

const TOOLS=[
{id:'timecard',cat:'Work & pay',name:'Time card',kw:'timesheet hours worked overtime shift clock in out weekly',desc:'Weekly hours, overtime and gross pay.',
 render(){const s=store.get('tc',null);const rows=s?s.rows:SAMPLE;const rate=s?s.rate:22.5;const ot=s&&s.ot!=null?s.ot:R().ot;const mult=s?s.mult:1.5;
  return `<div class="inputs">
   <div class="tc-wrap"><table><thead><tr><th>Day</th><th>Start</th><th>End</th><th>Break (min)</th><th style="text-align:right">Hours</th></tr></thead><tbody>
   ${DAYS.map((d,i)=>`<tr><td class="day">${d}</td><td><input type="time" id="tcs${i}" value="${rows[i][0]}"></td><td><input type="time" id="tce${i}" value="${rows[i][1]}"></td><td><input type="number" min="0" id="tcb${i}" value="${rows[i][2]}" inputmode="numeric"></td><td class="num" id="tch${i}">—</td></tr>`).join('')}
   </tbody></table></div>
   <div class="row">${field('rate','Hourly rate',rate,{unit:R().cur})}${field('otat','Overtime after',ot,{unit:'hrs'})}${field('otx','Overtime rate',mult,{unit:'×'})}</div>
   <p class="hint" id="otnote">${R().otNote} Shifts past midnight count automatically. Your entries are saved in this browser.</p>
   <div class="actions"><button class="btn" type="button" id="tcclear">Clear week</button><button class="btn" type="button" id="tcsample">Load example week</button></div>
  </div><div class="result" id="out"></div>`},
 calc(){let total=0;const rows=[];
  DAYS.forEach((d,i)=>{const s=toMin($('#tcs'+i).value),e=toMin($('#tce'+i).value),b=parseFloat($('#tcb'+i).value)||0;let h=0;
   if(s!=null&&e!=null){let m=e-s;if(m<=0)m+=1440;h=Math.max(0,(m-b)/60)}
   $('#tch'+i).textContent=h?hm(h):'—';total+=h;rows.push([$('#tcs'+i).value,$('#tce'+i).value,b])});
  const rate=v('rate'),otAt=v('otat'),mult=v('otx');
  const ot=otAt>0?Math.max(0,total-otAt):0,reg=total-ot,pay=reg*rate+ot*rate*(mult||1);
  store.set('tc',{rows,rate,ot:isNaN(otAt)?null:otAt,mult});
  $('#out').innerHTML=`<span class="label">Gross pay this week</span><div class="big"><em>${money(pay)}</em></div>
   ${kv([['Total hours',hm(total)],['Decimal hours',num(total)],['Regular',hm(reg)],['Overtime',hm(ot)],['Regular pay',money(reg*rate)],['Overtime pay',money(ot*rate*(mult||1))]])}${copyBtn}`;
  return `Time card: ${num(total)} hrs (${num(ot)} OT), gross pay ${money(pay)}`},
 after(){ $('#tcclear').onclick=()=>{DAYS.forEach((d,i)=>{$('#tcs'+i).value='';$('#tce'+i).value='';$('#tcb'+i).value=0});update()};
  $('#tcsample').onclick=()=>{SAMPLE.forEach((r,i)=>{$('#tcs'+i).value=r[0];$('#tce'+i).value=r[1];$('#tcb'+i).value=r[2]});update()} }},

{id:'hours',cat:'Work & pay',name:'Hours between times',kw:'hours calculator time duration shift length',desc:'How long between two clock times.',
 render(){return `<div class="inputs"><div class="row">${field('h1','Start time','08:45',{type:'time'})}${field('h2','End time','17:15',{type:'time'})}${field('hb','Unpaid break',30,{unit:'min'})}</div><p class="hint">End earlier than start counts as an overnight shift.</p></div><div class="result" id="out"></div>`},
 calc(){const s=toMin($('#h1').value),e=toMin($('#h2').value);let m=e-s;if(m<=0)m+=1440;m-= (v('hb')||0);const h=Math.max(0,m/60);
  $('#out').innerHTML=`<span class="label">Time worked</span><div class="big"><em>${hm(h)}</em></div>${kv([['Decimal hours',num(h)],['Minutes',num(h*60,0)]])}${copyBtn}`;return `${hm(h)} (${num(h)} hrs)`}},

{id:'salary',cat:'Work & pay',name:'Hourly ↔ salary',kw:'hourly to salary annual wage converter how much a year per hour',desc:'Convert hourly wage to yearly, monthly and weekly pay.',
 state:{mode:'hourly'},
 render(){const st=this.state;return `<div class="inputs">${seg('smode',[['hourly','I know my hourly rate'],['annual','I know my salary']],st.mode)}
  <div class="row">${field('samt',st.mode==='hourly'?'Hourly rate':'Annual salary',st.mode==='hourly'?25:52000,{unit:R().cur})}${field('shw','Hours per week',region==='AU'?38:40,{unit:'hrs'})}${field('swy','Paid weeks per year',52,{unit:'wks'})}</div>
  <p class="hint">Gross pay before tax and deductions.</p></div><div class="result" id="out"></div>`},
 calc(){const a=v('samt'),hw=v('shw'),wy=v('swy');const yr=this.state.mode==='hourly'?a*hw*wy:a;const hr=yr/(hw*wy);
  $('#out').innerHTML=`<span class="label">${this.state.mode==='hourly'?'Per year':'Per hour'}</span><div class="big"><em>${this.state.mode==='hourly'?money(yr,0):money(hr)}</em></div>
  ${kv([['Hourly',money(hr)],['Daily (5-day week)',money(yr/wy/5)],['Weekly',money(yr/wy)],['Every 2 weeks',money(yr/wy*2)],['Monthly',money(yr/12)],['Yearly',money(yr,0)]])}${copyBtn}`;return `${money(hr)}/hr = ${money(yr,0)}/yr`},
 after(){bindSeg('smode',m=>{this.state.mode=m;open('salary')})}},

{id:'tip',cat:'Money',name:'Tip & split',kw:'tip gratuity restaurant bill split people',desc:'Tip amount and each person’s share.',
 render(){return `<div class="inputs"><div class="row">${field('tb','Bill total',86.4,{unit:R().cur})}${field('tp','Tip',region==='US'||region==='CA'?18:10,{unit:'%'})}${field('tn','People',3)}</div>
  <div class="actions">${[10,15,18,20,25].map(p=>`<button class="btn" type="button" data-tip="${p}">${p}%</button>`).join('')}</div></div><div class="result" id="out"></div>`},
 calc(){const b=v('tb'),p=v('tp'),n=Math.max(1,v('tn')||1);const t=b*p/100;
  $('#out').innerHTML=`<span class="label">Each person pays</span><div class="big"><em>${money((b+t)/n)}</em></div>${kv([['Tip',money(t)],['Total with tip',money(b+t)],['Tip per person',money(t/n)]])}${copyBtn}`;return `Each pays ${money((b+t)/n)}`},
 after(){document.querySelectorAll('[data-tip]').forEach(x=>x.onclick=()=>{$('#tp').value=x.dataset.tip;update()})}},

{id:'percent',cat:'Money',name:'Percentage',kw:'percent percentage change increase decrease discount of',desc:'Percent of, percent change, and what-percent.',
 state:{mode:'of'},
 render(){const m=this.state.mode;const L={of:['Percent','Of number',15,240],what:['Number','Is what % of',45,180],chg:['From','To',80,100]}[m];
  return `<div class="inputs">${seg('pmode',[['of','X% of Y'],['what','X is what % of Y'],['chg','% change']],m)}<div class="row">${field('pa',L[0],L[2])}${field('pb',L[1],L[3])}</div></div><div class="result" id="out"></div>`},
 calc(){const a=v('pa'),b=v('pb'),m=this.state.mode;let big,rest;
  if(m==='of'){const r=a/100*b;big=num(r,4);rest=[['Added to '+num(b),num(b+r,4)],['Taken from '+num(b),num(b-r,4)]]}
  else if(m==='what'){big=num(a/b*100,4)+'%';rest=[['Remaining',num(100-a/b*100,4)+'%']]}
  else{const c=(b-a)/Math.abs(a)*100;big=(c>0?'+':'')+num(c,4)+'%';rest=[['Difference',num(b-a,4)],['Direction',c>0?'Increase':c<0?'Decrease':'No change']]}
  $('#out').innerHTML=`<span class="label">Result</span><div class="big"><em>${big}</em></div>${kv(rest)}${copyBtn}`;return big},
 after(){bindSeg('pmode',m=>{this.state.mode=m;open('percent')})}},

{id:'loan',cat:'Money',name:'Loan & mortgage',kw:'mortgage loan car auto payment interest amortization emi home',desc:'Monthly payment, total interest and payoff by year.',
 render(){return `<div class="inputs"><div class="row">${field('la','Loan amount',350000,{unit:R().cur})}${field('lr','Interest rate',6.5,{unit:'%'})}${field('ly','Term',30,{unit:'yrs'})}</div>
  <div id="amort"></div></div><div class="result" id="out"></div>`},
 calc(){const P=v('la'),r=v('lr')/1200,n=Math.round(v('ly')*12);const pm=r?P*r/(1-Math.pow(1+r,-n)):P/n;const tot=pm*n;
  $('#out').innerHTML=`<span class="label">Monthly payment</span><div class="big"><em>${money(pm)}</em></div>${kv([['Total of payments',money(tot,0)],['Total interest',money(tot-P,0)],['Payments',num(n,0)]])}${copyBtn}`;
  let bal=P,yrs=[];for(let y=1;y<=Math.ceil(n/12);y++){let pi=0,ii=0;for(let k=0;k<12&&bal>0.005;k++){const i=bal*r;const p=Math.min(pm-i,bal);ii+=i;pi+=p;bal-=p}yrs.push([y,pi,ii,bal])}
  const step=Math.max(1,Math.ceil(yrs.length/10));const show=yrs.filter((x,i)=>i%step===0||i===yrs.length-1);
  $('#amort').innerHTML=yrs.length?`<div class="field"><label>Where each year’s payments go</label></div><div class="legend"><span><i style="background:var(--accent)"></i>Principal</span><span><i style="background:var(--mark)"></i>Interest</span></div>
   <div class="bars">${show.map(([y,p,i,b])=>`<div class="barrow"><span>Yr ${y}</span><div class="track"><div class="p" style="width:${p/(p+i)*100}%"></div><div class="i" style="width:${i/(p+i)*100}%"></div></div><span style="text-align:right">${money(b,0)} left</span></div>`).join('')}</div>`:'';
  return `${money(pm)}/month`}},

{id:'bmi',cat:'Health',name:'BMI',kw:'bmi body mass index weight height healthy',desc:'Body mass index with the WHO category.',
 state:{sys:null},
 render(){const s=this.state.sys||(R().imperial?'imp':'met');this.state.sys=s;
  return `<div class="inputs">${seg('bsys',[['imp','ft / lb'],['met','cm / kg']],s)}<div class="row">${s==='imp'?field('bft','Height',5,{unit:'ft'})+field('bin','',9,{unit:'in'})+field('bw','Weight',165,{unit:'lb'}):field('bcm','Height',175,{unit:'cm'})+field('bw','Weight',72,{unit:'kg'})}</div>
  <p class="hint">BMI is a screening number for adults. It does not measure body fat directly.</p></div><div class="result" id="out"></div>`},
 calc(){let m,kg;if(this.state.sys==='imp'){m=((v('bft')||0)*12+(v('bin')||0))*0.0254;kg=v('bw')*0.45359237}else{m=v('bcm')/100;kg=v('bw')}
  const b=kg/(m*m);const cat=b<18.5?'Underweight':b<25?'Healthy weight':b<30?'Overweight':'Obesity';
  const lo=18.5*m*m,hi=24.9*m*m;const w=x=>this.state.sys==='imp'?num(x/0.45359237,0)+' lb':num(x,1)+' kg';
  $('#out').innerHTML=`<span class="label">Your BMI</span><div class="big"><em>${num(b,1)}</em></div>${kv([['Category',cat],['Healthy weight for your height',w(lo)+' – '+w(hi)]])}${copyBtn}`;return `BMI ${num(b,1)} (${cat})`},
 after(){bindSeg('bsys',s=>{this.state.sys=s;open('bmi')})}},

{id:'sleep',cat:'Health',name:'Sleep time',kw:'sleep calculator bedtime wake up cycles rem',desc:'Bedtimes that line up with 90-minute sleep cycles.',
 state:{mode:'wake'},
 render(){return `<div class="inputs">${seg('slm',[['wake','I need to wake up at'],['now','I’m going to bed at']],this.state.mode)}<div class="row">${field('slt',this.state.mode==='wake'?'Wake-up time':'Bedtime',this.state.mode==='wake'?'06:30':'23:00',{type:'time'})}${field('slf','Time to fall asleep',15,{unit:'min'})}</div>
  <div id="sltimes"></div><p class="hint">Each cycle is about 90 minutes. Five or six cycles suit most adults. Waking at the end of a cycle usually feels easier.</p></div><div class="result" id="out"></div>`},
 calc(){const t=toMin($('#slt').value),f=v('slf')||0,wake=this.state.mode==='wake';const list=[6,5,4,3].map(c=>({c,t:wake?t-c*90-f:t+f+c*90}));
  $('#sltimes').innerHTML=`<div class="times">${list.map(x=>`<div class="time-chip ${x.c>=5?'best':''}"><b>${fmtClock(x.t)}</b><small>${x.c} cycles · ${hm(x.c*1.5)}</small></div>`).join('')}</div>`;
  $('#out').innerHTML=`<span class="label">${wake?'Best time to go to bed':'Best time to wake up'}</span><div class="big"><em>${fmtClock(list[1].t)}</em></div>${kv([['For 6 cycles (9h)',fmtClock(list[0].t)],['For 5 cycles (7.5h)',fmtClock(list[1].t)]])}${copyBtn}`;return `${wake?'Go to bed':'Wake up'} at ${fmtClock(list[1].t)} or ${fmtClock(list[0].t)}`},
 after(){bindSeg('slm',m=>{this.state.mode=m;open('sleep')})}},

{id:'age',cat:'Dates & time',name:'Age',kw:'age birthday how old born date of birth',desc:'Exact age and days until your next birthday.',
 render(){return `<div class="inputs"><div class="row">${field('ab','Date of birth','1994-03-17',{type:'date'})}${field('ao','Age on',new Date().toISOString().slice(0,10),{type:'date'})}</div></div><div class="result" id="out"></div>`},
 calc(){const b=new Date($('#ab').value+'T00:00'),o=new Date($('#ao').value+'T00:00');if(isNaN(b)||isNaN(o)||o<b){$('#out').innerHTML='<span class="label">Result</span><p class="hint">Pick a birth date before the second date.</p>';return''}
  let tm=(o.getFullYear()-b.getFullYear())*12+o.getMonth()-b.getMonth();if(o.getDate()<b.getDate())tm--;const an=new Date(b.getFullYear(),b.getMonth()+tm,1);an.setDate(Math.min(b.getDate(),new Date(an.getFullYear(),an.getMonth()+1,0).getDate()));const y=Math.floor(tm/12),m=tm%12,d=Math.round((o-an)/864e5);
  const days=Math.round((o-b)/864e5);let nb=new Date(o.getFullYear(),b.getMonth(),b.getDate());if(nb<o)nb.setFullYear(nb.getFullYear()+1);const till=Math.round((nb-o)/864e5);
  $('#out').innerHTML=`<span class="label">Age</span><div class="big"><em>${y}</em> yrs</div>${kv([['Exactly',`${y}y ${m}m ${d}d`],['In days',num(days,0)],['In weeks',num(days/7,0)],['Next birthday in',till===0?'Today 🎉':num(till,0)+' days']])}${copyBtn}`;return `${y} years, ${m} months, ${d} days`}},

{id:'days',cat:'Dates & time',name:'Days between dates',kw:'days between dates countdown date difference business working days add days',desc:'Calendar days and weekdays between two dates.',
 render(){const t=new Date();const x=new Date(t.getFullYear(),11,25);if(x<t)x.setFullYear(x.getFullYear()+1);const iso=d=>new Date(d-d.getTimezoneOffset()*6e4).toISOString().slice(0,10);
  return `<div class="inputs"><div class="row">${field('d1','From',iso(t),{type:'date'})}${field('d2','To',iso(x),{type:'date'})}</div><p class="hint">Example: days until Christmas. Weekdays count Monday to Friday and skip public holidays only if you remove them yourself.</p></div><div class="result" id="out"></div>`},
 calc(){const a=new Date($('#d1').value+'T00:00'),b=new Date($('#d2').value+'T00:00');const n=Math.round((b-a)/864e5);let wd=0;const s=n<0?-1:1;for(let i=0;i<Math.abs(n);i++){const d=new Date(a);d.setDate(a.getDate()+s*(i+1));const g=d.getDay();if(g&&g<6)wd++}
  $('#out').innerHTML=`<span class="label">Days</span><div class="big"><em>${num(Math.abs(n),0)}</em></div>${kv([['Weekdays',num(wd,0)],['Weeks',num(Math.abs(n)/7,1)],['Months (approx.)',num(Math.abs(n)/30.437,1)]])}${copyBtn}`;return `${Math.abs(n)} days`}},

{id:'convert',cat:'Converters',name:'Unit converter',kw:'convert cups grams ml oz fahrenheit celsius inches cm feet meters pounds kg miles km',desc:'Kitchen, length, weight and temperature.',
 state:{kind:'cook'},
 U:{cook:{cup:236.588,'metric cup':250,tbsp:14.7868,tsp:4.92892,'fl oz':29.5735,ml:1,l:1000,'pint':473.176},len:{in:2.54,ft:30.48,yd:91.44,mi:160934.4,mm:.1,cm:1,m:100,km:100000},wt:{oz:28.3495,lb:453.592,g:1,kg:1000,st:6350.29},temp:{'°F':0,'°C':0,'K':0}},
 D:{cook:['cup','ml',1.5],len:['in','cm',12],wt:['lb','kg',10],temp:['°F','°C',350]},
 render(){const k=this.state.kind,u=Object.keys(this.U[k]),d=this.D[k];const sel=(id,cur)=>`<select id="${id}">${u.map(x=>`<option ${x===cur?'selected':''}>${x}</option>`).join('')}</select>`;
  return `<div class="inputs">${seg('ck',[['cook','Kitchen'],['len','Length'],['wt','Weight'],['temp','Temperature']],k)}<div class="row">${field('cv','Value',d[2])}<div class="field"><label for="cf">From</label>${sel('cf',d[0])}</div><div class="field"><label for="ct">To</label>${sel('ct',d[1])}</div></div>
  <div class="actions"><button class="btn" type="button" id="cswap">Swap units</button></div>${k==='temp'?'<p class="hint">Oven tip: 350 °F is about 175 °C, gas mark 4. For an air fryer, lower the oven temperature by about 25 °F / 15 °C.</p>':''}</div><div class="result" id="out"></div>`},
 calc(){const k=this.state.kind,x=v('cv'),f=$('#cf').value,t=$('#ct').value;let r;
  if(k==='temp'){const c=f==='°C'?x:f==='°F'?(x-32)*5/9:x-273.15;r=t==='°C'?c:t==='°F'?c*9/5+32:c+273.15}else r=x*this.U[k][f]/this.U[k][t];
  const others=Object.keys(this.U[k]).filter(u=>u!==f&&u!==t).slice(0,4).map(u=>{let o;if(k==='temp'){const c=f==='°C'?x:f==='°F'?(x-32)*5/9:x-273.15;o=u==='°C'?c:u==='°F'?c*9/5+32:c+273.15}else o=x*this.U[k][f]/this.U[k][u];return[u,num(o,4)]});
  $('#out').innerHTML=`<span class="label">${num(x,4)} ${f} =</span><div class="big"><em>${num(r,4)}</em> ${t}</div>${kv(others)}${copyBtn}`;return `${num(x,4)} ${f} = ${num(r,4)} ${t}`},
 after(){bindSeg('ck',k=>{this.state.kind=k;open('convert')});$('#cswap').onclick=()=>{const a=$('#cf').value;$('#cf').value=$('#ct').value;$('#ct').value=a;update()}}},

{id:'calorie',cat:'Health',name:'Calorie needs',kw:'calorie calculator tdee bmr maintenance daily calories diet energy',desc:'Daily calories to maintain, lose or gain weight.',
 state:{sys:null,sex:'f'},
 render(){const s=this.state.sys||(R().imperial?'imp':'met');this.state.sys=s;
  return `<div class="inputs"><div class="actions">${seg('csys',[['imp','ft / lb'],['met','cm / kg']],s)}${seg('csex',[['f','Female'],['m','Male']],this.state.sex)}</div>
  <div class="row">${field('cage','Age',34,{unit:'yrs'})}${s==='imp'?field('cft','Height',5,{unit:'ft'})+field('cin','',6,{unit:'in'})+field('cw','Weight',150,{unit:'lb'}):field('ccm','Height',168,{unit:'cm'})+field('cw','Weight',68,{unit:'kg'})}</div>
  <div class="field"><label for="cact">Activity</label><select id="cact"><option value="1.2">Mostly sitting, little exercise</option><option value="1.375" selected>Light exercise 1–3 days a week</option><option value="1.55">Moderate exercise 3–5 days a week</option><option value="1.725">Hard exercise 6–7 days a week</option><option value="1.9">Physical job plus training</option></select></div>
  <p class="hint">Uses the Mifflin-St Jeor equation, a common estimate for adults. Needs vary; a doctor or dietitian can give personal advice.</p></div><div class="result" id="out"></div>`},
 calc(){let cm,kg;if(this.state.sys==='imp'){cm=((v('cft')||0)*12+(v('cin')||0))*2.54;kg=v('cw')*0.45359237}else{cm=v('ccm');kg=v('cw')}
  const bmr=10*kg+6.25*cm-5*v('cage')+(this.state.sex==='m'?5:-161);const t=bmr*parseFloat($('#cact').value);const floor=this.state.sex==='m'?1500:1200;const f=x=>num(Math.max(floor,Math.round(x/10)*10),0)+' kcal';
  $('#out').innerHTML=`<span class="label">To maintain weight</span><div class="big"><em>${num(Math.round(t/10)*10,0)}</em> kcal/day</div>${kv([['Gentle loss (~0.25 kg / ½ lb a week)',f(t-250)],['Loss (~0.5 kg / 1 lb a week)',f(t-500)],['Gentle gain',num(Math.round((t+250)/10)*10,0)+' kcal'],['Resting rate (BMR)',num(Math.round(bmr),0)+' kcal']])}${copyBtn}`;return `Maintenance about ${num(Math.round(t/10)*10,0)} kcal/day`},
 after(){bindSeg('csys',s=>{this.state.sys=s;open('calorie')});bindSeg('csex',s=>{this.state.sex=s;update()})}},

{id:'gpa',cat:'Students',name:'GPA',kw:'gpa grade point average college high school semester credits',desc:'Semester GPA on the US 4.0 scale, plus cumulative.',
 rows:null,
 G:{'A+':4,'A':4,'A-':3.7,'B+':3.3,'B':3,'B-':2.7,'C+':2.3,'C':2,'C-':1.7,'D+':1.3,'D':1,'F':0},
 render(){if(!this.rows)this.rows=store.get('gpa',[['English Composition','A-',3],['Calculus I','B+',4],['Intro to Psychology','A',3],['Biology Lab','B',1],['World History','A-',3]]);
  const g=Object.keys(this.G);
  return `<div class="inputs"><div class="tc-wrap"><table><thead><tr><th>Course</th><th>Grade</th><th>Credits</th><th></th></tr></thead><tbody id="gbody">
  ${this.rows.map((r,i)=>`<tr><td><input id="gn${i}" value="${String(r[0]).replace(/"/g,'&quot;')}" aria-label="Course name"></td><td><select id="gg${i}" aria-label="Grade" style="width:100%;background:transparent;border:1px solid var(--line);border-radius:6px;padding:5px">${g.map(x=>`<option ${x===r[1]?'selected':''}>${x}</option>`).join('')}</select></td><td><input id="gc${i}" type="number" min="0" step="0.5" value="${r[2]}" aria-label="Credits"></td><td><button class="btn" type="button" data-del="${i}" aria-label="Remove course">✕</button></td></tr>`).join('')}
  </tbody></table></div>
  <div class="actions"><button class="btn primary" type="button" id="gadd">Add course</button></div>
  <div class="row">${field('gprev','Current cumulative GPA (optional)','')}${field('gprevc','Credits already earned','',{unit:'cr'})}</div>
  <p class="hint">Unweighted 4.0 scale. Your courses are saved in this browser.</p></div><div class="result" id="out"></div>`},
 calc(){let pts=0,cr=0;this.rows=this.rows.map((r,i)=>{const n=$('#gn'+i).value,gr=$('#gg'+i).value,c=parseFloat($('#gc'+i).value)||0;pts+=this.G[gr]*c;cr+=c;return[n,gr,c]});store.set('gpa',this.rows);
  const sem=cr?pts/cr:NaN,pg=v('gprev'),pc=v('gprevc');const cum=pg>=0&&pc>0?(pts+pg*pc)/(cr+pc):NaN;
  $('#out').innerHTML=`<span class="label">Semester GPA</span><div class="big"><em>${isFinite(sem)?sem.toFixed(2):'—'}</em></div>${kv([['Credits this term',num(cr,1)],['Grade points',num(pts,2)],['Cumulative GPA',isFinite(cum)?cum.toFixed(2):'Add past GPA']])}${copyBtn}`;return `GPA ${isFinite(sem)?sem.toFixed(2):'—'}`},
 after(){$('#gadd').onclick=()=>{this.calc();this.rows.push(['New course','A',3]);open('gpa')};document.querySelectorAll('[data-del]').forEach(b=>b.onclick=()=>{this.calc();this.rows.splice(+b.dataset.del,1);open('gpa')})}},

{id:'autoloan',cat:'Money',name:'Auto loan',kw:'auto loan car payment vehicle finance down payment trade in sales tax',desc:'Monthly car payment with down payment, trade-in and tax.',
 render(){return `<div class="inputs"><div class="row">${field('ap','Vehicle price',34000,{unit:R().cur})}${field('ad','Down payment',4000,{unit:R().cur})}${field('at','Trade-in value',3000,{unit:R().cur})}</div>
  <div class="row">${field('ax','Sales tax',region==='US'?7:0,{unit:'%'})}${field('ar','Interest rate',6.9,{unit:'%'})}<div class="field"><label for="am">Term</label><select id="am">${[36,48,60,72,84].map(m=>`<option value="${m}" ${m===60?'selected':''}>${m} months</option>`).join('')}</select></div></div>
  <p class="hint">Tax is applied to the price after trade-in, which is how most US states count it. Leave tax at 0 if it is already in the price.</p></div><div class="result" id="out"></div>`},
 calc(){const price=v('ap'),dn=v('ad')||0,tr=v('at')||0,tax=Math.max(0,price-tr)*(v('ax')||0)/100;const P=Math.max(0,price-dn-tr+tax),r=v('ar')/1200,n=+$('#am').value;const pm=r?P*r/(1-Math.pow(1+r,-n)):P/n;
  $('#out').innerHTML=`<span class="label">Monthly payment</span><div class="big"><em>${money(pm)}</em></div>${kv([['Amount financed',money(P,0)],['Sales tax',money(tax,0)],['Total interest',money(pm*n-P,0)],['Total cost of car',money(pm*n+dn+tr,0)]])}${copyBtn}`;return `${money(pm)}/month for ${n} months`}},

{id:'dice',cat:'Fun',name:'Dice roller',kw:'dice roller roll d6 d20 random number dnd board game',desc:'Roll any number of dice, from d4 to d100.',
 state:{sides:6,last:null},
 render(){return `<div class="inputs">${seg('dsides',[4,6,8,10,12,20,100].map(x=>[String(x),'d'+x]),String(this.state.sides))}
  <div class="row">${field('dn','Number of dice',2,{step:'1'})}${field('dm','Add modifier',0,{step:'1'})}</div>
  <div class="actions"><button class="btn primary" type="button" id="droll">Roll dice</button></div><div id="dfaces" class="times"></div></div><div class="result" id="out"></div>`},
 roll(){const n=Math.min(50,Math.max(1,Math.round(v('dn')||1)));const a=new Uint32Array(n);crypto.getRandomValues(a);this.state.last=[...a].map(x=>x%this.state.sides+1)},
 calc(){if(!this.state.last||this.state.last.length!==Math.min(50,Math.max(1,Math.round(v('dn')||1))))this.roll();const l=this.state.last,m=Math.round(v('dm')||0),s=l.reduce((a,b)=>a+b,0)+m;
  $('#dfaces').innerHTML=l.map(x=>`<div class="time-chip ${x===this.state.sides?'best':''}"><b>${x}</b><small>d${this.state.sides}</small></div>`).join('');
  $('#out').innerHTML=`<span class="label">Total</span><div class="big"><em>${s}</em></div>${kv([['Dice',l.length+'d'+this.state.sides+(m?(m>0?' + ':' − ')+Math.abs(m):'')],['Highest roll',Math.max(...l)],['Lowest roll',Math.min(...l)]])}${copyBtn}`;return `Rolled ${l.join(', ')} = ${s}`},
 after(){bindSeg('dsides',s=>{this.state.sides=+s;this.roll();update()});$('#droll').onclick=()=>{this.roll();update()}}},

{id:'lcm',cat:'Students',name:'LCM',kw:'lcm least common multiple lowest common denominator math',desc:'Least common multiple of two or more whole numbers.',
 render(){return `<div class="inputs">${field('ln','Numbers (separate with commas or spaces)','12, 18, 30',{type:'text'})}<p class="hint">Works with up to 20 whole numbers. Useful for finding a common denominator when adding fractions.</p><div id="lsteps"></div></div><div class="result" id="out"></div>`},
 calc(){return mathTool('lcm')}},

{id:'gcf',cat:'Students',name:'GCF',kw:'gcf gcd greatest common factor divisor highest common factor hcf simplify fraction',desc:'Greatest common factor of two or more whole numbers.',
 render(){return `<div class="inputs">${field('ln','Numbers (separate with commas or spaces)','48, 180, 72',{type:'text'})}<p class="hint">Also called GCD or HCF. Divide both parts of a fraction by the GCF to simplify it.</p><div id="lsteps"></div></div><div class="result" id="out"></div>`},
 calc(){return mathTool('gcf')}},

{id:'sqft',cat:'Home',name:'Square footage',kw:'square footage area sq ft square meters room floor flooring carpet paint tile',desc:'Area of rooms and shapes, with material cost.',
 state:{shape:'rect',unit:null},
 render(){const u=this.state.unit||(R().imperial?'ft':'m');this.state.unit=u;const s=this.state.shape;const L=u==='ft'?'ft':'m';
  const f={rect:field('sa','Length',u==='ft'?14:4.2,{unit:L})+field('sb','Width',u==='ft'?12:3.6,{unit:L}),circle:field('sa','Diameter',u==='ft'?10:3,{unit:L}),tri:field('sa','Base',u==='ft'?12:3.5,{unit:L})+field('sb','Height',u==='ft'?8:2.5,{unit:L})}[s];
  return `<div class="inputs"><div class="actions">${seg('sshape',[['rect','Rectangle'],['circle','Circle'],['tri','Triangle']],s)}${seg('sunit',[['ft','Feet'],['m','Metres']],u)}</div>
  <div class="row">${f}${field('sq','Rooms or areas',1,{step:'1'})}</div>
  <div class="row">${field('sp',u==='ft'?'Material price per sq ft':'Material price per m²',u==='ft'?4.5:45,{unit:R().cur})}${field('sw','Extra for waste',10,{unit:'%'})}</div>
  <p class="hint">Add 10% waste for straight tile or flooring layouts, 15% for diagonal or patterned layouts.</p></div><div class="result" id="out"></div>`},
 calc(){const a=v('sa'),b=v('sb'),s=this.state.shape,q=Math.max(1,v('sq')||1);let area=s==='rect'?a*b:s==='circle'?Math.PI*(a/2)**2:a*b/2;area*=q;
  const ft=this.state.unit==='ft';const sqft=ft?area:area*10.7639,sqm=ft?area/10.7639:area;const buy=area*(1+(v('sw')||0)/100);
  $('#out').innerHTML=`<span class="label">Total area</span><div class="big"><em>${num(ft?sqft:sqm,2)}</em> ${ft?'sq ft':'m²'}</div>${kv([[ft?'In square metres':'In square feet',ft?num(sqm,2)+' m²':num(sqft,2)+' sq ft'],['To buy (with waste)',num(buy,2)+(ft?' sq ft':' m²')],['Material cost',money(buy*(v('sp')||0))],['Square yards',num(sqft/9,2)]])}${copyBtn}`;return `${num(ft?sqft:sqm,2)} ${ft?'sq ft':'m²'}`},
 after(){bindSeg('sshape',x=>{this.state.shape=x;open('sqft')});bindSeg('sunit',x=>{this.state.unit=x;open('sqft')})}},

{id:'paycheck',cat:'Work & pay',name:'Take-home pay (US)',kw:'paycheck take home pay net pay salary after tax federal income tax fica social security medicare withholding',desc:'2026 US paycheck after federal tax, FICA and state tax.',
 state:{fs:'single',freq:'26'},
 B:{single:[[12400,.10],[50400,.12],[105700,.22],[201775,.24],[256225,.32],[640600,.35],[Infinity,.37]],mfj:[[24800,.10],[100800,.12],[211400,.22],[403550,.24],[512450,.32],[768700,.35],[Infinity,.37]]},
 SD:{single:16100,mfj:32200},
 render(){return `<div class="inputs"><div class="actions">${seg('pfs',[['single','Single'],['mfj','Married filing jointly']],this.state.fs)}</div>
  <div class="row">${field('pg','Annual salary',65000,{unit:'USD'})}<div class="field"><label for="pf">Paid</label><select id="pf">${[['52','Weekly'],['26','Every 2 weeks'],['24','Twice a month'],['12','Monthly']].map(([x,l])=>`<option value="${x}" ${x===this.state.freq?'selected':''}>${l}</option>`).join('')}</select></div></div>
  <div class="row">${field('pp','Pre-tax 401(k) and benefits per year',0,{unit:'USD'})}${field('ps','State income tax (estimate)',0,{unit:'%'})}</div>
  <p class="hint">Uses 2026 federal brackets and standard deduction. Alaska, Florida, Nevada, New Hampshire, South Dakota, Tennessee, Texas, Washington and Wyoming have no state income tax on wages.${region!=='US'?' This calculator uses US tax rules.':''}</p></div><div class="result" id="out"></div>`},
 calc(){const usd=n=>isFinite(n)?n.toLocaleString('en-US',{style:'currency',currency:'USD'}):'—';
  const g=Math.max(0,v('pg')||0),pre=Math.min(g,Math.max(0,v('pp')||0)),fs=this.state.fs;this.state.freq=$('#pf').value;const per=+this.state.freq;
  const ti=Math.max(0,g-pre-this.SD[fs]);let fed=0,lo=0,top=0;for(const[hi,r]of this.B[fs]){if(ti>lo){fed+=(Math.min(ti,hi)-lo)*r;top=r}lo=hi}
  const ss=Math.min(g,184500)*0.062,med=g*0.0145+Math.max(0,g-(fs==='mfj'?250000:200000))*0.009,st=(g-pre)*Math.max(0,v('ps')||0)/100;
  const net=g-pre-fed-ss-med-st;
  $('#out').innerHTML=`<span class="label">Take-home pay per paycheck</span><div class="big"><em>${usd(net/per)}</em></div>${kv([['Take-home per year',usd(net)],['Gross per paycheck',usd(g/per)],['Federal income tax',usd(fed/per)],['Social Security (6.2%)',usd(ss/per)],['Medicare',usd(med/per)],['State tax',usd(st/per)],['Pre-tax deductions',usd(pre/per)],['Effective federal rate',g?(fed/g*100).toFixed(1)+'%':'—'],['Top federal bracket',(top*100).toFixed(0)+'%']])}${copyBtn}`;
  return `Take-home ${usd(net/per)} per paycheck (${usd(net)} a year)`},
 after(){bindSeg('pfs',x=>{this.state.fs=x;update()})}},

{id:'concrete',cat:'Home',name:'Concrete',kw:'concrete calculator cubic yards slab footing bags 80 lb 60 lb cement post hole patio driveway premix',desc:'Cubic yards or m³ and bags for slabs and post holes.',
 state:{shape:'slab',unit:null},
 render(){const u=this.state.unit||(R().imperial?'ft':'m');this.state.unit=u;const s=this.state.shape,ft=u==='ft';
  const dims=s==='slab'?field('ca','Length',ft?10:3,{unit:ft?'ft':'m'})+field('cb','Width',ft?10:3,{unit:ft?'ft':'m'})+field('cc','Thickness',ft?4:10,{unit:ft?'in':'cm'}):field('ca','Hole diameter',ft?10:25,{unit:ft?'in':'cm'})+field('cc','Hole depth',ft?36:90,{unit:ft?'in':'cm'});
  return `<div class="inputs"><div class="actions">${seg('cshape',[['slab','Slab or patio'],['hole','Post hole']],s)}${seg('cunit',[['ft','Feet / inches'],['m','Metres / cm']],u)}</div>
  <div class="row">${dims}${field('cq',s==='slab'?'Number of slabs':'Number of holes',s==='slab'?1:8,{step:'1'})}</div><div class="row">${field('cw','Extra for waste',10,{unit:'%'})}</div>
  <p class="hint">${ft?'Bag yields: 80 lb ≈ 0.60 cu ft, 60 lb ≈ 0.45 cu ft, 40 lb ≈ 0.30 cu ft of concrete.':'A 20 kg bag of premix makes about 0.01 m³ of concrete.'}</p></div><div class="result" id="out"></div>`},
 calc(){const ft=this.state.unit==='ft',q=Math.max(1,Math.round(v('cq')||1)),w=1+(v('cw')||0)/100;let vol;
  if(this.state.shape==='slab')vol=ft?v('ca')*v('cb')*v('cc')/12:v('ca')*v('cb')*v('cc')/100;
  else{const r=v('ca')/2;vol=ft?Math.PI*(r/12)**2*(v('cc')/12):Math.PI*(r/100)**2*(v('cc')/100)}
  vol*=q*w;
  if(ft){const yd=vol/27;$('#out').innerHTML=`<span class="label">Concrete needed</span><div class="big"><em>${num(yd,2)}</em> cu yd</div>${kv([['Cubic feet',num(vol,2)],['80 lb bags',num(Math.ceil(vol/0.6),0)],['60 lb bags',num(Math.ceil(vol/0.45),0)],['40 lb bags',num(Math.ceil(vol/0.3),0)],['In cubic metres',num(vol*0.0283168,2)+' m³']])}${copyBtn}`;return `${num(yd,2)} cu yd of concrete`}
  $('#out').innerHTML=`<span class="label">Concrete needed</span><div class="big"><em>${num(vol,3)}</em> m³</div>${kv([['Litres',num(vol*1000,0)],['20 kg bags',num(Math.ceil(vol/0.01),0)],['In cubic yards',num(vol*1.30795,2)+' cu yd']])}${copyBtn}`;return `${num(vol,3)} m³ of concrete`},
 after(){bindSeg('cshape',x=>{this.state.shape=x;open('concrete')});bindSeg('cunit',x=>{this.state.unit=x;open('concrete')})}},

{id:'paint',cat:'Home',name:'Paint',kw:'paint calculator gallons litres wall room ceiling coats how much paint',desc:'How much paint a room needs, in gallons or litres.',
 state:{unit:null},
 render(){const u=this.state.unit||(R().imperial?'ft':'m');this.state.unit=u;const ft=u==='ft',L=ft?'ft':'m';
  return `<div class="inputs">${seg('punit',[['ft','Feet / gallons'],['m','Metres / litres']],u)}
  <div class="row">${field('pl','Room length',ft?14:4.2,{unit:L})}${field('pw','Room width',ft?12:3.6,{unit:L})}${field('ph','Wall height',ft?8:2.4,{unit:L})}</div>
  <div class="row">${field('pd','Doors',1,{step:'1'})}${field('pwn','Windows',2,{step:'1'})}${field('pc','Coats',2,{step:'1'})}</div>
  <div class="row"><div class="field"><label for="pceil">Surfaces</label><select id="pceil"><option value="0">Walls only</option><option value="1">Walls and ceiling</option></select></div>${field('pcov',ft?'Coverage per gallon':'Coverage per litre',ft?350:10,{unit:ft?'sq ft':'m²'})}</div>
  <p class="hint">Each door counts as ${ft?'20 sq ft':'1.9 m²'} and each window as ${ft?'15 sq ft':'1.4 m²'}. Check the coverage printed on your paint can.</p></div><div class="result" id="out"></div>`},
 calc(){const ft=this.state.unit==='ft',l=v('pl'),w=v('pw'),h=v('ph');
  const walls=Math.max(0,2*(l+w)*h-(v('pd')||0)*(ft?20:1.9)-(v('pwn')||0)*(ft?15:1.4)),ceil=$('#pceil').value==='1'?l*w:0,coats=Math.max(1,Math.round(v('pc')||1));
  const area=(walls+ceil)*coats,amt=area/(v('pcov')||1),u=ft?' gal':' L',a=ft?' sq ft':' m²';
  $('#out').innerHTML=`<span class="label">Paint needed</span><div class="big"><em>${num(amt,2)}</em>${u}</div>${kv([[ft?'Buy (whole gallons)':'Buy (whole litres)',num(Math.ceil(amt),0)+u],['Wall area',num(walls,1)+a],['Ceiling area',num(ceil,1)+a],['Total with '+coats+(coats>1?' coats':' coat'),num(area,1)+a]])}${copyBtn}`;return `${num(amt,2)}${u} of paint`},
 after(){bindSeg('punit',x=>{this.state.unit=x;open('paint')})}},

{id:'random',cat:'Fun',name:'Random number',kw:'random number generator picker rng raffle pick a number between winner',desc:'Random whole numbers in any range, with or without repeats.',
 state:{last:null,key:''},
 render(){return `<div class="inputs"><div class="row">${field('rmin','From',1,{step:'1'})}${field('rmax','To',100,{step:'1'})}${field('rn','How many',1,{step:'1'})}</div>
  <div class="row"><div class="field"><label for="ru">Repeats</label><select id="ru"><option value="1">No repeats</option><option value="0">Allow repeats</option></select></div><div class="field"><label for="rs">Order</label><select id="rs"><option value="0">As drawn</option><option value="1">Sorted low to high</option></select></div></div>
  <div class="actions"><button class="btn primary" type="button" id="rgo">Generate</button></div><div id="rlist" class="times mini"></div></div><div class="result" id="out"></div>`},
 rint(lo,hi){const span=hi-lo+1,lim=Math.floor(4294967296/span)*span,a=new Uint32Array(1);do{crypto.getRandomValues(a)}while(a[0]>=lim);return lo+a[0]%span},
 draw(){let lo=Math.ceil(v('rmin')),hi=Math.floor(v('rmax'));if(lo>hi)[lo,hi]=[hi,lo];
  const n=Math.min(1000,Math.max(1,Math.round(v('rn')||1))),uniq=$('#ru').value==='1',span=hi-lo+1;
  if(!isFinite(lo)||!isFinite(hi)||span>4294967296){this.state.last={err:'Enter whole numbers for From and To, no more than about 4 billion apart.'};return}
  if(uniq&&n>span){this.state.last={err:`There are only ${span} whole numbers from ${lo} to ${hi}. Lower “How many” or allow repeats.`};return}
  const out=[],seen=new Set();while(out.length<n){const x=this.rint(lo,hi);if(uniq){if(seen.has(x))continue;seen.add(x)}out.push(x)}this.state.last={out,lo,hi}},
 calc(){const k=['rmin','rmax','rn','ru'].map(i=>$('#'+i).value).join('|');if(!this.state.last||this.state.key!==k){this.state.key=k;this.draw()}const L=this.state.last;
  if(L.err){$('#rlist').innerHTML='';$('#out').innerHTML=`<span class="label">Result</span><p class="hint">${L.err}</p>`;return''}
  const list=$('#rs').value==='1'?[...L.out].sort((a,b)=>a-b):L.out,many=list.length>1;
  $('#rlist').innerHTML=!many?'':list.length<=200?list.map(x=>`<div class="time-chip"><b>${x}</b></div>`).join(''):`<p class="hint" style="grid-column:1/-1;word-break:break-word">${list.join(', ')}</p>`;
  $('#out').innerHTML=`<span class="label">${many?list.length+' numbers':'Your number'}</span><div class="big"><em>${many?list.slice(0,4).join(', ')+(list.length>4?' …':''):list[0]}</em></div>${kv([['Range',`${L.lo} to ${L.hi}`],['Repeats',$('#ru').value==='1'?'None':'Allowed'],['Chance of any one number',`1 in ${num(L.hi-L.lo+1,0)}`]])}${copyBtn}`;
  return list.join(', ')},
 after(){$('#rgo').onclick=()=>{this.draw();update()}}},

{id:'coin',cat:'Fun',name:'Coin flip',kw:'coin flip toss heads or tails flip a coin random decision',desc:'Flip a coin once or up to 1,000 times.',
 state:{res:null},
 render(){return `<div class="inputs"><div class="row">${field('cfn','Number of flips',1,{step:'1'})}</div><div class="actions"><button class="btn primary" type="button" id="cfgo">Flip coin</button></div><div id="cfs" class="times mini"></div><p class="hint">Each flip uses your browser's cryptographic random number generator, so heads and tails are exactly 50/50.</p></div><div class="result" id="out"></div>`},
 flip(){const n=Math.min(1000,Math.max(1,Math.round(v('cfn')||1))),a=new Uint8Array(n);crypto.getRandomValues(a);this.state.res=[...a].map(x=>x&1?'H':'T')},
 calc(){const n=Math.min(1000,Math.max(1,Math.round(v('cfn')||1)));if(!this.state.res||this.state.res.length!==n)this.flip();
  const r=this.state.res,h=r.filter(x=>x==='H').length;let best=0,c=0,p='';for(const x of r){c=x===p?c+1:1;p=x;if(c>best)best=c}
  $('#cfs').innerHTML=n>1&&n<=200?r.map(x=>`<div class="time-chip ${x==='H'?'best':''}"><b>${x}</b></div>`).join(''):'';
  $('#out').innerHTML=`<span class="label">${n===1?'Result':n+' flips'}</span><div class="big"><em>${n===1?(r[0]==='H'?'Heads':'Tails'):h+' H · '+(n-h)+' T'}</em></div>${kv([['Heads',`${h} (${num(h/n*100,1)}%)`],['Tails',`${n-h} (${num((n-h)/n*100,1)}%)`],['Longest streak',String(best)]])}${copyBtn}`;
  return n===1?(r[0]==='H'?'Heads':'Tails'):`${h} heads, ${n-h} tails`},
 after(){$('#cfgo').onclick=()=>{this.flip();update()}}},
{id:'grade',cat:'Students',name:'Grade',kw:'grade calculator weighted grade class grade average assignments categories percentage letter grade',desc:'Weighted class grade from your assignments and categories.',
 rows:null,
 render(){if(!this.rows)this.rows=store.get('grade',[['Homework',92,20],['Quizzes',85,15],['Midterm exam',78,25],['Project',88,15],['Participation',100,5]]);
  return `<div class="inputs"><div class="tc-wrap"><table><thead><tr><th>Assignment or category</th><th>Score %</th><th>Weight %</th><th></th></tr></thead><tbody id="grbody">
  ${this.rows.map((r,i)=>`<tr><td><input id="grn${i}" value="${String(r[0]).replace(/"/g,'&quot;')}" aria-label="Name"></td><td><input id="grs${i}" type="number" min="0" step="any" value="${r[1]}" aria-label="Score percent" inputmode="decimal"></td><td><input id="grw${i}" type="number" min="0" step="any" value="${r[2]}" aria-label="Weight percent" inputmode="decimal"></td><td><button class="btn" type="button" data-gdel="${i}" aria-label="Remove row">✕</button></td></tr>`).join('')}
  </tbody></table></div>
  <div class="actions"><button class="btn primary" type="button" id="gradd">Add row</button></div>
  <p class="hint">Enter scores as percentages (for 45 out of 50, enter 90). Weights don't have to add up to 100: if they add up to less, the result is your grade on the work marked so far. Rows are saved in this browser.</p></div><div class="result" id="out"></div>`},
 calc(){let sw=0,ws=0;this.rows=this.rows.map((r,i)=>{const n=$('#grn'+i).value,s=parseFloat($('#grs'+i).value),w=parseFloat($('#grw'+i).value);if(isFinite(s)&&isFinite(w)&&w>0){sw+=s*w;ws+=w}return[n,isFinite(s)?s:'',isFinite(w)?w:'']});store.set('grade',this.rows);
  const g=ws?sw/ws:NaN;
  $('#out').innerHTML=`<span class="label">Current grade</span><div class="big"><em>${isFinite(g)?num(g,2)+'%':'—'}</em></div>${kv([['Letter grade',isFinite(g)?letter(g):'—'],['Weight entered',num(ws,1)+'%'],['Weight still to come',ws<100?num(100-ws,1)+'%':'None']])}${ws>0&&ws<100?`<a class="copy" href="/final-grade-calculator/">What do I need on the final?</a>`:''}${copyBtn}`;
  return isFinite(g)?`Grade ${num(g,2)}% (${letter(g)})`:''},
 after(){$('#gradd').onclick=()=>{this.calc();this.rows.push(['New assignment','',10]);open('grade')};document.querySelectorAll('[data-gdel]').forEach(b=>b.onclick=()=>{this.calc();this.rows.splice(+b.dataset.gdel,1);open('grade')})}},

{id:'finalgrade',cat:'Students',name:'Final grade',kw:'final grade calculator final exam what do i need on my final to pass get an a b grade needed',desc:'The score you need on the final exam to reach your target grade.',
 render(){return `<div class="inputs"><div class="row">${field('fgc','Current grade',84,{unit:'%'})}${field('fgw','Final exam weight',25,{unit:'%'})}${field('fgt','Grade you want',85,{unit:'%'})}</div>
  <div class="actions">${[['A',90],['B',80],['C',70],['D',60]].map(([l,x])=>`<button class="btn" type="button" data-fgt="${x}">${l} (${x}%)</button>`).join('')}</div>
  <p class="hint">Find your current grade with the <a href="/grade-calculator/">grade calculator</a>. The final exam weight is in your course syllabus.</p><div id="fgtable"></div></div><div class="result" id="out"></div>`},
 calc(){const c=v('fgc'),w=v('fgw')/100,t=v('fgt');if(!(w>0&&w<=1)||!isFinite(c)||!isFinite(t)){$('#out').innerHTML='<span class="label">Result</span><p class="hint">Enter a final exam weight between 1 and 100%.</p>';$('#fgtable').innerHTML='';return''}
  const need=x=>(x-c*(1-w))/w,n=need(t);
  const msg=n>100?`Even 100% on the final gives ${num(c*(1-w)+100*w,1)}%.`:n<=0?`You already have it, even with 0% on the final.`:`Score at least ${num(n,1)}% on the final.`;
  $('#fgtable').innerHTML=`<div class="tbl"><table><thead><tr><th>Target</th><th>You need on the final</th></tr></thead><tbody>${[['A',90],['B',80],['C',70],['D',60]].map(([l,x])=>{const r=need(x);return`<tr><td>${l} (${x}%)</td><td>${r>100?'Not reachable':r<=0?'Already secured':num(r,1)+'%'}</td></tr>`}).join('')}</tbody></table></div>`;
  $('#out').innerHTML=`<span class="label">You need on the final</span><div class="big"><em>${n>100?'Not reachable':n<=0?'0%':num(n,1)+'%'}</em></div><p class="hint" style="color:var(--ink)">${msg}</p>${kv([['Grade if you score 100%',num(c*(1-w)+100*w,1)+'%'],['Grade if you score 70%',num(c*(1-w)+70*w,1)+'%'],['Grade if you score 0%',num(c*(1-w),1)+'%']])}${copyBtn}`;
  return n>100?`${t}% is not reachable`:`Need ${num(Math.max(0,n),1)}% on the final`},
 after(){document.querySelectorAll('[data-fgt]').forEach(b=>b.onclick=()=>{$('#fgt').value=b.dataset.fgt;update()})}}

];
function letter(g){const L=[[97,'A+'],[93,'A'],[90,'A−'],[87,'B+'],[83,'B'],[80,'B−'],[77,'C+'],[73,'C'],[70,'C−'],[67,'D+'],[63,'D'],[60,'D−']];for(const[x,l]of L)if(g>=x)return l;return 'F'}
function gcd2(a,b){while(b){[a,b]=[b,a%b]}return a}
function factor(n){const f={};let d=2;while(n>1&&d*d<=n){while(n%d===0){f[d]=(f[d]||0)+1;n/=d}d++}if(n>1)f[n]=(f[n]||0)+1;return f}
const fstr=f=>Object.entries(f).map(([p,e])=>e>1?`${p}<sup>${e}</sup>`:p).join(' × ')||'1';
function mathTool(kind){const raw=$('#ln').value.split(/[\s,;]+/).filter(Boolean);const ns=raw.map(Number);
  if(ns.length<2||ns.length>20||ns.some(n=>!Number.isInteger(n)||n<1||n>1e9)){$('#out').innerHTML='<span class="label">Result</span><p class="hint">Enter 2 to 20 whole numbers between 1 and 1,000,000,000.</p>';$('#lsteps').innerHTML='';return''}
  const g=ns.reduce(gcd2);let l=ns[0];for(const n of ns.slice(1))l=l/gcd2(l,n)*n;const r=kind==='lcm'?l:g;
  $('#lsteps').innerHTML=`<div class="field"><label>Prime factorization</label></div><dl class="kv">${ns.map(n=>`<div><dt>${num(n,0)}</dt><dd>${fstr(factor(n))}</dd></div>`).join('')}</dl>`;
  $('#out').innerHTML=`<span class="label">${kind==='lcm'?'Least common multiple':'Greatest common factor'}</span><div class="big"><em>${isFinite(r)&&r<=Number.MAX_SAFE_INTEGER?num(r,0):'Too large'}</em></div>${kv([[kind==='lcm'?'GCF of the same numbers':'LCM of the same numbers',kind==='lcm'?num(g,0):(l<=Number.MAX_SAFE_INTEGER?num(l,0):'Too large')],['As prime factors',r<=1e12?fstr(factor(r)):'—']])}${copyBtn}`;
  return `${kind.toUpperCase()}(${ns.join(', ')}) = ${r}`}

/* ---------- page shell ---------- */
const SLUGS={timecard:'time-card-calculator',hours:'hours-calculator',salary:'hourly-to-salary-calculator',tip:'tip-calculator',percent:'percentage-calculator',loan:'mortgage-calculator',bmi:'bmi-calculator',sleep:'sleep-calculator',age:'age-calculator',days:'days-between-dates',convert:'unit-converter',calorie:'calorie-calculator',gpa:'gpa-calculator',autoloan:'auto-loan-calculator',dice:'dice-roller',lcm:'lcm-calculator',gcf:'gcf-calculator',sqft:'square-footage-calculator',concrete:'concrete-calculator',paint:'paint-calculator',fraction:'fraction-calculator',random:'random-number-generator',coin:'coin-flip',grade:'grade-calculator',finalgrade:'final-grade-calculator'};
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
