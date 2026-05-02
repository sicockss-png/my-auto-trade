import asyncio
from playwright.async_api import async_playwright

async def run_auto_buy():
    # 설정 정보
    USER_ID = "9714" 
    USER_PW = "0000" 
    STOCK_NAME = "서연탑메탈"  # 시공테크에서 서연탑메탈로 변경

    async with async_playwright() as p:
        # 화면 크기를 넉넉하게 설정하여 버튼이 가려지지 않게 함
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1920, "height": 1080})
        page = await context.new_page()
        
        try:
            print(f"[{STOCK_NAME}] 매수 프로세스 시작...")
            
            # 1. 로그인 페이지 접속
            await page.goto("https://bs3-wts.com/Login", wait_until="networkidle")
            await page.fill('input[name="userid"]', USER_ID)
            await page.fill('input[name="password"]', USER_PW)
            await page.click('button[type="submit"]')
            
            # 로그인 후 메인화면 로딩 대기
            await page.wait_for_timeout(10000) # 요청하신 10초 대기 추가
            
            # 2. 종목 검색
            search_input = page.locator('input[placeholder*="검색"]').first
            await search_input.fill(STOCK_NAME)
            await page.wait_for_timeout(3000) # 검색 결과 나타날 때까지 대기
            await page.click(f'text="{STOCK_NAME}"')
            
            # 3. 매수 주문 시도
            # 화면 로딩과 버튼 활성화를 위해 여기서도 10초를 기다립니다.
            print("주문 버튼 대기 중 (10초)...")
            await page.wait_for_timeout(10000) 
            
            # "+" 버튼 클릭 시도
            plus_button = page.locator('button:has-text("+")').last
            await plus_button.click()
            await page.wait_for_timeout(2000)
            
            # "매수" 버튼 클릭
            buy_button = page.locator('button:has-text("매수")').last
            await buy_button.click()
            await page.wait_for_timeout(2000)
            
            # 4. 최종 확인 창 클릭
            confirm = page.locator('button:has-text("확인"), button:has-text("승인")').first
            if await confirm.is_visible():
                await confirm.click()
                print(f"★ {STOCK_NAME} 주문 완료")
            else:
                print("확인 버튼이 보이지 않습니다. 이미 주문되었거나 화면 확인이 필요합니다.")
                
        except Exception as e:
            print(f"오류 발생: {e}")
            # 에러 발생 시 현재 화면을 찍어두면 나중에 분석하기 좋습니다.
            # await page.screenshot(path="error_screenshot.png")
            
        finally:
            await browser.close()
            print("프로세스 종료")

if __name__ == "__main__":
    asyncio.run(run_auto_buy())
