import string
import random

def id_generator(size, characters=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(characters) for _ in range(size))