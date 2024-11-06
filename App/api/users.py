# App/api/user.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from App.models import UsersModel
from App.schemas import User
from App.db import get_db

router = APIRouter(prefix="/users", tags=["Users"])


