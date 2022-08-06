test:
	pytest --cov=biomics tests/

kmers:
	streamlit run apps/kmers.py