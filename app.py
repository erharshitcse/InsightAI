from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import pandas as pd
import sqlite3
import re
import os

app = Flask(__name__)

# 1. Gemini Config - Render/Local dono ke liye safe setup
# Pehle environment variable check karega, nahi toh hardcoded key use karega
API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyDPdtWdzeXCJA58-JAsD5XimYunl-idF9M")
genai.configure(api_key=API_KEY)

# Direct Gemini 1.5 Flash use karo, 404 error khatam!
model = genai.GenerativeModel('gemini-1.5-flash')

# Database connection (In-memory)
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
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
            
        file = request.files['file']
        df = pd.read_csv(file)
        
        # SQL table ke liye column names clean karna zaroori hai
        df.columns = [c.replace(' ', '_').replace('-', '_').replace('(', '').replace(')', '') for c in df.columns]
        current_cols = list(df.columns)
        
        df.to_sql('data_table', db_conn, index=False, if_exists='replace')
        return jsonify({"message": "Success", "columns": current_cols})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/query', methods=['POST'])
def query():
    if not current_cols:
        return jsonify({"error": "Pehle CSV upload karo bhai!"}), 400

    user_input = request.json.get('query')
    
    # Prompt ko thoda aur robust banaya taaki AI galat SQL na de
    prompt = f"""
    You are a SQLite expert. 
    Table Name: 'data_table'
    Columns: {current_cols}
    
    Task:
    1. Write a SQLite query to answer: "{user_input}"
    2. Suggest a chart type (bar, line, or pie).
    
    Return the response ONLY in this format:
    SQL: [Your Query]
    CHART: [Type]
    """
    
    try:
        response = model.generate_content(prompt).text
        
        # Regex se SQL aur Chart type nikalna
        sql_match = re.search(r"SQL:(.*?)CHART:", response, re.DOTALL | re.IGNORECASE)
        chart_match = re.search(r"CHART:(.*)", response, re.DOTALL | re.IGNORECASE)
        
        if sql_match and chart_match:
            sql = sql_match.group(1).strip().replace("```sql", "").replace("```", "")
            chart = chart_match.group(1).strip().lower()
            
            res_df = pd.read_sql_query(sql, db_conn)
            
            # Agar query result khali hai toh handle karein
            if res_df.empty:
                return jsonify({"error": "Query toh sahi thi, par data nahi mila!"}), 200

            return jsonify({
                "labels": res_df.iloc[:, 0].tolist(),
                "values": res_df.iloc[:, 1].tolist() if len(res_df.columns) > 1 else res_df.iloc[:, 0].tolist(),
                "chart_type": chart,
                "table_html": res_df.to_html(classes='min-w-full text-sm text-gray-300', index=False)
            })
        else:
            return jsonify({"error": "AI ne response format galat diya!"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Render ke liye port config
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
