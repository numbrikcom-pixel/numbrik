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
