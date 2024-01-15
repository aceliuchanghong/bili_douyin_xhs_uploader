对于项目bili_douyin_xhs_uploader,core/upload.py是一个上传视频到网站的抽象类,platform是各平台,里面uploader继承自upload,
读取cookies目录下对应平台的cookie文件然后使用playwright上传文件,以下是自己的项目结构,其中不重要的文件已省略,
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
core/exceptions.py
```python
class UploadError(Exception):
    """Base class for exceptions in this module."""
    pass
class LoginError(UploadError):
    """Raised when login to the platform fails."""
    pass
class VideoUploadError(UploadError):
    """Raised when the video upload fails."""
    pass
```
core/upload.py
```python
import abc
from core import config
import logging
class Upload(abc.ABC):
    def __init__(self):
        self.logger = self._setup_logger()
    def _setup_logger(self):
        logger = logging.getLogger(self.__class__.__name__)
        # 可以根据需要配置日志记录器，比如设置日志级别、格式和输出位置
        logger.setLevel(config.LOG_LEVEL)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger
    @abc.abstractmethod
    def upload_video(self, *args, **kwargs):
        pass
```
main.py

```python
import argparse
from platforms.bili.uploader import BiliUploader
from platforms.douyin.uploader import DouyinUploader
from platforms.xhs.uploader import XhsUploader

UPLOADERS = {
    'bili': BiliUploader,
    'douyin': DouyinUploader,
    'xhs': XhsUploader
}


def main(platform_name, video_path, title, description):
    if platform_name not in UPLOADERS:
        print(f"Unsupported platform: {platform_name}")
        return
    uploader_class = UPLOADERS[platform_name]
    try:
        uploader_class.upload_video(video_path, title, description)
        print(f"Video uploaded successfully to {platform_name}.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload videos to various platforms.")
    parser.add_argument('--platform', required=True,
                        help="The platform to upload the video to (e.g., 'bili', 'douyin', 'xhs').")
    parser.add_argument('--video', required=True, help="Path to the video file.")
    parser.add_argument('--title', required=True, help="Title of the video.")
    parser.add_argument('--description', required=False, default="", help="Description of the video.")
    args = parser.parse_args()
    main(args.platform, args.video, args.title, args.description)
```
core/video_info.py
```python
class VideoInfo:
    def __init__(self):
        self.video_name = None  # 文件名字
        self.download_date = None  # 日期
        self.video_url = None  # 链接地址
        self.video_path = None  # 本地路径
        self.remark1 = None  # 结果路径
        self.describe = None  # 备注
```
基于以上帮我解决以下问题
