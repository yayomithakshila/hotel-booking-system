# Hotel Booking System

A comprehensive hotel booking system built with Flask, featuring an admin dashboard, room management, booking system, and customer review analytics.

## Features

- User booking interface
- Admin dashboard
- Room management
- Booking processing
- Review system with sentiment analysis
- Email notifications
- Interactive chatbot
- Analytics and reporting

## Technology Stack

- Backend: Flask (Python)
- Database: SQLAlchemy with PostgreSQL
- Frontend: HTML5, CSS3, JavaScript, Bootstrap 5
- Additional: Chart.js, DataTables, TextBlob

## Prerequisites

- Python 3.8+
- Node.js and npm
- PostgreSQL
- Git

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/hotel-booking-system.git
cd hotel-booking-system
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Install frontend dependencies:
```bash
npm install
```

5. Set up environment variables:
```bash
cp .env.example .env
# Edit .env file with your configuration
```

6. Initialize the database:
```bash
flask db upgrade
```

7. Run the development server:
```bash
flask run
```

## Configuration

Create a `.env` file in the root directory with the following variables:
```
FLASK_APP=app.py
FLASK_ENV=development
DATABASE_URL=postgresql://username:password@localhost/dbname
SECRET_KEY=your-secret-key
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-email-password
```

## Project Structure

```
hotel-booking-system/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   └── utils.py
├── static/
│   ├── css/
│   ├── js/
│   └── img/
├── templates/
│   ├── admin/
│   └── public/
├── tests/
├── venv/
├── .env
├── .gitignore
├── app.py
├── config.py
├── requirements.txt
└── README.md
```

## Development

1. Start the development server:
```bash
flask run
```

2. Watch for frontend changes:
```bash
npm run watch
```

## Testing

Run the test suite:
```bash
pytest
```

Generate coverage report:
```bash
coverage run -m pytest
coverage report
```

## Deployment

1. Set up production server (e.g., Ubuntu with Nginx):
```bash
sudo apt-get update
sudo apt-get install nginx python3-pip postgresql
```

2. Configure Nginx:
```bash
sudo nano /etc/nginx/sites-available/hotel-booking
```

3. Set up Gunicorn:
```bash
gunicorn -w 4 -b 127.0.0.1:8000 app:app
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Flask documentation
- Bootstrap documentation
- SQLAlchemy documentation
- Chart.js documentation 