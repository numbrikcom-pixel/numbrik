{id:'vadisab',cat:'Money',name:'VA disability calculator',kw:'va disability calculator va rating calculator combined rating va math veterans compensation 2026 pay chart dependents spouse children bilateral',desc:'Combined VA rating and monthly pay for 2026.',
 state:{sp:'no',aa:'no'},
 // Monthly rates effective Dec 1, 2025 (2.8% COLA). Index 0 = 10% ... 9 = 100%. Dependent columns start at 30%.
 RT:{a:[180.42,356.66,552.47,795.84,1132.90,1435.02,1808.45,2102.15,2362.30,3938.58],s:[617.47,882.84,1241.90,1566.02,1961.45,2277.15,2559.30,4158.17],sc:[666.47,947.84,1322.90,1663.02,2074.45,2406.15,2704.30,4318.99],c:[596.47,853.84,1205.90,1523.02,1910.45,2219.15,2494.30,4085.43],
  k:[32,43,54,65,76,87,98,109.11],sch:[105,140,176,211,246,281,317,352.45],aa:[61,81,101,121,141,161,181,201.41]},
 usd(n){return new Intl.NumberFormat('en-US',{style:'currency',currency:'USD'}).format(n)},
 render(){const s=this.state;return `<div class="inputs"><div class="row">${field('vrr','Your individual VA ratings (%), separated by commas','50, 30, 10',{type:'text'})}</div>
  <div class="row"><div class="field"><label>Spouse</label>${seg('vsp',[['no','No spouse'],['yes','Married']],s.sp)}</div>${s.sp==='yes'?`<div class="field"><label>Spouse needs Aid &amp; Attendance</label>${seg('vaa',[['no','No'],['yes','Yes']],s.aa)}</div>`:''}</div>
  <div class="row">${field('vk','Children under 18',0,{step:1})}${field('vks','Children 18–23 in school',0,{step:1})}</div>
  <p class="hint">2026 rates, effective December 1, 2025. Dependents add pay only at a combined rating of 30% or more. An estimate, not a VA decision.</p></div><div class="result" id="out"></div>`},
 calc(){const s=this.state,rs=($('#vrr').value.match(/\d+(\.\d+)?/g)||[]).map(Number).filter(x=>x>0&&x<=100).sort((a,b)=>b-a);
  if(!rs.length){$('#out').innerHTML='<span class="label">Combined rating</span><p class="hint">Enter at least one rating, like 50, 30, 10.</p>';return''}
  let eff=0;const steps=[];for(const r of rs){const before=eff;eff=Math.round(eff+(100-eff)*r/100);steps.push([`${r}% of the remaining ${100-before}%`,`${before}% → ${eff}%`])}
  const comb=Math.min(100,Math.round(eff/10)*10),i=comb/10-1,R=this.RT;let pay=comb>=10?R.a[i]:0,dep=[];
  const k=Math.max(0,Math.floor(v('vk')||0)),ks=Math.max(0,Math.floor(v('vks')||0)),kids=k+ks;
  if(comb>=30){const j=i-2;const sp=s.sp==='yes';
   if(sp&&kids)pay=R.sc[j];else if(sp)pay=R.s[j];else if(kids)pay=R.c[j];
   if(kids){const extraU18=Math.max(0,k-1),extraSch=k>=1?ks:Math.max(0,ks-1);pay+=extraU18*R.k[j]+extraSch*R.sch[j];if(extraU18)dep.push([`${extraU18} more child${extraU18>1?'ren':''} under 18`,'+'+this.usd(extraU18*R.k[j])]);if(extraSch)dep.push([`${extraSch} more child${extraSch>1?'ren':''} in school`,'+'+this.usd(extraSch*R.sch[j])])}
   if(sp&&s.aa==='yes'){pay+=R.aa[j];dep.push(['Spouse Aid & Attendance','+'+this.usd(R.aa[j])])}}
  const note=comb<30&&(s.sp==='yes'||kids)?'<p class="hint">At 10% and 20%, VA pays the same amount with or without dependents.</p>':'';
  $('#out').innerHTML=`<span class="label">Combined VA rating</span><div class="big"><em>${comb}%</em></div><p class="answer">Your ratings combine to ${eff}%, which VA rounds to <strong>${comb}%</strong>. That pays about <strong>${this.usd(pay)} a month</strong> (${this.usd(pay*12)} a year), tax-free.</p>${kv([['Exact combined value',eff+'%'],['Monthly payment',this.usd(pay)],['Yearly payment',this.usd(pay*12)],...dep])}${note}<div class="field"><label>How VA math combined your ratings</label></div>${kv(steps)}${copyBtn}`;
  return `VA combined rating ${comb}% — ${this.usd(pay)}/month`},
 after(){bindSeg('vsp',x=>{this.state.sp=x;open('vadisab')});if(this.state.sp==='yes')bindSeg('vaa',x=>{this.state.aa=x;update()})}},

{id:'timecalc',cat:'Dates & time',name:'Time calculator',kw:'time calculator add time subtract time hours minutes seconds add hours to a time duration calculator clock time plus minutes what time will it be',desc:'Add or subtract hours, minutes and seconds.',
 state:{m:'dur',op:'add'},
 parse(t){t=t.trim();if(!t)return null;let sg=1;if(/^[-−]/.test(t)){sg=-1;t=t.slice(1).trim()}else if(t[0]==='+')t=t.slice(1).trim();
  if(/^\d+(:\d{1,2}){1,2}$/.test(t)){const p=t.split(':').map(Number);return sg*(p[0]*3600+p[1]*60+(p[2]||0))}
  const re=/(\d+(?:\.\d+)?)\s*(h(?:ours?|rs?)?|m(?:in(?:ute)?s?)?|s(?:ec(?:ond)?s?)?)\b/gi;let m,tot=0,hit=false,rest=t;
  while(m=re.exec(t)){hit=true;const n=+m[1],u=m[2][0].toLowerCase();tot+=u==='h'?n*3600:u==='m'?n*60:n;rest=rest.replace(m[0],'')}
  if(hit&&!rest.trim())return sg*tot;if(/^\d+(\.\d+)?$/.test(t))return sg*(+t)*3600;return NaN},
 hms(x){const sg=x<0?'−':'';x=Math.abs(Math.round(x));const h=Math.floor(x/3600),m=Math.floor(x%3600/60),s=x%60;return sg+h+':'+String(m).padStart(2,'0')+(s?':'+String(s).padStart(2,'0'):'')},
 words(x){const sg=x<0?'minus ':'';x=Math.abs(Math.round(x));const h=Math.floor(x/3600),m=Math.floor(x%3600/60),s=x%60;return sg+[h?h+' hr':'',m?m+' min':'',s?s+' sec':''].filter(Boolean).join(' ')||'0 min'},
 render(){const s=this.state;return `<div class="inputs"><div class="row">${seg('tcm',[['dur','Add up durations'],['clock','Time of day ± hours']],s.m)}</div>
  ${s.m==='dur'?`<div class="field"><label for="tcl">One time per line (2:45, 1:30:20, 1h 15m, or −0:20 to subtract)</label><textarea id="tcl" rows="6">2:45\n1:30\n0:50\n-0:20</textarea></div>`
  :`<div class="row"><div class="field"><label for="tct">Start time</label><input id="tct" type="time" value="09:30" step="60"></div><div class="field"><label>Add or subtract</label>${seg('tco',[['add','Add'],['sub','Subtract']],s.op)}</div></div>
  <div class="row">${field('tch','Hours',8)}${field('tcmi','Minutes',45)}</div>`}</div><div class="result" id="out"></div>`},
 calc(){const s=this.state;
  if(s.m==='dur'){const ls=$('#tcl').value.split('\n').map(x=>x.trim()).filter(Boolean),vals=ls.map(x=>this.parse(x));const bad=ls.filter((x,i)=>!isFinite(vals[i]));const tot=vals.filter(isFinite).reduce((a,b)=>a+b,0);
   $('#out').innerHTML=`<span class="label">Total time</span><div class="big"><em>${this.hms(tot)}</em></div><p class="answer">${vals.filter(isFinite).length} times add up to <strong>${this.words(tot)}</strong>.</p>${kv([['Decimal hours',num(tot/3600,4)],['Total minutes',num(tot/60,2)],['Total seconds',num(tot,0)]])}${bad.length?`<p class="hint">Skipped (couldn't read): ${bad.map(x=>x.replace(/[<>&]/g,'')).join(', ')}</p>`:''}${copyBtn}`;
   return `Total ${this.hms(tot)} (${num(tot/3600,4)} hours)`}
  const [H,M]=($('#tct').value||'0:0').split(':').map(Number),d=((v('tch')||0)*60+(v('tcmi')||0))*(s.op==='add'?1:-1),t0=H*60+M,t1=t0+d,day=Math.floor(t1/1440),mm=((t1%1440)+1440)%1440;
  const fmt=x=>{const h=Math.floor(x/60),m=Math.round(x%60);return new Date(2026,0,1,h,m).toLocaleTimeString('en-US',{hour:'numeric',minute:'2-digit'})};
  const when=day===0?'the same day':day===1?'the next day':day===-1?'the day before':(day>0?day+' days later':(-day)+' days earlier');
  $('#out').innerHTML=`<span class="label">Result</span><div class="big"><em>${fmt(mm)}</em></div><p class="answer">${fmt(t0)} ${s.op==='add'?'plus':'minus'} ${this.words(Math.abs(d)*60)} is <strong>${fmt(mm)}</strong>, ${when}.</p>${kv([['24-hour clock',String(Math.floor(mm/60)).padStart(2,'0')+':'+String(Math.round(mm%60)).padStart(2,'0')],['Day',when]])}${copyBtn}`;
  return `${fmt(t0)} ${s.op==='add'?'+':'−'} ${this.words(Math.abs(d)*60)} = ${fmt(mm)} (${when})`},
 after(){bindSeg('tcm',x=>{this.state.m=x;open('timecalc')});if(this.state.m==='clock')bindSeg('tco',x=>{this.state.op=x;update()})}},

{id:'invoice',cat:'Work & pay',name:'Invoice generator',kw:'invoice generator free invoice maker invoice template freelance invoice pdf create invoice online bill generator small business',desc:'Make a professional invoice and save it as a PDF.',
 state:null,
 def(){const d=new Date(),iso=x=>x.toISOString().slice(0,10),due=new Date(d.getTime()+30*864e5);return{from:'Your Name or Business\nyou@example.com',to:'Client Name\nClient address',no:'INV-001',date:iso(d),due:iso(due),cur:'USD',tax:0,disc:0,notes:'Payment due within 30 days. Thank you for your business.',items:[['Design work',10,50],['Hosting (1 month)',1,20]]}},
 h(s){return String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]))},
 read(){const s=this.state,g=id=>{const e=document.getElementById(id);return e?e.value:''};if(!document.getElementById('ivfrom'))return;
  Object.assign(s,{from:g('ivfrom'),to:g('ivto'),no:g('ivno'),date:g('ivdate'),due:g('ivdue'),cur:g('ivcur'),tax:+g('ivtax')||0,disc:+g('ivdisc')||0,notes:g('ivnotes')});
  s.items=[...document.querySelectorAll('.ivrow')].map(r=>[r.querySelector('.ivd').value,+r.querySelector('.ivq').value||0,+r.querySelector('.ivr').value||0]);store.set('invoice',s)},
 render(){if(!this.state)this.state=Object.assign(this.def(),store.get('invoice',{}));const s=this.state,h=x=>this.h(x);
  const rows=s.items.map((it,i)=>`<div class="row ivrow"><div class="field" style="flex:3"><label>Item ${i+1}</label><input class="ivd" type="text" value="${h(it[0])}" aria-label="Item ${i+1} description"></div><div class="field"><label>Qty</label><input class="ivq" type="number" step="any" value="${it[1]}"></div><div class="field"><label>Price</label><input class="ivr" type="number" step="any" value="${it[2]}"></div><button type="button" class="ivdel copy" data-i="${i}" aria-label="Remove item ${i+1}" style="align-self:flex-end">✕</button></div>`).join('');
  return `<div class="inputs"><div class="row"><div class="field"><label for="ivfrom">From (you)</label><textarea id="ivfrom" rows="3">${h(s.from)}</textarea></div><div class="field"><label for="ivto">Bill to</label><textarea id="ivto" rows="3">${h(s.to)}</textarea></div></div>
  <div class="row">${field('ivno','Invoice number',h(s.no),{type:'text'})}<div class="field"><label for="ivdate">Date</label><input id="ivdate" type="date" value="${s.date}"></div><div class="field"><label for="ivdue">Due date</label><input id="ivdue" type="date" value="${s.due}"></div>
  <div class="field"><label for="ivcur">Currency</label><select id="ivcur">${['USD','EUR','GBP','CAD','AUD','INR'].map(c=>`<option${c===s.cur?' selected':''}>${c}</option>`).join('')}</select></div></div>
  ${rows}<div class="row"><button type="button" class="copy" id="ivadd">+ Add item</button></div>
  <div class="row">${field('ivtax','Tax',s.tax,{unit:'%'})}${field('ivdisc','Discount',s.disc,{unit:'%'})}</div>
  <div class="field"><label for="ivnotes">Notes or payment terms</label><textarea id="ivnotes" rows="2">${h(s.notes)}</textarea></div>
  <p class="hint">Everything stays in your browser; nothing is uploaded. Your last invoice is remembered on this device.</p></div><div class="result" id="out"></div>`},
 calc(){this.read();const s=this.state,h=x=>this.h(x),loc={USD:'en-US',EUR:'de-DE',GBP:'en-GB',CAD:'en-CA',AUD:'en-AU',INR:'en-IN'}[s.cur]||'en-US',m=n=>new Intl.NumberFormat(loc,{style:'currency',currency:s.cur}).format(n||0);
  const sub=s.items.reduce((a,[,q,r])=>a+q*r,0),disc=sub*s.disc/100,tax=(sub-disc)*s.tax/100,tot=sub-disc+tax,fd=d=>d?new Date(d+'T12:00').toLocaleDateString('en-US',{year:'numeric',month:'short',day:'numeric'}):'';
  $('#out').innerHTML=`<span class="label">Invoice total</span><div class="big"><em>${m(tot)}</em></div>
  <div id="invPrev" class="invoice"><div class="iv-top"><div><h2>INVOICE</h2><p>${h(s.no)}</p></div><div class="iv-dates"><p><b>Date:</b> ${fd(s.date)}</p><p><b>Due:</b> ${fd(s.due)}</p></div></div>
  <div class="iv-parties"><div><small>From</small><p>${h(s.from).replace(/\n/g,'<br>')}</p></div><div><small>Bill to</small><p>${h(s.to).replace(/\n/g,'<br>')}</p></div></div>
  <table><thead><tr><th>Description</th><th>Qty</th><th>Price</th><th>Amount</th></tr></thead><tbody>${s.items.map(([d,q,r])=>`<tr><td>${h(d)}</td><td>${num(q,2)}</td><td>${m(r)}</td><td>${m(q*r)}</td></tr>`).join('')}</tbody></table>
  <dl class="iv-tot"><div><dt>Subtotal</dt><dd>${m(sub)}</dd></div>${s.disc?`<div><dt>Discount (${num(s.disc,2)}%)</dt><dd>−${m(disc)}</dd></div>`:''}${s.tax?`<div><dt>Tax (${num(s.tax,2)}%)</dt><dd>${m(tax)}</dd></div>`:''}<div class="iv-grand"><dt>Total due</dt><dd>${m(tot)}</dd></div></dl>
  ${s.notes?`<p class="iv-notes">${h(s.notes).replace(/\n/g,'<br>')}</p>`:''}</div>
  <div class="row"><button type="button" class="copy" id="ivpdf">Download PDF / Print</button>${copyBtn}</div><p class="hint">In the print window, choose “Save as PDF” as the destination.</p>`;
  const b=$('#ivpdf');if(b)b.onclick=()=>{document.body.classList.add('print-invoice');const off=()=>{document.body.classList.remove('print-invoice');window.removeEventListener('afterprint',off)};window.addEventListener('afterprint',off);window.print();setTimeout(off,1500)};
  return `Invoice ${s.no}: total ${m(tot)} due ${fd(s.due)}`},
 after(){const t=this;$('#ivadd').onclick=()=>{t.read();t.state.items.push(['',1,0]);open('invoice')};
  document.querySelectorAll('.ivdel').forEach(b=>b.onclick=()=>{t.read();t.state.items.splice(+b.dataset.i,1);if(!t.state.items.length)t.state.items.push(['',1,0]);open('invoice')})}},

{id:'emi',cat:'Money',name:'EMI calculator',kw:'emi calculator loan emi home loan emi car loan emi personal loan emi monthly instalment equated monthly installment india rupees',desc:'Monthly EMI, total interest and repayment schedule.',
 state:{u:'y'},
 inr(n,d=0){return isFinite(n)?new Intl.NumberFormat('en-IN',{style:'currency',currency:'INR',maximumFractionDigits:d}).format(n):'—'},
 render(){const s=this.state;return `<div class="inputs"><div class="row">${field('emp','Loan amount',2500000,{unit:'₹'})}${field('emr','Interest rate (per year)',8.5,{unit:'%'})}</div>
  <div class="row">${field('emn','Loan tenure',s.u==='y'?20:240,{unit:s.u==='y'?'years':'months'})}<div class="field"><label>Tenure in</label>${seg('emu',[['y','Years'],['m','Months']],s.u)}</div></div></div><div class="result" id="out"></div>`},
 calc(){const P=v('emp'),rate=v('emr'),n=Math.round((v('emn')||0)*(this.state.u==='y'?12:1)),r=rate/1200;
  if(!(P>0&&n>0&&rate>=0)){$('#out').innerHTML='<span class="label">EMI</span><p class="hint">Enter the loan amount, rate and tenure.</p>';return''}
  const emi=r?P*r*(1+r)**n/((1+r)**n-1):P/n,tot=emi*n,int=tot-P;let bal=P,rows=[],yi=0,yp=0;
  for(let k=1;k<=n;k++){const i=bal*r,p=emi-i;bal-=p;yi+=i;yp+=p;if(k%12===0||k===n){rows.push([`Year ${Math.ceil(k/12)}`,this.inr(yp),this.inr(yi),this.inr(Math.max(0,bal))]);yi=yp=0}}
  $('#out').innerHTML=`<span class="label">Monthly EMI</span><div class="big"><em>${this.inr(emi)}</em></div><p class="answer">A loan of ${this.inr(P)} at ${num(rate,2)}% for ${n} months costs <strong>${this.inr(emi)} a month</strong>. You repay ${this.inr(tot)} in total, of which ${this.inr(int)} is interest.</p>${kv([['Principal',this.inr(P)],['Total interest',this.inr(int)],['Total payment',this.inr(tot)],['Interest as % of loan',num(int/P*100,1)+'%']])}
  <div class="tbl"><table><thead><tr><th>Year</th><th>Principal paid</th><th>Interest paid</th><th>Balance</th></tr></thead><tbody>${rows.map(r=>'<tr>'+r.map(c=>`<td>${c}</td>`).join('')+'</tr>').join('')}</tbody></table></div>${copyBtn}`;
  return `EMI ${this.inr(emi)}/month on ${this.inr(P)} at ${rate}% for ${n} months`},
 after(){bindSeg('emu',x=>{const val=v('emn');this.state.u=x;open('emi');const e=$('#emn');if(e&&isFinite(val)){e.value=x==='m'?Math.round(val*12):+(val/12).toFixed(2);update()}})}},

{id:'sip',cat:'Money',name:'SIP calculator',kw:'sip calculator mutual fund sip returns systematic investment plan step up sip calculator monthly investment india rupees future value',desc:'What a monthly SIP grows to, with optional step-up.',
 inr(n){return isFinite(n)?new Intl.NumberFormat('en-IN',{style:'currency',currency:'INR',maximumFractionDigits:0}).format(n):'—'},
 render(){return `<div class="inputs"><div class="row">${field('sipm','Monthly investment',10000,{unit:'₹'})}${field('sipr','Expected return (per year)',12,{unit:'%'})}</div>
  <div class="row">${field('sipy','Time period',15,{unit:'years'})}${field('sips','Yearly step-up (optional)',0,{unit:'%'})}</div>
  <p class="hint">Returns on mutual funds are not guaranteed. 12% is a common long-run assumption for equity funds; debt funds are usually lower.</p></div><div class="result" id="out"></div>`},
 calc(){const P=v('sipm'),R=v('sipr'),Y=Math.round(v('sipy')||0),st=v('sips')||0,i=R/1200;
  if(!(P>0&&Y>0&&R>-100)){$('#out').innerHTML='<span class="label">SIP value</span><p class="hint">Enter the monthly amount, return and years.</p>';return''}
  let val=0,inv=0,amt=P,rows=[];for(let y=1;y<=Y;y++){for(let m=0;m<12;m++){val=(val+amt)*(1+i);inv+=amt}rows.push([`Year ${y}`,this.inr(amt),this.inr(inv),this.inr(val)]);amt*=1+st/100}
  const gain=val-inv;
  $('#out').innerHTML=`<span class="label">Estimated value after ${Y} years</span><div class="big"><em>${this.inr(val)}</em></div><p class="answer">Investing ${this.inr(P)} a month${st?` (rising ${num(st,1)}% a year)`:''} at ${num(R,2)}% a year grows to about <strong>${this.inr(val)}</strong>: ${this.inr(inv)} invested and ${this.inr(gain)} in returns.</p>${kv([['Total invested',this.inr(inv)],['Estimated returns',this.inr(gain)],['Final value',this.inr(val)],['Value ÷ invested',num(val/inv,2)+'×']])}
  <div class="tbl"><table><thead><tr><th>Year</th><th>Monthly SIP</th><th>Invested so far</th><th>Value</th></tr></thead><tbody>${rows.map(r=>'<tr>'+r.map(c=>`<td>${c}</td>`).join('')+'</tr>').join('')}</tbody></table></div>${copyBtn}`;
  return `SIP of ${this.inr(P)}/month for ${Y} years at ${R}% ≈ ${this.inr(val)}`}},
