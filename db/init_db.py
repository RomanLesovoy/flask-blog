import sqlite3

schema_init = open('db/schema.sql')

connection = sqlite3.connect('database.db')

cur = connection.cursor()

# print(schema_init.read(), connection)
cur.executescript(schema_init.read())

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
    ('First Post', 'Content for the first post')
)

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
    ('Second Post', 'Content for the second post')
)

cur.execute("INSERT INTO pagesInfo (pageName, content) VALUES (?, ?)",
    ('about', 'First app with python ever')
)

connection.commit()
connection.close()
