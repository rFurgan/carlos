import random

class Actor():

	def __init__(self, transform, blueprint, ai=None):
		self.transform = transform
		self.blueprint = blueprint
		self.ai = ai

class RoadUser():
	def __init__(self, world):
		self.world = world
		self.spawn_points = self.world.get_map().get_spawn_points()
		# self.blueprints = self.world.get_blueprint_library()
		self.walker_blueprints = self.world.get_blueprint_library().filter('walker.*')
		# self.vehicle_blueprints = self.world.get_blueprint_library().filter('vehicle.*')
		self.walker_ai = self.world.get_blueprint_library().find('controller.ai.walker')


	def __get_transform(self):
		random.shuffle(self.spawn_points)
		return random.choice(self.spawn_points)

	def __get_walker_ai(self):
		return self.walker_ai

	def __get_walker_blueprint(self):
		return random.choice(self.walker_blueprints.filter('walker'))

	def __get_vehicle_blueprint(self):
		return random.choice(self.blueprints.filter('vehicle'))

	def get_walker(self):
		return Actor(self.__get_transform(), self.__get_walker_blueprint(), self.__get_walker_ai())

	def get_vehicle(self):
		return Actor(self.__get_transform(), self.__get_vehicle_blueprint())
	