# 📊 InsightAI: Gen-AI Powered Business Intelligence

**InsightAI** ek modern SaaS-style dashboard hai jo users ko unke CSV data ke saath "baat" karne ki power deta hai. Google Gemini 1.5 Flash ka use karke, ye natural language queries ko instant SQL commands aur interactive visualizations mein badal deta hai.

## ✨ Key Features
- **Conversational Analytics:** SQL likhne ki zarurat nahi, bas pucho "What is my total profit?".
- **Dynamic Charting:** Query ke according automatically Bar, Line, ya Pie charts generate hote hain.
- **Glassmorphism UI:** Tailwind CSS ke saath ek premium dark-themed business interface.
- **Data Agnostic:** Kisi bhi standard CSV file ke saath kaam karta hai.

## 🛠️ Tech Stack
- **Backend:** Flask (Python)
- **AI Engine:** Google Gemini 1.5 Flash API
- **Frontend:** HTML5, Tailwind CSS, JavaScript
- **Charts:** Chart.js
- **Database:** SQLite (In-memory for speed)

## ⚙️ Installation & Setup
1. **Clone the project:**
   ```bash
   git clone [https://github.com/yourusername/insight-ai.git](https://github.com/yourusername/insight-ai.git)
   cd InsightAI
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **API Configuration:**
   `app.py` mein apni Gemini API Key update karein ya `.env` file ka use karein.

4. **Run the application:**
   ```bash
   python app.py
   ```
   Open `http://127.0.0.1:5000` in your browser.

## 🚀 How to Use
1. Landing page par **"Launch Dashboard"** par click karein.
2. Sidebar se apni **CSV file** upload karein.
3. Search bar mein apna sawal likhein (e.g., *"Show top 5 products by sales"*).
4. AI ke magic ka wait karein aur interactive charts dekhein!

---
*Developed for Hackathon 2026*
