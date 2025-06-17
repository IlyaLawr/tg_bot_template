from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy import ForeignKey, MetaData, DateTime, Integer, String, Boolean, func, text


convention = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s',
}


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(naming_convention=convention)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class ProfileModel(Base):
    client_id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(String(100), default='', server_default='')
    registration_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    taps_statistics: Mapped[int] = mapped_column(default=0, server_default=text('0'))
    about: Mapped[str] = mapped_column(String(500), default='', server_default='')
    photo: Mapped[str] = mapped_column(String(255), default='', server_default='')

    user: Mapped['UserModel'] = relationship('UserModel', 
                                             back_populates='profile', 
                                             uselist=False,
                                             cascade='all, delete-orphan')


class UserModel(Base):
    client_id: Mapped[int] = mapped_column(Integer,
                                           ForeignKey('profilemodel.client_id', ondelete='CASCADE'),
                                           primary_key=True,
                                           unique=True)

    username: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    access: Mapped[bool] = mapped_column(Boolean, default=False)
    
    profile: Mapped['ProfileModel'] = relationship('ProfileModel', back_populates='user')
