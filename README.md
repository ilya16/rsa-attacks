# Analysis of attacks on RSA
Simple analysis of attacks on RSA in Python.

Analyzed attacks:
* Fermat Factorization for close numbers `p` and `q`
* Hastad's Broadcast Attack for Low Public exponent `e`

See [notebook](rsa-analysis.ipynb) for the results of the analysis.

## Setup

Install reqirements using:
```
pip install -r requirements
```

Run Fermat Factorization experiments using:
```
python fermat_test.py
```

Test Hastad's Broadcast attack using:
```
python hastads_test.py
```