
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
 after(){$('#cfgo').onclick=()=>{this.flip();update()}}}
