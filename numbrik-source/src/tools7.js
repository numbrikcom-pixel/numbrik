{id:'turkey',cat:'Home',name:'Turkey calculator',kw:'turkey calculator thanksgiving turkey cooking time roasting time thawing time how big turkey per person christmas turkey',desc:'Turkey size, thawing and roasting time.',
 state:{mode:'guests',stuff:'no',thaw:'fridge'},
 R:[[8,1.5,3.25,null,null],[12,2.75,3,3,3.5],[14,3,3.75,3.5,4],[18,3.75,4.25,4,4.25],[20,4.25,4.5,4.25,4.75],[99,4.5,5,4.75,5.25]],
 tg(){const n=new Date(),y=n.getMonth()===11&&n.getDate()>1?n.getFullYear()+1:n.getFullYear();let d=new Date(y,10,1);d.setDate(1+((4-d.getDay()+7)%7)+21);if(d<n){d=new Date(y+1,10,1);d.setDate(1+((4-d.getDay()+7)%7)+21)}const p=x=>String(x).padStart(2,'0');return `${d.getFullYear()}-${p(d.getMonth()+1)}-${p(d.getDate())}T17:00`},
 render(){const s=this.state;return `<div class="inputs">${seg('tkm',[['guests','I know how many guests'],['weight','I have a turkey']],s.mode)}
  <div class="row">${s.mode==='guests'?field('tkg','Guests',12,{unit:'people',step:1})+`<div class="field"><label for="tkl"><input type="checkbox" id="tkl" checked> I want leftovers</label></div>`:field('tkw','Turkey weight',16,{unit:'lb'})}</div>
  <div class="row"><div class="field"><label>Stuffing</label>${seg('tks',[['no','Unstuffed'],['yes','Stuffed']],s.stuff)}</div><div class="field"><label>Thawing</label>${seg('tkt',[['fridge','Fridge'],['water','Cold water'],['none','Fresh / thawed']],s.thaw)}</div></div>
  ${field('tkd','Dinner time',this.tg(),{type:'datetime-local'})}
  <div id="tkplan"></div><p class="hint">Times are for a 325°F (163°C) oven, from the USDA chart. Always check the turkey reaches 165°F (74°C).</p></div><div class="result" id="out"></div>`},
 calc(){const s=this.state;let w;if(s.mode==='guests'){const g=Math.round(v('tkg'));if(!(g>0)){$('#out').innerHTML='<span class="label">Turkey</span><p class="hint">Enter the number of guests.</p>';$('#tkplan').innerHTML='';return''}w=g*($('#tkl').checked?1.5:1)}else w=v('tkw');
  if(!(w>=4&&w<=40)){$('#out').innerHTML='<span class="label">Turkey</span><p class="hint">Enter a turkey between 4 and 40 lb.</p>';$('#tkplan').innerHTML='';return''}
  const row=this.R.find(r=>w<r[0])||this.R[this.R.length-1],st=s.stuff==='yes'&&row[3]!=null,lo=st?row[3]:row[1],hi=st?row[4]:row[2];
  const fh=h=>{const m=Math.round(h*60);return `${Math.floor(m/60)} h ${String(m%60).padStart(2,'0')} min`};
  const thawLo=s.thaw==='fridge'?Math.max(1,Math.round(w/5)):w*0.5,thawHi=s.thaw==='fridge'?Math.ceil(w/4):w*0.5;
  const d=$('#tkd').value?new Date($('#tkd').value):null,rows=[];let inOven=null;
  if(d&&!isNaN(d)){const out=new Date(d-30*6e4);inOven=new Date(out-hi*36e5);const F=x=>x.toLocaleString(R().loc,{weekday:'short',month:'short',day:'numeric',hour:'numeric',minute:'2-digit'});
   if(s.thaw==='fridge'){const t=new Date(inOven);t.setDate(t.getDate()-thawHi);t.setHours(9,0,0,0);rows.push(['Move turkey to the fridge',t.toLocaleDateString(R().loc,{weekday:'long',month:'short',day:'numeric'})+' (morning)'])}
   if(s.thaw==='water'){const t=new Date(inOven-(thawHi*36e5+36e5));rows.push(['Start cold-water thaw',F(t)])}
   rows.push(['Heat oven to 325°F',F(new Date(inOven-20*6e4))],['Turkey in the oven',F(inOven)],['Start checking temperature',F(new Date(inOven.getTime()+(lo-0.5)*36e5))],['Out of the oven to rest',F(out)],['Dinner',F(d)])}
  $('#tkplan').innerHTML=rows.length?`<div class="field"><label>Your timeline</label></div>${kv(rows)}`:'';
  $('#out').innerHTML=`<span class="label">${s.mode==='guests'?'Buy a turkey of about':'Roasting time'}</span><div class="big"><em>${s.mode==='guests'?num(Math.ceil(w),0)+' lb':fh(lo)+' – '+fh(hi)}</em></div>${kv([['Turkey weight',`${num(w,1)} lb (${num(w*0.4536,1)} kg)`],['Roasting at 325°F',`${fh(lo)} – ${fh(hi)}${s.stuff==='yes'&&!st?' (don’t stuff a turkey this small)':''}`],['Thawing',s.thaw==='fridge'?`${thawLo===thawHi?thawHi:thawLo+'–'+thawHi} days in the fridge`:s.thaw==='water'?`${num(thawHi,1)} hours in cold water`:'Not needed'],['Done when',`165°F (74°C) in breast, thigh and wing`],['Rest before carving','20–30 minutes']])}${copyBtn}`;
  return `${num(w,1)} lb turkey: roast ${fh(lo)}–${fh(hi)} at 325°F`+(inOven?`, in the oven ${inOven.toLocaleTimeString(R().loc,{hour:'numeric',minute:'2-digit'})}`:'')},
 after(){bindSeg('tkm',x=>{this.state.mode=x;open('turkey')});bindSeg('tks',x=>{this.state.stuff=x;update()});bindSeg('tkt',x=>{this.state.thaw=x;update()});const l=$('#tkl');if(l)l.addEventListener('change',update)}},
