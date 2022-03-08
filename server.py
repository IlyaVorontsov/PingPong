import socket


SERVER_IP = ('127.0.0.1', 8888)
PASSWORD = '1234'

class UDP_server:
	def __init__(self, SERVER_IP):
		self.SERVER_IP = SERVER_IP
		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.server_socket.bind(self.SERVER_IP)
		self.client_list = []


	def send_to_client(self, addr, data):
		data = bytes(str(data), encoding='utf-8')
		self.server_socket.sendto(data, addr)

	
	def recive_from_client(self):
		data, addr = self.server_socket.recvfrom(4096)
		return data, addr

	
	def connection_check(self):
		while len(self.client_list) < 2:
			data, addr = self.server_socket.recvfrom(4096)
			if data.decode('utf-8') == PASSWORD:
				if len(self.client_list) == 0:
					self.client_list.append({'Player1': addr})
					self.send_to_client(addr, '201')
					print('[*] Player1 connected')
				elif len(self.client_list) == 1:
					self.client_list.append({'Player2': addr})
					self.send_to_client(addr, '202')
					print('[*] Player2 connected')


	def send_start_flag(self):
		self.send_to_client(self.client_list[0]['Player1'], 'True')
		self.send_to_client(self.client_list[1]['Player2'], 'True')		


	def run(self):
		self.connection_check()
		self.send_start_flag()
		while True:
			try:
				data, addr = self.server_socket.recvfrom(4096)
				if addr == self.client_list[0]['Player1']:
					self.send_to_client(self.client_list[1]['Player2'], data)
				elif addr == self.client_list[1]['Player2']:
					self.send_to_client(self.client_list[0]['Player1'], data)
			except KeyboardInterrupt:
				self.server_socket.close()
				break

if __name__ == '__main__':
	server = UDP_server()
	server.run()