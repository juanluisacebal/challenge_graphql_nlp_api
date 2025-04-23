from sqlalchemy import Column, Integer, Float, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from typing import Optional, List
import re

Base = declarative_base()

class CategoryNode:
    def __init__(self, name: str, path: str):
        self.name = name
        self.path = path
        self.children: List['CategoryNode'] = []

    def add_child(self, child: 'CategoryNode'):
        self.children.append(child)

    def find_node(self, path: str) -> Optional['CategoryNode']:
        if self.path == path:
            return self
        for child in self.children:
            result = child.find_node(path)
            if result:
                return result
        return None

    def get_all_paths(self) -> List[str]:
        paths = [self.path]
        for child in self.children:
            paths.extend(child.get_all_paths())
        return paths

class ChallengeData(Base):
    __tablename__ = "challenge_graphql_nlp_api"

    id_tie_fecha_valor = Column(Integer, primary_key=True)
    id_cli_cliente = Column(Integer, nullable=True)
    #id_ga_vista = Column(Integer, nullable=True)
    #id_ga_tipo_dispositivo = Column(Integer, nullable=True)
    id_ga_fuente_medio = Column(Integer, nullable=True)
    #desc_ga_sku_producto = Column(Text, nullable=True)
    desc_ga_categoria_producto = Column(Float, nullable=True)
    fc_agregado_carrito_cant = Column(Integer, nullable=True)
    fc_ingreso_producto_monto = Column(Float, nullable=True)
    #fc_retirado_carrito_cant = Column(Float, nullable=True)
    fc_detalle_producto_cant = Column(Integer, nullable=True)
    fc_producto_cant = Column(Integer, nullable=True)
    #desc_ga_nombre_producto = Column(Float, nullable=True)
    #fc_visualizaciones_pag_cant = Column(Float, nullable=True)
    flag_pipol = Column(Integer, nullable=True)
    #sasasa = Column(Text, nullable=True)
    id_ga_producto = Column(Integer, nullable=True)
    desc_ga_nombre_producto_1 = Column(String, nullable=True)
    desc_ga_sku_producto_1 = Column(String, nullable=True)
    desc_ga_marca_producto = Column(String, nullable=True)
    desc_ga_cod_producto = Column(Float, nullable=True)
    desc_categoria_producto = Column(String, nullable=True)
    desc_categoria_prod_principal = Column(String, nullable=True)

    @property
    def category_paths(self) -> List[str]:
        """Devuelve las rutas de categoría como lista"""
        if not self.desc_categoria_producto:
            return []
        return [path.strip() for path in self.desc_categoria_producto.split(',')]

    @property
    def category_tree(self) -> CategoryNode:
        """Construye y devuelve el árbol de categorías"""
        root = CategoryNode("root", "")
        
        for path in self.category_paths:
            current_node = root
            parts = path.split('/')
            current_path = ""
            
            for part in parts:
                current_path = f"{current_path}/{part}" if current_path else part
                existing_node = current_node.find_node(current_path)
                
                if not existing_node:
                    new_node = CategoryNode(part, current_path)
                    current_node.add_child(new_node)
                    current_node = new_node
                else:
                    current_node = existing_node
        
        return root

    def is_in_category(self, category_path: str) -> bool:
        """Verifica si el producto pertenece a una categoría específica"""
        return any(path.startswith(category_path) for path in self.category_paths) 