from enum import Enum

class OrderStatus(Enum):
    PENDING = "Pending"
    PROCESSING = "Processing"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"
