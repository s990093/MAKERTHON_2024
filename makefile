show:
	source .venv/bin/activate && python camera.py

camera:
	source .venv/bin/activate && python camera/main.py --use_device = 0 --ip = 8000 --port = 8000
