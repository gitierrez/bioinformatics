test:
	pytest --cov=biomics --cov-report=term-missing tests/

genome-locator:
	streamlit run apps/genome_locator.py