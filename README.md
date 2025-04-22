# User Data Management System

A Flask-based web application for managing user data with MongoDB integration. The application allows users to input their details, track expenses, and view analytics.

## Live Demo

The application is currently hosted on AWS and accessible at:
http://13.245.187.167:5000/

## Features

- User data input form
- Expense tracking across multiple categories
- Data visualization and analytics
- Random data generation for testing
- MongoDB integration for data persistence

## Prerequisites

- Python 3.8 or higher
- MongoDB connection string
- Required Python packages (listed in setup instructions)

## Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-directory>
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install flask pymongo python-dotenv pandas matplotlib seaborn
```

4. Set up environment variables:
   - Copy `sample.env` to `.env`
   - Update the MongoDB connection string in `.env` with your credentials

5. Run the application:
```bash
python src/main.py
```

The application will be available at:
- Local development: http://localhost:5000
- Network access: http://<your-ip-address>:5000

## Project Structure

```
.
├── src/
│   ├── main.py              # Main application file
│   ├── visualizations.ipynb # Data analysis notebook
│   └── user_data.py         # User data utilities
├── .env                     # Environment variables (not in version control)
├── sample.env              # Environment variables template
└── README.md               # This file
```

## Environment Variables

Create a `.env` file based on `sample.env` with the following variables:
- `MONGODB_URI`: Your MongoDB connection string

## Data Visualization

The project includes a Jupyter notebook (`src/visualizations.ipynb`) for data analysis and visualization. To use it:

1. Install Jupyter:
```bash
pip install jupyter
```

2. Run the notebook:
```bash
jupyter notebook src/visualizations.ipynb
```

## Security Notes

- Never commit the `.env` file to version control
- Keep your MongoDB credentials secure
- The application is configured to accept connections from any host (0.0.0.0)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 