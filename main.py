import pygame as pg
import sys
import constants as const
from threading import Thread
from time import sleep
from input_box import InputBox
import ipaddress


SERVER_IP = '192.168.1.248', 8888


def validate_ip(row_ip):
	try:
		ip, port = row_ip.split(':')
	except Exception:
		return False
	try:
		ipaddress.ip_address(ip)
		return True
	except ValueError:
		return False


class Game:
	def __init__(self):
		pg.init()
		self.screen = pg.display.set_mode((const.WIDTH, const.HEIGHT))
		self.clock = pg.time.Clock()
		self.font = pg.font.Font(None, 50)
		self.run_one_comp = False
		self.run_two_comp = False
		self.text_init()
		pg.display.set_caption('PingPong')

	def text_init(self):
		self.text0 = self.font.render('Ping Pong', True, const.BLACK)
		self.text1 = self.font.render('One comp game', True, const.RED, const.PINK)
		self.text2 = self.font.render('Two comp game', True, const.RED, const.PINK)
		self.text4 = self.font.render('Enter IP adress', True, const.RED, const.PINK)
		self.main_label = self.text0.get_rect(center=(const.WIDTH//2, 50))
		self.one_comp_button = self.text1.get_rect(center=(const.WIDTH//2, const.HEIGHT//2))
		self.two_comp_button = self.text2.get_rect(center=(const.WIDTH//2, const.HEIGHT//2 + 50))
		self.enter_ip_label = self.text4.get_rect(center=(const.WIDTH//2, const.HEIGHT//2 + 50))


	def event_check(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				sys.exit()
			if event.type == pg.MOUSEBUTTONDOWN:
				mouse_pos = event.pos
				if self.one_comp_button.collidepoint(mouse_pos):
					self.run_one_comp = True
				if self.two_comp_button.collidepoint(mouse_pos):
					self.run_two_comp = True


	def input_ip_screen(self):
		input_box = InputBox(const.WIDTH//2-100, 100, 100, 40)
		while True:
			for event in pg.event.get():
				if event.type == pg.QUIT:
					pg.quit()
					sys.exit()
				row_ip = input_box.handle_event(event)
				if row_ip != None:
					if validate_ip(row_ip):
						return row_ip.split(':')[0], int(row_ip.split(':')[1])
			input_box.update()
			self.screen.fill(const.WHITE)
			input_box.draw(self.screen)
			self.screen.blit(self.text4, self.enter_ip_label)
			pg.display.update()
			self.clock.tick(const.FPS)


	def main_screen(self):
		while True:
			self.event_check()
			self.screen.fill(const.WHITE)
			self.screen.blit(self.text0, self.main_label)
			self.screen.blit(self.text1, self.one_comp_button)
			self.screen.blit(self.text2, self.two_comp_button)
			pg.display.update()
			self.clock.tick(const.FPS)
			if self.run_one_comp or self.run_two_comp:
				break
		if self.run_one_comp:
			import onecomp
			game = onecomp.Game(self.screen)
			sleep(2)
			game.run()
		if self.run_two_comp:
			addr = self.input_ip_screen()
			import server
			import twocomp
			try:
				udp_server = server.UDP_server(SERVER_IP)
				server_process = Thread(target=udp_server.run)
				server_process.start()
			except OSError:
				pass
			sleep(2)
			game = twocomp.Game(self.screen, addr)
			client_process = Thread(target=game.run)
			client_process.run()

if __name__ == '__main__':
	game = Game()
	game.main_screen()