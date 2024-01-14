class VideoInfo:
    def __init__(self):
        self.video_name = None  # 文件名字
        self.download_date = None  # 日期
        self.video_url = None  # 链接地址
        self.video_path = None  # 本地路径
        self.remark1 = None  # 结果路径
        self.describe = None  # 备注

    def __str__(self):
        attrs = ['video_name', 'download_date', 'video_url', 'video_path', 'remark1', 'describe']
        return '\n' + '\n'.join(f'{attr}="{getattr(self, attr)}"' for attr in attrs)

    def to_clazz(self):
        attrs = ['video_name', 'download_date', 'video_url', 'video_path', 'remark1', 'describe']
        return '\n' + '\n'.join(f'videoresult.{attr} = "{getattr(self, attr)}"' for attr in attrs)
