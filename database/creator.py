from sqlalchemy import create_engine,ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship, backref
from sqlalchemy.testing.schema import mapped_column


class Base(DeclarativeBase):
    pass


class UserTable(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]


class WalletTable(Base):
    __tablename__ = 'wallet'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    private_key: Mapped[str]
    user: Mapped[UserTable] = relationship(UserTable, backref=backref("children", cascade="all,delete"))


if __name__ == '__main__':
    engine = create_engine("sqlite:///main.db")
    Base.metadata.create_all(engine)
