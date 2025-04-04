from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from textblob import TextBlob
import plotly.express as px
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for session management
csrf = CSRFProtect(app)

# Configure the database (SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookings.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configure Flask-Mail for email notifications
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'coralbayhoteltest@gmail.com'
app.config['MAIL_PASSWORD'] = 'hvci pojl pllw ptgm'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

# Initialize extensions
db = SQLAlchemy(app)
mail = Mail(app)
login_manager = LoginManager(app)
login_manager.login_view = 'admin_login'

# Admin model
class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

# Room model
class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_type = db.Column(db.String(100), nullable=False)
    room_number = db.Column(db.String(50), nullable=False, unique=True)
    availability = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"<Room {self.room_type}, {self.room_number}>"

# Booking model
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guest_name = db.Column(db.String(100), nullable=False)
    guest_email = db.Column(db.String(100), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    check_in_date = db.Column(db.String(20), nullable=False)
    check_out_date = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"<Booking {self.guest_name}, {self.room_id}>"

# Review model
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Review {self.name}, Rating: {self.rating}>"

# Initialize database and add default rooms
with app.app_context():
    # Create tables if they don't exist
    db.create_all()

    # Create default admin if not exists
    if not Admin.query.filter_by(username='admin').first():
        admin = Admin(username='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()

    # Add default rooms if no rooms exist
    if not Room.query.first():
        rooms = [
            Room(room_type='Single', room_number='101'),
            Room(room_type='Single', room_number='102'),
            Room(room_type='Family', room_number='201'),
            Room(room_type='Family', room_number='202'),
            Room(room_type='Double', room_number='301'),
            Room(room_type='Double', room_number='302'),
            Room(room_type='Double', room_number='303'),
            Room(room_type='Double', room_number='304'),
            Room(room_type='Double', room_number='305'),
            Room(room_type='Double', room_number='306'),
        ]
        db.session.add_all(rooms)
        db.session.commit()

# Function to update room availability after checkout (without email notification)
def update_room_availability():
    today = datetime.today().strftime('%Y-%m-%d')
    expired_bookings = Booking.query.filter(Booking.check_out_date == today).all()

    for booking in expired_bookings:
        room = Room.query.get(booking.room_id)
        if room:
            # Mark the room as available again
            room.availability = True
            db.session.delete(booking)

    db.session.commit()

# Background scheduler to update availability daily
scheduler = BackgroundScheduler()
scheduler.add_job(update_room_availability, 'interval', days=1)
scheduler.start()

def send_booking_update_email(booking, status):
    msg = Message(
        f'Booking {status}',
        sender='coralbayhoteltest@gmail.com',
        recipients=[booking.guest_email]
    )
    room = Room.query.get(booking.room_id)
    msg.body = f"""
    Dear {booking.guest_name},

    Your booking at Coral Bay Hotel has been {status}.

    Booking Details:
    Room Type: {room.room_type}
    Room Number: {room.room_number}
    Check-In: {booking.check_in_date}
    Check-Out: {booking.check_out_date}

    If you have any questions, please contact us.

    Best regards,
    Coral Bay Hotel
    """
    mail.send(msg)

# Admin routes
class AdminLoginForm(FlaskForm):
    pass

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    form = AdminLoginForm()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        admin = Admin.query.filter_by(username=username).first()
        
        if admin and admin.check_password(password):
            login_user(admin)
            return redirect(url_for('admin_dashboard'))
        flash('Invalid username or password')
    return render_template('admin_login.html', form=form)

@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    form = FlaskForm()
    bookings = Booking.query.all()
    rooms = Room.query.all()
    reviews = Review.query.all()
    
    # Prepare review data for visualization
    review_data = []
    sentiment_categories = {'Positive': 0, 'Neutral': 0, 'Negative': 0}
    
    for review in reviews:
        analysis = TextBlob(review.text)
        sentiment_score = analysis.sentiment.polarity
        
        # Categorize sentiment
        if sentiment_score > 0.1:
            sentiment_category = 'Positive'
        elif sentiment_score < -0.1:
            sentiment_category = 'Negative'
        else:
            sentiment_category = 'Neutral'
            
        sentiment_categories[sentiment_category] += 1
        
        review_data.append({
            'name': review.name,
            'rating': review.rating,
            'sentiment': sentiment_score,
            'category': sentiment_category
        })
    
    if review_data:
        df = pd.DataFrame(review_data)
        
        # Create rating distribution chart
        rating_fig = px.histogram(df, x='rating', 
                                title='Rating Distribution',
                                labels={'rating': 'Rating', 'count': 'Number of Reviews'},
                                nbins=5)
        rating_fig.update_layout(
            showlegend=False,
            title_x=0.5,
            margin=dict(t=50, l=50, r=50, b=50)
        )
        rating_chart = rating_fig.to_html(full_html=False)
        
        # Create sentiment pie chart
        sentiment_df = pd.DataFrame({
            'Sentiment': list(sentiment_categories.keys()),
            'Count': list(sentiment_categories.values())
        })
        
        sentiment_fig = px.pie(sentiment_df, 
                             values='Count', 
                             names='Sentiment',
                             title='Review Sentiment Analysis',
                             color='Sentiment',
                             color_discrete_map={
                                 'Positive': '#28a745',
                                 'Neutral': '#ffc107',
                                 'Negative': '#dc3545'
                             })
        sentiment_fig.update_layout(
            title_x=0.5,
            margin=dict(t=50, l=50, r=50, b=50)
        )
        sentiment_chart = sentiment_fig.to_html(full_html=False)
    else:
        rating_chart = "<p>No reviews available</p>"
        sentiment_chart = "<p>No reviews available</p>"
    
    return render_template('admin_dashboard.html', 
                         bookings=bookings, 
                         rooms=rooms, 
                         reviews=reviews,
                         review_data=review_data,
                         rating_chart=rating_chart,
                         sentiment_chart=sentiment_chart,
                         form=form)

@app.route('/admin/booking/<int:booking_id>/cancel', methods=['POST'])
@login_required
def cancel_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    room = Room.query.get(booking.room_id)
    room.availability = True
    db.session.delete(booking)
    db.session.commit()
    send_booking_update_email(booking, "cancelled")
    flash('Booking cancelled successfully')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/booking/<int:booking_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if request.method == 'POST':
        # Get the current room to free it up
        current_room = Room.query.get(booking.room_id)
        current_room.availability = True
        
        # Update booking details
        booking.guest_name = request.form['guest_name']
        booking.guest_email = request.form['guest_email']
        booking.check_in_date = request.form['check_in_date']
        booking.check_out_date = request.form['check_out_date']
        
        # Handle room change if requested
        new_room_id = request.form.get('room_id')
        if new_room_id and int(new_room_id) != booking.room_id:
            new_room = Room.query.get(new_room_id)
            if new_room and new_room.availability:
                new_room.availability = False
                booking.room_id = new_room_id
            else:
                flash('Selected room is not available')
                return redirect(url_for('edit_booking', booking_id=booking_id))
        else:
            current_room.availability = False
        
        db.session.commit()
        send_booking_update_email(booking, "updated")
        flash('Booking updated successfully')
        return redirect(url_for('admin_dashboard'))
    
    available_rooms = Room.query.filter(db.or_(
        Room.availability == True,
        Room.id == booking.room_id
    )).all()
    return render_template('edit_booking.html', booking=booking, rooms=available_rooms)

@app.route('/admin/booking/new', methods=['GET', 'POST'])
@login_required
def new_booking():
    if request.method == 'POST':
        room_id = request.form['room_id']
        room = Room.query.get(room_id)
        
        if room and room.availability:
            booking = Booking(
                guest_name=request.form['guest_name'],
                guest_email=request.form['guest_email'],
                room_id=room_id,
                check_in_date=request.form['check_in_date'],
                check_out_date=request.form['check_out_date']
            )
            room.availability = False
            db.session.add(booking)
            db.session.commit()
            send_booking_update_email(booking, "confirmed")
            flash('Booking created successfully')
            return redirect(url_for('admin_dashboard'))
        flash('Selected room is not available')
    
    available_rooms = Room.query.filter_by(availability=True).all()
    return render_template('new_booking.html', rooms=available_rooms)

@app.route('/admin/rooms')
@login_required
def manage_rooms():
    form = FlaskForm()
    rooms = Room.query.all()
    return render_template('manage_rooms.html', rooms=rooms, form=form)

class RoomForm(FlaskForm):
    pass

@app.route('/admin/rooms/add', methods=['GET', 'POST'])
@login_required
def add_room():
    form = RoomForm()
    if request.method == 'POST':
        room_type = request.form['room_type']
        room_number = request.form['room_number']
        
        # Check if room number already exists
        if Room.query.filter_by(room_number=room_number).first():
            flash('Room number already exists')
            return redirect(url_for('add_room'))
        
        room = Room(room_type=room_type, room_number=room_number, availability=True)
        db.session.add(room)
        db.session.commit()
        flash('Room added successfully')
        return redirect(url_for('manage_rooms'))
    
    return render_template('add_room.html', form=form)

@app.route('/admin/rooms/<int:room_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_room(room_id):
    room = Room.query.get_or_404(room_id)
    
    if request.method == 'POST':
        new_room_number = request.form['room_number']
        # Check if new room number already exists (excluding current room)
        existing_room = Room.query.filter(Room.room_number == new_room_number, Room.id != room_id).first()
        if existing_room:
            flash('Room number already exists')
            return redirect(url_for('edit_room', room_id=room_id))
        
        room.room_type = request.form['room_type']
        room.room_number = new_room_number
        db.session.commit()
        flash('Room updated successfully')
        return redirect(url_for('manage_rooms'))
    
    return render_template('edit_room.html', room=room)

@app.route('/admin/rooms/<int:room_id>/delete', methods=['POST'])
@login_required
def delete_room(room_id):
    room = Room.query.get_or_404(room_id)
    
    # Check if room has any active bookings
    if not room.availability:
        flash('Cannot delete room with active bookings')
        return redirect(url_for('manage_rooms'))
    
    db.session.delete(room)
    db.session.commit()
    flash('Room deleted successfully')
    return redirect(url_for('manage_rooms'))

@app.route('/admin/review/<int:review_id>/delete', methods=['POST'])
@login_required
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)
    db.session.delete(review)
    db.session.commit()
    flash('Review deleted successfully')
    return redirect(url_for('admin_dashboard'))

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

class BookingForm(FlaskForm):
    pass

@app.route('/book', methods=['GET', 'POST'])
def book():
    form = BookingForm()
    message = None
    room_types = Room.query.with_entities(Room.room_type).distinct().all()
    room_types = [r.room_type for r in room_types]
    available_rooms = []
    selected_room_type = None

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'check_availability':
            selected_room_type = request.form.get('room_type')
            available_rooms = Room.query.filter_by(room_type=selected_room_type, availability=True).all()

            if not available_rooms:
                message = "No available rooms for the selected type."

            return render_template('book.html', form=form, room_types=room_types, available_rooms=available_rooms, message=message, selected_room_type=selected_room_type)

        elif action == 'confirm_booking':
            name = request.form['name']
            email = request.form['email']
            room_id = request.form['room_id']
            check_in_date = request.form['check_in_date']
            check_out_date = request.form['check_out_date']

            selected_room = Room.query.get(room_id)
            if selected_room and selected_room.availability:
                selected_room.availability = False
                booking = Booking(guest_name=name, guest_email=email, room_id=room_id, 
                                  check_in_date=check_in_date, check_out_date=check_out_date)
                db.session.add(booking)
                db.session.commit()

                # Send confirmation email to guest
                msg_guest = Message('Booking Confirmation', sender='coralbayhoteltest@gmail.com', recipients=[email])
                msg_guest.body = f"""
                Dear {name},

                Your reservation at Coral Bay Hotel is confirmed!

                Room Type: {selected_room.room_type}
                Room Number: {selected_room.room_number}
                Check-In: {check_in_date}
                Check-Out: {check_out_date}

                If you are not coming please send an email to cancel the booking.
                See you soon!

                - Coral Bay Hotel
                +94 234 567 890
                coralbayhoteltest@gmail.com
                123 Coral Street, Hikkaduwa, Sri Lanka
                """
                mail.send(msg_guest)

                # Send notification email to hotel
                msg_hotel = Message('New Booking Alert', sender='coralbayhoteltest@gmail.com', recipients=['coralbayhoteltest@gmail.com'])
                msg_hotel.body = f"""
                New Booking Received:

                Guest Name: {name}
                Guest Email: {email}
                Room Type: {selected_room.room_type}
                Room Number: {selected_room.room_number}
                Check-In: {check_in_date}
                Check-Out: {check_out_date}

                Please prepare the room accordingly.

                - Coral Bay Hotel System
                """
                mail.send(msg_hotel)

                flash(f"Booking successful! Room {selected_room.room_number} confirmed.")
                # Redirect to GET request to clear form data
                return redirect(url_for('book'))
            else:
                message = "Room is no longer available."

    return render_template('book.html', form=form, room_types=room_types, available_rooms=available_rooms, message=message, selected_room_type=selected_room_type)

# Reviews page
@app.route('/reviews')
def reviews():
    reviews = Review.query.all()
    return render_template('reviews.html', reviews=reviews)

class ReviewForm(FlaskForm):
    pass

@app.route('/submit_review', methods=['GET', 'POST'])
def submit_review():
    form = ReviewForm()
    if request.method == 'POST':
        name = request.form['name']
        text = request.form['review']  # Changed from 'text' to match the form
        rating = int(request.form['rating'])

        # Perform sentiment analysis
        analysis = TextBlob(text)
        sentiment_score = analysis.sentiment.polarity

        review = Review(name=name, text=text, rating=rating)
        db.session.add(review)
        db.session.commit()

        flash('Thank you for your review!')
        return redirect(url_for('reviews'))

    return render_template('submit_review.html', form=form)

# Chatbot responses
CHATBOT_RESPONSES = {
    "booking": {
        "question": "How can I make a booking?",
        "answer": "You have two options to make a booking:\n1. Use our online booking system: Click the 'Book Now' button on our homepage\n2. Contact us directly:\n   - Phone: +94 234 567 890\n   - Email: contact@coralbayhotel.com\n\nOur staff will be happy to assist you with your reservation."
    },
    "check_in": {
        "question": "What are the check-in and check-out times?",
        "answer": "Our check-in and check-out times are:\n- Check-in: 2:00 PM\n- Check-out: 11:00 AM\n\nEarly check-in or late check-out may be available upon request, subject to availability."
    },
    "contact": {
        "question": "What are your contact details?",
        "answer": "You can reach us through:\n- Phone: +94 234 567 890\n- Email: contact@coralbayhotel.com\n- Address: 123 Coral Street, Hikkaduwa, Sri Lanka\n\nOur front desk is available 24/7 to assist you."
    },
    "room_prices": {
        "question": "What are your room rates?",
        "answer": "Our current room rates per night are:\n- Single Room: $50\n- Double Room: $80\n- Family Room: $120\n\nRates may vary during peak seasons. Contact us for special deals and group bookings."
    },
    "amenities": {
        "question": "What amenities do you offer?",
        "answer": "We offer a range of amenities including:\n- Swimming pool\n- Free Wi-Fi throughout the property\n- Free parking (both outdoor and covered)\n- Restaurant\n- Room service\n- 24/7 front desk\n- Air conditioning\n- TV in all rooms\n- Private bathroom in all rooms"
    },
    "wifi": {
        "question": "Do you have Wi-Fi?",
        "answer": "Yes, we provide free Wi-Fi access throughout the hotel for all our guests. The network details will be provided during check-in."
    },
    "swimming_pool": {
        "question": "Do you have a swimming pool?",
        "answer": "Yes, we have a swimming pool available for all our guests. The pool is open daily from 7:00 AM to 9:00 PM."
    },
    "parking": {
        "question": "Is parking available?",
        "answer": "Yes, we offer free parking for all our guests. Both outdoor and covered parking spaces are available on a first-come, first-served basis."
    },
    "cancellation": {
        "question": "What is your cancellation policy?",
        "answer": "You can cancel your booking up to 24 hours before check-in without any charge. For cancellations less than 24 hours before check-in, one night's stay will be charged."
    },
    "pets": {
        "question": "Are pets allowed?",
        "answer": "We welcome pets in designated pet-friendly rooms. There is an additional charge of $20 per night per pet. Please inform us in advance if you plan to bring a pet."
    },
    "restaurant": {
        "question": "Do you have a restaurant?",
        "answer": "Yes, our on-site restaurant serves:\n- Breakfast: 6:30 AM - 10:30 AM\n- Lunch: 12:00 PM - 3:00 PM\n- Dinner: 6:00 PM - 10:00 PM\n\nRoom service is also available during these hours."
    },
    "location": {
        "question": "How far are you from the beach?",
        "answer": "We are located directly on Hikkaduwa Beach at 123 Coral Street. All our ocean-view rooms offer stunning views of the Indian Ocean, and the beach is just steps away from the hotel."
    }
}

# Chat routes
@app.route('/chat')
def chat():
    return render_template('chat.html', predefined_questions=list(CHATBOT_RESPONSES.values()))

@app.route('/api/chat', methods=['GET', 'POST'])
@csrf.exempt
def chat_api():
    if request.method == 'GET':
        return jsonify({
            'available_questions': [
                {'question': qa['question'], 'answer': qa['answer']} 
                for qa in CHATBOT_RESPONSES.values()
            ]
        })
    
    # Handle POST request
    query = request.json.get('query', '').lower() if request.is_json else request.form.get('query', '').lower()
    
    # Find the best matching question
    best_match = None
    highest_similarity = 0
    
    for key, qa in CHATBOT_RESPONSES.items():
        # Simple word matching similarity
        question_words = set(qa['question'].lower().split())
        query_words = set(query.split())
        common_words = question_words.intersection(query_words)
        
        if len(common_words) > highest_similarity:
            highest_similarity = len(common_words)
            best_match = qa
    
    if best_match and highest_similarity > 0:
        return jsonify({
            'answer': best_match['answer'],
            'question': best_match['question']
        })
    
    return jsonify({
        'answer': "I'm sorry, I don't understand that question. Please try asking something else or contact our staff for assistance.",
        'question': None
    })

if __name__ == '__main__':
    app.run(debug=True)
