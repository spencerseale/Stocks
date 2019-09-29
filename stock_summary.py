#!/usr/bin/env python3

#Alpha Vantage API key: 6B3T0LVSE9RMUZFT

import requests
from datetime import datetime
from fpdf import FPDF

#determing Friday's date, must run on Saturdays
today_date = datetime.today().strftime('%Y-%m-%d')
if today_date[8:] == "10":
    friday_date = today_date[:8] + "09"
elif today_date[8:] == "20":
    friday_date = today_date[:8] + "19"
elif today_date[8:] == "30":
    friday_date = today_date[:8] + "29"
else:
    friday_date = today_date[:9] + str(int(today_date[9:]) - 1)

#Function to grab api data for a specific stock and report weekly data
def stock_DATA(comp_sym, filename):
    api = "https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol="+comp_sym+"&interval=5min&apikey=6B3T0LVSE9RMUZFT"
    search_site = (requests.get(api)).json()

    info = search_site['Meta Data']['1. Information']
    week_stat = search_site['Weekly Time Series'][friday_date]

    open = week_stat['1. open'][:(len(week_stat['1. open']))-2]
    close = week_stat['4. close'][:(len(week_stat['4. close']))-2]
    low = week_stat['3. low'][:(len(week_stat['3. low']))-2]
    high = week_stat['2. high'][:(len(week_stat['2. high']))-2]
    volume = week_stat['5. volume']

    print("-------------------------------------------------------------------------------", file=filename)
    print(f"*{comp_sym}", file=filename)
    print(f"The {info} for {comp_sym} are as follows:", file=filename)
    print(f"{comp_sym} opened this week at ${open}.", file=filename)
    print(f"{comp_sym} closed this week at ${close}.", file=filename)
    print(f"{comp_sym} had a low of ${low}.", file=filename)
    print(f"{comp_sym} had a high of ${high}.", file=filename)
    print(f"This week's total volume for {comp_sym} was {volume}.\n", file=filename)

##client ticker lists
#Spencer
spencer_tick = ["MSFT", "AAPL"]
colin_tick = ["LEVI", "ACB"]
dad_tick = ["TD", "NVDA", "ADPT", "GO", "PANW", "TSLA", "GE", "INTC", "FEYE"]

##client and their ticker list
#key=client, value=ticker list
client_ticker_dict = {
"spencer" : spencer_tick,
"colin" : colin_tick,
"dad" : dad_tick
}

#writing stock summary for each client to separate .txt files
client_dir = "/Users/spencerseale/gitUO/client_stock_smry/"
#performing data summary to pdf creation for one client at a time
for cli in client_ticker_dict.keys():
    print(f"compiling data for {cli}")
    filename = cli+"_stock_smry_"+friday_date+".txt"
    with open(client_dir+filename, "w") as id:
        for ticker in client_ticker_dict[cli]:
            print("Fetching", ticker)
            stock_DATA(ticker, id)
#transforming .txt to .pdf
    pdf = FPDF()
    pdf.add_page()
    #specs from: https://pyfpdf.readthedocs.io/en/latest/reference/set_font/index.html
    pdf.set_font('Arial', size=12)
    x = open(client_dir+filename, "r")
    contents = x.readlines()
    for _ in contents:
        pdf.cell(20, 10, _, 0, 1)
    pdf_name = filename[:(len(filename)-4)]+".pdf"
    pdf.output(client_dir+pdf_name, 'F')
