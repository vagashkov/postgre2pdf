import psycopg2

# default database connection establishment
conn = psycopg2.connect(
    database="postgres",
    user='postgres',
    password='password',
    host='localhost',
    port='5432'
)
conn.autocommit = True

# Creating a cursor object
cursor = conn.cursor()

# create new database
sql = '''CREATE database db2pdf'''
cursor.execute(sql)
print("Database db2pdf created...")
#  Closing the connection
conn.close()

# reopen connection to target database
conn = psycopg2.connect(
    database="db2pdf",
    user='postgres',
    password='password',
    host='localhost',
    port='5432'
)
conn.autocommit = True
cursor = conn.cursor()
print("Connected to db2pdf")

sql = '''CREATE SCHEMA staff'''
cursor.execute(sql)
print("Created staff schema")

# query to delete table if it is already exists
sql = '''DROP TABLE IF EXISTS staff.person'''
cursor.execute(sql)

# create table from scratch
sql = '''CREATE TABLE staff.person (
id serial PRIMARY KEY,
name VARCHAR ( 100 ) NOT NULL,
position VARCHAR ( 100 ) NOT NULL,
office VARCHAR ( 100 ) NOT NULL,
age INT NOT NULL,
salary INT NOT NULL)
'''
cursor.execute(sql)

#
# # and fill it with some data
sql = '''INSERT INTO
     staff.person(name, position, office, age, salary)
 VALUES
 	('Ivan Ivanov', 'Director', 'Tokyo', 36, 5689),
 	('Petr Petrov', 'Manager', 'London', 56, 5648),
 	('Sidor Sidorov', 'Software Engineer', 'San Francisco', 23, 5689),
 	('Sergey Sergeev', 'Software Engineer', 'Olongapo', 23, 54654),
 	('Fantazia Konchilas', 'Software Engineer', 'San Francisco', 26, 5465)
 	'''
cursor.execute(sql)

conn.close()
