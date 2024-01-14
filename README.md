# bili_douyin_xhs_uploader
国内视频网站的uploader,用来批量上传视频

### install
#pip list --format=freeze > requirements.txt
conda create -n uploader python=3.9

conda activate worker

pip install -r requirements.txt --proxy=127.0.0.1:10809
