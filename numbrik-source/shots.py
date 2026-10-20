import asyncio, os, sys, subprocess, re, json
from playwright.async_api import async_playwright
D=os.path.abspath('dist'); F=D+'/assets/fonts/'
OG=f"""<html><head><style>
@font-face{{font-family:B;src:url(file://{F}bricolage-700.woff2)}}@font-face{{font-family:P;src:url(file://{F}plex-sans-400.woff2)}}@font-face{{font-family:M;src:url(file://{F}plex-mono-500.woff2)}}
body{{margin:0;width:1200px;height:630px;background:#F3F5F8;font-family:P;display:flex;flex-direction:column;justify-content:space-between;padding:72px;box-sizing:border-box;color:#121A2B}}
.top{{display:flex;align-items:center;gap:20px;font-family:B;font-size:52px}}
h1{{font-family:B;font-size:84px;line-height:1;margin:0;letter-spacing:-2px;max-width:900px}}
.row{{display:flex;gap:14px;font-family:M;font-size:26px}}.row span{{background:#fff;border:2px solid #D3D9E3;border-radius:999px;padding:10px 22px}}
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
