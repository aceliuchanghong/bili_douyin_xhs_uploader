import asyncio
import json
from playwright.async_api import async_playwright
import random
from core import config
from core.upload import Upload
from utils.util_sqlite import excute_sqlite_sql
from datetime import datetime


class BiliUploader(Upload):
    """
    开始上传,包括以下几个部分:
    1.作品名称 2.作品简介 3.添加话题 4.选择合集
    若是上传成功之后,将数据写入sqlite数据库,没成功就不写入
    """
    platform = "bili"

    async def upload_video(self, video_url, video_path, video_name, description=None, topics=None, collection=None):
        try:
            self.logger.info(f"Uploading video '{video_name}' to {self.platform}...")
            # cookie 加载
            with open(config.bili_config["cookie_path"], 'r') as file:
                storage_state = json.load(file)
            async with (async_playwright() as playwright):
                # 登录
                self.logger.info(self.platform + ":登陆中")
                try:
                    browser = await playwright.chromium.launch(headless=False)
                    context = await browser.new_context(storage_state=storage_state)
                    page = await context.new_page()

                    await page.goto(config.bili_config["up_site"])
                    await page.wait_for_url(config.bili_config["up_site"])
                except Exception as e:
                    print(f"{self.platform}:Cookie过期: {e}")
                    return False
                self.logger.info(self.platform + ":登陆成功")
                # 视频上传
                self.logger.info(self.platform + ":视频上传中")
                async with page.expect_file_chooser() as fc_info:
                    await page.locator('//*[@id="video-up-app"]/div[1]/div[2]/div/div[1]/div/div/div').click()
                file_chooser = await fc_info.value
                await file_chooser.set_files(video_path, timeout=3000)
                # await page.set_input_files('input[type="file"]', [video_path])
                self.logger.info(self.platform + ":视频上传完毕")
                # 填写作品名称
                self.logger.info(self.platform + ":设置标题")
                titles = ["猫派狗派谁更胜一筹|" + video_name, "网红美食真的好吃吗|" + video_name,
                          "动画改编真人版讨论|" + video_name, "童年游戏最佳排名|" + video_name,
                          "智能家居便利还是麻烦|" + video_name, "未来学校是否无需老师|" + video_name,
                          "拍照滤镜是非必需|" + video_name, "睡前刷手机好不好|" + video_name,
                          "无人驾驶车辆安全性|" + video_name, "星巴克咖啡过于昂贵|" + video_name]
                up_title = random.choice(titles)
                await asyncio.sleep(2.2)
                await page.locator('.input.input-container > .input-instance > .input-val').fill('')
                await page.locator('.input.input-container > .input-instance > .input-val').fill(up_title)
                # 填写作品来源
                self.logger.info(self.platform + ":填写作品来源")
                await page.locator('div.type-source-input-wrp .input-container .input-instance .input-val'
                                   ).fill("youtube")
                # 选择合集
                self.logger.info(self.platform + ":选择合集")
                await page.locator('div.season-enter .season-enter-text-default >> nth=0').click()
                await asyncio.sleep(0.5)
                await page.locator('text=欢乐视频合集').click()
                """
                # 打开声明面板 ==> 此处搞不定
                self.logger.info(self.platform + ":打开声明面板")
                # await page.locator('div.title > span.label').click()
                # await page.locator('div.specific-section > span.label:has(svg.icon-sprite)').click()
                await page.locator('span.label:has(svg.icon-sprite)').click()
                """
                # 发布
                self.logger.info(self.platform + ":开始发布")
                try:
                    await asyncio.sleep(6)
                    await page.locator(
                        'div.form-item > div.submit-container > span.submit-add'
                    ).click()
                    await asyncio.sleep(10)
                    element = page.locator('.step-des:has-text("稿件投递成功")')
                    count = await element.count()
                    if count == 1:
                        self.logger.info(self.platform + ":发布成功")
                        # ("xhs", "00", "20240114", "htts://00.mp4", "../files/test/00.mp4", "", "测试")
                        excute_sqlite_sql(config.table_add_sql,
                                          (self.platform, video_name, datetime.now().strftime('%Y%m%d'),
                                           video_url, video_path, collection, description))
                        await browser.close()
                        await playwright.stop()
                        return True
                    else:
                        self.logger.error(self.platform + " ERR:跳转错误,出现验证码滑块")
                        await browser.close()
                        await playwright.stop()
                        return False
                except Exception as e:
                    self.logger.error(f"{self.platform} ERR:发布失败 {e}")
                    return False
        except Exception as e:
            print(f"An error occurred during the upload: {e}")
            return False
