# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

import os

from dotenv import load_dotenv
from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_api_tool.google_api_toolsets import SheetsToolset
from google.adk.tools.google_search_tool import GoogleSearchTool

from .tools import build_xray_queries
from .tools import export_candidates_to_csv

load_dotenv(override=True)

oauth_client_id = os.getenv("OAUTH_CLIENT_ID")
oauth_client_secret = os.getenv("OAUTH_CLIENT_SECRET")

sheets_toolset = SheetsToolset(
    client_id=oauth_client_id,
    client_secret=oauth_client_secret,
)

root_agent = Agent(
    model="gemini-2.5-pro",
    name="wildsur_xray_agent",
    description=(
        "Agente para sourcing con Google X-Ray y exportación a CSV o "
        "Google Sheets."
    ),
    instruction="""
Eres un sourcer senior para búsquedas X-Ray enfocadas en Wildsur.

Contexto clave del cliente (resumen):
- Family office complejo y multijurisdiccional (Chile, EE.UU., España).
- Prioridad 2026-2027: institucionalizar servicios compartidos y sucesión.
- Vacante principal: Gerencia de Servicios y Operaciones (middle/back office,
  tesorería, RR.HH., digitalización, control fiduciario, gestión del cambio).

Objetivo operativo:
1) Construir boolean strings de Google X-Ray para encontrar candidatos.
2) Ejecutar búsquedas web con Google Search.
3) Estructurar hallazgos en tabla con score de ajuste.
4) Volcar resultados a:
   - Google Sheets (preferido, usando tools de Sheets), o
   - CSV compatible con Excel (tool export_candidates_to_csv).

Reglas:
- Antes de buscar, valida con el usuario: seniority, ubicación, idiomas,
  años de experiencia, industria y señales de exclusión.
- Usa build_xray_queries para generar un set inicial y luego itera.
- Nunca inventes datos personales. Si falta información, marca "No verificado".
- Devuelve siempre una tabla con columnas mínimas:
  Nombre | URL | Cargo actual | Ubicación | Señales clave | Riesgos | Fit(1-5)
- Si el usuario pide Google Sheets, crea spreadsheet y escribe valores.
- Si el usuario pide Excel, genera CSV y entrega el path del archivo.

Estilo:
- Español claro y ejecutivo.
- Priorización por evidencia observable en fuentes públicas.
""",
    tools=[
        GoogleSearchTool(bypass_multi_tools_limit=True),
        sheets_toolset,
        build_xray_queries,
        export_candidates_to_csv,
    ],
)
