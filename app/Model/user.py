from datetime import date
from typing import List
from pydantic import BaseModel
from pydantic import EmailStr
import json


class BankAccount(BaseModel):
    bankName: str
    agency: str
    accountNumber: str
    balance: float
    accountType: str


class User(BaseModel):
    name: str
    email: EmailStr
    password: str
    isActive: bool
    lastActiveDate: date
    account: List[BankAccount]


class Template(BaseModel):
    name: str
    category: str
    fields: json

