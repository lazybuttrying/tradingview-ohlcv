import shutil
from playwright.sync_api import sync_playwright
from playwright.sync_api import Page
import random
import os
import pandas as pd
import logging
import time
from dataclasses import dataclass
from datetime import datetime
import sys
sys.stdout.reconfigure(encoding='utf-8')
logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
    filename='ohlcv_premium_spot.log', filemode='a')
LOGGER = logging.getLogger(__name__)

google_profile_directory = r'C:\Users\Administrator\AppData\Local\Google\Chrome\User Data\Profile'
root_folder = 'F:\\tradingview'  # Adjust this path as needed

@dataclass
class freqOption:
    d1: str = '1D'  # 1 day
    m1: str = '1'  # 1 minute
    m15: str = '15'
    m30: str = '30'  # 30 minutes
    h1: str = '60'  # 1 hour
    

def click_freq_button_in_header_toolbar(page):
    try:
        button = page.locator('#header-toolbar-intervals button[aria-label="1 day"]').first
        if button.is_visible():
            print("🕒 Clicking '1 day' button inside header-toolbar-intervals...")
            button.click()
            time.sleep(0.5)
        else:
            print("⚠️ '1 day' button inside header-toolbar-intervals not visible.")
    except Exception as e:
        print(f"⚠️ Error clicking '1 day' button inside header-toolbar-intervals: {e}")

# <button aria-label="1 day" role="radio" aria-checked="false" data-value="1D" tabindex="-1" type="button" class="button-S_1OCXUK button-GwQQdU8S apply-common-tooltip isInteractive-GwQQdU8S isGrouped-GwQQdU8S accessible-GwQQdU8S" data-tooltip="1 day"><div class="js-button-text text-GwQQdU8S"><div class="value-gwXludjS">D</div></div></button>

def click_interval_option_by_value(page, data_value:str):
    try:
        button = page.locator('#header-toolbar-intervals').first.locator('button[data-value="%s"]' % data_value)
        button.click()
        return True
    except Exception as e:
        print(f"⚠️ Error clicking interval option with data-value '{data_value}': {e}")
    return False


def extract_ohlcv(page):
    page.wait_for_selector("div.values-_gbYDtbd")
    delay_randomized()
    fields = ["Date", "Time", "Open", "High", "Low", "Close", "Vol"]
    result = {}
    for label in fields:
        try:
            item = page.locator(f'div.values-_gbYDtbd >> div.item-_gbYDtbd:has(div[data-test-id-value-title="{label}"])')
            value_span = item.locator("span").first
            value = value_span.inner_text().replace(',', '').replace(' ', '')  # narrow no-break space 제거
            result[label.lower()] = value
        except Exception as e:
            print(f"❌ Failed to extract {label}: {e}")
            result[label.lower()] = None

    raw_date = result.get("date")
    if raw_date:
        try:
            # 예: "Fri 27 Jun '25" → datetime.date(2025, 6, 27)
            parsed_date = datetime.strptime(raw_date, "%a %d %b '%y")
            result["date"] = parsed_date.strftime("%Y-%m-%d")  # ISO 포맷으로 변환
        except Exception as e:
            print(f"❌ Failed to parse date: {e}")
            result["date"] = None 

    return result



ZINDEX_HELPER = """
() => {
  const elements = Array.from(document.querySelectorAll('*')).filter(el => {
    const z = parseInt(getComputedStyle(el).zIndex);
    return !isNaN(z) && z > %d;
  });
  return elements;
}
"""

def has_high_zindex_elements(page, threshold=3):
    return page.evaluate(ZINDEX_HELPER % threshold).__len__() > 0

def remove_high_zindex_elements(page, threshold=3):
    print("High z-index elements detected, removing them...")
    page.evaluate(f"""
        const elements = ({ZINDEX_HELPER % threshold})();
        elements.forEach(el => el.remove());
    """)
    
    
def focus_to_canvas(page: Page):
    canvas = page.locator('canvas[data-name="pane-top-canvas"]')
    box = canvas.bounding_box()
    if not box:
        print("❗ Error: Unable to find the chart canvas. Exiting.")
        return False
    print("🖱 Clicking chart canvas to focus...")
    page.mouse.click(
        box["x"] + box["width"] - 300, 
        box["y"] + box["height"] - 300
    )
    delay_randomized(0.5)
    return True

def wait_then_click(page, selector):
    page.wait_for_selector(selector)
    delay_randomized()
    page.click(selector)

def delay_randomized(seconds: int = 2):
    delay = random.uniform(0.5, seconds)
    time.sleep(delay)

def get_ohlcv_in_chart(symbol='CRYPTOCOM:BTCUSD', freq=None, free_option=None, headless=True):
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=rf'{google_profile_directory} {free_option.profile_number if free_option else 18}',
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
            downloads_path=root_folder,
            accept_downloads=True,
            channel='chrome',
            headless=headless,
            args=[
  
            ]
        )
        page = browser.new_page()
        page.goto(f"https://www.tradingview.com/chart/?symbol={symbol}")
        


        if page.locator(".errorCard__message-S9sXvhAu", has_text="Invalid symbol").is_visible():
            print("Invalid symbol error exists.")
            browser.close()
            raise Exception("Invalid symbol error exists: " + symbol)
        
        if freq:
            click_interval_option_by_value(page, freq)
        
        date = datetime.now().strftime('%Y%m%d_%H%M%S')
        save_mid_path ='\\..' + '\\dumdum\\' + date +'_' ## remove useless filename using '\\..'
        
        if free_option:
            print("🖱 Clicking 'Data Window' button first...")
            page.locator('button[data-name="object_tree"]').click()
            delay_randomized()
            page.locator('button#data-window').click()
            delay_randomized()
        

            all_data = []
            cnt_indentical = 0
            for i in range(free_option.numbar):
                if has_high_zindex_elements(page, threshold=3):
                    print("⚠️ High z-index elements detected, removing them...")
                    remove_high_zindex_elements(page, threshold=3)
                    if not focus_to_canvas(page):
                        browser.close()
                        return
                    
                print(f"📦 Candle {i + 1}")
                ohlcv = extract_ohlcv(page)
                if ohlcv['date'] == None:
                    print("❗ No more data available, stopping extraction.")
                    break
                if all_data and ohlcv == all_data[-1]:
                    cnt_indentical += 1
                    if cnt_indentical > 5:
                        print("⚠️ Too many identical candles detected, stopping extraction.")
                        break
                
                all_data.append(ohlcv)
                page.keyboard.press("ArrowLeft")
                time.sleep(random.randint(1, 3) / 10)  # Random sleep to avoid detection
                
            if all_data:
                print(f"📊 Extracted {len(all_data)} candles for {symbol}")
                pd.DataFrame(all_data).to_csv(
                    # 'iamfree' is just useless folder name, to detour '\\..' in filename 
                    f'{root_folder}\\iamfree\\' + save_mid_path + symbol.replace(':', '_') + f', {free_option.freq}.csv', 
                    index=False, encoding='utf-8-sig')
                
        else:
            if has_high_zindex_elements(page, threshold=15):
                remove_high_zindex_elements(page, threshold=15)
            if not focus_to_canvas(page):
                browser.close()
                return
            
            print("🖱 Load Full OHLCV Candles")
            page.keyboard.down('Control')
            page.keyboard.down("ArrowLeft")
            time.sleep(15)
            page.keyboard.up("ArrowLeft")
            page.keyboard.up('Control')
            delay_randomized()
            
            print("Save Chart Data")
            page.click('button[data-name="save-load-menu"]')
            wait_then_click(page, "div[role='row']:has-text('Export chart data…')")
            wait_then_click(page, "button:has-text('Export')")
            with page.expect_download() as download_info:
                print(download_info.value.suggested_filename)
                print('⏳ Waiting for download to complete...')
                
            
            download = download_info.value
            fpath =  str(download.path()) + save_mid_path  + download.suggested_filename
            while os.path.exists(download.path()) is False:
                delay_randomized()
            shutil.copy2(download.path(), fpath)
            download.save_as(f'{root_folder}\\' + download.suggested_filename)
            print("📥 Download complete, file saved as:",  download.suggested_filename,
                os.path.getsize(fpath))
            
            
        browser.close()

markets = [ 'DELTAIN', 'DELTA',
    'CAPITALCOM', 'BITMART', 'XTCOM', 'TOKOCRYPTO', 'HTX', 'KCEX',  'PYTH', 'BLOFIN',
        'DEEPCOIN', 'ASCENDEX', 'BITFOREX', 'BICONOMYCOM', 'COINW', 'PROBIT', 'BVOX',
        'BIFINANCE', 'HIBT', 'ORANGEX', 'BTCC', 'BITVAVO', 'TAPBIT', 'COINCHECK',
        'WEEX', 'UZX', 'TOOLBIT', 'BITFINEX', 'BITTREX', 'PIONEX', 'FAMEEX', 'P2B',
    'CRYPTOCOM', 'BINANCE', 'COINBASE', 'BITSTAMP', 'BYBIT', 'KRAKEN', 'WHITEBIT',
 'OKX', 'BITGET', 'HUOBI', 'GATEIO', 'BITMEX', 'DERIBIT', 'BINANCEUS',
   'BITFLYER', 'KUCINNEX', 'BITTREX', 'POLONIEX', 'COINEX', 'BITZ', 'ZOOMEX',
 'BITSO', 'BITBANK', 'COINCHECK', 'WOOX', 'MEXC', 'PHEMEX', 'POLONIEX',
    'LBANK', 'BITRUE', 'GEMINI',  'DERIBIT', 'OKCOIN', 'BINGX', 'KUCOIN',
        # 'UPBIT', 'BITHUMB',  'BITHUMB', /
    # 'CETUS', 'TURBOSFINANCE', 'SUSHISWAP', 'PANGOLIN', 'TRADERJOE', 'BLUEFIN',
    # 'UNISWAP3', 'SUNSWAP', 'TOKENIZE', 'TVC', 'OSMOSIS', 'KLAYSWAP', 'MORPHO',
]




perpecture = False


invalid_symbols = pd.read_csv(
    os.path.join(root_folder, 'analysis', 'invalid_symbols.csv')).symbol.unique()

@dataclass
class FreeOHLCV:
    numbar: int = 5000
    profile_number: int = 11  # Chrome profile number
    
for pairA in reversed([
    'BTC', 'ETH', 'XRP', 'WBTC', 'WETH', 'XRP',
    'BNB', 'PEPE', 'SHIB', 'TRUMP', 'TRUMPOFFICIAL',
    'SOL', 'TRON', 'SUI', 'ADA', 
    'DOT',
    'PEPE', '1000PEPE', '1000BONK', 
    'MATIC', 'LTC', 'BCH', 'LINK', 'XLM', 'ONDO', 'AAVE', 'OP',
    'DOGE', 'AVAX', 'UNI',    
]):
    
    for pairB in ['USDT', 'USDC', 'DAI', 'USD'] + ([] if perpecture else ['KRW']):
        for m in (markets if pairB != 'KRW' else ['UPBIT', 'BITHUMB', 'COINONE', 'GOPAX']):    
            symbol = f'{m}:{pairA}{"G" if m=="GEMINI" else ""}{pairB}' + ('.P' if perpecture else '')
            if symbol in invalid_symbols:
                print(f"Skipping invalid symbol: {symbol}")
                continue
            try:
                print(f"Fetching OHLCV data for {symbol}...")
                get_ohlcv_in_chart(
                    symbol,
                    freq=freqOption.m15,
                    headless=True,
                    # free_option=FreeOHLCV(freq='30')
                )
            except Exception as e:
                print(f"⚠️ Error fetching OHLCV data for {symbol}: {e}")
                LOGGER.error(f"Error fetching OHLCV data for {symbol}: {e}")
                continue
            