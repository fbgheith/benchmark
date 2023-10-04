"""
HuggingFace Stable Diffusion model.
It requires users to specify "HUGGINGFACE_AUTH_TOKEN" in environment variable
to authorize login and agree HuggingFace terms and conditions.
"""
from torch import nn
from torchbenchmark.tasks import COMPUTER_VISION
from torchbenchmark.util.model import BenchmarkModel
from torchbenchmark.util.framework.huggingface.model_factory import HuggingFaceAuthMixin

import torch
from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler

class SDPipelineWrapper(nn.Module):
    def __init__(self, pipe):
        super().__init__()
        self.pipe = pipe

    def forward(self, x):
        return self.pipe(x)

class Model(BenchmarkModel, HuggingFaceAuthMixin):
    task = COMPUTER_VISION.GENERATION

    DEFAULT_TRAIN_BSIZE = 1
    DEFAULT_EVAL_BSIZE = 1
    ALLOW_CUSTOMIZE_BSIZE = False
    # Skip deepcopy because it will oom on A100 40GB
    DEEPCOPY = False
    # Default eval precision on CUDA device is fp16
    DEFAULT_EVAL_CUDA_PRECISION = "fp16"

    def __init__(self, test, device, batch_size=None, extra_args=[]):
        HuggingFaceAuthMixin.__init__(self)
        super().__init__(test=test, device=device,
                         batch_size=batch_size, extra_args=extra_args)
        model_id = "stabilityai/stable-diffusion-2"
        scheduler = EulerDiscreteScheduler.from_pretrained(model_id, subfolder="scheduler")
        pipe = StableDiffusionPipeline.from_pretrained(model_id, scheduler=scheduler)
        self.model = SDPipelineWrapper(pipe).to(self.device)
        self.example_inputs = "a photo of an astronaut riding a horse on mars"

    def enable_fp16(self):
        # This model uses fp16 by default
        # Make this function no-op.
        pass

    def get_module(self):
        return self.model, self.example_inputs

    def set_module(self, module):
        self.model = module

    def train(self):
        raise NotImplementedError("Train test is not implemented for the stable diffusion model.")

    def eval(self):
        images = self.model(self.example_inputs)
        return (images, )