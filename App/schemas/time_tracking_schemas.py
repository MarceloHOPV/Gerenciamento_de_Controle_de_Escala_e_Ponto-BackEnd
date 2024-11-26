from pydantic import BaseModel
from typing import List, Optional, Dict
from App.utils.common_schemas_Enum import Hora, Dia_semana
#**********************************Modelos*****************************************#

class BankHours(BaseModel):
    horas_trabalhadas: Hora
    saldo_horas: Optional[Hora]

class WorkScheduleEntry(BaseModel):
    day_of_week: Dia_semana
    start_time: Hora
    end_time: Hora

# Modelo que contém a lista de horários
class WorkScheduleSchema(BaseModel):
    data_hora: List[WorkScheduleEntry]
    
class TimePunchCreate(BaseModel):
    employee_id: int