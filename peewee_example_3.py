from peewee import Model, PostgresqlDatabase, CharField, IntegerField, ForeignKeyField

db = PostgresqlDatabase("test", user="", password="", host="localhost")


class BaseModel(Model):
    class Meta:
        database = db


class Author(BaseModel):
    name = CharField()


class Book(BaseModel):
    title = CharField()
    author = ForeignKeyField(Author, backref="books")


# Connect to the database and create tables
db.connect()
db.create_tables([Author, Book])

# Insert some data
author = Author.create(name="John Doe")
book = Book.create(title="Book 1", author=author)

# Perform a join query
query = Book.select(Book.title, Author.name).join(Author).where(Book.title == "Book 1")

# Convert the result to a list of dictionaries
result_dicts = [dict(row.__dict__) for row in query]

# Print the resulting list of dictionaries
print(result_dicts)
