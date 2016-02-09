#!/bin/env python
# -*- coding: utf8 -*-

import sys
from ghost import Ghost

def site_capture():
	print(sys.argv[1])
	print(sys.argv[2])
	
	try:
		g = Ghost()
		r = g.open(sys.argv[1])
		g.capture_to(sys.argv[2])

		g.exit()
		print('success')
	except Exception, e:
		print('fail' + str(e))
		pass

if __name__ == '__main__':
	site_capture()
