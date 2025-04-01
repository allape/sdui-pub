import http.server
import io
import json
import socketserver
import torch
from pipeline import build_audiosep, separate_audio
from urllib.parse import parse_qs

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = build_audiosep(
    config_yaml='config/audiosep_base.yaml',
    checkpoint_path='checkpoint/audiosep_base_4M_steps.ckpt',
    device=device)

output_file = 'output.wav'


class CustomHandler(http.server.BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        # Handle preflight requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'PUT,OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type,Content-Length')
        self.end_headers()

    def do_PUT(self):
        content_length = int(self.headers['Content-Length'])
        post_body = self.rfile.read(content_length)
        audio_file = io.BytesIO(post_body)

        qs = parse_qs(self.path[2:])
        text = qs.get('text', [None])[0]

        if text is None:
            self.send_response(400)
            self.send_header("Content-type", "plain/text; charset=utf-8")
            self.end_headers()
            self.wfile.write(b'Missing text parameter.')
            return

        separate_audio(model, audio_file, text, output_file, device, use_chunk=True)

        # read the output file
        with open(output_file, 'rb') as f:
            audio_data = f.read()
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header("Content-Type", "audio/wav")
        self.send_header("Content-Length", str(len(audio_data)))
        self.end_headers()
        self.wfile.write(audio_data)


PORT = 9090

with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
