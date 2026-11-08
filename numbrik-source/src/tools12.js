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
