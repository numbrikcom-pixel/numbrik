{id:'shoe',cat:'Converters',name:'Shoe size converter',kw:'shoe size converter shoe size conversion chart us uk eu european mens womens kids eu to us shoe size foot length cm inches',desc:'Convert shoe sizes between US, UK and EU.',
 state:{who:'m',from:'us'},
 R2(x){return Math.round(x*2)/2},
 inchFrom(sys,who,x){if(sys==='in')return x;if(sys==='cm')return x/2.54;if(sys==='eu')return ((x-2)/1.27)/3;if(who==='k'){if(sys==='us')return (x+9.67)/3;if(sys==='uk')return (x+10)/3}if(sys==='uk')return (x+23)/3;return (x+(who==='w'?21:22))/3},
 render(){const s=this.state,def={m:{us:10,uk:9,eu:42.5,cm:27.1,in:10.67},w:{us:8,uk:6,eu:39,cm:24.6,in:9.67},k:{us:11,uk:10.5,eu:29,cm:17.4,in:6.89}}[s.who][s.from];
  const lbl={us:s.who==='k'?'US kids size':'US size',uk:'UK size',eu:'EU size',cm:'Foot length',in:'Foot length'}[s.from];
  return `<div class="inputs"><div class="row">${seg('shw',[['m','Men'],['w','Women'],['k','Kids']],s.who)}</div>
  <div class="row">${seg('shf',[['us','US'],['uk','UK'],['eu','EU'],['cm','cm'],['in','inches']],s.from)}</div>
  <div class="row">${field('shx',lbl,def,{unit:s.from==='cm'?'cm':s.from==='in'?'in':'',step:s.from==='cm'||s.from==='in'?0.1:0.5})}</div>
  <p class="hint">${s.who==='k'?'Kids’ US sizes run 0–13.5, then youth sizes start again at 1Y. Enter a youth size as 13 + the youth number (1Y = 14).':'Sizes vary by brand by about half a size. Check the brand’s own chart before you buy.'}</p></div><div class="result" id="out"></div>`},
 calc(){const s=this.state,x=v('shx');if(!(x>0)){$('#out').innerHTML='<span class="label">Your size</span><p class="hint">Enter a size or foot length.</p>';return''}
  const i=this.inchFrom(s.from,s.who,x),cm=i*2.54,eu=1.27*(3*i)+2,r=n=>this.R2(n).toString();
  if(!(cm>8&&cm<36)){$('#out').innerHTML='<span class="label">Your size</span><p class="hint">That size is outside the usual range. Check the number and the system.</p>';return''}
  let rows,main;
  if(s.who==='k'){const us=3*i-9.67,uk=3*i-10,f=n=>n<13.75?r(n):r(n-13)+'Y';main=`US kids ${f(us)}`;rows=[['US kids',f(us)],['UK kids',f(uk)],['EU',r(eu)],['Foot length',`${num(i,2)} in · ${num(cm,1)} cm`]]}
  else{const m=3*i-22,w=3*i-21,uk=3*i-23;main=s.who==='m'?`US men's ${r(m)}`:`US women's ${r(w)}`;rows=[['US men',r(m)],['US women',r(w)],['UK',r(uk)],['EU',r(eu)],['Foot length',`${num(i,2)} in · ${num(cm,1)} cm`]]}
  $('#out').innerHTML=`<span class="label">Your size</span><div class="big"><em>${main}</em></div>${kv(rows)}${copyBtn}`;
  return rows.map(r=>r[0]+' '+r[1]).join(', ')},
 after(){bindSeg('shw',x=>{this.state.who=x;open('shoe')});bindSeg('shf',x=>{this.state.from=x;open('shoe')})}},
