import pygame.font

class Button():
	def __init__(self,ai_game,msg):
		"Инициализирует атрибуты кнопки."
		self.screen = ai_game.screen
		self.screen_rect = self.screen.get_rect()

		"Назначение размеров и свойств кнопок"
		self.width, self.height = 200, 50
		self.button_color = (0,0,255)
		self.text_color = (255,255,255)
		self.font = pygame.font.SysFont(None, 48)

		#Построение объекта rect кнопки и выравнивание по центру
		self.rect = pygame.Rect(0,0,self.width,self.height)
		self.rect.x = self.screen_rect.centerx - 100
		self.rect.y = self.screen_rect.y + 450

		#Сообщение кнопки создается только один раз
		self._prep_msg(msg)

	def _prep_msg(self,msg):
		self.msg_image = self.font.render(msg,True,self.text_color,self.button_color)
		self.msg_image_rect = self.msg_image.get_rect()
		self.msg_image_rect.center = self.rect.center

	def draw_button(self):
		#Отображение пустой кнопки и вывод сообщения
		self.screen.fill(self.button_color,self.rect)
		self.screen.blit(self.msg_image, self.msg_image_rect)