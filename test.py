from core import config
from utils.util_sqlite import check, excute_sqlite_sql

if __name__ == "__main__":
    # 执行
    # excute_sqlite_sql(config.table_add_sql,("xhs", "00", "20240114", "htts://00.mp4", "../files/test/00.mp4", "", "测试"))
    # excute_sqlite_sql(config.table_select_url_sql, ("xhs", "htts://00.mp4"))
    # check("xhs", "https://test")
    print(check("xhs", "https://test"))
    # excute_sqlite_sql(config.table_all_sql)
