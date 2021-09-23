import time
from typing import List
import pandas as pd
from database import CompanyFinance, database
import settings

INTERVALS = ("1d", "1wk", "1m")


def save_company_finances(
    company: str,
    start: int = 0,
    end: int = int(time.time()),
    interval: str = "1d",
) -> None:
    if interval not in INTERVALS:
        valid_intervals_msg = f"{', '.join(INTERVALS[:-1])} or {INTERVALS[1]}"
        raise ValueError(f"Invalid interval value. Should be {valid_intervals_msg}")

    download_url = settings.DATA_DOWNLOAD_URL_TEMPLATE.format(
        title=company, start=start, end=end, interval=interval
    )
    company_dataframe = pd.read_csv(download_url)

    company_dataframe.insert(loc=0, column="company", value=company)
    inserted_cols = company_dataframe.columns.str.lower().str.split().str.join("_")
    renaming_data = dict(zip(company_dataframe.columns, inserted_cols))
    company_dataframe = company_dataframe.rename(renaming_data, axis=1)

    company_data = company_dataframe.to_dict(orient="records")
    with database.atomic():
        CompanyFinance.insert_many(company_data).execute()


def extract_company_finances(company: str, records: int = 50) -> List[CompanyFinance]:
    with database.atomic():
        company_mask = CompanyFinance.company == company
        by_company = CompanyFinance.select().where(company_mask)
        if by_company.count() == 0:
            save_company_finances(company)
        return by_company[:records]


def extract_all_finances(records: int = None) -> List[CompanyFinance]:
    with database.atomic():
        if records is None:
            all_companies = CompanyFinance.select().count()
            return CompanyFinance.select()[:all_companies]
        return CompanyFinance.select()[:records]
