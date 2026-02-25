# Wildsur X-Ray Agent

Agente de ejemplo para hacer sourcing con búsquedas Google X-Ray y exportar
resultados a Google Sheets o a CSV (compatible con Excel).

## Qué hace

- Construye búsquedas booleanas tipo X-Ray para perfiles en LinkedIn.
- Ejecuta búsquedas web con `google_search`.
- Estructura resultados en una tabla para priorizar candidatos.
- Exporta resultados a:
  - Google Sheets mediante `SheetsToolset`.
  - CSV local con `export_candidates_to_csv`.

## Estructura

```text
wildsur_xray_agent/
├── __init__.py
├── agent.py
└── tools.py
```

## Requisitos

1. Variables de entorno para Google API OAuth:

```bash
export OAUTH_CLIENT_ID="..."
export OAUTH_CLIENT_SECRET="..."
```

2. Dependencias instaladas (en entorno del repo):

```bash
uv sync --all-extras
```

## Ejecución

Desde la raíz del repositorio:

```bash
adk run contributing/samples/wildsur_xray_agent
```

## Ejemplos de prompts

- "Busquemos 15 candidatos para Gerencia de Servicios y Operaciones en Chile,
  con experiencia en tesorería centralizada, RR.HH. y ERP."
- "Genera un shortlist y súbelo a Google Sheets con ranking de fit."
- "Exporta el shortlist a un CSV llamado `wildsur_shortlist.csv`."
