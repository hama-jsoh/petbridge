from argparse import Namespace
from time import time
from typing import Optional
import os
import sys
import numpy as np
from PIL import Image
import torch
import torchvision.transforms as transforms

sys.path.append(".")
sys.path.append("..")

from utils.common import tensor2im
from models.psp import pSp


class Encoder4editor:
    def __init__(
        self,
        exp_type: str,
        img_path: str,
        device: Optional[str] = None,
    ) -> None:
        self.exp_type = exp_type
        self.img_path = img_path
        self.device = device
        self.exp_args = self._Config()
        self.net = self._LoadModel()
        self.transformed_img = self._TransformImg()

    def _LoadModel(self):
        checkPoint = torch.load(self.exp_args['model_path'], map_location="cpu")
        opts = checkPoint["opts"]
        opts["checkpoint_path"] = self.exp_args['model_path']
        opts = Namespace(**opts)
        net = pSp(opts)
        net.eval
        net.cuda()
        print(f"Model successfully loaded!")
        return net

    def _Config(self):
        expDataArgs = {
            "dog_encode": {
                "model_path": "pretrained_models/e4e_dog_encode.pt",
                "image_path": self.img_path,
            }
        }
        expArgs = expDataArgs[self.exp_type]
        expArgs["transform"] = transforms.Compose(
            [
                transforms.Resize((256, 256)),
                transforms.ToTensor(),
                transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5]),
            ]
        )
        modelPath = expArgs["model_path"]
        return expArgs

    def _TransformImg(self):
        # convert RGB
        imgPath = self.exp_args["image_path"]
        origImg = imgPath
        origImg = origImg.convert("RGB")

        # resize Img
        resizeDims = (256, 256)
        origImg.resize(resizeDims)

        # transform Img
        imgTransforms = self.exp_args['transform']
        transFormedImg = imgTransforms(origImg)
        return transFormedImg

    def _RunOnBatch(self, inputs, net):
        _, latents = self.net(inputs.to('cuda').float(), randomize_noise=False, return_latents=True)
        return latents

    def Inference(self):
        with torch.no_grad():
            latents = self._RunOnBatch(self.transformed_img.unsqueeze(0), self.net)
            print("Inference success!")
            torch.save(latents, '/encoder4editing/latents/latents.pt')
            print("Saved latents.pt!")
