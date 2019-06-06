#!/usr/bin/python3

"""
Python3 Script to check Status, PING ICMP, DNS/IP for IP Pool List.
"""
import subprocess
import csv
import socket
import ipaddress

# ip_list = ["10.0.0.1", "192.168.0.1", "192.168.0.11", "192.168.0.100",\
# 			"192.168.0.10", "192.168.0.9", "192.168.0.20", "google.com",
# 			"facebook.com","instagram.com"]


def ip_pinger(ip):
	'''
	This function return True if Ping ICMP is Successful. 
	'''
	ping_getstatus = subprocess.run(["ping", "-c1", "-w1", ip], stdout=subprocess.PIPE)
	success = ping_getstatus.returncode
	if (success == 0):
	    return "UP"
	else:
	    return "DOWN"


def check_ip_dns(ip):
	'''
	This function use check_name and check_ip functions to
	test wich one it is.
	'''
	def check_name(ip):
		'''
		This function check DNS.
		'''
		try:   
			socket.gethostbyname(ip)  
			return True
		except socket.error:
			return False

	def check_ip(ip):	
		'''
		This function check IP.
		'''
		try:
			ipaddress.ip_address(ip)
			return True
		except ValueError:
			return False

	if check_ip(ip) is True:
		return "IP"
	elif check_name(ip) is True:
		return "DNS"
	else:
		return "Unknown"


def main():
	'''
	This function open a file and get all the IP in it
	to test and get some info. 
	'''
	with open("ip_pool.txt", "r") as csv_file:
		rfile	=	csv.reader(csv_file, delimiter=',')
		for ip_pool in rfile:
			for ip in ip_pool:
				print("<IP:> {} <Status:> {} <IP/DNS:> {}".format(
								ip, ip_pinger(ip), check_ip_dns(ip)))
	csv_file.close()


if __name__ == "__main__":
	main()
