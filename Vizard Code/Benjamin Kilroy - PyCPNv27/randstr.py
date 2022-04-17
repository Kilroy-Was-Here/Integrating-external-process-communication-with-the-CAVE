import random

def randStr(size):
	arr = []
	for i in range(size):
		arr.append(chr(random.randint(32,126))) # printable ascii
	return ''.join(arr)
