def my_sum(my_integer):
	results = 0
	for x in my_integer:
		results += x
	return results

list_of_integers = [1,2,3]
print(my_sum(list_of_integers))