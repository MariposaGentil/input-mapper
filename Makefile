run: 
	python main.py -d "2.4G Wireless Optical Mouse  Mouse" -p MOUSE_SPOTY_PROFILE -g

run2: 
	python main.py -d "AT Translated Set 2 keyboard" -a -p DEFAULT_PROFILE

list: 
	python main.py -l

mouse:
	python main.py -l -d "mouse"

example:
	python example.py

help:
	python main.py --help