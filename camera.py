import json
import threading
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
# exit_event = threading.Event()
SCAL =  3
pix = (640, 480)
DELAY = 5
model = YOLO('yolov8s.pt')  # 确保路径正确

image_url = "http://192.168.232.185/capture"  # 确保 URL 是正确的

# # 初始化摄像头
# cap = cv.VideoCapture(0)  # 0 表示第一个摄像头
# if not cap.isOpened():
#     raise Exception("无法打开摄像头")



def check_server(url):
    try:
        # Send a simple GET request to the server
        response = requests.get(url, timeout=15)  # Set a timeout to avoid waiting too long
        
        # Check the response status code
        if response.status_code == 200:
            # The server is reachable and returned a success status
            return True
        else:
            # The server returned a non-success status code
            return False

    except requests.Timeout:
        # The request timed out
        raise Exception("The server request timed out. Please check the server status and network connection.")

    except requests.RequestException as e:
        # Any other request-related exception
        raise Exception(f"An error occurred while checking the server: {str(e)}")



def send_message_to_django(queue):
    while True:
        # Check if there's data in the queue
        if not queue.empty():
            dict_data = queue.get()  # Get data from the queue
            
            
            # The URL to post data to
            api_url = "http://49.213.238.75:8000/app/"
            # api_url = "http://127.0.0.1:8000/app/"
            headers = {"Content-Type": "application/json"}  # Set the correct Content-Type

            # Send the data to Django
            response = requests.post(api_url, data=dict_data)  # Use JSON data
            
            
            # Log the status code
            # console.log(f"Sent data to Django, status code -> {response.status_code}")

        time.sleep(0.05)  # Wait before checking the queue again


def process_result(results, queue):
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
    # top_two = class_probabilities_sorted[]

    # 创建一个字典来存储结果，包括 'person' 的数量
    result_dict = {"top_objects": []}

    # 添加前两个物体及其置信度
    for obj, prob in class_probabilities_sorted:
        result_dict["top_objects"].append({"object": obj, "confidence": prob})

    # 添加 'person' 的计数到结果字典
    result_dict["people_count"] = people_count
    
    # console.log(f"people_count -> {people_count}")
    

    queue.put(result_dict)
    
    # delay execution
    
    if people_count > 2:
        time.sleep(DELAY)
        


def yolo_process():
    # Create a queue for sending data to Django
    queue = mp.Queue()

    # Start the process for sending data
    django_sender = mp.Process(target=send_message_to_django, args=(queue,))
    django_sender.start()
    
    try:
        while True:
            start_time = time.time()

            # Fetch image from the specified URL
            response = requests.get(image_url, stream=True, timeout=30) 
            
            if response.status_code != 200:
                print(f"Unexpected status code -> {response.status_code}")
                time.sleep(1)  # Wait before retrying
                continue

            # Convert to OpenCV format
            image_bytes = np.asarray(bytearray(response.content), dtype=np.uint8)
           
            frame = cv.imdecode(image_bytes, cv.IMREAD_COLOR)

            # Resize the frame
            frame_resized = cv.resize(frame, pix)  # Adjust size as needed

            # Run YOLO detection
            results = model(frame_resized, stream=False, device = "mps")

            # Draw annotated results
            annotated_frame = results[0].plot()

            # Flip vertically (optional)
            # flipped_frame = cv.flip(annotated_frame, 0)  # Check this operation for errors

            # Resize for display (three times larger)
            display_frame = cv.resize(annotated_frame, (pix[0] * SCAL, pix[1] * SCAL))  # Ensure resizing works

            # Display the frame
            cv.imshow("YOLO Image Stream", display_frame)


            # Calculate loop execution time
            end_time = time.time()
            execution_time = end_time - start_time
            
            print(f"Execution time: {execution_time:.2f} seconds")

            # Process results and send to Django via the queue
            process_result(results, queue)
            
            
            if cv.waitKey(1) & 0xFF == ord('q'):  # Ensure this condition doesn't cause early exit
                break
    

    finally:
        cv.destroyAllWindows()  # Close OpenCV windows
        django_sender.terminate()  # Terminate the Django sender process

        

if __name__ == "__main__":
    try:
        server_is_reachable = check_server(image_url)
        
        if server_is_reachable:
            print("The server is reachable.")
        else:
            print("The server is not reachable. Please check the URL or the server status.")

    except Exception as e:
        print(f"Error: {e}")
    
    yolo_process()
