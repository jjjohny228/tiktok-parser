import datetime

from peewee import CharField, Model, SqliteDatabase, ForeignKeyField, DateTimeField, BigIntegerField, BooleanField

db = SqliteDatabase('data/TikTok.db')


class _BaseModel(Model):
    class Meta:
        database = db


class User(_BaseModel):
    """
    The model contains users information.
    """
    class Meta:
        db_table = 'users'

    username = CharField(default='Пользователь')
    first_name = CharField(null=True)
    last_name = CharField(null=True)
    telegram_id = BigIntegerField(unique=True, null=False)
    registration_timestamp = DateTimeField(default=datetime.datetime.now())


class Channel(_BaseModel):
    """
    Contains info about TikTok channels
    """
    class Meta:
        db_table = 'channels'

    url = CharField(unique=True)
    name = CharField()


class Video(_BaseModel):
    """
    Contains info about TikTok videos
    """
    class Meta:
        db_table = 'videos'

    channel = ForeignKeyField(Channel, backref='videos', on_delete='CASCADE')
    url = CharField(unique=True)
    parsed_time = DateTimeField(default=datetime.datetime.now())


class Target(_BaseModel):
    """
    Contains info about TikTok source channels and YouTube channel apostol id where parsed videos will be posted
    """
    class Meta:
        db_table = 'targets'

    source_channel = ForeignKeyField(Channel, backref='target', on_delete='CASCADE', unique=True)
    target_channel_url = CharField(unique=True)
    channel_apostol_id = CharField(unique=True)
    platform = CharField(default='youtube')
    last_video_published_time = DateTimeField(null=True)


def register_models() -> None:
    db.execute_sql("PRAGMA foreign_keys = ON;")
    for model in _BaseModel.__subclasses__():
        model.create_table()
