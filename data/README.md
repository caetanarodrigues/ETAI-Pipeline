# Dataset -- COMPAS Recidivism (ProPublica)

# 20260639 Caetana Rodrigues 

## Pipeline progress

Week 3: changed the preprocessing doc - added a clean data set function to clean our data
Week 4: changed the prepocessor function

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

### Week 4
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
