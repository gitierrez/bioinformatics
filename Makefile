test:
	pytest --cov=biomics --cov-report=term-missing tests/

kmers:
	streamlit run apps/kmers.py