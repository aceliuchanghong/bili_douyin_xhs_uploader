from platforms.douyin.uploader import DouyinUploader
from platforms.xhs.uploader import XhsUploader
from platforms.bili.uploader import BiliUploader
import asyncio


# 假设你的XhsUploader类定义是正确的，并且upload_video是一个异步方法

async def main():
    # xhs = XhsUploader()
    # await xhs.upload_video("https://00.mp4", "../files/test/00.mp4", "00", "20240114", [], "测试")
    bili = BiliUploader()
    await bili.upload_video("https://00.mp4", "../files/test/00.mp4", "00", "20240114", [], "测试")
    # douyin = DouyinUploader()
    # await douyin.upload_video("https://00.mp4", "../files/test/00.mp4", "00", "20240114", [], "测试")


if __name__ == "__main__":
    # 运行主函数
    asyncio.run(main())
