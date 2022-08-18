class Reserve():
    def __init__(self, userId, roomCode, startDate, endDate) -> None:
        self.userId = userId
        self.roomCode = roomCode
        self.startDate = startDate
        self.endDate = endDate

    def to_JSON(self):
        return {
            'userId': self.userId,
            'roomCode': self.roomCode,
            'startDate': self.startDate,
            'endDate': self.endDate
        }
