```python
from redis import StrictRedis


class Settings(object):
    '''
    Redis数据库配置
    '''
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    REDIS_PASSWORD = None
    REDIS_DB = 1  # 1号数据库


class RedisClient(object):
    def __init__(self, set_name):
        self.set_name = set_name
        self.__conn = StrictRedis(
            host=Settings.REDIS_HOST,
            port=Settings.REDIS_PORT,
            password=Settings.REDIS_PASSWORD,
            db=Settings.REDIS_DB,
            decode_responses=True
        )

    # 添加n个
    def put(self, *values):
        self.__conn.sadd(self.set_name, *values)

    # 获取指定数据数目
    def get(self, num=None):
        return self.__conn.srandmember(name=self.set_name, number=num)

    # 数据条数
    def length(self):
        return self.__conn.scard(name=self.set_name)

    def empty(self):
        return 0 == self.length()

    # 指定删除
    def pop(self, *cookies):
        self.__conn.srem(self.set_name, *cookies)

    # 随机删除num个
    def spop(self, num=None):
        if num is not None:
            for i in range(num):
                self.__conn.spop(name=self.set_name, count=None)
        else:
            self.__conn.spop(name=self.set_name, count=None)

    # 返回全部
    def get_all(self):
        return self.__conn.smembers(name=self.set_name)

    # 删除全部
    def pop_all(self):
        self.spop(self.length())


if __name__ == '__main__':
    rc = RedisClient(set_name='my_set')
    rc.pop_all()
    print(rc.get_all())
    print(rc.length())
    rc.put('AAAA')
    rc.put('aaaa', 'bbbb', 'cccc', 'dddd')
    print(rc.get_all())
    print(rc.length())
    print('get获取两个:', rc.get(2))
    rc.pop('aa')  # set没有'aa', 执行无效
    rc.pop('aaaa', 'bbbb')
    print('pop之后:', rc.get_all())
    rc.spop()
    print(rc.get_all())
    print(rc.empty())
    ```
