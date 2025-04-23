import strawberry
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from starlette.requests import Request

from ...core.database import get_db
from ...core.models import ChallengeData
from ...core.auth import get_current_user

@strawberry.type
class Category:
    path: str
    name: str
    children: List['Category']

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
    async def categories(self, info) -> List[Category]:
        # Verificar autenticación y permisos
        request = info.context.get("request")
        if not request:
            raise HTTPException(
                status_code=401,
                detail="No se pudo obtener el contexto de la petición"
            )
        
        current_user = await get_current_user(request)
        if not current_user.get("realm_access", {}).get("roles"):
            raise HTTPException(
                status_code=403,
                detail="No tiene permisos para acceder a las categorías"
            )
        
        db: Session = next(get_db())
        try:
            # Obtener todos los productos para construir el árbol de categorías
            products = db.query(ChallengeData).all()
            
            # Construir el árbol de categorías
            category_map = {}
            root = Category(path="", name="root", children=[])
            category_map[""] = root
            
            for product in products:
                for path in product.category_paths:
                    parts = path.split('/')
                    current_path = ""
                    
                    for part in parts:
                        parent_path = current_path
                        current_path = f"{current_path}/{part}" if current_path else part
                        
                        if current_path not in category_map:
                            category = Category(path=current_path, name=part, children=[])
                            category_map[current_path] = category
                            category_map[parent_path].children.append(category)
            
            return root.children
        except Exception as e:
            raise Exception(str(e))
        finally:
            db.close()

    @strawberry.field
    async def get_data_points(
        self,
        info,
        category: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[DataPoint]:
        # Verificar autenticación y permisos
        request = info.context.get("request")
        if not request:
            raise HTTPException(
                status_code=401,
                detail="No se pudo obtener el contexto de la petición"
            )
        
        current_user = await get_current_user(request)
        if not current_user.get("realm_access", {}).get("roles"):
            raise HTTPException(
                status_code=403,
                detail="No tiene permisos para acceder a los datos"
            )
        
        db: Session = next(get_db())
        try:
            query = db.query(ChallengeData)
            
            if category:
                query = query.filter(
                    ChallengeData.desc_categoria_producto.like(f"%{category}%")
                )
            
            if start_date:
                query = query.filter(ChallengeData.id_tie_fecha_valor >= start_date)
            
            if end_date:
                query = query.filter(ChallengeData.id_tie_fecha_valor <= end_date)
            
            return query.all()
        except Exception as e:
            raise Exception(str(e))
        finally:
            db.close()

    @strawberry.field
    async def get_data_point(
        self,
        info,
        id_tie_fecha_valor: int
    ) -> Optional[DataPoint]:
        # Verificar autenticación y permisos
        request = info.context.get("request")
        if not request:
            raise HTTPException(
                status_code=401,
                detail="No se pudo obtener el contexto de la petición"
            )
        
        current_user = await get_current_user(request)
        if not current_user.get("realm_access", {}).get("roles"):
            raise HTTPException(
                status_code=403,
                detail="No tiene permisos para acceder a los datos"
            )
        
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
        finally:
            db.close()

schema = strawberry.Schema(query=Query) 