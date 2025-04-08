📊 CSV Chatbot Web App

A smart and interactive CSV Chatbot built using Flask and JavaScript that allows users to:

- Upload CSV files
- Get summaries of the dataset
- Ask questions like:
  - "What are the column names?"
  - "How many missing values are there?"
  - "What is the mean of Age?"
  - "Replace missing values"
- Automatically clean missing values (on request)
- Download the updated CSV after processing

🚀 Features

✅ Upload CSV files  
✅ Interactive chatbot-style UI  
✅ Real-time responses with Flask backend  
✅ Handles:
- Column analysis  
- Mean, min, max calculations  
- Missing value detection  
- Missing value replacement (by mean)  
✅ Cleaned CSV available for download

🛠️ Tech Stack

- Python (Flask)
- JavaScript (Vanilla)
- HTML5 + CSS3
- Pandas

📂 How It Works

1. Upload any CSV file
2. Ask questions in natural language (e.g., “mean of Fare”, “missing values?”)
3. If you ask for "replace missing values", it fills them using column-wise mean
4. The chatbot responds like a conversation and keeps chat history
5. Download the cleaned CSV file if changes were made

📥 Example Queries


What are the column names?
Show missing values
Replace missing values
What is the max of Age?
Get mean of Fare


📁 Folder Structure

csv-chatbot/
├── app.py
├── templates/
│   └── index.html
├── static/
│   └── style.css
├── uploads/
├── processed/
├── requirements.txt
├── .gitignore


💡 Future Improvements

- NLP-enhanced query understanding
- File type support beyond CSV
- User login for history tracking
- Chatbot personality customization
