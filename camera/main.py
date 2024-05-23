import click



# rich
from rich import pretty
from rich import print,print_json
from rich.console import Console
import click

from src.new_camera import *
from ultralytics import YOLO



pretty.install()
console = Console()





@click.command()
@click.option('--use_device', default=0, help='Device to use.')
@click.option('--ip', default='0.0.0.0', help='IP address to bind.')
@click.option('--port', default=8000, help='Port to bind.', type=int)
def main(use_device, ip, port):
    # For example, you might want to call a function like run_camera(use_device, ip, port)
    
    # model = YOLO("yolov8n.pt")

    # Export the model to CoreML format
    # model.export(format="coreml")  # creates 'yolov8n.mlpackage'

    # Load the exported CoreML model

    # Run inference
    # results = coreml_model("https://ultralytics.com/images/bus.jpg")

    coreml_model = YOLO("yolov8n.mlpackage")

    rtsp_url = "rtsp://172.20.10.2:554"
    
    conf = {
            "FRAME_MAX_COUNT": 12,
            "FPS": 30
            }
    # read_and_display_rtsp(rtsp_url)
    yolo_process(coreml_model,rtsp_url,conf)



if __name__ == '__main__':
    main()
