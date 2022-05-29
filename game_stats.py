class GameStats():
	#Отслеживание статистики
	def __init__(self,ai_game):
		self.settings = ai_game.settings
		self.reset_stats()
		#Игра запускается в неактивном состоянии
		self.game_active = False
		#Рекорд не должен сбрасываться
		self.high_score = 0

	def reset_stats(self):
		#Инициализирует статистику, изменяющуюся в ходе игры
		self.ships_left = self.settings.ship_limit
		self.score = 0
		self.level = 1