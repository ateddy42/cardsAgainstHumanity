import numpy as np

def normalize(v):
	length = np.sqrt(np.sum(np.multiply(v,v)))
	return v/length

L = [2,0]
print normalize(L)