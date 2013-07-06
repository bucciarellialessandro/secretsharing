from provapoly import *
from DH import *
import threading
import socket
import re
import time


addr=""
sharers=[]
sharers_pubk=[]

dh_object_dealer=DiffieHellman()



class Dealer_rec(threading.Thread):
	def __init__(self,socket,buff=3000,nickname=None):
		threading.Thread.__init__(self)
		self.socket = socket
		self.buff = buff
		self.nickname = nickname
		self.DiffieHellman=DiffieHellman()
	def run(self):
		global addr
		global dh_object_dealer
		global sharers_pubk
		while True:
			message = str(self.socket.recv(self.buff).strip())
			if ("Client pubk:" in message):
				sharers_pubk.append(long(message.strip("Client pubk:")[0:]))		
			elif message == "1":
				if addr in sharers:
					pass
				else:
					sharers.append(addr)
					self.socket.send("I'll send you the share soon"+"\r")
					print(sharers)
			elif (message.strip()=="exit" or message.strip()=="Exit"):
				self.socket.close()
				exit()
			print("Received"+" "+message+" "+"from"+" "+str(addr[0])+","+str(addr[1])+"\r")


class Dealer_send(threading.Thread):
	def __init__(self,socket,buff=3000):
		threading.Thread.__init__(self)
		self.socket=socket
		self.buff = buff
	
	
	def run(self):
		global dh_object_dealer
		number=0
		u=True
		self.socket.send("Server pubk:"+str(dh_object_dealer.publicKey))
		self.socket.send("Type 1 if you want to share a secret with me \n")
		while True:
			message=raw_input("Server >")
			if ( message.strip() == "exit" or message == "Exit"):
				self.socket.close()
				quit()
			self.socket.send(message+"\n")
		




def startdealer():
	while True:
		a=[]
		global addr
		s=socket.socket()
		s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
		s.bind(("127.0.0.1",9999))
		s.listen(100)
		con,addr = s.accept()
		a.append(addr)
		print("Connection from {0}".format(addr))
		print(a)
		print(sharers_pubk)
		dealer = Dealer_rec(con,3000,"Dealer")
		dealer1 = Dealer_send(con,3000)
		dealer.start()
		dealer1.start()
	 	print(sharers_pubk[0])



if __name__ =="__main__":
	print dh_object_dealer.publicKey
	
	startdealer()









