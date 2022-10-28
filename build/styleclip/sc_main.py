import tensorflow as tf
from dnnlib import tflib
import numpy as np
import torch
import clip
from PIL import Image
import pickle
import copy
from MapTS import GetFs, GetBoundary, GetDt
from manipulate import Manipulator
from typing import Optional
import datetime


class StyleClipGenerator:
    def __init__(
        self,
        device: Optional[str] = None,
        dataset_name: str = "afhqdog",
        e4e_weight_path: str = "../../encoder4editing/latents/latents.pt",
    ) -> None:
        if device is not "cpu":
            device = "cuda" if torch.cuda.is_available() else "cpu"
        self.device = device
        self.dataset_name = dataset_name
        self.e4e_weight_path = e4e_weight_path
        self.model, self.fs3, self.dlatent, self.M = self._LoadModel()
        self.M_ = self._Body()
        self.filename = self._makeName()

    def _LoadModel(self):

        model, preprocess = clip.load("ViT-B/32", device=self.device)
        fs3 = np.load("/StyleCLIP/global/npy/afhqdog/fs3.npy")
        np.set_printoptions(suppress=True)

        latents = torch.load(self.e4e_weight_path)
        w_plus = latents.cpu().detach().numpy()

        M = Manipulator(dataset_name=self.dataset_name)

        dlatents_loaded = M.W2S(w_plus)

        img_indexes = [0]
        M.num_images = len(img_indexes)

        dlatent_tmp = [tmp[img_indexes] for tmp in dlatents_loaded]
        return model, fs3, dlatent_tmp, M

    def _Body(self):
        M = self.M
        M.alpha = [0]
        M.manipulate_layers = [0]
        codes, out = M.EditOneC(0, self.dlatent)
        original = Image.fromarray(out[0, 0]).resize((512, 512))
        M.manipulate_layers = None
        return M

    def _makeName(self):
        baseName = "image"
        suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
        fileName = "_".join([baseName, suffix])

        return fileName

    def Inference(
        self,
        neutral="face",
        target="wink",
        beta=0.14,
        alpha=3.2,
    ) -> None:
        classnames = [target, neutral]
        dt = GetDt(classnames, self.model)
        self.M_.alpha = [alpha]
        boundary_tmp2, c = GetBoundary(self.fs3, dt, self.M_, threshold=beta)
        codes = self.M_.MSCode(self.dlatent, boundary_tmp2)
        out = self.M_.GenerateImg(codes)

        genImage = Image.fromarray(out[0, 0])
        baseDir = "/output/"
        imageName = f"{self.filename}.jpg"
        imagePath = os.path.join(baseDir, imageName)
        genImage.save(imagePath, 'JPEG')
        print(f"generated img ({genImage})")
        return imagePath, imageName
