import datetime
import psycopg2
import smtplib
import random
import base64
from flask import Flask,jsonify,request, make_response
from flask_restful import Resource
from functools import wraps
from flask_jwt_extended import (
  	jwt_required, create_access_token, get_current_user, 
    get_jwt_identity 
)
from models.user_model import Usermodel, Users
import africastalking

types_status = ["delivered", "cancled"]

cashflow = psycopg2.connect(dbname='d92a0rb0j8rphh', user='gaijmyignhvtkw', password='7e0acadc7013645d81437d922b7030782cdee4006cadf7f54501aa291b29d3e6', host='ec2-23-21-65-173.compute-1.amazonaws.com')
curr_maney = cashflow.cursor()

class Daily_Sum(Resource):
	""" Class Sum all Daily total """
	def get(self):
		curr_maney.execute("SELECT SUM(amount::int) FROM payments WHERE book_id = book_id AND created_on BETWEEN NOW() - INTERVAL '24 HOURS' AND NOW()")
		cashflow.commit()
		dailyTotal = curr_maney.fetchall()
		return {"num": dailyTotal}

class Weekly_Sum(Resource):
	""" Class sum all weekly""" 
	def get(self):
		curr_maney.execute("SELECT SUM(amount::int) FROM payments WHERE book_id = book_id AND created_on > current_date - interval '7 days'")
		cashflow.commit()
		weekly = curr_maney.fetchall()
		return {"week": weekly}

class Monthly_Sum(Resource):
	def get(self):
		curr_maney.execute("SELECT to_char(created_on, 'Mon') AS mon, EXTRACT(year FROM created_on) AS yyyy, SUM(amount::int) AS amount FROM payments WHERE book_id = book_id GROUP BY 1,2 LIMIT 1")
		cashflow.commit()
		monthly = curr_maney.fetchall()
		money = []
		for monx in monthly:
			mon = monx[0]
			yyyy = monx[1]
			amount = monx[2]
			money.append({"mon":mon, "yyyy":yyyy, "amount":amount})
		return {"month": money}


class Daily_Sum_Receptions(Resource):
	""" Class Sum all Daily total on Receptions paid with M-pesa"""
	def get(self):
		curr_maney.execute("SELECT SUM(amount::int) FROM payments WHERE desk_id = desk_id AND created_on BETWEEN NOW() - INTERVAL '24 HOURS' AND NOW()")
		cashflow.commit()

		dailyTotal = curr_maney.fetchall()
		return {"num": dailyTotal}

class Weekly_Sum_Receptions(Resource):
	""" Class sum all weekly on Receptions paid with M-pesa""" 
	def get(self):
		curr_maney.execute("SELECT SUM(amount::int) FROM payments WHERE desk_id = desk_id AND created_on > current_date - interval '7 days'")
		cashflow.commit()
		weekly = curr_maney.fetchall()
		return {"week": weekly}

class Monthly_Sum_Receptions(Resource):
	""" Class sum all Monthly on Receptions paid with M-pesa"""
	def get(self):
		curr_maney.execute("SELECT to_char(created_on, 'Mon') AS mon, EXTRACT(year FROM created_on) AS yyyy, SUM(amount::int) AS amount FROM payments WHERE desk_id = desk_id GROUP BY 1,2 LIMIT 1")
		cashflow.commit()
		monthly = curr_maney.fetchall()
		money = []
		for monx in monthly:
			mon = monx[0]
			yyyy = monx[1]
			amount = monx[2]
			money.append({"mon":mon, "yyyy":yyyy, "amount":amount})
		return {"month": money}

class Daily_Book_Cash(Resource):
	""" Class Sum all Daily total for client booked by Cash"""
	def get(self):
		curr_maney.execute("SELECT SUM(total) FROM booking WHERE payments = 'Cash' AND created_on BETWEEN NOW() - INTERVAL '24 HOURS' AND NOW()")
		cashflow.commit()
		dayTotal = curr_maney.fetchall()
		return {"cash": dayTotal}


class Weekly_Book_Cash(Resource):
	""" Class Sum all weekly total for client booked by Cash"""
	def get(self):
		curr_maney.execute("SELECT SUM(total) FROM booking WHERE payments = 'Cash' AND created_on > current_date - interval '7 days'")
		cashflow.commit()
		weeklyTotal = curr_maney.fetchall()
		return {"cashweek": weeklyTotal}


class Monthly_Book_Sum_Desk(Resource):
	""" Class sum all Monthly booked by clint online """
	def get(self):
		curr_maney.execute("SELECT to_char(created_on, 'Mon') AS mon, EXTRACT(year FROM created_on) AS yyyy, SUM(total) AS amount FROM booking WHERE payments = 'Cash' GROUP BY 1,2 LIMIT 1")
		cashflow.commit()
		monthly = curr_maney.fetchall()
		money = []
		for monx in monthly:
			mon = monx[0]
			yyyy = monx[1]
			amount = monx[2]
			money.append({"mon":mon, "yyyy":yyyy, "amount":amount})
		return {"month": money}


class Daily_Desk_Cash(Resource):
	""" Class Sum all Daily total dane by reception"""
	def get(self):
		curr_maney.execute("SELECT SUM(amount) FROM desk WHERE payments = 'Cash' AND created_on BETWEEN NOW() - INTERVAL '24 HOURS' AND NOW()")
		cashflow.commit()
		dayTotal = curr_maney.fetchall()
		return {"cash": dayTotal}


class Weekly_Desk_Cash(Resource):
	""" Class Sum all weekly total for client booked by Cash"""
	def get(self):
		curr_maney.execute("SELECT SUM(amount) FROM desk WHERE payments = 'Cash' AND created_on > current_date - interval '7 days'")
		cashflow.commit()
		weeklyTotal = curr_maney.fetchall()
		return {"cash": weeklyTotal}


class Monthly_Desk_Sum_Desk(Resource):
	""" Class sum all Monthly on  reception paid with M-pesa """
	def get(self):
		curr_maney.execute("SELECT to_char(created_on, 'Mon') AS mon, EXTRACT(year FROM created_on) AS yyyy, SUM(amount) AS amount FROM desk WHERE payments = 'Cash' GROUP BY 1,2 LIMIT 1")
		cashflow.commit()
		monthly = curr_maney.fetchall()
		money = []
		for monx in monthly:
			mon = monx[0]
			yyyy = monx[1]
			amount = monx[2]
			money.append({"mon":mon, "yyyy":yyyy, "amount":amount})
		return {"month": money}