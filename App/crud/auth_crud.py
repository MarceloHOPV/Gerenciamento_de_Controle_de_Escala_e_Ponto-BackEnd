from sqlalchemy.orm import Session
from App.db import SessionLocal
from typing import Annotated
from fastapi import HTTPException, Depends
from App.models import User
# from schemas.auth_schemas # Colocar o criado



