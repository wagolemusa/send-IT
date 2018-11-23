import os
import psycopg2
from psycopg2 import Error
connection = psycopg2.connect(dbname='sendit', user='postgres', password='refuge', host='localhost')


def init_db():
	conn = connection
	return conn


def create_table():
	queries = ("""
		CREATE TABLE IF NOT EXISTS users(
			user_id SERIAL PRIMARY KEY UNIQUE NOT NULL,
			first_name VARCHAR(50) NOT NULL,
			last_name VARCHAR(50) NOT NULL,
			username VARCHAR(50) NOT NULL,
			phone INT,
			email VARCHAR(150) NOT NULL,
			password VARCHAR(250) NOT NULL,
			is_admin BOOLEAN DEFAULT False);""",

				"""CREATE TABLE IF NOT EXISTS orders(
			parcel_id SERIAL PRIMARY KEY UNIQUE NOT NULL,
			user_id  INT,
			title VARCHAR(50) NOT NULL,
			username VARCHAR(50) NOT NULL,
			pickup VARCHAR(50) NOT NULL,
			rec_id INT,
			rec_phone INT,
			rec_name  VARCHAR(50) NOT NULL,
			destination VARCHAR(50) NOT NULL,
			weight INT,
			status VARCHAR DEFAULT 'In Transit',
			created_on TIMESTAMP DEFAULT NOW(),
			FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
		);""",)
	connection = init_db()
	curr = connection.cursor()
	for query in queries:
		curr.execute(query)
	connection.commit()


def drop_table():
	""" Methon for droping table """
	connection = init_db()
	curr = connection.cursor()

	queries = (
		"""DROP TABLE IF orders;""", """DROP TABLE IF EXISTS users CASCADE;""") 
	try:
		for query in queries:
			curr.execute(query)
			connection.commit()

	except (Exception, Error) as error:
		print(error)

def close_instance():
	connection = init_db()
	curr = connection.cursor()
	connection.close()
	curr.close()

