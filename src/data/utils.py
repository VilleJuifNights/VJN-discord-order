from typing import Union

import discord
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.data.engine import engine
from src.data.models import Order, OrderTopping
from src.domain.entity.Config import Category, Choice
from src.domain.entity.OrderStatus import OrderStatus


def get_next_counter() -> int:
    with engine.connect() as con:
        r = con.execute(text("SELECT nextval(\'counter_seq\')"))
        result = r.fetchone()
        return result[0]


def reset_counter():
    with engine.connect() as con:
        con.execute(text("SELECT setval(\'counter_seq\', 1, false)"))


def get_session() -> Session:
    return Session(engine)


def create_order(user: Union[discord.Member,discord.User, str], category: Category, toppings: list[Choice]) -> Order:
    price = category.price + sum([topping.extra for topping in toppings])
    status = OrderStatus.PENDING if price > 0 else OrderStatus.PAYED
    order = Order(
        pretty_id=get_next_counter(),
        user_id=user.id if isinstance(user, discord.Member) or isinstance(user, discord.User) else user,
        status=status,
        total_cost=price,
        category=category.name,
        toppings=[OrderTopping(name=topping.name) for topping in toppings]
    )

    return order
