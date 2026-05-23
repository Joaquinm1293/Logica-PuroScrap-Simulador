from typing import List, Optional
from pydantic import BaseModel


class DetalleCalculoOut(BaseModel):
    formula_tiempo_paralelo: str
    formula_jornales_x_emp: str
    formula_jornales_totales: str
    formula_costo_laboral: str
    formula_costo_fijo: str
    formula_costo_total: str
    formula_rentabilidad: str

class EscenarioOut(BaseModel):
    n_empleados:      int
    factible:         bool
    jornales_totales: int
    dias_necesarios:  int
    costo_laboral:    float
    costo_fijo_total: float
    costo_total:      float
    rentabilidad:     float
    es_optimo:        bool
    detalles:         DetalleCalculoOut 

class SimulacionOut(BaseModel):
    cant_mouses:       int
    cant_teclados:     int
    costo_hora:        float
    horas_jornada:     int
    cantidad_mesas:    int
    costo_fijo_diario: float
    min_empleados:     int
    max_empleados:     int

    tiempo_total_minutos:     float
    tiempo_total_horas:       float
    ingreso_total:            float
    cant_reciclados:          int
    cant_reutilizados:        int
    cant_piezas_recicladas:   int
    cant_piezas_reutilizadas: int
    cant_piezas_desechadas:   int

    escenarios: List[EscenarioOut]

    optimo_n_empleados:      Optional[int]
    optimo_jornales:         Optional[int]
    optimo_dias:             Optional[int]
    optimo_costo_laboral:    Optional[float]
    optimo_costo_fijo:       Optional[float]
    optimo_costo_total:      Optional[float]
    optimo_rentabilidad:     Optional[float]
    optimo_es_ganancia:      Optional[bool]

