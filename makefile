.PHONY: camera show run check_port kill_port

# 默认参数
use_device ?= 0
ip ?= 0.0.0.0
port ?= 8000

# 检测操作系统
UNAME_S := $(shell uname -s)

# macOS 和 Windows 的虚拟环境激活命令
ifeq ($(UNAME_S), Darwin)
    ACTIVATE_CMD = source .venv/bin/activate
    CHECK_PORT_CMD = lsof -i :$(port)
    KILL_PORT_CMD = lsof -ti :$(port) | xargs kill -9
else
    ACTIVATE_CMD = .venv\Scripts\activate
    CHECK_PORT_CMD = netstat -ano | findstr :$(port)
    KILL_PORT_CMD = for /f "tokens=5" %a in ('netstat -ano ^| findstr :$(port)') do taskkill /f /pid %a
endif

# 检查端口是否被占用，并在占用时终止进程
check_port:
	@echo "Checking if port $(port) is in use..."
	@if $(CHECK_PORT_CMD); then \
		echo "Port $(port) is in use, attempting to free it..."; \
		$(KILL_PORT_CMD); \
	else \
		echo "Port $(port) is free"; \
	fi

# show 目标
show: check_port
	$(ACTIVATE_CMD) && python camera.py

# camera 目标
camera: check_port
	$(ACTIVATE_CMD) && python camera/main.py --use_device=$(use_device) --ip=$(ip) --port=$(port)

# run 目标
run: check_port
	$(ACTIVATE_CMD) && cd server && python manage.py runserver $(ip):$(port)

test_js:
	npm test