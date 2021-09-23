from fastapi import FastAPI
import uvicorn
import logic

api = FastAPI()


@api.get("/finances/")
def get_all_finances(overall_records: int = 100):
    finances = logic.extract_all_finances(records=overall_records)
    finances = [finance.to_dict() for finance in finances]
    return {"items": finances, "records": overall_records}


@api.get("/finances/{company}")
def get_all_finances(company: str, records: int = 100):
    finances = logic.extract_company_finances(company=company, records=records)
    finances = [finance.to_dict() for finance in finances]
    return {"items": finances, "records": records}


if __name__ == "__main__":
    uvicorn.run(api)
