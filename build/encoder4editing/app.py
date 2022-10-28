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
from s3 import UploadFile2, RetrieveFile, LoadConfig
from io import BytesIO
from urllib import request as req
from tools import RequestQueue, LoadQueue, ChangeStatus, ParseQueue


def set_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cid", type=int, help="container_id")
    parser.add_argument("--htext", type=str, help="host_text")
    parser.add_argument("--total", type=int, help="task_queue_length")
    args = parser.parse_args()
    return args

config = LoadConfig('./config.yaml')
ARGS = set_argument()
CID = ARGS.cid
HTEXT = ARGS.htext
TOTAL = ARGS.total


class RememberAI:
    """
    Description:
        1. encoder4editing -> latents.pt
        2. styleclip -> image.jpg
    """
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
        """
        Description:
            styleclip 추론 함수
        """
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
    """
    Description:
        리턴 직렬화
    """
    returnMsg = {"Status": status, "Msg": msg, "Type": errType, "Data": data}
    return returnMsg


def predict(cid, text, total):
    """
    Description:
        전체 추론 (1 cycle)
    """
    failed = []
    done = []

    objectName = RetrieveFile(cid)[0]
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

    # encoder 모델 추론 -> latents.pt
    rememberAi = RememberAI(image)

    if fileExt in exts:
        # styleclip 모델 추론 -> generate image(jpg)
        imagePath, imageName = rememberAi.Inference(text=text)
        response = UploadFile2(imagePath, cid)
        if response == "SUCCEEDED":
            done.append(dict(rp_idx=cid, msg=response))
        else:
            failed.append(dict(rp_idx=cid, msg=response))
    elif fileExt not in exts:
        failed.append(dict(rp_idx=cid, msg=-1))
    else:
        failed.append(dict(rp_idx=cid, msg="File format or file extension is not vaild"))

    data = dict(total=total, fail=failed, success=done)
    response = ReturnMsg(1, "Success", 1, data)
    result = dict(Result=response, flag='off')
    print(json.dumps(result, ensure_ascii=False, indent=4))

    # 최종결과 람다에 전달(flag=off 포함)
    ChangeStatus(result)


if __name__ == "__main__":
    predict(CID, HTEXT, TOTAL)
