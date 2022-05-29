import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
	'''Класс управления снарядами, выпущенныи кораблем'''
	def __init__(self,ai_game):
		"""Создает объект снарядов в текущей позиции корабля"""
		super().__init__()
		self.screen = ai_game.screen
		self.settings = ai_game.settings
		self.color = self.settings.bullet_color
		"""Создание снаряда в позиции 0,0 и назначение правильной позиции"""
		self.image = pygame.image.load('images/fire1.png')
		self.rect = self.image.get_rect()

#		self.rect = pygame.Rect(0,0, self.settings.bullet_widht, self.settings.bullet_height)
		self.rect.midbottom = ai_game.ship.rect.midtop
		"""Позиция снаряда хранится в вещественном формате"""
		self.y = float(self.rect.y)

	def update(self):
		"""Перемещает снаряд вверх по экрану"""
		#Обновление позиции сняряда в вещественном формате
		self.y -= self.settings.bullet_speed
		#Обновление позиции прямоугольника
		self.rect.y = self.y

	def draw_bullet(self):
		"""Вывод снарядов на экран"""
#		pygame.draw.rect(self.screen,self.color,self.rect)
		self.screen.blit(self.image, self.rect)

