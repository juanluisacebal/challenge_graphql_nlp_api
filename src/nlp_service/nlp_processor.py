import os
from typing import Dict, List, Optional
from openai import OpenAI
from sqlalchemy.orm import Session
from ...core.models import ChallengeData

class NLPProcessor:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.system_prompt = """
        Eres un asistente especializado en análisis de datos de comercio electrónico.
        Tu tarea es convertir consultas en lenguaje natural a consultas SQL o filtros específicos.
        
        La tabla tiene las siguientes columnas:
        - id_tie_fecha_valor: ID de fecha
        - id_cli_cliente: ID de cliente
        - id_ga_vista: ID de vista
        - id_ga_tipo_dispositivo: ID de tipo de dispositivo
        - id_ga_fuente_medio: ID de fuente/medio
        - desc_ga_sku_producto: SKU del producto
        - desc_ga_categoria_producto: Categoría del producto
        - fc_agregado_carrito_cant: Cantidad agregada al carrito
        - fc_ingreso_producto_monto: Monto de ingreso al producto
        - fc_retirado_carrito_cant: Cantidad retirada del carrito
        - fc_detalle_producto_cant: Cantidad de detalles de producto
        - fc_producto_cant: Cantidad de productos
        - desc_ga_nombre_producto: Nombre del producto
        - fc_visualizaciones_pag_cant: Cantidad de visualizaciones de página
        - flag_pipol: Flag PIPOL
        - sasasa: Campo SASASA
        - id_ga_producto: ID de producto
        - desc_ga_nombre_producto_1: Nombre del producto 1
        - desc_ga_sku_producto_1: SKU del producto 1
        - desc_ga_marca_producto: Marca del producto
        - desc_ga_cod_producto: Código del producto
        - desc_categoria_producto: Categoría del producto
        - desc_categoria_prod_principal: Categoría principal del producto
        """

    async def process_query(self, query: str, db: Session) -> Dict:
        """
        Procesa una consulta en lenguaje natural y devuelve los resultados.
        
        Args:
            query: Consulta en lenguaje natural
            db: Sesión de la base de datos
        
        Returns:
            Dict con los resultados y metadatos
        """
        try:
            # Obtener respuesta de OpenAI
            response = self.client.chat.completions.create(
                model="gpt-4.1-nano",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"Convierte esta consulta a filtros SQL: {query}"}
                ],
                temperature=0.3
            )
            
            # Extraer filtros de la respuesta
            filters = self._parse_filters(response.choices[0].message.content)
            
            # Aplicar filtros a la consulta
            query = db.query(ChallengeData)
            for field, value in filters.items():
                if hasattr(ChallengeData, field):
                    query = query.filter(getattr(ChallengeData, field) == value)
            
            # Ejecutar consulta
            results = query.all()
            
            return {
                "result": "Consulta procesada exitosamente",
                "confidence": 0.9,
                "data_points": results,
                "filters_applied": filters
            }
            
        except Exception as e:
            return {
                "result": f"Error al procesar la consulta: {str(e)}",
                "confidence": 0.0,
                "data_points": [],
                "filters_applied": {}
            }

    def _parse_filters(self, response: str) -> Dict:
        """
        Parsea la respuesta de OpenAI para extraer los filtros.
        
        Args:
            response: Respuesta de OpenAI
        
        Returns:
            Dict con los filtros extraídos
        """
        # TODO: Implementar lógica de parsing más robusta
        filters = {}
        # Ejemplo simple de parsing
        if "categoría" in response.lower():
            filters["desc_categoria_producto"] = response.split("=")[1].strip()
        return filters 