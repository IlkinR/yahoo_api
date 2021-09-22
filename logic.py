import time
import pandas as pd
from database import CompanyFinance, database

DATA_DOWNLOAD_URL_TEMPLATE = "https://query1.finance.yahoo.com/v7/finance/download/{title}?period1={start}&period2={end}&interval={interval}&events=history&includeAdjustedClose=true"


def save_company_finances(
    database, 
    company_title: str,
    start: int = 0,
    end: int = int(time.time()),
    interval: str = "1d",
):
    company_dataframe = pd.read_csv(DATA_DOWNLOAD_URL_TEMPLATE.format(
        title=company_title, start=start, end=end, interval=interval
    ))

    company_dataframe.insert(loc=0, column="company", value=company_title)
    inserted_cols = company_dataframe.columns.str.lower().str.split().str.join("_")
    renaming_data = dict(zip(company_dataframe.columns, inserted_cols))
    company_dataframe = company_dataframe.rename(renaming_data, axis=1)
    
    company_data = company_dataframe.to_dict(orient="records")
    with database.atomic():
        CompanyFinance.insert_many(company_data).execute()


