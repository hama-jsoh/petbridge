# petbridge
펫브릿지 with AWS
#
## 1. pre-requisite
아래 커맨드로 `copyfiles.zip`을 다운로드 받고 `docker/build/` 폴더 아래에 압축을 푼다.  

download `copyfiles.zip`
```bash
wget --load-cookies ~/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies ~/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1Kazha62DSt59RFkUpssUTWZJA5SImAxW' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1Kazha62DSt59RFkUpssUTWZJA5SImAxW" -O copyfiles.zip && rm -rf ~/cookies.txt
```

set folder structure
```bash
git clone https://github.com/hama-jsoh/petbridge.git

mv build/ petbridge/docker/
mv copyfiles.zip petbridge/docker/build/ && unzip copyfiles.zip && rm copyfiles.zip
```

## 2. build
```bash
cd petbridge/docker
docker-compose -f docker-compose-build.yaml up -d
```

## 3. Run service
```bash
cd petbridge/docker
docker-compose up -d
```
