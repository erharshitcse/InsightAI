from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import pandas as pd
import sqlite3
import re
import os

app = Flask(__name__)

# 1. Gemini Config
API_KEY = "AIzaSyDPdtWdzeXCJA58-JAsD5XimYunl-idF9M" # Apni key yahan check kar lena
genai.configure(api_key=API_KEY)

def get_model():
    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        if 'models/gemini-1.5-flash' in models: return genai.GenerativeModel('gemini-1.5-flash')
        return genai.GenerativeModel('gemini-pro')
    except:
        return genai.GenerativeModel('gemini-pro')

model = get_model()
db_conn = sqlite3.connect(':memory:', check_same_thread=False)
current_cols = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/upload', methods=['POST'])
def upload():
    global current_cols
    file = request.files['file']
    df = pd.read_csv(file)
    df.columns = [c.replace(' ', '_').replace('-', '_') for c in df.columns]
    current_cols = list(df.columns)
    df.to_sql('data_table', db_conn, index=False, if_exists='replace')
    return jsonify({"message": "Success", "columns": current_cols})

@app.route('/api/query', methods=['POST'])
def query():
    user_input = request.json.get('query')
    prompt = f"Table: 'data_table' Columns: {current_cols}. Return SQL: [SQL] and CHART: [bar/line/pie] for: {user_input}. No markdown."
    
    response = model.generate_content(prompt).text
    try:
        sql = re.search(r"SQL:(.*?)CHART:", response, re.DOTALL | re.IGNORECASE).group(1).strip()
        chart = re.search(r"CHART:(.*)", response, re.DOTALL | re.IGNORECASE).group(1).strip().lower()
        res_df = pd.read_sql_query(sql, db_conn)
        return jsonify({
            "labels": res_df.iloc[:, 0].tolist(),
            "values": res_df.iloc[:, 1].tolist() if len(res_df.columns) > 1 else res_df.iloc[:, 0].tolist(),
            "chart_type": chart,
            "table_html": res_df.to_html(classes='min-w-full text-sm text-gray-300', index=False)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)