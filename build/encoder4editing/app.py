import sys

sc_path = "/StyleCLIP/global/"
sys.path.append(sc_path)
e4e_path = "/encoder4editing/"
sys.path.append(e4e_path)

from sc_main import StyleClipGenerator
from e4e_main import Encoder4editor
import os
import json
import requests
from PIL import Image
from s3 import UploadFile, RetrieveFile, LoadConfig
from io import BytesIO
from urllib import request as req

config = LoadConfig('./config.yaml')


class RememberAI:
    def __init__(
        self,
        image: str,
    ) -> None:
        imgBytes = req.urlopen(image).read()
        image = Image.open(BytesIO(imgBytes))

        self.e4e = Encoder4editor(exp_type="dog_encode", img_path=image, device="cuda")
        self.e4e.Inference()
        self.sc = StyleClipGenerator(
            device="cuda",
            dataset_name="afhqdog",
            e4e_weight_path="/encoder4editing/latents/latents.pt",
        )

    def Inference(self, text: str = None):
        target = {
            "wink": "wink",
            "cute": "cute",
            "sad": "so sad face",
            "happy": "smiling",
            "goldenFur": "golden fur",
            "whiteFur": "white fur",
            "blackFur": "black fur",
            "brownFur": "brown fur",
        }

        if "Fur" in text:
            hostNeutral = "face with fur"
            hostBeta = 0.12
            hostAlpha = 3.2

        elif "black" in text:
            hostNeutral = "face with fur"
            hostBeta = 0.09
            hostAlpha = 4.2

        else:
            hostNeutral = "face"
            hostBeta = 0.12
            hostAlpha = 1.3

        imagePath, imageName = self.sc.Inference(
            neutral=hostNeutral,
            target=target[text],
            beta=hostBeta,
            alpha=hostAlpha,
        )

        return imagePath, imageName


def ReturnMsg(status, msg, errType, data):
    returnMsg = {"Status": status, "Msg": msg, "Type": errType, "Data": data}
    return returnMsg


def predict():
    # TaskQueue 불러오기
    url = "http://devapi.petbridge.co.kr/api/remembrance/ai?done=0"
    response = requests.get(url).json()
    taskList = response['Data']['Result']['List']

    hostTexts = []
    containerIds = []
    for task in taskList:
        hostTexts.append(task['ac_text'])
        containerIds.append(task['rp_idx'])
    taskQueue = dict(zip(containerIds, hostTexts))

    failed = []
    done = []
    total = len(taskQueue)
    for containerId, hostText in taskQueue.items():
        objectName = RetrieveFile(containerId)[0]
        image = f"https://{config['bucketName']}.s3.{config['location']}.amazonaws.com/{objectName}"

        fileExt = image[image.rfind(".") :]
        exts = [".PNG", ".png", ".jpg", ".JPG", ".jpeg", ".JPEG"]
        texts = [
            "wink",
            "cute",
            "sad",
            "happy",
            "goldenFur",
            "whiteFur",
            "blackFur",
            "brownFur",
        ]

        rememberAi = RememberAI(image)

        if fileExt in exts:
            imagePath, imageName = rememberAi.Inference(text=hostText)
            imageUrl = UploadFile(imagePath, imageName, containerId)
            done.append(dict(rp_idx=containerId, msg=imageUrl))
        elif fileExt not in exts:
            failed.append(dict(rp_idx=containerId, msg=-1))
        else:
            failed.append(dict(rp_idx=containerId, msg="File format or file extension is not vaild"))

    data = dict(total=total, fail=failed, success=done)
    response = ReturnMsg(1, "Success", 1, data)
    result = dict(Result=response, flag='off')
    print(json.dumps(result, ensure_ascii=False, indent=4))

    lambdaUrl = "https://34ml67fwcb.execute-api.ap-northeast-2.amazonaws.com/aiStyleInstanceCon/instance"
    res = requests.post(lambdaUrl, json=result)
    print(res.text)


if __name__ == "__main__":
    predict()
