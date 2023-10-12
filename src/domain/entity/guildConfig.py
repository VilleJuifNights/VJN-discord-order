import datetime
import json
from typing import Optional, List

import discord
import yaml
from pydantic import BaseModel, Field, validator, field_validator, root_validator, model_validator


class Choice(BaseModel):
    name: str = Field(..., description="Name of the choice")
    price: float = Field(..., description="Price of the choice")


class Toppings(BaseModel):
    default: Optional[Choice] = Field(None, description="Default choice of the toppings")
    options: List[Choice] = Field([], description="List of choices of the toppings")
    recommandations: Optional[List[Choice]] = Field([], description="List of recommandations of the toppings")


class Category(BaseModel):
    name: str = Field(..., description="Name of the category")
    id: str = Field(..., description="ID of the category")
    emote: Optional[str] = Field(None, description="Emote of the category")
    toppings: Optional[Toppings] = Field(None, description="Toppings of the category")


class Config(BaseModel):
    categories: List[Category] = Field(..., description="List of categories")
