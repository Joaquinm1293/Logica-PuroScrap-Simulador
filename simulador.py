import math
import random
import datetime
import numpy as np
from typing import List, Optional



ahora = datetime.datetime.now()
n0 = (ahora.hour * 3600) + (ahora.minute * 60) + ahora.second

def gu() -> float:
    global n0  # Le dice a la función que use y actualice el 'n0' de arriba
    
    a = 10
    c = 5
    m = 10000
    digitos = 5
    
    n0 = (a * n0 + c) % m
    
    return round(n0 / m, digitos)


def exponencial_inversa(media: float = 7.0) -> float:
    u = max(gu(), 1e-10)
    return -media * math.log(u)

def poisson_num_piezas(lam: float = 15) -> int:
    return max(1, int(np.random.poisson(lam)))

def normal_gramos(media: float, desv: float = 1.6) -> float:
    return max(0.0, np.random.normal(media, desv))

def uniforme_gramos(minimo: float = 15.0, maximo: float = 30.0) -> float:
    return minimo + (maximo - minimo) * gu()

def reciclar(tipo: str):
    if tipo == "Mouse":
        return normal_gramos(10.0, 1.6), normal_gramos(7.0, 1.6)
    return uniforme_gramos(15.0, 30.0), uniforme_gramos(15.0, 30.0)

def desamblar(tipo: str, lam_piezas: float = 15):
    precio_C, precio_H = 13.7, 0.50
    mat_reutilizado = mat_desechado = mat_reciclado = 0
    total_cobre = total_hierro = 0.0

    m = poisson_num_piezas(lam_piezas)
    i = 1
    while i <= m:
        u = gu()
        if u <= 0.72:
            cg, hg = reciclar(tipo)
            total_cobre  += cg
            total_hierro += hg
            mat_reciclado += 1
        elif u <= 0.97:
            mat_reutilizado += 1
        else:
            mat_desechado += 1
        i += 1

    ingreso = (total_cobre * precio_C) + (total_hierro * precio_H)
    return ingreso, mat_reciclado, mat_reutilizado, mat_desechado


def ejecutar_simulacion(
    cant_mouses:       int,
    cant_teclados:     int,
    costo_hora:        float,
    horas_jornada:     int,
    cantidad_mesas:    int,
    costo_fijo_diario: float,
    min_empleados:     int,
    max_empleados:     int,
    lam_piezas:        float = 15,
    prob_recicla:      float = 0.80,
    semilla:           Optional[int] = None,
) -> dict:

    if semilla is not None:
        random.seed(semilla)
        np.random.seed(semilla)

    minutos_jornada = horas_jornada * 60
    cantidad_P      = cant_mouses + cant_teclados
    tipo            = "Mouse"
    tiempo_total    = 0.0
    ingreso_Total   = 0.0
    reciclados = reutilizados = 0
    piezas_recicladas = piezas_reutilizadas = piezas_desechadas = 0

    i = 0
    while i < cantidad_P:
        tiempo_total += exponencial_inversa(7.0)
        u = gu()

        if u <= prob_recicla:
            ing, pr, pu, pd = desamblar(tipo, lam_piezas)
            ingreso_Total      += ing
            piezas_recicladas  += pr
            piezas_reutilizadas+= pu
            piezas_desechadas  += pd
            reciclados         += 1
        else:
            if tipo == "Mouse":
                ingreso_Total += uniforme_gramos(5_000.0, 8_000.0)
            else:
                ingreso_Total += uniforme_gramos(6_000.0, 12_000.0)
            reutilizados += 1

        if i + 1 == cant_mouses:
            tipo = "Teclado"
        i += 1

   
    escenarios = []
    for n in range(min_empleados, max_empleados + 1):
        factible         = (n <= cantidad_mesas)
        tiempo_paralelo  = tiempo_total / n
        jornales_x_emp   = math.ceil(tiempo_paralelo / minutos_jornada)
        jornales_totales = jornales_x_emp * n
        dias_necesarios  = jornales_x_emp
        costo_laboral    = round(jornales_totales * horas_jornada * costo_hora,    2)
        costo_fijo_total = round(dias_necesarios  * costo_fijo_diario,             2)
        costo_total      = round(costo_laboral + costo_fijo_total,                 2)
        rentabilidad     = round(ingreso_Total - costo_total,                      2)

        
        detalles = {
            "formula_tiempo_paralelo": f"{tiempo_total:.2f} min totales / {n} empleados = {tiempo_paralelo:.2f} min por empleado",
            "formula_jornales_x_emp": f"Techo({tiempo_paralelo:.2f} min / {minutos_jornada} min/día) = {jornales_x_emp} días trabajando",
            "formula_jornales_totales": f"{jornales_x_emp} días x {n} empleados = {jornales_totales} jornales a pagar",
            "formula_costo_laboral": f"{jornales_totales} jornales x {horas_jornada} horas x ${costo_hora}/h = ${costo_laboral}",
            "formula_costo_fijo": f"{dias_necesarios} días de alquiler x ${costo_fijo_diario}/día = ${costo_fijo_total}",
            "formula_costo_total": f"${costo_laboral} (Laboral) + ${costo_fijo_total} (Fijo) = ${costo_total}",
            "formula_rentabilidad": f"${ingreso_Total:.2f} (Ingresos) - ${costo_total} (Costos) = ${rentabilidad}"
        }

        escenarios.append({
            "n_empleados":      n,
            "factible":         factible,
            "jornales_totales": jornales_totales,
            "dias_necesarios":  dias_necesarios,
            "costo_laboral":    costo_laboral,
            "costo_fijo_total": costo_fijo_total,
            "costo_total":      costo_total,
            "rentabilidad":     rentabilidad,
            "es_optimo":        False,
            "detalles":         detalles # Lo agregamos al diccionario
        })

    factibles = [e for e in escenarios if e["factible"]]
    optimo    = max(factibles, key=lambda e: e["rentabilidad"]) if factibles else None
    if optimo:
        optimo["es_optimo"] = True

    return {
        "cant_mouses":            cant_mouses,
        "cant_teclados":          cant_teclados,
        "costo_hora":             costo_hora,
        "horas_jornada":          horas_jornada,
        "cantidad_mesas":         cantidad_mesas,
        "costo_fijo_diario":      costo_fijo_diario,
        "min_empleados":          min_empleados,
        "max_empleados":          max_empleados,
        "tiempo_total_minutos":   round(tiempo_total, 2),
        "tiempo_total_horas":     round(tiempo_total / 60, 2),
        "ingreso_total":          round(ingreso_Total, 2),
        "cant_reciclados":        reciclados,
        "cant_reutilizados":      reutilizados,
        "cant_piezas_recicladas":   piezas_recicladas,
        "cant_piezas_reutilizadas": piezas_reutilizadas,
        "cant_piezas_desechadas":   piezas_desechadas,
        "escenarios":             escenarios,
        "optimo_n_empleados":     optimo["n_empleados"]      if optimo else None,
        "optimo_jornales":        optimo["jornales_totales"] if optimo else None,
        "optimo_dias":            optimo["dias_necesarios"]  if optimo else None,
        "optimo_costo_laboral":   optimo["costo_laboral"]    if optimo else None,
        "optimo_costo_fijo":      optimo["costo_fijo_total"] if optimo else None,
        "optimo_costo_total":     optimo["costo_total"]      if optimo else None,
        "optimo_rentabilidad":    optimo["rentabilidad"]     if optimo else None,
        "optimo_es_ganancia":     (optimo["rentabilidad"] >= 0) if optimo else None,
    }
