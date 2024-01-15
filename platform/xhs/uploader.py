import asyncio
import json
from playwright.async_api import async_playwright
import random
from core import config
from core.upload import Upload
from core.exceptions import VideoUploadError
from utils.util_sqlite import excute_sqlite_sql
from datetime import datetime


class XhsUploader(Upload):
    """
    开始上传,包括以下几个部分:
    1.作品名称 2.作品简介 3.添加话题 4.选择合集
    若是上传成功之后,将数据写入sqlite数据库,没成功就不写入
    """
    platform = "xhs"

    async def upload_video(self, video_url, video_path, video_name, description=None, topics=None, collection=None):
        if topics is None:
            topics = []
        topics = topics + config.keywords
        try:
            self.logger.info(f"Uploading video '{video_name}' to {self.platform}...")
            # cookie 加载
            with open(config.xhs_config["cookie_path"], 'r') as file:
                storage_state = json.load(file)
            async with (async_playwright() as playwright):
                # 登录
                self.logger.info(self.platform + ":登陆中")
                browser = await playwright.chromium.launch(headless=False)
                context = await browser.new_context(storage_state=storage_state)
                page = await context.new_page()

                await page.goto(config.xhs_config["up_site"])
                await page.wait_for_url(config.xhs_config["up_site"])
                self.logger.info(self.platform + ":登陆成功")
                # 视频上传
                self.logger.info(self.platform + ":视频上传中")
                # 点击上传按钮
                file_input_locator = page.locator('//*[@id="publish-container"]/div/div[2]/div[1]/div/input')
                await file_input_locator.wait_for(state="visible")
                await file_input_locator.set_input_files([video_path])
                self.logger.info(self.platform + ":视频上传完毕")
                # 填写作品名称 简介 话题
                self.logger.info(self.platform + ":设置标题")
                up_title = video_name + "|" + random.choice(config.key_sentence)
                await page.locator('//*[@id="publish-container"]/div/div[3]/div[2]/div[3]/input').fill(up_title)
                self.logger.info(self.platform + ":设置简介")
                await page.locator('//*[@id="post-textarea"]').fill(description)
                self.logger.info(self.platform + ":添加话题")
                css_selector = ".topic-container"
                await page.press(css_selector, "Enter")
                for topic in topics:
                    await page.locator('//*[@id="topicBtn"]/span').click()
                    await page.locator('//*[@id="post-textarea"]').type(topic)
                    await asyncio.sleep(1.3)
                    await page.press(css_selector, "Enter")
                # 地点
                self.logger.info(self.platform + ":添加地点")
                await page.locator(
                    '//*[@id="publish-container"]/div/div[3]/div[2]/div[8]/div[1]/div[2]/div/div/div/input').fill(
                    '上海')
                await asyncio.sleep(1.3)
                await page.locator(
                    '//*[@id="publish-container"]/div/div[3]/div[2]/div[8]/div[1]/div[2]/div/div/div/div[1]/ul/li[1]'
                ).click()
                await asyncio.sleep(1.3)
                # 发布
                self.logger.info(self.platform + ":开始发布")
                try:
                    async with page.expect_navigation(timeout=3000):
                        await page.locator('//*[@id="publish-container"]/div/div[3]/div[2]/div[9]/button[1]/span'
                                           ).click()
                        await asyncio.sleep(2)
                    if page.url == config.xhs_config["check_site"]:
                        self.logger.info(self.platform + ":发布成功")
                        # ("xhs", "00", "20240114", "htts://00.mp4", "../files/test/00.mp4", "", "测试")
                        excute_sqlite_sql(config.table_add_sql,
                                          (self.platform, video_name, datetime.now().strftime('%Y%m%d'),
                                           video_url, video_path, collection, description))
                        await browser.close()
                        await playwright.stop()
                        return True
                    else:
                        self.logger.error(self.platform + " ERR:跳转错误")
                        await browser.close()
                        await playwright.stop()
                        return False
                except Exception as e:
                    self.logger.error(f"{self.platform} ERR:发布失败 {e}")
                    return False
        except Exception as e:
            print(f"An error occurred during the upload: {e}")
            return False
