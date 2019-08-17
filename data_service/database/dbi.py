from data_service import database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy import exc as sc_exc
from sqlalchemy import desc
from data_service.database import models
from data_service.utils import constant
from data_service.database import execption
from data_service.utils.page import paginate


class Dbi(database.Base):
    name = "happy_dinner"

    def __init__(self, database_url):
        self.__engine = create_engine(
            database_url,
            encoding="utf8",
            convert_unicode=True,
            echo=True,
            pool_pre_ping=True,
            poolclass=NullPool
        )
        self.__session = sessionmaker(bind=self.__engine)

    def select_user_by_username(self, username):
        """
        Select user depend username
        :param username: [str] Username of user
        :return:
        """
        session = self.__session()
        try:
            user = session.query(models.User).filter(models.User.username == username).first()
            if user is None:
                raise execption.UsernameNotFound("Username not found.")
            msg = {
                "code": constant.ErrCode.ERR_OK,
                "message": "Select success",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "password": user.password,
                    "is_active": user.is_active,
                    "is_superuser": user.is_superuser,
                    "email": user.email,
                    "phone": user.phone,
                    "realname": user.realname,
                    "avatar": user.avatar,
                    "service_serial": user.service_serial,
                    "is_modify_username": user.is_modify_username,
                    "is_vip": user.is_vip
                }
            }
            return msg
        except Exception:
            raise
        finally:
            session.close()

    def select_user_by_id(self, user_id):
        """
        Select user info by user id
        :param user_id: [int] User table id
        :return:
        """
        session = self.__session()
        try:
            user = session.query(models.User).filter(models.User.id == user_id).first()
            if user is None:
                msg = {
                    "code": constant.ErrCode.ERR_USERNAME_NOT_FOUND,
                    "message": "Username not found."
                }
                return msg
            msg = {
                "code": constant.ErrCode.ERR_OK,
                "message": "Select success",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "password": user.password,
                    "is_active": user.is_active,
                    "is_superuser": user.is_superuser,
                    "email": user.email,
                    "phone": user.phone,
                    "realname": user.realname,
                    "avatar": user.avatar,
                    "service_serial": user.service_serial,
                    "is_modify_username": user.is_modify_username,
                    "is_vip": user.is_vip
                }
            }
            return msg
        except Exception as e:
            msg = {
                "code": constant.ErrCode.ERR_UNKNOWN,
                "message": str(e)
            }
            return msg
        finally:
            session.close()

    def create_user(self, username, password):
        """
        Create user by username and password
        :param username: [str] username
        :param password: [str] password with hashed
        :return:
        """
        session = self.__session()
        try:
            user = models.User()
            user.username = username
            user.password = password
            session.add(user)
            session.commit()
            msg = {
                "code": constant.ErrCode.ERR_OK,
                "message": "Create user success"
            }
            return msg
        except sc_exc.IntegrityError:
            raise execption.UsernameAlreadyExist()
        except Exception:
            raise
        finally:
            session.close()

    def select_user_list_by_page(self, page=1, page_size=20, keyword=None, sort_name=None, sort_order=None):
        """
        Select user list
        :param page: [int] Page number
        :param page_size: [int] Number items in one page
        :param keyword: [str] Keyword
        :param sort_name: [str] Order by column name
        :param sort_order: [str] Order by asc or desc
        :return:
        """
        session = self.__session()
        try:
            query = session.query(models.User).filter()
            if keyword:
                query = query.filter(models.User.username.like("%{}%".format(keyword)))

            if sort_name:
                if hasattr(models.User, sort_name):
                    sort_column_attr = getattr(models.User, sort_name)
                    if sort_order == "descending":
                        query.order_by(desc(sort_column_attr))
                    elif sort_order == "ascending":
                        query.order_by(sort_column_attr)
            else:
                query = query.order_by(desc(models.User.create_at))
            page_info = paginate(query=query, page=page, per_page=page_size)
            user_list = []
            for item in page_info.items:
                user_list.append({
                    "id": item.id,
                    "username": item.username,
                    "is_superuser": item.is_superuser,
                    "is_active": item.is_active,
                    "create_at": item.create_at.strftime("%Y-%y-%d %H:%M"),
                    "update_at": item.update_at.strftime("%Y-%y-%d %H:%M")
                })
            msg = {
                "total": page_info.total,
                "list": user_list
            }
            return msg
        except Exception:
            raise
        finally:
            session.close()
