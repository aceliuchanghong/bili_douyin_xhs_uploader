import sqlite3
from sqlite3 import Connection
from core import config
import logging


class VerboseCursor(sqlite3.Cursor):
    """
    增加一个VerboseCursor修饰类,可以输出语句,记录日志
    """

    def __init__(self, __cursor: Connection):
        super().__init__(__cursor)
        self.logger = self._setup_logger()

    def _setup_logger(self):
        """
        设置日志记录器
        """
        logger = logging.getLogger(self.__class__.__name__)
        # 可以根据需要配置日志记录器，比如设置日志级别、格式和输出位置
        logger.setLevel(config.LOG_LEVEL)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def safe_format_sql(self, sql, parameters):
        # 使用 SQLite 的参数替换机制来安全地格式化 SQL 语句
        # 注意：这只是为了打印目的，不要使用这个函数来执行实际的 SQL 语句
        parameterized_sql = sql
        if parameters:
            for param in parameters:
                # 替换参数占位符
                parameterized_sql = parameterized_sql.replace("?", repr(param), 1)
        return parameterized_sql

    def execute(self, sql, parameters=None):
        self.logger.info(f"Executing SQL statement:{self.safe_format_sql(sql, parameters)}")
        if parameters:
            try:
                super().execute(sql, parameters)
            except sqlite3.Error as e:
                print(f"execute2:An error occurred: {e}")
                return False
            return True
        try:
            super().execute(sql)
        except sqlite3.Error as e:
            print(f"execute:An error occurred: {e}")
            return False
        return True


def excute_sqlite_sql(sql, param=None, should_print=False):
    conn = sqlite3.connect(config.db_path)
    c = VerboseCursor(conn)
    boolP = c.execute(sql, param)
    if boolP:
        results = c.fetchall()
        if should_print:
            for row in results:
                print(row)
        conn.commit()
    else:
        conn.rollback()
        return None
    c.close()
    conn.close()
    return results


def check(platform, url, should_print=False):
    ans = excute_sqlite_sql(config.table_select_url_count_sql, (platform, url), should_print)
    return ans[0][0]
