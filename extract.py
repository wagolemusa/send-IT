


# import json
# json_data = '{"Body":{"stkCallback":{"MerchantRequestID":"22531-976234-1","CheckoutRequestID":"ws_CO_DMZ_250600506_23022019144745852","ResultCode":0,"ResultDesc":"The service request is processed successfully.","CallbackMetadata":{"Item":[{"Name":"Amount","Value":1.00},{"Name":"MpesaReceiptNumber","Value":"NBN52K8A1J"},{"Name":"Balance"},{"Name":"TransactionDate","Value":20190223144807},{"Name":"PhoneNumber","Value":254725696042}]}}}}'
# data = json.loads(json_data)

# # paid = ""
# # faild = ""

# json_da = data['Body']

# # list_data = data['CallbackMetadata']


# print (json_da)

# # print (list_data)

# merchant = json_da['stkCallback']['MerchantRequestID']
# resultcode = json_da['stkCallback']['ResultCode']
# checkout = json_da['stkCallback']['CheckoutRequestID']
# resultdesc = json_da['stkCallback']['ResultDesc']

# def status():
# 	if resultcode == 0:
# 		return "paid"
# 	elif resultcode == 1:
# 		return "failed"
# 	else:
# 		return "badrequest"




# print()
# print('mat' " " + merchant)
# print(resultcode)
# print(checkout)
# print(resultdesc)
# print()
# print()
# print()

# p =  status()
# print (p)



import json
me = {"Body":{"stkCallback":{"MerchantRequestID":"22531-976234-1","CheckoutRequestID":"ws_CO_DMZ_250600506_23022019144745852","ResultCode":0,"ResultDesc":"The service request is processed successfully.","CallbackMetadata":{"Item":[{"Name":"Amount","Value":1.00},{"Name":"MpesaReceiptNumber","Value":"NBN52K8A1J"},{"Name":"Balance"},{"Name":"TransactionDate","Value":20190223144807},{"Name":"PhoneNumber","Value":254725696042}]}}}}

data = json.dumps(me)


print (data)
# paid = ""
# faild = ""

json_da = me.get('Body')# -> the only thing changed. use dict.get(key) which returns the content inside the body.

list_data = me.get('Item')


print (json_da)

print (list_data)

merchant = json_da['stkCallback']['MerchantRequestID']
resultcode = json_da['stkCallback']['ResultCode']
checkout = json_da['stkCallback']['CheckoutRequestID']
resultdesc = json_da['stkCallback']['ResultDesc']

CallbackMetadata = json_da['stkCallback']['CallbackMetadata']

yes = CallbackMetadata.get('Item')


serial = ['CallbackMetadata']['MpesaReceiptNumber']

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
print(yes)
# print(CallbackMetadata)
print(serial)

p = status()
print(p)