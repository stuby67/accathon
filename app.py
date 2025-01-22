from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import google.generativeai as genai
import logging
import requests
from bs4 import BeautifulSoup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Replace with a secure key

# Configure Google Generative AI
genai.configure(api_key="your_google_gen_ai_api_key_here")

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Dummy in-memory database for user credentials (replace with a database for production)
USERS = {"admin": "password123", "gstexpert": "gst@expert"}

def get_gemini_response(question):
    try:
        # Use the Gemini model to process the question
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = (
            f"You are an expert in Goods and Services Tax (GST). Your role is to provide clear, "
            f"professional, and actionable guidance related to GST queries. "
            f"Answer the following question in a clean, formatted manner without using unnecessary symbols or characters:\n\n"
            f"Question: {question}\n\n"
            f"Response:"
        )
        response = model.generate_content([prompt])
        if response and hasattr(response, 'text') and response.text.strip():
            return response.text.strip()
        else:
            logging.error("Empty or invalid response from Generative AI.")
            return "Sorry, I couldn't understand your query. Please try rephrasing or provide more details."
    except Exception as e:
        logging.error(f"Error generating response from Generative AI: {e}")
        return "An error occurred while processing your request. Please try again later."

def fetch_latest_news():
    try:
        url = "https://www.moneycontrol.com/news/tags/gst.html"  # Example website
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Example scraping logic (adjust based on website structure)
        news = []
        articles = soup.find_all("div", class_="news_content", limit=5)  # Modify class and limit as needed
        for article in articles:
            title = article.find("a").text.strip()
            link = article.find("a")["href"]
            snippet = article.find("p").text.strip() if article.find("p") else "Click to read more."
            news.append({"title": title, "link": link, "snippet": snippet})

        return news
    except Exception as e:
        logging.error(f"Error fetching news: {e}")
        return [{"title": "Unable to fetch news. Please try again later.", "link": "#", "snippet": ""}]

@app.route('/')
def index():
    return render_template('index.html', user=session.get('user'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in USERS and USERS[username] == password:
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid username or password")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/ask_ajax', methods=['POST'])
def ask_ajax():
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        if not question:
            return jsonify({"response": "Please provide a valid question."})
        response = get_gemini_response(question)
        return jsonify({"response": response})
    except Exception as e:
        logging.error(f"Error in ask_ajax route: {e}")
        return jsonify({"response": "An unexpected error occurred. Please try again later."})

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in USERS:
            return render_template('signup.html', error="Username already exists. Please try another.")
        USERS[username] = password
        flash("Account created successfully! You can now log in.", "success")
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')
    return render_template('dashboard.html', user=session.get('user'))



if __name__ == '__main__':
    app.run(debug=True)
