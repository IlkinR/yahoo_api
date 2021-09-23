# Yahoo Financer

The applcation can be used to extract all available financial data from [Yahoo](https://finance.yahoo.com/) for the whole period of time for the given company in the automatic way.

## How run it ?
1. Install dependencies 
```shell
pip install -r requirements.txt
```
2. Create a database for the application. It'll be created in the root folder together with **src**
```shell
python .\database.py
```
3. Run the api
```shell
uvicorn app:api --reload  
```
