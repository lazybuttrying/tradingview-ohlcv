from scrap_js import delay_randomized, wait_then_click, has_high_zindex_elements, remove_high_zindex_elements
from extractor import extract_ohlcv, focus_to_canvas, is_valid_symbol
from config import LOGGER, FreqOption, google_profile_directory, root_folder, markets, pairAasset




perpecture = False

for pairA in pairAasset:
    for pairB in ['USDT', 'USDC', 'DAI', 'USD'] + ([] if perpecture else ['KRW']):
        for m in (markets if pairB != 'KRW' else ['UPBIT', 'BITHUMB', 'COINONE', 'GOPAX']):    
            symbol = f'{m}:{pairA}{"G" if m=="GEMINI" else ""}{pairB}' + ('.P' if perpecture else '')
            if is_valid_symbol(symbol):
                print(f"Skipping invalid symbol: {symbol}")
                continue
            try:
                print(f"Fetching OHLCV data for {symbol}...")
                get_ohlcv_in_chart(
                    symbol,
                    freq=FreqOption.m15,
                    headless=True,
                    # free_option=FreeOHLCV(freq='30')
                )
            except Exception as e:
                print(f"⚠️ Error fetching OHLCV data for {symbol}: {e}")
                LOGGER.error(f"Error fetching OHLCV data for {symbol}: {e}")
                continue
            