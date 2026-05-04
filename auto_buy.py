import asyncio
from playwright.async_api import async_playwright

async def run_auto_buy():
    # 설정 정보
    USER_ID = "9714" 
    USER_PW = "0000" 
    STOCK_NAME = "서연탑메탈"

    async with async_playwright() as p:
        # 화면 크기를 넉넉하게 설정
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1280, "height": 1024})
        page = await context.new_page()
        
        try:
            print(f"[{STOCK_NAME}] 매수 프로세스 시작...")
            
            # 1. 로그인 페이지 접속
            await page.goto("https://bs3-wts.com/Login", wait_until="networkidle")
            await page.fill('input[name="userid"]', USER_ID)
            await page.fill('input[name="password"]', USER_PW)
            await page.click('button[type="submit"]')
            
            # 로그인 후 메인화면 로딩 대기
            await page.wait_for_timeout(5000) 
            
            # 2. 종목 검색
            search_input = page.locator('input[placeholder*="검색"]').first
            await search_input.fill(STOCK_NAME)
            await page.wait_for_timeout(2000)
            await page.click(f'text="{STOCK_NAME}"')
            
            # 3. 매수 주문 시도 (수정된 로직)
            print("주문 페이지 로딩 대기 중...")
            await page.wait_for_timeout(5000) 
            
            # [시장가] 버튼 클릭 - 가격 입력 생략
            market_price_btn = page.locator('button:has-text("시장가")')
            await market_price_btn.click()
            print("- 시장가 선택 완료")
            await page.wait_for_timeout(1000)

            # [10%] 버튼 클릭 - 비중 설정
            percent_10_btn = page.locator('button:has-text("10%")')
            await percent_10_btn.click()
            print("- 투자 비중 10% 설정 완료")
            await page.wait_for_timeout(1000)
            
            # 하단 [매수] 버튼 클릭
            # '주문' 탭 안에 있는 빨간색 '매수' 버튼을 정확히 클릭합니다.
            buy_button = page.locator('button:has-text("매수")').last
            await buy_button.click()
            print("- 매수 버튼 클릭 완료")
            await page.wait_for_timeout(2000)
            
            # 4. 최종 확인 창 클릭 (팝업이 뜨는 경우 처리)
            confirm = page.locator('button:has-text("확인"), button:has-text("승인")').first
            if await confirm.is_visible():
                await confirm.click()
                print(f"★ {STOCK_NAME} 최종 주문 완료")
            else:
                print("추가 확인 창 없음 - 주문 완료 확인")
                
        except Exception as e:
            print(f"오류 발생: {e}")
            
        finally:
            await browser.close()
            print("프로세스 종료")

if __name__ == "__main__":
    asyncio.run(run_auto_buy())
