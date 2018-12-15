import os
import psycopg2
connection = psycopg2.connect(dbname='d92a0rb0j8rphh', user='gaijmyignhvtkw', password='7e0acadc7013645d81437d922b7030782cdee4006cadf7f54501aa291b29d3e6', host='ec2-23-21-65-173.compute-1.amazonaws.com')

def init_db ():
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

				"""CREATE TABLE IF NOT EXISTS prices(
			price_id SERIAL PRIMARY KEY UNIQUE NOT NULL,
			from_location VARCHAR(50) NOT NULL,
			to_location  VARCHAR(50) NOT NULL,
			price INT);"""

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
		"""DROP TABLE IF EXISTS orders CASCADE;""", """DROP TABLE IF EXISTS users CASCADE;""")
	for query in queries:
		curr.execute(query)
		connection.commit()

def close_instance():
	connection = init_db()
	curr = connection.cursor()
	connection.close()
	curr.close()

def admin():
	connection = init_db()
	curr = connection.cursor()

	first_name = 'admin'
	last_name =  'wise'
	username  = 'admin'
	phone = '0725696042'
	email = 'admin@admin.com'
	password = 'admin@wise'
	is_admin=True

	sql = "SELECT * FROM users WHERE username = %s"
	curr.execute(sql, (username,))
	data = curr.fetchone()

	if not data:
		sql = """INSERT INTO users(first_name, last_name, username, phone, email, password, is_admin)\
					VALUES(%s, %s, %s, %s, %s, %s, %s)"""
		curr.execute(sql, (first_name, last_name, username, phone, email, password, is_admin))
		connection.commit()


