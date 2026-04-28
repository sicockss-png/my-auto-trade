import asyncio
from playwright.async_api import async_playwright

async def run_auto_buy():
    USER_ID = "9714" 
    USER_PW = "0000" 
    STOCK_NAME = "시공테크"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1280, "height": 720})
        page = await context.new_page()
        
        try:
            print("매수 프로세스 시작...")
            await page.goto("https://bs3-wts.com/Login", wait_until="networkidle")
            await page.fill('input[name="userid"]', USER_ID)
            await page.fill('input[name="password"]', USER_PW)
            await page.click('button[type="submit"]')
            await page.wait_for_timeout(5000)
            
            search_input = page.locator('input[placeholder*="검색"]').first
            await search_input.fill(STOCK_NAME)
            await page.wait_for_timeout(2000)
            await page.click(f'text="{STOCK_NAME}"')
            
            await page.locator('button:has-text("+")').last.click()
            await page.locator('button:has-text("매수")').last.click()
            
            confirm = page.locator('button:has-text("확인"), button:has-text("승인")').first
            await confirm.click()
            print("★ 주문 완료")
        except Exception as e:
            print(f"오류: {e}")
        finally:
            await browser.close()

asyncio.run(run_auto_buy())
