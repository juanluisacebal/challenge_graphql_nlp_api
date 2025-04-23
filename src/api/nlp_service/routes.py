from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...core.auth import get_current_user
from .nlp_processor import NLPProcessor

router = APIRouter()
nlp_processor = NLPProcessor()

class NLPQuery(BaseModel):
    query: str
    context: Optional[dict] = None

class DataPoint(BaseModel):
    id_tie_fecha_valor: Optional[int] = None
    id_cli_cliente: Optional[int] = None
    #id_ga_vista: Optional[int] = None
    #id_ga_tipo_dispositivo: Optional[int] = None
    id_ga_fuente_medio: Optional[int] = None
    #desc_ga_sku_producto: Optional[str] = None
    desc_ga_categoria_producto: Optional[float] = None
    fc_agregado_carrito_cant: Optional[int] = None
    fc_ingreso_producto_monto: Optional[float] = None
    #fc_retirado_carrito_cant: Optional[float] = None
    fc_detalle_producto_cant: Optional[int] = None
    fc_producto_cant: Optional[int] = None
    #desc_ga_nombre_producto: Optional[float] = None
    #fc_visualizaciones_pag_cant: Optional[float] = None
    flag_pipol: Optional[int] = None
    #sasasa: Optional[str] = None
    id_ga_producto: Optional[int] = None
    desc_ga_nombre_producto_1: Optional[str] = None
    desc_ga_sku_producto_1: Optional[str] = None
    desc_ga_marca_producto: Optional[str] = None
    desc_ga_cod_producto: Optional[float] = None
    desc_categoria_producto: Optional[str] = None
    desc_categoria_prod_principal: Optional[str] = None

    class Config:
        orm_mode = True

class NLPResponse(BaseModel):
    result: str
    confidence: float
    data_points: List[DataPoint]
    filters_applied: dict

@router.post("/query", response_model=NLPResponse)
async def process_nlp_query(
    query: NLPQuery,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Procesa una consulta en lenguaje natural.
    
    Args:
        query: Consulta en lenguaje natural
        db: Sesión de la base de datos
        current_user: Usuario autenticado
    
    Returns:
        NLPResponse: Resultados de la consulta
    """
    try:
        return await nlp_processor.process_query(query.query, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 