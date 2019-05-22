Auto Change Waifu
===
Automatically download image from [yande.re](https://yande.re/), detect face, then set your waifu as Telegram profile photo.

## Installation
```bash
pip3 install -r requirements.txt
```
Download `lbpcascade_animeface.xml` from [lbpcascade_animeface](https://github.com/nagadomi/lbpcascade_animeface) for face detection.

## Config
Copy `config-example.py` to `config.py`.

To obtain API ID, please refer to [Creating your Telegram Application](https://core.telegram.org/api/obtaining_api_id).

## Run
```bash
python3 main.py
```
The first time you run you should be prompted with account login.
