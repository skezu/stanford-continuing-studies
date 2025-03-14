import pandas as pd
from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)

# Global variables to hold model and training info
MODEL_PATH = "churn_model.joblib"
model = joblib.load(MODEL_PATH)
print("Model loaded successfully.")

# Recreate training info (numeric features and training columns) by reprocessing the training CSV.
# This is used to clean new data before prediction.
training_df = pd.read_csv("WA_Fn_UseC__Telco_Customer_Churn.csv")
training_df['TotalCharges'] = pd.to_numeric(training_df['TotalCharges'], errors='coerce')
training_df = training_df.dropna()

# Get training columns (features) excluding the target.
target = 'Churn'
training_columns = [col for col in training_df.columns if col != target]
# Determine which columns are numeric in training.
numeric_features = training_df[training_columns].select_dtypes(include=[float, int]).columns.tolist()

@app.route('/predict', methods=['POST'])
def predict():
    """
    Expects a CSV file uploaded under key "file" containing new data with the same feature columns as used during training.
    Performs cleaning on numeric columns (converting strings to numbers and dropping rows with invalid values).
    Returns predictions in JSON format.
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided. Please upload a CSV file with key "file".'}), 400

    file = request.files['file']
    try:
        data = pd.read_csv(file)
    except Exception as e:
        return jsonify({'error': f'Failed to read CSV file: {str(e)}'}), 400

    # Check if all expected training columns are present
    missing_cols = [col for col in training_columns if col not in data.columns]
    if missing_cols:
        return jsonify({'error': f'Missing columns in input data: {missing_cols}'}), 400

    # Clean numeric columns: convert to numeric and drop rows that fail conversion
    for col in numeric_features:
        if col in data.columns:
            data[col] = pd.to_numeric(data[col], errors='coerce')
    data = data.dropna(subset=numeric_features)

    try:
        preds = model.predict(data)
        probs = model.predict_proba(data)[:, 1]
    except Exception as e:
        return jsonify({'error': f'Prediction error: {str(e)}'}), 500

    # Map numeric predictions back to labels ("Yes"/"No")
    pred_labels = ["Yes" if p == 1 else "No" for p in preds]
    data['churn_prediction'] = pred_labels
    data['churn_probability'] = probs

    result = data.to_json(orient='records')
    return result, 200

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
