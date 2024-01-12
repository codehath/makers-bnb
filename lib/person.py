from peewee import *
from creds import *

db = PostgresqlDatabase(db_name, user=user, password=password, host=host)


class Person(Model):
    id = AutoField()
    name = CharField()
    email = CharField()
    password = CharField()
    number = CharField(max_length=11)
    logged_in = BooleanField(default=False)

    class Meta:
        database = db  # This model uses the "people.db" database.
    
   

