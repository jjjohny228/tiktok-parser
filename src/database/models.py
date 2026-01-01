import datetime

from peewee import CharField, Model, SqliteDatabase, ForeignKeyField, DateTimeField

db = SqliteDatabase('TikTok.db')


class BaseModel(Model):
    class Meta:
        database = db


class Channel(BaseModel):
    class Meta:
        db_table = 'channels'

    url = CharField(unique=True)
    name = CharField(unique=True)


class Video(BaseModel):
    class Meta:
        db_table = 'videos'

    channel = ForeignKeyField(Channel, backref='videos')
    url = CharField(unique=True)
    parsed_time = DateTimeField(default=datetime.datetime.now())


class Target(BaseModel):
    class Meta:
        db_table = 'targets'

    source_channel = ForeignKeyField(Channel, backref='targets')
    target_channel_url = CharField(unique=True)
    channel_apostol_id = CharField(unique=True)


def register_models() -> None:
    for model in BaseModel.__subclasses__():
        model.create_table()
