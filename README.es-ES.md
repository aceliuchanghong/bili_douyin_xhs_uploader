

# bili_douyin_xhs_uploader

Cargador para plataformas de video chinas, diseñado para la carga por lotes de videos.

### Ejemplo
![example_video_windows.gif](log%2Fexample_video_windows.gif)

### Instalación
```
#pip list --format=freeze > requirements.txt
git clone https://github.com/aceliuchanghong/bili_douyin_xhs_uploader.git
conda create -n uploader python=3.9
conda activate uploader
pip install -r requirements.txt --proxy=127.0.0.1:10809
```
Coloca las cookies de los sitios web correspondientes en `cookies/bili_cookies.json`, `cookies/xhs_cookies.json`, `cookies/douyin_cookies.json`, o modifica la ruta dentro de `core/config.py`.

### Estructura del proyecto

```
bili_douyin_xhs_uploader/
|
├── LICENSE
├── README.md
├── gpt_prompt.md
├── main.py
├── requirements.txt
├── test.py
├── cookies/
├── core/
│   ├── config.py
│   ├── exceptions.py
│   ├── upload.py
│   └── video_info.py
├── files/
├── log/
│   ├── ftp_log.md
│   └── media_uploader.db
├── platforms/
│   ├── bili/
│   │   └── uploader.py
│   ├── douyin/
│   │   └── uploader.py
│   └── xhs/
│       └── uploader.py
└── utils/
    └── util_sqlite.py
```

### Uso

```shell
# Verifica si ya existe en la base de datos; si existe, no se carga
# ej:
cd bili_douyin_xhs_uploader
python main.py --platforms "xhs" --video_url "https://test" --video_path "files/test/11.mp4" --video_name "我只在乎你鄧麗君" --description "我只在乎你鄧麗君 琵琶 演奏"

python main.py --platforms "douyin" --video_url "https://test" --video_path "files/test/11.mp4" --video_name "我只在乎你鄧麗君" --description "我只在乎你鄧麗君 琵琶 演奏"
python main.py --platforms "douyin" --video_url "https://test2" --video_path "files/test/00.mp4" --video_name "你的身边有我们 你的背后是祖国" --description "你的身边有我们 你的背后是祖国"

python main.py --platforms "bili" --video_url "https://test" --video_path "files/test/11.mp4" --video_name "我只在乎你鄧麗君" --description "我只在乎你鄧麗君 琵琶 演奏"

python main.py --platforms "toutiao" --video_url "https://test2" --video_path "files/test/burn-tool.mp4" --video_name "你的身边有我们 你的背后是祖国" --cover_path "files/test/01.jpg" --description "你的身边有我们 你的背后是祖国"
```
### Ubuntu
```shell
python main.py --platforms "douyin" --video_url "https://test_ubuntu" --video_path "/home/aceliuchanghong/ftpfiles/liu/00.mp4" --video_name "你的身边有我们 你的背后是祖国" --description "你的身边有我们 你的背后是祖国" --headless
python main.py --platforms "xhs" --video_url "https://test2" --video_path "files/test/00.mp4" --video_name "你的身边有我们 你的背后是祖国" --description "你的身边有我们 你的背后是祖国" --headless
```
### Preguntas y respuestas
```errorinfo
Q1:
2024-01-15 04:52:53,590 - DouyinUploader - INFO - Uploading video '你的身边有我们 你的背后是祖国' to douyin...
An error occurred during the upload: 'utf-8' codec can't decode byte 0xb4 in position 41121: invalid start byte
A1:
El error indica un problema con la codificación del archivo. Modifícalo al formato UTF-8 para solucionarlo.

Q2:
2024-01-15 05:02:47,844 - DouyinUploader - INFO - douyin:登陆中
An error occurred during the upload: Target page, context or browser has been closed
Browser logs:
╔════════════════════════════════════════════════════════════════════════════════════════════════╗
║ Looks like you launched a headed browser without having a XServer running.                     ║
║ Set either 'headless: true' or use 'xvfb-run <your-playwright-app>' before running Playwright. ║
║                                                                                                ║
║ <3 Playwright Team                                                                             ║
╚════════════════════════════════════════════════════════════════════════════════════════════════╝
A2:
--headless

```
