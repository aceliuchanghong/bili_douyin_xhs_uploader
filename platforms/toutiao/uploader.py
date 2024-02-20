import asyncio
import json
from playwright.async_api import async_playwright
import random
from core import config
from core.upload import Upload
from utils.util_sqlite import excute_sqlite_sql
from datetime import datetime


class ToutiaoUploader(Upload):
    """
    开始上传,包括以下几个部分:
    1.作品名称 2.作品简介 3.添加话题 4.选择合集
    若是上传成功之后,将数据写入sqlite数据库,没成功就不写入

    此处仅涉及横屏视频上传代码,竖屏未写
    方正粉丝体还不错,之后可以考虑下
    使用CSS选择器和文本选择器结合 会很舒服
    """
    platform = "toutiao"

    async def upload_video(self, video_url, video_path, video_name, cover_path=None, description=None, topics=None,
                           collection=None,
                           headless=False):
        if topics is None:
            topics = []
        topics = topics + config.toutiao_keywords
        try:
            self.logger.info(f"Uploading video '{video_name}' to {self.platform}...")
            # cookie 加载
            with open(config.toutiao_config["cookie_path"], 'r') as file:
                storage_state = json.load(file)
            async with (async_playwright() as playwright):
                # 登录
                self.logger.info(self.platform + ":登陆中")
                browser = await playwright.chromium.launch(headless=headless)
                context = await browser.new_context(storage_state=storage_state)
                page = await context.new_page()

                await page.goto(config.toutiao_config["up_site"])
                await page.wait_for_url(config.toutiao_config["up_site"])
                self.logger.info(self.platform + ":登陆成功")
                # 视频上传
                self.logger.info(self.platform + ":视频上传中")
                # 点击上传按钮
                async with page.expect_file_chooser() as fc_info:
                    await page.locator(
                        '//*[@id="root"]/div/div[1]/div[2]/div/div[1]/div/div/div/div[2]/div/div/div/div/div/div'
                    ).click()
                file_chooser = await fc_info.value
                await file_chooser.set_files(video_path, timeout=3000)
                self.logger.info(self.platform + ":视频上传完毕")
                # 填写作品标题
                self.logger.info(self.platform + ":设置标题")
                up_title = video_name + "|" + random.choice(config.key_sentence)
                await page.locator(
                    '//*[@id="root"]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div/div/div/input'
                ).fill(up_title[:29])
                # 填写作品简介
                self.logger.info(self.platform + ":设置简介")
                await page.locator(
                    '//*[@id="root"]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div[6]/div[2]/div/div/textarea'
                ).fill(description)
                # 填写作品话题
                self.logger.info(self.platform + ":添加作品话题")
                css_selector = ".arco-input-tag-input"
                await page.click(css_selector)
                for topic in topics:
                    await page.type(css_selector, topic)
                    await asyncio.sleep(1.3)
                    await page.press(css_selector, "Enter")
                # 关闭智能标题/封面
                self.logger.info(self.platform + ":关闭智能标题/封面")
                await page.locator(
                    '//*[@id="root"]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div[2]/div/div/div/p/button'
                ).click()
                await page.locator(
                    '//*[@id="root"]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div[5]/div/div/div/p/button'
                ).click()
                # 点击转载
                self.logger.info(self.platform + ":点击转载")
                await page.locator(
                    '.byte-radio:has-text("转载")'
                ).click()
                # 生成图文 ==>默认开启,不要点了
                self.logger.info(self.platform + ":生成图文")
                # await page.locator(
                #     '//*[@id="root"]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div[8]/div[2]/div/div[2]/label/span/span'
                # ).click()
                # 取自站外
                self.logger.info(self.platform + ":取自站外")
                await page.locator(
                    '//*[@id="root"]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div[3]/div[2]/div/div/span/label[1]/span/span'
                ).click()
                # 取消同步到抖音
                self.logger.info(self.platform + ":取消同步到抖音")
                await page.locator(
                    '//*[@id="root"]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div[4]/div[2]/div/div/div/label/span/span'
                ).click()
                # 选择合集
                self.logger.info(self.platform + ":选择合集")
                await page.locator(
                    '//*[@id="root"]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div[1]/div[2]/div/button/span/span'
                ).click()
                await page.locator(
                    '.byte-radio:has-text("赚钱方法论实践合集2.0")'
                ).click()
                # 合集点击确认 ==> 使用CSS选择器和文本选择器结合
                await page.locator(
                    '.byte-btn-primary:has-text("确定")'
                ).click()
                # 设置封面
                self.logger.info(self.platform + ":封面上传中")
                async with page.expect_file_chooser() as fc_info:
                    await page.locator(
                        '//*[@id="root"]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div[4]/div[2]/div[1]/div/div'
                    ).click()
                    await page.locator(
                        'ul.header > li:nth-child(2)'
                    ).click()
                    await page.locator(
                        '.byte-upload-trigger-picture'
                    ).click()
                file_chooser = await fc_info.value
                await file_chooser.set_files(cover_path, timeout=3000)
                # 完成裁剪
                try:
                    await page.locator(
                        '//*[@id="tc-ie-base-content"]/div[2]/div[2]/div[2]/div/div[2]/div/div/div[2]'
                    ).click()
                except Exception as e:
                    self.logger.info(self.platform + ":封面上传裁剪不需要")
                # 点击我的
                await page.locator(
                    '//*[@id="tc-ie-base-content"]/div[2]/div[1]/div/div/div[1]/div[1]'
                ).click()
                # 自定义模板
                await page.locator(
                    '//*[@id="tc-ie-base-content"]/div[2]/div[1]/div/div/div[2]/div[2]/div[2]'
                ).click()
                # 模板点击
                try:
                    await page.locator(
                        '//*[@id="tc-ie-base-content"]/div[2]/div[1]/div/div/div[3]/div/div/div[2]/div/img'
                    ).click()
                except Exception as e:
                    self.logger.info(self.platform + ":封面上传无对应模板")
                # 确认点击
                await page.locator(
                    '//*[@id="tc-ie-base-content"]/div[2]/div[2]/div[3]/div[3]/button[2]'
                ).click()
                # 再次确认点击
                await page.locator(
                    '.footer .m-button.red:has-text("确定")'
                ).click()
                await asyncio.sleep(10)
                self.logger.info(self.platform + ":封面上传完毕")
                # 发布
                self.logger.info(self.platform + ":开始发布")
                try:
                    async with page.expect_navigation(timeout=3000):
                        await page.locator(
                            '//*[@id="root"]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/div[2]/div[3]/div/button[2]'
                        ).click()
                        await asyncio.sleep(1.5)
                    # print(page.url)
                    if page.url == config.toutiao_config["check_site"]:
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
