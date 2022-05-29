import sys
from time import sleep

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import ScoreBoard

class AlienInvasion:
	"""Класс для упрвления ресурсами и поведением игры"""
	def __init__(self):
		"""Инициализирует игру и создает игровые ресурсы"""
		pygame.init()
		self.settings = Settings()
		self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))			#Установка разрешения окна импортируется из модуля Settings
		#self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
		self.settings.screen_width = self.screen.get_rect().width

		self.bg = pygame.image.load('images/bg.jpg')

		self.settings.screen_height = self.screen.get_rect().height
		pygame.display.set_caption("Alien Invasion")
		#Создание экземпляра для хранения игровой статистики
		self.stats = GameStats(self)
		self.sb = ScoreBoard(self)
		self.ship = Ship(self)
		self.bullets = pygame.sprite.Group()
		self.aliens = pygame.sprite.Group()
		self._create_fleet()
		#Создание кнопки Play
		self.play_button = Button(self,"Play")

	def run_game(self):
		"""Запуск основного цикла игры"""
		while True:
			self._check_events()
			if self.stats.game_active:
				self.ship.update()
				self._update_bullets()
				self._update_aliens()
			
			self._update_screen()
			self.bullets.update()


	def _check_events(self):							#Вспомогательный метод для метода run_game начинается с _
		"""Отслеживание событий клавиатуры и мыши"""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				self._check_play_button(mouse_pos)

			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)

			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)

	def _check_play_button(self,mouse_pos):
		#Запускает новую игру при нажатии кнопки PLay
		button_clicked = self.play_button.rect.collidepoint(mouse_pos)
		if button_clicked and not self.stats.game_active:
			self.settings.initialize_dynamic_settings()
			self.stats.reset_stats()
			self.stats.game_active = True
			self.sb.prep_score()
			self.sb.prep_level()
			self.sb.prep_ships()

			#Очистка списков пришельцев и снарядов
			self.aliens.empty()
			self.bullets.empty()

			#Создание нового флота и размещение корабля в центре
			self._create_fleet()
			self.ship.center_ship()

			#Указатель мыши скрывается
			pygame.mouse.set_visible(False)


	def _check_keydown_events(self,event):
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = True
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = True
		elif event.key == pygame.K_SPACE:
			self._fire_bullet()
		elif event.key == pygame.K_q:
			sys.exit()

	def _check_keyup_events(self,event):
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = False
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = False

	def _fire_bullet(self):
		"""Создание нового снаряда и включение его в  группу bullets"""
		if len(self.bullets) < self.settings.bullets_allowed:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)

	def _update_bullets(self):
		#Обновляет позиции снарядов и удаляет старые пули
		for bullet in self.bullets.copy():
			if bullet.rect.bottom <= 0:
				self.bullets.remove(bullet)
		self._check_bullet_alien_collisions()

	def _check_bullet_alien_collisions(self):
		#Обработка коллизий снарядов с прищельцами
		#При обнаружении попадания удалить снаряд и пришельца
		collisions = pygame.sprite.groupcollide(self.bullets,self.aliens,True,True)
		if collisions:
			for aliens in collisions.values():
				self.stats.score += self.settings.alien_points * len(aliens)
			self.sb.prep_score()
			self.sb.check_high_score()
		#Уничтожение существующих снарядов и создние нового флота
		if not self.aliens:
			self.bullets.empty()
			self._create_fleet()
			self.settings.increase_speed()

			#Увеличение уровня
			self.stats.level += 1
			self.sb.prep_level()

	def _update_aliens(self):
		#Проверяет, достиг ли флот края экрана
		self._check_fleet_edges()
		#Обновляет позиции всех пришельцев
		self.aliens.update()
		if pygame.sprite.spritecollideany(self.ship,self.aliens):
			self._ship_hit()
		#Проверить, добрались ли пришельцы до нижнего края
		self._check_aliens_bottom()

	def _ship_hit(self):
		#Обрабатывает столкновение корабля с пришельцем
		if self.stats.ships_left > 0:
			#Уменьшение количества кораблей и обновление счета кораблей
			self.stats.ships_left -= 1
			self.sb.prep_ships()
			#Очистка списка пишельцев и снарядов
			self.aliens.empty()
			self.bullets.empty()
			#Создание нового флота и размещение корабля в центре
			self._create_fleet()
			self.ship.center_ship()
			#Пауза
			sleep(0.5)
		else:	
			self.stats.game_active = False
			pygame.mouse.set_visible(True)

	def _check_aliens_bottom(self):
		#Проверяет, добрались ли пришельцы до нижнего края экрана
		screen_rect = self.screen.get_rect()
		for alien in self.aliens.sprites():
			if alien.rect.bottom >= screen_rect.bottom:
				#Происходит то же что и при столкновении с кораблем
				self._ship_hit()
				break

	def _create_fleet(self):
		"""Создание флота пришельцев"""
		#Создание пришельца и вычисление количества пришельцев в ряду
		#Интервал между соседними пришельцами равен ширине пришельца
		alien = Alien(self)
		allien_width,alien_height = alien.rect.size
		available_space_x = self.settings.screen_width - (2 * allien_width)
		number_aliens_x = available_space_x//(2*allien_width)
		"""Определят количество рядов, помещающихся на экране"""
		ship_height = self.ship.rect.height
		available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
		number_rows = 3 #available_space_y // ( alien_height)

		#Создание флота вторжения
		for row_number in range(number_rows):
			for alien_number in range(number_aliens_x):
				self._create_alien(alien_number,row_number)

	def _create_alien(self,alien_number,row_number):
			#Создание пришельца и размещение его в ряду
			alien = Alien(self)
			allien_width, alien_height = alien.rect.size
			alien.x = allien_width + 2.5 * allien_width * alien_number
			alien.rect.x = alien.x
			alien.rect.y = 20 + alien.rect.height +   1.2* alien.rect.height * row_number		# умножить на 2
			self.aliens.add(alien)
				

	def _check_fleet_edges(self):
		#Реагирует на достижение пришельцем края экрана
		for alien in self.aliens.sprites():
			if alien.check_edges():
				self._change_fleet_direction()
				break

	def _change_fleet_direction(self):
		#Опускает весь флот вниз и меняет направление
		for alien in self.aliens.sprites():
			alien.rect.y += self.settings.fleet_drop_speed
		self.settings.fleet_direction *= -1

	def _update_screen(self):							#Вспомогательный метод для метода run_game начинается с _
		"""При каждом прохождении цикла перерисовывается экран"""
#		self.screen.fill(self.settings.bg_color)					#Импортируется из модуля Settings
		self.screen.blit(self.bg, (0,0))
		self.ship.blitme()
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()
		self.aliens.draw(self.screen)
		self.sb.show_score()

		#Кнопка PLay отображается если игра неактивна
		if not self.stats.game_active:
			self.play_button.draw_button()
		"""Отображение последнего прорисованного экрана"""
		pygame.display.flip()



if __name__ == '__main__':
	"""Создание экземпляра и запуск игры"""
	ai = AlienInvasion()
	ai.run_game()
