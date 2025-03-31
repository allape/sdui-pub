from pipeline import build_audiosep, separate_audio
import torch

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = build_audiosep(
    config_yaml='config/audiosep_base.yaml',
    checkpoint_path='checkpoint/audiosep_base_4M_steps.ckpt',
    device=device)

audio_file = 'test.wav'
text = 'vocal'
output_file='vocal.wav'

separate_audio(model, audio_file, text, output_file, device, use_chunk=True)
