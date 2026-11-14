# Chicago Taxi Fare Prediction — Linear Regression

## Overview

This repository documents my work with Google's **Machine Learning Crash Course — Linear Regression** programming exercise. The goal is to explore Chicago taxi-trip data, train a regression model to predict taxi fares, and examine how training settings influence prediction error.

**Exercise:** https://developers.google.com/machine-learning/crash-course/linear-regression/programming-exercise

The answers to the assignment's eight questions are in **[ANSWERS.md](ANSWERS.md)**.

## Environment and setup

The exercise runs in **Google Colab** (a browser-based Jupyter notebook), so a local Python or Jupyter installation is not required.

1. Open the exercise from the Google Machine Learning Crash Course page in Google Colab.
2. Sign in to Google if prompted, and connect to a Colab runtime.
3. Run the notebook's library-installation section before importing its dependencies.
4. If the notebook reports `ModuleNotFoundError: No module named 'ml_edu'`, check the package with:

   ```python
   %pip show google-ml-edu
   ```

   If missing, install the version used in the exercise:

   ```python
   %pip install google-ml-edu==0.1.3
   ```

5. Run the notebook's setup and function-definition cells in order. In particular, `create_model()` and `train_model()` must be defined before the experiment cells run.

> Package versions and notebook cells may change. Prefer the requirements provided by the notebook when they differ from the troubleshooting command above.

## Execution instructions

1. Run the dependency and data-loading cells.
2. Explore the taxi data and identify the target (`FARE`) and available predictors, including `TRIP_MILES` and `TRIP_MINUTES`.
3. Run the model-function definition cells.
4. Run **Experiment 1**, noting the RMSE graph and predicted-versus-observed fare results.
5. Run the modified experiment with **50 epochs**, **learning rate 0.001**, and **batch size 50**.
6. Compare the reported metrics and record observations in [ANSWERS.md](ANSWERS.md).

## Testing and evaluation

The notebook provides an RMSE training/evaluation plot and sample predictions with observed fares and L1 (absolute) errors.

- **Reported Experiment 1 RMSE:** `3.7458`
- **Reported modified-experiment RMSE:** `3.7458`
- **Example close prediction:** predicted `$41.80`, observed `$42.00`, absolute error `$0.20`
- **Example large miss:** predicted `$14.47`, observed `$32.85`, absolute error `$18.38`

**Important limitation:** These are the results reported from the exercise. A separate held-out **test-set** metric has **not** been verified. To evaluate real-world generalization, the model should also be measured on data not used during training, ideally with a suitable train/test split and consistent preprocessing.

## Assumptions and limitations

- Taxi fare is a continuous numerical target, so regression is appropriate.
- Trip distance is an important predictor, but other factors (such as trip duration, traffic, and pricing details) may influence fares.
- The reported error metrics come from the user's Colab execution, not an independently reproduced run.
- The statement that extra epochs did not improve RMSE assumes that the baseline and modified runs used the same data and other relevant settings; the original epoch count has not been independently confirmed.
- Colab package installation may require troubleshooting, and notebook cells must run in dependency order.
- The exercise should not be treated as a production-ready fare estimator without an independent evaluation and checks for data quality and distribution changes.

## Repository contents

- `ANSWERS.md` — responses to assignment questions 1–8.
- `README.md` — project overview, setup, execution, testing, and assumptions.
- Google Colab notebook (`.ipynb`) — **add your completed notebook to the repository if required by your instructor**.
