# scikit_learn_estimator_structure

In scikit-learn, the model structure follows a very consistent object-oriented design based on *estimators*. An estimator is any object that learns from data—it could be a classifier, regressor, transformer, or pipeline. All estimators implement a common API: you initialize them with parameters (no data), fit them to data with `.fit()`, and then use `.predict()` (for supervised models), `.transform()` (for transformers), or `.predict_proba()` (for probabilistic outputs). This API lets you chain models together and work in a consistent way regardless of the underlying algorithm.

Internally, an estimator class has a defined `__init__()` that stores the hyperparameters you provide. When you call `.fit(X, y)`, the object learns from the data and stores results in attributes ending in an underscore, such as `coef_` or `feature_importances_`. These attributes are then used in `.predict()` or `.transform()`. Importantly, the structure is stateless across function calls: `.fit()` returns `self` so you can chain calls, but each call builds or updates the model in-place.

Because the structure is standardized, scikit-learn makes it easy to combine models in `Pipeline`, tune hyperparameters with `GridSearchCV` or `RandomizedSearchCV`, and do cross-validation with tools like `cross_val_score`. The core idea is that an estimator is a plain Python object with consistent method names and attributes that you can mix and match across different tasks.

This project aims to create methods that look a lot like scikit-learn ways of doing things.
