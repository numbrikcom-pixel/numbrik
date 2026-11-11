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
