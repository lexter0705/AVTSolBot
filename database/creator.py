from sqlalchemy import create_engine,ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship, backref
from sqlalchemy.testing.schema import mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]


class Wallet(Base):
    __tablename__ = 'wallet'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    address: Mapped[str]
    secret_phrase: Mapped[str]
    user: Mapped[User] = relationship(User, backref=backref("children", cascade="all,delete"))


if __name__ == '__main__':
    engine = create_engine("sqlite:///main.db")
    Base.metadata.create_all(engine)
