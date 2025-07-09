import random
import time
from config import root_folder, google_profile_directory
from playwright.sync_api import sync_playwright
from datetime import datetime
import pandas as pd

invalid_symbols = pd.read_csv('invalid_symbols.csv').symbol.unique()



def is_valid_symbol(symbol):
    return symbol not in invalid_symbols

def wait_then_click(page, selector):
    page.wait_for_selector(selector)
    delay_randomized()
    page.click(selector)

def delay_randomized(seconds: int = 2):
    delay = random.uniform(0.5, seconds)
    time.sleep(delay)

def extract_ohlcv(page):
    fields = ["Date", "Time", "Open", "High", "Low", "Close", "Vol"]
    result = {'date': None}
    for label in fields:
        try:
            item = page.locator(
                f'div.values-_gbYDtbd >> div.item-_gbYDtbd:has(div[data-test-id-value-title="{label}"])'
            )
            value = item.locator("span").first.inner_text().replace(',', '').replace(' ', '')
            result[label.lower()] = value
        except Exception:
            result[label.lower()] = None

    raw_date = result.get("date")
    if raw_date:
        try:
            parsed_date = datetime.strptime(raw_date, "%a %d %b '%y")
            result["date"] = parsed_date.strftime("%Y-%m-%d")
        except Exception:
            pass
    return result

def focus_to_canvas(page):
    canvas = page.locator('canvas[data-name="pane-top-canvas"]')
    box = canvas.bounding_box()
    if not box:
        print("❗ Cannot locate chart canvas.")
        return False
    page.mouse.click(box["x"] + box["width"] - 300, box["y"] + box["height"] - 300)
    return True

def click_interval_option_by_value(page, data_value:str):
    try:
        button = page.locator('#header-toolbar-intervals').first.locator('button[data-value="%s"]' % data_value)
        button.click()
        return True
    except Exception as e:
        print(f"⚠️ Error clicking interval option with data-value '{data_value}': {e}")
    return False


def is_valid_page(page, symbol, browser):
    if page.locator(".errorCard__message-S9sXvhAu", has_text="Invalid symbol").is_visible():
        print("Invalid symbol error exists.")
        browser.close()
        raise Exception("Invalid symbol error exists: " + symbol)
        

def launch_browser(symbol, headless=True, free_option=None):
    p = sync_playwright().start()
    browser = p.chromium.launch_persistent_context(
        user_data_dir=rf'{google_profile_directory} {free_option.profile_number if free_option else 18}',
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
        downloads_path=root_folder,
        accept_downloads=True,
        channel='chrome',
        headless=headless,
        args=[
                # '--disable-web-security',
                # '--disable-features=IsolateOrigins,site-per-process',
                # '--disable-blink-features=AutomationControlled',
                # '--disable-infobars',
                # '--no-sandbox',/
                # '--no-first-run',
                # '--disable-setuid-sandbox',
                # '--disable-dev-shm-usage',
        ]
    )
    page = browser.new_page()
    page.goto(f"https://www.tradingview.com/chart/?symbol={symbol}")
    
    print("⏳ Waiting for TradingView chart to load...")
    page.wait_for_timeout(3000)
    
    return p, browser, page  # 반드시 나중에 종료해야 함


def get_ohlcv_in_chart(
    symbol,
    freq='1D',
    headless=True,
    free_option=None
):
    p, browser, page = launch_browser(symbol, headless, free_option)
    
    is_valid_page(page, symbol, browser)
    if freq:
        click_interval_option_by_value(page, freq)
    
    date = datetime.now().strftime('%Y%m%d_%H%M%S')
    save_mid_path ='\\..' + '\\dumdum\\' + date +'_' ## remove useless filename using '\\..'
        
        
    

    browser.close()
    p.stop()  # 반드시 종료해야 함