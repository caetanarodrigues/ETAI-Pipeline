import pandas as pd
from src.evaluate import corrected_paired_test

runs = pd.read_csv("results/runs.csv", dtype={"run": str})
folds = [f"fold_{i}" for i in range(1, 6)]

# the two tuned XGBoost runs: the last one with selection and the last one without
xgb = runs[(runs["model"] == "xgboost") & (runs["tuned"] == True)]
with_sel = xgb[xgb["feature_selection"] != "off"].iloc[-1]
without = xgb[xgb["feature_selection"] == "off"].iloc[-1]

print(f"with selection    ({with_sel['run']}): {with_sel['mean']:.3f} ± {with_sel['std']:.3f}")
print(f"without selection ({without['run']}): {without['mean']:.3f} ± {without['std']:.3f}")

n_splits = len(folds)
result = corrected_paired_test(with_sel[folds].astype(float), without[folds].astype(float),
                               test_train_ratio=1 / (n_splits - 1))
print(result)