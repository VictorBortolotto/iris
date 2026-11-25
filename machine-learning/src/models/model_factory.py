
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

def create_models():

  return {
    "KNN": Pipeline([
      ("scaler", StandardScaler()),
      ("model", KNeighborsClassifier())
    ]),

    "Decision Tree": Pipeline([
      ("scaler", "passthrough"),
      ("model", DecisionTreeClassifier(
        random_state=42
      ))
    ]),

    "Naive Bayes": Pipeline([
      ("scaler", "passthrough"),
      ("model", GaussianNB())
    ]),

    "SVM": Pipeline([
      ("scaler", StandardScaler()),
      ("model", SVC(probability=True))
    ])
  }
