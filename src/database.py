import peewee as pw
import settings

database = pw.SqliteDatabase(settings.DATABASE_NAME)


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

    def to_dict(self):
        return {
            "company": self.company,
            "date": self.date.strftime("%Y-%m-%d"),
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "close": self.close,
            "adj_close": self.adj_close,
            "volume": self.volume,
        }


if __name__ == "__main__":
    with database.atomic():
        database.create_tables([CompanyFinance])
