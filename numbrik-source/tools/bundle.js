// Splits src/app.js into one small bundle per calculator (core + that tool) plus core.js for pages without a tool.
const fs=require('fs'),path=require('path');

const acorn=require('acorn'),{minify}=require('terser');
const [,,inFile,outDir]=process.argv;
const src=fs.readFileSync(inFile,'utf8');
const ast=acorn.parse(src,{ecmaVersion:2022});
let arr=null;
(function walk(n){if(!n||typeof n!=='object'||arr)return;if(n.type==='VariableDeclarator'&&n.id&&n.id.name==='TOOLS'){arr=n.init;return}for(const k in n){const v=n[k];if(Array.isArray(v))v.forEach(walk);else if(v&&typeof v.type==='string')walk(v)}})(ast);
const val=(e,k)=>{const p=e.properties.find(p=>p.key&&p.key.name===k);return p&&p.value.type==='Literal'?p.value.value:''};
const tools=arr.elements.map(e=>({id:val(e,'id'),code:src.slice(e.start,e.end),idx:{id:val(e,'id'),name:val(e,'name'),kw:val(e,'kw'),desc:val(e,'desc'),cat:val(e,'cat')}}));
let core=src.slice(0,arr.start)+'__TOOLS__'+src.slice(arr.end);
if(!core.includes('return s?TOOLS.filter('))throw new Error('search hook missing');
core=core.replace('return s?TOOLS.filter(','return s?IDX.filter(').replace('const TOOLS=__TOOLS__','const IDX='+JSON.stringify(tools.map(t=>t.idx))+';const TOOLS=__TOOLS__');
fs.mkdirSync(outDir,{recursive:true});
(async()=>{let total=0;
  for(const t of [{id:'core',code:''},...tools]){const js=core.replace('__TOOLS__','['+t.code+']');const r=await minify(js,{compress:true,mangle:true});if(!r.code)throw new Error('minify '+t.id);fs.writeFileSync(path.join(outDir,t.id+'.js'),r.code);total+=r.code.length}
  console.log('bundles',tools.length+1,'avg',Math.round(total/(tools.length+1)),'bytes');})().catch(e=>{console.error(e);process.exit(1)});
