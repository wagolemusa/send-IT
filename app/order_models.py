Orders = []



class Parcel:
	def __init__(self, user_id, username, pickup, destination, weight, price, status="Transit"):
		self.user_id = user_id
		self.username = username
		self.pickup = pickup
		self.destination = destination
		self.weight = weight
		self.price = weight * 180
		self.status = status
		self.id = None

	def create_order(self):
		""" Save details in the database """
		order = {}
		order[parcel_id] = str(len(parcel)+ 1)
		order['user_id'] = self.user_id
		order['username'] = self.username
		order['pickup'] = self.pickup
		order['destination'] = self.destination
		order['weight'] = self.weight
		order['price'] = self.price
		order['status'] = self.status
		Orders.append(order)
		return order

	def all_parcel_order(self):
		return Orders

	def one_parcel_order(self, parcel_id):
		order = [ parcel for parcel in Orders if (parcel['parcel_id'] == parcelId)]
		return order

	 




