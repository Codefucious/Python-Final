# Flask + MongoDB App: app.py
# Install dependencies: pip install flask pymongo python-dotenv

from flask import Flask, request, render_template_string, redirect, url_for
from pymongo import MongoClient
import random
from datetime import datetime
from dotenv import load_dotenv
import os
random.seed(datetime.now().timestamp())  # Ensure different random values each time

# Load environment variables
load_dotenv()

# Initialize Flask app and MongoDB client
app = Flask(__name__)

# Use MongoDB URI from environment variable
MONGODB_URI = os.getenv('MONGODB_URI')
if not MONGODB_URI:
    raise ValueError("No MONGODB_URI found in environment variables")

client = MongoClient(MONGODB_URI)

db = client['user_data_db']
collection = db['user_details']

# HTML form and data display template
HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>User Data Form</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 2rem; }
    label { display: block; margin: 0.5rem 0; }
    fieldset { margin: 1rem 0; }
    button { padding: 0.5rem 1rem; }
    .message { color: green; }
    table { width: 100%; border-collapse: collapse; margin-top: 2rem; }
    th, td { border: 1px solid #ccc; padding: 0.5rem; text-align: left; }
    th { background-color: #f4f4f4; }
    .seed-button { 
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        margin: 10px 0;
    }
    .seed-button:hover {
        background-color: #45a049;
    }
  </style>
</head>
<body>
  <h1>Enter User Details</h1>
  <form method="post">
    <label>Age: <input type="number" name="age" required></label>
    <label>Gender:
      <select name="gender" required>
        <option value="">Select</option>
        <option value="Male">Male</option>
        <option value="Female">Female</option>
        <option value="Other">Other</option>
      </select>
    </label>
    <label>Total Income: <input type="number" name="income" step="0.01" required></label>
    <fieldset>
      <legend>Expenses</legend>
      {% for cat in categories %}
      <label>
        <input type="checkbox" name="expense_categories" value="{{ cat }}">
        {{ cat.replace('_', ' ').capitalize() }}
      </label>
      <input type="number" name="{{ cat }}_amount" step="0.01" placeholder="Amount"><br>
      {% endfor %}
    </fieldset>
    <button type="submit">Submit</button>
  </form>

  <form action="{{ url_for('seed_data') }}" method="post">
    <button type="submit" class="seed-button">Seed 100 Random Entries</button>
  </form>

  {% if message %}
  <p class="message">{{ message }}</p>
  {% endif %}

  <h2>Stored Entries</h2>
  <table>
    <thead>
      <tr>
        <th>Age</th>
        <th>Gender</th>
        <th>Income</th>
        <th>Expenses</th>
      </tr>
    </thead>
    <tbody>
      {% for rec in records %}
      <tr>
        <td>{{ rec.age }}</td>
        <td>{{ rec.gender }}</td>
        <td>{{ rec.income }}</td>
        <td>{{ rec.expenses | tojson }}</td>
      </tr>
      {% endfor %}
    </tbody>
  </table>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    categories = ['utilities', 'entertainment', 'school_fees', 'shopping', 'healthcare']
    message = None

    if request.method == 'POST':
        # Collect form data
        age = int(request.form['age'])
        gender = request.form['gender']
        income = float(request.form['income'])
        selected = request.form.getlist('expense_categories')
        expenses = {}
        for cat in selected:
            amount = request.form.get(f"{cat}_amount")
            if amount:
                expenses[cat] = float(amount)
        # Insert into MongoDB
        document = {'age': age, 'gender': gender, 'income': income, 'expenses': expenses}
        collection.insert_one(document)
        message = "Data saved successfully!"

    # Fetch all records (excluding MongoDB-generated _id)
    records = list(collection.find({}, {'_id': False}))
    return render_template_string(HTML_TEMPLATE, categories=categories, message=message, records=records)

def generate_random_entry():
    age = random.randint(18, 80)
    gender = random.choice(['Male', 'Female', 'Other'])
    income = round(random.uniform(20000, 150000), 2)
    
    # Randomly select 1-5 expense categories
    num_expenses = random.randint(1, 5)
    categories = ['utilities', 'entertainment', 'school_fees', 'shopping', 'healthcare']
    selected_categories = random.sample(categories, num_expenses)
    
    expenses = {}
    for cat in selected_categories:
        # Generate random expense amount between 100 and 5000
        expenses[cat] = round(random.uniform(100, 5000), 2)
    
    return {
        'age': age,
        'gender': gender,
        'income': income,
        'expenses': expenses
    }

@app.route('/seed', methods=['POST'])
def seed_data():
    # Generate and insert 100 random entries
    random_entries = [generate_random_entry() for _ in range(100)]
    collection.insert_many(random_entries)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
