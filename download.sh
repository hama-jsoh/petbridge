wget --load-cookies ~/cookies.txt \
  "https://docs.google.com/uc?export=download&confirm=\
  $(wget --quiet --save-cookies ~/cookies.txt --keep-session-cookies --no-check-certificate \
  'https://docs.google.com/uc?export=download&id=1Kazha62DSt59RFkUpssUTWZJA5SImAxW' \
  -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1Kazha62DSt59RFkUpssUTWZJA5SImAxW" \
  -O copyfiles.zip \
  && rm -rf ~/cookies.txt

python3 petbridge/__about__.py

mv build/ docker/ \
  && unzip copyfiles.zip -d docker/build/ \
  && rm copyfiles.zip
