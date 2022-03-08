import pygame as pg
import sys
import constants as const
import socket


class PlatformP1:
	
	def __init__(self):
		self.x = const.indent
		self.y = const.HEIGHT//2 - const.platform_len//2
		self.platform_surface = pg.Surface((const.indent, const.platform_len))
		self.platform_rect = pg.Rect((self.x, self.y, const.indent, const.platform_len))

	
	def move_up(self, platform_speed):
		if self.y > 0:
			self.y -= platform_speed
			self.platform_rect = pg.Rect((self.x, self.y, const.indent, const.platform_len))

	
	def move_down(self, platform_speed):
		if self.y < const.HEIGHT - const.platform_len:
			self.y += platform_speed
			self.platform_rect = pg.Rect((self.x, self.y, const.indent, const.platform_len))


	def draw(self, screen):
		self.platform_surface.fill(const.WHITE)
		screen.blit(self.platform_surface, self.platform_rect)


class PlatformP2(PlatformP1):
	def __init__(self):
		self.x = const.WIDTH - 2*const.indent
		self.y = const.HEIGHT//2 - const.platform_len//2
		self.platform_surface = pg.Surface((const.indent, const.platform_len))
		self.platform_rect = pg.Rect((self.x, self.y, const.indent, const.platform_len))


class Ball:
	
	def __init__(self, screen):
		self.screen = screen
		self.x = const.WIDTH//2
		self.y = const.HEIGHT//2
		self.ball_surface = pg.Surface((20, 20))
		self.ball_rect = pg.draw.circle(self.screen, const.WHITE, (self.x, self.y), 10)
		self.ball_speed = const.ball_speed
		self.is_collide_p1 = False
		self.is_collide_p2 = False

	def collide_check(self, platform_rect_p1, platform_rect_p2):
		self.is_collide_p1 = self.ball_rect.colliderect(platform_rect_p1)
		self.is_collide_p2 = self.ball_rect.colliderect(platform_rect_p2)

	def reflect_check(self):
		if self.is_collide_p1 or self.ball_rect.left <= 0:
			self.ball_speed = (self.ball_speed[0]*(-1), self.ball_speed[1]*(-1))
		if self.is_collide_p2 or self.ball_rect.right >= const.WIDTH:
			self.ball_speed = (self.ball_speed[0]*(-1), self.ball_speed[1])
		if self.ball_rect.top <= 0:
			self.ball_speed = (self.ball_speed[0], self.ball_speed[1]*(-1))
		if self.ball_rect.bottom >= const.HEIGHT:
			self.ball_speed = (self.ball_speed[0], self.ball_speed[1]*(-1))
		
	def move(self):
		self.reflect_check()
		self.x += self.ball_speed[0]
		self.y += self.ball_speed[1]

	def draw(self):
		self.ball_rect = pg.draw.circle(self.screen, const.WHITE, (self.x, self.y), 10)

class Game:

	def __init__(self, screen):
		#self.screen = pg.display.set_mode((const.WIDTH, const.HEIGHT))
		self.screen = screen
		self.clock = pg.time.Clock()
		self.platform_p1 = PlatformP1()
		self.platform_p2 = PlatformP2()
		self.ball = Ball(self.screen)
		self.platform_speed = const.platform_speed
		self.ball_speed = const.ball_speed
		self.move_flag_p1 = None
		self.move_flag_p2 = None


	def event_check(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				sys.exit()
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_UP:
					self.move_flag_p1 = 'UP'
				elif event.key == pg.K_DOWN:
					self.move_flag_p1 = 'DOWN'
				elif event.key == pg.K_w:
					self.move_flag_p2 = 'UP'
				elif event.key == pg.K_s:
					self.move_flag_p2 = 'DOWN'
			elif event.type == pg.KEYUP:
				if event.key in (pg.K_UP, pg.K_DOWN, pg.K_w, pg.K_s):
					self.move_flag_p1, self.move_flag_p2 = None, None

	
	def move_platform_p1(self, flag=None):
		if flag == 'UP':
			self.platform_p1.move_up(self.platform_speed)
		if flag == 'DOWN':
			self.platform_p1.move_down(self.platform_speed)

	def move_platform_p2(self, flag=None):
		if flag == 'UP':
			self.platform_p2.move_up(self.platform_speed)
		if flag == 'DOWN':
			self.platform_p2.move_down(self.platform_speed)		


	def run(self):
		while True:
			self.screen.fill(const.GREEN)
			self.event_check()
			self.move_platform_p1(self.move_flag_p1)
			self.move_platform_p2(self.move_flag_p2)
			self.platform_p1.draw(self.screen)
			self.platform_p2.draw(self.screen)
			self.ball.collide_check(self.platform_p1.platform_rect, self.platform_p2.platform_rect)
			self.ball.move()
			self.ball.draw()
			pg.display.update()
			self.clock.tick(const.FPS)


if __name__ == '__main__':
	game = Game()
	game.run()