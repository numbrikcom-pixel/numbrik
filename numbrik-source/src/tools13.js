{id:'afford',cat:'Money',name:'House affordability calculator',kw:'how much house can i afford calculator home affordability calculator mortgage affordability how much mortgage can i afford income 28/36 rule debt to income dti',desc:'How much house you can afford on your income.',
 state:{rule:'36'},
 solve(inc,debt,down,rate,yrs,tax,ins,hoa,rule){const r=rate/1200,n=yrs*12,k=r?r/(1-Math.pow(1+r,-n)):1/n,front=rule==='36'?0.28:0.31,back=rule==='36'?0.36:0.43;
  const M=Math.min(inc/12*front,inc/12*back-debt),fixed=ins/12+hoa;let pm=0.005/12,H=(M-fixed+down*(k+pm))/(k+tax/1200+pm);if(down>=0.2*H){pm=0;H=(M-fixed+down*k)/(k+tax/1200)}
  H=Math.max(H,down);const L=Math.max(0,H-down),pi=L*k,tx=H*tax/1200,pmi=down<0.2*H?L*0.005/12:0;return{H,L,pi,tx,ins:ins/12,hoa,pmi,tot:pi+tx+ins/12+hoa+pmi,M,front,back}},
 render(){const s=this.state,c=R().cur;return `<div class="inputs"><div class="row">${field('afi','Annual household income (before tax)',100000,{unit:c})}${field('afd','Monthly debt payments',500,{unit:c})}${field('afp','Down payment',40000,{unit:c})}</div>
  <div class="row">${field('afr','Mortgage rate',6.5,{unit:'%'})}${field('aft','Loan term',30,{unit:'yrs'})}${field('afx','Property tax',1.1,{unit:'% / yr'})}</div>
  <div class="row">${field('afn','Home insurance',1800,{unit:c+'/yr'})}${field('afh','HOA fees',0,{unit:c+'/mo'})}<div class="field"><label>Debt-to-income rule</label>${seg('afrule',[['36','28/36 (conservative)'],['43','31/43 (FHA-style)']],s.rule)}</div></div>
  <p class="hint">Monthly debts: car loans, student loans, credit card minimums, child support. Not rent, utilities or groceries.</p></div><div class="result" id="out"></div>`},
 calc(){const g=id=>v(id)||0,inc=v('afi');if(!(inc>0)){$('#out').innerHTML='<span class="label">You can afford</span><p class="hint">Enter your annual income.</p>';return''}
  const x=this.solve(inc,g('afd'),g('afp'),g('afr'),g('aft')||30,g('afx'),g('afn'),g('afh'),this.state.rule);
  if(!(x.M>x.ins+x.hoa)||x.H<=g('afp')+1){$('#out').innerHTML='<span class="label">You can afford</span><p class="hint">Your monthly debts are too high for this rule. Paying some down, or the 31/43 rule, will raise your budget.</p>';return''}
  const p=n=>money(n,0);
  $('#out').innerHTML=`<span class="label">You can afford a home of about</span><div class="big"><em>${p(x.H)}</em></div><p class="answer">With ${p(g('afp'))} down, that's a ${p(x.L)} mortgage and about ${p(x.tot)} a month including taxes and insurance.</p>${kv([['Principal & interest',p(x.pi)],['Property tax',p(x.tx)],['Home insurance',p(x.ins)],...(x.hoa?[['HOA',p(x.hoa)]]:[]),...(x.pmi?[['PMI (est. 0.5%/yr, under 20% down)',p(x.pmi)]]:[]),['Total monthly payment',p(x.tot)],['Housing ratio (front-end DTI)',num(x.tot/(inc/12)*100,1)+'%'],['Total debt ratio (back-end DTI)',num((x.tot+g('afd'))/(inc/12)*100,1)+'%'],['Down payment',num(g('afp')/x.H*100,1)+'% of price']])}${copyBtn}`;
  return `You can afford a home of about ${p(x.H)} (${p(x.tot)}/month)`},
 after(){bindSeg('afrule',x=>{this.state.rule=x;update()})}},
