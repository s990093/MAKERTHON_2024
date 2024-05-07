show:
	source .venv/bin/activate && python camera.py

camera:
	source .venv/bin/activate && python camera/main.py --use_device = 0 --ip = 8000 --port = 8000


run:
	source .venv/bin/activate && server/python manage.py 0.0.0.0:8000