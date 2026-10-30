# epex-forecast

Simple forecast for the EPEX day-ahead morning auction (GB, GBP/MWh).

## Overview

This repo creates a one-off forecast for the EPEX day-ahead auction for **30/10/2026**. In practice I'd want the model to be fully online, updating daily, but due to constraints in finding EPEX price data it instead makes a one-off forecast for the required date.

### Approach

Given the two days available to complete this project and the need to use open-source data, the models used are relatively simple, and most design choices are standard. The rationale is that any model is limited by the data it is trained on: a ridge regression with good data will perform better than an LSTM on rubbish data.

## File outline

```
epex-forecast/
├── data/
│   ├── raw/
│   └── processed/
├── helpers/
│   ├── utils
│   └── fetch_data
├── models/
│   ├── baselines.ipynb
│   ├── ridge.ipynb
│   └── ridge.joblib
├── .gitignore
├── EDA.ipynb
└── forecast.ipynb
```

## Raw datasets

All files live in `data/raw/`.

- **`DCOILBRENTEU.csv`**: sourced from [FRED](https://fred.stlouisfed.org/series/DCOILBRENTEU). Price of Brent crude oil in Europe. We use D-3 prices to predict D prices.
- **`EURO_GBP_rates.csv`**: sourced from the Bank of England. Needed to convert EUR/MWh to GBP/MWh for some datasets.
- **`daily_SAP_gas_prices.csv`**: sourced from [National Gas](https://data.nationalgas.com/reports/gas-day-summary) and the [ONS](https://www.ons.gov.uk/economy/economicoutputandproductivity/output/datasets/systemaveragepricesapofgas). Again we use D-3 to predict D prices; it is tricky to do better with open-source data while keeping historical prices consistent with fresh open-source prices.
- **`dayahead_demand.csv`**: sourced from the [NESO 1-day ahead demand forecast](https://www.neso.energy/data-portal/1-day-ahead-demand-forecast). Pulled on the morning of the forecast, so we use their forecast as an input to ours.
- **`dayahead_wind.csv`**: sourced from the [NESO day-ahead wind forecast](https://www.neso.energy/data-portal/day-ahead-wind-forecast). Same as above.
- **`United_Kingdom.csv`**: sourced from [Ember](https://ember-energy.org/data/european-wholesale-electricity-price-data/). Historical day-ahead wholesale electricity prices from 2016 to early October 2026. Day-ahead prices for day D-1 are set on D-2, so prices for D-1 can safely be used to predict prices on day D. This is not explicitly the EPEX day-ahead price, but it aligns closely (checked via a free trial of paid services).
- **`prices_2026-10-30.csv`**: EPEX price data from the 29/10/26 auction. Manually created from a free trial of a paid data product.

## Results

| Model | RMSE (GBP/MWh) |
|---|---|
| Previous-day baseline | ~30 |
| Ridge regression | ~17.5 |

## Limitations and next steps

- One-off forecast rather than an online model updated daily
- Brent and SAP gas prices are lagged by three days because of open-source data availability
- Ember prices are a close proxy for, not identical to, EPEX prices
