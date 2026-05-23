import uvicorn
from typing import List, Optional
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware 
from esquemas import SimulacionOut
from simulador import ejecutar_simulacion

app = FastAPI(
    title       = "PuroScrap API",
    description = "Simulación Montecarlo de planta de reciclaje electrónico.",
    version     = "1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite que cualquier frontend se conecte
    allow_credentials=True,
    allow_methods=["*"],  # Permite GET, POST, etc.
    allow_headers=["*"],
)


@app.get("/health", summary="Estado de la API")
def health():
    return {"status": "ok", "service": "PuroScrap API v1.0.0"}


@app.get(
    "/simular",
    response_model = SimulacionOut,
    summary        = "Ejecutar simulación Montecarlo",
    description    = """
Simula el proceso de desensamble y reciclaje de periféricos electrónicos
y devuelve la tabla comparativa de rentabilidad por número de empleados.

**Parámetros requeridos:** `cant_mouses`, `cant_teclados`

**Parámetros opcionales con defaults razonables:**
- `min_empleados` / `max_empleados`: rango a evaluar (default 1–10)
- `cantidad_mesas`: capacidad física del galpón (default 5)
- `costo_hora`: $/hora-hombre (default 4500)
- `costo_fijo_diario`: costo fijo del galpón por día (default 20000)
- `horas_jornada`: horas por jornada (default 8)
- `semilla`: para reproducibilidad (default: aleatorio)
    """,
)
def simular(
    cant_mouses: int = Query(
        ..., ge=1, le=10_000,
        description="Cantidad de mouses a procesar (requerido, 1–10000)"
    ),
    cant_teclados: int = Query(
        ..., ge=1, le=10_000,
        description="Cantidad de teclados a procesar (requerido, 1–10000)"
    ),
    min_empleados: int = Query(
        1, ge=1, le=50,
        description="Mínimo de empleados a evaluar (default=1)"
    ),
    max_empleados: int = Query(
        10, ge=1, le=50,
        description="Máximo de empleados a evaluar (default=10)"
    ),
    cantidad_mesas: int = Query(
        5, ge=1, le=50,
        description="Capacidad física máxima de operarios simultáneos (default=5)"
    ),
    costo_hora: float = Query(
        4_500, ge=1,
        description="Costo por hora-hombre en $ (default=4500)"
    ),
    costo_fijo_diario: float = Query(
        20_000, ge=0,
        description="Costo fijo del galpón por día en $ (default=20000)"
    ),
    horas_jornada: int = Query(
        8, ge=1, le=24,
        description="Horas de trabajo por jornada (default=8)"
    ),
    semilla: Optional[int] = Query(
        None,
        description="Semilla RNG para reproducibilidad (default: aleatorio)"
    ),
):
    # Validaciones de negocio
    if min_empleados > max_empleados:
        raise HTTPException(
            status_code=422,
            detail="min_empleados no puede ser mayor que max_empleados."
        )

    resultado = ejecutar_simulacion(
        cant_mouses       = cant_mouses,
        cant_teclados     = cant_teclados,
        costo_hora        = costo_hora,
        horas_jornada     = horas_jornada,
        cantidad_mesas    = cantidad_mesas,
        costo_fijo_diario = costo_fijo_diario,
        min_empleados     = min_empleados,
        max_empleados     = max_empleados,
        semilla           = semilla,
    )

    return JSONResponse(content=resultado)



if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
