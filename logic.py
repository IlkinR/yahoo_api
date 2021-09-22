import time
import pandas as pd
import peewee as pw
from database import CompanyFinance, database

DATA_DOWNLOAD_URL_TEMPLATE = "https://query1.finance.yahoo.com/v7/finance/download/{title}?period1={start}&period2={end}&interval={interval}&events=history&includeAdjustedClose=true"


def save_company_finances(
    database: pw.SqliteDatabase,
    company_title: str,
    start: int = 0,
    end: int = int(time.time()),
    interval: str = "1d",
):
    download_url = DATA_DOWNLOAD_URL_TEMPLATE.format(
        title=company_title, start=start, end=end, interval=interval
    )
    company_dataframe = pd.read_csv(download_url)

    company_dataframe.insert(loc=0, column="company", value=company_title)
    inserted_cols = company_dataframe.columns.str.lower().str.split().str.join("_")
    renaming_data = dict(zip(company_dataframe.columns, inserted_cols))
    company_dataframe = company_dataframe.rename(renaming_data, axis=1)

    company_data = company_dataframe.to_dict(orient="records")
    with database.atomic():
        CompanyFinance.insert_many(company_data).execute()


def extract_company_finances(
    database: pw.SqliteDatabase, company_name: str, records: int = 50
):
    with database.atomic():
        company_mask = CompanyFinance.company == company_name
        by_company = CompanyFinance.select().where(company_mask)
        if by_company.count() == 0:
            print("downloading")
            # there is no records for company, so we'll load them
            save_company_finances(database, company_name)

    with database.atomic():
        company_mask = CompanyFinance.company == company_name
        by_company = CompanyFinance.select().where(company_mask)
        return by_company[:records]


def extract_all_finances(database: pw.SqliteDatabase, records: int = None):
    with database.atomic():
        if records is None:
            max_companies = CompanyFinance.select().count()
            return CompanyFinance.select()[:max_companies]
        return CompanyFinance.select()[:records]