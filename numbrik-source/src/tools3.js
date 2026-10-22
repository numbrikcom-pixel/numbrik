
{id:'grade',cat:'Students',name:'Grade',kw:'grade calculator weighted grade class grade average assignments categories percentage letter grade',desc:'Weighted class grade from your assignments and categories.',
 rows:null,
 render(){if(!this.rows)this.rows=store.get('grade',[['Homework',92,20],['Quizzes',85,15],['Midterm exam',78,25],['Project',88,15],['Participation',100,5]]);
  return `<div class="inputs"><div class="tc-wrap"><table><thead><tr><th>Assignment or category</th><th>Score %</th><th>Weight %</th><th></th></tr></thead><tbody id="grbody">
  ${this.rows.map((r,i)=>`<tr><td><input id="grn${i}" value="${String(r[0]).replace(/"/g,'&quot;')}" aria-label="Name"></td><td><input id="grs${i}" type="number" min="0" step="any" value="${r[1]}" aria-label="Score percent" inputmode="decimal"></td><td><input id="grw${i}" type="number" min="0" step="any" value="${r[2]}" aria-label="Weight percent" inputmode="decimal"></td><td><button class="btn" type="button" data-gdel="${i}" aria-label="Remove row">✕</button></td></tr>`).join('')}
  </tbody></table></div>
  <div class="actions"><button class="btn primary" type="button" id="gradd">Add row</button></div>
  <p class="hint">Enter scores as percentages (for 45 out of 50, enter 90). Weights don't have to add up to 100: if they add up to less, the result is your grade on the work marked so far. Rows are saved in this browser.</p></div><div class="result" id="out"></div>`},
 calc(){let sw=0,ws=0;this.rows=this.rows.map((r,i)=>{const n=$('#grn'+i).value,s=parseFloat($('#grs'+i).value),w=parseFloat($('#grw'+i).value);if(isFinite(s)&&isFinite(w)&&w>0){sw+=s*w;ws+=w}return[n,isFinite(s)?s:'',isFinite(w)?w:'']});store.set('grade',this.rows);
  const g=ws?sw/ws:NaN;
  $('#out').innerHTML=`<span class="label">Current grade</span><div class="big"><em>${isFinite(g)?num(g,2)+'%':'—'}</em></div>${kv([['Letter grade',isFinite(g)?letter(g):'—'],['Weight entered',num(ws,1)+'%'],['Weight still to come',ws<100?num(100-ws,1)+'%':'None']])}${ws>0&&ws<100?`<a class="copy" href="/final-grade-calculator/">What do I need on the final?</a>`:''}${copyBtn}`;
  return isFinite(g)?`Grade ${num(g,2)}% (${letter(g)})`:''},
 after(){$('#gradd').onclick=()=>{this.calc();this.rows.push(['New assignment','',10]);open('grade')};document.querySelectorAll('[data-gdel]').forEach(b=>b.onclick=()=>{this.calc();this.rows.splice(+b.dataset.gdel,1);open('grade')})}},

{id:'finalgrade',cat:'Students',name:'Final grade',kw:'final grade calculator final exam what do i need on my final to pass get an a b grade needed',desc:'The score you need on the final exam to reach your target grade.',
 render(){return `<div class="inputs"><div class="row">${field('fgc','Current grade',84,{unit:'%'})}${field('fgw','Final exam weight',25,{unit:'%'})}${field('fgt','Grade you want',85,{unit:'%'})}</div>
  <div class="actions">${[['A',90],['B',80],['C',70],['D',60]].map(([l,x])=>`<button class="btn" type="button" data-fgt="${x}">${l} (${x}%)</button>`).join('')}</div>
  <p class="hint">Find your current grade with the <a href="/grade-calculator/">grade calculator</a>. The final exam weight is in your course syllabus.</p><div id="fgtable"></div></div><div class="result" id="out"></div>`},
 calc(){const c=v('fgc'),w=v('fgw')/100,t=v('fgt');if(!(w>0&&w<=1)||!isFinite(c)||!isFinite(t)){$('#out').innerHTML='<span class="label">Result</span><p class="hint">Enter a final exam weight between 1 and 100%.</p>';$('#fgtable').innerHTML='';return''}
  const need=x=>(x-c*(1-w))/w,n=need(t);
  const msg=n>100?`Even 100% on the final gives ${num(c*(1-w)+100*w,1)}%.`:n<=0?`You already have it, even with 0% on the final.`:`Score at least ${num(n,1)}% on the final.`;
  $('#fgtable').innerHTML=`<div class="tbl"><table><thead><tr><th>Target</th><th>You need on the final</th></tr></thead><tbody>${[['A',90],['B',80],['C',70],['D',60]].map(([l,x])=>{const r=need(x);return`<tr><td>${l} (${x}%)</td><td>${r>100?'Not reachable':r<=0?'Already secured':num(r,1)+'%'}</td></tr>`}).join('')}</tbody></table></div>`;
  $('#out').innerHTML=`<span class="label">You need on the final</span><div class="big"><em>${n>100?'Not reachable':n<=0?'0%':num(n,1)+'%'}</em></div><p class="hint" style="color:var(--ink)">${msg}</p>${kv([['Grade if you score 100%',num(c*(1-w)+100*w,1)+'%'],['Grade if you score 70%',num(c*(1-w)+70*w,1)+'%'],['Grade if you score 0%',num(c*(1-w),1)+'%']])}${copyBtn}`;
  return n>100?`${t}% is not reachable`:`Need ${num(Math.max(0,n),1)}% on the final`},
 after(){document.querySelectorAll('[data-fgt]').forEach(b=>b.onclick=()=>{$('#fgt').value=b.dataset.fgt;update()})}}
