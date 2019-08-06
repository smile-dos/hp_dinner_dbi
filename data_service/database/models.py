from data_service.database import Model
import sqlalchemy as sc
import datetime


class User(Model):
    __tablename__ = "hd_user"

    id = sc.Column(sc.Integer, primary_key=True)
    username = sc.Column(sc.String(50), nullable=False, unique=True)
    password = sc.Column(sc.String(200), nullable=False)
    is_superuser = sc.Column(sc.Boolean, default=False, nullable=False)
    is_active = sc.Column(sc.Boolean, default=False, nullable=False)
    email = sc.Column(sc.String(300), nullable=True, unique=True)
    phone = sc.Column(sc.String(30), nullable=True, unique=True)
    contactor = sc.Column(sc.String(50), nullable=True)
    realname = sc.Column(sc.String(50), nullable=True)
    avatar = sc.Column(sc.String(200), nullable=True)
    service_serial = sc.Column(sc.String(200), nullable=True)
    is_modify_username = sc.Column(sc.Boolean, default=False, nullable=False)
    is_vip = sc.Column(sc.Boolean, default=False, nullable=False)
    vip_id = sc.Column(sc.Integer, nullable=True)
    create_at = sc.Column(sc.DateTime, default=datetime.datetime.now)
    update_at = sc.Column(sc.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
