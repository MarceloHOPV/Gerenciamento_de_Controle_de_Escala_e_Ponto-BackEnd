from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from App.db import Base
from App.utils.common_schemas_Enum import Genero

class UsersModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    hashed_password = Column(String, index=False)  # Remove o índice para hashed_password
    is_active = Column(Boolean, index=True)
    user_type = Column(String) 
    __mapper_args__ = {
        'polymorphic_identity': 'users',
        'polymorphic_on': user_type
    }

