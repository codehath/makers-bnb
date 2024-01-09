from peewee import Model, PostgresqlDatabase, CharField, IntegerField

# Replace the following with your PostgreSQL database connection details
db = PostgresqlDatabase("test", user="farhath", password="", host="localhost")


class BaseModel(Model):
    class Meta:
        database = db


class Person(BaseModel):
    name = CharField()
    age = IntegerField()


# Replace the following with your PostgreSQL database connection details
db.connect()

# if db.table_exists(Person):
#     # If the table exists, drop it
#     db.drop_tables([Person])

# db.create_tables([Person])

# new_person = Person.create(name='Jack Doe', age=25)
# Person.create(name="Joe Doe", age=22)

people_over_21 = Person.select().where(Person.age > 21)
for person in people_over_21:
    print(person.name, person.age)

db.drop_tables([Person])

db.close()
