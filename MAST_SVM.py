import json
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import pearsonr
from collections import defaultdict
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.metrics import precision_score, recall_score

# --- Open Files & Setup ---
# Initialize separate variables
melodyIndexTrain = defaultdict(dict)
RefSegsTrueTrain = defaultdict(dict)
PerSegsTrueTrain = defaultdict(dict)
PerSegsFalseTrain = defaultdict(dict)
melodyIndexTest = defaultdict(dict)
RefSegsTrueTest = defaultdict(dict)
PerSegsTrueTest = defaultdict(dict)
PerSegsFalseTest = defaultdict(dict)

# -- Import Json Files --
# array of json files, split into training and testing at around 80-20 %
json_files_training = ["511.json","512.json","521.json","522.json","531.json","532.json","541.json","542.json","551.json","552.json","561.json","562.json","571.json","572.json","581.json","582.json","5101.json","5102.json","611.json","612.json","621.json","622.json","631.json","632.json","641.json","642.json","651.json","652.json","661.json","662.json"]
json_files_testing = ["671.json","672.json","681.json","682.json", "691.json", "692.json", "6101.json","6102.json"]
index = 0
for filenum in json_files_training:	# open json files for training
    with open(filenum, 'r') as file:
        data = file.read()
        # Make a dictionary with keys: melodyIndex | RefSegsTrue | PerSegsTrue | PerSegsFalse
        this_dict = json.loads(data)
        # Extract data from json fileinto separate variables
        melodyIndexTrain[index] = this_dict['melodyIndex']
        RefSegsTrueTrain[index] = this_dict['RefSegsTrue']
        PerSegsTrueTrain[index] = this_dict['PerSegsTrue']
        PerSegsFalseTrain[index] = this_dict['PerSegsFalse']
        index = index + 1

index1 = 0
for filenum in json_files_testing:	# open json files for testing
    with open(filenum, 'r') as file:
        data = file.read()
        # Make a dictionary with keys: melodyIndex | RefSegsTrue | PerSegsTrue | PerSegsFalse
        this_dict = json.loads(data)
        # Extract data from json fileinto separate variables
        melodyIndexTest[index1] = this_dict['melodyIndex']
        RefSegsTrueTest[index1] = this_dict['RefSegsTrue']
        PerSegsTrueTest[index1] = this_dict['PerSegsTrue']
        PerSegsFalseTest[index1] = this_dict['PerSegsFalse']
        index1 = index1 + 1


# -- Support Vector Machine --
# initialize lists
xtrue = []
xfalse = []
ytrue = []
yfalse = []
xtrue_test = []
xfalse_test = []
ytrue_test = []
yfalse_test = []

# iterate through TRAINING data. x is input features, y is 0 or 1 pass/fail
for i in PerSegsTrueTrain:
    xtrue = xtrue + PerSegsTrueTrain[i]
    ytrue = ytrue + list(np.ones(len(PerSegsTrueTrain[i]), dtype=int))

for i in PerSegsFalseTrain:
    xfalse = xfalse + PerSegsFalseTrain[i]
    yfalse = yfalse + list(np.zeros(len(PerSegsFalseTrain[i]), dtype=int))

# iterate throught TESTING data. x is input features, y is 0 or 1 pass/fail
for i in PerSegsTrueTest:
    xtrue_test = xtrue_test + PerSegsTrueTest[i]
    ytrue_test = ytrue_test + list(np.ones(len(PerSegsTrueTest[i]), dtype=int))

for i in PerSegsFalseTest:
    xfalse_test = xfalse_test + PerSegsFalseTest[i]
    yfalse_test = yfalse_test + list(np.zeros(len(PerSegsFalseTest[i]), dtype=int))


#finalize test and train variables
X_train = xtrue + xfalse
y_train = ytrue + yfalse
X_test = xtrue_test + xfalse_test
y_test = ytrue_test + yfalse_test

# -- SVM Classifier --
svclassifier = SVC(kernel = 'poly', degree = 3)
svclassifier.fit(X_train, y_train)

y_pred = list(svclassifier.predict(X_test))


# -- Visualize Results --
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))

print("Precision score: {}".format(precision_score(y_test,y_pred))) # precision is accuracy of positive predictions
print("Recall score: {}".format(recall_score(y_test,y_pred))) # fraction of positives that were correct

