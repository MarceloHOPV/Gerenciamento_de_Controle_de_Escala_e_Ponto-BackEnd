from pydantic import BaseModel
from typing import List, Optional, Dict
from App.utils.common_schemas_Enum import Hora, Dia_semana
#**********************************Modelos*****************************************#

class BankHours(BaseModel):
    horas_trabalhadas: Hora
    saldo_horas: Optional[Hora]

class WorkSchedule(BaseModel):
    data_hora: List[Dict[Dia_semana,Hora]]

class TimePunches(BaseModel):
    data_hora: List[Dict[Dia_semana,Hora]]