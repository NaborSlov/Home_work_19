from dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, uid: int) -> User:
        """
        Получение одного пользователя по id
        """
        return self.session.query(User).get(uid)

    def get_by_username(self, username: str) -> User:
        """
        Получение пользователя по username
        """
        return self.session.query(User).filter(User.username == username).first()

    def get_all(self) -> list[User]:
        """
        Получение всех пользователей
        """
        return self.session.query(User).all()

    def put(self, new_user: User):
        """
        Изменение пользователя
        """
        self.session.add(new_user)
        self.session.commit()

    def create(self, user_data: dict):
        """
        Создание нового пользователя
        """
        user = User(**user_data)
        self.session.add(user)
        self.session.commit()

    def delete(self, uid: int):
        """
        Удаление пользователя
        """
        user = self.get_one(uid)
        self.session.delete(user)
        self.session.commit()

