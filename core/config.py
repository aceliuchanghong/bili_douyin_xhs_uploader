# 基础配置
PROXY = False
proxies = {
    "http": "http://127.0.0.1:10809",
    "https": "http://127.0.0.1:10809"
}
# DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL = "INFO"
# 上传网站属性
bili_config = {
    "cookie_path": "cookies/bili_cookies.json",
    "up_site": "https://member.bilibili.com/platform/upload/video/frame",
    "check_site": "https://member.bilibili.com/platform/upload/video/frame?page_from=creative_home_top_upload"
}
douyin_config = {
    "cookie_path": "cookies/douyin_cookies.json",
    "up_site": "https://creator.douyin.com/creator-micro/content/upload",
    "up_site2": "https://creator.douyin.com/creator-micro/content/publish?enter_from=publish_page",
    "check_site": "https://creator.douyin.com/creator-micro/content/manage"
}
toutiao_config = {
    "cookie_path": "cookies/toutiao_cookies.json",
    "up_site": "https://mp.toutiao.com/profile_v4/xigua/upload-video?from=toutiao_pc",
    "check_site": "https://mp.toutiao.com/profile_v4/xigua/content-manage-v2"
}
xhs_config = {
    "cookie_path": "cookies/xhs_cookies.json",
    "up_site": "https://creator.xiaohongshu.com/publish/publish",
    "check_site": "https://creator.xiaohongshu.com/publish/success?source&bind_status=not_bind"
}
# sqlite
db_path = "log/media_uploader.db"
create_table_sql = """
CREATE TABLE IF NOT EXISTS media_upload_info
(platform TEXT,video_name TEXT,download_date TEXT, video_url TEXT, video_path TEXT, remark1 TEXT, description TEXT)
"""
table_select_url_count_sql = """
select count(*) from media_upload_info where platform = ? and video_url = ?
"""
table_select_url_sql = """
select * from media_upload_info where platform = ? and video_url = ?
"""
table_count_sql = """
select count(*) from media_upload_info
"""
table_all_sql = """
select * from media_upload_info
"""
table_add_sql = """
INSERT INTO media_upload_info (platform, video_name, download_date, video_url, video_path, remark1, description)
VALUES (?, ?, ?, ?, ?, ?, ?)
"""
table_del_url_sql = """
delete from media_upload_info where platform = ? and video_url = ?
"""
table_truncate_sql = """
DELETE FROM media_upload_info
"""
# 关键字
keywords = [
    "搞笑",
    "外国人",
    "美女",
    "可爱女孩",
    "恋爱日常",
    "原神",
    "lol",
    "王者荣耀",
    "秋叶原",
    "日本"
]
douyin_keywords = [
    "搞笑",
    "外国人",
    "美女",
    "可爱女孩",
    "王者荣耀",
]

toutiao_keywords = [
    "搞笑",
    "外国人",
    "美女",
    "可爱女孩",
    "王者荣耀",
]

# 关键句
key_sentence = [
    "为什么最能打拼的员工默默离职，却连一声问候都未曾收到",
    "为何那些不曾在风口浪尖却始终坚守岗位的人，总是悄无声息地被遗忘",
    "为什么工作最勤恳的人总是不被提拔，他们的辛劳似乎只是被默认的存在",
    "为何那些总是默默解决问题的人，他们的背影却从不出现在表彰仪式上",
    "为什么那些总是最后离开办公室的人，他们的努力却从不成为加薪的理由",
    "为什么公司的支柱总是悄无声息地走人，而留下的只是对他们成就的轻描淡写",
    "为何总是那些对工作有真才实学的人，他们的离开却不足为领导所动",
    "为什么那些在困难中挺身而出的人，离去时却连一句感激都未能听到",
    "为何每当夜深人静，办公室里还有人在加班，但他们的名字从不出现在升职名单上",
    "为什么那些总是无私奉献的人，当他们选择离开时，却连一次留下的机会都没有",
    "为何那些默默填补团队裂痕的人，他们的贡献却从不被公开表扬",
    "为什么在危机时刻挺身而出的英雄，平静时却无人记起他们的名字",
    "为何公司的静默奉献者，在决定离开时，却未曾得到过一次诚挚的挽留",
    "为什么那些提升团队凝聚力的人，他们的离别却如同无声的烟花，美丽却瞬间即逝",
    "为什么那些总是为公司考虑的人，当他们走后，连一次回头的机会都没有",
    "为何那些在细节中追求完美的人，他们的精益求精往往只能自我欣赏",
    "为什么那些为团队稳健前行默默承受压力的人，他们的负重却很少有人去理解",
    "为何在项目关键时刻总能依靠的人，项目成功后却很少有人铭记",
    "为什么那些总是在关键时刻站出来的领路人，他们的辛劳往往不被看作是领导力的体现",
    "为何那些无怨无悔投入工作的人，他们的默默付出却常常不被视作是职责之外的努力",
    "为什么对公司文化建设有巨大贡献的人，他们的离开却未能激起一丝波澜",
    "为何那些在团队中默默耕耘，却鲜有成果展示机会的人，总是悄悄地被边缘化",
    "为什么那些总是以身作则，却不善于自我推销的人，他们的努力很少被看作是成功的典范",
    "为何那些在日常工作中总能提供创见的人，他们的智慧往往只在小圈子里被赞赏",
    "为什么那些在客户面前维护公司形象的人，他们的辛勤工作往往不被内部所知",
    "为何那些在技术上不断突破自我，却不擅长表达的人，他们的才华往往被埋没",
    "为什么那些在危机中保持冷静，为公司避免损失的人，他们的智慧很少被记载",
    "为何那些在工作中总是默默承担最多的人，他们的付出往往不被作为加薪的依据",
    "为什么那些对公司忠诚度极高的人，在选择离开时，连一句留言的机会都没有",
    "为何那些在组织中起到黏合剂作用的人，他们的离去却不会引起领导层的注意",
    "为什么那些夜以继日攻克学术难题的学者，他们的成就却很少有人去歌颂",
    "为何那些图书馆的常客，对知识有着渴望的人，他们的努力往往只为自己所知",
    "为什么在学术讨论中总能提出独到见解的思想者，他们的声音却鲜被大众听见",
    "为何那些在学术领域默默耕耘，却不善于宣传自己的研究者，往往默默无闻",
    "为什么那些在考试中总是名列前茅，却不居功自傲的学生，他们的谦逊很少被提及",
    "为何在学习上不断自我突破，却不张扬的人，他们的进步往往不被看作是激励他人的榜样",
    "为什么那些对知识有着无尽追求的人，在选择离开学术界时，却未引起足够重视",
    "为何那些在学术刊物上频繁发表，却鲜有人知晓的作者，他们的贡献往往不为出版社所重",
    "为什么那些在学校中默默帮助他人，却不求回报的学生，他们的善行往往不被记录",
    "为何那些在教育领域默默奉献，却不求名利的教师，他们的贡献往往不被社会所颂扬"
]
