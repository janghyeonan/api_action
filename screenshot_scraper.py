#!/usr/bin/env python3
"""
웹사이트 스크린샷 자동화 스크립트
Playwright를 사용하여 헤드리스 브라우저로 여러 웹사이트의 스크린샷을 촬영합니다.
"""

import asyncio
import os
import time
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright
import sys

class WebsiteScreenshotCapture:
    def __init__(self, output_dir="screenshots"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 대상 웹사이트들
        self.websites = [
            {"name": "naver", "url": "https://www.naver.com", "wait_selector": "#NM_FAVORITE"},
            {"name": "coupang", "url": "https://www.coupang.com", "wait_selector": "header"},
            {"name": "musinsa", "url": "https://www.musinsa.com", "wait_selector": "#header"},
            {"name": "google", "url": "https://www.google.com", "wait_selector": "input[name='q']"}
        ]
    
    async def capture_website(self, browser, site_info, delay=3):
        """개별 웹사이트 스크린샷 캡처"""
        site_name = site_info["name"]
        site_url = site_info["url"]
        wait_selector = site_info.get("wait_selector")
        
        print(f"📸 {site_name.upper()} 스크린샷 캡처 시작...")
        
        try:
            # 새 페이지 생성
            page = await browser.new_page()
            
            # 뷰포트 크기 설정 (1920x1080)
            await page.set_viewport_size({"width": 1920, "height": 1080})
            
            # 사이트 접속
            print(f"🌐 {site_url} 접속 중...")
            await page.goto(site_url, wait_until="networkidle", timeout=30000)
            
            # 특정 요소가 로드될 때까지 대기 (선택적)
            if wait_selector:
                try:
                    await page.wait_for_selector(wait_selector, timeout=10000)
                    print(f"✅ {site_name}: 페이지 로딩 완료")
                except:
                    print(f"⚠️ {site_name}: 특정 요소 로딩 실패, 계속 진행")
            
            # 페이지가 완전히 로드되도록 추가 대기
            await page.wait_for_load_state("networkidle")
            
            # 딜레이 적용
            print(f"⏱️ {delay}초 대기 중...")
            await asyncio.sleep(delay)
            
            # 스크린샷 파일명 생성
            screenshot_filename = f"{self.timestamp}_{site_name}.png"
            screenshot_path = self.output_dir / screenshot_filename
            
            # 전체 페이지 스크린샷 촬영
            await page.screenshot(
                path=str(screenshot_path),
                full_page=True,
                type="png"
            )
            
            print(f"✅ {site_name} 스크린샷 저장: {screenshot_path}")
            
            # 페이지 정보 수집
            page_info = {
                "name": site_name,
                "url": site_url,
                "title": await page.title(),
                "screenshot_path": str(screenshot_path),
                "file_size": os.path.getsize(screenshot_path),
                "timestamp": datetime.now().isoformat()
            }
            
            await page.close()
            return page_info
            
        except Exception as e:
            print(f"❌ {site_name} 스크린샷 캡처 실패: {str(e)}")
            return {
                "name": site_name,
                "url": site_url,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def capture_all_websites(self, delay=3):
        """모든 웹사이트의 스크린샷을 순차적으로 캡처"""
        print("🚀 웹사이트 스크린샷 캡처 시작")
        print(f"📁 출력 디렉토리: {self.output_dir}")
        print(f"🕐 타임스탬프: {self.timestamp}")
        print("=" * 50)
        
        results = []
        
        async with async_playwright() as p:
            # 브라우저 시작 (헤드리스 모드)
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-gpu',
                    '--no-first-run',
                    '--no-zygote',
                    '--single-process',
                    '--disable-extensions'
                ]
            )
            
            try:
                # 각 웹사이트를 순차적으로 처리
                for i, site_info in enumerate(self.websites, 1):
                    print(f"\n[{i}/{len(self.websites)}] {site_info['name'].upper()} 처리 중...")
                    
                    result = await self.capture_website(browser, site_info, delay)
                    results.append(result)
                    
                    # 사이트 간 간격
                    if i < len(self.websites):
                        print(f"⏳ 다음 사이트까지 1초 대기...")
                        await asyncio.sleep(1)
                
            finally:
                await browser.close()
        
        return results
    
    def generate_report(self, results):
        """결과 리포트 생성"""
        report_file = self.output_dir / f"{self.timestamp}_report.txt"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(f"웹사이트 스크린샷 캡처 리포트\n")
            f.write(f"생성 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"타임스탬프: {self.timestamp}\n")
            f.write("=" * 60 + "\n\n")
            
            successful = 0
            failed = 0
            
            for result in results:
                if 'error' in result:
                    failed += 1
                    f.write(f"❌ {result['name'].upper()} - 실패\n")
                    f.write(f"   URL: {result['url']}\n")
                    f.write(f"   오류: {result['error']}\n")
                else:
                    successful += 1
                    f.write(f"✅ {result['name'].upper()} - 성공\n")
                    f.write(f"   URL: {result['url']}\n")
                    f.write(f"   제목: {result['title']}\n")
                    f.write(f"   파일: {result['screenshot_path']}\n")
                    f.write(f"   크기: {result['file_size']:,} bytes\n")
                
                f.write(f"   시간: {result['timestamp']}\n\n")
            
            f.write("=" * 60 + "\n")
            f.write(f"총 {len(results)}개 사이트 처리\n")
            f.write(f"성공: {successful}개, 실패: {failed}개\n")
        
        print(f"\n📄 리포트 생성: {report_file}")
        return report_file

async def main():
    """메인 실행 함수"""
    # 명령행 인자에서 딜레이 시간 가져오기 (기본값: 3초)
    delay = 3
    if len(sys.argv) > 1:
        try:
            delay = int(sys.argv[1])
        except ValueError:
            print("⚠️ 잘못된 딜레이 값입니다. 기본값 3초를 사용합니다.")
    
    print(f"⏱️ 딜레이 설정: {delay}초")
    
    # 스크린샷 캡처 실행
    capturer = WebsiteScreenshotCapture()
    results = await capturer.capture_all_websites(delay=delay)
    
    # 결과 출력
    print("\n" + "=" * 50)
    print("📊 캡처 결과 요약")
    print("=" * 50)
    
    successful = 0
    failed = 0
    
    for result in results:
        if 'error' in result:
            failed += 1
            print(f"❌ {result['name'].upper()}: {result['error']}")
        else:
            successful += 1
            print(f"✅ {result['name'].upper()}: {result['title']}")
    
    print(f"\n총 {len(results)}개 사이트 처리 완료")
    print(f"성공: {successful}개, 실패: {failed}개")
    
    # 리포트 생성
    report_file = capturer.generate_report(results)
    
    print(f"\n📁 스크린샷 저장 위치: {capturer.output_dir}")
    print("🎉 모든 작업이 완료되었습니다!")

if __name__ == "__main__":
    asyncio.run(main())
