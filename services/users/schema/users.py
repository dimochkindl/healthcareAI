from datetime import datetime
import sqlalchemy
from core.db import DefaultBase
from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

class User(DefaultBase):
    __tablename__ = 'users'
    metadata = DefaultBase.metadata

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(20), unique=True)
    password_hash: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    def __repr__(self):
        return f'<User username={self.username}, email={self.email}, is_active={self.is_active}, created_at={self.created_at}>'

    def __str__(self):
        return self.username


class Role(DefaultBase):
    __tablename__ = 'roles'
    metadata = DefaultBase.metadata

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)

    def __repr__(self):
        return f'<Role name={self.name}, description={self.description}>'


class Permission(DefaultBase):
    __tablename__ = 'permissions'
    metadata = DefaultBase.metadata

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50))
    action: Mapped[str] = mapped_column(String)
    resource: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)

    def __repr__(self):
        return f'<Permission name={self.name}, description={self.description}>'


class Group(DefaultBase):
    __tablename__ = 'groups'
    metadata = DefaultBase.metadata

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)

    def __repr__(self):
        return f'<Group name={self.name}, description={self.description}>'


user_roles = sqlalchemy.Table(
    'user_roles',
    DefaultBase.metadata,
    sqlalchemy.Column('user_id', Integer, ForeignKey('users.id')),
    sqlalchemy.Column('role_id', Integer, ForeignKey('roles.id')),
)


user_permissions = sqlalchemy.Table(
    'user_permissions',
    DefaultBase.metadata,
    sqlalchemy.Column('user_id', Integer, ForeignKey('users.id')),
    sqlalchemy.Column('permission_id', Integer, ForeignKey('permissions.id')),
)


user_groups = sqlalchemy.Table(
    'user_groups',
    DefaultBase.metadata,
    sqlalchemy.Column('user_id', Integer, ForeignKey('users.id')),
    sqlalchemy.Column('group_id', Integer, ForeignKey('groups.id')),
)


role_permissions = sqlalchemy.Table(
    'role_permissions',
    DefaultBase.metadata,
    sqlalchemy.Column('role_id', Integer, ForeignKey('roles.id', ondelete='CASCADE')),
    sqlalchemy.Column('permission_id', Integer, ForeignKey('permissions.id')),
)


group_roles = sqlalchemy.Table(
    'group_roles',
    DefaultBase.metadata,
    sqlalchemy.Column('group_id', Integer, ForeignKey('groups.id')),
    sqlalchemy.Column('role_id', Integer, ForeignKey('roles.id', ondelete='CASCADE')),
)
