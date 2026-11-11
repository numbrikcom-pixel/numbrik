import asyncio, os, sys, subprocess, re, json
from playwright.async_api import async_playwright
D=os.path.abspath('dist'); F=D+'/assets/fonts/'
import base64 as _b64
def _fu(n): return ('data:font/woff2;base64,'+_b64.b64encode(open(F+n,'rb').read()).decode()) if os.path.exists(F+n) else 'about:blank'
FB,FP,FM=_fu('bricolage-700.woff2'),_fu('plex-sans-400.woff2'),_fu('plex-mono-500.woff2')
OG=f"""<html><head><style>
@font-face{{font-family:B,'Liberation Sans',Arial,sans-serif;src:url({FB})}}@font-face{{font-family:P,'Liberation Sans',Arial,Helvetica,sans-serif;src:url({FP})}}@font-face{{font-family:M,'DejaVu Sans Mono','Liberation Mono',monospace;src:url({FM})}}
body{{margin:0;width:1200px;height:630px;background:#F3F5F8;font-family:P,'Liberation Sans',Arial,Helvetica,sans-serif;display:flex;flex-direction:column;justify-content:space-between;padding:72px;box-sizing:border-box;color:#121A2B}}
.top{{display:flex;align-items:center;gap:20px;font-family:B,'Liberation Sans',Arial,sans-serif;font-size:52px}}
h1{{font-family:B,'Liberation Sans',Arial,sans-serif;font-size:84px;line-height:1;margin:0;letter-spacing:-2px;max-width:900px}}
.row{{display:flex;gap:14px;font-family:M,'DejaVu Sans Mono','Liberation Mono',monospace;font-size:26px}}.row span{{background:#fff;border:2px solid #D3D9E3;border-radius:999px;padding:10px 22px}}
</style></head><body><div class="top">{open('build.py').read().split("FAVICON = '")[1].split("'")[0].replace('viewBox','width="72" height="72" viewBox')}Numbrik</div>
<h1>Free calculators that answer as you type</h1><div class="row"><span>Time card</span><span>GPA</span><span>Mortgage</span><span>Calories</span></div></body></html>"""
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':1200,'height':630}); await pg.set_content(OG); await pg.wait_for_timeout(300)
        await pg.screenshot(path=D+'/og.png')
        fav=open(D+'/favicon.svg').read()
        for size,name in [(180,'apple-touch-icon.png'),(32,'favicon-32.png')]:
            pg=await b.new_page(viewport={'width':size,'height':size})
            await pg.set_content(f'<body style="margin:0">{fav.replace("<svg ",f"<svg width=\"{size}\" height=\"{size}\" ")}</body>'); await pg.screenshot(path=D+'/'+name,omit_background=True)
        await b.close()
asyncio.run(main())

OGT="""<html><head><style>
@font-face{{font-family:B,'Liberation Sans',Arial,sans-serif;src:url({FB})}}@font-face{{font-family:P,'Liberation Sans',Arial,Helvetica,sans-serif;src:url({FP})}}@font-face{{font-family:M,'DejaVu Sans Mono','Liberation Mono',monospace;src:url({FM})}}
body{{margin:0;width:1200px;height:630px;background:#F3F5F8;font-family:P,'Liberation Sans',Arial,Helvetica,sans-serif;display:flex;flex-direction:column;justify-content:space-between;padding:64px 72px;box-sizing:border-box;color:#121A2B}}
.top{{display:flex;align-items:center;gap:18px;font-family:B,'Liberation Sans',Arial,sans-serif;font-size:44px}}.cat{{margin-left:auto;font-family:M,'DejaVu Sans Mono','Liberation Mono',monospace;font-size:24px;color:#2340C9;background:#fff;border:2px solid #D3D9E3;border-radius:999px;padding:8px 20px}}
h1{{font-family:B,'Liberation Sans',Arial,sans-serif;font-size:{fs}px;line-height:1.02;margin:0 0 18px;letter-spacing:-2px;max-width:1050px}}p{{font-size:34px;margin:0;color:#3B4660;max-width:1000px}}
.row{{display:flex;gap:14px;font-family:M,'DejaVu Sans Mono','Liberation Mono',monospace;font-size:24px;color:#121A2B}}.row span{{background:#fff;border:2px solid #D3D9E3;border-radius:999px;padding:9px 20px}}
</style></head><body><div class="top">{logo}Numbrik<span class="cat">{cat}</span></div><div><h1>{name}</h1><p>{desc}</p></div>
<div class="row"><span>Free</span><span>No sign-up</span><span>Shows the formula</span><span>numbrik.com</span></div></body></html>"""
async def og_pages():
    import html as _h
    items=json.load(open('og_list.json')); os.makedirs(D+'/og',exist_ok=True)
    logo=open('build.py').read().split("FAVICON = '")[1].split("'")[0].replace('viewBox','width="60" height="60" viewBox')
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1200,'height':630})
        for it in items:
            n=it['name']; fs=96 if len(n)<=22 else 80 if len(n)<=30 else 68
            await pg.set_content(OGT.format(FB=FB,FP=FP,FM=FM,fs=fs,logo=logo,cat=_h.escape(it['cat']),name=_h.escape(n),desc=_h.escape(it['desc'])))
            await pg.wait_for_timeout(60); await pg.screenshot(path=f"{D}/og/{it['slug']}.png")
        await b.close()
asyncio.run(og_pages())
