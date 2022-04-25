# =====================================================================================================================#
# ================================================= YAHOO FINANCE =====================================================#

# API DOCUMENTATION     ->  https://openweathermap.org/api
api_key_weather = 'API KEY'

# OPTIONS
latitude = "LAT"
longitude = "LONG"
language_code = "en"
units = 'imperial'
weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key_weather}&units={units}&lang={language_code}"
weather_forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&appid={api_key_weather}&units={units}&lang={language_code}"

# MORE INFO:
# LANGUAGE CODES -> https://openweathermap.org/current#multi
# UNITS          -> https://openweathermap.org/current#data

# =====================================================================================================================#
# =================================================== NEWS API ========================================================#

# API DOCUMENTATION -> https://newsapi.org/docs
# LIMITATIONS

api_key_news = 'API KEY'
news_url = f'https://newsapi.org/v2/top-headlines?apiKey={api_key_news}&country='

# SAMPLE COUNTRY CODES
lcl_nws_cnt = 'US'
int_nws_cnt = 'FR'
# FOR A COMPLETE LIST OF COUNTRIES -> https://newsapi.org/docs/endpoints/sources

# =====================================================================================================================#
# ================================================= YAHOO FINANCE =====================================================#

# API DOCUMENTATION  -> https://www.yahoofinanceapi.com/
# LIMITATIONS: ONLY 100 API REQUEST A DAY ON THE FREE PLAN

api_key_finance2 = "API KEY"
financial_url = "https://yfapi.net/v6/finance/quote"

# SAMPLE FINANCIAL SYMBOLS
financial_symbols = ["AAPL", "GPRO", "COMP", "TSLA", "CYXT", "SANG", "NFLX", "TWTR", "NVDA", "IBM"]

# PREMIUM MEMBERSHIP URL -> https://www.yahoofinanceapi.com/pricing#
# =====================================================================================================================#

# =================================================EXCHANGE RATE ======================================================#

# API DOCUMENTATION -> https://www.alphavantage.co/documentation/
# LIMITATION: ONLY 5 API REQUEST PER MINUTE ON ON THE FREE PLAN.

api_key_finance = "API KEY"
ext_rates_url = f'https://www.alphavantage.co/query?&apikey={api_key_finance}&function=CURRENCY_EXCHANGE_RATE&'

# SAMPLE CODES
exc_rate_code = [
    {'from': 'USD', 'to': 'CAD'},
    {'from': 'USD', 'to': 'EUR'},
    {'from': 'USD', 'to': 'JPY'},
    {'from': 'USD', 'to': 'GBP'},
    {'from': 'BTC', 'to': 'USD'},
]

# PREMIUM MEMBERSHIP URL -> https://www.alphavantage.co/premium/
# =====================================================================================================================#
