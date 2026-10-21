import asyncio, re
from playwright.async_api import async_playwright
urls=re.findall(r'<loc>https://numbrik.com(.*?)</loc>',open('dist/sitemap.xml').read())
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); bad=0
        for u in urls:
            pg=await b.new_page(viewport={'width':1280,'height':900}); errs=[]
            pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('console',lambda m:m.type=='error' and errs.append(m.text))
            pg.on('requestfailed',lambda r:('googletagmanager' not in r.url) and errs.append('FAIL '+r.url))
            await pg.goto('http://localhost:8765'+u); await pg.wait_for_timeout(250)
            big=await pg.evaluate("document.querySelector('#out .big')?.textContent||''")
            words=await pg.evaluate("document.querySelector('main').innerText.split(/\\s+/).length")
            ow=await pg.evaluate("document.documentElement.scrollWidth>innerWidth")
            title=await pg.title()
            if errs or ow: bad+=1
            print(f"{u:34} {big[:18]:18} words={words:4} {'OVERFLOW' if ow else ''} {errs[:2] if errs else ''}  [{len(title)}] {title}")
            await pg.close()
        # mobile overflow + interactions
        pg=await b.new_page(viewport={'width':380,'height':800})
        for u in urls[:20]:
            await pg.goto('http://localhost:8765'+u); await pg.wait_for_timeout(150)
            if await pg.evaluate("document.documentElement.scrollWidth>innerWidth+1"): print('MOBILE OVERFLOW',u); bad+=1
        await pg.goto('http://localhost:8765/'); await pg.fill('#q','overtime'); r=await pg.inner_text('#qres'); print('search ->',r.split('\n')[0])
        await pg.press('#q','Enter'); await pg.wait_for_load_state(); print('enter ->',pg.url)
        await pg.select_option('#region','AU'); await pg.wait_for_timeout(100); print('AU otat=',await pg.input_value('#otat'), await pg.inner_text('#out .big'))
        await pg.click('#themeBtn'); print('theme',await pg.evaluate("document.documentElement.dataset.theme"))
        await pg.goto('http://localhost:8765/gpa-calculator/'); print('theme persists',await pg.evaluate("document.documentElement.dataset.theme"), 'region persists', await pg.input_value('#region'))
        await pg.click('#gadd'); print('gpa rows', await pg.evaluate("document.querySelectorAll('#gbody tr').length"))
        await b.close(); print('PROBLEMS:',bad)
asyncio.run(main())
