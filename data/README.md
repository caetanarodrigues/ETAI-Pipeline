# Dataset -- COMPAS Recidivism (ProPublica)

# 20260639 Caetana Rodrigues 

## Pipeline progress

Week 3: changed the preprocessing doc - added a clean data set function to clean our data
Week 4: changed the prepocessor function
Week 4 update: added the crossvalidation 
Week 5: added hyperparameter tuning 
Week 6: added two new models - oblique random forest and adaboost
Week 7: added Gradient Boosting, HistGradientBoosting and Naive Bayes; 8 metrics from out-of-fold probabilities; ROC-AUC as the selection metric; scoreboard in `results/runs.csv` with the no-model floor and untuned score per run

## Preprocessing decisions

## Best Model 

### Week 2 
--> logistic regression: 
Train accuracy: 0.680
Test accuracy:  0.678
Gap (train - test): +0.002

--> decision tree:
Train accuracy: 0.829
Test accuracy:  0.627
Gap (train - test): +0.202

--> Analysis: The best model is the logistic regression since the test accuracy is better than the decision tree. We can also see that the decision tree has a problem of overfitting, the train accuracy is much better than the test accuracy. 

### Week 3
--> logistic regression:
Train accuracy: 0.678
Test accuracy:  0.655
Gap (train - test): +0.023
    > The test accuracy dropped from 0.678 to 0.655. The gap between the training and test sets increased slightly from +0.002 to +0.023, indicating a minor loss in generalization.

--> decision tree:
Train accuracy: 0.799
Test accuracy:  0.603
Gap (train - test): +0.197
    > The test accuracy also declined, dropping from 0.627 to 0.603. Train accuracy fell from 0.829 to 0.799, reducing the gap from +0.202 to +0.197. Although the severe overfitting issue persists.

--> Analysis: The best model is the logistic regression, as its test accuracy (0.655) outperforms the decision tree (0.603). The decision tree continues to suffer from significant overfitting, demonstrated by a train accuracy (0.799) that remains much higher than its test accuracy (0.603).

### Week 4 (Without CV)
--> logistic regression: (max_iter = 2000 instead of 1000)
Train accuracy: 0.676
Test accuracy:  0.658
Gap (train - test): +0.018
    > with this week's encoder/scaler pair in place, 1000 iterations was cutting lbfgs off before it converged (a ConvergenceWarning, not a real problem,but worth just giving it enough room rather than living with the warning). The test accuracy improved slightly from 0.655 to 0.658. The gap between the training and test sets decreased from +0.023 to +0.018, indicating better generalization with the increased max_iter.

--> decision tree:
Train accuracy: 0.686
Test accuracy:  0.596
Gap (train - test): +0.090
    > The overfitting issue was significantly reduced, with the gap dropping from +0.197 to +0.090. However, this came at the cost of overall performance, as train accuracy fell from 0.799 to 0.686 and test accuracy decreased slightly from 0.603 to 0.596.

--> dummy:
Train accuracy: 0.549
Test accuracy:  0.550
Gap (train - test): -0.001

--> random_forest:
Train accuracy: 0.736
Test accuracy:  0.638
Gap (train - test): +0.097

--> Analysis: The best model is the logistic regression, as its test accuracy (0.658) is the highest among all models, outperforming the random forest (0.638), the decision tree (0.596), and the dummy baseline (0.550). It also shows excellent generalization, maintaining the smallest gap between train and test accuracy (+0.018).

### Week 5 (With CV now)
Did not run it before doing week 6

### Week 6
| Model | Default: CV mean ± std (gap) | Tuned: nested CV mean ± std (gap) | Tuning score (best trial) | Chosen hyperparameters |
|---|---|---|---|---|
| Logistic regression | 0.672 ± 0.013 (+0.003)  | — | — | — |
| Decision tree | 0.611 ± 0.015 (+0.084) | 0.675 ± 0.020 (+0.009) | 0.680 | 'model__max_depth': 9, 'model__min_samples_leaf': 101, 'model__criterion': 'gini' |
| Random forest | 0.652 ± 0.017 (+0.080) | 0.680 ± 0.015 (+0.009) | 0.682 | 'model__max_depth': 19, 'model__min_samples_leaf': 16, 'model__max_features': 'sqrt' |
| Oblique random forest | 0.650 ± 0.009 (+0.113) | 0.682 ± 0.014 (+0.011)  | 0.683 | 'model__estimator__tree__max_depth': 4, 'model__estimator__tree__min_samples_leaf': 2, 'model__estimator__project__n_components': 10 |
| AdaBoost | 0.676 ± 0.012 (+0.006) | 0.682 ± 0.016 (+0.005) | 0.684 | 'model__estimator__max_depth': 4, 'model__n_estimators': 220, 'model__learning_rate': 0.025081156860452335 |

--> Analysis: Th best model is the AdaBoost, because it has the highest tuned score (nested CV 0.682 ± 0.016, tied with the oblique random forest) and a very small train/validation gap (+0.005). However, its lead is not bigger than the fold-to-fold std: it is only 0.007 above the decision tree and 0.002 above the random forest, while the std is 0.014-0.020, so the four tuned models are statistically tied. The chosen hyperparameters match how each model works. The single decision tree needs big leaves (101) to stay smooth, and the random forest can afford deeper trees (19) because averaging reduces variance. The oblique forest ended up shallow (depth 4) because each split uses a random projection of up to 10 features and is already more expressive, and AdaBoost picked a low learning rate (0.025) with 220 trees, so each small step corrects the previous errors without overfitting. I would report 0.682 ± 0.016, the nested CV score, rather than the 0.684 best-trial score, because the latter is the maximum over 30 trials and therefore optimistic.

### Week 7
Selection metric: ROC-AUC · 5-fold stratified CV (same folds for every run) · tuned = nested CV, 30 Optuna trials

| Model | Untuned | Tuned (nested) ± std | Floor |
|---|---|---|---|
| Gradient boosting | 0.727 | 0.728 ± 0.014 | 0.500 |
| HistGradientBoosting | 0.717 | 0.728 ± 0.015 | 0.500 |
| Oblique random forest | 0.686 | 0.727 ± 0.015 | 0.500 |
| AdaBoost | 0.723 | 0.727 ± 0.014 | 0.500 |
| Random forest | 0.683 | 0.726 ± 0.013 | 0.500 |
| Logistic regression | 0.719 ± 0.014 | — | 0.500 |
| Decision tree | 0.605 | 0.718 ± 0.015 | 0.500 |
| Naive Bayes | 0.685 | 0.705 ± 0.012 | 0.500 |
| Dummy | 0.500 | — | 0.500 |

--> Selection metric: I chose ROC-AUC. COMPAS is a risk score used to rank defendants by how likely they are to reoffend, and ROC-AUC measures that ranking across all thresholds. Choosing the threshold, and so the trade-off between false positives and missed reoffenders, is a separate decision that shouldn't be made inside model selection. ROC-AUC is also less noisy than accuracy for comparing models, so the corrected t-test can actually separate them.

## The problem

In 2016, ProPublica investigated COMPAS, a risk-assessment algorithm
actually used by courts in Broward County, Florida, to help inform
bail and sentencing decisions. COMPAS scores a defendant's likelihood
of reoffending on a 1-10 scale; judges could see that score when
deciding, among other things, whether someone should be released
before trial. ProPublica obtained COMPAS's scores for thousands of
defendants and matched them against what actually happened over the
following two years, then published the data.

This dataset is that data: each row is one defendant, with their
demographics and criminal history at the time of screening, COMPAS's
own risk score for them, and whether they were actually rearrested
within two years.

**Your task:** predict `two_year_recid` -- will this person be
rearrested within two years? -- from the case facts. Once you have a
model, the more interesting question is the one ProPublica actually
asked: is it equally accurate for everyone, or does it get things
wrong more often, in a particular direction, for some groups than
others? `race` is deliberately excluded from the model's own inputs
(see `config.yaml` and `src/preprocessing.py`) so it can be used
afterward purely to check this, in `src/evaluate.py`.

Before any of that: look at the data first. It comes from a real
system with real data-entry and record-keeping quirks -- don't assume
every column is clean or consistent just because it loads without
error.

## Data dictionary

| column | type | description | notable values |
|--------|------|--------------|------------------|
| `id` | identifier | internal record id | not a model feature |
| `sex` | categorical | defendant's sex | `Male`, `Female` |
| `age` | numeric | defendant's age (years) at screening | |
| `age_cat` | categorical | age bucket | `Less than 25`, `25 - 45`, `Greater than 45` |
| `race` | categorical | defendant's race, as recorded | `African-American`, `Caucasian`, `Hispanic`, `Asian`, `Native American`, `Other`; excluded from model features, used only to audit fairness |
| `juv_fel_count` | numeric | number of prior juvenile felony offenses | |
| `juv_misd_count` | numeric | number of prior juvenile misdemeanor offenses | |
| `juv_other_count` | numeric | number of other prior juvenile offenses | |
| `juvenile_total` | numeric | total juvenile offenses | |
| `priors_count` | numeric | number of prior adult offenses | |
| `prior_offenses` | numeric | number of prior offenses | |
| `age_in_months` | numeric | age expressed in months | |
| `c_charge_degree` | categorical | degree of the current charge | `F` (felony), `M` (misdemeanor) |
| `decile_score` | numeric | COMPAS's own risk score | 1 (lowest risk) to 10 (highest risk); excluded from model features, used only for comparison |
| `score_text` | categorical | COMPAS's own risk category | `Low`, `Medium`, `High`; excluded from model features, used only for comparison |
| `two_year_recid` | binary | **target** -- was this person rearrested within two years? | `0` = no, `1` = yes |

Source: derived from [propublica/compas-analysis](https://github.com/propublica/compas-analysis) (the data behind the "Machine Bias" investigation). Personally-identifying columns (name, date of birth, case numbers, charge descriptions) were removed.
