class Vehicle:
	def __init__(self, registration_num, driver_age):
		self.driver_age = driver_age
		self.registration_num = registration_num


class Car(Vehicle):
	def __init__(self, registration_num, driver_age):
		Vehicle.__init__(self, registration_num, driver_age)
