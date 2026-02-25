# Wildsur X-Ray Agent

Agente de ejemplo para ejecutar búsquedas **Google X-Ray** orientadas a
reclutamiento/due diligence y volcar resultados en:

- Google Sheets
- Archivo Excel (`.xlsx`) en Google Drive

## Qué hace

- Construye queries X-Ray (`site:`, `intitle:`, `inurl:`, booleanos).
- Busca candidatos/empresas con `google_search`.
- Estructura resultados en un pipeline tabular.
- Crea/actualiza hojas en Sheets.
- Puede crear un XLSX y subirlo a Drive.

## Estructura del agente

Cumple la convención de ADK:

- `__init__.py` contiene `from . import agent`
- `agent.py` define `root_agent`

## Cómo ejecutarlo

```bash
adk run contributing/samples/wildsur_xray_agent
```

o en UI:

```bash
adk web contributing/samples
```

## Requisitos de autenticación

El agente usa `SheetsToolset` y `GoogleApiToolset("drive", "v3")`, por lo
que debes configurar autenticación para Google APIs (OAuth o service account)
con permisos de Drive y Sheets antes de usar exportación.
