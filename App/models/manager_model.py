from App.models import UsersModel,EmployeesModel
from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

class ManagersModel(UsersModel):
    __tablename__ = 'managers'
    id = Column(Integer, ForeignKey("users.id"), primary_key=True, index=True)
    employees = relationship("EmployeesModel", back_populates="manager", foreign_keys=[EmployeesModel.manager_id])

    __mapper_args__ = {
        'polymorphic_identity': 'managers' 
    }