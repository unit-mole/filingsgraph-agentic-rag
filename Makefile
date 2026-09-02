PYTHON ?= python
setup:
	$(PYTHON) -m pip install -U pip
	$(PYTHON) -m pip install -e ".[dev]"

data:
	$(PYTHON) -m scripts.resolve_companies
	$(PYTHON) -m scripts.download_filings
	$(PYTHON) -m scripts.download_companyfacts
	$(PYTHON) -m scripts.validate_data
	$(PYTHON) -m scripts.build_documents
	$(PYTHON) -m scripts.build_database

index:
	$(PYTHON) -m scripts.build_index

graph:
	$(PYTHON) -m scripts.build_graph

eval:
	$(PYTHON) -m scripts.build_eval_set
	$(PYTHON) -m scripts.evaluate_all

app:
	$(PYTHON) app/gradio_app.py

test:
	pytest

all:
	$(PYTHON) -m scripts.run_pipeline --stage all
