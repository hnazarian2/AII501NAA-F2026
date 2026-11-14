# Linear Regression Exercise — Questions and Answers

## 1. What is the target variable, and what are the input features? Why is this regression rather than classification?

The target variable is **`FARE`**, the taxi fare in dollars. The dataset includes **`TRIP_MILES`** (distance) and **`TRIP_MINUTES`** (duration) as potential input features. The basic experiment uses `TRIP_MILES` to predict the fare. This is a **regression** problem because the output is a numerical amount, not a category or class.

## 2. Why split data into training and test sets? What happens if we test on the training data?

Training data is used to fit the model, while test data provides an independent check on how it predicts **unseen** examples. Evaluating only on the training data can produce an overly optimistic and or exaggerated result because the model has already learned from those observations. A low training error does not guarantee good performance on new trips.

## 3. What does MAE or MSE measure? Report your model's value and explain it in plain words.

**Mean Absolute Error (MAE)** averages the absolute differences between predicted and observed values. **Mean Squared Error (MSE)** averages squared differences, so larger mistakes count more heavily. In Google's exercise **Root Mean Squared Error (RMSE)** is the square root of MSE.

My model's reported **RMSE was 3.7458 (approximately $3.75)**. This means the root mean square of its fare-prediction errors was about $3.75. It is **not** the same as an MAE of $3.75. This is the reported exercise metric.

## 4. Where does the model do well and where does it struggle?

In the displayed predictions, most fares were fairly close to their observed values. For example, one trip had a predicted fare of **$41.80** versus an observed **$42.00** (an absolute error of **$0.20**). However, the model also made some substantial errors: one trip was predicted at **$14.47** but actually cost **$32.85**, a difference of **$18.38**. Thus, the model captures the general relationship but struggles with some unusual or less well-explained trips. Distance alone may not explain every fare.

## 5. Change one setting. What changed in the results, and why?

I ran an experiment using **50 epochs**, a **learning rate of 0.001**, and a **batch size of 50**. The reported RMSE remained **3.7458**. This suggests the extra training did not noticeably improve the displayed metric, potentially because the model was already near convergence. This conclusion assumes the other settings and data were kept the same; if they differed from the baseline, the comparison would not isolate the effect of epochs.

## 6. Which feature seems most important, and how did you decide?

**`TRIP_MILES`** appears especially important for predicting taxi fare: the model uses distance as an input, and longer rides generally cost more. The exercise's exploration of fare relationships also supports this choice. However, this is a qualitative judgment, **not a formal feature-importance result**. To establish which feature contributes most among multiple inputs, I would compare models or use an appropriate feature-importance method.

## 7. What is the difference between classification and regression? Give an example of each.

**Regression** predicts a numeric value, such as how many hours I might need to finish a programming assignment. **Classification** predicts a category, such as whether an incoming email is spam or not spam.

## 8. What could go wrong if the model were deployed in the real world?

Missing or inaccurate trip information could cause incorrect fare estimates. The training data might also underrepresent certain neighborhoods, trip types, or time periods, causing uneven performance. Changes in traffic, pricing rules, or rider behavior could make predictions less reliable over time. The model would need data-quality checks, evaluation on new and representative trips, monitoring, and periodic retraining.
