
import enum


class OrderStatus(enum.Enum):
    PENDING = "PENDING"
    PAYED = "PAYED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    RETRIEVED = "RETRIEVED"

    CANCELED = "CANCELED"
    EXPIRED = "EXPIRED"


