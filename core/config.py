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
