# petbridge
펫브릿지 with AWS
#
## 1. pre-requisite
아래 링크에서 `copyfiles.zip`을 다운로드 받고 `docker/build/` 폴더 아래에 압축을 풀어주세요.  
Download Link : [Google_Drive](https://drive.google.com/file/d/1Kazha62DSt59RFkUpssUTWZJA5SImAxW/view?usp=sharing)  
```bash
git clone https://github.com/hama-jsoh/petbridge.git
mv build/ petbridge/docker/
mv copyfiles.zip petbridge/docker/build/ && unzip copyfiles.zip
```

## 2. build
```bash
cd docker
docker-compose -f docker-compose-build.yaml up -d
```

## 3. Run service
```bash
cd docker
docker-compose up -d
```
