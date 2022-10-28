# petbridge

<p align="right"> <img src="https://komarev.com/ghpvc/?username=hama-jsoh&color=brightgreen" alt="hama-jsoh" /> </p>

----

<p align="center">
  <b> 펫브릿지 with AWS </b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-0.0.1-orange?style=flat-square">
  <img src="https://img.shields.io/badge/Python-3.6.x-3776AB?style=flat-square&logo=Python&logoColor=white">
  <img src="https://img.shields.io/badge/CUDA-11.2.0-76B900?style=flat-square&logo=NVIDIA&logoColor=white">
  <img src="https://img.shields.io/badge/CUDNN-8-76B900?style=flat-square&logo=NVIDIA&logoColor=white">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/AWS-Lambda-FF9900?style=flat-square&logo=AWS-Lambda&logoColor=white">
  <img src="https://img.shields.io/badge/Amazon-EC2-FF9900?style=flat-square&logo=Amazon-EC2&logoColor=white">
  <img src="https://img.shields.io/badge/Amazon-RDS-527FFF?style=flat-square&logo=Amazon-RDS&logoColor=white">
  <img src="https://img.shields.io/badge/Amazon-S3-569A31?style=flat-square&logo=Amazon-S3&logoColor=white">
  
  <img src="https://img.shields.io/badge/Amazon-CloudWatch-FF4F8B?style=flat-square&logo=Amazon-CloudWatch&logoColor=white">
  <img src="https://img.shields.io/badge/Amazon-API_Gateway-A100FF?style=flat-square&logo=Amazon-API-Gateway&logoColor=white">
</p>

----

## 1. pre-requisite
아래 커맨드로 `copyfiles.zip`을 다운로드 받고 `docker/build/` 폴더 아래에 압축을 푼다.  

### 1-1. git clone repository
```bash
git clone https://github.com/hama-jsoh/petbridge.git
```

### 1-2. download copyfiles.zip
```bash
wget --load-cookies ~/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies ~/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1Kazha62DSt59RFkUpssUTWZJA5SImAxW' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1Kazha62DSt59RFkUpssUTWZJA5SImAxW" -O copyfiles.zip && rm -rf ~/cookies.txt
```

### 1-3. set folder structure
```bash
mv petbridge/build/ petbridge/docker/ \
 && mv copyfiles.zip petbridge/docker/build/ \
 && unzip petbridge/docker/build/copyfiles.zip \
 && rm petbridge/docker/build/copyfiles.zip
```

## 2. build (dev server)
```bash
cd petbridge/docker \
 && docker-compose -f docker-compose-build.yaml up -d
```

## 3. Run service (service server)
```bash
docker-compose up -d
```

----

## 임시
```bash
python3 queue_loader.py
```
