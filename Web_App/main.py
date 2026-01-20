# main.py
import os
from flask import send_from_directory
from Backend import create_app
import flask_excel as excel

app = create_app()
# init flask-excel (safe)
excel.init_excel(app)

# health check
@app.route("/ping")
def ping():
    return {"message": "Backend is alive"}, 200

# Serve Vue.js frontend from the local 'dist' folder
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_vue(path):
    # This points to the dist folder inside Web_App
    dist_dir = os.path.join(os.path.dirname(__file__), 'dist')
    
    if path and os.path.exists(os.path.join(dist_dir, path)):
        return send_from_directory(dist_dir, path)
    else:
        # If file not found, serve index.html (for Vue Router)
        return send_from_directory(dist_dir, 'index.html')

# DO NOT run app.run() in production