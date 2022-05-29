class Settings():
	def __init__(self):
		"""Инициализирует статические настройки игры"""
		#Настройки экрана
		self.screen_width = 1200
		self.screen_height = 600
		self.bg_color = (150,200,255)
		
		#Настройки корабля
		self.ship_limit = 3

		#Настройки снарядов
		self.bullet_widht = 5
		self.bullet_height = 20
		self.bullet_color = (60,60,60)
		self.bullets_allowed = 5

		#Настройки пришельцев
		self.fleet_drop_speed = 10
		
		#Темп ускорения игры
		self.speedup_scale = 1.5

		#Темп роста стоимости пришельцев
		self.score_scale = 1.5

		self.initialize_dynamic_settings()

	def initialize_dynamic_settings(self):
		self.ship_speed = 1.5
		self.bullet_speed = 3.0
		self.alien_speed = 1.0
		#Подсчет очков
		self.alien_points = 50

		#fleet_direction = 1 движение вправо -1 движение влево
		self.fleet_direction = 1		

	def increase_speed(self):
		"""Увеличивает настройки скорости"""
		self.ship_speed *= self.speedup_scale
		self.bullet_speed *= self.speedup_scale
		self.alien_speed *= self.speedup_scale

		#После перехода на новый уровень прирост стоимости очков за попадание
		self.alien_points = int(self.alien_points * self.score_scale)