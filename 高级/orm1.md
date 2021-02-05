```python

class Session:
    def add(self, instance):
        print('=== Session.add ===')
        table_name = self.__get_table_name(instance)
        fields = self.__get_fields(instance)
        sql_str = 'select `%s` from `%s`' % (', '.join(fields), table_name)
        self.execute_sql(sql_str)

    def add_all(self, instances):
        for instance in instances:
            self.add(instance)

    def delete(self, instance):
        pass

    def update(self, instance):
        pass

    @staticmethod
    def __get_table_name(instance):
        return instance.__class__.__tablename__

    @staticmethod
    def __get_fields(instance):
        """
        将 {'_name': 'Ming', '_age': 15, '_sex': '男'}
        转为 {'name': 'Ming', 'age': 15, 'sex': '男'}
        """
        # return {_k[1:]: v for _k, v in _d.items()}    # 列表推导式
        fields = {}
        for _key, value in instance.__dict__.items():
            column_name = _key[1:]
            fields[column_name] = value
        return fields

    def execute_sql(self, sql_str):
        print(sql_str)
        
```
```python
from mm.db_model import Session

class Field(object):
    def __init__(self, read_only=False):
        self.field_name = None
        self.read_only = read_only

    def __set__(self, instance, value):
        setattr(instance, self.field_name, value)

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.field_name, '')


class CharField(Field):
    def __init__(self, max_length=10, **kwargs):
        super().__init__(**kwargs)
        # max_length 必须为大于0的数
        if max_length is None or max_length < 0:
            raise ValueError('max_length must be a positive number')
        self.max_length = max_length

    def __set__(self, instance, value):
        # 1. read_only 只允许第一次赋值，不允许之后第二次赋值
        if self.read_only and \
                getattr(instance, self.field_name, ''):
            raise RuntimeError('read_only can not be modify')
        # 2. len(value) 不能大于 max_length
        if len(value) > self.max_length:
            raise ValueError("value's len must small than mat_length")
        super().__set__(instance, value)    # 调用父类


class IntegerField(Field):
    def __set__(self, instance, value):
        # value 必须为 int 类型
        if not isinstance(value, int):
            raise ValueError('IntegerField value must be int')
        super().__set__(instance, value)    # 调用父类


class Meta(type):
    def __new__(mcs, name, bases, class_dict):
        for key, value in class_dict.items():
            if isinstance(value, Field):
                value.field_name = '_' + key
        return super().__new__(mcs, name, bases, class_dict)


class Model(object, metaclass=Meta):
    def __init__(self, **kwargs):
        super().__init__()
        for k, v in kwargs.items():
            setattr(self, k, v)


class User(Model):
    __tablename__ = 'user'

    name = CharField()
    age = IntegerField()
    sex = CharField(max_length=2)
    number = CharField(read_only=True)      # 只读的number，仅第一次可以写

    # def __init__(self, name, age, sex, number):
    #     super().__init__(name=name, age=age, sex=sex, number=number)


if __name__ == "__main__":
    user1 = User(name="XiaoMing", age=15, sex="男", number='201010')
    user2 = User(name="XiaoHong", age=26, sex="女")
    print(user1.name, user1.age, user1.sex)
    print(user2.name, user2.age, user2.sex)
    user2.number = '101010'       # 第一次赋值
    # user1.number = '202020'     # 已经初始化过了，第二次赋值报错
    print(user1.__dict__)
    print(user2.__dict__)
    # user2.sex = '我是女'       # 报错

    session = Session()
    session.add(user1)
    session.add_all([user1, user2])
```
