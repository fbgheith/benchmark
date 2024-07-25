from torchbenchmark.util.framework.diffusers import install_diffusers
import torch
import os
import warnings

MODEL_NAME = "timbrooks/instruct-pix2pix"

def load_model_checkpoint():
    from diffusers import StableDiffusionInstructPix2PixPipeline

    StableDiffusionInstructPix2PixPipeline.from_pretrained(MODEL_NAME, torch_dtype=torch.float16, safety_checker=None)

if __name__ == '__main__':
    install_diffusers()
    if not "HUGGING_FACE_HUB_TOKEN" in os.environ:
        warnings.warn(
            "Make sure to set `HUGGINGFACE_HUB_TOKEN` so you can download weights"
        )
    else:
        load_model_checkpoint()