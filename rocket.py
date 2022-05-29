import pygame
from pygame.sprite import Sprite
class Rocket(Sprite):
	def __init__(self,vs):
		super(). __init__()
		self.screen = vs.screen
		self.screen_rect = vs.screen.get_rect()
		self.image = pygame.image.load('rocket.jpg')
		self.rect = self.image.get_rect()

		self.rect.midleft = vs.ship.image_rect.midright
		self.rect.x = float(self.rect.x)


	def draw(self):
		self.screen.blit(self.image, self.rect)

	def update(self):
		self.rect.x += 1