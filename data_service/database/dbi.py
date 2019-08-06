from data_service import database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from data_service.database import models
from data_service.utils import constant


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
                    "password": user.password
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