import json
import cv2 as cv
import numpy as np
import requests
from ultralytics import YOLO
import time
import multiprocessing as mp
import matplotlib.pyplot as plt

# rich
from rich import pretty
from rich import print,print_json
from rich.console import Console

pretty.install()
console = Console()
execution_times_queue = mp.Queue()
model = YOLO('yolov8s.pt')  # 确保路径正确

image_url = "http://192.168.232.185/capture"  # 确保 URL 是正确的
# # 初始化摄像头
# cap = cv.VideoCapture(0)  # 0 表示第一个摄像头
# if not cap.isOpened():
#     raise Exception("无法打开摄像头")



def send_message_to_django(json_data):
    api_url = "http://49.213.238.75:8000/app/"  # 这个URL应该是Django后端的API URL
    console.log(json_data)
    # data_to_send = json.dumps(json_data)
    response = requests.post(api_url, data=json_data)
    
    console.log(f"send data to django -> {response.status_code}")
    

def process_result(results):
    # 用于存储类别和置信度的列表
    class_probabilities = []
    people_count = 0  # 用于统计 'person' 的数量

    # 遍历检测结果
    for result in results:
        class_ids = result.boxes.cls  # 类别索引
        confidences = result.boxes.conf  # 置信度

        # 存储每个类别和它的置信度，并计数 'person'
        class_probabilities.extend(
            [(model.names[int(cls_id)], round(float(conf), 2)) for cls_id, conf in zip(class_ids, confidences)]
        )

        # 统计 'person' 的数量
        people_count += sum(1 for cls_id in class_ids if model.names[int(cls_id)] == "person")

    # 按置信度从高到低排序
    class_probabilities_sorted = sorted(class_probabilities, key=lambda x: x[1], reverse=True)

    # 提取前两个类别和置信度
    top_two = class_probabilities_sorted[:2]

    # 创建一个字典来存储结果，包括 'person' 的数量
    result_dict = {"top_objects": []}

    # 添加前两个物体及其置信度
    for obj, prob in top_two:
        result_dict["top_objects"].append({"object": obj, "confidence": prob})

    # 添加 'person' 的计数到结果字典
    result_dict["people_count"] = people_count
    
    # console.log(f"people_count -> {people_count}")

    send_message_to_django(result_dict)



# def main():
#     try:
#         while True:
#             # 读取一帧
#             ret, frame = cap.read()
#             if not ret:
#                 print("无法读取摄像头画面")
#                 break

#             # 调整图像大小
#             frame_resized = cv.resize(frame, (640, 480))

#             # 运行 YOLO 模型
#             results = model(frame_resized)

#             # 处理检测结果
#             sorted_probabilities = process_result(results)

#             # 显示处理后的结果
#             annotated_frame = results[0].plot()  # 绘制带注释的帧
#             cv.imshow("YOLO Webcam Stream", annotated_frame)

#             # 检查退出条件
#             if cv.waitKey(1) & 0xFF == ord('q'):  # 按 'q' 键退出
#                 break

#             # 可选：设置延迟以减少资源占用
#             time.sleep(0.1)  # 每帧之间等待 100 毫秒

#     finally:
#         # 清理资源
#         cap.release()  # 释放摄像头
#         cv.destroyAllWindows()  # 关闭所有 OpenCV 窗口
       
       
def yolo_process(queue):
    try:
        while True:
            start_time = time.time()

            # 获取图像
            response = requests.get(image_url, stream=True, timeout=30) 
            if response.status_code != 200:
                console.log(f"Unexpected status code: {response.status_code}")
                time.sleep(1)  # Wait before retrying
                continue

            # 转换为 OpenCV 格式
            image_bytes = np.asaray(bytearray(response.content), dtype=np.uint8)
            frame = cv.imdecode(image_bytes, cv.IMREAD_COLOR)
            
            # 顛倒
            frame_flipped = cv.flip(frame, 0)
            # 调整图像大小
            frame_resized = cv.resize(frame_flipped, (640, 480))

            # 运行 YOLO 模型
            results = model(frame_resized, stream= False)

            # 显示带注释的结果
            annotated_frame = results[0].plot()  # 绘制带注释的帧
            cv.imshow("YOLO Image Stream", annotated_frame)

            # 检查退出条件
            if cv.waitKey(1) & 0xFF == ord('q'):
                break

            end_time = time.time()  # 获取当前时间

            # 计算循环运行时间
            execution_time = end_time - start_time
            queue.put(execution_time)  # 将执行时间放入队列

    finally:
        # 清理资源
        cv.destroyAllWindows()  # 关闭所有 OpenCV 窗口

# 实时绘制执行时间的过程
def plot_process(queue):
    execution_times = []  # 用于记录执行时间
    plt.ion()  # 启用交互模式
    fig, ax = plt.subplots()  # 创建图形和轴

    while True:
        # 检查队列中是否有新数据
        if not queue.empty():
            execution_time = queue.get()  # 从队列中获取执行时间
            execution_times.append(execution_time)

            # 更新折线图
            ax.clear()  # 清空图形
            ax.plot(range(len(execution_times)), execution_times)  # 绘制折线
            ax.set_xlabel("Number of loops")         
            ax.set_ylabel("Execution time (seconds)")
            ax.set_title("YOLO loop execution time")
            
            plt.pause(0.05)  # 暂停以更新图形

        time.sleep(0.1)  # 避免过度占用 CPU
        

if __name__ == "__main__":
    # 创建 YOLO 检测进程
    yolo_proc = mp.Process(target=yolo_process, args=(execution_times_queue,))

    # 创建绘图进程
    plot_proc = mp.Process(target=plot_process, args=(execution_times_queue,))

    # 启动进程
    yolo_proc.start()
    plot_proc.start()

    # 等待进程结束
    yolo_proc.join()
    plot_proc.join()