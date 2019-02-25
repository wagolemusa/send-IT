# import json

# # some JSON:
# x = '{ "name":"John", "age":30, "city":"New York"}'

# # parse x:
# y = json.loads(x)

# # the result is a Python dictionary:
# print(y)
# print(y["age"])
# print(y["name"])



import json
json_data = '{"Body":{"stkCallback":{"MerchantRequestID":"22531-976234-1","CheckoutRequestID":"ws_CO_DMZ_250600506_23022019144745852","ResultCode":0,"ResultDesc":"The service request is processed successfully.","CallbackMetadata":{"Item":[{"Name":"Amount","Value":1.00},{"Name":"MpesaReceiptNumber","Value":"NBN52K8A1J"},{"Name":"Balance"},{"Name":"TransactionDate","Value":20190223144807},{"Name":"PhoneNumber","Value":254725696042}]}}}}'
data = json.loads(json_data)

# paid = ""
# faild = ""

json_da = data['Body']

# list_data = data['CallbackMetadata']

m = []

print (json_da)

# print (list_data)

merchant = json_da['stkCallback']['MerchantRequestID']
resultcode = json_da['stkCallback']['ResultCode']
checkout = json_da['stkCallback']['CheckoutRequestID']
resultdesc = json_da['stkCallback']['ResultDesc']

def status():
	if resultcode == 0:
		return "paid"
	elif resultcode == 1:
		return "faild"
	else:
		return "badrequest"




print()
print('mat' " " + merchant)
print(resultcode)
print(checkout)
print(resultdesc)
print()
print()
print()

p = status()
print(p)