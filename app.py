from fastapi import FastAPI
import logic
from playhouse.shortcuts import model_to_dict, dict_to_model


api = FastAPI()


@api.get("/finances/")
def get_all_finances(overall_records: int = 100):
    finances = logic.extract_all_finances(records=overall_records)
    finances = [finance.to_dict() for finance in finances]
    return {"items": finances, "records": overall_records}


@api.get("/finances/{company_title}")
def get_all_finances(company_title: str, overall_records: int = 100):
    finances = logic.extract_company_finances(
        company_name=company_title, records=overall_records
    )
    finances = [finance.to_dict() for finance in finances]
    return {"items": finances, "records": overall_records}
