import strawberry
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import Depends

from ...core.database import get_db
from ...core.models import ChallengeData
from ...core.auth import get_current_user

@strawberry.type
class DataPoint:
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

@strawberry.type
class Query:
    @strawberry.field
    async def get_data_points(
        self,
        info,
        category: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[DataPoint]:
        # Verificar autenticación
        await get_current_user(info.context["request"])
        
        db: Session = next(get_db())
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
            raise Exception(str(e))

    @strawberry.field
    async def get_data_point(
        self,
        info,
        id_tie_fecha_valor: int
    ) -> Optional[DataPoint]:
        # Verificar autenticación
        await get_current_user(info.context["request"])
        
        db: Session = next(get_db())
        try:
            data_point = db.query(ChallengeData).filter(
                ChallengeData.id_tie_fecha_valor == id_tie_fecha_valor
            ).first()
            
            if not data_point:
                raise Exception("Punto de datos no encontrado")
            
            return data_point
        except Exception as e:
            raise Exception(str(e))

schema = strawberry.Schema(query=Query) 