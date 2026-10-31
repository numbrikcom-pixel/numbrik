import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch();pg=await b.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        B='http://localhost:8765'
        await pg.goto(B+'/take-home-pay-calculator/');
        await pg.click('#pfs button[data-v="mfj"]');await pg.fill('#pg','100000');await pg.fill('#pp','6000');await pg.fill('#ps','5');await pg.wait_for_timeout(80)
        print('paycheck mfj',(await pg.inner_text('#out .kv')).split('\n')[1])
        await pg.goto(B+'/concrete-calculator/');await pg.click('#cshape button[data-v="hole"]');await pg.wait_for_timeout(80);print('holes',await pg.inner_text('#out .big'),(await pg.inner_text('#out .kv')).split('\n')[3])
        await pg.click('#cunit button[data-v="m"]');await pg.wait_for_timeout(80);print('holes m',await pg.inner_text('#out .big'))
        await pg.goto(B+'/paint-calculator/');await pg.select_option('#pceil','1');await pg.wait_for_timeout(80);print('paint+ceil',await pg.inner_text('#out .big'))
        await pg.goto(B+'/random-number-generator/');await pg.fill('#rmin','1');await pg.fill('#rmax','49');await pg.fill('#rn','6');await pg.wait_for_timeout(80);print('random 6/49',await pg.inner_text('#out .big'), await pg.evaluate("document.querySelectorAll('#rlist .time-chip').length"))
        await pg.fill('#rn','60');await pg.wait_for_timeout(80);print('too many ->',await pg.inner_text('#out'))
        # uniformity check
        d=await pg.evaluate("(()=>{const t=TOOLS=null;return 1})()") if False else None
        await pg.goto(B+'/coin-flip/');await pg.fill('#cfn','1000');await pg.wait_for_timeout(80);print('coin',await pg.inner_text('#out .big'))
        await pg.click('#cfgo');await pg.wait_for_timeout(50);print('coin again',await pg.inner_text('#out .big'))
        print('errors',errs)
        await b.close()
asyncio.run(main())
