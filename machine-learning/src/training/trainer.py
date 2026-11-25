
from sklearn.model_selection import GridSearchCV, StratifiedKFold

def train_models(models, param_grids, X_train, y_train):

  cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
  )

  best_models = {}
  cv_results = {}

  for name, pipeline in models.items():

    grid = GridSearchCV(
      estimator=pipeline,
      param_grid=param_grids[name],
      cv=cv,
      scoring="accuracy",
      n_jobs=-1
    )

    grid.fit(X_train, y_train)

    best_models[name] = grid.best_estimator_
    cv_results[name] = {
      "accuracy": grid.best_score_,
      "parameters": grid.best_params_
    }

  return best_models, cv_results
