import time
from datetime import datetime
from time import sleep

import requests
from rich import box
from rich.columns import Columns
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table


from variables import *

console = Console()


class Header:

    def __rich__(self) -> Panel:
        grid = Table.grid(expand=True)
        grid.add_column(justify="center", ratio=1)
        grid.add_column(justify="right")
        grid.add_row(
            "[b]Weather, Current Events & Stocks[/b]",
            datetime.now().ctime().replace(":", "[blink]:[/]"),
        )
        return Panel(grid, style="white")


# CREATE THE GENERAL LAYOUT OF THE APP
def create_layout() -> Layout:
    layout = Layout(name="root")

    layout.split(
        Layout(name="header_pnl", size=3),
        Layout(name="main_pnl", ratio=1),
        Layout(name="footer_pnl", size=7),
    )
    layout["main_pnl"].split_row(
        Layout(name="side_pnl"),
        Layout(name="body_pnl", ratio=3, minimum_size=60),
    )
    layout['body_pnl'].split(Layout(name="local_news_pnl"),
                             Layout(name="int_news_pnl"))
    layout["side_pnl"].split(Layout(name="weather_pnl"),
                             Layout(name="forecast_pnl"))
    layout["footer_pnl"].split_row(Layout(name="financial_pnl", ratio=2),
                                   Layout(name="exchange_pnl"))
    return layout


# CREATE THE WEATHER PANEL
def create_weather_panel() -> Panel:
    weather_data = get_weather()

    # weather_description = weather_data['weather'][0]['description']

    sponsor_message = Table(expand=True, box=box.SIMPLE)
    sponsor_message.add_column(str(weather_data['name']), justify="right", no_wrap=False)
    sponsor_message.add_column("Description", justify="left", no_wrap=True, style="red")

    sunrise = datetime.fromtimestamp(int(weather_data['sys']['sunrise'])).strftime('%H:%M')
    sunset = datetime.fromtimestamp(int(weather_data['sys']['sunset'])).strftime('%H:%M')

    sponsor_message.add_row("Description", weather_data['weather'][0]['description'])
    sponsor_message.add_row("Temperature", str(weather_data['main']['temp']) + " F")
    sponsor_message.add_row("Feels Like", str(weather_data['main']['feels_like']) + " F")
    sponsor_message.add_row("Min Temp.", str(weather_data['main']['temp_min']) + " F")
    sponsor_message.add_row("Max Temp.", str(weather_data['main']['temp_max']) + " F")
    sponsor_message.add_row("Humidity.", str(weather_data['main']['humidity']) + " %")
    sponsor_message.add_row("Wind", str(weather_data['wind']['speed']) + " MPH")
    sponsor_message.add_row("Clouds", str(weather_data['clouds']['all']) + " %")
    sponsor_message.add_row("Sunrise", sunrise + " Hrs")
    sponsor_message.add_row("Sunset", sunset + " Hrs")

    weather_panel = Panel(
        sponsor_message,
        box=box.SQUARE_DOUBLE_HEAD,
        title="Weather",
    )
    return weather_panel


# CREATE THE WEATHER FORECAST PANEL
def create_weather_forcast() -> Panel:
    tbl = Table(expand=True, box=box.SIMPLE)
    tbl.add_column("Date", justify="center", no_wrap=True)
    tbl.add_column("Temp (F)", justify="center", style="red")

    tbl.add_column("Clouds (%)", justify="center", style="cyan")

    tbl.add_column("Desc", justify="center", style="green", no_wrap=True)

    forecast_data = get_weather_forecast()

    for dicty in forecast_data['list']:
        unformated = datetime.strptime(dicty['dt_txt'], '%Y-%m-%d %H:%M:%S').strftime('%m/%d %H:%M')

        tbl.add_row("" + str(unformated),
                    "" + str(dicty['main']['temp']),
                    "" + str(dicty['clouds']['all']),
                    "" + str(dicty['weather'][0]['description']))

    weather_panel = Panel(
        tbl,
        box=box.SQUARE_DOUBLE_HEAD,
        title="Weather Forecast",
        # border_style="bright_red",
    )

    return weather_panel


# CREATE THE FINANCIAL PANEL
def create_financial_panel() -> Panel:
    financial_data_raw = get_financial_data()

    results = []

    for i in range(len(financial_symbols)):
        results.append(format_stock_data(financial_data_raw['quoteResponse']['result'][i]))

    user_renderables = [Panel(result, expand=True, box=box.SQUARE , ) for result in results]

    return Columns(user_renderables)


# CREATE THE FINANCIAL PANEL
def create_exchange_pnl() -> Panel:
    results = []

    for index in range(len(exc_rate_code)):
        result = get_exchange_rate(exc_rate_code[index]['from'], exc_rate_code[index]['to'])
        results.append(
            f"{exc_rate_code[index]['from']} [b][red]->[/red][/b] {exc_rate_code[index]['to']}\n{str(result)}")

    user_renderables = [Panel(resultes, expand=True, box=box.SIMPLE , border_style="red", ) for resultes in results]

    return Columns(user_renderables)


# CREATE THE NEWS PANEL BASE ON THE COUNTRY CODE
def create_news_panel(country_val) -> Panel:
    sponsor_message = Table(expand=True, box=box.SIMPLE, row_styles=["dim", ""], )

    sponsor_message.add_column("Title (" + country_val + ")", justify="left", style="bright_white", width=50)
    sponsor_message.add_column("Description", justify="left", style="grey85")

    content = get_news(country_val)

    articles = content['articles']

    results = []
    for article in articles:
        sponsor_message.add_row("-" + str(article['title']) + "->", str(article['description']))

    news_panel = Panel(
        sponsor_message,
        box=box.SQUARE,
        title="News",
    )
    return news_panel


# FETCH THE FINANCIAL DATA
def get_financial_data():
    querystring = {"symbols": ",".join(financial_symbols)}

    headers = {
        'x-api-key': "" + api_key_finance2
    }

    response = requests.request("GET", financial_url, headers=headers, params=querystring)

    content = response.json()
    return content


# FETCH NEWS FROM API
def get_news(country):
    r = requests.get(news_url + country)
    content = r.json()
    return content


# FETCH WEATHER FROM API
def get_weather():
    r = requests.get(weather_url)
    return (r.json())


# FETCH WEATHER FORECAST FROM API
def get_weather_forecast():
    r = requests.get(weather_forecast_url)
    return (r.json())


def get_exchange_rate(from_c, to_c):
    fetch_url = f"{ext_rates_url}from_currency={from_c}&to_currency={to_c}"

    result = requests.get(fetch_url)
    data = result.json()
    unformatted_res = data['Realtime Currency Exchange Rate']['5. Exchange Rate']
    formatted_res = "${:,.2f}".format(float(unformatted_res))
    return formatted_res


# FETCH STOCK DATA FROM API
def format_stock_data(user):
    display_name = user["displayName"]
    redularMarketPrice = format_value_to_money(user["regularMarketPrice"])
    market_change = user["regularMarketChange"]
    return f"[b]{display_name}[/b]\n[red]{redularMarketPrice}\n{market_change}\n[/red]"


def format_value_to_money(value):
    return "${:,.2f}".format(float(value))


# FUNCTIONS CALLS
layout = create_layout()
layout["header_pnl"].update(Header())
layout["weather_pnl"].update(create_weather_panel())
layout["forecast_pnl"].update(create_weather_forcast())
layout["local_news_pnl"].update(create_news_panel(lcl_nws_cnt))
layout["int_news_pnl"].update(create_news_panel(int_nws_cnt))
layout["financial_pnl"].update(create_financial_panel())
layout["exchange_pnl"].update(create_exchange_pnl())


counter = 0
counter_max = 500
with Live(layout, refresh_per_second=1, screen=True):
    time.sleep(175)
    while counter <= counter_max:
        # layout["financial_pnl"].update(create_financial_panel())
        counter += 1
