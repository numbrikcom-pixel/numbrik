import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch();pg=await b.new_page()
        await pg.goto('http://localhost:8765/age-calculator/')
        for dob,on in [('2025-01-31','2025-03-01'),('1994-03-17','2026-10-20'),('2000-02-29','2026-03-01'),('1990-05-31','2026-06-30'),('2010-12-25','2026-12-24')]:
            await pg.fill('#ab',dob);await pg.fill('#ao',on);await pg.wait_for_timeout(50)
            print(dob,on,'->',(await pg.inner_text('#out .kv')).split('\n')[1])
        await b.close()
asyncio.run(main())
