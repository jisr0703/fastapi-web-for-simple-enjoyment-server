from sqlalchemy import Column, BigInteger, DateTime, func, String, SmallInteger
from sqlalchemy.orm import Session

from app.database import conn


class BaseMixin:
    id = Column(BigInteger, primary_key=True, index=True)
    updated_at = Column(DateTime, nullable=True, default=func.utc_timestamp())
    created_at = Column(DateTime, nullable=True, default=func.utc_timestamp())

    def all_columns(self):
        return [c for c in self.__table__.columns if c.primary_key is False and c.name != 'create_at']

    def __hash__(self):
        return hash(self.id)

    @classmethod
    def create(cls, session: Session, auto_commit: bool = False, **kwargs):
        obj = cls()
        for col in obj.all_columns():
            col_name = col.name
            if col_name in kwargs:
                setattr(obj, col_name, kwargs.get(col_name))
        session.add(obj)
        session.flush()
        if auto_commit:
            session.commit()
        return obj

    @classmethod
    def get(cls, **kwargs):
        session = next(conn.db.session())
        query = session.query(cls)
        for key, val in kwargs.items():
            col = getattr(cls, key)
            query = query.filter(col == val)

            if query.count() > 1:
                raise Exception("Only one row is supposed to be returned, but got more than one.")
            return query.first()


class Feelings(conn.Base, BaseMixin):
    __tablename__ = 'feelings'
    feeling = Column(String(length=20), nullable=False)


class FellingComments(conn.Base, BaseMixin):
    __tablename__ = 'felling_comments'
    parent_id = Column(BigInteger, nullable=False)
    feeling_id = Column(BigInteger, nullable=False)
    reference_datetime = Column(DateTime, nullable=False)
    temp_id = Column(String(length=50), nullable=False)
    temp_pw = Column(String(length=50), nullable=False)
    comment = Column(String(length=2048), nullable=False)


class IPs(conn.Base, BaseMixin):
    __tablename__ = 'ips'
    ip = Column(String(length=50), nullable=False)
    # ipv4 = Column(Integer, nullable=True, signed=True)
    # ipv6 = Column(BINARY(length=16), nullable=True)


class Reactions(conn.Base, BaseMixin):
    __tablename__ = 'reactions'
    reaction = Column(String(20), nullable=False)


class FellingCommentReactions(conn.Base, BaseMixin):
    __tablename__ = 'felling_comment_reactions'
    ip_id = Column(BigInteger, nullable=False)
    comment_id =  Column(BigInteger, nullable=False)
    reaction_id =  Column(BigInteger, nullable=False)


# Log
class FeelingsLog(conn.Base, BaseMixin):
    __tablename__ = 'feelings_log'
    ip_id = Column(BigInteger, nullable=False)
    feeling_id = Column(BigInteger, nullable=False)
    # feelings_id = Column(BigInteger, nullable=False, ForeignKey=True)


class Users(conn.Base, BaseMixin):
    __tablename__ = 'Users'
    uid = Column(String(length=255), nullable=False)
    name = Column(String(length=50), nullable=False)
    profile_img = Column(String(length=255), nullable=True)
    email = Column(String(length=50), nullable=True)
    gender = Column(String(length=4), nullable=True)
    birth = Column(String(length=10), nullable=True)
