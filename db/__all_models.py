import datetime

import sqlalchemy

from db.db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    user_id = sqlalchemy.Column(sqlalchemy.BIGINT, unique=True, primary_key=True)
    referer_first_level_id = sqlalchemy.Column(sqlalchemy.BIGINT, default=0)
    balance = sqlalchemy.Column(sqlalchemy.FLOAT, default=0)
    deposit = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    request_time = sqlalchemy.Column(sqlalchemy.String)
    user_tariff_id = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    tokens_balance = sqlalchemy.Column(sqlalchemy.Integer, default=5000)
    reset_tokens = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    time_subscription = sqlalchemy.Column(sqlalchemy.Integer, default=None)
    time_to_new_request = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    is_banned = sqlalchemy.Column(sqlalchemy.BOOLEAN, default=False)
    last_answer = sqlalchemy.Column(sqlalchemy.String, default='')
    last_question = sqlalchemy.Column(sqlalchemy.String, default='')
    text = sqlalchemy.Column(sqlalchemy.String, default='')
