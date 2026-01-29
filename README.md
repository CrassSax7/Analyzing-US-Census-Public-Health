# Analyzing US Census and Public Health Data to Support Policy Decisions

**Author:** J. Casey Brookshier  
**Date:** July 31, 2025  

## Objective
Evaluate whether median household income is significantly correlated with obesity
rates in the United States using Census and CDC public health data.

## Research Question
**Is median household income significantly correlated with obesity rates?**

## Data Sources
- American Community Survey (ACS) 2019 – Median household income
- CDC BRFSS (LLCP) 2019 – Body Mass Index (BMI)
- US Census Bureau – County boundaries (used during processing)

Only cleaned, analysis-ready datasets are included in this repository.

## Methodology
1. Cleaned ACS income data at the county level
2. Aggregated BRFSS BMI data to the state level
3. Merged datasets into a unified analytical file
4. Conducted:
   - Pearson correlation test
   - Ordinary Least Squares (OLS) regression
5. Visualized results using regression plots

## Key Results
- **Pearson correlation:** -0.303
- **p-value:** 5.09e-69
- **Conclusion:** Median household income is significantly and negatively correlated with obesity rates.

## How to Run
```bash
git clone https://github.com/yourusername/Analyzing-US-Census-Public-Health.git
cd Analyzing-US-Census-Public-Health
pip install -r requirements.txt
python scripts/analysis.py

git clone git@github.com:CrassSax7/hospital_readmission_forecasting.git
cd hospital_readmission_forecasting
pip install -r requirements.txt
python src/prepare_data.py
python src/train_readmissions_model.py




