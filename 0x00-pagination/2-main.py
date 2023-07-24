#!/usr/bin/env python3
"""
Main file
"""
from pprint import pprint

Server = __import__("2-hypermedia_pagination").Server

server = Server()

pprint(server.get_hyper(1, 2))
pprint("---")
pprint(server.get_hyper(2, 2))
pprint("---")
pprint(server.get_hyper(100, 3))
pprint("---")
pprint(server.get_hyper(3000, 100))
