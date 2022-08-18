class User():

    def __init__(self, fullName, document, email, password) -> None:
        self.fullName = fullName
        self.document = document
        self.email = email
        self.password = password

    def to_JSON(self):
        return {
            'fullName': self.fullName,
            'document': self.document,
            'email': self.email,
            'password': self.password
        }


class userJoin():

    def __init__(self, id, fullName, document, email, role) -> None:
        self.id = id
        self.fullName = fullName
        self.document = document
        self.email = email
        self.role = role

    def to_JSON(self):
        return {
            'id': self.id,
            'fullName': self.fullName,
            'document': self.document,
            'email': self.email,
            'role': self.role
        }


class UserEdit():

    def __init__(self, id, fullName, email) -> None:
        self.id = id
        self.fullName = fullName
        self.email = email

    def to_JSON(self):
        return {
            'id': self.id,
            'fullname': self.fullName,
            'email': self.email,
        }
