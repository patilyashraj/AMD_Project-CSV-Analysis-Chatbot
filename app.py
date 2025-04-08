from flask import Flask, request, jsonify, render_template, send_from_directory
import pandas as pd
import os
import re

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

dataframe = None
filename = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    global dataframe, filename
    file = request.files['file']
    if file.filename.endswith('.csv'):
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        dataframe = pd.read_csv(filepath)
        filename = file.filename
        return jsonify({"message": "File uploaded successfully!"})
    return jsonify({"error": "Only CSV files are allowed."})

@app.route('/ask', methods=['POST'])
def ask():
    global dataframe
    if dataframe is None:
        return jsonify({'response': "Please upload a CSV file first."})

    user_message = request.json.get("question", "").lower()
    response = ""

    if "column" in user_message or "columns" in user_message:
        response = f"The dataset has the following columns: {', '.join(dataframe.columns)}."

    

    elif re.search(r"(replace|get rid of).*missing", user_message):
        numeric_cols = dataframe.select_dtypes(include='number').columns
        dataframe[numeric_cols] = dataframe[numeric_cols].fillna(dataframe[numeric_cols].mean())
        processed_path = os.path.join(PROCESSED_FOLDER, "processed_file.csv")
        dataframe.to_csv(processed_path, index=False)
        response = (
            "Missing values in numeric columns were replaced with the mean. "
            "You can download the updated file <a href='/download/processed_file.csv' target='_blank'>here</a>."
        )
        
    elif "missing" in user_message:
        missing = dataframe.isnull().sum().to_dict()
        response = "Missing values per column:\n" + "\n".join(f"{k}: {v}" for k, v in missing.items())

    elif "data type" in user_message or "type of" in user_message:
        dtypes = dataframe.dtypes.to_dict()
        response = "Here are the data types of each column:<br>" + "<br>".join([f"{k}: {v}" for k, v in dtypes.items()])

    elif "mean" in user_message:
        for col in dataframe.columns:
            if col.lower() in user_message and pd.api.types.is_numeric_dtype(dataframe[col]):
                response = f"The mean of '{col}' is {dataframe[col].mean():.2f}."
                break
        else:
            response = "Please specify a valid numeric column for mean calculation."

    elif "min" in user_message or "maximum" in user_message or "max" in user_message:
        for col in dataframe.columns:
            if col.lower() in user_message and pd.api.types.is_numeric_dtype(dataframe[col]):
                col_min = dataframe[col].min()
                col_max = dataframe[col].max()
                response = f"Minimum of '{col}' is {col_min}, and maximum is {col_max}."
                break
        else:
            response = "Please specify a valid numeric column for min/max calculation."

    else:
        response = "I'm not sure how to respond to that. Try asking about columns, missing values, mean, etc."

    return jsonify({"response": response})

@app.route('/download/<path:filename>', methods=['GET'])
def download(filename):
    return send_from_directory(PROCESSED_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
