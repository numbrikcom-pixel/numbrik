{id:'lease',cat:'Money',name:'Car lease calculator',kw:'car lease calculator lease payment calculator money factor residual value capitalized cost auto lease monthly payment lease vs buy',desc:'Monthly car lease payment from price, residual and money factor.',
 state:{},
 render(){const c=R().cur;return `<div class="inputs"><div class="row">${field('lsm','MSRP (sticker price)',40000,{unit:c})}${field('lsp','Negotiated price',37500,{unit:c})}${field('lsd','Down payment + trade-in',3000,{unit:c})}</div>
  <div class="row">${field('lst','Lease term',36,{unit:'months'})}${field('lsr','Residual value',58,{unit:'% of MSRP'})}${field('lsa','Interest rate (APR)',6,{unit:'%'})}</div>
  <div class="row">${field('lsf','Fees added to the lease',995,{unit:c})}${field('lsx','Sales tax on payment',7,{unit:'%'})}</div>
  <p class="hint">Dealers quote the rate as a money factor: money factor = APR ÷ 2,400, so 6% APR is 0.0025. Most US states tax the monthly payment, not the whole car.</p></div><div class="result" id="out"></div>`},
 calc(){const g=id=>v(id)||0,msrp=g('lsm'),price=g('lsp'),down=g('lsd'),n=Math.round(g('lst')),rp=g('lsr'),apr=g('lsa'),fees=g('lsf'),tx=g('lsx')/100;
  if(!(msrp>0&&price>0&&n>0&&rp>0)){$('#out').innerHTML='<span class="label">Monthly lease payment</span><p class="hint">Enter the price, term and residual value.</p>';return''}
  const cap=price+fees-down,res=msrp*rp/100,mf=apr/2400,dep=(cap-res)/n,fin=(cap+res)*mf,base=dep+fin,tax=base*tx,pm=base+tax,tot=pm*n+down;
  if(cap<=res){$('#out').innerHTML='<span class="label">Monthly lease payment</span><p class="hint">The capitalized cost is below the residual value. Check the price, down payment and residual.</p>';return''}
  $('#out').innerHTML=`<span class="label">Monthly lease payment</span><div class="big"><em>${money(pm)}</em></div><p class="answer">${money(pm)} a month for ${n} months, ${money(tot,0)} in total including your ${money(down,0)} down.</p>${kv([['Depreciation part',money(dep)],['Finance (rent) charge',money(fin)],['Sales tax',money(tax)],['Money factor',mf.toFixed(5)],['Residual (buyout) value',money(res,0)],['Net capitalized cost',money(cap,0)],['Total cost of the lease',money(tot,0)]])}${copyBtn}`;
  return `Lease payment ${money(pm)}/month for ${n} months`}},

{id:'retire',cat:'Money',name:'Retirement calculator',kw:'retirement calculator how much will i have at retirement 401k calculator retirement savings calculator 4% rule how much do i need to retire nest egg',desc:'Projected retirement savings and income.',
 state:{},
 render(){const c=R().cur;return `<div class="inputs"><div class="row">${field('rta','Current age',35,{unit:'yrs'})}${field('rtr','Retirement age',67,{unit:'yrs'})}${field('rts','Current savings',50000,{unit:c})}</div>
  <div class="row">${field('rtm','Monthly contribution',800,{unit:c})}${field('rtg','Expected annual return',6,{unit:'%'})}${field('rti','Inflation',2.5,{unit:'%'})}</div>
  <div class="row">${field('rtx','Contribution increase per year',2,{unit:'%'})}${field('rtw','Withdrawal rate in retirement',4,{unit:'%'})}</div>
  <p class="hint">Returns aren't guaranteed. 6% is a common long-run assumption for a diversified stock and bond mix; use a lower number to be cautious.</p><div id="rttab" class="tc-wrap"></div></div><div class="result" id="out"></div>`},
 calc(){const g=id=>v(id)||0,a=Math.round(g('rta')),r=Math.round(g('rtr')),s=g('rts'),m=g('rtm'),ret=g('rtg')/100,inf=g('rti')/100,inc=g('rtx')/100,wr=g('rtw')/100,tab=$('#rttab');
  if(!(r>a&&a>0)){$('#out').innerHTML='<span class="label">At retirement</span><p class="hint">Retirement age must be later than your current age.</p>';tab.innerHTML='';return''}
  const mr=Math.pow(1+ret,1/12)-1;let b=s,c=m,contrib=s,rows=[];for(let y=1;y<=r-a;y++){for(let k=0;k<12;k++){b=b*(1+mr)+c;contrib+=c}if(y%5===0||y===r-a)rows.push(`<tr><td>${a+y}</td><td class="num">${money(contrib,0)}</td><td class="num">${money(b,0)}</td><td class="num">${money(b/Math.pow(1+inf,y),0)}</td></tr>`);c*=1+inc}
  const real=b/Math.pow(1+inf,r-a),inc1=b*wr;
  tab.innerHTML=`<table><thead><tr><th>Age</th><th>Total contributed</th><th>Balance</th><th>In today's money</th></tr></thead><tbody>${rows.join('')}</tbody></table>`;
  $('#out').innerHTML=`<span class="label">Savings at age ${r}</span><div class="big"><em>${money(b,0)}</em></div><p class="answer">That's about ${money(real,0)} in today's money, enough for roughly ${money(inc1/12,0)} a month (${money(inc1/12/Math.pow(1+inf,r-a),0)} in today's money) at a ${num(wr*100,1)}% withdrawal rate.</p>${kv([['Total you contribute',money(contrib,0)],['Investment growth',money(b-contrib,0)],[`Yearly income at ${num(wr*100,1)}%`,money(inc1,0)],['Years until retirement',String(r-a)]])}${copyBtn}`;
  return `About ${money(b,0)} at ${r} (${money(real,0)} in today's money)`}},

{id:'savings',cat:'Money',name:'Savings calculator',kw:'savings calculator how much will my savings grow high yield savings calculator monthly deposit interest savings goal calculator how much to save each month',desc:'How savings grow with deposits and interest, or what to save for a goal.',
 state:{mode:'grow'},
 render(){const s=this.state,c=R().cur;return `<div class="inputs"><div class="row">${seg('svm',[['grow','How much will I have?'],['goal','How much to save each month?']],s.mode)}</div>
  <div class="row">${field('svi','Starting balance',5000,{unit:c})}${s.mode==='grow'?field('svd','Monthly deposit',300,{unit:c}):field('svg','Savings goal',25000,{unit:c})}</div>
  <div class="row">${field('svr','Interest rate (APY)',4.25,{unit:'%'})}${field('svy','Time',5,{unit:'years'})}</div><div id="svtab" class="tc-wrap"></div></div><div class="result" id="out"></div>`},
 calc(){const s=this.state,P=v('svi')||0,apy=(v('svr')||0)/100,yrs=v('svy'),n=Math.round(yrs*12),tab=$('#svtab');
  if(!(n>0)){$('#out').innerHTML='<span class="label">Savings</span><p class="hint">Enter how many years you will save.</p>';tab.innerHTML='';return''}
  const r=Math.pow(1+apy,1/12)-1,fv=(d)=>{let b=P,rows=[];for(let k=1;k<=n;k++){b=b*(1+r)+d;if(k%12===0)rows.push([k/12,b,P+d*k])}return[b,rows]};
  let d;if(s.mode==='goal'){const G=v('svg')||0,grow=P*Math.pow(1+r,n),fac=r?(Math.pow(1+r,n)-1)/r:n;d=Math.max(0,(G-grow)/fac)}else d=v('svd')||0;
  const [b,rows]=fv(d),dep=P+d*n;tab.innerHTML=rows.length?`<table><thead><tr><th>Year</th><th>Deposited</th><th>Interest earned</th><th>Balance</th></tr></thead><tbody>${rows.map(([y,bb,dd])=>`<tr><td>${y}</td><td class="num">${money(dd,0)}</td><td class="num">${money(bb-dd,0)}</td><td class="num">${money(bb,0)}</td></tr>`).join('')}</tbody></table>`:'';
  if(s.mode==='goal'){$('#out').innerHTML=`<span class="label">Save each month</span><div class="big"><em>${money(d)}</em></div><p class="answer">Saving ${money(d)} a month for ${num(yrs,1)} years at ${num(apy*100,2)}% APY grows ${money(P,0)} to ${money(b,0)}.</p>${kv([['Total deposited',money(dep,0)],['Interest earned',money(b-dep,0)]])}${copyBtn}`;return `Save ${money(d)} a month`}
  $('#out').innerHTML=`<span class="label">Balance after ${num(yrs,1)} years</span><div class="big"><em>${money(b,0)}</em></div>${kv([['Total deposited',money(dep,0)],['Interest earned',money(b-dep,0)],['Interest in the final year',rows.length>1?money(rows[rows.length-1][1]-rows[rows.length-2][1]-d*12,0):money(b-dep,0)]])}${copyBtn}`;
  return `${money(b,0)} after ${num(yrs,1)} years`},
 after(){bindSeg('svm',x=>{this.state.mode=x;open('savings')})}},

{id:'studentloan',cat:'Money',name:'Student loan calculator',kw:'student loan calculator student loan payment calculator federal student loan repayment 10 year standard extended plan payoff extra payments student loan interest',desc:'Student loan payment, total interest and payoff with extra payments.',
 state:{},
 pm(P,r,n){return r?P*r/(1-Math.pow(1+r,-n)):P/n},
 render(){const c=R().cur;return `<div class="inputs"><div class="row">${field('sla','Loan balance',30000,{unit:c})}${field('slr','Interest rate',6.5,{unit:'%'})}${field('slt','Repayment term',10,{unit:'years'})}</div>
  <div class="row">${field('slx','Extra payment per month',0,{unit:c})}</div>
  <p class="hint">The federal Standard Repayment Plan is 10 years. Income-driven plans base the payment on income instead and aren't modelled here.</p></div><div class="result" id="out"></div>`},
 calc(){const P=v('sla'),r=(v('slr')||0)/1200,yrs=v('slt'),n=Math.round(yrs*12),x=Math.max(0,v('slx')||0);
  if(!(P>0&&n>0)){$('#out').innerHTML='<span class="label">Monthly payment</span><p class="hint">Enter the balance, rate and term.</p>';return''}
  const pm=this.pm(P,r,n),base=pm*n-P;let b=P,k=0,ti=0;while(b>0.005&&k<600){const i=b*r;b-=Math.min(b,pm+x-i);ti+=i;k++}
  const alt=[[10,'10-year standard'],[20,'20 years'],[25,'25-year extended']].filter(([y])=>y!==yrs).map(([y,l])=>[`${l}`,`${money(this.pm(P,r,y*12))}/mo, ${money(this.pm(P,r,y*12)*y*12-P,0)} interest`]);
  const rows=[['Total interest',money(ti,0)],['Total paid',money(P+ti,0)],['Payoff time',`${Math.floor(k/12)} yrs ${k%12} mos`],['Interest in the first month',money(P*r)]];if(x>0)rows.push(['Saved with extra payments',`${money(base-ti,0)} and ${n-k} months`]);
  $('#out').innerHTML=`<span class="label">Monthly payment</span><div class="big"><em>${money(pm)}</em></div>${kv(rows.concat(alt))}${copyBtn}`;
  return `Student loan payment ${money(pm)}/month, ${money(ti,0)} interest`}},

{id:'rentbuy',cat:'Money',name:'Rent vs buy calculator',kw:'rent vs buy calculator should i rent or buy a house buying vs renting calculator is it better to rent or buy cost of owning vs renting',desc:'Compare the true cost of renting and buying over time.',
 state:{},
 render(){const c=R().cur;return `<div class="inputs"><div class="row">${field('rbp','Home price',400000,{unit:c})}${field('rbd','Down payment',20,{unit:'%'})}${field('rbr','Mortgage rate',6.5,{unit:'%'})}${field('rby','Years you’ll stay',7,{unit:'yrs'})}</div>
  <div class="row">${field('rbt','Property tax',1.1,{unit:'%/yr'})}${field('rbi','Insurance + HOA',2400,{unit:c+'/yr'})}${field('rbm','Maintenance',1,{unit:'%/yr'})}${field('rba','Home price growth',3,{unit:'%/yr'})}</div>
  <div class="row">${field('rbn','Monthly rent',2200,{unit:c})}${field('rbg','Rent increase',3,{unit:'%/yr'})}${field('rbo','Investment return',5,{unit:'%/yr'})}</div>
  <p class="hint">Assumes a 30-year fixed mortgage, 3% closing costs to buy and 6% selling costs. The down payment and closing costs are counted as money that could otherwise be invested.</p></div><div class="result" id="out"></div>`},
 calc(){const g=id=>v(id)||0,H=g('rbp'),dp=g('rbd')/100,rate=g('rbr')/1200,Y=Math.round(g('rby')),tx=g('rbt')/100,ins=g('rbi'),mt=g('rbm')/100,ap=g('rba')/100,rent=g('rbn'),rg=g('rbg')/100,inv=g('rbo')/100;
  if(!(H>0&&Y>0&&rent>0)){$('#out').innerHTML='<span class="label">Rent vs buy</span><p class="hint">Enter the home price, rent and years.</p>';return''}
  const down=H*dp,L=H-down,n=360,pm=rate?L*rate/(1-Math.pow(1+rate,-n)):L/n,close=H*0.03;let bal=L,own=down+close,val=H,rentT=0,rr=rent;
  for(let y=0;y<Y;y++){for(let k=0;k<12;k++){const i=bal*rate;bal-=pm-i;own+=pm}own+=val*tx+ins+val*mt;val*=1+ap;rentT+=rr*12;rr*=1+rg}
  const equity=val*0.94-bal,opp=(down+close)*(Math.pow(1+inv,Y)-1),buyNet=own-equity+opp,diff=rentT-buyNet,better=diff>0?'Buying':'Renting';
  $('#out').innerHTML=`<span class="label">Over ${Y} years</span><div class="big"><em>${better}</em> comes out ${money(Math.abs(diff),0)} ahead</div><p class="answer">Buying costs about ${money(buyNet,0)} net over ${Y} years after selling, versus ${money(rentT,0)} in rent.</p>${kv([['Mortgage payment (P&I)',money(pm,0)+'/mo'],['Total spent owning',money(own,0)],['Equity when you sell (after 6% costs)',money(equity,0)],['Lost investment return on down payment',money(opp,0)],['Net cost of buying',money(buyNet,0)],['Total rent paid',money(rentT,0)],['Home value after '+Y+' years',money(val,0)]])}${copyBtn}`;
  return `${better} is about ${money(Math.abs(diff),0)} cheaper over ${Y} years`}},
