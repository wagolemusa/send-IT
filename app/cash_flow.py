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

connection = psycopg2.connect(dbname='d92a0rb0j8rphh', user='gaijmyignhvtkw', password='7e0acadc7013645d81437d922b7030782cdee4006cadf7f54501aa291b29d3e6', host='ec2-23-21-65-173.compute-1.amazonaws.com')
curr = connection.cursor()



class Daily_Sum(Resource):
	""" Class Sum all Daily total"""
	def get(self):
		curr.execute("SELECT SUM(amount::int) FROM payments WHERE book_id = book_id AND created_on BETWEEN NOW() - INTERVAL '24 HOURS' AND NOW()")
		connection.commit()

		dailyTotal = curr.fetchall()
		return {"num": dailyTotal}


class Weekly_Sum(Resource):
	""" Class sum all weekly""" 
	def get(self):
		curr.execute("SELECT SUM(amount::int) FROM payments WHERE book_id = book_id AND created_on BETWEEN NOW()::DATE-EXTRACT(DOW FROM NOW())::INTEGER-7 AND NOW()::DATE-EXTRACT(DOW FROM NOW())::INTEGER")
		connection.commit()
		weekly = curr.fetchall()
		return {"week": weekly}

class Monthly_Sum(Resource):
	def get(self):
		curr.execute("SELECT to_char(created_on, 'Mon') AS mon, EXTRACT(year FROM created_on) AS yyyy, SUM(amount::int) AS amount FROM payments WHERE book_id = book_id GROUP BY 1,2")
		connection.commit()
		monthly = curr.fetchall()
		money = []
		for monx in monthly:
			mon = monx[0]
			yyyy = monx[1]
			amount = monx[2]
			money.append({"mon":mon, "yyyy":yyyy, "amount":amount})
		return {"month": money}