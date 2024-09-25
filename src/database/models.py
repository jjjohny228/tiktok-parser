from peewee import CharField, IntegerField, Model, SqliteDatabase, ForeignKeyField

db = SqliteDatabase('TikTok.db')


class BaseModel(Model):
    class Meta:
        database = db


class Channel(BaseModel):
    class Meta:
        db_table = 'channels'

    url = CharField(unique=True)


class Video(BaseModel):
    class Meta:
        db_table = 'videos'

    channel = ForeignKeyField(Channel, backref='videos')
    url = CharField(unique=True)


def register_models() -> None:
    for model in BaseModel.__subclasses__():
        model.create_table()
