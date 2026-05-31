from typing import List
from pydantic import BaseModel

class EscenarioOut(BaseModel):
    n_empleados:          int
    dias_requeridos:      int
    costo_laboral:        float
    costo_almacenamiento: float
    costo_total:          float
    rentabilidad:         float

class DatosGeneralesOut(BaseModel):
    Total_Perifericos:        int
    Ingreso_Bruto_USD:        float
    Tiempo_Total_Horas:       float
    Material_Reutilizable_gr: float
    Residuo_Peligroso_gr:     float
    Perifericos_Reciclados:   int
    Perifericos_Reutilizados: int


class SimulacionOut(BaseModel):
    Datos_Generales:      DatosGeneralesOut
    Recomendacion_Optima: EscenarioOut
    Todos_Los_Escenarios: List[EscenarioOut]