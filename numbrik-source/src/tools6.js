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
