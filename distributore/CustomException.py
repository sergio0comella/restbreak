class OutOfRangeError(Exception):
    def __init__(self, message):
        super().__init__(message)

class GoalPositionNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)

class GoalPositionUnreacheable(Exception):
    def __init__(self, message):
        super().__init__(message)


class GoalPositionAlreadyReached(Exception):
    def __init__(self, message):
        super().__init__(message)
