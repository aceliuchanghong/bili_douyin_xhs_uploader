import asyncio
import json
from playwright.async_api import async_playwright
import random
from core import config
from core.upload import Upload
from utils.util_sqlite import excute_sqlite_sql
from datetime import datetime


class DouyinUploader(Upload):
    """
    开始上传,包括以下几个部分:
    1.作品名称 2.作品简介 3.添加话题 4.选择合集
    若是上传成功之后,将数据写入sqlite数据库,没成功就不写入
    """
    platform = "douyin"

    async def upload_video(self, video_url, video_path, video_name, description=None, topics=None, collection=None,
                           headless=False):
        if topics is None:
            topics = []
        topics = topics + config.douyin_keywords
        try:
            self.logger.info(f"Uploading video '{video_name}' to {self.platform}...")
            # cookie 加载
            with open(config.douyin_config["cookie_path"], 'r') as file:
                storage_state = json.load(file)
            async with (async_playwright() as playwright):
                # 登录
                self.logger.info(self.platform + ":登陆中")
                browser = await playwright.chromium.launch(headless=headless)
                context = await browser.new_context(storage_state=storage_state)
                page = await context.new_page()

                await page.goto(config.douyin_config["up_site"])
                await page.wait_for_url(config.douyin_config["up_site"])
                self.logger.info(self.platform + ":登陆成功")
                # 视频上传
                self.logger.info(self.platform + ":视频上传中")
                await page.locator(
                    "label:has-text(\"为了更好的观看体验和平台安全，平台将对上传的视频预审。超过40秒的视频建议上传横版视频\")"
                ).set_input_files(video_path)
                await page.wait_for_url(config.douyin_config["up_site2"])
                self.logger.info(self.platform + ":视频上传完毕")
                # 填写作品名称 简介 话题
                self.logger.info(self.platform + ":设置标题")
                up_title = video_name + "|" + random.choice(config.key_sentence)
                await page.locator(
                    '//*[@id="root"]/div/div/div[2]/div[1]/div[2]/div/div/div/div[1]/div/div/input').fill(
                    up_title)
                self.logger.info(self.platform + ":设置简介")
                await page.locator('//*[@id="root"]/div/div/div[2]/div[1]/div[2]/div/div/div/div[2]/div'
                                   ).fill(description)

                self.logger.info(self.platform + ":添加话题")
                css_selector = ".zone-container"
                await page.press(css_selector, "Enter")
                for topic in topics:
                    await page.locator(
                        '//*[@id="root"]/div/div/div[2]/div[1]/div[2]/div/div/div/div[3]/div[1]/div/div/div[1]'
                    ).click()
                    await page.locator('//*[@id="root"]/div/div/div[2]/div[1]/div[2]/div/div/div/div[2]/div').type(
                        topic)
                    await asyncio.sleep(1.3)
                    await page.press(css_selector, "Enter")
                # 选择合集
                self.logger.info(self.platform + ":选择合集")
                await page.locator(
                    '//*[@id="root"]/div/div/div[2]/div[1]/div[11]/div[2]/div[2]/div[1]/div/span').click()
                await page.locator('text=欢乐集结').click()
                # 地点
                self.logger.info(self.platform + ":添加地点")
                await page.locator(
                    '//*[@id="root"]/div/div/div[2]/div[1]/div[8]/div[2]/div[2]/div/div/div[1]/div/span'
                ).click()
                await page.locator(
                    '//*[@id="root"]/div/div/div[2]/div[1]/div[8]/div[2]/div[2]/div/div[1]/div[1]/div/div/input').fill(
                    '上海徐汇')
                await asyncio.sleep(1.2)
                '//*[@id="semi-select-671v8bk3bip"]/div/div[1]'
                await page.locator(
                    '//*[@id="root"]/div/div/div[2]/div[1]/div[8]/div[2]/div[2]/div/div[2]/div/div/div/div'
                ).click()
                # 发布
                self.logger.info(self.platform + ":开始发布")
                try:
                    async with page.expect_navigation(timeout=3000):
                        await page.locator(
                            'xpath=//*[@id="root"]//div/button[@class="button--1SZwR primary--1AMXd fixed--3rEwh"]'
                        ).click()
                        await asyncio.sleep(1.5)
                    if page.url == config.douyin_config["check_site"]:
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
