from enum import Enum


class OrderStatus(Enum):
    NEW = "NEW"
    PAID = "PAID"
    CANCELED = "CANCELED"
