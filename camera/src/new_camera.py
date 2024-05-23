import cv2 as cv
import time
import multiprocessing as mp
from rich.console import Console


console = Console()

__all__ = ['yolo_process']



def capture_frames(rtsp_url, queue, frame_count, conf:dict):
    capture = cv.VideoCapture(rtsp_url)
    capture.set(cv.CAP_PROP_BUFFERSIZE, 1)
    capture.set(cv.CAP_PROP_FPS, conf['FPS'])
    
    if not capture.isOpened():
        print("Failed to open RTSP stream.")
        return

    try:
        while True:
            res, frame = capture.read()
            if not res:
                break

            if frame_count.value >= conf.get("FRAME_MAX_COUNT"):
                try:
                    queue.get_nowait()  # Discard the oldest frame if queue is full
                    with frame_count.get_lock():
                        frame_count.value -= 1
                except:
                    pass

            queue.put(frame)
            with frame_count.get_lock():
                frame_count.value += 1

            if cv.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        capture.release()

def process_frames(model, queue, frame_count):
    # Export the model to CoreML format
        # model.export(format="coreml")  # creates 'yolov8n.mlpackage'

# Load the exported CoreML model
        # coreml_model = YOLO("yolov8n.mlpackage")

# Run inference
# results = coreml_model("https://ultralytics.com/images/bus.jpg")
    try:
        while True:
            if not queue.empty():
                frame = queue.get()
                with frame_count.get_lock():
                    frame_count.value -= 1

                start_time = time.time()

                # Run YOLO detection
                # results = model(frame, stream=False, device="mps")
                results = model(frame)

                # Draw annotated results
                annotated_frame = results[0].plot()

                # Display the frame
                cv.imshow("YOLO Image Stream", annotated_frame)

                # Calculate loop execution time
                end_time = time.time()
                execution_time = end_time - start_time
                
                print(f"Execution time: {execution_time:.2f} seconds")

                if cv.waitKey(1) & 0xFF == ord('q'):
                    break
    finally:
        cv.destroyAllWindows()

def yolo_process(model, rtsp_url,conf: dict):
    """_summary_

    Args:
        model (_type_): _description_
        rtsp_url (_type_): _description_
        conf (dict): _description_
    """
    # Create a queue for sending data between processes
    queue = mp.Queue()
    frame_count = mp.Value('i', 0)  # Shared counter for frame count

    # Create the processes
    capture_process = mp.Process(target=capture_frames, args=(rtsp_url, queue, frame_count,conf))
    process_process = mp.Process(target=process_frames, args=(model, queue, frame_count))

    # Start the processes
    capture_process.start()
    process_process.start()

    # Wait for the processes to finish
    capture_process.join()
    process_process.join() 