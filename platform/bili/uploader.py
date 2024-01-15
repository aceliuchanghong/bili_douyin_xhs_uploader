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
                titles = [video_name + "|为什么最能打拼的员工默默离职，却连一声问候都未曾收到",
                          video_name + "|为何那些不曾在风口浪尖却始终坚守岗位的人，总是悄无声息地被遗忘",
                          video_name + "|为什么工作最勤恳的人总是不被提拔，他们的辛劳似乎只是被默认的存在",
                          video_name + "|为何那些总是默默解决问题的人，他们的背影却从不出现在表彰仪式上",
                          video_name + "|为什么那些总是最后离开办公室的人，他们的努力却从不成为加薪的理由",
                          video_name + "|为什么公司的支柱总是悄无声息地走人，而留下的只是对他们成就的轻描淡写",
                          video_name + "|为何总是那些对工作有真才实学的人，他们的离开却不足为领导所动",
                          video_name + "|为什么那些在困难中挺身而出的人，离去时却连一句感激都未能听到",
                          video_name + "|为何每当夜深人静，办公室里还有人在加班，但他们的名字从不出现在升职名单上",
                          video_name + "|为什么那些总是无私奉献的人，当他们选择离开时，却连一次留下的机会都没有",
                          video_name + "|为何那些默默填补团队裂痕的人，他们的贡献却从不被公开表扬",
                          video_name + "|为什么在危机时刻挺身而出的英雄，平静时却无人记起他们的名字",
                          video_name + "|为何公司的静默奉献者，在决定离开时，却未曾得到过一次诚挚的挽留",
                          video_name + "|为什么那些提升团队凝聚力的人，他们的离别却如同无声的烟花，美丽却瞬间即逝",
                          video_name + "|为什么那些总是为公司考虑的人，当他们走后，连一次回头的机会都没有",
                          video_name + "|为何那些在细节中追求完美的人，他们的精益求精往往只能自我欣赏",
                          video_name + "|为什么那些为团队稳健前行默默承受压力的人，他们的负重却很少有人去理解",
                          video_name + "|为何在项目关键时刻总能依靠的人，项目成功后却很少有人铭记",
                          video_name + "|为什么那些总是在关键时刻站出来的领路人，他们的辛劳往往不被看作是领导力的体现",
                          video_name + "|为何那些无怨无悔投入工作的人，他们的默默付出却常常不被视作是职责之外的努力",
                          video_name + "|为什么对公司文化建设有巨大贡献的人，他们的离开却未能激起一丝波澜",
                          video_name + "|为何那些在团队中默默耕耘，却鲜有成果展示机会的人，总是悄悄地被边缘化",
                          video_name + "|为什么那些总是以身作则，却不善于自我推销的人，他们的努力很少被看作是成功的典范",
                          video_name + "|为何那些在日常工作中总能提供创见的人，他们的智慧往往只在小圈子里被赞赏",
                          video_name + "|为什么那些在客户面前维护公司形象的人，他们的辛勤工作往往不被内部所知",
                          video_name + "|为何那些在技术上不断突破自我，却不擅长表达的人，他们的才华往往被埋没",
                          video_name + "|为什么那些在危机中保持冷静，为公司避免损失的人，他们的智慧很少被记载",
                          video_name + "|为何那些在工作中总是默默承担最多的人，他们的付出往往不被作为加薪的依据",
                          video_name + "|为什么那些对公司忠诚度极高的人，在选择离开时，连一句留言的机会都没有",
                          video_name + "|为何那些在组织中起到黏合剂作用的人，他们的离去却不会引起领导层的注意"]
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
