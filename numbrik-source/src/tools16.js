{id:'cryptotax',cat:'Money',name:'Crypto tax calculator',kw:'crypto tax calculator bitcoin tax calculator capital gains on crypto short term long term crypto gains tax 2026 irs uk cgt india 30% vda tax ethereum',desc:'Tax on crypto gains for the US, UK and India.',
 state:{c:null,fs:'s',hold:'long'},
 US:{s:{sd:16100,b:[[12400,.10],[50400,.12],[105700,.22],[201775,.24],[256225,.32],[640600,.35],[Infinity,.37]],lt:[49450,545500],niit:200000},m:{sd:32200,b:[[24800,.10],[100800,.12],[211400,.22],[403550,.24],[512450,.32],[768700,.35],[Infinity,.37]],lt:[98900,613700],niit:250000}},
 tax(b,x){let t=0,lo=0;for(const[hi,r]of b){if(x>lo)t+=(Math.min(x,hi)-lo)*r;lo=hi}return t},
 marg(b,x){for(const[hi,r]of b)if(x<hi)return r;return .37},
 render(){const s=this.state;if(!s.c)s.c=region==='UK'?'uk':(R().loc==='en-IN'?'in':'us');const sym={us:'USD',uk:'GBP',in:'INR'}[s.c];
  return `<div class="inputs"><div class="row">${seg('ctc',[['us','United States'],['uk','United Kingdom'],['in','India']],s.c)}</div>
  ${s.c==='us'?`<div class="row">${seg('ctf',[['s','Single'],['m','Married filing jointly']],s.fs)}${seg('cth',[['short','Held 1 year or less'],['long','Held over 1 year']],s.hold)}</div>`:''}
  <div class="row">${field('ctb','Total cost (what you paid, incl. fees)',s.c==='in'?100000:5000,{unit:sym})}${field('cts','Sale value (what you received, after fees)',s.c==='in'?160000:s.c==='uk'?15000:8000,{unit:sym})}</div>
  ${s.c==='in'?'':`<div class="row">${field('cti',s.c==='us'?'Other income this year (wages etc.)':'Your income this tax year (salary etc.)',s.c==='us'?75000:40000,{unit:sym})}</div>`}
  <p class="hint">${s.c==='us'?'Tax year 2026 federal rates (IRS Rev. Proc. 2025-32), standard deduction applied. State income tax is extra.':s.c==='uk'?'2026/27 rates: 18% within the basic-rate band, 24% above it, after the £3,000 annual exempt amount.':'Flat 30% plus 4% cess under section 115BBH. Surcharge for very high incomes is not included.'} An estimate, not tax advice.</p></div><div class="result" id="out"></div>`},
 calc(){const s=this.state,cost=v('ctb')||0,sale=v('cts')||0,g=sale-cost,cur={us:'USD',uk:'GBP',in:'INR'}[s.c],loc={us:'en-US',uk:'en-GB',in:'en-IN'}[s.c];
  const m=n=>new Intl.NumberFormat(loc,{style:'currency',currency:cur,maximumFractionDigits:0}).format(n),pc=n=>num(n*100,1)+'%';
  if(!(cost>=0&&sale>=0)||(cost===0&&sale===0)){$('#out').innerHTML='<span class="label">Crypto tax</span><p class="hint">Enter what you paid and what you sold for.</p>';return''}
  let tax=0,rows=[],ans='';
  if(s.c==='us'){const T=this.US[s.fs],inc=Math.max(0,v('cti')||0),ti=Math.max(0,inc-T.sd);
   if(g<=0){const ded=Math.min(-g,3000),save=ded*this.marg(T.b,ti);
    $('#out').innerHTML=`<span class="label">Capital loss</span><div class="big"><em>${m(-g)}</em></div><p class="answer">No tax is due. You can deduct up to ${m(3000)} of net capital losses against other income this year (saving about ${m(save)}), and carry ${m(Math.max(0,-g-3000))} forward.</p>${copyBtn}`;return `Capital loss ${m(-g)}`}
   if(s.hold==='short'){tax=this.tax(T.b,ti+g)-this.tax(T.b,ti);rows.push(['Taxed as','Ordinary income (short-term)'],['Your top bracket',pc(this.marg(T.b,ti+g))])}
   else{const[z,f]=T.lt;let rem=g,base=ti,t0=Math.max(0,Math.min(rem,z-base));rem-=t0;base+=t0;const t15=Math.max(0,Math.min(rem,f-Math.max(base,z)));rem-=t15;tax=t15*.15+rem*.20;
    rows.push(['Taxed at 0%',m(t0)],['Taxed at 15%',m(t15)]);if(rem>0)rows.push(['Taxed at 20%',m(rem)])}
   const magi=inc+g,niit=Math.max(0,Math.min(g,magi-T.niit))*.038;if(niit>0){tax+=niit;rows.push(['Net investment income tax (3.8%)',m(niit)])}
   ans=`On a ${m(g)} ${s.hold==='short'?'short':'long'}-term gain you'd owe about ${m(tax)} in federal tax.`}
  else if(s.c==='uk'){const inc=Math.max(0,v('cti')||0),aea=3000,tg=Math.max(0,g-aea),band=Math.max(0,50270-Math.max(inc,12570)),at18=Math.min(tg,band);
   if(g<=0){$('#out').innerHTML=`<span class="label">Capital loss</span><div class="big"><em>${m(-g)}</em></div><p class="answer">No CGT is due. Report the loss to HMRC within four years so you can set it against future gains.</p>${copyBtn}`;return `Capital loss ${m(-g)}`}
   tax=at18*.18+(tg-at18)*.24;rows.push(['Annual exempt amount used',m(Math.min(g,aea))],['Taxable gain',m(tg)],['At 18%',m(at18)],['At 24%',m(tg-at18)]);
   ans=tg>0?`On a ${m(g)} gain you'd pay about ${m(tax)} Capital Gains Tax.`:`Your gain is within the ${m(aea)} annual exempt amount, so no CGT is due.`}
  else{const tds=sale*.01;if(g<=0){$('#out').innerHTML=`<span class="label">Loss</span><div class="big"><em>${m(-g)}</em></div><p class="answer">No tax on this sale. Crypto losses can't be set off against other income or other crypto gains, or carried forward. 1% TDS of ${m(tds)} may still have been deducted; claim it in your return.</p>${copyBtn}`;return `Loss ${m(-g)}`}
   const base=g*.30,cess=base*.04;tax=base+cess;rows.push(['Tax at 30%',m(base)],['Health & education cess (4%)',m(cess)],['1% TDS already deducted on sale',m(tds)],['Left to pay after TDS',m(Math.max(0,tax-tds))]);
   ans=`On a ${m(g)} gain the tax is ${m(tax)} (31.2%). 1% TDS of ${m(tds)} counts towards it.`}
  const net=g-tax;rows.unshift(['Gain',m(g)]);rows.push(['Effective rate on the gain',g>0?pc(tax/g):'0%'],['You keep',m(net)]);
  $('#out').innerHTML=`<span class="label">Estimated tax on your crypto gain</span><div class="big"><em>${m(tax)}</em></div><p class="answer">${ans}</p>${kv(rows)}${copyBtn}`;
  return `Crypto tax ${m(tax)} on a ${m(g)} gain`},
 after(){bindSeg('ctc',x=>{this.state.c=x;open('cryptotax')});if(this.state.c==='us'){bindSeg('ctf',x=>{this.state.fs=x;update()});bindSeg('cth',x=>{this.state.hold=x;update()})}}},
