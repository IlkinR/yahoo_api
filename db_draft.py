import peewee as pw

db = pw.SqliteDatabase("comp_finances.db")


class Person(pw.Model):
    name = pw.CharField()

    class Meta:
        database = db


class Vector(pw.Model):
    x = pw.CharField()

    class Meta:
        database = db


# names = ["Bob", "Alice", "Jordon", "Madison"]
# nkeys = ["name"] * len(names)
# to_add = list(zip(names, ["name"] * len(names)))
# print(to_add)

data = [{"name": "John"}, {"name": "Kilo"}]


with db.atomic():
    # pass
    # person = Person(name="Bob")
    # person.save()
    Person.insert_many(data).execute()

# db.create_tables([Vector])
