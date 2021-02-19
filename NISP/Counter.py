


class Counter:
	def __init__(self):
		self.value = 0
	def __iadd__(self,other_value):
		self.value += other_value
	def get_counter(self):
		return self.value