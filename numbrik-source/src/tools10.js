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
