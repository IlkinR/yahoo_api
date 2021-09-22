import os

DATA_DOWNLOAD_URL_TEMPLATE = "https://query1.finance.yahoo.com/v7/finance/download/{title}?period1={start}&period2={end}&interval={interval}&events=history&includeAdjustedClose=true"

DATABASE_NAME = os.path.join(os.path.dirname(os.getcwd()), "comp_finances.db")