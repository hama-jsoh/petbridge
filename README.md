# petbridge

<p align="right"> <img src="https://komarev.com/ghpvc/?username=hama-jsoh&color=brightgreen" alt="hama-jsoh" /> </p>

----

<p align="center">
  <b> 펫브릿지 with AWS </b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-0.0.4-orange?style=flat-square">
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
  
## 1. Git clone repo & setup folder structure
```bash
git clone https://github.com/hama-jsoh/petbridge.git && cd petbridge && bash download.sh
```
    
### 1-1. Folder structure
```bash
build/
├── copyfiles
│   ├── afhqdog
│   │   ├── fs3.npy
│   │   ├── S
│   │   ├── S_mean_std
│   │   └── W.npy
│   ├── model
│   │   └── afhqdog.pkl
│   └── pretrained_models
│       └── e4e_dog_encode.pt
├── encoder4editing
│   ├── app.py
│   ├── config.yaml
│   ├── e4e_main.py
│   ├── queue_loader.py
│   ├── s3.py
│   └── tools.py
└── styleclip
    ├── manipulate.py
    └── sc_main.py
```
  
### 1-2. Modify config.yaml
- awsAccessKey : "Enter your aws_access_key_id"
- awsSecretKey : "Enter your aws_access_secret_key"

## 2. Build (dev server)
```bash
cd docker \
 && docker-compose -f docker-compose-build.yaml up -d
```

## 3. Run service (service server)
```bash
docker-compose up -d
```

----

## Hotfix
```bash
python3 queue_loader.py
```
