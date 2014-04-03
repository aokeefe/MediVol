import uuid

def id_generator(size):
	return uuid.uuid4().hex[:size]