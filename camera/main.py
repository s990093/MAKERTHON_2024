

from camera.src.camera import check_server, yolo_process

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

image_url = "http://192.168.232.185/capture"  

if __name__ == "__main__":
    yolo_process()
