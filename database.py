import peewee as pw

database = pw.SqliteDatabase("comp_finances.db")


class CompanyFinance(pw.Model):
    company = pw.CharField()
    date = pw.DateTimeField()
    open = pw.FloatField()
    high = pw.FloatField()
    low = pw.FloatField()
    close = pw.FloatField()
    adj_close = pw.FloatField()
    volume = pw.IntegerField()

    class Meta:
        database = database
        table_name = "company_finances"


with database.atomic():
    database.create_tables([CompanyFinance])
