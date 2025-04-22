import os
from typing import Dict, List, Optional
from openai import OpenAI
from sqlalchemy.orm import Session
from sqlalchemy import and_
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
        - id_ga_fuente_medio: ID de fuente/medio
        - desc_ga_categoria_producto: Categoría del producto
        - fc_agregado_carrito_cant: Cantidad agregada al carrito
        - fc_ingreso_producto_monto: Monto de ingreso al producto
        - fc_detalle_producto_cant: Cantidad de detalles de producto
        - fc_producto_cant: Cantidad de productos
        - flag_pipol: Flag PIPOL
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
            filter_clauses = []
            for field, condition in filters.items():
                column = getattr(ChallengeData, field)
                op = condition["op"]
                val = condition["value"]

                if op == "=":
                    filter_clauses.append(column == val)
                elif op == "!=":
                    filter_clauses.append(column != val)
                elif op == ">":
                    filter_clauses.append(column > val)
                elif op == "<":
                    filter_clauses.append(column < val)
                elif op == ">=":
                    filter_clauses.append(column >= val)
                elif op == "<=":
                    filter_clauses.append(column <= val)

            query = query.filter(and_(*filter_clauses))
            
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
        Extrae pares campo=valor (y variantes) desde la respuesta de OpenAI.
        Soporta múltiples operadores (=, !=, >, <, >=, <=) y valida que los campos existan en ChallengeData.

        Ejemplo:
        "Filtrar donde desc_categoria_producto = 'Ropa' y id_ga_fuente_medio != google y fc_producto_cant >= 5"
        """
        import re
        filters = {}

        # Regex para capturar: campo operador valor
        pattern = re.compile(r"(\w+)\s*(=|!=|>=|<=|<|>)\s*['\"]?([\w\s\-\.\:\,]+?)['\"]?(?=\s|$|y|and)", re.IGNORECASE)

        matches = pattern.findall(response)
        for field, operator, value in matches:
            field = field.strip()
            operator = operator.strip()
            value = value.strip()

            if hasattr(ChallengeData, field):
                filters[field] = {"op": operator, "value": value}

        return filters



'''
        - id_ga_vista: ID de vista
        - id_ga_tipo_dispositivo: ID de tipo de dispositivo
        - desc_ga_sku_producto: SKU del producto
        - fc_retirado_carrito_cant: Cantidad retirada del carrito
        - desc_ga_nombre_producto: Nombre del producto
        - fc_visualizaciones_pag_cant: Cantidad de visualizaciones de página
        - sasasa: Campo SASASA



SELECT
  COUNT(DISTINCT id_tie_fecha_valor) AS id_tie_fecha_valor,
  COUNT(DISTINCT id_cli_cliente) AS id_cli_cliente,
  COUNT(DISTINCT id_ga_vista) AS id_ga_vista,
  COUNT(DISTINCT id_ga_tipo_dispositivo) AS id_ga_tipo_dispositivo,
  COUNT(DISTINCT id_ga_fuente_medio) AS id_ga_fuente_medio,
  COUNT(DISTINCT desc_ga_sku_producto) AS desc_ga_sku_producto,
  COUNT(DISTINCT desc_ga_categoria_producto) AS desc_ga_categoria_producto,
  COUNT(DISTINCT fc_agregado_carrito_cant) AS fc_agregado_carrito_cant,
  COUNT(DISTINCT fc_ingreso_producto_monto) AS fc_ingreso_producto_monto,
  COUNT(DISTINCT fc_retirado_carrito_cant) AS fc_retirado_carrito_cant,
  COUNT(DISTINCT fc_detalle_producto_cant) AS fc_detalle_producto_cant,
  COUNT(DISTINCT fc_producto_cant) AS fc_producto_cant,
  COUNT(DISTINCT desc_ga_nombre_producto) AS desc_ga_nombre_producto,
  COUNT(DISTINCT fc_visualizaciones_pag_cant) AS fc_visualizaciones_pag_cant,
  COUNT(DISTINCT flag_pipol) AS flag_pipol,
  COUNT(DISTINCT "SASASA") AS sasasa,
  COUNT(DISTINCT id_ga_producto) AS id_ga_producto,
  COUNT(DISTINCT desc_ga_nombre_producto_1) AS desc_ga_nombre_producto_1,
  COUNT(DISTINCT desc_ga_sku_producto_1) AS desc_ga_sku_producto_1,
  COUNT(DISTINCT desc_ga_marca_producto) AS desc_ga_marca_producto,
  COUNT(DISTINCT desc_ga_cod_producto) AS desc_ga_cod_producto,
  COUNT(DISTINCT desc_categoria_producto) AS desc_categoria_producto,
  COUNT(DISTINCT desc_categoria_prod_principal) AS desc_categoria_prod_principal
FROM public.challenge_graphql_nlp_api;'''