from dataclasses import dataclass
import sys
import logging
sys.stdout.reconfigure(encoding='utf-8')
logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
    filename='ohlcv_premium_spot.log', filemode='a')
LOGGER = logging.getLogger(__name__)

@dataclass
class FreqOption:
    d1: str = '1D'  # 1 day
    m1: str = '1'  # 1 minute
    m5: str = '5'  # 5 minutes
    m15: str = '15'
    m20: str = '20'  # 20 minutes
    m30: str = '30'  # 30 minutes
    h1: str = '60'  # 1 hour
    

@dataclass
class FreeOHLCV:
    numbar: int = 5000
    profile_number: int = 11  # Chrome profile number
    
    
google_profile_directory = 'C:\\Users\\Administrator\\AppData\\Local\\Google\\Chrome\\User Data\\Profile'
root_folder = 'F:\\tradingview'

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

pairAasset = [
      'BTC', 'ETH', 'XRP', 'WBTC', 'WETH', 'XRP',
    'BNB', 'PEPE', 'SHIB', 'TRUMP', 'TRUMPOFFICIAL',
    'SOL', 'TRON', 'SUI', 'ADA', 
    'DOT',
    'PEPE', '1000PEPE', '1000BONK', 
    'MATIC', 'LTC', 'BCH', 'LINK', 'XLM', 'ONDO', 'AAVE', 'OP',
    'DOGE', 'AVAX', 'UNI',    
]