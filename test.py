from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import google.generativeai as genai
import logging
import os

from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../.env')) 
api_key = os.getenv('GEMINI_API_KEY') 

# Initialize Flask app
app = Flask(__name__)
app.secret_key = api_key  # Replace with a secure key