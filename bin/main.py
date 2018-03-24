# This is the core file of the stocks project.
# stocks is a program to retrieve the latest prices of a given stock or list of
# stocks in a given index and present it in a pretty way in terminal.
# Future builds should include a graphical interface and a virtual wallet for management purposes.
# This is a web scraper, no api is being used, so it is quite limited.

# from bin.wallet import Wallet
from datetime import datetime, date
from functools import reduce
from lxml import html
from third_party.highlight import highlight
import operator
import requests

cac40_info = {'stocks': {}}
cac40_table = {"AC": "ACCOR", "AI": "AIR LIQUIDE", "AIR": "AIRBUS", "AMT": " ARCELORMITTAL", "ATO": "ATOS", "CS": "AXA",
               "BNP": "BNP PARIBAS BR-A", "EN": "BOUYGUES", "CAP": "CAPGEMINI",  "CA": "CARREFOUR",
               "ACA": "CREDIT AGRICOLE SA", "ENGI": "ENGIE", "BN": "DANONE","EI": "ESSILOR INTL", "KER": "KERING (Ex: PPR)",
               "OR": "L'OREAL", "LHN": "LAFARGEHOLCIM N", "LR": "LEGRAND", "MC":  "LVMH MOET VUITTON",
               "ML": "MICHELIN N", "ORA": "ORANGE (ex: FRANCE TELECOM)", "PRI": "PERNOD RICARD", "UG": "PEUGEOT",
               "PUB": "PUBLICIS GRP", "RNO": "RENAULT", "SAF": "SAFRAN", "SGO": "SAINT-GOBAIN", "SAN": "SANOFI",
               "SU": "SCHNEIDER E.SE", "GLE": "SOCIETE GENERALE", "SW": "SODEXO", "OLB": "SOLVAY", "STM": "STMICROELECTR",
               "FTI": "TECHNIP", "FP": "TOTAL", "UL": "UNIBAIL-RODAMCO", "FR": "VALEO", "VIE": "VEOLIA ENVIRONMENT",
               "DG": "VINCI", "VIV": "VIVENDI"}

dax30_info = {'stocks': {}}
# dax30_table
time_of_request = datetime.now()
start = True
version = "0.01"


# get_stock_listing should connect to boursorama, read the constituents of each index and modify the list of the
# corresponding index with new values
def get_stock_listing():
    stocks = []
    latest_price = []
    variation = []
    opening_price = []
    highest_price = []
    lowest_price = []

    info = [stocks, latest_price, variation, opening_price, highest_price, lowest_price]

    for i in range(1, 3):
        page = requests.get("https://www.boursorama.com/bourse/actions/cotations/page-" + str(i) + "?quotation_az_filter[market]=1rPCAC")
        tree = html.fromstring(page.content)

        stocks.append(tree.xpath('//li[@class="o-list-inline__item o-list-inline__item--middle"]/a/text()'))
        latest_price.append(tree.xpath('//tr[@class="c-table__row"]/td[@class="c-table__cell c-table__cell--dotted u-text-right u-text-medium "]/span[@class="c-instrument c-instrument--last"]/text()'))
        variation.append(tree.xpath('//span[@class="c-instrument c-instrument--instant-variation"]/text()'))
        opening_price.append(tree.xpath('//span[@class="c-instrument c-instrument--open"]/text()'))
        highest_price.append(tree.xpath('//span[@class="c-instrument c-instrument--high"]/text()'))
        lowest_price.append(tree.xpath('//span[@class="c-instrument c-instrument--low"]/text()'))

    for j in range(len(info)):
        info[j] = reduce(operator.concat, info[j])

    print(info[0], info[1], info[2], info[3], info[4], info[5], sep='\n')

    for k in range(40):
        cac40_info["stocks"][info[0][k]] = {"LatestPrice": info[1][k], "Variation": info[2][k],
                                            "OpeningPrice": info[3][k], "HighestPrice": info[4][k],
                                            "LowestPrice": info[5][k]}

    print(cac40_info)

    # page = requests.get("http://www.boursorama.com/bourse/actions/inter_az.phtml?PAYS=49&BI=5pDAX")
    # tree = html.fromstring(page.content)
    #
    # stocks = tree.xpath('//table[@class="list hover alt sortserver"]/tbody/tr/td[@class="tdv-libelle"]/a/text()')
    # latest_price = tree.xpath(
    #     '//table[@class="list hover alt sortserver"]/tbody/tr/td[@class="tdv-last"]/span/text()')
    # variation = tree.xpath('//table[@class="list hover alt sortserver"]/tbody/tr/td[@class="tdv-var"]/span/text()')
    # opening_price = tree.xpath(
    #     '//table[@class="list hover alt sortserver"]/tbody/tr/td[@class="tdv-open"]/span/text()')
    # highest_price = tree.xpath(
    #     '//table[@class="list hover alt sortserver"]/tbody/tr/td[@class="tdv-high"]/span/text()')
    # lowest_price = tree.xpath(
    #     '//table[@class="list hover alt sortserver"]/tbody/tr/td[@class="tdv-low"]/span/text()')
    # variation_from1_jan = tree.xpath(
    #     '//table[@class="list hover alt sortserver"]/tbody/tr/td[@class="tdv-var_an"]/span/text()')
    #
    # for i in range(30):
    #     dax30_info["stocks"][stocks[i]] = {"LatestPrice": latest_price[i], "Variation": variation[i],
    #                                        "OpeningPrice": opening_price[i], "HighestPrice": highest_price[i],
    #                                        "LowestPrice": lowest_price[i]}


def display_stock_info(stock_list, stock):
    print("\n")

    print("Information for stock: %s" % stock)
    print("Latest Price: %s" % stock_list["LatestPrice"])
    print("Variation: %s" % highlight(stock_list["Variation"]))
    print("Opening Price: %s" % stock_list["OpeningPrice"])
    print("Highest Price in Session: %s" % stock_list["HighestPrice"])
    print("Lowest Price in Session: %s" % stock_list["LowestPrice"])

    print("\n")


# Program main loop
print("StockParser version %s" % version, sep="\n")
print("Initializing...")
get_stock_listing()

while start:
    print("Select an option:")
    print("0: Debug")
    print("1: Display Index Info (Might generate big lists of data).")
    print("2: Refresh Stock Lists.")
    print("3: Show Info of a Given Stock.")
    print("4: Exit")

    option = input("> ")

    if option == "0":
        stock = input("Insert a stock > ").upper()
        stock = cac40_table[stock]

        display_stock_info(cac40_info["stocks"][stock], stock)

        start = False

    if option == "1":
        index = input("Insert an index > ").upper()

        if index == "CAC40":
            keys = list(cac40_info["stocks"].keys())
            for i in range(len(cac40_info["stocks"])):  # Looking for a stock this way
                display_stock_info(cac40_info["stocks"][keys[i]], keys[i])

            print("Data retrieved on: %s" % time_of_request)
            print("Data might be delayed by up to 15 minutes.")

        elif index == "DAX30":
            keys = list(dax30_info["stocks"].keys())
            for i in range(len(dax30_info["stocks"])):
                display_stock_info(dax30_info["stocks"][keys[i]], keys[i])

            print("Data retrieved on: %s" % time_of_request)
            print("Data might be delayed by up to 15 minutes.")

        print("\n")

    elif option == "2":
        print("Refreshing...")
        time_of_request = datetime.now()
        get_stock_listing()
        print("Done\n")

    elif option == "3":
        index = input("Insert an index > ").upper()
        stock = input("Insert a stock > ").upper()

        if index == "CAC40":

            try:
                stock = cac40_table[stock]

                display_stock_info(cac40_info["stocks"][stock], stock)

            except KeyError:
                print("The stock %s does not exist in %s" % (stock, index))

        elif index == "DAX30":
            try:
                display_stock_info(dax30_info["stocks"][stock], stock)

            except KeyError:
                print("The stock %s does not exist in %s" % (stock, index))

        print("\n")

    elif option == "4":
        # Exit loop
        start = False

exit(0)
