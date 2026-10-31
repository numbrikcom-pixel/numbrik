import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':1366,'height':900});await pg.goto('http://localhost:8765/');await pg.wait_for_timeout(300);await pg.screenshot(path='home.png')
        await pg.goto('http://localhost:8765/time-card-calculator/');await pg.wait_for_timeout(300);await pg.screenshot(path='tc.png')
        c=await b.new_context(viewport={'width':390,'height':844},color_scheme='dark',device_scale_factor=2);m=await c.new_page()
        await m.goto('http://localhost:8765/gpa-calculator/');await m.wait_for_timeout(300);await m.screenshot(path='gpa_m.png',full_page=False)
        await b.close()
asyncio.run(main())
