from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class UserInfo(Base):
    __tablename__ = 'user_info'
    id = Column(Integer, primary_key=True)
    languages = Column(String)  # Убедитесь что название поля совпадает


# Явно укажите путь к БД и включите логирование SQL
engine = create_engine('sqlite:///database/users.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def savedata(user_id: int, languages: str):

    with Session() as session:
        try:
            # 1. Поиск записи
            user = session.query(UserInfo).get(user_id)

            # 2. Обновление или создание
            if user:
                user.languages = languages
            else:
                user = UserInfo(id=user_id, languages=languages)
                session.add(user)

            # 3. Фиксация изменений
            session.commit()

        except Exception as e:
            session.rollback()
            raise


def savedones(id):
    with Session() as session:
        try:
            # 1. Поиск записи
            user = session.query(UserInfo).get(id)
            if user:
                language = user.languages.split(' ')
                language = ', '.join(language)
                return f"или воспользуйтесь /skip, чтобы использовать языки, которые вы использовали в прошлый раз: {language.lower()}"
            else:
                return ''
        except Exception:
            return ''


def esh(id):
    with Session() as session:
        user = session.query(UserInfo).get(id)
        return user.languages