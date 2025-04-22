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

    if re.search(r"(replace|get rid of).*missing", user_message):
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
        response = "Missing values per column:<br>" + "<br>".join(f"{k}: {v}" for k, v in missing.items())

    elif "data type" in user_message or "type of" in user_message:
        dtypes = dataframe.dtypes.to_dict()
        response = "Here are the data types of each column:<br>" + "<br>".join([f"{k}: {v}" for k, v in dtypes.items()])

    elif "mean" in user_message:
        lowered_columns = {col.lower(): col for col in dataframe.columns}
        for key in lowered_columns:
            if key in user_message and pd.api.types.is_numeric_dtype(dataframe[lowered_columns[key]]):
                actual_col = lowered_columns[key]
                response = f"The mean of '{actual_col}' is {dataframe[actual_col].mean():.4f}."
                break
        else:
            response = "Please specify a valid numeric column for mean calculation."

    elif "min" in user_message or "minimum" in user_message:
        for col in dataframe.columns:
            if col.lower() in user_message and pd.api.types.is_numeric_dtype(dataframe[col]):
                col_min = dataframe[col].min()
                response = f"Minimum of '{col}' is {col_min:.4f}."
                break
        else:
            response = "Please specify a valid numeric column for min calculation."
            
    elif "maximum" in user_message or "max" in user_message:
        for col in dataframe.columns:
            if col.lower() in user_message and pd.api.types.is_numeric_dtype(dataframe[col]):
                col_max = dataframe[col].max()
                response = f"Maximum of '{col}' is {col_max:.4f}."
                break
        else:
            response = "Please specify a valid numeric column for max calculation."

    elif "count" in user_message:
        for col in dataframe.columns:
            if col.lower() in user_message:
                count_val = dataframe[col].count()
                response = f"The count of non-null values in '{col}' is {count_val:.4f}."
                break
        else:
            response = "Please specify a valid column for count calculation."

    elif "sum" in user_message:
        for col in dataframe.columns:
            if col.lower() in user_message and pd.api.types.is_numeric_dtype(dataframe[col]):
                sum_val = dataframe[col].sum()
                response = f"The sum of values in '{col}' is {sum_val:.4f}."
                break
        else:
            response = "Please specify a valid numeric column for sum calculation."
            
    elif "column" in user_message or "columns" in user_message:
        response = f"The dataset has the following columns {', '.join(dataframe.columns)}."
        

    else:
        response = "I'm not sure how to respond to that. Try asking about columns, missing values, mean, etc."
    
    

    return jsonify({"response": response})

@app.route('/info')
def info():
    return render_template('info.html')


@app.route('/download/<path:filename>', methods=['GET'])
def download(filename):
    return send_from_directory(PROCESSED_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
    

