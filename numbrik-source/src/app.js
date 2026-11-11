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

{id:'hours',cat:'Work & pay',name:'Hours between times',kw:'hours calculator time duration shift length how many hours between two times hours counter add hours to time hours between dates',desc:'How long between two clock times.',
 state:{mode:'times'},
 ft(min){const d=new Date(2000,0,1,0,0);d.setMinutes(((min%1440)+1440)%1440);return d.toLocaleTimeString(R().loc,{hour:'numeric',minute:'2-digit'})},
 hmw(m){m=Math.round(m);const h=Math.floor(m/60),r=m%60;return (h?`${h} hour${h===1?'':'s'}`:'')+(h&&r?' ':'')+(r||!h?`${r} minute${r===1?'':'s'}`:'')},
 nowT(){const d=new Date();return String(d.getHours()).padStart(2,'0')+':'+String(d.getMinutes()).padStart(2,'0')},
 nowDT(){const d=new Date(),p=x=>String(x).padStart(2,'0');return `${d.getFullYear()}-${p(d.getMonth()+1)}-${p(d.getDate())}T${p(d.getHours())}:${p(d.getMinutes())}`},
 render(){const m=this.state.mode,now='<button type="button" class="chip" data-now="%">Now</button>';
  const top=seg('hmode',[['times','Between two times'],['dates','Between two dates'],['add','Add hours to a time']],m);
  if(m==='dates')return `<div class="inputs">${top}<div class="row">${field('hd1','Start date and time','2026-11-06T22:00',{type:'datetime-local'})}${field('hd2','End date and time','2026-11-08T06:00',{type:'datetime-local'})}</div><div class="actions">${now.replace('%','hd1').replace('Now','Start = now')}${now.replace('%','hd2').replace('Now','End = now')}</div><div class="row">${field('hb','Unpaid break',0,{unit:'min'})}</div><p class="hint">For periods longer than a day, such as a multi-day shift or a trip.</p></div><div class="result" id="out"></div>`;
  if(m==='add')return `<div class="inputs">${top}<div class="row">${field('ha','Start time','08:15',{type:'time'})}${field('hh','Hours to add',8,{unit:'hrs',step:0.25})}${field('hm','Minutes to add',0,{unit:'min',step:1})}</div><div class="actions">${now.replace('%','ha')}</div><p class="hint">Use a minus sign to go back in time, e.g. −3 hours.</p></div><div class="result" id="out"></div>`;
  return `<div class="inputs">${top}<div class="row">${field('h1','Start time','08:00',{type:'time'})}${field('h2','End time','17:00',{type:'time'})}${field('hb','Unpaid break',0,{unit:'min'})}</div><div class="actions">${now.replace('%','h1').replace('Now','Start = now')}${now.replace('%','h2').replace('Now','End = now')}</div><p class="hint">End earlier than start counts as an overnight shift.</p></div><div class="result" id="out"></div>`},
 calc(){const m=this.state.mode,brk=Math.max(0,v('hb')||0);
  if(m==='add'){const s=toMin($('#ha').value),add=(v('hh')||0)*60+(v('hm')||0);if(!$('#ha').value){$('#out').innerHTML='<span class="label">End time</span><p class="hint">Enter a start time.</p>';return''}
   const e=s+add,dd=Math.floor(e/1440),when=dd===0?'same day':dd===1?'next day':dd===-1?'previous day':(dd>0?`${dd} days later`:`${-dd} days earlier`);
   const sent=`${this.hmw(Math.abs(add))} ${add<0?'before':'after'} ${this.ft(s)} is ${this.ft(e)}${dd?` (${when})`:''}.`;
   $('#out').innerHTML=`<span class="label">End time</span><div class="big"><em>${this.ft(e)}</em></div><p class="answer">${sent}</p>${kv([['Day',when],['24-hour time',String(Math.floor(((e%1440)+1440)%1440/60)).padStart(2,'0')+':'+String(((e%60)+60)%60).padStart(2,'0')]])}${copyBtn}`;return sent}
  let mins,sent;
  if(m==='dates'){const a=new Date($('#hd1').value),b=new Date($('#hd2').value);if(isNaN(a)||isNaN(b)){$('#out').innerHTML='<span class="label">Hours</span><p class="hint">Enter both dates and times.</p>';return''}
   mins=Math.round((b-a)/6e4);if(mins<0){$('#out').innerHTML='<span class="label">Hours</span><p class="hint">The end is before the start. Swap them.</p>';return''}
   const F=x=>x.toLocaleString(R().loc,{weekday:'short',month:'short',day:'numeric',hour:'numeric',minute:'2-digit'});
   sent=`${F(a)} to ${F(b)} is ${this.hmw(mins)}`}
  else{if(!$('#h1').value||!$('#h2').value){$('#out').innerHTML='<span class="label">Hours</span><p class="hint">Enter a start and end time.</p>';return''}
   const s=toMin($('#h1').value),e=toMin($('#h2').value);mins=e-s;if(mins<=0)mins+=1440;
   sent=`${this.ft(s)} to ${this.ft(e)}${e<=s?' (overnight)':''} is ${this.hmw(mins)}`}
  const net=Math.max(0,mins-brk),h=net/60;
  sent+=brk?`, or ${this.hmw(net)} after a ${brk}-minute break.`:` (${num(mins,0)} minutes, ${num(mins/60)} decimal hours).`;
  $('#out').innerHTML=`<span class="label">${brk?'Time worked':'Total time'}</span><div class="big"><em>${hm(h)}</em></div><p class="answer">${sent}</p>${kv([['Decimal hours',num(h)],['Minutes',num(net,0)]].concat(m==='dates'&&net>=1440?[['Days and hours',`${Math.floor(net/1440)} d ${hm((net%1440)/60)}`]]:[]))}${copyBtn}`;return sent},
 after(){bindSeg('hmode',x=>{this.state.mode=x;open('hours')});document.querySelectorAll('[data-now]').forEach(b=>b.addEventListener('click',()=>{const el=$('#'+b.dataset.now);el.value=el.type==='datetime-local'?this.nowDT():this.nowT();update()}))}},

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

{id:'loan',cat:'Money',name:'Loan & mortgage',kw:'mortgage loan car auto payment interest amortization emi home property tax insurance pmi hoa extra payment payoff schedule',desc:'Monthly payment with taxes, insurance and extra payments, plus a full schedule.',
 state:{sched:'year'},
 render(){const c=R().cur;return `<div class="inputs"><div class="row">${field('la','Loan amount',350000,{unit:c})}${field('lr','Interest rate',6.5,{unit:'%'})}${field('ly','Term',30,{unit:'yrs'})}</div>
  <details class="more"><summary>Taxes, insurance and extra payments</summary><div class="row">${field('ltx','Property tax per year',0,{unit:c})}${field('lin','Home insurance per year',0,{unit:c})}${field('lpmi','PMI per month',0,{unit:c})}${field('lhoa','HOA per month',0,{unit:c})}${field('lx','Extra payment per month',0,{unit:c})}</div><p class="hint">Leave these at 0 for a plain loan payment. Extra payments go straight to principal and shorten the loan.</p></details>
  <div id="amort"></div>
  <div class="actions">${seg('lsch',[['year','Yearly schedule'],['month','Monthly schedule']],this.state.sched)}</div><div id="lsched" class="tc-wrap sched"></div></div><div class="result" id="out"></div>`},
 calc(){const P=v('la'),r=v('lr')/1200,n=Math.round(v('ly')*12);const pm=r?P*r/(1-Math.pow(1+r,-n)):P/n;
  const tx=(v('ltx')||0)/12,ins=(v('lin')||0)/12,pmi=v('lpmi')||0,hoa=v('lhoa')||0,x=Math.max(0,v('lx')||0);
  const base=pm*n-P;let bal=P,m=0,tint=0;const rows=[];const now=new Date();
  while(bal>0.005&&m<n+1){const i=bal*r;let p=Math.min(pm+x-i,bal);if(p<=0){p=0;bal=Infinity;break}bal-=p;tint+=i;m++;rows.push([m,i,p,Math.max(0,bal)])}
  const ok=isFinite(bal);const pay=new Date(now.getFullYear(),now.getMonth()+m,1);const total=pm+x+tx+ins+pmi+hoa;
  const extras=[['Principal & interest',money(pm)]];if(x)extras.push(['Extra principal',money(x)]);if(tx)extras.push(['Property tax',money(tx)]);if(ins)extras.push(['Home insurance',money(ins)]);if(pmi)extras.push(['PMI',money(pmi)]);if(hoa)extras.push(['HOA',money(hoa)]);
  const more=[['Total interest',money(ok?tint:base,0)],['Total of loan payments',money(P+(ok?tint:base),0)],['Payments',num(m,0)],['Payoff date',pay.toLocaleDateString(R().loc,{month:'long',year:'numeric'})]];
  if(x&&ok){more.push(['Interest saved',money(base-tint,0)]);more.push(['Paid off early by',`${Math.floor((n-m)/12)} yrs ${(n-m)%12} mos`])}
  $('#out').innerHTML=`<span class="label">${total>pm+0.001?'Total monthly payment':'Monthly payment'}</span><div class="big"><em>${money(total)}</em></div>${kv((total>pm+0.001?extras:[]).concat(more))}${copyBtn}`;
  const yrs=[];for(let y=0;y<Math.ceil(rows.length/12);y++){const s=rows.slice(y*12,y*12+12);yrs.push([y+1,s.reduce((a,q)=>a+q[2],0),s.reduce((a,q)=>a+q[1],0),s[s.length-1][3]])}
  const step=Math.max(1,Math.ceil(yrs.length/10));const show=yrs.filter((q,i)=>i%step===0||i===yrs.length-1);
  $('#amort').innerHTML=yrs.length?`<div class="field"><label>Where each year’s payments go</label></div><div class="legend"><span><i style="background:var(--accent)"></i>Principal</span><span><i style="background:var(--mark)"></i>Interest</span></div>
   <div class="bars">${show.map(([y,p,i,b])=>`<div class="barrow"><span>Yr ${y}</span><div class="track"><div class="p" style="width:${p/(p+i)*100}%"></div><div class="i" style="width:${i/(p+i)*100}%"></div></div><span style="text-align:right">${money(b,0)} left</span></div>`).join('')}</div>`:'';
  const mon=d=>new Date(now.getFullYear(),now.getMonth()+d,1).toLocaleDateString(R().loc,{month:'short',year:'numeric'});
  $('#lsched').innerHTML=this.state.sched==='year'
   ?`<table><thead><tr><th>Year</th><th>Principal</th><th>Interest</th><th>Balance</th></tr></thead><tbody>${yrs.map(([y,p,i,b])=>`<tr><td>${y}</td><td class="num">${money(p,0)}</td><td class="num">${money(i,0)}</td><td class="num">${money(b,0)}</td></tr>`).join('')}</tbody></table>`
   :`<table><thead><tr><th>#</th><th>Month</th><th>Principal</th><th>Interest</th><th>Balance</th></tr></thead><tbody>${rows.map(([k,i,p,b])=>`<tr><td>${k}</td><td>${mon(k)}</td><td class="num">${money(p)}</td><td class="num">${money(i)}</td><td class="num">${money(b,0)}</td></tr>`).join('')}</tbody></table>`;
  return `${money(total)}/month`},
 after(){bindSeg('lsch',s=>{this.state.sched=s;update()})}},
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

{id:'sleep',cat:'Health',name:'Sleep calculator',kw:'sleep calculator bedtime wake up cycles rem',desc:'Bedtimes that line up with 90-minute sleep cycles.',
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
  const g=x=>num(Math.round(x/10)*10,0)+' kcal';$('#out').innerHTML=`<span class="label">To maintain your weight</span><div class="big"><em>${num(Math.round(t/10)*10,0)}</em> calories/day</div><p class="answer">Eat about ${g(t)} a day to stay the same weight, or about ${f(t-500)} to lose roughly 1 lb (0.5 kg) a week.</p>${kv([['Mild weight loss (½ lb / 0.25 kg a week)',f(t-250)],['Weight loss (1 lb / 0.5 kg a week)',f(t-500)],['Fast weight loss (2 lb / 1 kg a week)',f(t-1000)],['Mild weight gain (½ lb / 0.25 kg a week)',g(t+250)],['Weight gain (1 lb / 0.5 kg a week)',g(t+500)],['Resting rate (BMR)',num(Math.round(bmr),0)+' kcal']])}${t-1000<floor?`<p class="hint">Targets stop at ${floor} calories a day; going lower needs medical supervision.</p>`:''}${copyBtn}`;return `Maintenance about ${num(Math.round(t/10)*10,0)} kcal/day`},
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
  <div class="row">${field('gtarget','Target cumulative GPA (optional)','')}${field('gnext','Credits you will take next','',{unit:'cr'})}</div>
  <p class="hint">Unweighted 4.0 scale. Your courses are saved in this browser.</p></div><div class="result" id="out"></div>`},
 calc(){let pts=0,cr=0;this.rows=this.rows.map((r,i)=>{const n=$('#gn'+i).value,gr=$('#gg'+i).value,c=parseFloat($('#gc'+i).value)||0;pts+=this.G[gr]*c;cr+=c;return[n,gr,c]});store.set('gpa',this.rows);
  const sem=cr?pts/cr:NaN,pg=v('gprev'),pc=v('gprevc');const cum=pg>=0&&pc>0?(pts+pg*pc)/(cr+pc):NaN;const tg=v('gtarget'),nx=v('gnext');let plan=[];if(tg>0&&nx>0){const have=(pg>=0&&pc>0?pg*pc:0)+pts,hc=(pg>=0&&pc>0?pc:0)+cr,need=(tg*(hc+nx)-have)/nx;plan=[[`GPA needed in next ${num(nx,1)} credits`,need>4?'Not reachable on a 4.0 scale':need<=0?'Already reached':need.toFixed(2)]]}
  $('#out').innerHTML=`<span class="label">Semester GPA</span><div class="big"><em>${isFinite(sem)?sem.toFixed(2):'—'}</em></div>${kv([['Credits this term',num(cr,1)],['Grade points',num(pts,2)],['Cumulative GPA',isFinite(cum)?cum.toFixed(2):'Add past GPA']].concat(plan))}${copyBtn}`;return `GPA ${isFinite(sem)?sem.toFixed(2):'—'}`},
 after(){$('#gadd').onclick=()=>{this.calc();this.rows.push(['New course','A',3]);open('gpa')};document.querySelectorAll('[data-del]').forEach(b=>b.onclick=()=>{this.calc();this.rows.splice(+b.dataset.del,1);open('gpa')})}},

{id:'autoloan',cat:'Money',name:'Auto loan',kw:'auto loan car payment vehicle finance down payment trade in sales tax',desc:'Monthly car payment with down payment, trade-in and tax.',
 render(){return `<div class="inputs"><div class="row">${field('ap','Vehicle price',34000,{unit:R().cur})}${field('ad','Down payment',4000,{unit:R().cur})}${field('at','Trade-in value',3000,{unit:R().cur})}</div>
  <div class="row">${field('ax','Sales tax',region==='US'?7:0,{unit:'%'})}${field('af','Fees (title, registration, dealer)',0,{unit:R().cur})}${field('ar','Interest rate',6.9,{unit:'%'})}<div class="field"><label for="am">Term</label><select id="am">${[36,48,60,72,84].map(m=>`<option value="${m}" ${m===60?'selected':''}>${m} months</option>`).join('')}</select></div></div>
  <p class="hint">Tax is applied to the price after trade-in, which is how most US states count it. Leave tax at 0 if it is already in the price. Add fees to include them in the loan, or leave them at 0 if you'll pay them up front.</p></div><div class="result" id="out"></div>`},
 calc(){const price=v('ap'),dn=v('ad')||0,tr=v('at')||0,tax=Math.max(0,price-tr)*(v('ax')||0)/100;const fees=Math.max(0,v('af')||0),P=Math.max(0,price-dn-tr+tax+fees),r=v('ar')/1200,n=+$('#am').value;const pm=r?P*r/(1-Math.pow(1+r,-n)):P/n;
  $('#out').innerHTML=`<span class="label">Monthly payment</span><div class="big"><em>${money(pm)}</em></div>${kv([['Amount financed',money(P,0)],['Sales tax',money(tax,0)],['Fees added to loan',money(fees,0)],['Total interest',money(pm*n-P,0)],['Total cost of car',money(pm*n+dn+tr,0)]])}${copyBtn}`;return `${money(pm)}/month for ${n} months`}},

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
 after(){document.querySelectorAll('[data-fgt]').forEach(b=>b.onclick=()=>{$('#fgt').value=b.dataset.fgt;update()})}},
{id:'scientific',cat:'Math',name:'Scientific calculator',kw:'calculator scientific calculator online calculator basic calculator sin cos tan log ln square root exponent power factorial',desc:'An online calculator with trig, logs, powers and roots.',
 state:{expr:'',deg:true,ans:0,hist:[],last:null},
 ROWS:[['sin','cos','tan','ln','log'],['(',')','√','x²','xʸ'],['π','e','n!','%','EXP'],['7','8','9','÷','AC'],['4','5','6','×','⌫'],['1','2','3','−','Ans'],['0','.','+','=']],
 INS:{'sin':'sin(','cos':'cos(','tan':'tan(','ln':'ln(','log':'log(','√':'√(','x²':'^2','xʸ':'^','n!':'!','EXP':'E'},
 render(){const k=r=>r.map(x=>`<button type="button" class="key${/^[0-9.]$/.test(x)?' num':''}${x==='='?' eq':''}${x==='0'?' zero':''}${['AC','⌫'].includes(x)?' clr':''}" data-k="${x}">${x}</button>`).join('');
  return `<div class="inputs"><div class="calc"><div class="screen"><div class="expr" id="scx" aria-live="polite">${esc(this.state.expr)||'&nbsp;'}</div><div class="val" id="scv">0</div></div>
  <div class="actions">${seg('scm',[['deg','Degrees'],['rad','Radians']],this.state.deg?'deg':'rad')}</div>
  <div class="keys">${this.ROWS.map(k).join('')}</div></div><p class="hint">You can also type: numbers, + − * / ^ ( ) %, Enter for =, Backspace and Esc.</p></div><div class="result" id="out"></div>`},
 tok(s){s=s.replace(/E/g,'×10^');const t=[];let i=0;while(i<s.length){const c=s[i];
   if(/[0-9.]/.test(c)){let j=i;while(j<s.length&&/[0-9.]/.test(s[j]))j++;const x=s.slice(i,j);if((x.match(/\./g)||[]).length>1||x==='.')throw 0;t.push({n:parseFloat(x)});i=j;continue}
   if(/[a-zA-Z]/.test(c)){let j=i;while(j<s.length&&/[a-zA-Z]/.test(s[j]))j++;const w=s.slice(i,j).toLowerCase();i=j;
     if(w==='ans')t.push({n:this.state.ans});else if(w==='e')t.push({n:Math.E});else if(w==='pi')t.push({n:Math.PI});else if(['sin','cos','tan','asin','acos','atan','ln','log','sqrt'].includes(w))t.push({f:w});else throw 0;continue}
   if(c==='π'){t.push({n:Math.PI});i++;continue}if(c==='√'){t.push({f:'sqrt'});i++;continue}
   const o={'+':'+','-':'-','−':'-','*':'*','×':'*','/':'/','÷':'/','^':'^','%':'%','!':'!','(':'(',')':')'}[c];if(o){t.push({o});i++;continue}
   if(c===' '){i++;continue}throw 0}return t},
 evalx(s){const t=this.tok(s);let p=0;const deg=this.state.deg;const peek=()=>t[p],eat=o=>{if(t[p]&&t[p].o===o){p++;return true}return false};
  const starts=x=>x&&(x.n!==undefined||x.f||x.o==='(');
  const fact=n=>{if(n<0||n!==Math.floor(n)||n>170)throw 0;let r=1;for(let i=2;i<=n;i++)r*=i;return r};
  const fn=(f,x)=>{const a=deg?x*Math.PI/180:x,snap=v=>Math.abs(v)<1e-12?0:v;
    if(f==='sin')return snap(Math.sin(a));if(f==='cos')return snap(Math.cos(a));if(f==='tan'){const c=Math.cos(a);if(Math.abs(c)<1e-12)throw 0;return snap(Math.sin(a)/c)}
    if(f==='asin')return Math.asin(x)*(deg?180/Math.PI:1);if(f==='acos')return Math.acos(x)*(deg?180/Math.PI:1);if(f==='atan')return Math.atan(x)*(deg?180/Math.PI:1);
    if(f==='ln'){if(x<=0)throw 0;return Math.log(x)}if(f==='log'){if(x<=0)throw 0;return Math.log10(x)}if(f==='sqrt'){if(x<0)throw 0;return Math.sqrt(x)}throw 0};
  const primary=()=>{const x=peek();if(!x)throw 0;
    if(x.n!==undefined){p++;return x.n}
    if(x.f){p++;if(eat('(')){const v=expr();if(!eat(')'))throw 0;return fn(x.f,v)}return fn(x.f,postfix())}
    if(eat('(')){const v=expr();if(!eat(')'))throw 0;return v}throw 0};
  const postfix=()=>{let v=primary();for(;;){if(eat('!'))v=fact(v);else if(eat('%'))v=v/100;else break}return v};
  const unary=()=>{if(eat('-'))return -unary();if(eat('+'))return unary();return power()};
  const power=()=>{const b=postfix();if(eat('^')){const e=unary();return Math.pow(b,e)}return b};
  const term=()=>{let v=unary();for(;;){if(eat('*'))v*=unary();else if(eat('/')){const d=unary();if(d===0)throw 0;v/=d}else if(starts(peek()))v*=unary();else break}return v};
  const expr=()=>{let v=term();for(;;){if(eat('+'))v+=term();else if(eat('-'))v-=term();else break}return v};
  const v=expr();if(p!==t.length||!isFinite(v))throw 0;return v},
 fmt(v){if(v===0)return '0';const a=Math.abs(v);if(a>=1e15||a<1e-9)return v.toExponential(9).replace(/\.?0+e/,'e');return String(parseFloat(v.toPrecision(12)))},
 closed(s){const o=(s.match(/\(/g)||[]).length-(s.match(/\)/g)||[]).length;return s+')'.repeat(Math.max(0,o))},
 press(k){const s=this.state;
  if(k==='AC'){s.expr='';s.last=null}else if(k==='⌫'){s.expr=s.expr.replace(/(sin\(|cos\(|tan\(|ln\(|log\(|√\(|Ans|.)$/,'')}
  else if(k==='='){if(!s.expr)return;try{const v=this.evalx(this.closed(s.expr));s.hist.unshift([this.closed(s.expr),this.fmt(v)]);s.hist=s.hist.slice(0,5);s.ans=v;s.last=v;s.expr=''}catch(e){s.hist.unshift([this.closed(s.expr),'Error']);s.hist=s.hist.slice(0,5);s.last='Error';s.expr=''}}
  else{if(s.last!==null&&s.expr===''&&/^[+−×÷^%!]|x²|xʸ/.test(k))s.expr='Ans';if(s.last!==null&&s.expr===''&&/^[0-9.(π√]|sin|cos|tan|ln|log|e$/.test(k))s.last=null;s.expr+=this.INS[k]||k}
  update()},
 calc(){const s=this.state;let live='';if(s.expr){try{live=this.fmt(this.evalx(this.closed(s.expr)))}catch(e){live=''}}
  const shown=s.expr?(live||'…'):(s.last===null?'0':typeof s.last==='number'?this.fmt(s.last):s.last);
  $('#scx').innerHTML=esc(s.expr)||(s.hist[0]?esc(s.hist[0][0])+' =':'&nbsp;');$('#scv').textContent=shown;
  $('#out').innerHTML=`<span class="label">Result</span><div class="big"><em>${esc(shown)}</em></div>${kv([['Angle mode',s.deg?'Degrees':'Radians']].concat(s.hist.map(h=>[esc(h[0]),h[1]])))}${copyBtn}`;
  return shown},
 after(){const self=this;document.querySelectorAll('.keys .key').forEach(b=>b.onclick=()=>self.press(b.dataset.k));bindSeg('scm',m=>{self.state.deg=m==='deg';update()});
  if(!this.kb){this.kb=true;document.addEventListener('keydown',e=>{if(cur!==self||e.ctrlKey||e.metaKey||e.altKey)return;const tg=e.target;if(tg&&(tg.tagName==='INPUT'||tg.tagName==='TEXTAREA'||tg.tagName==='SELECT'))return;
    const m={'Enter':'=','=':'=','Backspace':'⌫','Escape':'AC','*':'×','/':'÷','-':'−','+':'+','^':'xʸ','(':'(',')':')','%':'%','.':'.','!':'n!'};const k=/^[0-9]$/.test(e.key)?e.key:m[e.key];if(!k)return;e.preventDefault();self.press(k)})}}},

{id:'fraction',cat:'Math',name:'Fraction calculator',kw:'fraction calculator add subtract multiply divide fractions mixed numbers simplify',desc:'Add, subtract, multiply and divide fractions and mixed numbers.',
 render(){const f=(p,w,n,d)=>`<div class="frac"><input id="${p}w" type="number" step="1" value="${w}" aria-label="Whole number" placeholder="0"><div class="nd"><input id="${p}n" type="number" step="1" value="${n}" aria-label="Numerator"><input id="${p}d" type="number" step="1" value="${d}" aria-label="Denominator"></div></div>`;
  return `<div class="inputs"><div class="fracrow">${f('fa','',3,4)}<select id="fop" aria-label="Operation"><option value="+">+</option><option value="-">−</option><option value="*">×</option><option value="/">÷</option></select>${f('fb','',5,6)}</div>
  <p class="hint">The left box is an optional whole number for mixed numbers, such as 1 ¾. Leave it empty for a simple fraction.</p><div id="fsteps"></div></div><div class="result" id="out"></div>`},
 calc(){const g=(a,b)=>{a=Math.abs(a);b=Math.abs(b);while(b){[a,b]=[b,a%b]}return a||1};
  const rd=p=>{const w=parseInt($('#'+p+'w').value)||0,n=parseInt($('#'+p+'n').value)||0,d=parseInt($('#'+p+'d').value);if(!d)return null;const s=(w<0||(w===0&&(n<0)!==(d<0)))?-1:1;return[s*(Math.abs(w)*Math.abs(d)+Math.abs(n)),Math.abs(d)]};
  const a=rd('fa'),b=rd('fb'),op=$('#fop').value;if(!a||!b){$('#out').innerHTML='<span class="label">Result</span><p class="hint">A denominator can’t be 0 or empty.</p>';$('#fsteps').innerHTML='';return''}
  let n,d,steps;const F=(x,y)=>`${x}/${y}`;
  if(op==='+'||op==='-'){const l=a[1]/g(a[1],b[1])*b[1],x=a[0]*(l/a[1]),y=b[0]*(l/b[1]);n=op==='+'?x+y:x-y;d=l;steps=`${F(a[0],a[1])} ${op==='+'?'+':'−'} ${F(b[0],b[1])} = ${F(x,l)} ${op==='+'?'+':'−'} ${F(y,l)} = ${F(n,l)}`}
  else if(op==='*'){n=a[0]*b[0];d=a[1]*b[1];steps=`${F(a[0],a[1])} × ${F(b[0],b[1])} = ${F(a[0]+'×'+b[0],a[1]+'×'+b[1])} = ${F(n,d)}`}
  else{if(b[0]===0){$('#out').innerHTML='<span class="label">Result</span><p class="hint">You can’t divide by zero.</p>';$('#fsteps').innerHTML='';return''}n=a[0]*b[1];d=a[1]*b[0];if(d<0){n=-n;d=-d}steps=`${F(a[0],a[1])} ÷ ${F(b[0],b[1])} = ${F(a[0],a[1])} × ${F(b[1],b[0])} = ${F(n,d)}`}
  const k=g(n,d),sn=n/k,sd=d/k,w=Math.trunc(sn/sd),rm=Math.abs(sn%sd);
  const mixed=sd===1?String(sn):w===0?`${sn}/${sd}`:`${w} ${rm}/${sd}`;
  $('#fsteps').innerHTML=`<div class="field"><label>Working</label></div><p class="formula">${steps}${k>1?`\n= ${F(sn,sd)} (divide top and bottom by ${k})`:''}</p>`;
  $('#out').innerHTML=`<span class="label">Answer</span><div class="big"><em>${sd===1?sn:`${sn}/${sd}`}</em></div>${kv([['Mixed number',mixed],['Decimal',num(sn/sd,6)],['Percent',num(sn/sd*100,4)+'%']])}${copyBtn}`;return sd===1?String(sn):`${sn}/${sd}`}},

{id:'stdev',cat:'Math',name:'Standard deviation',kw:'standard deviation calculator variance mean median sample population statistics',desc:'Standard deviation, variance, mean and median of a data set.',
 render(){return `<div class="inputs"><div class="field"><label for="sdv">Numbers (separate with commas, spaces or new lines)</label><textarea id="sdv" rows="4">10, 12, 23, 23, 16, 23, 21, 16</textarea></div><p class="hint">Use sample standard deviation for data that is a sample of a bigger group, and population when you have every value.</p></div><div class="result" id="out"></div>`},
 calc(){const xs=$('#sdv').value.split(/[\s,;]+/).filter(Boolean).map(Number);if(xs.length<2||xs.some(x=>!isFinite(x))){$('#out').innerHTML='<span class="label">Result</span><p class="hint">Enter at least two numbers.</p>';return''}
  const n=xs.length,s=xs.reduce((a,b)=>a+b,0),m=s/n,ss=xs.reduce((a,b)=>a+(b-m)**2,0),srt=[...xs].sort((a,b)=>a-b),med=n%2?srt[(n-1)/2]:(srt[n/2-1]+srt[n/2])/2;
  $('#out').innerHTML=`<span class="label">Sample standard deviation</span><div class="big"><em>${num(Math.sqrt(ss/(n-1)),6)}</em></div>${kv([['Population standard deviation',num(Math.sqrt(ss/n),6)],['Sample variance',num(ss/(n-1),6)],['Population variance',num(ss/n,6)],['Mean',num(m,6)],['Median',num(med,6)],['Count',n],['Sum',num(s,6)],['Min / Max',`${num(srt[0],6)} / ${num(srt[n-1],6)}`],['Range',num(srt[n-1]-srt[0],6)]])}${copyBtn}`;
  return `s = ${num(Math.sqrt(ss/(n-1)),6)}`}},

{id:'compound',cat:'Money',name:'Compound interest',kw:'compound interest calculator savings investment growth monthly contribution future value',desc:'How savings grow with compound interest and monthly deposits.',
 render(){const c=R().cur;return `<div class="inputs"><div class="row">${field('ci0','Starting amount',10000,{unit:c})}${field('cim','Monthly deposit',200,{unit:c})}</div>
  <div class="row">${field('cir','Yearly interest rate',7,{unit:'%'})}${field('ciy','Years',10,{unit:'yrs'})}<div class="field"><label for="cik">Compounding</label><select id="cik"><option value="1">Yearly</option><option value="4">Quarterly</option><option value="12" selected>Monthly</option><option value="365">Daily</option></select></div></div>
  <div id="cigrow" class="tc-wrap"></div><p class="hint">Deposits are added at the end of each month. Taxes and fees are not included.</p></div><div class="result" id="out"></div>`},
 calc(){const p0=v('ci0')||0,dm=v('cim')||0,r=(v('cir')||0)/100,y=Math.min(100,Math.max(0,Math.round(v('ciy')||0))),k=+$('#cik').value;const mr=Math.pow(1+r/k,k/12)-1;
  let b=p0,dep=p0;const rows=[];for(let i=1;i<=y*12;i++){b=b*(1+mr)+dm;dep+=dm;if(i%12===0)rows.push([i/12,dep,b-dep,b])}
  $('#cigrow').innerHTML=rows.length?`<table><thead><tr><th>Year</th><th>Deposits</th><th>Interest</th><th>Balance</th></tr></thead><tbody>${rows.map(([yy,d,it,bb])=>`<tr><td>${yy}</td><td class="num">${money(d,0)}</td><td class="num">${money(it,0)}</td><td class="num">${money(bb,0)}</td></tr>`).join('')}</tbody></table>`:'';
  $('#out').innerHTML=`<span class="label">Balance after ${y} ${y===1?'year':'years'}</span><div class="big"><em>${money(b,0)}</em></div>${kv([['Total deposits',money(dep,0)],['Interest earned',money(b-dep,0)],['Effective yearly rate',num((Math.pow(1+r/k,k)-1)*100,3)+'%']])}${copyBtn}`;return `${money(b,0)} after ${y} years`}},

{id:'salestax',cat:'Money',name:'Sales tax',kw:'sales tax calculator vat gst hst add tax remove tax reverse sales tax price before tax',desc:'Add or remove sales tax, VAT or GST from a price.',
 state:{mode:'add'},
 DEF:{US:7,CA:13,AU:10,UK:20,NL:21},
 render(){const c=R().cur,add=this.state.mode==='add';return `<div class="inputs">${seg('stm',[['add','Add tax to a price'],['rem','Remove tax from a total']],this.state.mode)}
  <div class="row">${field('stp',add?'Price before tax':'Total including tax',add?100:107,{unit:c})}${field('str','Tax rate',this.DEF[region]??7,{unit:'%'})}</div>
  <p class="hint">Rates differ by state and province. Typical rates: UK VAT 20%, Netherlands BTW 21%, Australia GST 10%, Canada GST 5% or HST 13–15%. US sales tax is set by each state and city.</p></div><div class="result" id="out"></div>`},
 calc(){const p=v('stp')||0,r=(v('str')||0)/100,add=this.state.mode==='add';const pre=add?p:p/(1+r),tax=pre*r,tot=pre+tax;
  $('#out').innerHTML=`<span class="label">${add?'Total with tax':'Price before tax'}</span><div class="big"><em>${money(add?tot:pre)}</em></div>${kv([['Price before tax',money(pre)],['Tax',money(tax)],['Total',money(tot)]])}${copyBtn}`;return add?`Total ${money(tot)}`:`Before tax ${money(pre)}`},
 after(){bindSeg('stm',m=>{this.state.mode=m;open('salestax')})}},

{id:'duedate',cat:'Health',name:'Due date',kw:'due date calculator pregnancy calculator how far along am i weeks pregnant conception ivf',desc:'Estimated due date, how many weeks pregnant, and trimester dates.',
 state:{mode:'lmp'},
 render(){const iso=d=>new Date(d-d.getTimezoneOffset()*6e4).toISOString().slice(0,10);const t=new Date();const ex=new Date(t.getFullYear(),t.getMonth(),t.getDate()-70);const m=this.state.mode;
  return `<div class="inputs">${seg('ddm',[['lmp','First day of last period'],['conc','Conception date'],['ivf','IVF transfer']],m)}
  <div class="row">${field('ddd',m==='lmp'?'First day of last period':m==='conc'?'Conception date':'Transfer date',iso(ex),{type:'date'})}${m==='lmp'?field('ddc','Average cycle length',28,{unit:'days'}):m==='ivf'?`<div class="field"><label for="ddi">Embryo age</label><select id="ddi"><option value="3">Day 3</option><option value="5" selected>Day 5</option></select></div>`:''}</div>
  <p class="hint">An estimate only. Your doctor or midwife will confirm the date, often with an early ultrasound. Most babies arrive within two weeks either side of it.</p><div id="ddtri"></div></div><div class="result" id="out"></div>`},
 calc(){const d=new Date($('#ddd').value+'T00:00');if(isNaN(d)){$('#out').innerHTML='<span class="label">Result</span><p class="hint">Pick a date.</p>';return''}
  const m=this.state.mode,add=(x,n)=>new Date(x.getFullYear(),x.getMonth(),x.getDate()+n);let due;
  if(m==='lmp')due=add(d,280+((v('ddc')||28)-28));else if(m==='conc')due=add(d,266);else due=add(d,266-(+$('#ddi').value));
  const start=add(due,-280),t=new Date(),today=new Date(t.getFullYear(),t.getMonth(),t.getDate()),ga=Math.round((today-start)/864e5),f=x=>x.toLocaleDateString(R().loc,{weekday:'short',month:'long',day:'numeric',year:'numeric'});
  const along=ga<0?'Not yet started':ga>300?'Past the due date range':`${Math.floor(ga/7)} weeks, ${ga%7} ${ga%7===1?'day':'days'}`;
  const tri=ga<0||ga>300?'—':ga<98?'First':ga<196?'Second':'Third';
  $('#ddtri').innerHTML=`<div class="tc-wrap"><table><thead><tr><th>Milestone</th><th>Date</th></tr></thead><tbody>
   <tr><td>Conception (about)</td><td>${f(add(start,14))}</td></tr><tr><td>First trimester ends (end of week 13)</td><td>${f(add(start,97))}</td></tr><tr><td>Second trimester ends (end of week 27)</td><td>${f(add(start,195))}</td></tr><tr><td>Full term (37 weeks)</td><td>${f(add(start,259))}</td></tr><tr><td>Due date (40 weeks)</td><td>${f(due)}</td></tr></tbody></table></div>`;
  $('#out').innerHTML=`<span class="label">Estimated due date</span><div class="big"><em>${due.toLocaleDateString(R().loc,{month:'short',day:'numeric',year:'numeric'})}</em></div>${kv([['How far along today',along],['Trimester',tri],['Days to go',ga<0||ga>300?'—':num(Math.max(0,280-ga),0)]])}${copyBtn}`;return `Due ${f(due)}`},
 after(){bindSeg('ddm',x=>{this.state.mode=x;open('duedate')})}},

{id:'bodyfat',cat:'Health',name:'Body fat',kw:'body fat calculator navy method body fat percentage waist neck hip lean mass',desc:'Body fat percentage with the US Navy tape method.',
 state:{sys:null,sex:'m'},
 render(){const s=this.state.sys||(R().imperial?'imp':'met');this.state.sys=s;const u=s==='imp'?'in':'cm',w=s==='imp'?'lb':'kg',m=this.state.sex==='m',I=s==='imp';
  return `<div class="inputs"><div class="actions">${seg('bfs',[['imp','Inches / lb'],['met','cm / kg']],s)}${seg('bfx',[['m','Male'],['f','Female']],this.state.sex)}</div>
  <div class="row">${field('bfh','Height',I?(m?69:64):(m?175:163),{unit:u})}${field('bfw','Weight',I?(m?180:150):(m?82:68),{unit:w})}</div>
  <div class="row">${field('bfn','Neck',I?(m?15.5:13):(m?39:33),{unit:u})}${field('bfa','Waist',I?(m?34:30):(m?86:76),{unit:u})}${m?'':field('bfp','Hips',I?40:102,{unit:u})}</div>
  <p class="hint">${m?'Measure the waist at the navel':'Measure the waist at its narrowest point and the hips at their widest'}, and the neck just below the larynx. Keep the tape level and snug, not tight.</p></div><div class="result" id="out"></div>`},
 calc(){const k=this.state.sys==='imp'?1:1/2.54,h=v('bfh')*k,n=v('bfn')*k,a=v('bfa')*k,hp=this.state.sex==='f'?v('bfp')*k:0,m=this.state.sex==='m';
  const arg=m?a-n:a+hp-n;if(!(arg>0&&h>0)){$('#out').innerHTML='<span class="label">Result</span><p class="hint">Check the measurements: the waist must be bigger than the neck.</p>';return''}
  const bf=m?86.010*Math.log10(arg)-70.041*Math.log10(h)+36.76:163.205*Math.log10(arg)-97.684*Math.log10(h)-78.387;
  const cats=m?[[2,'Essential fat'],[6,'Athletes'],[14,'Fitness'],[18,'Average'],[25,'Obese']]:[[10,'Essential fat'],[14,'Athletes'],[21,'Fitness'],[25,'Average'],[32,'Obese']];
  let cat='Below essential fat';for(const[c,l]of cats)if(bf>=c)cat=l;const wt=v('bfw'),wu=this.state.sys==='imp'?'lb':'kg';
  $('#out').innerHTML=`<span class="label">Body fat</span><div class="big"><em>${num(bf,1)}%</em></div>${kv([['Category (ACE)',cat]].concat(wt>0?[['Fat mass',num(wt*bf/100,1)+' '+wu],['Lean mass',num(wt*(1-bf/100),1)+' '+wu]]:[]))}${copyBtn}`;return `Body fat ${num(bf,1)}%`},
 after(){bindSeg('bfs',x=>{this.state.sys=x;open('bodyfat')});bindSeg('bfx',x=>{this.state.sex=x;open('bodyfat')})}},

{id:'password',cat:'Fun',name:'Password generator',kw:'password generator strong random password secure generate',desc:'Strong random passwords, made in your browser.',
 state:{pw:[],key:''},
 SETS:{pu:'ABCDEFGHJKLMNPQRSTUVWXYZ',pl:'abcdefghijkmnopqrstuvwxyz',pd:'23456789',ps:'!@#$%^&*-_=+?'},
 FULL:{pu:'ABCDEFGHIJKLMNOPQRSTUVWXYZ',pl:'abcdefghijklmnopqrstuvwxyz',pd:'0123456789',ps:'!@#$%^&*()-_=+[]{};:,.?/'},
 render(){const c=(id,l)=>`<label class="chk"><input type="checkbox" id="${id}" checked> ${l}</label>`;
  return `<div class="inputs"><div class="row">${field('pwl','Length',16,{step:'1'})}</div><div class="chks">${c('pu','Uppercase A–Z')}${c('pl','Lowercase a–z')}${c('pd','Numbers 0–9')}${c('ps','Symbols !@#')}<label class="chk"><input type="checkbox" id="pa"> Avoid look-alikes (0 O 1 l I)</label></div>
  <div class="actions"><button class="btn primary" type="button" id="pwgo">Generate new</button></div><div id="pwlist"></div><p class="hint">Passwords are made with your browser's cryptographic random generator and never leave your device.</p></div><div class="result" id="out"></div>`},
 rnd(n){const lim=Math.floor(4294967296/n)*n,a=new Uint32Array(1);do{crypto.getRandomValues(a)}while(a[0]>=lim);return a[0]%n},
 gen(){const L=Math.min(128,Math.max(4,Math.round(v('pwl')||16))),src=$('#pa').checked?this.SETS:this.FULL,on=['pu','pl','pd','ps'].filter(k=>$('#'+k).checked);if(!on.length)return null;
  const pool=on.map(k=>src[k]).join(''),one=()=>{const ch=on.map(k=>src[k][this.rnd(src[k].length)]);while(ch.length<L)ch.push(pool[this.rnd(pool.length)]);for(let i=ch.length-1;i>0;i--){const j=this.rnd(i+1);[ch[i],ch[j]]=[ch[j],ch[i]]}return ch.slice(0,L).join('')};
  return{list:[one(),one(),one(),one(),one()],bits:L*Math.log2(pool.length)}},
 calc(){const key=['pwl','pu','pl','pd','ps','pa'].map(i=>{const e=$('#'+i);return e.type==='checkbox'?e.checked:e.value}).join('|');if(this.state.key!==key){this.state.key=key;this.state.pw=this.gen()}const g=this.state.pw;
  if(!g){$('#out').innerHTML='<span class="label">Password</span><p class="hint">Choose at least one character type.</p>';$('#pwlist').innerHTML='';return''}
  const s=g.bits<40?'Weak':g.bits<60?'Fair':g.bits<80?'Strong':'Very strong';
  $('#pwlist').innerHTML=`<div class="field"><label>More options</label></div><ul class="pwl">${g.list.slice(1).map(p=>`<li><code>${esc(p)}</code></li>`).join('')}</ul>`;
  $('#out').innerHTML=`<span class="label">Your password</span><div class="big pw"><em>${esc(g.list[0])}</em></div>${kv([['Strength',s],['Entropy',num(g.bits,0)+' bits'],['Length',g.list[0].length]])}${copyBtn}`;return g.list[0]},
 after(){$('#pwgo').onclick=()=>{this.state.key='';update()}}}
,
{id:'bmr',cat:'Health',name:'BMR calculator',kw:'bmr calculator basal metabolic rate resting metabolic rate rmr calories at rest mifflin st jeor harris benedict tdee',desc:'Calories your body burns at rest each day.',
 state:{sex:'m',unit:null},
 render(){const s=this.state;if(!s.unit)s.unit=R().imperial?'imp':'met';const imp=s.unit==='imp';
  return `<div class="inputs"><div class="row">${seg('bms',[['m','Male'],['f','Female']],s.sex)}${seg('bmu',[['imp','US units'],['met','Metric']],s.unit)}</div>
  <div class="row">${field('bma','Age',35,{unit:'yrs'})}${imp?field('bmft','Height (feet)',5,{unit:'ft'})+field('bmin','Height (inches)',10,{unit:'in'}):field('bmcm','Height',178,{unit:'cm'})}${field('bmw','Weight',imp?181:82,{unit:imp?'lb':'kg'})}</div>
  <div id="bmtab" class="tc-wrap"></div><p class="hint">For adults 18 and over. An estimate, not medical advice.</p></div><div class="result" id="out"></div>`},
 calc(){const s=this.state,imp=s.unit==='imp',a=v('bma');const h=imp?((v('bmft')||0)*12+(v('bmin')||0))*2.54:v('bmcm'),w=imp?v('bmw')*0.45359237:v('bmw');
  if(!(a>0&&h>0&&w>0)){$('#out').innerHTML='<span class="label">BMR</span><p class="hint">Enter your age, height and weight.</p>';$('#bmtab').innerHTML='';return''}
  const m=s.sex==='m';const mif=10*w+6.25*h-5*a+(m?5:-161),hb=m?88.362+13.397*w+4.799*h-5.677*a:447.593+9.247*w+3.098*h-4.330*a;
  const A=[['Sedentary',1.2],['Light exercise 1–3 days/week',1.375],['Moderate exercise 3–5 days/week',1.55],['Hard exercise 6–7 days/week',1.725],['Very hard exercise or physical job',1.9]];
  $('#bmtab').innerHTML=`<table><thead><tr><th>Activity level</th><th style="text-align:right">Calories/day</th></tr></thead><tbody>${A.map(([n,f])=>`<tr><td>${n}</td><td class="num">${num(mif*f,0)}</td></tr>`).join('')}</tbody></table>`;
  $('#out').innerHTML=`<span class="label">Your BMR (Mifflin-St Jeor)</span><div class="big"><em>${num(mif,0)}</em> calories/day</div>${kv([['Harris-Benedict (revised)',num(hb,0)+' cal'],['Per hour at rest',num(mif/24,0)+' cal'],['Daily calories, moderately active',num(mif*1.55,0)+' cal']])}${copyBtn}`;
  return `BMR ${num(mif,0)} calories/day`},
 after(){bindSeg('bms',x=>{this.state.sex=x;update()});bindSeg('bmu',x=>{this.state.unit=x;open('bmr')})}},

{id:'ratio',cat:'Math',name:'Ratio calculator',kw:'ratio calculator proportion calculator solve proportion simplify ratio cross multiply aspect ratio scale',desc:'Solve proportions and simplify ratios.',
 render(){return `<div class="inputs"><div class="row">${field('ra','A',3)}${field('rb','B',4)}</div><p class="hint">A : B = C : D. Enter C to find the missing value D.</p><div class="row">${field('rc','C',12)}</div></div><div class="result" id="out"></div>`},
 simp(a,b){let k=1;while(k<1e6&&(Math.abs(a*k-Math.round(a*k))>1e-9||Math.abs(b*k-Math.round(b*k))>1e-9))k*=10;const x=Math.round(a*k),y=Math.round(b*k),g=gcd2(Math.abs(x),Math.abs(y))||1;return[x/g,y/g]},
 calc(){const a=v('ra'),b=v('rb'),c=v('rc');if(!isFinite(a)||!isFinite(b)||a===0){$('#out').innerHTML='<span class="label">Result</span><p class="hint">Enter A and B. A can’t be zero.</p>';return''}
  const [x,y]=this.simp(a,b),rows=[['Simplified ratio',`${num(x,6)} : ${num(y,6)}`],['As 1 : n',`1 : ${num(b/a,6)}`],['As n : 1',`${num(a/b,6)} : 1`],['As a fraction and decimal',`${num(x,6)}/${num(y,6)} = ${num(a/b,6)}`]];
  if(isFinite(c)){const d=b*c/a;$('#out').innerHTML=`<span class="label">Missing value D</span><div class="big"><em>${num(d,6)}</em></div><p class="hint">${num(a,6)} : ${num(b,6)} = ${num(c,6)} : ${num(d,6)}, because D = ${num(b,6)} × ${num(c,6)} ÷ ${num(a,6)}</p>${kv(rows)}${copyBtn}`;return `${a}:${b} = ${c}:${num(d,6)}`}
  $('#out').innerHTML=`<span class="label">Simplified ratio</span><div class="big"><em>${num(x,6)} : ${num(y,6)}</em></div>${kv(rows.slice(1))}${copyBtn}`;return `${a}:${b} = ${x}:${y}`}},

{id:'slope',cat:'Math',name:'Slope calculator',kw:'slope calculator find slope two points rise over run slope intercept form line equation y=mx+b gradient grade',desc:'Slope, equation and distance from two points.',
 render(){return `<div class="inputs"><div class="row">${field('sx1','x₁',2)}${field('sy1','y₁',3)}</div><div class="row">${field('sx2','x₂',6)}${field('sy2','y₂',11)}</div><div id="swork"></div></div><div class="result" id="out"></div>`},
 calc(){const x1=v('sx1'),y1=v('sy1'),x2=v('sx2'),y2=v('sy2');if([x1,y1,x2,y2].some(n=>!isFinite(n))){$('#out').innerHTML='<span class="label">Slope</span><p class="hint">Enter both points.</p>';$('#swork').innerHTML='';return''}
  const dx=x2-x1,dy=y2-y1,d=Math.hypot(dx,dy),mid=`(${num((x1+x2)/2,6)}, ${num((y1+y2)/2,6)})`;
  if(dx===0){$('#swork').innerHTML='';$('#out').innerHTML=`<span class="label">Slope</span><div class="big"><em>Undefined</em></div><p class="hint">The line is vertical: x = ${num(x1,6)}</p>${kv([['Distance',num(d,6)],['Midpoint',mid],['Angle','90°']])}${copyBtn}`;return 'Slope undefined (vertical line)'}
  const m=dy/dx,b=y1-m*x1,eq=`y = ${m===0?'':num(m,6)+'x'}${m===0?num(b,6):b===0?'':(b>0?' + ':' − ')+num(Math.abs(b),6)}`;
  $('#swork').innerHTML=`<p class="hint">m = (${num(y2,6)} − ${num(y1,6)}) ÷ (${num(x2,6)} − ${num(x1,6)}) = ${num(dy,6)} ÷ ${num(dx,6)} = ${num(m,6)}</p>`;
  $('#out').innerHTML=`<span class="label">Slope (m)</span><div class="big"><em>${num(m,6)}</em></div>${kv([['Equation',eq],['y-intercept (b)',num(b,6)],['x-intercept',m===0?'None':num(-b/m,6)],['Angle',num(Math.atan(m)*180/Math.PI,4)+'°'],['Grade',num(m*100,4)+'%'],['Distance',num(d,6)],['Midpoint',mid]])}${copyBtn}`;
  return `m = ${num(m,6)}, ${eq}`}},

{id:'protein',cat:'Health',name:'Protein calculator',kw:'protein calculator how much protein do i need a day grams of protein per day muscle gain weight loss',desc:'How much protein you need a day.',
 state:{unit:null,goal:'mus'},
 G:{rda:[0.8,0.8,'Minimum for health (RDA)'],old:[1.0,1.2,'Adults 65 and over'],act:[1.2,1.6,'Regular exercise'],mus:[1.6,2.2,'Building muscle'],cut:[1.8,2.4,'Losing fat, keeping muscle']},
 render(){const s=this.state;if(!s.unit)s.unit=R().imperial?'lb':'kg';
  return `<div class="inputs"><div class="row">${field('prw','Body weight',s.unit==='lb'?180:82,{unit:s.unit})}<div class="field"><label>Units</label>${seg('pru',[['lb','lb'],['kg','kg']],s.unit)}</div></div>
  <div class="field"><label for="prg">Goal</label><select id="prg">${Object.entries(this.G).map(([k,g])=>`<option value="${k}"${k===s.goal?' selected':''}>${g[2]}</option>`).join('')}</select></div>
  <p class="hint">General guidance for healthy adults. Follow your doctor's advice if you have kidney disease.</p></div><div class="result" id="out"></div>`},
 calc(){const s=this.state;s.goal=$('#prg').value;const kg=s.unit==='lb'?v('prw')*0.45359237:v('prw');if(!(kg>0)){$('#out').innerHTML='<span class="label">Protein</span><p class="hint">Enter your weight.</p>';return''}
  const [lo,hi]=this.G[s.goal],a=kg*lo,b=kg*hi,r=lo===hi?`${num(a,0)} g`:`${num(a,0)}–${num(b,0)} g`;
  $('#out').innerHTML=`<span class="label">Protein per day</span><div class="big"><em>${r}</em></div>${kv([['Per meal (3 meals)',lo===hi?num(a/3,0)+' g':`${num(a/3,0)}–${num(b/3,0)} g`],['Per meal (4 meals)',lo===hi?num(a/4,0)+' g':`${num(a/4,0)}–${num(b/4,0)} g`],['Grams per kg',lo===hi?lo:`${lo}–${hi}`],['Calories from protein',lo===hi?num(a*4,0):`${num(a*4,0)}–${num(b*4,0)}`]])}${copyBtn}`;
  return `${r} of protein a day`},
 after(){bindSeg('pru',x=>{this.state.unit=x;open('protein')})}},

{id:'onerm',cat:'Health',name:'One rep max',kw:'one rep max calculator 1rm calculator bench press max squat deadlift epley brzycki strength',desc:'Estimate your 1RM from a set of reps.',
 state:{unit:null},
 render(){const s=this.state;if(!s.unit)s.unit=R().imperial?'lb':'kg';
  return `<div class="inputs"><div class="row">${field('orw','Weight lifted',s.unit==='lb'?225:100,{unit:s.unit})}${field('orr','Reps',5,{unit:'reps',step:1})}<div class="field"><label>Units</label>${seg('oru',[['lb','lb'],['kg','kg']],s.unit)}</div></div>
  <div id="ortab" class="tc-wrap"></div><p class="hint">Most accurate for sets of 2–10 reps taken close to failure.</p></div><div class="result" id="out"></div>`},
 calc(){const w=v('orw'),r=Math.round(v('orr')),u=this.state.unit;if(!(w>0)||!(r>=1&&r<=30)){$('#out').innerHTML='<span class="label">One rep max</span><p class="hint">Enter the weight and 1 to 30 reps.</p>';$('#ortab').innerHTML='';return''}
  const ep=r===1?w:w*(1+r/30),bz=r===1?w:r<37?w*36/(37-r):NaN,lb=w*Math.pow(r,0.1);
  const P=[[100,1],[95,2],[93,3],[90,4],[87,5],[85,6],[83,7],[80,8],[77,9],[75,10],[70,12],[65,15]];
  $('#ortab').innerHTML=`<table><thead><tr><th>% of 1RM</th><th>Approx. reps</th><th style="text-align:right">Weight</th></tr></thead><tbody>${P.map(([p,n])=>`<tr><td>${p}%</td><td>${n}</td><td class="num">${num(ep*p/100,1)} ${u}</td></tr>`).join('')}</tbody></table>`;
  $('#out').innerHTML=`<span class="label">Estimated one rep max</span><div class="big"><em>${num(ep,1)}</em> ${u}</div>${kv([['Epley',num(ep,1)+' '+u],['Brzycki',num(bz,1)+' '+u],['Lombardi',num(lb,1)+' '+u],['Average',num((ep+bz+lb)/3,1)+' '+u]])}${r>12?'<p class="hint">Over 12 reps the estimate is rough.</p>':''}${copyBtn}`;
  return `1RM ≈ ${num(ep,1)} ${u}`},
 after(){bindSeg('oru',x=>{this.state.unit=x;open('onerm')})}},

{id:'macro',cat:'Health',name:'Macro calculator',kw:'macro calculator macros carbs protein fat grams iifym keto macros high protein diet',desc:'Split daily calories into carbs, protein and fat.',
 state:{split:'bal'},
 S:{bal:[50,20,30,'Balanced'],hp:[40,30,30,'High protein'],lc:[25,35,40,'Low carb'],keto:[5,25,70,'Keto'],cus:[null,null,null,'Custom']},
 render(){const s=this.state,c=this.S[s.split];
  return `<div class="inputs">${field('mcal','Daily calories',2200,{unit:'cal'})}<p class="hint">Don't know your calories? Use the <a href="/calorie-calculator/">calorie calculator</a>.</p>
  ${seg('msp',Object.entries(this.S).map(([k,x])=>[k,x[3]]),s.split)}
  ${s.split==='cus'?`<div class="row">${field('mc','Carbs',40,{unit:'%'})}${field('mp','Protein',30,{unit:'%'})}${field('mf','Fat',30,{unit:'%'})}</div>`:`<p class="hint">${c[0]}% carbs, ${c[1]}% protein, ${c[2]}% fat.</p>`}</div><div class="result" id="out"></div>`},
 calc(){const s=this.state,k=v('mcal');let [c,p,f]=this.S[s.split];if(s.split==='cus'){c=v('mc')||0;p=v('mp')||0;f=v('mf')||0}
  if(!(k>0)){$('#out').innerHTML='<span class="label">Macros</span><p class="hint">Enter your daily calories.</p>';return''}
  const t=c+p+f,C=k*c/100/4,P=k*p/100/4,F=k*f/100/9;
  $('#out').innerHTML=`<span class="label">Daily macros</span><div class="big"><em>${num(P,0)} g</em> protein</div>${kv([['Carbs',`${num(C,0)} g (${num(k*c/100,0)} cal)`],['Protein',`${num(P,0)} g (${num(k*p/100,0)} cal)`],['Fat',`${num(F,0)} g (${num(k*f/100,0)} cal)`],['Per meal (3 meals)',`${num(C/3,0)} g carbs, ${num(P/3,0)} g protein, ${num(F/3,0)} g fat`]])}${Math.abs(t-100)>0.01?`<p class="hint">Your percentages add up to ${num(t,1)}%, not 100%.</p>`:''}${copyBtn}`;
  return `${num(C,0)} g carbs, ${num(P,0)} g protein, ${num(F,0)} g fat`},
 after(){bindSeg('msp',x=>{this.state.split=x;open('macro')})}},

{id:'pace',cat:'Health',name:'Pace calculator',kw:'pace calculator running pace per mile per km minutes per mile speed mph 5k 10k half marathon marathon time',desc:'Running pace per mile or km, speed and finish times.',
 state:{unit:null},
 render(){const s=this.state;if(!s.unit)s.unit=R().imperial?'mi':'km';
  return `<div class="inputs"><div class="row">${field('pd','Distance',s.unit==='mi'?3.10686:5,{unit:s.unit})}<div class="field"><label>Units</label>${seg('pu',[['mi','Miles'],['km','km']],s.unit)}</div></div>
  <div class="actions" id="prace"><button type="button" class="chip" data-km="5">5K</button><button type="button" class="chip" data-km="10">10K</button><button type="button" class="chip" data-km="21.0975">Half marathon</button><button type="button" class="chip" data-km="42.195">Marathon</button></div>
  <div class="row">${field('ph','Hours',0,{unit:'h',step:1})}${field('pm','Minutes',28,{unit:'min',step:1})}${field('ps','Seconds',0,{unit:'s',step:1})}</div>
  <div id="ptab" class="tc-wrap"></div></div><div class="result" id="out"></div>`},
 t(sec){sec=Math.round(sec);const h=Math.floor(sec/3600),m=Math.floor(sec%3600/60),s=sec%60;return h?`${h}:${String(m).padStart(2,'0')}:${String(s).padStart(2,'0')}`:`${m}:${String(s).padStart(2,'0')}`},
 calc(){const d=v('pd'),u=this.state.unit,sec=(v('ph')||0)*3600+(v('pm')||0)*60+(v('ps')||0);if(!(d>0&&sec>0)){$('#out').innerHTML='<span class="label">Pace</span><p class="hint">Enter a distance and a time.</p>';$('#ptab').innerHTML='';return''}
  const km=u==='mi'?d*1.609344:d,pk=sec/km,pm=pk*1.609344;
  $('#ptab').innerHTML=`<table><thead><tr><th>At this pace</th><th style="text-align:right">Finish time</th></tr></thead><tbody>${[['1 mile',1.609344],['5K',5],['10K',10],['Half marathon',21.0975],['Marathon',42.195]].map(([n,k])=>`<tr><td>${n}</td><td class="num">${this.t(pk*k)}</td></tr>`).join('')}</tbody></table>`;
  $('#out').innerHTML=`<span class="label">Pace per ${u==='mi'?'mile':'km'}</span><div class="big"><em>${this.t(u==='mi'?pm:pk)}</em></div>${kv([['Pace per mile',this.t(pm)],['Pace per km',this.t(pk)],['Speed',`${num(km/1.609344/(sec/3600),2)} mph · ${num(km/(sec/3600),2)} km/h`]])}${copyBtn}`;
  return `${this.t(pm)} per mile, ${this.t(pk)} per km`},
 after(){bindSeg('pu',x=>{if(x===this.state.unit)return;const d=v('pd'),k=['ph','pm','ps'].map(i=>$('#'+i).value);this.state.unit=x;open('pace');['ph','pm','ps'].forEach((i,j)=>$('#'+i).value=k[j]);if(isFinite(d))$('#pd').value=+(x==='km'?d*1.609344:d/1.609344).toFixed(4);update()});
  $('#prace').addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;const k=+b.dataset.km;$('#pd').value=+(this.state.unit==='mi'?k/1.609344:k).toFixed(4);update()})}},

{id:'average',cat:'Math',name:'Average calculator',kw:'average calculator mean median mode range calculator find the average of numbers arithmetic mean',desc:'Mean, median, mode and range of a list of numbers.',
 render(){return `<div class="inputs"><div class="field"><label for="avv">Numbers (separate with commas, spaces or new lines)</label><textarea id="avv" rows="4">4, 8, 15, 16, 23, 42</textarea></div></div><div class="result" id="out"></div>`},
 calc(){const xs=$('#avv').value.split(/[\s,;]+/).filter(Boolean).map(Number);if(!xs.length||xs.some(x=>!isFinite(x))){$('#out').innerHTML='<span class="label">Average</span><p class="hint">Enter one or more numbers.</p>';return''}
  const n=xs.length,s=xs.reduce((a,b)=>a+b,0),m=s/n,srt=[...xs].sort((a,b)=>a-b),med=n%2?srt[(n-1)/2]:(srt[n/2-1]+srt[n/2])/2;
  const cnt={};xs.forEach(x=>cnt[x]=(cnt[x]||0)+1);const top=Math.max(...Object.values(cnt));const modes=top>1?Object.keys(cnt).filter(k=>cnt[k]===top).map(Number).sort((a,b)=>a-b):[];
  const gm=xs.every(x=>x>0)?Math.exp(xs.reduce((a,x)=>a+Math.log(x),0)/n):NaN;
  $('#out').innerHTML=`<span class="label">Average (mean)</span><div class="big"><em>${num(m,6)}</em></div><p class="hint">${num(s,6)} ÷ ${n} = ${num(m,6)}</p>${kv([['Median',num(med,6)],['Mode',modes.length?modes.map(x=>num(x,6)).join(', ')+` (appears ${top} times)`:'None'],['Range',num(srt[n-1]-srt[0],6)],['Min / Max',`${num(srt[0],6)} / ${num(srt[n-1],6)}`],['Sum',num(s,6)],['Count',n],['Geometric mean',isFinite(gm)?num(gm,6):'Needs all positive numbers']])}${copyBtn}`;
  return `Mean ${num(m,6)}, median ${num(med,6)}`}},

{id:'triangle',cat:'Math',name:'Right triangle',kw:'right triangle calculator pythagorean theorem calculator hypotenuse calculator a2+b2=c2 missing side angle trigonometry',desc:'Hypotenuse, sides, angles and area of a right triangle.',
 render(){return `<div class="inputs"><div class="row">${field('ta','Side a (leg)',5)}${field('tb','Side b (leg)',12)}${field('tc','Hypotenuse c','')}</div><p class="hint">Enter any two sides and leave the third blank.</p></div><div class="result" id="out"></div>`},
 calc(){let a=v('ta'),b=v('tb'),c=v('tc');const has=[a,b,c].map(x=>isFinite(x)&&x>0),k=has.filter(Boolean).length;const bad=t=>{$('#out').innerHTML=`<span class="label">Right triangle</span><p class="hint">${t}</p>`;return''};
  if(k<2)return bad('Enter two of the three sides.');let find='';
  if(has[0]&&has[1]&&!has[2]){c=Math.hypot(a,b);find='c'}else if(has[0]&&has[2]&&!has[1]){if(c<=a)return bad('The hypotenuse must be longer than each leg.');b=Math.sqrt(c*c-a*a);find='b'}
  else if(has[1]&&has[2]&&!has[0]){if(c<=b)return bad('The hypotenuse must be longer than each leg.');a=Math.sqrt(c*c-b*b);find='a'}else return bad('Leave one side blank so it can be found.');
  const A=Math.asin(a/c)*180/Math.PI,nm={a:'Side a',b:'Side b',c:'Hypotenuse c'}[find],val={a,b,c}[find];
  $('#out').innerHTML=`<span class="label">${nm}</span><div class="big"><em>${num(val,6)}</em></div>${kv([['Sides a, b, c',`${num(a,4)}, ${num(b,4)}, ${num(c,4)}`],['Angle A (opposite a)',num(A,4)+'°'],['Angle B (opposite b)',num(90-A,4)+'°'],['Area',num(a*b/2,6)],['Perimeter',num(a+b+c,6)],['Height to hypotenuse',num(a*b/c,6)]])}${copyBtn}`;
  return `${find} = ${num(val,6)}`}},

{id:'quadratic',cat:'Math',name:'Quadratic formula',kw:'quadratic formula calculator quadratic equation solver roots discriminant ax2+bx+c factoring parabola vertex',desc:'Solve ax² + bx + c = 0 with steps.',
 render(){return `<div class="inputs"><div class="row">${field('qa','a',1)}${field('qb','b',-5)}${field('qc','c',6)}</div><div id="qwork"></div></div><div class="result" id="out"></div>`},
 calc(){const a=v('qa'),b=v('qb'),c=v('qc'),n=x=>num(x,6);if(![a,b,c].every(isFinite)){$('#out').innerHTML='<span class="label">Roots</span><p class="hint">Enter a, b and c.</p>';$('#qwork').innerHTML='';return''}
  if(a===0){$('#qwork').innerHTML='';if(b===0){$('#out').innerHTML='<span class="label">Roots</span><p class="hint">With a and b both zero there is no x to solve for.</p>';return''}
   $('#out').innerHTML=`<span class="label">Linear equation (a = 0)</span><div class="big"><em>x = ${n(-c/b)}</em></div>${copyBtn}`;return `x = ${n(-c/b)}`}
  const D=b*b-4*a*c,vx=-b/(2*a),vy=c-b*b/(4*a);let r,txt;
  if(D>0){const s=Math.sqrt(D),x1=(-b+s)/(2*a),x2=(-b-s)/(2*a);r=`x = ${n(x1)} and x = ${n(x2)}`;txt=r}
  else if(D===0){r=`x = ${n(vx)}`;txt=r+' (repeated root)'}
  else{const im=Math.sqrt(-D)/(2*Math.abs(a));r=`x = ${n(vx)} ± ${n(im)}i`;txt=r}
  $('#qwork').innerHTML=`<p class="hint">D = b² − 4ac = (${n(b)})² − 4 × ${n(a)} × ${n(c)} = ${n(D)}<br>x = (${n(-b)} ± √${n(D)}) ÷ ${n(2*a)}</p>`;
  $('#out').innerHTML=`<span class="label">${D>0?'Two real roots':D===0?'One repeated root':'Two complex roots'}</span><div class="big"><em>${r}</em></div>${kv([['Discriminant',n(D)],['Vertex',`(${n(vx)}, ${n(vy)})`],['Axis of symmetry',`x = ${n(vx)}`],['Opens',a>0?'Upward (minimum)':'Downward (maximum)'],['y-intercept',n(c)]])}${copyBtn}`;
  return txt}},

{id:'cd',cat:'Money',name:'CD calculator',kw:'cd calculator certificate of deposit interest apy cd rates savings interest earned maturity',desc:'Interest earned on a certificate of deposit.',
 render(){const c=R().cur;return `<div class="inputs"><div class="row">${field('cdp','Deposit',10000,{unit:c})}${field('cdr','APY',4.5,{unit:'%'})}${field('cdt','Term',12,{unit:'months',step:1})}</div>
  <div id="cdtab" class="tc-wrap"></div><p class="hint">Uses the APY the bank quotes, which already includes compounding. Taxes and early-withdrawal penalties are not included.</p></div><div class="result" id="out"></div>`},
 calc(){const p=v('cdp'),r=(v('cdr')||0)/100,t=v('cdt');if(!(p>0&&t>0&&t<=600)){$('#out').innerHTML='<span class="label">CD</span><p class="hint">Enter a deposit and a term of 1 to 600 months.</p>';$('#cdtab').innerHTML='';return''}
  const bal=m=>p*Math.pow(1+r,m/12),b=bal(t);
  $('#cdtab').innerHTML=`<table><thead><tr><th>Term</th><th style="text-align:right">Interest</th><th style="text-align:right">Balance</th></tr></thead><tbody>${[[3,'3 months'],[6,'6 months'],[12,'1 year'],[18,'18 months'],[24,'2 years'],[36,'3 years'],[60,'5 years']].map(([m,nm])=>`<tr><td>${nm}</td><td class="num">${money(bal(m)-p)}</td><td class="num">${money(bal(m))}</td></tr>`).join('')}</tbody></table>`;
  $('#out').innerHTML=`<span class="label">Balance at maturity</span><div class="big"><em>${money(b)}</em></div>${kv([['Interest earned',money(b-p)],['Deposit',money(p)],['Term',`${num(t,0)} months`],['Interest per month (average)',money((b-p)/t)]])}${copyBtn}`;
  return `${money(b)} after ${num(t,0)} months`}},
{id:'halfbday',cat:'Dates & time',name:'Half birthday',kw:'half birthday calculator when is my half birthday six months birthday 6 month milestone',desc:'Find your half birthday and days until it.',
 render(){return `<div class="inputs">${field('hbd','Date of birth','2015-03-10',{type:'date'})}<div id="hblist"></div></div><div class="result" id="out"></div>`},
 half(b,y){let m=b.getMonth()+6,yy=y;if(m>11){m-=12;yy++}const last=new Date(yy,m+1,0).getDate();return new Date(yy,m,Math.min(b.getDate(),last))},
 calc(){const s=$('#hbd').value;if(!s){$('#out').innerHTML='<span class="label">Half birthday</span><p class="hint">Enter your date of birth.</p>';$('#hblist').innerHTML='';return''}
  const[a,b,c]=s.split('-').map(Number),bd=new Date(a,b-1,c),n=new Date(),t=new Date(n.getFullYear(),n.getMonth(),n.getDate());
  if(bd>t){$('#out').innerHTML='<span class="label">Half birthday</span><p class="hint">Enter a date in the past.</p>';$('#hblist').innerHTML='';return''}
  let y=t.getFullYear()-1,h=this.half(bd,y);while(h<t){y++;h=this.half(bd,y)}const days=Math.round((h-t)/864e5);
  let age=h.getFullYear()-bd.getFullYear();if(h.getMonth()<bd.getMonth()||(h.getMonth()===bd.getMonth()&&h.getDate()<bd.getDate()))age--;
  const L=d=>d.toLocaleDateString(R().loc,{weekday:'long',year:'numeric',month:'long',day:'numeric'});
  const rows=[0,1,2,3,4].map(i=>this.half(bd,y+i));
  $('#hblist').innerHTML=`<div class="field"><label>Your next half birthdays</label></div><dl class="kv">${rows.map(d=>`<div><dt>${d.getFullYear()}</dt><dd>${d.toLocaleDateString(R().loc,{weekday:'short',month:'long',day:'numeric'})}</dd></div>`).join('')}</dl>`;
  $('#out').innerHTML=`<span class="label">${days===0?'Happy half birthday!':'Your next half birthday'}</span><div class="big"><em>${L(h)}</em></div>${kv([['Days to go',days===0?'Today':num(days,0)],['You’ll be',`${age} and a half`],['Birthday',bd.toLocaleDateString(R().loc,{month:'long',day:'numeric'})]])}${copyBtn}`;
  return `Half birthday: ${L(h)}`}},

{id:'military',cat:'Dates & time',name:'Military time converter',kw:'military time converter 24 hour clock army time convert military time to standard time am pm chart',desc:'Convert 24-hour military time to AM/PM and back.',
 render(){return `<div class="inputs"><div class="row">${field('mtm','Military time (e.g. 1830)','1830',{type:'text'})}${field('mts','Standard time (e.g. 6:30 PM)','6:30 PM',{type:'text'})}</div><p class="hint">Type in either box. The other one updates.</p></div><div class="result" id="out"></div>`},
 last:'m',
 parseM(s){s=s.replace(/[^0-9]/g,'');if(!/^\d{3,4}$/.test(s))return null;s=s.padStart(4,'0');const h=+s.slice(0,2),m=+s.slice(2);if(h>24||m>59||(h===24&&m))return null;return[h%24,m]},
 parseS(s){const x=s.trim().toLowerCase().match(/^(\d{1,2})(?::?(\d{2}))?\s*(a|p)\.?m?\.?$/);if(!x)return null;let h=+x[1],m=+(x[2]||0);if(h<1||h>12||m>59)return null;if(x[3]==='a')h=h%12;else h=h%12+12;return[h,m]},
 calc(){const ae=document.activeElement;if(ae&&ae.id==='mts')this.last='s';else if(ae&&ae.id==='mtm')this.last='m';const p=this.last==='m'?this.parseM($('#mtm').value):this.parseS($('#mts').value);
  if(!p){$('#out').innerHTML=`<span class="label">Converted time</span><p class="hint">${this.last==='m'?'Enter military time as 4 digits, like 0730 or 1945.':'Enter a time like 7:30 AM or 9 PM.'}</p>`;return''}
  const[h,m]=p,mm=String(m).padStart(2,'0'),milS=String(h).padStart(2,'0')+mm,std=`${h%12||12}:${mm} ${h<12?'AM':'PM'}`;
  if(this.last==='m')$('#mts').value=std;else $('#mtm').value=milS;
  $('#out').innerHTML=`<span class="label">${this.last==='m'?'Standard time':'Military time'}</span><div class="big"><em>${this.last==='m'?std:milS}</em></div>${kv([['Military',milS],['Standard',std],['24-hour clock',`${String(h).padStart(2,'0')}:${mm}`],['Written with hours',milS+' hours']])}${copyBtn}`;
  return `${milS} = ${std}`},
 after(){$('#mtm').addEventListener('input',()=>{this.last='m'},true);$('#mts').addEventListener('input',()=>{this.last='s'},true)}},

{id:'raise',cat:'Work & pay',name:'Pay raise',kw:'pay raise calculator salary increase calculator raise percentage new salary hourly raise percent increase',desc:'New pay after a raise, or the raise percentage.',
 state:{mode:'pct',per:'h'},
 render(){const s=this.state,c=R().cur,h=s.per==='h';return `<div class="inputs">${seg('rsm',[['pct','Raise %'],['amt','Raise amount'],['new','I know my new pay']],s.mode)}
  <div class="row">${field('rso',h?'Current hourly pay':'Current yearly salary',h?24:50000,{unit:c})}<div class="field"><label>Pay is</label>${seg('rsp',[['h','Hourly'],['y','Yearly']],s.per)}</div></div>
  <div class="row">${s.mode==='pct'?field('rsx','Raise',5,{unit:'%'}):s.mode==='amt'?field('rsx',h?'Raise per hour':'Raise per year',h?1.5:3000,{unit:c}):field('rsx',h?'New hourly pay':'New yearly salary',h?25.2:53000,{unit:c})}</div>
  <p class="hint">Hourly and yearly figures assume 40 hours a week, 52 weeks a year. Pay is before tax.</p></div><div class="result" id="out"></div>`},
 calc(){const s=this.state,o=v('rso'),x=v('rsx');if(!(o>0)||!isFinite(x)){$('#out').innerHTML='<span class="label">New pay</span><p class="hint">Enter your current pay and the raise.</p>';return''}
  const n=s.mode==='pct'?o*(1+x/100):s.mode==='amt'?o+x:x,pct=(n-o)/o*100,f=s.per==='h'?2080:1,yo=o*f,yn=n*f;
  $('#out').innerHTML=`<span class="label">${s.mode==='new'?'Your raise':'New pay'}</span><div class="big"><em>${s.mode==='new'?num(pct,2)+'%':money(n)}</em>${s.mode==='new'?'':s.per==='h'?' /hour':' /year'}</div>${kv([['Raise',`${num(pct,2)}% (${money(n-o)} ${s.per==='h'?'per hour':'per year'})`],['New hourly',money(yn/2080)],['New weekly',money(yn/52)],['New monthly',money(yn/12)],['New yearly',money(yn,0)],['Extra per year',money(yn-yo,0)],['Extra per month',money((yn-yo)/12)]])}${copyBtn}`;
  return `${money(o)} → ${money(n)} (${num(pct,2)}%)`},
 after(){bindSeg('rsm',m=>{this.state.mode=m;open('raise')});bindSeg('rsp',p=>{this.state.per=p;open('raise')})}},

{id:'water',cat:'Health',name:'Water intake',kw:'water intake calculator how much water should i drink a day hydration daily water ounces litres cups',desc:'How much water to drink a day.',
 state:{unit:null},
 render(){const s=this.state;if(!s.unit)s.unit=R().imperial?'lb':'kg';return `<div class="inputs"><div class="row">${field('ww','Body weight',s.unit==='lb'?160:73,{unit:s.unit})}<div class="field"><label>Units</label>${seg('wu',[['lb','lb'],['kg','kg']],s.unit)}</div></div>
  <div class="row">${field('wex','Exercise per day',30,{unit:'min'})}<div class="field"><label for="whot"><input type="checkbox" id="whot"> Hot or humid weather</label></div></div>
  <p class="hint">A general estimate for healthy adults. People with heart or kidney conditions should follow their doctor's advice.</p></div><div class="result" id="out"></div>`},
 calc(){const lb=this.state.unit==='lb'?v('ww'):v('ww')/0.45359237;if(!(lb>0)){$('#out').innerHTML='<span class="label">Water</span><p class="hint">Enter your weight.</p>';return''}
  const oz=lb*0.5+Math.max(0,v('wex')||0)/30*12+($('#whot').checked?16:0),L=oz/33.814;
  $('#out').innerHTML=`<span class="label">Drink about</span><div class="big"><em>${R().imperial?num(oz,0)+' oz':num(L,1)+' L'}</em> a day</div>${kv([['Ounces',num(oz,0)+' oz'],['Litres',num(L,1)+' L'],['Cups (8 oz)',num(oz/8,1)],['500 ml bottles',num(L*2,1)]])}${copyBtn}`;
  return `${num(oz,0)} oz (${num(L,1)} L) a day`},
 after(){bindSeg('wu',x=>{this.state.unit=x;open('water')});$('#whot').addEventListener('change',update)}},

{id:'mulch',cat:'Home',name:'Mulch calculator',kw:'mulch calculator how much mulch do i need cubic yards bags topsoil gravel calculator landscaping',desc:'Cubic yards and bags of mulch, soil or gravel.',
 state:{shape:'rect',unit:null},
 render(){const s=this.state;if(!s.unit)s.unit=R().imperial?'ft':'m';const ft=s.unit==='ft',L=ft?'ft':'m';
  return `<div class="inputs"><div class="row">${seg('mls',[['rect','Rectangle'],['circle','Circle']],s.shape)}${seg('mlu',[['ft','Feet'],['m','Metres']],s.unit)}</div>
  <div class="row">${s.shape==='rect'?field('mll','Length',ft?20:6,{unit:L})+field('mlw','Width',ft?10:3,{unit:L}):field('mld','Diameter',ft?8:2.5,{unit:L})}${field('mlh','Depth',ft?3:7.5,{unit:ft?'in':'cm'})}</div>
  <p class="hint">2–3 inches (5–7.5 cm) is typical for flower beds. Add 5–10% for settling.</p></div><div class="result" id="out"></div>`},
 calc(){const s=this.state,ft=s.unit==='ft';const a=s.shape==='rect'?v('mll')*v('mlw'):Math.PI*Math.pow(v('mld')/2,2),d=v('mlh');
  if(!(a>0&&d>0)){$('#out').innerHTML='<span class="label">Mulch</span><p class="hint">Enter the bed size and depth.</p>';return''}
  const cf=ft?a*d/12:a*d/100*35.3147,cy=cf/27,m3=cf/35.3147;
  $('#out').innerHTML=`<span class="label">You need</span><div class="big"><em>${ft?num(cy,2)+' yd³':num(m3,2)+' m³'}</em></div>${kv([['Cubic yards',num(cy,2)],['Cubic feet',num(cf,1)],['Cubic metres',num(m3,2)],['2 cu ft bags',Math.ceil(cf/2)],['3 cu ft bags',Math.ceil(cf/3)],['Area',`${num(a,1)} ${ft?'sq ft':'m²'}`]])}${copyBtn}`;
  return `${num(cy,2)} cubic yards (${Math.ceil(cf/2)} bags of 2 cu ft)`},
 after(){bindSeg('mls',x=>{this.state.shape=x;open('mulch')});bindSeg('mlu',x=>{this.state.unit=x;open('mulch')})}},

{id:'workdays',cat:'Dates & time',name:'Working days in a year',kw:'how many working days in a year work days business days in a year 2026 2027 working days calculator federal holidays',desc:'Work days in any year and month, minus holidays.',
 render(){const y=new Date().getFullYear();return `<div class="inputs"><div class="row"><div class="field"><label for="wdy">Year</label><select id="wdy">${[y-1,y,y+1,y+2].map(x=>`<option${x===y?' selected':''}>${x}</option>`).join('')}</select></div>${field('wdp','Vacation / PTO days',0,{unit:'days',step:1})}</div>
  <div class="field"><label for="wdh"><input type="checkbox" id="wdh" checked> Remove US federal holidays</label></div><div id="wdtab" class="tc-wrap"></div></div><div class="result" id="out"></div>`},
 hols(y){const n=(m,dow,k)=>{const d=new Date(y,m,1);return new Date(y,m,1+((dow-d.getDay()+7)%7)+7*(k-1))},l=(m,dow)=>{const d=new Date(y,m+1,0);d.setDate(d.getDate()-((d.getDay()-dow+7)%7));return d},o=d=>{const g=d.getDay();if(g===6)d.setDate(d.getDate()-1);else if(g===0)d.setDate(d.getDate()+1);return d};
  return [o(new Date(y,0,1)),n(0,1,3),n(1,1,3),l(4,1),o(new Date(y,5,19)),o(new Date(y,6,4)),n(8,1,1),n(9,1,2),o(new Date(y,10,11)),n(10,4,4),o(new Date(y,11,25)),o(new Date(y+1,0,1))].filter(d=>d.getFullYear()===y&&d.getDay()%6)},
 calc(){const y=+$('#wdy').value,useH=$('#wdh').checked,pto=Math.max(0,Math.round(v('wdp')||0)),H=useH?this.hols(y):[];const rows=[];let tw=0,th=0;
  for(let m=0;m<12;m++){let w=0;const dim=new Date(y,m+1,0).getDate();for(let d=1;d<=dim;d++){const g=new Date(y,m,d).getDay();if(g%6)w++}const h=H.filter(d=>d.getMonth()===m).length;tw+=w;th+=h;rows.push([new Date(y,m,1).toLocaleDateString(R().loc,{month:'long'}),w,h,w-h])}
  const work=tw-th-pto;
  $('#wdtab').innerHTML=`<table><thead><tr><th>Month</th><th style="text-align:right">Weekdays</th><th style="text-align:right">Holidays</th><th style="text-align:right">Working days</th></tr></thead><tbody>${rows.map(r=>`<tr><td>${r[0]}</td><td class="num">${r[1]}</td><td class="num">${r[2]}</td><td class="num">${r[3]}</td></tr>`).join('')}</tbody></table>`;
  $('#out').innerHTML=`<span class="label">Working days in ${y}</span><div class="big"><em>${work}</em> days</div>${kv([['Weekdays (Mon–Fri)',tw],['Federal holidays on weekdays',useH?th:'Not removed'],['Vacation / PTO',pto],['Work hours (8 h/day)',num(work*8,0)],['Weekend days',(new Date(y,1,29).getDate()===29?366:365)-tw]])}${copyBtn}`;
  return `${work} working days in ${y}`},
 after(){$('#wdh').addEventListener('change',update)}},
{id:'turkey',cat:'Home',name:'Turkey calculator',kw:'turkey calculator thanksgiving turkey cooking time roasting time thawing time how big turkey per person christmas turkey',desc:'Turkey size, thawing and roasting time.',
 state:{mode:'guests',stuff:'no',thaw:'fridge'},
 R:[[8,1.5,3.25,null,null],[12,2.75,3,3,3.5],[14,3,3.75,3.5,4],[18,3.75,4.25,4,4.25],[20,4.25,4.5,4.25,4.75],[99,4.5,5,4.75,5.25]],
 tg(){const n=new Date(),y=n.getMonth()===11&&n.getDate()>1?n.getFullYear()+1:n.getFullYear();let d=new Date(y,10,1);d.setDate(1+((4-d.getDay()+7)%7)+21);if(d<n){d=new Date(y+1,10,1);d.setDate(1+((4-d.getDay()+7)%7)+21)}const p=x=>String(x).padStart(2,'0');return `${d.getFullYear()}-${p(d.getMonth()+1)}-${p(d.getDate())}T17:00`},
 render(){const s=this.state;return `<div class="inputs">${seg('tkm',[['guests','I know how many guests'],['weight','I have a turkey']],s.mode)}
  <div class="row">${s.mode==='guests'?field('tkg','Guests',12,{unit:'people',step:1})+`<div class="field"><label for="tkl"><input type="checkbox" id="tkl" checked> I want leftovers</label></div>`:field('tkw','Turkey weight',16,{unit:'lb'})}</div>
  <div class="row"><div class="field"><label>Stuffing</label>${seg('tks',[['no','Unstuffed'],['yes','Stuffed']],s.stuff)}</div><div class="field"><label>Thawing</label>${seg('tkt',[['fridge','Fridge'],['water','Cold water'],['none','Fresh / thawed']],s.thaw)}</div></div>
  ${field('tkd','Dinner time',this.tg(),{type:'datetime-local'})}
  <div id="tkplan"></div><p class="hint">Times are for a 325°F (163°C) oven, from the USDA chart. Always check the turkey reaches 165°F (74°C).</p></div><div class="result" id="out"></div>`},
 calc(){const s=this.state;let w;if(s.mode==='guests'){const g=Math.round(v('tkg'));if(!(g>0)){$('#out').innerHTML='<span class="label">Turkey</span><p class="hint">Enter the number of guests.</p>';$('#tkplan').innerHTML='';return''}w=g*($('#tkl').checked?1.5:1)}else w=v('tkw');
  if(!(w>=4&&w<=40)){$('#out').innerHTML='<span class="label">Turkey</span><p class="hint">Enter a turkey between 4 and 40 lb.</p>';$('#tkplan').innerHTML='';return''}
  const row=this.R.find(r=>w<r[0])||this.R[this.R.length-1],st=s.stuff==='yes'&&row[3]!=null,lo=st?row[3]:row[1],hi=st?row[4]:row[2];
  const fh=h=>{const m=Math.round(h*60);return `${Math.floor(m/60)} h ${String(m%60).padStart(2,'0')} min`};
  const thawLo=s.thaw==='fridge'?Math.max(1,Math.round(w/5)):w*0.5,thawHi=s.thaw==='fridge'?Math.ceil(w/4):w*0.5;
  const d=$('#tkd').value?new Date($('#tkd').value):null,rows=[];let inOven=null;
  if(d&&!isNaN(d)){const out=new Date(d-30*6e4);inOven=new Date(out-hi*36e5);const F=x=>x.toLocaleString(R().loc,{weekday:'short',month:'short',day:'numeric',hour:'numeric',minute:'2-digit'});
   if(s.thaw==='fridge'){const t=new Date(inOven);t.setDate(t.getDate()-thawHi);t.setHours(9,0,0,0);rows.push(['Move turkey to the fridge',t.toLocaleDateString(R().loc,{weekday:'long',month:'short',day:'numeric'})+' (morning)'])}
   if(s.thaw==='water'){const t=new Date(inOven-(thawHi*36e5+36e5));rows.push(['Start cold-water thaw',F(t)])}
   rows.push(['Heat oven to 325°F',F(new Date(inOven-20*6e4))],['Turkey in the oven',F(inOven)],['Start checking temperature',F(new Date(inOven.getTime()+(lo-0.5)*36e5))],['Out of the oven to rest',F(out)],['Dinner',F(d)])}
  $('#tkplan').innerHTML=rows.length?`<div class="field"><label>Your timeline</label></div>${kv(rows)}`:'';
  $('#out').innerHTML=`<span class="label">${s.mode==='guests'?'Buy a turkey of about':'Roasting time'}</span><div class="big"><em>${s.mode==='guests'?num(Math.ceil(w),0)+' lb':fh(lo)+' – '+fh(hi)}</em></div>${kv([['Turkey weight',`${num(w,1)} lb (${num(w*0.4536,1)} kg)`],['Roasting at 325°F',`${fh(lo)} – ${fh(hi)}${s.stuff==='yes'&&!st?' (don’t stuff a turkey this small)':''}`],['Thawing',s.thaw==='fridge'?`${thawLo===thawHi?thawHi:thawLo+'–'+thawHi} days in the fridge`:s.thaw==='water'?`${num(thawHi,1)} hours in cold water`:'Not needed'],['Done when',`165°F (74°C) in breast, thigh and wing`],['Rest before carving','20–30 minutes']])}${copyBtn}`;
  return `${num(w,1)} lb turkey: roast ${fh(lo)}–${fh(hi)} at 325°F`+(inOven?`, in the oven ${inOven.toLocaleTimeString(R().loc,{hour:'numeric',minute:'2-digit'})}`:'')},
 after(){bindSeg('tkm',x=>{this.state.mode=x;open('turkey')});bindSeg('tks',x=>{this.state.stuff=x;update()});bindSeg('tkt',x=>{this.state.thaw=x;update()});const l=$('#tkl');if(l)l.addEventListener('change',update)}},
{id:'soh',cat:'Money',name:'Save Our Homes (Florida)',kw:'save our homes calculator florida homestead tax savings assessed value cap portability amendment 3 property tax florida',desc:'Florida homestead assessment cap and tax savings.',
 CAPS:{1995:2.7,1996:2.5,1997:3,1998:1.7,1999:1.6,2000:2.7,2001:3,2002:1.6,2003:2.4,2004:1.9,2005:3,2006:3,2007:2.5,2008:3,2009:0.1,2010:2.7,2011:1.5,2012:3,2013:1.7,2014:1.5,2015:0.8,2016:0.7,2017:2.1,2018:2.1,2019:1.9,2020:2.3,2021:1.4,2022:3,2023:3,2024:3,2025:2.9,2026:2.7},
 NOW:2026,
 usd(n){return isFinite(n)?new Intl.NumberFormat('en-US',{style:'currency',currency:'USD',maximumFractionDigits:0}).format(n):'—'},
 render(){const ys=[];for(let y=this.NOW;y>=1994;y--)ys.push(y);return `<div class="inputs"><div class="row"><div class="field"><label for="shy">Homestead since (year)</label><select id="shy">${ys.map(y=>`<option${y===2015?' selected':''}>${y}</option>`).join('')}</select></div>${field('shb','Market value that year',250000,{unit:'USD'})}</div>
  <div class="row">${field('shn','Market value now (2026)',450000,{unit:'USD'})}${field('sha','2026 assessed value (optional)','',{unit:'USD'})}</div><p class="hint">If you have your TRIM notice, enter the assessed value from it for an exact result. Otherwise it's estimated from the yearly caps.</p>
  <div class="row">${field('shs','School millage',6,{unit:'mills',step:0.01})}${field('sho','Other millage',11.5,{unit:'mills',step:0.01})}</div>
  <p class="hint">Millage rates are on your TRIM notice or tax bill. 1 mill = $1 per $1,000 of taxable value. Defaults are typical Florida rates.</p><div id="shtab" class="tc-wrap"></div></div><div class="result" id="out"></div>`},
 tax(a,y,s,o){const sec=Math.min(Math.max(0,a-50000),y>=2026?26411:y===2025?25722:25000);return Math.max(0,a-25000)*s/1000+Math.max(0,a-25000-sec)*o/1000},
 calc(){const y0=+$('#shy').value,b=v('shb'),n=v('shn'),s=Math.max(0,v('shs')||0),o=Math.max(0,v('sho')||0);
  if(!(b>0&&n>0)){$('#out').innerHTML='<span class="label">Save Our Homes</span><p class="hint">Enter both market values.</p>';$('#shtab').innerHTML='';return''}
  const k=this.NOW-y0,g=k>0?Math.pow(n/b,1/k):1;let a=b,cum=0;const rows=[];
  for(let y=y0;y<=this.NOW;y++){const j=b*Math.pow(g,y-y0);if(y>y0)a=Math.min(j,a*(1+(this.CAPS[y]||3)/100));const sv=y>=1995?this.tax(j,y,s,o)-this.tax(a,y,s,o):0;cum+=sv;rows.push([y,j,a,sv])}
  if(k===0)a=n;const given=v('sha');if(given>0)a=given;const J=n,A=Math.min(a,n),tw=this.tax(A,this.NOW,s,o),two=this.tax(J,this.NOW,s,o),diff=Math.max(0,Math.round(J-A)),a3=Math.max(0,A-150000)*o/1000+Math.max(0,A-25000)*s/1000;
  $('#shtab').innerHTML=`<table><thead><tr><th>Year</th><th style="text-align:right">Market</th><th style="text-align:right">Assessed</th><th style="text-align:right">Saved</th></tr></thead><tbody>${rows.slice().reverse().slice(0,12).map(r=>`<tr><td>${r[0]}</td><td class="num">${this.usd(r[1])}</td><td class="num">${this.usd(r[2])}</td><td class="num">${this.usd(r[3])}</td></tr>`).join('')}</tbody></table>`;
  $('#out').innerHTML=`<span class="label">You save in 2026</span><div class="big"><em>${this.usd(Math.max(0,Math.round(two-tw)))}</em></div>${kv([['2026 assessed value (capped)',this.usd(A)],['Value not taxed (SOH benefit)',this.usd(diff)],['2026 tax with the cap',this.usd(tw)],['Tax without the cap',this.usd(two)],[`Total saved since ${y0}`,this.usd(Math.max(0,Math.round(cum)))],['Portable to a new homestead',this.usd(Math.min(diff,500000))],['2027 preview with Amendment 3',`about ${this.usd(a3)} a year*`]])}<p class="hint">*Same assessed value under the new $150,000 non-school exemption. Estimate only; excludes non-ad valorem fees.</p>${k===0?'<p class="hint">The cap starts on January 1 after your first homestead year, so there is no saving yet.</p>':''}${copyBtn}`;
  return `Save Our Homes saves ${this.usd(two-tw)} in 2026 (assessed ${this.usd(A)} vs market ${this.usd(J)})`}},
{id:'shoe',cat:'Converters',name:'Shoe size converter',kw:'shoe size converter shoe size conversion chart us uk eu european mens womens kids eu to us shoe size foot length cm inches',desc:'Convert shoe sizes between US, UK and EU.',
 state:{who:'m',from:'us'},
 R2(x){return Math.round(x*2)/2},
 inchFrom(sys,who,x){if(sys==='in')return x;if(sys==='cm')return x/2.54;if(sys==='eu')return ((x-2)/1.27)/3;if(who==='k'){if(sys==='us')return (x+9.67)/3;if(sys==='uk')return (x+10)/3}if(sys==='uk')return (x+23)/3;return (x+(who==='w'?21:22))/3},
 render(){const s=this.state,def={m:{us:10,uk:9,eu:42.5,cm:27.1,in:10.67},w:{us:8,uk:6,eu:39,cm:24.6,in:9.67},k:{us:11,uk:10.5,eu:29,cm:17.4,in:6.89}}[s.who][s.from];
  const lbl={us:s.who==='k'?'US kids size':'US size',uk:'UK size',eu:'EU size',cm:'Foot length',in:'Foot length'}[s.from];
  return `<div class="inputs"><div class="row">${seg('shw',[['m','Men'],['w','Women'],['k','Kids']],s.who)}</div>
  <div class="row">${seg('shf',[['us','US'],['uk','UK'],['eu','EU'],['cm','cm'],['in','inches']],s.from)}</div>
  <div class="row">${field('shx',lbl,def,{unit:s.from==='cm'?'cm':s.from==='in'?'in':'',step:s.from==='cm'||s.from==='in'?0.1:0.5})}</div>
  <p class="hint">${s.who==='k'?'Kids’ US sizes run 0–13.5, then youth sizes start again at 1Y. Enter a youth size as 13 + the youth number (1Y = 14).':'Sizes vary by brand by about half a size. Check the brand’s own chart before you buy.'}</p></div><div class="result" id="out"></div>`},
 calc(){const s=this.state,x=v('shx');if(!(x>0)){$('#out').innerHTML='<span class="label">Your size</span><p class="hint">Enter a size or foot length.</p>';return''}
  const i=this.inchFrom(s.from,s.who,x),cm=i*2.54,eu=1.27*(3*i)+2,r=n=>this.R2(n).toString();
  if(!(cm>8&&cm<36)){$('#out').innerHTML='<span class="label">Your size</span><p class="hint">That size is outside the usual range. Check the number and the system.</p>';return''}
  let rows,main;
  if(s.who==='k'){const us=3*i-9.67,uk=3*i-10,f=n=>n<13.75?r(n):r(n-13)+'Y';main=`US kids ${f(us)}`;rows=[['US kids',f(us)],['UK kids',f(uk)],['EU',r(eu)],['Foot length',`${num(i,2)} in · ${num(cm,1)} cm`]]}
  else{const m=3*i-22,w=3*i-21,uk=3*i-23;main=s.who==='m'?`US men's ${r(m)}`:`US women's ${r(w)}`;rows=[['US men',r(m)],['US women',r(w)],['UK',r(uk)],['EU',r(eu)],['Foot length',`${num(i,2)} in · ${num(cm,1)} cm`]]}
  $('#out').innerHTML=`<span class="label">Your size</span><div class="big"><em>${main}</em></div>${kv(rows)}${copyBtn}`;
  return rows.map(r=>r[0]+' '+r[1]).join(', ')},
 after(){bindSeg('shw',x=>{this.state.who=x;open('shoe')});bindSeg('shf',x=>{this.state.from=x;open('shoe')})}},
{id:'discount',cat:'Money',name:'Discount calculator',kw:'discount calculator percent off calculator sale price calculator % off price after discount extra percent off double discount savings',desc:'Sale price and savings after a percent off.',
 state:{},
 render(){return `<div class="inputs"><div class="row">${field('dcp','Original price',80,{unit:R().cur})}${field('dcd','Discount',25,{unit:'% off'})}</div>
  <div class="row">${field('dce','Extra discount (optional)',0,{unit:'% off'})}${field('dct','Sales tax (optional)',0,{unit:'%'})}</div>
  <p class="hint">“Extra 10% off” is taken from the already-reduced price, so 25% + 10% is 32.5% off, not 35%.</p></div><div class="result" id="out"></div>`},
 calc(){const p=v('dcp'),d=v('dcd')||0,e=v('dce')||0,t=v('dct')||0;
  if(!(p>0)||d<0||d>100||e<0||e>100){$('#out').innerHTML='<span class="label">Sale price</span><p class="hint">Enter a price and a discount between 0 and 100%.</p>';return''}
  const s1=p*(1-d/100),s2=s1*(1-e/100),tax=s2*t/100,tot=s2+tax,save=p-s2,eff=save/p*100;
  const rows=[['You save',money(save)],['Effective discount',num(eff,2)+'%']];if(e>0)rows.push(['Price after first discount',money(s1)]);if(t>0)rows.push(['Sales tax',money(tax)],['Total to pay',money(tot)]);
  $('#out').innerHTML=`<span class="label">Sale price</span><div class="big"><em>${money(s2)}</em></div><p class="answer">${money(p)} with ${num(d,2)}% off${e>0?` and an extra ${num(e,2)}% off`:''} is ${money(s2)}. You save ${money(save)}.</p>${kv(rows)}${copyBtn}`;
  return `Sale price ${money(s2)}, you save ${money(save)}`}},

{id:'tdee',cat:'Health',name:'TDEE calculator',kw:'tdee calculator total daily energy expenditure maintenance calories calculator how many calories do i burn a day calories to lose weight cut bulk',desc:'Maintenance calories from your activity level.',
 state:{sex:'m',unit:null,act:'1.55'},
 render(){const s=this.state;if(!s.unit)s.unit=R().imperial?'imp':'met';const imp=s.unit==='imp';
  return `<div class="inputs"><div class="row">${seg('tds',[['m','Male'],['f','Female']],s.sex)}${seg('tdu',[['imp','US units'],['met','Metric']],s.unit)}</div>
  <div class="row">${field('tda','Age',30,{unit:'yrs'})}${imp?field('tdft','Height (feet)',5,{unit:'ft'})+field('tdin','Height (inches)',10,{unit:'in'}):field('tdcm','Height',178,{unit:'cm'})}${field('tdw','Weight',imp?180:82,{unit:imp?'lb':'kg'})}</div>
  <div class="row"><div class="field"><label>Activity</label>${seg('tdx',[['1.2','Desk job'],['1.375','Light'],['1.55','Moderate'],['1.725','Active'],['1.9','Very active']],s.act)}</div></div>
  <p class="hint">Light = exercise 1–3 days a week, moderate = 3–5 days, active = 6–7 days, very active = hard daily training or a physical job. An estimate for adults, not medical advice.</p></div><div class="result" id="out"></div>`},
 calc(){const s=this.state,imp=s.unit==='imp',a=v('tda');const h=imp?((v('tdft')||0)*12+(v('tdin')||0))*2.54:v('tdcm'),w=imp?v('tdw')*0.45359237:v('tdw');
  if(!(a>0&&h>0&&w>0)){$('#out').innerHTML='<span class="label">TDEE</span><p class="hint">Enter your age, height and weight.</p>';return''}
  const bmr=10*w+6.25*h-5*a+(s.sex==='m'?5:-161),f=parseFloat(s.act),t=bmr*f,c=n=>num(Math.round(n/10)*10,0)+' cal';
  $('#out').innerHTML=`<span class="label">Maintenance calories (TDEE)</span><div class="big"><em>${num(Math.round(t/10)*10,0)}</em> calories/day</div><p class="answer">Eat about ${c(t)} a day to stay at your current weight.</p>${kv([['BMR (at rest)',c(bmr)],['Mild loss (about 0.5 lb/week)',c(t-250)],['Weight loss (about 1 lb/week)',c(t-500)],['Lean bulk (about 0.5 lb/week)',c(t+250)],['Weekly TDEE',c(t*7)]])}${copyBtn}`;
  return `TDEE ${c(t)} per day`},
 after(){bindSeg('tds',x=>{this.state.sex=x;update()});bindSeg('tdu',x=>{this.state.unit=x;open('tdee')});bindSeg('tdx',x=>{this.state.act=x;update()})}},

{id:'idealweight',cat:'Health',name:'Ideal weight calculator',kw:'ideal weight calculator ideal body weight ibw how much should i weigh for my height and age healthy weight range devine robinson miller hamwi formula',desc:'Ideal body weight for your height, four formulas.',
 state:{sex:'m',unit:null},
 render(){const s=this.state;if(!s.unit)s.unit=R().imperial?'imp':'met';const imp=s.unit==='imp';
  return `<div class="inputs"><div class="row">${seg('iws',[['m','Male'],['f','Female']],s.sex)}${seg('iwu',[['imp','US units'],['met','Metric']],s.unit)}</div>
  <div class="row">${imp?field('iwft','Height (feet)',5,{unit:'ft'})+field('iwin','Height (inches)',10,{unit:'in'}):field('iwcm','Height',178,{unit:'cm'})}</div>
  <p class="hint">The formulas were built for adults about 5 ft (152 cm) and taller. They don't account for muscle, frame size or age.</p></div><div class="result" id="out"></div>`},
 calc(){const s=this.state,imp=s.unit==='imp';const cm=imp?((v('iwft')||0)*12+(v('iwin')||0))*2.54:v('iwcm');
  if(!(cm>120&&cm<230)){$('#out').innerHTML='<span class="label">Ideal weight</span><p class="hint">Enter a height between 4 ft and 7 ft 6 in (120–230 cm).</p>';return''}
  const over=Math.max(0,cm/2.54-60),m=s.sex==='m';
  const F=[['Robinson (1983)',m?52+1.9*over:49+1.7*over],['Miller (1983)',m?56.2+1.41*over:53.1+1.36*over],['Devine (1974)',m?50+2.3*over:45.5+2.3*over],['Hamwi (1964)',m?48+2.7*over:45.5+2.2*over]];
  const hm=cm/100,lo=18.5*hm*hm,hi=24.9*hm*hm,W=kg=>imp?num(kg/0.45359237,0)+' lb':num(kg,1)+' kg';
  const vals=F.map(x=>x[1]),mn=Math.min(...vals),mx=Math.max(...vals);
  $('#out').innerHTML=`<span class="label">Ideal weight</span><div class="big"><em>${W(mn)} – ${W(mx)}</em></div><p class="answer">Healthy BMI range for your height: ${W(lo)} to ${W(hi)}.</p>${kv(F.map(([n,k])=>[n,W(k)]).concat([['Healthy BMI 18.5–24.9',`${W(lo)} – ${W(hi)}`]]))}${copyBtn}`;
  return `Ideal weight ${W(mn)}–${W(mx)}; healthy BMI range ${W(lo)}–${W(hi)}`},
 after(){bindSeg('iws',x=>{this.state.sex=x;update()});bindSeg('iwu',x=>{this.state.unit=x;open('idealweight')})}},

{id:'roman',cat:'Converters',name:'Roman numeral converter',kw:'roman numeral converter roman numerals to numbers numbers to roman numerals translator date in roman numerals mmxxvi year chart',desc:'Numbers to Roman numerals and back.',
 state:{},
 V:[[1000,'M'],[900,'CM'],[500,'D'],[400,'CD'],[100,'C'],[90,'XC'],[50,'L'],[40,'XL'],[10,'X'],[9,'IX'],[5,'V'],[4,'IV'],[1,'I']],
 toR(n){let o='';for(const[a,r]of this.V)while(n>=a){o+=r;n-=a}return o},
 fromR(s){if(!/^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$/.test(s)||!s)return NaN;const m={I:1,V:5,X:10,L:50,C:100,D:500,M:1000};let t=0;for(let i=0;i<s.length;i++){const a=m[s[i]],b=m[s[i+1]]||0;t+=a<b?-a:a}return t},
 render(){return `<div class="inputs"><div class="row">${field('rmx','Number or Roman numeral','2026',{type:'text'})}</div>
  <p class="hint">Type a number from 1 to 3,999 (like 2026) or a Roman numeral (like MMXXVI). Dates work too: 11/08/2026.</p></div><div class="result" id="out"></div>`},
 calc(){const raw=(document.getElementById('rmx').value||'').trim();let out,label,steps;
  const dm=raw.match(/^(\d{1,2})[\/.\-](\d{1,2})[\/.\-](\d{2,4})$/);
  if(dm){const p=[+dm[1],+dm[2],+dm[3]];if(p.some(x=>x<1||x>3999)){out=null}else{const r=p.map(x=>this.toR(x));label='Date in Roman numerals';out=r.join('.');steps=[[raw,r.join(' · ')]]}}
  else if(/^\d+$/.test(raw.replace(/,/g,''))){const n=+raw.replace(/,/g,'');if(n>=1&&n<=3999){out=this.toR(n);label=`${num(n,0)} in Roman numerals`;steps=[];[1000,100,10,1].forEach(pl=>{const part=Math.floor(n/pl)%10*pl;if(part)steps.push([num(part,0),this.toR(part)])})}}
  else{const u=raw.toUpperCase().replace(/\s/g,'');const n=this.fromR(u);if(n){out=num(n,0);label=`${u} as a number`;steps=[...u.matchAll(/CM|CD|XC|XL|IX|IV|M|D|C|L|X|V|I/g)].map(x=>[x[0],num(this.fromR(x[0])||{M:1000,D:500,C:100,L:50,X:10,V:5,I:1}[x[0]],0)])}}
  if(!out){$('#out').innerHTML='<span class="label">Result</span><p class="hint">Enter a whole number from 1 to 3,999 or a valid Roman numeral such as XLII.</p>';return''}
  $('#out').innerHTML=`<span class="label">${label}</span><div class="big"><em>${out}</em></div>${kv(steps)}${copyBtn}`;
  return `${raw} = ${out}`}},

{id:'simpleint',cat:'Money',name:'Simple interest calculator',kw:'simple interest calculator i=prt formula interest per year per month principal rate time simple vs compound interest',desc:'Interest and total with I = P × r × t.',
 state:{per:'y'},
 render(){const s=this.state;return `<div class="inputs"><div class="row">${field('sip','Principal',10000,{unit:R().cur})}${field('sir','Interest rate',5,{unit:'% / year'})}</div>
  <div class="row">${field('sit','Time',3,{unit:s.per==='y'?'years':s.per==='m'?'months':'days'})}${seg('siper',[['y','Years'],['m','Months'],['d','Days']],s.per)}</div></div><div class="result" id="out"></div>`},
 calc(){const s=this.state,P=v('sip'),r=v('sir')/100,t0=v('sit');if(!(P>0&&r>=0&&t0>0)){$('#out').innerHTML='<span class="label">Interest</span><p class="hint">Enter the principal, rate and time.</p>';return''}
  const t=s.per==='y'?t0:s.per==='m'?t0/12:t0/365,I=P*r*t,C=P*Math.pow(1+r,t)-P;
  $('#out').innerHTML=`<span class="label">Simple interest</span><div class="big"><em>${money(I)}</em></div><p class="answer">${money(P)} at ${num(r*100,3)}% for ${num(t0,2)} ${s.per==='y'?'years':s.per==='m'?'months':'days'} earns ${money(I)}, for a total of ${money(P+I)}.</p>${kv([['Total (principal + interest)',money(P+I)],['Interest per year',money(P*r)],['Interest per month',money(P*r/12)],['Interest per day (365-day year)',money(P*r/365)],['Compound interest instead (yearly)',money(C)]])}${copyBtn}`;
  return `Interest ${money(I)}, total ${money(P+I)}`},
 after(){bindSeg('siper',x=>{this.state.per=x;open('simpleint')})}},

{id:'tile',cat:'Home',name:'Tile calculator',kw:'tile calculator how many tiles do i need floor tile calculator wall tile boxes square feet backsplash bathroom 12x24 12x12 waste',desc:'Number of tiles and boxes for a floor or wall.',
 state:{unit:null},
 render(){const s=this.state;if(!s.unit)s.unit=R().imperial?'ft':'m';const ft=s.unit==='ft';
  return `<div class="inputs"><div class="row">${seg('tlu',[['ft','Feet / inches'],['m','Metres / cm']],s.unit)}</div>
  <div class="row">${field('tll','Area length',ft?12:3.6,{unit:ft?'ft':'m'})}${field('tlw','Area width',ft?10:3,{unit:ft?'ft':'m'})}</div>
  <div class="row">${field('ttl','Tile length',ft?24:60,{unit:ft?'in':'cm'})}${field('ttw','Tile width',ft?12:30,{unit:ft?'in':'cm'})}${field('tlg','Grout gap',ft?0.125:3,{unit:ft?'in':'mm'})}</div>
  <div class="row">${field('tlx','Waste allowance',10,{unit:'%'})}${field('tlb','Tiles per box (optional)',8,{})}</div>
  <p class="hint">Use 10% extra for a straight layout and 15% for diagonal or herringbone. For an L-shaped room, split it into rectangles and add them up.</p></div><div class="result" id="out"></div>`},
 calc(){const ft=this.state.unit==='ft',A=v('tll')*v('tlw'),tl=v('ttl'),tw=v('ttw'),g=v('tlg')||0,w=v('tlx')||0,b=v('tlb');
  if(!(A>0&&tl>0&&tw>0)){$('#out').innerHTML='<span class="label">Tiles</span><p class="hint">Enter the area and tile size.</p>';return''}
  const ta=ft?(tl+g)*(tw+g)/144:(tl+g/10)*(tw+g/10)/10000,base=A/ta,need=Math.ceil(base*(1+w/100)),bx=b>0?Math.ceil(need/b):null;
  const rows=[['Area',`${num(A,2)} ${ft?'sq ft':'m²'}`],['Tiles without waste',num(Math.ceil(base),0)],['Waste allowance',`${num(w,0)}% (+${num(need-Math.ceil(base),0)} tiles)`]];if(bx)rows.push(['Boxes',`${bx} boxes of ${b} (${bx*b} tiles)`]);
  $('#out').innerHTML=`<span class="label">Tiles needed</span><div class="big"><em>${num(need,0)}</em> tiles</div>${kv(rows)}${copyBtn}`;
  return `${need} tiles${bx?` (${bx} boxes)`:''} for ${num(A,2)} ${ft?'sq ft':'m²'}`},
 after(){bindSeg('tlu',x=>{this.state.unit=x;open('tile')})}},

{id:'longdiv',cat:'Math',name:'Long division calculator',kw:'long division calculator with steps remainder quotient divide show work long division with decimals step by step',desc:'Quotient and remainder with every step shown.',
 state:{},
 render(){return `<div class="inputs"><div class="row">${field('ldn','Dividend',1764,{})}${field('ldd','Divisor',13,{})}</div>
  <p class="hint">Whole numbers show every long-division step. Decimals give the answer to 10 places.</p></div><div class="result" id="out"></div><div id="ldsteps" class="tc-wrap"></div>`},
 calc(){const n=v('ldn'),d=v('ldd'),st=$('#ldsteps');st.innerHTML='';
  if(!isFinite(n)||!isFinite(d)||d===0){$('#out').innerHTML=`<span class="label">Answer</span><p class="hint">${d===0?'You can’t divide by zero.':'Enter a dividend and a divisor.'}</p>`;return''}
  const q=n/d,int=Number.isInteger(n)&&Number.isInteger(d)&&n>=0&&d>0&&n<1e15;let rows=[['Decimal answer',num(q,10)]];
  if(int){const Q=Math.floor(n/d),Rm=n%d;rows.unshift(['Quotient',num(Q,0)],['Remainder',num(Rm,0)]);rows.push(['Mixed number',Rm?`${Q} ${Rm}/${d}`:String(Q)]);
   const ds=String(n);let cur=0,tr=[];for(const ch of ds){cur=cur*10+ +ch;const k=Math.floor(cur/d);if(k>0||tr.length){tr.push(`<tr><td class="num">${ch}</td><td class="num">${cur}</td><td class="num">${cur} ÷ ${d} = ${k}</td><td class="num">${k} × ${d} = ${k*d}</td><td class="num">${cur} − ${k*d} = ${cur-k*d}</td></tr>`)}cur-=k*d}
   if(tr.length&&tr.length<=20)st.innerHTML=`<table><thead><tr><th>Bring down</th><th>Number</th><th>Divide</th><th>Multiply</th><th>Subtract</th></tr></thead><tbody>${tr.join('')}</tbody></table>`}
  const ans=int?`${num(Math.floor(n/d),0)} R ${n%d}`:num(q,10);
  $('#out').innerHTML=`<span class="label">${num(n,10)} ÷ ${num(d,10)}</span><div class="big"><em>${ans}</em></div>${kv(rows)}${copyBtn}`;
  return `${n} ÷ ${d} = ${ans}`}},

{id:'zscore',cat:'Math',name:'Z-score calculator',kw:'z score calculator z-score to percentile probability normal distribution standard score p value from z table raw score mean standard deviation',desc:'Z-score, percentile and probability from a raw score.',
 state:{},
 cdf(z){const t=1/(1+0.2316419*Math.abs(z)),d=0.3989422804014327*Math.exp(-z*z/2),p=d*t*(0.319381530+t*(-0.356563782+t*(1.781477937+t*(-1.821255978+t*1.330274429))));return z>=0?1-p:p},
 render(){return `<div class="inputs"><div class="row">${field('zx','Raw score (x)',85,{})}${field('zm','Mean (μ)',70,{})}${field('zs','Standard deviation (σ)',10,{})}</div>
  <p class="hint">Assumes the data follow a normal (bell-curve) distribution.</p></div><div class="result" id="out"></div>`},
 calc(){const x=v('zx'),m=v('zm'),s=v('zs');if(!(isFinite(x)&&isFinite(m)&&s>0)){$('#out').innerHTML='<span class="label">Z-score</span><p class="hint">Enter a score, the mean and a standard deviation above 0.</p>';return''}
  const z=(x-m)/s,p=this.cdf(z),pct=v=>num(v*100,2)+'%';
  $('#out').innerHTML=`<span class="label">Z-score</span><div class="big"><em>${num(z,4)}</em></div><p class="answer">A score of ${num(x,4)} is ${num(Math.abs(z),2)} standard deviations ${z>=0?'above':'below'} the mean, higher than about ${pct(p)} of values.</p>${kv([['Percentile',pct(p)],['P(X < x), left tail',num(p,5)],['P(X > x), right tail',num(1-p,5)],['Two-tailed p-value',num(2*Math.min(p,1-p),5)],['Between mean and x',num(Math.abs(p-0.5),5)]])}${copyBtn}`;
  return `z = ${num(z,4)}, percentile ${pct(p)}`}},

{id:'margin',cat:'Money',name:'Margin calculator',kw:'margin calculator profit margin calculator gross margin markup calculator selling price from cost and margin margin vs markup',desc:'Profit margin, markup and selling price.',
 state:{mode:'cp'},
 render(){const s=this.state;return `<div class="inputs"><div class="row">${seg('mgm',[['cp','Cost + price'],['cm','Cost + margin'],['ck','Cost + markup']],s.mode)}</div>
  <div class="row">${field('mgc','Cost',40,{unit:R().cur})}${s.mode==='cp'?field('mgp','Selling price',60,{unit:R().cur}):s.mode==='cm'?field('mgx','Margin',30,{unit:'%'}):field('mgk','Markup',50,{unit:'%'})}</div></div><div class="result" id="out"></div>`},
 calc(){const s=this.state,c=v('mgc');let p;if(s.mode==='cp')p=v('mgp');else if(s.mode==='cm'){const m=v('mgx');p=m<100?c/(1-m/100):NaN}else p=c*(1+v('mgk')/100);
  if(!(c>0&&p>0&&isFinite(p))){$('#out').innerHTML='<span class="label">Margin</span><p class="hint">Enter a cost and a price (margin must be under 100%).</p>';return''}
  const pr=p-c,mg=pr/p*100,mk=pr/c*100;
  $('#out').innerHTML=`<span class="label">${s.mode==='cp'?'Gross margin':'Selling price'}</span><div class="big"><em>${s.mode==='cp'?num(mg,2)+'%':money(p)}</em></div><p class="answer">Buy at ${money(c)}, sell at ${money(p)}: ${money(pr)} profit, a ${num(mg,2)}% margin and a ${num(mk,2)}% markup.</p>${kv([['Selling price',money(p)],['Profit',money(pr)],['Gross margin',num(mg,2)+'%'],['Markup',num(mk,2)+'%']])}${copyBtn}`;
  return `Price ${money(p)}, profit ${money(pr)}, margin ${num(mg,2)}%, markup ${num(mk,2)}%`},
 after(){bindSeg('mgm',x=>{this.state.mode=x;open('margin')})}},

{id:'fuel',cat:'Money',name:'Gas cost calculator',kw:'gas cost calculator trip fuel cost calculator road trip gas money mpg cost per mile fuel calculator split gas cost l/100km',desc:'Fuel cost of a trip from distance and mileage.',
 state:{unit:null,rt:'1'},
 render(){const s=this.state;if(!s.unit)s.unit=R().imperial?'us':'met';const us=s.unit==='us';
  return `<div class="inputs"><div class="row">${seg('fuu',[['us','Miles / MPG'],['met','km / L per 100 km']],s.unit)}${seg('furt',[['1','One way'],['2','Round trip']],s.rt)}</div>
  <div class="row">${field('fud','Distance',us?300:500,{unit:us?'mi':'km'})}${field('fue','Fuel economy',us?28:7.5,{unit:us?'mpg':'L/100 km'})}</div>
  <div class="row">${field('fup','Fuel price',us?3.1:1.75,{unit:R().cur+(us?'/gal':'/L')})}${field('fun','People sharing',1,{})}</div></div><div class="result" id="out"></div>`},
 calc(){const s=this.state,us=s.unit==='us',d=v('fud')*(+s.rt),e=v('fue'),pr=v('fup'),n=Math.max(1,Math.round(v('fun')||1));
  if(!(d>0&&e>0&&pr>0)){$('#out').innerHTML='<span class="label">Trip cost</span><p class="hint">Enter distance, fuel economy and fuel price.</p>';return''}
  const f=us?d/e:d*e/100,c=f*pr,rows=[['Fuel used',`${num(f,2)} ${us?'gallons':'litres'}`],[`Cost per ${us?'mile':'km'}`,money(c/d,3)],['Total distance',`${num(d,1)} ${us?'mi':'km'}`]];if(n>1)rows.unshift(['Per person',money(c/n)]);
  $('#out').innerHTML=`<span class="label">Fuel cost</span><div class="big"><em>${money(c)}</em></div>${kv(rows)}${copyBtn}`;
  return `Fuel cost ${money(c)}${n>1?` (${money(c/n)} each)`:''}`},
 after(){bindSeg('fuu',x=>{this.state.unit=x;open('fuel')});bindSeg('furt',x=>{this.state.rt=x;update()})}},
{id:'gravel',cat:'Home',name:'Gravel calculator',kw:'gravel calculator how much gravel do i need tons cubic yards crushed stone pea gravel river rock sand driveway calculator landscape rock',desc:'Cubic yards and tons of gravel, stone or sand.',
 state:{unit:null},
 M:[['1.4','Gravel (general)'],['1.4','Pea gravel'],['1.35','Crushed stone'],['1.3','River rock'],['1.3','Sand'],['1.1','Topsoil']],
 render(){const s=this.state;if(!s.unit)s.unit=R().imperial?'ft':'m';const ft=s.unit==='ft';
  return `<div class="inputs"><div class="row">${seg('gvu',[['ft','Feet'],['m','Metres']],s.unit)}</div>
  <div class="row">${field('gvl','Length',ft?40:12,{unit:ft?'ft':'m'})}${field('gvw','Width',ft?12:3.5,{unit:ft?'ft':'m'})}${field('gvd','Depth',ft?4:10,{unit:ft?'in':'cm'})}</div>
  <div class="row"><div class="field"><label for="gvm">Material</label><select id="gvm">${this.M.map(([d,n],i)=>`<option value="${i}">${n} (~${d} t/yd³)</option>`).join('')}</select></div></div>
  <p class="hint">Typical depths: 2 in for paths, 3–4 in for patios, 4–6 in for driveways (in two layers). Densities are averages; your supplier's figure may differ by 10% or more.</p></div><div class="result" id="out"></div>`},
 calc(){const ft=this.state.unit==='ft',A=v('gvl')*v('gvw'),d=v('gvd');if(!(A>0&&d>0)){$('#out').innerHTML='<span class="label">Gravel</span><p class="hint">Enter the area and depth.</p>';return''}
  const cf=ft?A*d/12:A*d/100*35.3147,cy=cf/27,m3=cf/35.3147,den=+this.M[+($('#gvm').value||0)][0],tons=cy*den;
  $('#out').innerHTML=`<span class="label">You need</span><div class="big"><em>${num(cy,2)}</em> yd³ · <em>${num(tons,2)}</em> tons</div>${kv([['Cubic yards',num(cy,2)],['Cubic feet',num(cf,1)],['Cubic metres',num(m3,2)],['US tons',num(tons,2)],['Pounds',num(tons*2000,0)],['Metric tonnes',num(tons*0.907185,2)],['0.5 cu ft bags',Math.ceil(cf/0.5)]])}${copyBtn}`;
  return `${num(cy,2)} cubic yards, about ${num(tons,2)} tons`},
 after(){bindSeg('gvu',x=>{this.state.unit=x;open('gravel')})}},

{id:'stair',cat:'Home',name:'Stair calculator',kw:'stair calculator stair stringer calculator rise and run number of steps riser height tread depth staircase deck stairs building code',desc:'Number of steps, riser height, run and stringer length.',
 state:{unit:null},
 render(){const s=this.state;if(!s.unit)s.unit=R().imperial?'in':'cm';const i=s.unit==='in';
  return `<div class="inputs"><div class="row">${seg('stu',[['in','Inches'],['cm','Centimetres']],s.unit)}</div>
  <div class="row">${field('str','Total rise (floor to floor)',i?108:274,{unit:s.unit})}${field('stt','Tread depth',i?10.5:26.7,{unit:s.unit})}${field('stm','Maximum riser height',i?7.75:19.7,{unit:s.unit})}</div>
  <p class="hint">US residential code (IRC): risers no taller than 7¾ in, treads at least 10 in deep, at least 6 ft 8 in of headroom. Check your local code before you build.</p></div><div class="result" id="out"></div>`},
 calc(){const i=this.state.unit==='in',u=this.state.unit,rise=v('str'),tr=v('stt'),mx=v('stm');
  if(!(rise>0&&tr>0&&mx>0)){$('#out').innerHTML='<span class="label">Stairs</span><p class="hint">Enter the total rise, tread depth and maximum riser.</p>';return''}
  const n=Math.ceil(rise/mx-1e-9),rh=rise/n,treads=n-1,run=treads*tr,str=Math.hypot(rise,run),ang=Math.atan2(rise,run)*180/Math.PI,inch=x=>i?x:x/2.54;
  const f=x=>i?`${num(x,2)} in`:`${num(x,1)} cm`,ft=x=>i?` (${Math.floor(x/12)} ft ${num(x%12,1)} in)`:'';
  const ok=inch(rh)<=7.75+1e-9&&inch(tr)>=10-1e-9,rule=2*inch(rh)+inch(tr);
  $('#out').innerHTML=`<span class="label">Your staircase</span><div class="big"><em>${n}</em> risers · <em>${treads}</em> treads</div><p class="answer">Each step rises ${f(rh)}. ${ok?'That meets the IRC limits.':'Check this against your building code: the IRC allows a 7¾ in maximum riser and a 10 in minimum tread.'}</p>${kv([['Riser height',f(rh)],['Total run',f(run)+ft(run)],['Stringer length (approx.)',f(str)+ft(str)],['Stair angle',num(ang,1)+'°'],['Comfort check (2 × riser + tread)',`${num(rule,1)} in ${rule>=24&&rule<=25.5?'✓ comfortable':'(24–25 in is ideal)'}`]])}${copyBtn}`;
  return `${n} risers of ${f(rh)}, ${treads} treads, total run ${f(run)}`},
 after(){bindSeg('stu',x=>{this.state.unit=x;open('stair')})}},

{id:'period',cat:'Health',name:'Period & ovulation calculator',kw:'period calculator next period date menstrual cycle tracker ovulation calculator fertile window when will my period come period tracker ovulation date',desc:'Next period, ovulation day and fertile window.',
 state:{},
 render(){const iso=d=>new Date(d-d.getTimezoneOffset()*6e4).toISOString().slice(0,10);const t=new Date(),ex=new Date(t.getFullYear(),t.getMonth(),t.getDate()-12);
  return `<div class="inputs"><div class="row">${field('pdd','First day of your last period',iso(ex),{type:'date'})}${field('pdc','Average cycle length',28,{unit:'days'})}${field('pdl','Period length',5,{unit:'days'})}</div>
  <p class="hint">Cycles usually run 21–35 days. Predictions are estimates, less reliable for irregular cycles, and must not be used as birth control.</p><div id="pdtab" class="tc-wrap"></div></div><div class="result" id="out"></div>`},
 calc(){const d=new Date($('#pdd').value+'T00:00'),c=Math.round(v('pdc')),L=Math.round(v('pdl'))||5;const tab=$('#pdtab');
  if(isNaN(d)||!(c>=20&&c<=45)){$('#out').innerHTML='<span class="label">Next period</span><p class="hint">Pick a date and a cycle length between 20 and 45 days.</p>';tab.innerHTML='';return''}
  const add=(x,n)=>new Date(x.getFullYear(),x.getMonth(),x.getDate()+n),f=x=>x.toLocaleDateString(R().loc,{weekday:'short',month:'short',day:'numeric'}),t=new Date(),today=new Date(t.getFullYear(),t.getMonth(),t.getDate());
  let s=d;while(add(s,c)<=today)s=add(s,c);let nx=add(s,c);if(s>today)nx=s;
  const ov=add(nx,-14),fw1=add(ov,-5),days=Math.round((nx-today)/864e5);
  const rows=[];let p=nx;for(let k=0;k<6;k++){const o=add(p,-14);rows.push(`<tr><td>${f(p)} – ${f(add(p,L-1))}</td><td>${f(add(o,-5))} – ${f(add(o,1))}</td><td>${f(o)}</td></tr>`);p=add(p,c)}
  tab.innerHTML=`<table><thead><tr><th>Period</th><th>Fertile window</th><th>Ovulation</th></tr></thead><tbody>${rows.join('')}</tbody></table>`;
  $('#out').innerHTML=`<span class="label">Next period</span><div class="big"><em>${f(nx)}</em></div><p class="answer">${days===0?'Your period is due today.':`Your next period is due in ${days} ${days===1?'day':'days'}.`}</p>${kv([['Expected to last until',f(add(nx,L-1))],['Ovulation (estimated)',f(ov)],['Fertile window',`${f(fw1)} – ${f(add(ov,1))}`],['Cycle day today',String(Math.round((today-s)/864e5)+1)]])}${copyBtn}`;
  return `Next period ${f(nx)}, ovulation ${f(ov)}`}},

{id:'love',cat:'Fun',name:'Love calculator',kw:'love calculator name compatibility test love percentage calculator crush calculator love meter flames game true love test',desc:'A just-for-fun love percentage from two names.',
 state:{},
 render(){return `<div class="inputs"><div class="row">${field('lva','Your name','Alex',{type:'text'})}${field('lvb','Their name','Sam',{type:'text'})}</div>
  <p class="hint">Just for fun. The score comes from the letters in the names, so the same two names always get the same result.</p></div><div class="result" id="out"></div>`},
 calc(){const a=($('#lva').value||'').trim().toLowerCase().replace(/[^a-zÀ-ɏ ]/g,''),b=($('#lvb').value||'').trim().toLowerCase().replace(/[^a-zÀ-ɏ ]/g,'');
  if(!a||!b){$('#out').innerHTML='<span class="label">Love score</span><p class="hint">Enter two names.</p>';return''}
  const k=[a,b].sort().join('+loves+');let h=2166136261;for(const ch of k){h^=ch.charCodeAt(0);h=Math.imul(h,16777619)>>>0}const sc=35+h%66;
  const msg=sc>=90?'A match made in heaven!':sc>=75?'Great chemistry. Go for it!':sc>=60?'Good potential with a little effort.':sc>=45?'Friends first? Could grow into more.':'Opposites attract… sometimes!';
  const cap=x=>x.replace(/\b\w/g,c=>c.toUpperCase());
  $('#out').innerHTML=`<span class="label">${cap(a)} ❤ ${cap(b)}</span><div class="big"><em>${sc}%</em></div><p class="answer">${msg}</p><div style="height:12px;border-radius:6px;background:var(--line);overflow:hidden;margin:6px 0 14px"><div style="height:100%;width:${sc}%;background:#e2557a"></div></div>${copyBtn}`;
  return `${cap(a)} + ${cap(b)} = ${sc}% love match on Numbrik`}},

{id:'rmd',cat:'Money',name:'RMD calculator',kw:'rmd calculator required minimum distribution ira 401k uniform lifetime table rmd age 73 75 how much must i withdraw',desc:'Required minimum distribution from an IRA or 401(k).',
 state:{},
 U:{72:27.4,73:26.5,74:25.5,75:24.6,76:23.7,77:22.9,78:22.0,79:21.1,80:20.2,81:19.4,82:18.5,83:17.7,84:16.8,85:16.0,86:15.2,87:14.4,88:13.7,89:12.9,90:12.2,91:11.5,92:10.8,93:10.1,94:9.5,95:8.9,96:8.4,97:7.8,98:7.3,99:6.8,100:6.4,101:6.0,102:5.6,103:5.2,104:4.9,105:4.6,106:4.3,107:4.1,108:3.9,109:3.7,110:3.5,111:3.4,112:3.3,113:3.1,114:3.0,115:2.9,116:2.8,117:2.7,118:2.5,119:2.3,120:2.0},
 render(){const y=new Date().getFullYear();return `<div class="inputs"><div class="row">${field('rmb','Year of birth',1952,{})}${field('rmy','Distribution year',y,{})}</div>
  <div class="row">${field('rmv','Account balance on Dec 31 of the prior year',500000,{unit:'USD'})}${field('rmg','Expected growth (for projection)',5,{unit:'%'})}</div>
  <p class="hint">Uses the IRS Uniform Lifetime Table. If your spouse is your sole beneficiary and more than 10 years younger, the Joint Life table gives a smaller RMD. Not tax advice.</p><div id="rmtab" class="tc-wrap"></div></div><div class="result" id="out"></div>`},
 calc(){const b=Math.round(v('rmb')),y=Math.round(v('rmy')),bal=v('rmv'),g=(v('rmg')||0)/100,tab=$('#rmtab');const usd=n=>new Intl.NumberFormat('en-US',{style:'currency',currency:'USD',maximumFractionDigits:0}).format(n);
  if(!(b>1900&&y>=2023&&bal>=0)){$('#out').innerHTML='<span class="label">RMD</span><p class="hint">Enter your birth year, the year and the balance.</p>';tab.innerHTML='';return''}
  const start=b<=1950?72:b<=1959?73:75,age=y-b;
  if(age<start){tab.innerHTML='';$('#out').innerHTML=`<span class="label">RMD for ${y}</span><div class="big"><em>$0</em></div><p class="answer">No RMD is due for ${y}. Born in ${b}, your RMDs start at age ${start}: your first one is for ${b+start}, due by April 1, ${b+start+1}.</p>${copyBtn}`;return `No RMD due in ${y}; first RMD year ${b+start}`}
  const F=this.U[Math.min(age,120)],r=bal/F;let B=bal,rows=[];for(let k=0;k<10;k++){const a=age+k,fc=this.U[Math.min(a,120)],d=B/fc;rows.push(`<tr><td>${y+k}</td><td>${a}</td><td class="num">${fc.toFixed(1)}</td><td class="num">${usd(B)}</td><td class="num">${usd(d)}</td></tr>`);B=(B-d)*(1+g)}
  tab.innerHTML=`<table><thead><tr><th>Year</th><th>Age</th><th>Factor</th><th>Start balance</th><th>RMD</th></tr></thead><tbody>${rows.join('')}</tbody></table>`;
  const first=age===start;
  $('#out').innerHTML=`<span class="label">RMD for ${y}</span><div class="big"><em>${usd(r)}</em></div><p class="answer">At age ${age}, divide ${usd(bal)} by ${F.toFixed(1)}. ${first?`As your first RMD, you can delay it to April 1, ${y+1}, but then you'll take two that year.`:`Withdraw it by December 31, ${y}.`}</p>${kv([['Distribution period (factor)',F.toFixed(1)],['Percent of balance',num(r/bal*100,2)+'%'],['Monthly if spread out',usd(r/12)],['RMD start age for you',String(start)]])}${copyBtn}`;
  return `RMD for ${y}: ${usd(r)}`}},

{id:'rounding',cat:'Math',name:'Rounding calculator',kw:'rounding calculator round to nearest tenth hundredth whole number thousandth ten hundred round decimals significant figures round half up half even',desc:'Round a number to any place, any method.',
 state:{pl:'2',md:'hu'},
 rnd(x,d,md){const f=Math.pow(10,d),r=Number((x*f).toPrecision(14)),fl=Math.floor(r),fr=Number((r-fl).toPrecision(12));let o;
  if(md==='hu')o=Math.sign(r)*Math.floor(Math.abs(r)+0.5+1e-12);else if(md==='he')o=fr===0.5?(fl%2===0?fl:fl+1):Math.round(r);else if(md==='up')o=Math.ceil(r);else if(md==='dn')o=Math.floor(r);else o=Math.trunc(r);
  return d>0?Number((o/f).toFixed(d)):o/f},
 render(){const s=this.state;return `<div class="inputs"><div class="row">${field('rnx','Number',3.14159,{})}</div>
  <div class="row"><div class="field"><label>Round to</label>${seg('rnp',[['-2','Hundreds'],['-1','Tens'],['0','Whole'],['1','Tenths'],['2','Hundredths'],['3','Thousandths']],s.pl)}</div></div>
  <div class="row"><div class="field"><label>Method</label>${seg('rnm',[['hu','Half up'],['he','Half to even'],['up','Up (ceiling)'],['dn','Down (floor)'],['tr','Truncate']],s.md)}</div></div></div><div class="result" id="out"></div>`},
 calc(){const s=this.state,x=v('rnx');if(!isFinite(x)){$('#out').innerHTML='<span class="label">Rounded</span><p class="hint">Enter a number.</p>';return''}
  const d=+s.pl,fmt=(n,dd)=>dd>0?n.toFixed(dd):String(n),r=this.rnd(x,d,s.md);
  const P=[[-3,'Nearest thousand'],[-2,'Nearest hundred'],[-1,'Nearest ten'],[0,'Whole number'],[1,'Tenth (1 dp)'],[2,'Hundredth (2 dp)'],[3,'Thousandth (3 dp)'],[4,'Ten-thousandth (4 dp)']];
  $('#out').innerHTML=`<span class="label">Rounded</span><div class="big"><em>${fmt(r,d)}</em></div>${kv(P.map(([dd,n])=>[n,fmt(this.rnd(x,dd,s.md),dd)]))}${copyBtn}`;
  return `${x} rounded = ${fmt(r,d)}`},
 after(){bindSeg('rnp',x=>{this.state.pl=x;update()});bindSeg('rnm',x=>{this.state.md=x;update()})}},

{id:'timezone',cat:'Dates & time',name:'Time zone converter',kw:'time zone converter est to pst ist to est time difference convert time between time zones world clock meeting planner gmt utc cst',desc:'Convert a time between US and world time zones.',
 state:{},
 Z:[['America/New_York','Eastern (New York)'],['America/Chicago','Central (Chicago)'],['America/Denver','Mountain (Denver)'],['America/Phoenix','Arizona (Phoenix)'],['America/Los_Angeles','Pacific (Los Angeles)'],['America/Anchorage','Alaska'],['Pacific/Honolulu','Hawaii'],['America/Toronto','Toronto'],['America/Mexico_City','Mexico City'],['America/Sao_Paulo','São Paulo'],['UTC','UTC / GMT'],['Europe/London','London'],['Europe/Paris','Paris / Berlin (CET)'],['Africa/Lagos','Lagos'],['Asia/Dubai','Dubai'],['Asia/Karachi','Pakistan'],['Asia/Kolkata','India (IST)'],['Asia/Manila','Manila'],['Asia/Singapore','Singapore'],['Asia/Shanghai','China'],['Asia/Tokyo','Tokyo'],['Australia/Sydney','Sydney'],['Pacific/Auckland','Auckland']],
 off(ms,tz){const p={};new Intl.DateTimeFormat('en-US',{timeZone:tz,hourCycle:'h23',year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',second:'2-digit'}).formatToParts(new Date(ms)).forEach(x=>p[x.type]=x.value);return Date.UTC(+p.year,+p.month-1,+p.day,+p.hour%24,+p.minute,+p.second)-ms},
 sel(id,cur){return `<select id="${id}">${this.Z.map(([z,n])=>`<option value="${z}"${z===cur?' selected':''}>${n}</option>`).join('')}</select>`},
 render(){let me='America/New_York';try{const z=Intl.DateTimeFormat().resolvedOptions().timeZone;if(this.Z.some(x=>x[0]===z))me=z}catch(e){}
  const n=new Date(),iso=new Date(n-n.getTimezoneOffset()*6e4).toISOString();
  return `<div class="inputs"><div class="row">${field('tzd','Date',iso.slice(0,10),{type:'date'})}${field('tzt','Time',iso.slice(11,16),{type:'time'})}</div>
  <div class="row"><div class="field"><label for="tza">From</label>${this.sel('tza',me)}</div><div class="field"><label for="tzb">To</label>${this.sel('tzb',me==='Asia/Kolkata'?'America/New_York':'Asia/Kolkata')}</div></div>
  <p class="hint">Daylight saving time is applied automatically for the date you pick.</p><div id="tztab" class="tc-wrap"></div></div><div class="result" id="out"></div>`},
 calc(){const d=$('#tzd').value,t=$('#tzt').value,A=$('#tza').value,B=$('#tzb').value,tab=$('#tztab');if(!d||!t){$('#out').innerHTML='<span class="label">Converted time</span><p class="hint">Pick a date and time.</p>';return''}
  const [Y,M,D]=d.split('-').map(Number),[h,mi]=t.split(':').map(Number),g=Date.UTC(Y,M-1,D,h,mi);let u=g-this.off(g,A);u=g-this.off(u,A);
  const fmt=(tz,o={})=>new Intl.DateTimeFormat(R().loc,Object.assign({timeZone:tz,hour:'numeric',minute:'2-digit'},o)).format(new Date(u)),nm=z=>this.Z.find(x=>x[0]===z)[1];
  const diff=(this.off(u,B)-this.off(u,A))/36e5,ds=(diff>=0?'+':'−')+num(Math.abs(diff),2)+' h';
  tab.innerHTML=`<table><thead><tr><th>City</th><th style="text-align:right">Time</th></tr></thead><tbody>${['America/Los_Angeles','America/New_York','Europe/London','Europe/Paris','Asia/Dubai','Asia/Kolkata','Asia/Tokyo','Australia/Sydney'].map(z=>`<tr><td>${nm(z)}</td><td class="num">${fmt(z,{weekday:'short'})}</td></tr>`).join('')}</tbody></table>`;
  $('#out').innerHTML=`<span class="label">${nm(B)}</span><div class="big"><em>${fmt(B)}</em></div><p class="answer">${fmt(A)} in ${nm(A)} is ${fmt(B,{weekday:'long',month:'short',day:'numeric'})} in ${nm(B)}.</p>${kv([['Time difference',ds],['From',fmt(A,{weekday:'short',month:'short',day:'numeric'})+' '+fmt(A,{timeZoneName:'short'}).split(' ').pop()],['To',fmt(B,{weekday:'short',month:'short',day:'numeric'})+' '+fmt(B,{timeZoneName:'short'}).split(' ').pop()],['UTC',fmt('UTC',{weekday:'short'})]])}${copyBtn}`;
  return `${fmt(A)} ${nm(A)} = ${fmt(B)} ${nm(B)}`}},
{id:'height',cat:'Health',name:'Child height calculator',kw:'height calculator how tall will i be how tall will my child be adult height predictor child height prediction mid parental height kids growth',desc:'Predict a child’s adult height from the parents’ heights.',
 state:{sex:'m',unit:null,mode:'par'},
 render(){const s=this.state;if(!s.unit)s.unit=R().imperial?'imp':'met';const imp=s.unit==='imp';
  const H=(id,l,ft,inch,cm)=>imp?field(id+'f',l+' (ft)',ft,{unit:'ft'})+field(id+'i',l+' (in)',inch,{unit:'in'}):field(id,l,cm,{unit:'cm'});
  return `<div class="inputs"><div class="row">${seg('hts',[['m','Boy'],['f','Girl']],s.sex)}${seg('htu',[['imp','Feet / inches'],['met','cm']],s.unit)}</div>
  <div class="row">${seg('htm',[['par','From parents’ heights'],['two','From height as a toddler']],s.mode)}</div>
  <div class="row">${s.mode==='par'?H('htf','Father’s height',5,10,178)+H('htmo','Mother’s height',5,5,165):H('htk',s.sex==='m'?'Height at age 2':'Height at 18 months',2,10,86)}</div>
  <p class="hint">${s.mode==='par'?'The mid-parental method. Most children end up within about 4 inches (10 cm) of the prediction.':'The doubling rule: boys reach about twice their height at age 2, girls about twice their height at 18 months. A rough guide only.'}</p></div><div class="result" id="out"></div>`},
 calc(){const s=this.state,imp=s.unit==='imp',g=id=>imp?((v(id+'f')||0)*12+(v(id+'i')||0))*2.54:v(id);let cm,how;
  if(s.mode==='par'){const f=g('htf'),m=g('htmo');if(!(f>100&&m>100)){$('#out').innerHTML='<span class="label">Predicted adult height</span><p class="hint">Enter both parents’ heights.</p>';return''}cm=(f+m+(s.sex==='m'?13:-13))/2;how='Mid-parental height'}
  else{const k=g('htk');if(!(k>50&&k<120)){$('#out').innerHTML='<span class="label">Predicted adult height</span><p class="hint">Enter the toddler’s height.</p>';return''}cm=k*2;how='Doubling rule'}
  const F=c=>imp?`${Math.floor(Math.round(c/2.54)/12)} ft ${Math.round(c/2.54)%12} in`:`${num(c,0)} cm`;
  $('#out').innerHTML=`<span class="label">Predicted adult height</span><div class="big"><em>${F(cm)}</em></div><p class="answer">Likely range: ${F(cm-10)} to ${F(cm+10)}.</p>${kv([['Method',how],['In centimetres',num(cm,1)+' cm'],['In inches',num(cm/2.54,1)+' in']])}${copyBtn}`;
  return `Predicted adult height ${F(cm)} (range ${F(cm-10)}–${F(cm+10)})`},
 after(){bindSeg('hts',x=>{this.state.sex=x;open('height')});bindSeg('htu',x=>{this.state.unit=x;open('height')});bindSeg('htm',x=>{this.state.mode=x;open('height')})}},

{id:'deficit',cat:'Health',name:'Calorie deficit calculator',kw:'calorie deficit calculator how many calories to lose weight weight loss calculator goal weight date calories per day to lose 1 lb 2 lbs a week',desc:'Daily calories to reach a goal weight by a date.',
 state:{sex:'f',unit:null,rate:'1'},
 render(){const s=this.state;if(!s.unit)s.unit=R().imperial?'imp':'met';const imp=s.unit==='imp';
  return `<div class="inputs"><div class="row">${seg('cds',[['f','Female'],['m','Male']],s.sex)}${seg('cdu',[['imp','US units'],['met','Metric']],s.unit)}</div>
  <div class="row">${field('cda','Age',35,{unit:'yrs'})}${imp?field('cdft','Height (feet)',5,{unit:'ft'})+field('cdin','Height (inches)',5,{unit:'in'}):field('cdcm','Height',165,{unit:'cm'})}</div>
  <div class="row">${field('cdw','Current weight',imp?180:82,{unit:imp?'lb':'kg'})}${field('cdg','Goal weight',imp?160:73,{unit:imp?'lb':'kg'})}<div class="field"><label for="cdx">Activity</label><select id="cdx"><option value="1.2">Desk job, little exercise</option><option value="1.375" selected>Light exercise 1–3 days/week</option><option value="1.55">Moderate exercise 3–5 days/week</option><option value="1.725">Hard exercise 6–7 days/week</option></select></div></div>
  <div class="row"><div class="field"><label>Pace</label>${seg('cdr',imp?[['0.5','0.5 lb/week'],['1','1 lb/week'],['1.5','1.5 lb/week'],['2','2 lb/week']]:[['0.5','0.25 kg/week'],['1','0.5 kg/week'],['1.5','0.75 kg/week'],['2','1 kg/week']],s.rate)}</div></div>
  <p class="hint">An estimate for healthy adults. Talk to a doctor before a big change in diet, especially if you're pregnant, under 18 or have a medical condition.</p></div><div class="result" id="out"></div>`},
 calc(){const s=this.state,imp=s.unit==='imp',a=v('cda'),h=imp?((v('cdft')||0)*12+(v('cdin')||0))*2.54:v('cdcm'),toKg=x=>imp?x*0.45359237:x,w=toKg(v('cdw')),gw=toKg(v('cdg'));
  if(!(a>0&&h>0&&w>0&&gw>0)){$('#out').innerHTML='<span class="label">Daily calories</span><p class="hint">Enter your details and goal weight.</p>';return''}
  if(gw>=w){$('#out').innerHTML='<span class="label">Daily calories</span><p class="hint">Your goal weight should be lower than your current weight. To gain weight, use the TDEE calculator.</p>';return''}
  const bmr=10*w+6.25*h-5*a+(s.sex==='m'?5:-161),tdee=bmr*(+$('#cdx').value),lbw=+s.rate*(imp?1:1.10231),def=lbw*3500/7,floor=s.sex==='m'?1500:1200;
  let cal=tdee-def,warn='';if(cal<floor){warn=`<p class="hint">That pace would put you below ${floor} calories a day, which is hard to get enough nutrients on. The target is set at ${floor}; your loss will be slower.</p>`;cal=floor}
  const actual=Math.max(0.1,(tdee-cal)*7/3500),lbsToLose=(w-gw)/0.45359237,weeks=lbsToLose/actual,end=new Date(Date.now()+weeks*7*864e5),R10=n=>num(Math.round(n/10)*10,0);
  $('#out').innerHTML=`<span class="label">Eat about</span><div class="big"><em>${R10(cal)}</em> calories/day</div><p class="answer">You could reach your goal in about ${num(weeks,0)} weeks, around ${end.toLocaleDateString(R().loc,{month:'long',day:'numeric',year:'numeric'})}.</p>${warn}${kv([['Maintenance (TDEE)',R10(tdee)+' cal'],['Daily deficit',R10(tdee-cal)+' cal'],['To lose',imp?num(lbsToLose,1)+' lb':num(w-gw,1)+' kg'],['BMR',R10(bmr)+' cal']])}${copyBtn}`;
  return `${R10(cal)} calories/day, goal in about ${num(weeks,0)} weeks`},
 after(){bindSeg('cds',x=>{this.state.sex=x;update()});bindSeg('cdu',x=>{this.state.unit=x;open('deficit')});bindSeg('cdr',x=>{this.state.rate=x;update()})}},

{id:'bac',cat:'Health',name:'BAC calculator',kw:'bac calculator blood alcohol content calculator how drunk am i blood alcohol level widmark formula how long to sober up am i over the limit',desc:'Estimated blood alcohol content and time to sober up.',
 state:{sex:'m',unit:null},
 render(){const s=this.state;if(!s.unit)s.unit=R().imperial?'lb':'kg';
  return `<div class="inputs"><div class="row">${seg('bcs',[['m','Male'],['f','Female']],s.sex)}${seg('bcu',[['lb','lb'],['kg','kg']],s.unit)}</div>
  <div class="row">${field('bcw','Body weight',s.unit==='lb'?170:77,{unit:s.unit})}${field('bch','Hours since first drink',2,{unit:'hrs'})}</div>
  <div class="row">${field('bcb','Beers (12 oz, 5%)',2,{})}${field('bcv','Glasses of wine (5 oz, 12%)',1,{})}${field('bcl','Shots (1.5 oz, 40%)',0,{})}</div>
  <p class="hint"><strong>Never use this to decide whether you can drive.</strong> Real BAC varies with food, medication, health and drink size. If you've been drinking, don't drive.</p></div><div class="result" id="out"></div>`},
 calc(){const s=this.state,w=v('bcw')*(s.unit==='lb'?453.592:1000),h=Math.max(0,v('bch')||0),dr=(v('bcb')||0)+(v('bcv')||0)+(v('bcl')||0);
  if(!(w>0)){$('#out').innerHTML='<span class="label">Estimated BAC</span><p class="hint">Enter your weight and drinks.</p>';return''}
  const g=dr*14,r=s.sex==='m'?0.68:0.55,peak=g/(w*r)*100,bac=Math.max(0,peak-0.015*h),sober=bac/0.015;
  const st=bac<0.02?'Little or no effect for most people.':bac<0.05?'Relaxed, some loss of judgment.':bac<0.08?'Impaired judgment and coordination. Over the limit in Utah (0.05%).':bac<0.15?'Over the legal driving limit in every US state (0.08%). Clearly impaired.':bac<0.3?'Severely impaired. Risk of blackout and vomiting.':'Life-threatening. Call 911 if someone is this drunk, unresponsive or breathing slowly.';
  $('#out').innerHTML=`<span class="label">Estimated BAC</span><div class="big"><em>${bac.toFixed(3)}%</em></div><p class="answer">${st}</p>${kv([['Standard drinks',num(dr,1)],['Alcohol',num(g,0)+' g'],['Back to 0.00% in about',bac>0?`${Math.floor(sober)} h ${Math.round((sober%1)*60)} min`:'Now'],['US driving limit','0.08% (0.05% in Utah)']])}${copyBtn}`;
  return `Estimated BAC ${bac.toFixed(3)}%`},
 after(){bindSeg('bcs',x=>{this.state.sex=x;update()});bindSeg('bcu',x=>{this.state.unit=x;open('bac')})}},

{id:'bra',cat:'Converters',name:'Bra size calculator',kw:'bra size calculator how to measure bra size band size cup size calculator us uk eu bra size chart underbust bust measurement',desc:'Band and cup size from two measurements.',
 state:{unit:null},
 US:['AA','A','B','C','D','DD','DDD','G','H','I','J','K'],UK:['AA','A','B','C','D','DD','E','F','FF','G','GG','H'],EU:['AA','A','B','C','D','E','F','G','H','I','J','K'],
 render(){const s=this.state;if(!s.unit)s.unit=R().imperial?'in':'cm';const i=s.unit==='in';
  return `<div class="inputs"><div class="row">${seg('bru',[['in','Inches'],['cm','cm']],s.unit)}</div>
  <div class="row">${field('brb','Underbust (snug, around the ribcage)',i?32:81,{unit:s.unit})}${field('brt','Bust (fullest part, loosely)',i?36:91,{unit:s.unit})}</div>
  <p class="hint">Measure without a padded bra, tape level all the way round. This uses the modern method (band = underbust rounded to the nearest even inch, no “+4”).</p></div><div class="result" id="out"></div>`},
 calc(){const i=this.state.unit==='in',ub=i?v('brb'):v('brb')/2.54,bu=i?v('brt'):v('brt')/2.54;
  if(!(ub>20&&bu>ub)){$('#out').innerHTML='<span class="label">Bra size</span><p class="hint">Enter your underbust and bust. Bust must be larger than underbust.</p>';return''}
  const band=Math.max(28,2*Math.round(ub/2)),d=Math.max(0,Math.round(bu-band)),c=Math.min(d,11),eu=`${70+(band-32)/2*5}${this.EU[c]}`;
  const us=`${band}${this.US[c]}`,uk=`${band}${this.UK[c]}`,sis=[[band-2,Math.min(11,c+1)],[band+2,Math.max(0,c-1)]];
  $('#out').innerHTML=`<span class="label">Your bra size (US)</span><div class="big"><em>${us}</em></div>${kv([['UK',uk],['EU',eu],['Sister sizes (US)',sis.map(([b,k])=>b+this.US[k]).join(', ')],['Bust − band',num(d,0)+' in']])}${d>11?'<p class="hint">Larger than K: check a specialist brand’s chart.</p>':''}${copyBtn}`;
  return `Bra size US ${us}, UK ${uk}, EU ${eu}`},
 after(){bindSeg('bru',x=>{this.state.unit=x;open('bra')})}},

{id:'numerology',cat:'Fun',name:'Life path number calculator',kw:'numerology calculator life path number calculator birthday number destiny number expression number master number 11 22 33 numerology meaning',desc:'Your numerology life path and birthday numbers.',
 state:{},
 M:{1:'The Leader: independent, driven and original.',2:'The Peacemaker: diplomatic, patient and caring.',3:'The Communicator: creative, expressive and social.',4:'The Builder: practical, loyal and hard-working.',5:'The Adventurer: curious, restless and freedom-loving.',6:'The Nurturer: responsible, warm and protective.',7:'The Seeker: thoughtful, analytical and spiritual.',8:'The Achiever: ambitious, confident and business-minded.',9:'The Humanitarian: generous, idealistic and compassionate.',11:'Master number 11, the Intuitive: inspired, sensitive and visionary.',22:'Master number 22, the Master Builder: turns big dreams into reality.',33:'Master number 33, the Master Teacher: devoted to helping others.'},
 red(n,keep=true){while(n>9&&!(keep&&(n===11||n===22||n===33)))n=String(n).split('').reduce((a,b)=>a+ +b,0);return n},
 render(){return `<div class="inputs"><div class="row">${field('nmd','Date of birth','1990-07-23',{type:'date'})}${field('nmn','Full birth name (optional)','',{type:'text'})}</div>
  <p class="hint">For entertainment. Numerology is a tradition, not a science.</p></div><div class="result" id="out"></div>`},
 calc(){const d=$('#nmd').value;if(!d){$('#out').innerHTML='<span class="label">Life path number</span><p class="hint">Pick your date of birth.</p>';return''}
  const [y,m,dd]=d.split('-').map(Number),a=this.red(m),b=this.red(dd),c=this.red(y),lp=this.red(a+b+c);
  const rows=[['Month',`${m} → ${a}`],['Day',`${dd} → ${b}`],['Year',`${y} → ${c}`],['Birthday number',String(this.red(dd))]];
  const nm=($('#nmn').value||'').toUpperCase().replace(/[^A-Z]/g,'');if(nm){const val=ch=>((ch.charCodeAt(0)-65)%9)+1;const ex=this.red([...nm].reduce((s,ch)=>s+val(ch),0)),su=this.red([...nm].filter(ch=>'AEIOU'.includes(ch)).reduce((s,ch)=>s+val(ch),0));rows.push(['Expression (destiny) number',String(ex)],['Soul urge number',String(su)])}
  $('#out').innerHTML=`<span class="label">Your life path number</span><div class="big"><em>${lp}</em></div><p class="answer">${this.M[lp]}</p>${kv(rows)}${copyBtn}`;
  return `Life path number ${lp}`}},

{id:'gloan',cat:'Money',name:'Loan calculator',kw:'loan calculator personal loan calculator monthly payment loan payment calculator amortization schedule interest total cost of loan payoff',desc:'Monthly payment, total interest and payoff schedule.',
 state:{tu:'y'},
 render(){const s=this.state,c=R().cur;return `<div class="inputs"><div class="row">${field('gla','Loan amount',20000,{unit:c})}${field('glr','Interest rate (APR)',9.5,{unit:'%'})}</div>
  <div class="row">${field('glt','Loan term',s.tu==='y'?5:60,{unit:s.tu==='y'?'years':'months'})}${seg('gltu',[['y','Years'],['m','Months']],s.tu)}${field('glx','Extra payment per month',0,{unit:c})}</div><div id="gltab" class="tc-wrap"></div></div><div class="result" id="out"></div>`},
 calc(){const s=this.state,P=v('gla'),r=v('glr')/1200,n=Math.round(s.tu==='y'?v('glt')*12:v('glt')),x=Math.max(0,v('glx')||0),tab=$('#gltab');
  if(!(P>0&&n>0&&r>=0)){$('#out').innerHTML='<span class="label">Monthly payment</span><p class="hint">Enter the amount, rate and term.</p>';tab.innerHTML='';return''}
  const pm=r?P*r/(1-Math.pow(1+r,-n)):P/n;let b=P,ti=0,k=0,yr=[],yi=0,yp=0;while(b>0.005&&k<1200){const i=b*r,pr=Math.min(b,pm+x-i);b-=pr;ti+=i;yi+=i;yp+=pr;k++;if(k%12===0||b<=0.005){yr.push(`<tr><td>${Math.ceil(k/12)}</td><td class="num">${money(yp,0)}</td><td class="num">${money(yi,0)}</td><td class="num">${money(Math.max(0,b),0)}</td></tr>`);yi=0;yp=0}}
  tab.innerHTML=`<table><thead><tr><th>Year</th><th>Principal paid</th><th>Interest</th><th>Balance</th></tr></thead><tbody>${yr.join('')}</tbody></table>`;
  const base=pm*n-P,rows=[['Total interest',money(ti)],['Total of payments',money(P+ti)],['Payoff time',`${Math.floor(k/12)} yrs ${k%12} mos`]];if(x>0)rows.push(['Interest saved by extra payments',money(base-ti)]);
  $('#out').innerHTML=`<span class="label">Monthly payment</span><div class="big"><em>${money(pm)}</em></div>${kv(rows)}${copyBtn}`;
  return `Monthly payment ${money(pm)}, total interest ${money(ti)}`},
 after(){bindSeg('gltu',x=>{this.state.tu=x;open('gloan')})}},

{id:'datecalc',cat:'Dates & time',name:'Date calculator',kw:'date calculator add days to a date subtract days from date add weeks months years date plus days what date is 90 days from date business days',desc:'Add or subtract days, weeks, months or years from a date.',
 state:{op:'+'},
 render(){const t=new Date(),iso=new Date(t-t.getTimezoneOffset()*6e4).toISOString().slice(0,10),s=this.state;
  return `<div class="inputs"><div class="row">${field('dcs','Start date',iso,{type:'date'})}${seg('dco',[['+','Add'],['-','Subtract']],s.op)}</div>
  <div class="row">${field('dcy','Years',0,{})}${field('dcm','Months',0,{})}${field('dcw','Weeks',0,{})}${field('dcd2','Days',90,{})}</div>
  <p class="hint">Months are added as calendar months: January 31 + 1 month = February 28 (or 29).</p></div><div class="result" id="out"></div>`},
 calc(){const s=this.state,d=new Date($('#dcs').value+'T00:00');if(isNaN(d)){$('#out').innerHTML='<span class="label">Result</span><p class="hint">Pick a start date.</p>';return''}
  const sg=s.op==='+'?1:-1,y=Math.round(v('dcy')||0)*sg,m=Math.round(v('dcm')||0)*sg,dd=(Math.round(v('dcw')||0)*7+Math.round(v('dcd2')||0))*sg;
  const tm=d.getMonth()+m+12*y,ty=d.getFullYear()+Math.floor(tm/12),mm=((tm%12)+12)%12,last=new Date(ty,mm+1,0).getDate();let r=new Date(ty,mm,Math.min(d.getDate(),last));r=new Date(r.getFullYear(),r.getMonth(),r.getDate()+dd);
  const f=x=>x.toLocaleDateString(R().loc,{weekday:'long',month:'long',day:'numeric',year:'numeric'}),diff=Math.round((r-d)/864e5);
  let bd=0;const st=diff<0?-1:1;for(let i=1;i<=Math.abs(diff)&&i<40000;i++){const q=new Date(d.getFullYear(),d.getMonth(),d.getDate()+st*i).getDay();if(q&&q<6)bd++}
  $('#out').innerHTML=`<span class="label">Result</span><div class="big"><em>${f(r)}</em></div>${kv([['Total days',num(Math.abs(diff),0)],['Weekdays (Mon–Fri) in between',num(bd,0)],['Weeks',num(Math.abs(diff)/7,2)],['Day of the year',String(Math.round((r-new Date(r.getFullYear(),0,1))/864e5)+1)]])}${copyBtn}`;
  return f(r)},
 after(){bindSeg('dco',x=>{this.state.op=x;update()})}},
{id:'afford',cat:'Money',name:'House affordability calculator',kw:'how much house can i afford calculator home affordability calculator mortgage affordability how much mortgage can i afford income 28/36 rule debt to income dti',desc:'How much house you can afford on your income.',
 state:{rule:'36'},
 solve(inc,debt,down,rate,yrs,tax,ins,hoa,rule){const r=rate/1200,n=yrs*12,k=r?r/(1-Math.pow(1+r,-n)):1/n,front=rule==='36'?0.28:0.31,back=rule==='36'?0.36:0.43;
  const M=Math.min(inc/12*front,inc/12*back-debt),fixed=ins/12+hoa;let pm=0.005/12,H=(M-fixed+down*(k+pm))/(k+tax/1200+pm);if(down>=0.2*H){pm=0;H=(M-fixed+down*k)/(k+tax/1200)}
  H=Math.max(H,down);const L=Math.max(0,H-down),pi=L*k,tx=H*tax/1200,pmi=down<0.2*H?L*0.005/12:0;return{H,L,pi,tx,ins:ins/12,hoa,pmi,tot:pi+tx+ins/12+hoa+pmi,M,front,back}},
 render(){const s=this.state,c=R().cur;return `<div class="inputs"><div class="row">${field('afi','Annual household income (before tax)',100000,{unit:c})}${field('afd','Monthly debt payments',500,{unit:c})}${field('afp','Down payment',40000,{unit:c})}</div>
  <div class="row">${field('afr','Mortgage rate',6.5,{unit:'%'})}${field('aft','Loan term',30,{unit:'yrs'})}${field('afx','Property tax',1.1,{unit:'% / yr'})}</div>
  <div class="row">${field('afn','Home insurance',1800,{unit:c+'/yr'})}${field('afh','HOA fees',0,{unit:c+'/mo'})}<div class="field"><label>Debt-to-income rule</label>${seg('afrule',[['36','28/36 (conservative)'],['43','31/43 (FHA-style)']],s.rule)}</div></div>
  <p class="hint">Monthly debts: car loans, student loans, credit card minimums, child support. Not rent, utilities or groceries.</p></div><div class="result" id="out"></div>`},
 calc(){const g=id=>v(id)||0,inc=v('afi');if(!(inc>0)){$('#out').innerHTML='<span class="label">You can afford</span><p class="hint">Enter your annual income.</p>';return''}
  const x=this.solve(inc,g('afd'),g('afp'),g('afr'),g('aft')||30,g('afx'),g('afn'),g('afh'),this.state.rule);
  if(!(x.M>x.ins+x.hoa)||x.H<=g('afp')+1){$('#out').innerHTML='<span class="label">You can afford</span><p class="hint">Your monthly debts are too high for this rule. Paying some down, or the 31/43 rule, will raise your budget.</p>';return''}
  const p=n=>money(n,0);
  $('#out').innerHTML=`<span class="label">You can afford a home of about</span><div class="big"><em>${p(x.H)}</em></div><p class="answer">With ${p(g('afp'))} down, that's a ${p(x.L)} mortgage and about ${p(x.tot)} a month including taxes and insurance.</p>${kv([['Principal & interest',p(x.pi)],['Property tax',p(x.tx)],['Home insurance',p(x.ins)],...(x.hoa?[['HOA',p(x.hoa)]]:[]),...(x.pmi?[['PMI (est. 0.5%/yr, under 20% down)',p(x.pmi)]]:[]),['Total monthly payment',p(x.tot)],['Housing ratio (front-end DTI)',num(x.tot/(inc/12)*100,1)+'%'],['Total debt ratio (back-end DTI)',num((x.tot+g('afd'))/(inc/12)*100,1)+'%'],['Down payment',num(g('afp')/x.H*100,1)+'% of price']])}${copyBtn}`;
  return `You can afford a home of about ${p(x.H)} (${p(x.tot)}/month)`},
 after(){bindSeg('afrule',x=>{this.state.rule=x;update()})}},
{id:'wordcount',cat:'Students',name:'Word counter',kw:'word counter count words online character count sentence counter paragraph counter reading time essay word count tool',desc:'Count words, characters, sentences and reading time.',
 state:{},
 stats(s){const w=(s.match(/[\p{L}\p{N}][\p{L}\p{N}'’\-]*/gu)||[]),chars=[...s].length,nos=[...s.replace(/\s/g,'')].length,sent=(s.match(/[^.!?…]*[\p{L}\p{N}][^.!?…]*([.!?…]+|$)/gu)||[]).filter(x=>x.trim()).length,para=s.split(/\n\s*\n/).filter(p=>p.trim()).length;
  const stop=new Set('the a an and or but of to in on at for with is are was were be been it this that as by from your you i we they he she his her their our not no so if then than too very can will just about into over also'.split(' '));const f={};w.forEach(x=>{const k=x.toLowerCase();if(k.length>2&&!stop.has(k))f[k]=(f[k]||0)+1});
  const top=Object.entries(f).sort((a,b)=>b[1]-a[1]).slice(0,5);return{words:w.length,chars,nos,sent,para,avg:w.length?w.reduce((a,b)=>a+b.length,0)/w.length:0,top}},
 dur(min){if(min<1)return Math.max(1,Math.round(min*60))+' sec';const m=Math.floor(min),s=Math.round((min-m)*60);return s?`${m} min ${s} sec`:`${m} min`},
 render(){return `<div class="inputs"><div class="field"><label for="wcx">Type or paste your text</label><textarea id="wcx" rows="8" placeholder="Paste your essay, article or post here…">Numbrik's word counter counts words, characters, sentences and paragraphs as you type. It also estimates reading and speaking time.</textarea></div>
  <p class="hint">Your text stays in your browser. It isn't sent anywhere or saved.</p></div><div class="result" id="out"></div>`},
 calc(){const x=this.stats($('#wcx').value);
  $('#out').innerHTML=`<span class="label">Word count</span><div class="big"><em>${num(x.words,0)}</em> words</div>${kv([['Characters',num(x.chars,0)],['Characters without spaces',num(x.nos,0)],['Sentences',num(x.sent,0)],['Paragraphs',num(x.para,0)],['Reading time (238 wpm)',this.dur(x.words/238)],['Speaking time (140 wpm)',this.dur(x.words/140)],['Average word length',num(x.avg,1)+' letters'],...(x.top.length?[['Top keywords',x.top.map(([k,n])=>`${k} (${n})`).join(', ')]]:[])])}${copyBtn}`;
  return `${x.words} words, ${x.chars} characters`}},

{id:'charcount',cat:'Students',name:'Character counter',kw:'character counter letter count characters with spaces without spaces twitter x character limit 280 sms 160 meta description length instagram caption limit',desc:'Count characters with and without spaces, against common limits.',
 state:{},
 L:[['X (Twitter) post',280],['SMS text message',160],['Google title tag (approx.)',60],['Meta description (approx.)',155],['Instagram caption',2200],['LinkedIn post',3000],['YouTube title',100],['TikTok caption',4000]],
 render(){return `<div class="inputs"><div class="field"><label for="ccx">Type or paste your text</label><textarea id="ccx" rows="6" placeholder="Paste your text here…">Count characters, letters and words instantly, and see how your text fits X, SMS, Instagram and Google limits.</textarea></div>
  <p class="hint">Emoji and accented letters count as one character each. Your text stays in your browser.</p></div><div class="result" id="out"></div>`},
 calc(){const s=$('#ccx').value,ch=[...s].length,nos=[...s.replace(/\s/g,'')].length,let_=(s.match(/\p{L}/gu)||[]).length,words=(s.match(/[\p{L}\p{N}][\p{L}\p{N}'’\-]*/gu)||[]).length;
  const bar=(n,l)=>{const p=Math.min(100,n/l*100),over=n>l;return `<span style="display:inline-block;width:70px;height:8px;border-radius:4px;background:var(--line);vertical-align:middle;margin-right:6px;overflow:hidden"><span style="display:block;height:100%;width:${p}%;background:${over?'#d64545':'var(--accent)'}"></span></span>${over?`<strong style="color:#d64545">${n-l} over</strong>`:`${l-n} left`}`};
  $('#out').innerHTML=`<span class="label">Characters</span><div class="big"><em>${num(ch,0)}</em> characters</div>${kv([['Without spaces',num(nos,0)],['Letters only',num(let_,0)],['Words',num(words,0)],...this.L.map(([n,l])=>[`${n} · ${num(l,0)}`,bar(ch,l)])])}${copyBtn}`;
  return `${ch} characters (${nos} without spaces), ${words} words`}},

{id:'timedec',cat:'Work & pay',name:'Time to decimal calculator',kw:'time to decimal calculator convert hours and minutes to decimal hours decimal to time minutes to decimal payroll timesheet 7:45 to decimal decimal hours to hours and minutes',desc:'Convert hours and minutes to decimal hours and back.',
 state:{mode:'t2d'},
 render(){const s=this.state;return `<div class="inputs"><div class="row">${seg('tdm',[['t2d','Time → decimal'],['d2t','Decimal → time']],s.mode)}</div>
  <div class="row">${s.mode==='t2d'?field('tdh','Hours',7,{unit:'h'})+field('tdn','Minutes',45,{unit:'min'})+field('tds2','Seconds',0,{unit:'sec'}):field('tdd','Decimal hours',7.75,{unit:'h',step:0.01})}</div>
  <p class="hint">${s.mode==='t2d'?'Decimal hours = hours + minutes ÷ 60 + seconds ÷ 3,600.':'Minutes = the decimal part × 60. 7.75 hours is 7 hours and 0.75 × 60 = 45 minutes.'}</p></div><div class="result" id="out"></div>`},
 calc(){const s=this.state;let H;if(s.mode==='t2d'){H=(v('tdh')||0)+(v('tdn')||0)/60+(v('tds2')||0)/3600}else H=v('tdd');
  if(!(H>=0)||!isFinite(H)){$('#out').innerHTML='<span class="label">Result</span><p class="hint">Enter a time or a decimal number of hours.</p>';return''}
  const tot=Math.round(H*3600),h=Math.floor(tot/3600),m=Math.floor(tot%3600/60),sec=tot%60,hm=`${h}:${String(m).padStart(2,'0')}${sec?':'+String(sec).padStart(2,'0'):''}`;
  const tz=x=>x.includes('.')?x.replace(/\.?0+$/,''):x,main=s.mode==='t2d'?tz(num(H,4))+' hours':`${h} h ${m} min${sec?` ${sec} s`:''}`;
  $('#out').innerHTML=`<span class="label">${s.mode==='t2d'?'Decimal hours':'Hours and minutes'}</span><div class="big"><em>${main}</em></div>${kv([['Decimal hours',tz(num(H,4))],['Hours : minutes',hm],['Total minutes',tz(num(H*60,2))],['Total seconds',num(tot,0)],['Decimal (2 places, for payroll)',H.toFixed(2)]])}${copyBtn}`;
  return `${hm} = ${H.toFixed(2)} hours`},
 after(){bindSeg('tdm',x=>{this.state.mode=x;open('timedec')})}},

{id:'pctchange',cat:'Math',name:'Percent change calculator',kw:'percent change calculator percentage increase calculator percentage decrease calculator percent difference increase by percent decrease by percent growth rate',desc:'Percentage increase or decrease between two numbers.',
 state:{mode:'chg'},
 render(){const s=this.state;return `<div class="inputs"><div class="row">${seg('pcm',[['chg','% change between two values'],['inc','Increase by %'],['dec','Decrease by %']],s.mode)}</div>
  <div class="row">${s.mode==='chg'?field('pca','Old value (from)',80,{})+field('pcb','New value (to)',100,{}):field('pca','Starting value',80,{})+field('pcp',s.mode==='inc'?'Increase by':'Decrease by',25,{unit:'%'})}</div></div><div class="result" id="out"></div>`},
 calc(){const s=this.state,a=v('pca');
  if(s.mode==='chg'){const b=v('pcb');if(!isFinite(a)||!isFinite(b)||a===0){$('#out').innerHTML=`<span class="label">Percent change</span><p class="hint">${a===0?'Percent change from zero is undefined. Use a starting value other than 0.':'Enter both values.'}</p>`;return''}
   const c=(b-a)/Math.abs(a)*100,d=Math.abs(a-b)/((Math.abs(a)+Math.abs(b))/2)*100,word=c>0?'increase':c<0?'decrease':'no change';
   $('#out').innerHTML=`<span class="label">Percent change</span><div class="big"><em>${c>0?'+':''}${num(c,2)}%</em></div><p class="answer">${c===0?`Going from ${num(a,4)} to ${num(b,4)} is no change.`:`Going from ${num(a,4)} to ${num(b,4)} is a ${num(Math.abs(c),2)}% ${word}.`}</p>${kv([['Change',`${b-a>0?'+':''}${num(b-a,4)}`],['Percent difference (symmetric)',num(d,2)+'%'],['New value as % of old',num(b/a*100,2)+'%'],['Multiplier',`× ${num(b/a,4)}`]])}${copyBtn}`;
   return `${num(a,4)} → ${num(b,4)}: ${c>0?'+':''}${num(c,2)}%`}
  const p=v('pcp');if(!isFinite(a)||!isFinite(p)){$('#out').innerHTML='<span class="label">Result</span><p class="hint">Enter a value and a percentage.</p>';return''}
  const r=s.mode==='inc'?a*(1+p/100):a*(1-p/100);
  $('#out').innerHTML=`<span class="label">Result</span><div class="big"><em>${num(r,4)}</em></div><p class="answer">${num(a,4)} ${s.mode==='inc'?'increased':'decreased'} by ${num(p,2)}% is ${num(r,4)}.</p>${kv([['Amount of change',num(Math.abs(r-a),4)],['Multiplier',`× ${num(r/a||0,4)}`],['To get back to the start',`${s.mode==='inc'?'decrease':'increase'} by ${num(Math.abs(a/r-1)*100,2)}%`]])}${copyBtn}`;
  return `${num(a,4)} ${s.mode==='inc'?'+':'−'} ${num(p,2)}% = ${num(r,4)}`},
 after(){bindSeg('pcm',x=>{this.state.mode=x;open('pctchange')})}},
{id:'lease',cat:'Money',name:'Car lease calculator',kw:'car lease calculator lease payment calculator money factor residual value capitalized cost auto lease monthly payment lease vs buy',desc:'Monthly car lease payment from price, residual and money factor.',
 state:{},
 render(){const c=R().cur;return `<div class="inputs"><div class="row">${field('lsm','MSRP (sticker price)',40000,{unit:c})}${field('lsp','Negotiated price',37500,{unit:c})}${field('lsd','Down payment + trade-in',3000,{unit:c})}</div>
  <div class="row">${field('lst','Lease term',36,{unit:'months'})}${field('lsr','Residual value',58,{unit:'% of MSRP'})}${field('lsa','Interest rate (APR)',6,{unit:'%'})}</div>
  <div class="row">${field('lsf','Fees added to the lease',995,{unit:c})}${field('lsx','Sales tax on payment',7,{unit:'%'})}</div>
  <p class="hint">Dealers quote the rate as a money factor: money factor = APR ÷ 2,400, so 6% APR is 0.0025. Most US states tax the monthly payment, not the whole car.</p></div><div class="result" id="out"></div>`},
 calc(){const g=id=>v(id)||0,msrp=g('lsm'),price=g('lsp'),down=g('lsd'),n=Math.round(g('lst')),rp=g('lsr'),apr=g('lsa'),fees=g('lsf'),tx=g('lsx')/100;
  if(!(msrp>0&&price>0&&n>0&&rp>0)){$('#out').innerHTML='<span class="label">Monthly lease payment</span><p class="hint">Enter the price, term and residual value.</p>';return''}
  const cap=price+fees-down,res=msrp*rp/100,mf=apr/2400,dep=(cap-res)/n,fin=(cap+res)*mf,base=dep+fin,tax=base*tx,pm=base+tax,tot=pm*n+down;
  if(cap<=res){$('#out').innerHTML='<span class="label">Monthly lease payment</span><p class="hint">The capitalized cost is below the residual value. Check the price, down payment and residual.</p>';return''}
  $('#out').innerHTML=`<span class="label">Monthly lease payment</span><div class="big"><em>${money(pm)}</em></div><p class="answer">${money(pm)} a month for ${n} months, ${money(tot,0)} in total including your ${money(down,0)} down.</p>${kv([['Depreciation part',money(dep)],['Finance (rent) charge',money(fin)],['Sales tax',money(tax)],['Money factor',mf.toFixed(5)],['Residual (buyout) value',money(res,0)],['Net capitalized cost',money(cap,0)],['Total cost of the lease',money(tot,0)]])}${copyBtn}`;
  return `Lease payment ${money(pm)}/month for ${n} months`}},

{id:'retire',cat:'Money',name:'Retirement calculator',kw:'retirement calculator how much will i have at retirement 401k calculator retirement savings calculator 4% rule how much do i need to retire nest egg',desc:'Projected retirement savings and income.',
 state:{},
 render(){const c=R().cur;return `<div class="inputs"><div class="row">${field('rta','Current age',35,{unit:'yrs'})}${field('rtr','Retirement age',67,{unit:'yrs'})}${field('rts','Current savings',50000,{unit:c})}</div>
  <div class="row">${field('rtm','Monthly contribution',800,{unit:c})}${field('rtg','Expected annual return',6,{unit:'%'})}${field('rti','Inflation',2.5,{unit:'%'})}</div>
  <div class="row">${field('rtx','Contribution increase per year',2,{unit:'%'})}${field('rtw','Withdrawal rate in retirement',4,{unit:'%'})}</div>
  <p class="hint">Returns aren't guaranteed. 6% is a common long-run assumption for a diversified stock and bond mix; use a lower number to be cautious.</p><div id="rttab" class="tc-wrap"></div></div><div class="result" id="out"></div>`},
 calc(){const g=id=>v(id)||0,a=Math.round(g('rta')),r=Math.round(g('rtr')),s=g('rts'),m=g('rtm'),ret=g('rtg')/100,inf=g('rti')/100,inc=g('rtx')/100,wr=g('rtw')/100,tab=$('#rttab');
  if(!(r>a&&a>0)){$('#out').innerHTML='<span class="label">At retirement</span><p class="hint">Retirement age must be later than your current age.</p>';tab.innerHTML='';return''}
  const mr=Math.pow(1+ret,1/12)-1;let b=s,c=m,contrib=s,rows=[];for(let y=1;y<=r-a;y++){for(let k=0;k<12;k++){b=b*(1+mr)+c;contrib+=c}if(y%5===0||y===r-a)rows.push(`<tr><td>${a+y}</td><td class="num">${money(contrib,0)}</td><td class="num">${money(b,0)}</td><td class="num">${money(b/Math.pow(1+inf,y),0)}</td></tr>`);c*=1+inc}
  const real=b/Math.pow(1+inf,r-a),inc1=b*wr;
  tab.innerHTML=`<table><thead><tr><th>Age</th><th>Total contributed</th><th>Balance</th><th>In today's money</th></tr></thead><tbody>${rows.join('')}</tbody></table>`;
  $('#out').innerHTML=`<span class="label">Savings at age ${r}</span><div class="big"><em>${money(b,0)}</em></div><p class="answer">That's about ${money(real,0)} in today's money, enough for roughly ${money(inc1/12,0)} a month (${money(inc1/12/Math.pow(1+inf,r-a),0)} in today's money) at a ${num(wr*100,1)}% withdrawal rate.</p>${kv([['Total you contribute',money(contrib,0)],['Investment growth',money(b-contrib,0)],[`Yearly income at ${num(wr*100,1)}%`,money(inc1,0)],['Years until retirement',String(r-a)]])}${copyBtn}`;
  return `About ${money(b,0)} at ${r} (${money(real,0)} in today's money)`}},

{id:'savings',cat:'Money',name:'Savings calculator',kw:'savings calculator how much will my savings grow high yield savings calculator monthly deposit interest savings goal calculator how much to save each month',desc:'How savings grow with deposits and interest, or what to save for a goal.',
 state:{mode:'grow'},
 render(){const s=this.state,c=R().cur;return `<div class="inputs"><div class="row">${seg('svm',[['grow','How much will I have?'],['goal','How much to save each month?']],s.mode)}</div>
  <div class="row">${field('svi','Starting balance',5000,{unit:c})}${s.mode==='grow'?field('svd','Monthly deposit',300,{unit:c}):field('svg','Savings goal',25000,{unit:c})}</div>
  <div class="row">${field('svr','Interest rate (APY)',4.25,{unit:'%'})}${field('svy','Time',5,{unit:'years'})}</div><div id="svtab" class="tc-wrap"></div></div><div class="result" id="out"></div>`},
 calc(){const s=this.state,P=v('svi')||0,apy=(v('svr')||0)/100,yrs=v('svy'),n=Math.round(yrs*12),tab=$('#svtab');
  if(!(n>0)){$('#out').innerHTML='<span class="label">Savings</span><p class="hint">Enter how many years you will save.</p>';tab.innerHTML='';return''}
  const r=Math.pow(1+apy,1/12)-1,fv=(d)=>{let b=P,rows=[];for(let k=1;k<=n;k++){b=b*(1+r)+d;if(k%12===0)rows.push([k/12,b,P+d*k])}return[b,rows]};
  let d;if(s.mode==='goal'){const G=v('svg')||0,grow=P*Math.pow(1+r,n),fac=r?(Math.pow(1+r,n)-1)/r:n;d=Math.max(0,(G-grow)/fac)}else d=v('svd')||0;
  const [b,rows]=fv(d),dep=P+d*n;tab.innerHTML=rows.length?`<table><thead><tr><th>Year</th><th>Deposited</th><th>Interest earned</th><th>Balance</th></tr></thead><tbody>${rows.map(([y,bb,dd])=>`<tr><td>${y}</td><td class="num">${money(dd,0)}</td><td class="num">${money(bb-dd,0)}</td><td class="num">${money(bb,0)}</td></tr>`).join('')}</tbody></table>`:'';
  if(s.mode==='goal'){$('#out').innerHTML=`<span class="label">Save each month</span><div class="big"><em>${money(d)}</em></div><p class="answer">Saving ${money(d)} a month for ${num(yrs,1)} years at ${num(apy*100,2)}% APY grows ${money(P,0)} to ${money(b,0)}.</p>${kv([['Total deposited',money(dep,0)],['Interest earned',money(b-dep,0)]])}${copyBtn}`;return `Save ${money(d)} a month`}
  $('#out').innerHTML=`<span class="label">Balance after ${num(yrs,1)} years</span><div class="big"><em>${money(b,0)}</em></div>${kv([['Total deposited',money(dep,0)],['Interest earned',money(b-dep,0)],['Interest in the final year',rows.length>1?money(rows[rows.length-1][1]-rows[rows.length-2][1]-d*12,0):money(b-dep,0)]])}${copyBtn}`;
  return `${money(b,0)} after ${num(yrs,1)} years`},
 after(){bindSeg('svm',x=>{this.state.mode=x;open('savings')})}},

{id:'studentloan',cat:'Money',name:'Student loan calculator',kw:'student loan calculator student loan payment calculator federal student loan repayment 10 year standard extended plan payoff extra payments student loan interest',desc:'Student loan payment, total interest and payoff with extra payments.',
 state:{},
 pm(P,r,n){return r?P*r/(1-Math.pow(1+r,-n)):P/n},
 render(){const c=R().cur;return `<div class="inputs"><div class="row">${field('sla','Loan balance',30000,{unit:c})}${field('slr','Interest rate',6.5,{unit:'%'})}${field('slt','Repayment term',10,{unit:'years'})}</div>
  <div class="row">${field('slx','Extra payment per month',0,{unit:c})}</div>
  <p class="hint">The federal Standard Repayment Plan is 10 years. Income-driven plans base the payment on income instead and aren't modelled here.</p></div><div class="result" id="out"></div>`},
 calc(){const P=v('sla'),r=(v('slr')||0)/1200,yrs=v('slt'),n=Math.round(yrs*12),x=Math.max(0,v('slx')||0);
  if(!(P>0&&n>0)){$('#out').innerHTML='<span class="label">Monthly payment</span><p class="hint">Enter the balance, rate and term.</p>';return''}
  const pm=this.pm(P,r,n),base=pm*n-P;let b=P,k=0,ti=0;while(b>0.005&&k<600){const i=b*r;b-=Math.min(b,pm+x-i);ti+=i;k++}
  const alt=[[10,'10-year standard'],[20,'20 years'],[25,'25-year extended']].filter(([y])=>y!==yrs).map(([y,l])=>[`${l}`,`${money(this.pm(P,r,y*12))}/mo, ${money(this.pm(P,r,y*12)*y*12-P,0)} interest`]);
  const rows=[['Total interest',money(ti,0)],['Total paid',money(P+ti,0)],['Payoff time',`${Math.floor(k/12)} yrs ${k%12} mos`],['Interest in the first month',money(P*r)]];if(x>0)rows.push(['Saved with extra payments',`${money(base-ti,0)} and ${n-k} months`]);
  $('#out').innerHTML=`<span class="label">Monthly payment</span><div class="big"><em>${money(pm)}</em></div>${kv(rows.concat(alt))}${copyBtn}`;
  return `Student loan payment ${money(pm)}/month, ${money(ti,0)} interest`}},

{id:'rentbuy',cat:'Money',name:'Rent vs buy calculator',kw:'rent vs buy calculator should i rent or buy a house buying vs renting calculator is it better to rent or buy cost of owning vs renting',desc:'Compare the true cost of renting and buying over time.',
 state:{},
 render(){const c=R().cur;return `<div class="inputs"><div class="row">${field('rbp','Home price',400000,{unit:c})}${field('rbd','Down payment',20,{unit:'%'})}${field('rbr','Mortgage rate',6.5,{unit:'%'})}${field('rby','Years you’ll stay',7,{unit:'yrs'})}</div>
  <div class="row">${field('rbt','Property tax',1.1,{unit:'%/yr'})}${field('rbi','Insurance + HOA',2400,{unit:c+'/yr'})}${field('rbm','Maintenance',1,{unit:'%/yr'})}${field('rba','Home price growth',3,{unit:'%/yr'})}</div>
  <div class="row">${field('rbn','Monthly rent',2200,{unit:c})}${field('rbg','Rent increase',3,{unit:'%/yr'})}${field('rbo','Investment return',5,{unit:'%/yr'})}</div>
  <p class="hint">Assumes a 30-year fixed mortgage, 3% closing costs to buy and 6% selling costs. The down payment and closing costs are counted as money that could otherwise be invested.</p></div><div class="result" id="out"></div>`},
 calc(){const g=id=>v(id)||0,H=g('rbp'),dp=g('rbd')/100,rate=g('rbr')/1200,Y=Math.round(g('rby')),tx=g('rbt')/100,ins=g('rbi'),mt=g('rbm')/100,ap=g('rba')/100,rent=g('rbn'),rg=g('rbg')/100,inv=g('rbo')/100;
  if(!(H>0&&Y>0&&rent>0)){$('#out').innerHTML='<span class="label">Rent vs buy</span><p class="hint">Enter the home price, rent and years.</p>';return''}
  const down=H*dp,L=H-down,n=360,pm=rate?L*rate/(1-Math.pow(1+rate,-n)):L/n,close=H*0.03;let bal=L,own=down+close,val=H,rentT=0,rr=rent;
  for(let y=0;y<Y;y++){for(let k=0;k<12;k++){const i=bal*rate;bal-=pm-i;own+=pm}own+=val*tx+ins+val*mt;val*=1+ap;rentT+=rr*12;rr*=1+rg}
  const equity=val*0.94-bal,opp=(down+close)*(Math.pow(1+inv,Y)-1),buyNet=own-equity+opp,diff=rentT-buyNet,better=diff>0?'Buying':'Renting';
  $('#out').innerHTML=`<span class="label">Over ${Y} years</span><div class="big"><em>${better}</em> comes out ${money(Math.abs(diff),0)} ahead</div><p class="answer">Buying costs about ${money(buyNet,0)} net over ${Y} years after selling, versus ${money(rentT,0)} in rent.</p>${kv([['Mortgage payment (P&I)',money(pm,0)+'/mo'],['Total spent owning',money(own,0)],['Equity when you sell (after 6% costs)',money(equity,0)],['Lost investment return on down payment',money(opp,0)],['Net cost of buying',money(buyNet,0)],['Total rent paid',money(rentT,0)],['Home value after '+Y+' years',money(val,0)]])}${copyBtn}`;
  return `${better} is about ${money(Math.abs(diff),0)} cheaper over ${Y} years`}}
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
const SLUGS={timecard:'time-card-calculator',hours:'hours-calculator',salary:'hourly-to-salary-calculator',tip:'tip-calculator',percent:'percentage-calculator',loan:'mortgage-calculator',bmi:'bmi-calculator',sleep:'sleep-calculator',age:'age-calculator',days:'days-between-dates',convert:'unit-converter',calorie:'calorie-calculator',gpa:'gpa-calculator',autoloan:'auto-loan-calculator',dice:'dice-roller',lcm:'lcm-calculator',gcf:'gcf-calculator',sqft:'square-footage-calculator',concrete:'concrete-calculator',paint:'paint-calculator',fraction:'fraction-calculator',random:'random-number-generator',coin:'coin-flip',grade:'grade-calculator',finalgrade:'final-grade-calculator',scientific:'scientific-calculator',fraction:'fraction-calculator',stdev:'standard-deviation-calculator',compound:'compound-interest-calculator',salestax:'sales-tax-calculator',duedate:'due-date-calculator',bodyfat:'body-fat-calculator',password:'password-generator',bmr:'bmr-calculator',ratio:'ratio-calculator',slope:'slope-calculator',protein:'protein-calculator',onerm:'one-rep-max-calculator',macro:'macro-calculator',pace:'pace-calculator',average:'average-calculator',triangle:'right-triangle-calculator',quadratic:'quadratic-formula-calculator',cd:'cd-calculator',halfbday:'half-birthday-calculator',military:'military-time-converter',raise:'pay-raise-calculator',water:'water-intake-calculator',mulch:'mulch-calculator',workdays:'working-days-calculator',turkey:'turkey-calculator',soh:'save-our-homes-calculator',shoe:'shoe-size-converter',discount:'discount-calculator',tdee:'tdee-calculator',idealweight:'ideal-weight-calculator',roman:'roman-numeral-converter',simpleint:'simple-interest-calculator',tile:'tile-calculator',longdiv:'long-division-calculator',zscore:'z-score-calculator',margin:'margin-calculator',fuel:'gas-cost-calculator',gravel:'gravel-calculator',stair:'stair-calculator',period:'period-calculator',love:'love-calculator',rmd:'rmd-calculator',rounding:'rounding-calculator',timezone:'time-zone-converter',height:'height-calculator',deficit:'calorie-deficit-calculator',bac:'bac-calculator',bra:'bra-size-calculator',numerology:'life-path-number-calculator',gloan:'loan-calculator',datecalc:'date-calculator',afford:'house-affordability-calculator',wordcount:'word-counter',charcount:'character-counter',timedec:'time-to-decimal-calculator',pctchange:'percent-change-calculator',lease:'car-lease-calculator',retire:'retirement-calculator',savings:'savings-calculator',studentloan:'student-loan-calculator',rentbuy:'rent-vs-buy-calculator'};
let cur=null,lastText='';
function update(){if(!cur)return;try{lastText=cur.calc()||''}catch(e){lastText=''}
  const c=$('#copyRes');if(c)c.onclick=()=>{const done=()=>{c.textContent='Copied';setTimeout(()=>c.textContent='Copy result',1400)};try{navigator.clipboard.writeText(lastText).then(done,()=>{c.textContent=lastText})}catch(e){c.textContent=lastText}}}
function open(id){const t=TOOLS.find(x=>x.id===id),body=$('#toolBody');if(!t||!body)return;cur=t;
  body.innerHTML=t.render();body.querySelectorAll('input,select,textarea').forEach(e=>e.addEventListener('input',update));
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
/* copy embed code */
document.querySelectorAll('[data-copy]').forEach(b=>b.addEventListener('click',()=>{const t=document.getElementById(b.dataset.copy);if(!t)return;t.select();const done=()=>{const o=b.textContent;b.textContent='Copied!';setTimeout(()=>b.textContent=o,1600)};if(navigator.clipboard)navigator.clipboard.writeText(t.value).then(done,()=>{document.execCommand('copy');done()});else{document.execCommand('copy');done()}}));
/* holiday countdowns */
const HOL={christmas:[12,25],halloween:[10,31],newyear:[1,1],valentines:[2,14],july4:[7,4]};
const nthDow=(y,m,dow,n)=>{const d=new Date(y,m-1,1);return new Date(y,m-1,1+((dow-d.getDay()+7)%7)+7*(n-1))};
function easterDate(y){const a=y%19,b=Math.floor(y/100),c=y%100,d=Math.floor(b/4),e=b%4,f=Math.floor((b+8)/25),g=Math.floor((b-f+1)/3),h=(19*a+b-d-g+15)%30,i=Math.floor(c/4),k=c%4,l=(32+2*e+2*i-h-k)%7,m=Math.floor((a+11*h+22*l)/451),x=h+l-7*m+114;return new Date(y,Math.floor(x/31)-1,x%31+1)}
function holDate(k,y){if(HOL[k])return new Date(y,HOL[k][0]-1,HOL[k][1]);if(k==='thanksgiving')return nthDow(y,11,4,4);if(k==='blackfriday'){const t=nthDow(y,11,4,4);t.setDate(t.getDate()+1);return t}if(k==='mothers')return nthDow(y,5,0,2);if(k==='fathers')return nthDow(y,6,0,3);if(k==='easter')return easterDate(y);const r=HOL2[k];if(!r)return null;if(r[0]==='f')return new Date(y,r[1]-1,r[2]);if(r[0]==='n')return nthDow(y,r[1],r[2],r[3]);const d=new Date(y,r[1],0);d.setDate(d.getDate()-((d.getDay()-r[2]+7)%7));return d}
const HOL2={christmaseve:['f',12,24],newyearseve:['f',12,31],stpatricks:['f',3,17],juneteenth:['f',6,19],veterans:['f',11,11],canadaday:['f',7,1],boxingday:['f',12,26],australiaday:['f',1,26],mlk:['n',1,1,3],presidents:['n',2,1,3],laborday:['n',9,1,1],cathanksgiving:['n',10,1,2],dstend:['n',11,0,1],dststart:['n',3,0,2],memorial:['l',5,1]};
function nextHol(k){const n=new Date(),t=new Date(n.getFullYear(),n.getMonth(),n.getDate());let d=holDate(k,t.getFullYear());if(d<t)d=holDate(k,t.getFullYear()+1);return{d,t,days:Math.round((d-t)/864e5)}}
function tickCountdowns(){document.querySelectorAll('[data-countdown]').forEach(el=>{const k=el.dataset.countdown,x=nextHol(k);if(!x.d)return;
  if(!el.classList.contains('cd')){el.textContent=x.days;return}
  const q=s=>el.querySelector(s);q('.cd-days').textContent=x.days===0?'Today!':x.days;q('.cd-unit').textContent=x.days===0?'':x.days===1?'day':'days';
  q('.cd-date').textContent=x.d.toLocaleDateString(R().loc,{weekday:'long',year:'numeric',month:'long',day:'numeric'});
  {const w=Math.floor(x.days/7),r=x.days%7;q('.cd-weeks').textContent=`${w} ${w===1?'week':'weeks'}, ${r} ${r===1?'day':'days'}`}
  let wd=0;for(let i=1;i<=x.days;i++){const dd=new Date(x.t);dd.setDate(dd.getDate()+i);const g=dd.getDay();if(g&&g<6)wd++}q('.cd-wd').textContent=wd;
  const ms=x.d-new Date();if(x.days===0){q('.cd-live').textContent='It’s here. Enjoy the day!'}else{const s=Math.max(0,Math.floor(ms/1000));q('.cd-live').textContent=`${Math.floor(s/86400)} days, ${Math.floor(s%86400/3600)} hours, ${Math.floor(s%3600/60)} minutes, ${s%60} seconds`}})}

/* days from today */
const longD=d=>d.toLocaleDateString(R().loc,{weekday:'long',year:'numeric',month:'long',day:'numeric'});
const plusDays=n=>{const t=new Date();return new Date(t.getFullYear(),t.getMonth(),t.getDate()+n)};
const plusBiz=n=>{const d=plusDays(0);let k=Math.abs(n);const s=n<0?-1:1;while(k){d.setDate(d.getDate()+s);const g=d.getDay();if(g&&g<6)k--}return d};
document.querySelectorAll('.afd').forEach(el=>{const n=+el.dataset.add,q=s=>el.querySelector(s),d=plusDays(n);
  q('.afd-date').textContent=longD(d);q('.afd-from').textContent='Counting from today, '+longD(plusDays(0));
  q('.afd-short').textContent=d.toLocaleDateString(R().loc);q('.afd-biz').textContent=longD(plusBiz(n));q('.afd-ago').textContent=longD(plusDays(-n))});
document.querySelectorAll('.afd-hols').forEach(ul=>{const lim=plusDays(+ul.dataset.add);let any=0;const lis=[...ul.querySelectorAll('li')].map(li=>{const x=nextHol(li.dataset.hk);const ok=x.d&&x.d>x.t&&x.d<=lim;li.hidden=!ok;if(ok){any++;li.querySelector('.afd-hd').textContent=x.d.toLocaleDateString(R().loc,{month:'short',day:'numeric'})}return[x.d,li]});lis.sort((p,q)=>p[0]-q[0]).forEach(([,li])=>ul.appendChild(li));const none=ul.nextElementSibling;if(none)none.hidden=!!any});
document.querySelectorAll('.afd-ago-x').forEach(e=>{e.textContent=longD(plusDays(-e.dataset.add))});
document.querySelectorAll('.afd-mini').forEach(el=>{el.textContent=longD(plusDays(+el.dataset.add))});
const afdN=$('#afdN');if(afdN){const run=()=>{const n=Math.round((parseFloat(afdN.value)||0)*(+$('#afdU').value));if(Math.abs(n)>100000)return;$('#afdOut').textContent=longD(plusDays(n));$('#afdBiz').textContent=longD(plusBiz(n));$('#afdAgo').textContent=longD(plusDays(-n))};afdN.addEventListener('input',run);$('#afdU').addEventListener('input',run);run()}
if(document.querySelector('[data-countdown]')){tickCountdowns();if(document.querySelector('.cd'))setInterval(tickCountdowns,1000)}

})();
