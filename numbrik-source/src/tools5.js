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
