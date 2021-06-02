import datetime
from mongoengine import *
from internals import errors

COL_ADMIN = "admin"

class Admin(Document):
    username = StringField(unique=True, required=True)
    password = StringField(required=True)
    createTime = DateTimeField(default=datetime.datetime.utcnow())

    # meta = {
    #     'ordering': ['-published_date']
    # }

    def isValidate(self) -> bool:
        if len(self.username) == 0 or len(self.password) == 0:
            return False
        return True

    def Add(self) -> str:
        try:
            self.save()
        except NotUniqueError:
            return "username is exist"
        return ""


def Get(admin: Admin) -> str:
    admin_users = Admin.objects(username=admin.username,password=admin.password)
    # print(len(admin_users))
    if not admin_users:
        return "username or password is wrong"
    return ""
