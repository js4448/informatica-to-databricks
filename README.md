# Informatica → Databricks converter

This project converts Informatica workflow/mapping XML files into Databricks-ready PySpark code (notebooks or .py files) and provides a small CLI and deployment helper for uploading to a Databricks workspace.

Quick start

1. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Generate notebooks from a sample XML:

```bash
python -m informatica_to_databricks.cli generate --input tests/samples/sample_mapping.xml --out generated
```

3. Upload generated files to Databricks (example using env vars):

```bash
export DATABRICKS_HOST=https://<your-workspace>
export DATABRICKS_TOKEN=<your-token>
python -m informatica_to_databricks.deploy --src generated --target /Users/you/generated
```

See `README.md` and the code for more details.
