class Room():

    def __init__(self, name, descriptionShort, descriptionLarge, price, code, score) -> None:
        self.name = name
        self.descriptionShort = descriptionShort
        self.descriptionLarge = descriptionLarge
        self.price = price
        self.code = code
        self.score = score

    def to_JSON(self):
        return {
            'name': self.name,
            'descriptionShort': self.descriptionShort,
            'descriptionLarge': self.descriptionLarge,
            'price': self.price,
            'code': self.code,
            'score': self.score
        }

class RoomJoin():

    def __init__(self, name, descriptionShort, descriptionLarge, price, code, score, image) -> None:
        self.name = name
        self.descriptionShort = descriptionShort
        self.descriptionLarge = descriptionLarge
        self.price = price
        self.code = code
        self.score = score
        self.image = image

    def to_JSON(self):
        return {
            'name': self.name,
            'descriptionShort': self.descriptionShort,
            'descriptionLarge': self.descriptionLarge,
            'price': self.price,
            'code': self.code,
            'score': self.score,
            'image': self.image
        }
