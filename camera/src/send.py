import time
import requests
import queue
import json
import logging
from datetime import datetime
import threading

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 定义队列的最大容量
MAX_QUEUE_SIZE = 10

# 函数：从队列发送数据到 Django
def send_message_to_django(q):
    while True:
        # 检查队列是否有数据
        if not q.empty():
            try:
                dict_data = q.get()  # 从队列中获取数据

                # 为数据添加时间戳
                dict_data['timestamp'] = datetime.now().isoformat()

                # 要发送数据的 URL
                api_url = "http://49.213.238.75:8000/app/"
                headers = {"Content-Type": "application/json"}  # 设置正确的 Content-Type

                # 将数据发送到 Django
                response = requests.post(api_url, json=dict_data, headers=headers)

                # 记录状态码
                logger.info(f"发送数据到 Django，状态码 -> {response.status_code}")

            except Exception as e:
                logger.error(f"向 Django 发送数据时出错: {e}")

        # 休息片刻
        time.sleep(0.05)  # 根据需要调整

# 函数：添加数据到队列
def add_to_queue(q, data):
    if q.qsize() >= MAX_QUEUE_SIZE:  # 如果队列已满
        # 清除当前队列中的所有数据
        while not q.empty():
            q.get()  # 清空队列
        logger.warning("队列已满，清除所有数据并添加新数据。")

    q.put(data)  # 将新的数据加入队列

# 示例用法
q = queue.Queue()

# 创建线程以发送队列中的消息
threading.Thread(target=send_message_to_django, args=(q,), daemon=True).start()

# 添加示例数据到队列
example_data = {"sensor": "temperature", "value": 23.5}
add_to_queue(q, example_data)

# 添加更多示例数据
example_data_2 = {"sensor": "humidity", "value": 60}
add_to_queue(q, example_data_2)
