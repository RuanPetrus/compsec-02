import numpy as np

rctab = [-1] * 500
MASK8 = (1 << 8) - 1
MASK32 = (1 << 32) - 1
KEY_LEN = 128

N = 4 # number of 32 bit words in original key

def get_words(key, total_bits=32, word_bits=8):
	result = []	
	mask = (1 << word_bits) - 1
	for i in range(total_bits//word_bits):
		result.append(key & mask)
		key >>= word_bits
	return result[::-1]

def get_num(words : list[int], word_sz=8) -> int:
	result=0
	for word in words:
		result <<= word_sz
		result |= word

	return result

def rc(i : int) -> int:
	if i == 1: return 1
	if rctab[i] != -1: return rctab[i]

	last = rc(i-1)
	if last < 0x80: 
		rctab[i] = (2*last) & MASK8
		return rctab[i]
	
	rctab[i] = ((2*last) ^ 0x11B) & MASK8
	return rctab[i]

def rcon(i : int) -> int:
	return get_num([rc(i),0,0,0])


def subword(x: int, sbox) -> int:
	words = get_words(x, 32, 8)
	words = [sbox[word] for word in words]
	return get_num(words)

def rotword(x : int) -> int:
	words = np.roll(get_words(x,32,8), -1)
	return get_num(words)


def getkeys(key, rounds, sbox):
	key_words = get_words(key, KEY_LEN, 32)
	
	for i in range(N, 4*rounds):
		last_w = key_words[i-1]
		old_w = key_words[i-N]
		if i % N == 0:
			new_w = subword(rotword(last_w), sbox) ^ rcon(i//N) ^ old_w
			key_words.append(new_w)
		elif N > 6 and i % N == 4:
			new_w = old_w ^ subword(last_w,sbox)
			key_words.append(new_w)
		else:
			new_w = old_w ^ last_w
			key_words.append(new_w)
	
	return key_words


	

