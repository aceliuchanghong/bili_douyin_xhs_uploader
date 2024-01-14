"""
*args：这是一个非关键字参数的列表，用于收集那些没有预先定义的参数。
参数 args 是一个元组，其中包含了所有未命名的变量参数。*args 可以接受任何数量的参数，这在你不确定将要传递给函数多少个参数时非常有用。
例如，如果你定义了一个函数 def my_function(*args):，你可以传递任意数量的非关键字参数给这个函数，这些参数将会被组织成一个元组。

**kwargs：这是一个关键字参数的字典，用于收集那些没有预先定义的关键字参数。
参数 kwargs 是一个字典，包含了所有未命名的关键字参数。**kwargs 允许你处理那些你事先不知道会收到的关键字参数。
例如，如果你定义了一个函数 def my_function(**kwargs):，你可以传递任意数量的关键字参数给这个函数，这些参数将会被组织成一个字典。

class Processor:
    def process(self, *args, **kwargs):
        print("Args:", args)
        print("Kwargs:", kwargs)

# 创建Processor类的实例
processor = Processor()

# 调用process方法，传入任意数量的参数
processor.process(1, 2, 3, a=4, b=5)

output:
Args: (1, 2, 3)
Kwargs: {'a': 4, 'b': 5}
"""
from core import config
from utils.util_sqlite import excute_sqlite_sql

if __name__ == "__main__":
    # excute_sqlite_sql(config.table_del_url_sql, ("douyin", "https://00.mp4"))
    excute_sqlite_sql(config.table_all_sql)
