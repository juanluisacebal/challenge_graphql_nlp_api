from sqlalchemy import Column, Integer, Float, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

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
    desc_ga_nombre_producto_1 = Column(Text, nullable=True)
    desc_ga_sku_producto_1 = Column(Text, nullable=True)
    desc_ga_marca_producto = Column(Text, nullable=True)
    desc_ga_cod_producto = Column(Float, nullable=True)
    desc_categoria_producto = Column(Text, nullable=True)
    desc_categoria_prod_principal = Column(Text, nullable=True) 