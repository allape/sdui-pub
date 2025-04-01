import torch
from pipeline import build_audiosep, separate_audio

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = build_audiosep(
    config_yaml='config/audiosep_base.yaml',
    checkpoint_path='checkpoint/audiosep_base_4M_steps.ckpt',
    device=device
)

print(model)
