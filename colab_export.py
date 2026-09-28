# Paste this into a NEW cell at the END of your Colab notebook and run it.
# Replace `model`, `scaler`, and `X` with your own variable names.
import joblib
from google.colab import files

joblib.dump(model, "wine_model.pkl")      # your trained model
files.download("wine_model.pkl")

# Only if you scaled the features (StandardScaler / MinMaxScaler) before training:
# joblib.dump(scaler, "scaler.pkl")
# files.download("scaler.pkl")

print(list(X.columns))   # <- check this matches FEATURES in app.py
print(type(model))
