import boto3
import json, yaml
import logging
import warnings
import requests

warnings.filterwarnings(action='ignore')


def ReturnMsg(status, msg, errType, data):
    returnMsg = {"Status": status, "Msg": msg, "Type": errType, "Data": data}

# 설정파일 불러오기
def LoadConfig(path: str) -> dict:
    """
    input: yaml
    output: json
    """
    filename = path.split(".")
    ext = filename[-1]
    if ext == "yaml":
        with open(path, encoding="utf-8") as y:
            config = yaml.safe_load(y)
            return config
    else:
        with open(path, "r") as j:
            config = json.load(j)
            return config

# S3 리소스 조회
def RetrieveFile(container_id: str = '11'):
    config = LoadConfig("./config.yaml")

    s3Resource = boto3.resource(
        service_name='s3',
        aws_access_key_id=config["awsAccessKey"],
        aws_secret_access_key=config["awsSecretKey"],
        region_name=config['location'],
    )

    prefix = f"{config['inputFirstDir']}/{container_id}/"
    bucket = s3Resource.Bucket(name=config['bucketName'])

    try:
        fileList = []
        for obj in bucket.objects.filter(Prefix=prefix):
            idx = obj.key.rfind('/')
            if obj.key[:idx+1] == prefix and obj.key != prefix:
                fileList.append(obj.key)
        return fileList
    except Exception as e:
        print(e)
        return False

# S3 파일 업로드 및 url 가져오기
def UploadFile1(imagePath: str, imageName: str, containerId: str) -> str:
    config = LoadConfig("./config.yaml")
    objectName = "{}/{}/{}".format(config['outputFirstDir'], containerId, imageName)
    bucketName = config["bucketName"]

    s3Client = boto3.client(
        service_name="s3",
        aws_access_key_id=config["awsAccessKey"],
        aws_secret_access_key=config["awsSecretKey"],
    )

    s3Client.put_object(
        Bucket=config['bucketName'], Key=(config['outputFirstDir'] + "/" + str(containerId) + "/")
    )

    try:
        s3Client.upload_file(imagePath, config['bucketName'], objectName)
    except Exception as e:
        print(e)
        return False

    imageUrl = f"https://{config['bucketName']}.s3.{config['location']}.amazonaws.com/{objectName}"
    return imageUrl

# API Call S3 파일 업로드 & DB 등록
def UploadFile2(imagePath: str, containerId: str):
    config = LoadConfig("./config.yaml")
    data = {"a_container_id": containerId, "a_container_type": config['outputFirstDir']}
    file = {"files": open(imagePath, 'rb')}
    url = "http://devapi.petbridge.co.kr/api/file"
    try:
        res = requests.post(url, files=file, data=data).json()
        response = res['ResultCode']
        return response
    except Exception as e:
        print(e)
        return False
