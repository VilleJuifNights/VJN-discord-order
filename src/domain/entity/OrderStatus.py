import enum
from typing import Optional


class OrderStatus(enum.Enum):
    PENDING = "PENDING"
    PAYED = "PAYED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    RETRIEVED = "RETRIEVED"

    CANCELED = "CANCELED"
    EXPIRED = "EXPIRED"


def status_to_string(status: OrderStatus) -> str:
    match = {
        OrderStatus.PENDING: "En attente de paiement",
        OrderStatus.PAYED: "Payé, en attente de préparation",
        OrderStatus.IN_PROGRESS: "En préparation",
        OrderStatus.COMPLETED: "Prêt à être récupéré",
        OrderStatus.RETRIEVED: "Récupéré",
        OrderStatus.CANCELED: "Annulé",
        OrderStatus.EXPIRED: "Expiré"
    }
    return match[status]


def status_to_button_label(status: OrderStatus) -> str:
    match = {
        OrderStatus.PAYED: "Marquer comme payé",
        OrderStatus.IN_PROGRESS: "Marquer comme en préparation",
        OrderStatus.COMPLETED: "Marquer comme prêt à être récupéré",
        OrderStatus.RETRIEVED: "Marquer comme récupéré",
    }
    return match[status]


def next_status(status: OrderStatus) -> OrderStatus:
    match = {
        OrderStatus.PENDING: OrderStatus.PAYED,
        OrderStatus.PAYED: OrderStatus.IN_PROGRESS,
        OrderStatus.IN_PROGRESS: OrderStatus.COMPLETED,
        OrderStatus.COMPLETED: OrderStatus.RETRIEVED,
    }
    return match[status]