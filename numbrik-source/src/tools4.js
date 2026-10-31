
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
  else if(k==='='){if(!s.expr)return;try{const v=this.evalx(this.closed(s.expr));s.hist.unshift([this.closed(s.expr),this.fmt(v)]);s.hist=s.hist.slice(0,5);s.ans=v;s.last=v;s.expr=''}catch(e){s.last='Error'}}
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
  <div class="row">${field('bfh','Height',I?69:175,{unit:u})}${field('bfw','Weight',I?(m?180:150):(m?82:68),{unit:w})}</div>
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
