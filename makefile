.PHONY: camera
use_device ?= 0
ip ?= 0.0.0.0
port ?= 8000


show:
	source .venv/bin/activate && python camera.py


camera:
	source .venv/bin/activate && python camera/main.py --use_device=$(use_device) --ip=$(ip) --port=$(port)

run:
	source .venv/bin/activate &&  cd server && python manage.py runserver 0.0.0.0:8000