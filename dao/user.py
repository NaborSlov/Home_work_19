from dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, uid: int) -> User:
        return self.session.query(User).get(uid)

    def get_by_username(self, username: str) -> User:
        user = self.session.query(User).filter(User.username == username).first()
        return user

    def get_all(self) -> list[User]:
        return self.session.query(User).all()

    def put(self, new_user: User):
        self.session.add(new_user)
        self.session.commit()

    def create(self, user_data: dict):
        user = User(**user_data)
        self.session.add(user)
        self.session.commit()

    def delete(self, uid: int):
        user = self.get_one(uid)
        self.session.delete(user)
        self.session.commit()

