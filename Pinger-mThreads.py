#!/usr/bin/python3

"""
Python3 Script to check Status, PING ICMP, DNS/IP for Host/IP Pool List.
"""
import subprocess
import socket
import ipaddress
import logging
import csv
from concurrent.futures import ThreadPoolExecutor
# import multiprocessing
# import threading

# ip_list = ["10.0.0.1", "192.168.0.1", "192.168.0.11", "192.168.0.100",\
# 			"192.168.0.10", "192.168.0.9", "192.168.0.20", "google.com",
# 			"facebook.com","instagram.com"]

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s\
                     - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


def ip_pinger(host):
    '''
    This function return True if Ping ICMP is Successful.
    '''
    ping_getstatus = subprocess.run(["ping", "-c1", "-w1", host],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
    success = ping_getstatus.returncode
    if (success == 0):
        return "UP"
    else:
        return "DOWN"


def check_ip_dns(host):
    """Check whether host is ip or dns type.
    """
    try:
        if (socket.gethostbyname(host) != host):
            return ("DNS")
        elif ipaddress.ip_address(host):
            return ("IP")
    except socket.gaierror:
        return ("Unknown")


def iplist_from_file(filetxt):
    '''
    This function open a file and get all the IP in it
    creating a list.
    '''
    ippool = []
    with open(filetxt, "r") as f:
        file_read = csv.reader(f, delimiter=',')
        for line in file_read:
            ippool += line

    f.close()
    return ippool


def main(host):
    '''
    This func recieved an IP and show info such as:
    ip, status, dns or not.
    '''
    print("HostName: {ipaddr} | HostStatus: {status} | HostType: {ipordns}"
          .format(ipaddr=host, status=ip_pinger(host),
                  ipordns=check_ip_dns(host)))


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    jobs = []

    logging.basicConfig(format=format, level=logging.DEBUG,
                        datefmt="%H:%M:%S")

    # IP List for multiprocessing
    iplist = iplist_from_file("ip_pool.txt")
    cores = 4

    # Multiprocessing code for fast operation.
    # Using func map to apply main func to IP List.

    with ThreadPoolExecutor() as executor:
        executor.map(main, iplist)

# for t in range(0, threads):
# thread = threading.Thread(target=main())
# jobs.append(thread)
