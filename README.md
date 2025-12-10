# DSS Autism

A Decision Support System (DSS) to help analyze screening and assessment data related to Autism Spectrum Disorder (ASD). This repository contains code, data handling utilities, model training scripts, and documentation to support research and clinical workflows.

## About
DSS Autism is intended to assist practitioners and researchers by providing reproducible pipelines for:
- Preprocessing screening and assessment data
- Feature engineering and exploratory analysis
- Training and evaluating interpretable models
- Exporting results and simple visualizations for reporting

## Prerequisites
- Git
- Python 3.8+ (recommended) or a supported runtime
- Common Python packages: pandas, scikit-learn, numpy, matplotlib, seaborn
- Optional: Jupyter Notebook / JupyterLab for exploration

## Installation
Clone the repository and create an isolated environment:
```bash
git clone <repo-url> DSS-Autism
cd "DSS-Autism"
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
pip install -r requirements.txt
```

If requirements.txt is not present, install common packages:
```bash
pip install pandas scikit-learn numpy matplotlib seaborn jupyter
```