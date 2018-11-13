# sentIT
[![Build Status](https://travis-ci.org/wagolemusa/send-IT.svg?branch=challenge-2)](https://travis-ci.org/wagolemusa/send-IT)
[![Coverage Status](https://coveralls.io/repos/github/wagolemusa/send-IT/badge.svg?branch=challenge-2)](https://coveralls.io/github/wagolemusa/send-IT?branch=challenge-2)
[![Maintainability](https://api.codeclimate.com/v1/badges/4c9728803fd8f046cdce/maintainability)](https://codeclimate.com/github/wagolemusa/send-IT/maintainabilit

SendIT is a courier service that helps users deliver parcels to different destinations. SendIT  provides courier quotes based on weight categories.

### Features

1. Users can create an account.
2. User can login.
3. User can logout.
4. User can create a parcel delivery order.
5. User can get all parcel delivery orders.
6. User can get a specific parcel delivery order.
7. User can cancel a parcel delivery order.
8. User can update a parcel delivery order.


### Installing

*Step 1*

Create directory
```$ mkdir sendit```

```$ cd sendit```

Create and activate virtual environment

```$ virtualenv -p /usr/bin/python3 venv```


```$ source venv/bin/activate```

### Clone the repository

https://github.com/wagolemusa/send-IT.git


Install dependencies for the project

```$ pip install -r requirements.txt```


#### Users Endpoints : /api

Method | Endpoint | Functionality
--- | --- | ---
POST | /v1/auth/signup | Create a user account
POST | /v1/auth/signin | Sign in a user
GET  | /v1/users | Get all users
POST | /v1/auth/logout | Sign out a user

#### Parcels Endpoints : /api

Method | Endpoints | Functionality
---| --- | ---
GET 	| / | Home
POST  | /v1/parcels | Post a parcel.
GET   | /v1/parcels | Get all parcel.
GET   | /v1/paecels/int:parcel_id| Get an parcel by ID.
PUT   | /v1/paecels/int:parcel_id| Update an parcel by ID.
DELETE  | /v1/paecels/int:parcel_id| Get an parcel by ID.


Hosted on Heroku[```here```](https://senditparcel.herokuapp.com/api/) 