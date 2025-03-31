# docker run --rm -it -p 8080:8080 -v "$(pwd)/predictor.py:/ultralytics/predictor.py" ultralytics/ultralytics:8.3.75-arm64 bash
# python predictor.py

import http.server
import io
import json
import numpy as np
import socketserver
import torch
import torch.nn.functional as F
from PIL import Image
from ultralytics import YOLO

model = YOLO("yolo11n.pt")


# model("./bus.jpg") # hot start

def image_binary_to_bchw_tensor(image_binary):
    image = Image.open(io.BytesIO(image_binary))
    np_array = np.array(image)
    tensor = torch.from_numpy(np_array).float()

    if len(tensor.shape) == 2:  # Grayscale image
        tensor = tensor.unsqueeze(0).unsqueeze(0)
    else:
        if tensor.shape[2] == 4:  # RGBA image
            tensor = tensor[:, :, :3]
        tensor = tensor.permute(2, 0, 1).unsqueeze(0)

    _, _, h, w = tensor.shape
    pad_h = (32 - h % 32) % 32
    pad_w = (32 - w % 32) % 32
    tensor = F.pad(tensor, (0, pad_w, 0, pad_h), mode='constant', value=0)

    return tensor


class CustomHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_body = self.rfile.read(content_length)

        tensor = image_binary_to_bchw_tensor(post_body)
        res = model(tensor)[0]

        boxes = []
        prediction = res.boxes
        for index in range(len(prediction.cls)):
            cls = prediction.cls[index]
            confidence = prediction.conf[index]
            xywh = prediction.xywh[index]
            boxes.append({
                "label": str(int(cls.item())),
                "confidence": confidence.item(),
                "x": xywh[0].item(),
                "y": xywh[1].item(),
                "width": xywh[2].item(),
                "height": xywh[3].item()
            })

        self.send_response(200)
        self.send_header("Content-type", "application/json; charset=utf-8")
        self.end_headers()

        self.wfile.write(json.dumps({
            "classes": res.names,
            "boxes": boxes
        }).encode("utf-8"))


PORT = 8080

with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
