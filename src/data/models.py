from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

from src.domain.entity.OrderStatus import OrderStatus
from src.data.engine import Base


class OrderTopping(Base):
    __tablename__ = 'order_toppings'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)

    order_id = Column(UUID(as_uuid=True), ForeignKey('orders.id'))
    order = relationship("Order", back_populates="toppings")


class Order(Base):
    __tablename__ = 'orders'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pretty_id = Column(Integer)

    user_id = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    status: Mapped["OrderStatus"] = mapped_column(default=OrderStatus.PENDING)
    total_cost = Column(Float)

    category = Column(String)
    toppings = relationship("OrderTopping", cascade="all, delete-orphan")
