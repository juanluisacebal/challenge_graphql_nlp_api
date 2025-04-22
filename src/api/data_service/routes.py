from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...core.models import ChallengeData
from ...core.auth import get_current_user

router = APIRouter()

class DataPoint(BaseModel):
    id_tie_fecha_valor: Optional[int] = None
    id_cli_cliente: Optional[int] = None
    id_ga_vista: Optional[int] = None
    id_ga_tipo_dispositivo: Optional[int] = None
    id_ga_fuente_medio: Optional[int] = None
    desc_ga_sku_producto: Optional[str] = None
    desc_ga_categoria_producto: Optional[float] = None
    fc_agregado_carrito_cant: Optional[int] = None
    fc_ingreso_producto_monto: Optional[float] = None
    fc_retirado_carrito_cant: Optional[float] = None
    fc_detalle_producto_cant: Optional[int] = None
    fc_producto_cant: Optional[int] = None
    desc_ga_nombre_producto: Optional[float] = None
    fc_visualizaciones_pag_cant: Optional[float] = None
    flag_pipol: Optional[int] = None
    sasasa: Optional[str] = None
    id_ga_producto: Optional[int] = None
    desc_ga_nombre_producto_1: Optional[str] = None
    desc_ga_sku_producto_1: Optional[str] = None
    desc_ga_marca_producto: Optional[str] = None
    desc_ga_cod_producto: Optional[float] = None
    desc_categoria_producto: Optional[str] = None
    desc_categoria_prod_principal: Optional[str] = None

    class Config:
        orm_mode = True

@router.get("/points", response_model=List[DataPoint])
async def get_data_points(
    category: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Obtiene puntos de datos con filtros opcionales.
    
    Args:
        category: Filtrar por categoría
        start_date: Fecha de inicio
        end_date: Fecha de fin
        db: Sesión de la base de datos
        current_user: Usuario autenticado
    
    Returns:
        List[DataPoint]: Lista de puntos de datos que coinciden con los filtros
    """
    try:
        query = db.query(ChallengeData)
        
        if category:
            query = query.filter(ChallengeData.desc_categoria_producto == category)
        
        if start_date:
            query = query.filter(ChallengeData.id_tie_fecha_valor >= start_date)
        
        if end_date:
            query = query.filter(ChallengeData.id_tie_fecha_valor <= end_date)
        
        return query.all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/points/{point_id}", response_model=DataPoint)
async def get_data_point(
    point_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Obtiene un punto de datos específico por ID.
    
    Args:
        point_id: ID del punto de datos
        db: Sesión de la base de datos
        current_user: Usuario autenticado
    
    Returns:
        DataPoint: El punto de datos solicitado
    """
    try:
        data_point = db.query(ChallengeData).filter(
            ChallengeData.id_tie_fecha_valor == point_id
        ).first()
        
        if not data_point:
            raise HTTPException(status_code=404, detail="Punto de datos no encontrado")
        
        return data_point
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 