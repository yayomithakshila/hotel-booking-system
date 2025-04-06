# Hotel Booking System Documentation
*By Yayomi*

## 1. System Overview
The hotel booking system is a web-based application developed using Flask framework that allows hotel administrators to manage room bookings, track room availability, and collect guest feedback. The system features a user-friendly interface for both administrators and guests.

### 1.1 Key Features
- Room booking management
- Real-time room availability tracking
- Guest review and rating system
- Admin dashboard with analytics
- Automated room status updates
- Sentiment analysis for guest reviews

[*Screenshot recommendation: Homepage showing the main navigation*]

## 2. Technical Architecture

### 2.1 Technology Stack
- Backend: Python Flask
- Database: SQLite
- Frontend: HTML5, CSS3, Bootstrap 5
- Additional Libraries: 
  - TextBlob (for sentiment analysis)
  - Flask-SQLAlchemy (database ORM)
  - Flask-Login (authentication)

### 2.2 Database Schema
```sql
Room:
- id (Primary Key)
- room_number
- room_type
- price
- availability_status

Booking:
- id (Primary Key)
- guest_name
- room_id (Foreign Key)
- check_in_date
- check_out_date
- booking_status

Review:
- id (Primary Key)
- name
- rating
- text
- timestamp
```

[*Screenshot recommendation: Database relationship diagram*]

## 3. Core Functionality

### 3.1 Room Booking Process
1. Admin selects room type and dates
2. System checks room availability
3. Admin enters guest details
4. System confirms booking and updates room status

[*Screenshot recommendation: Room booking form and availability check interface*]

### 3.2 Room Availability Management
```python
# Code snippet showing availability check logic
def check_room_availability(room_id, check_in_date, check_out_date):
    existing_bookings = Booking.query.filter(
        Booking.room_id == room_id,
        Booking.booking_status != 'cancelled'
    ).all()
    
    for booking in existing_bookings:
        if (check_in_date <= booking.check_out_date and 
            check_out_date >= booking.check_in_date):
            return False
    return True
```

[*Screenshot recommendation: Room availability calendar view*]

## 4. Admin Dashboard

### 4.1 Dashboard Features
- Current bookings overview
- Room status monitoring
- Review analytics
- Booking management tools

[*Screenshot recommendation: Admin dashboard main view*]

### 4.2 Room Management
- Add/Edit room details
- Update room status
- View booking history

[*Screenshot recommendation: Room management interface*]

## 5. Review System

### 5.1 Review Submission
The system allows guests to submit reviews with:
- Rating (1-5 stars)
- Written feedback
- Guest name

[*Screenshot recommendation: Review submission form*]

### 5.2 Rating System
```
⭐         - Poor
⭐⭐       - Fair
⭐⭐⭐     - Good
⭐⭐⭐⭐   - Very Good
⭐⭐⭐⭐⭐ - Excellent
```

[*Screenshot recommendation: Review display with ratings*]

### 5.3 Sentiment Analysis
```python
# Code snippet showing sentiment analysis implementation
def analyze_sentiment(review_text):
    analysis = TextBlob(review_text)
    sentiment_score = analysis.sentiment.polarity
    
    if sentiment_score > 0.3:
        return 'Positive'
    elif sentiment_score < -0.3:
        return 'Negative'
    else:
        return 'Neutral'
```

[*Screenshot recommendation: Sentiment analysis results in admin dashboard*]

## 6. Security Features

### 6.1 Authentication
- Admin login system
- Session management
- CSRF protection

### 6.2 Data Validation
- Input sanitization
- Form validation
- Error handling

[*Screenshot recommendation: Login interface and error messages*]

## 7. User Interface Design

### 7.1 Frontend Framework
- Bootstrap 5 components
- Responsive design
- Mobile-friendly interface

### 7.2 Key Templates
```html
templates/
├── admin_dashboard.html
├── new_booking.html
├── reviews.html
├── submit_review.html
├── header.html
└── footer.html
```

[*Screenshot recommendation: Mobile and desktop view comparison*]

## 8. System Testing

### 8.1 Test Cases
- Booking creation and validation
- Room availability checks
- Review submission and analysis
- Admin authentication
- Error handling scenarios

### 8.2 Performance Testing
- Load testing results
- Response time measurements
- Database query optimization

## 9. Future Enhancements
1. Online payment integration
2. Email notification system
3. Guest account management
4. Advanced booking analytics
5. Multi-language support

## 10. Installation and Deployment

### 10.1 Requirements
```
Flask==2.0.1
Flask-SQLAlchemy==2.5.1
Flask-Login==0.5.0
textblob==0.15.3
```

### 10.2 Setup Instructions
1. Database initialization
2. Environment configuration
3. Server deployment
4. Admin account creation

[*Screenshot recommendation: System architecture diagram*]

## Screenshot Placement Guide

For each major section, include screenshots that demonstrate:
1. User Interface elements
2. Workflow processes
3. System outputs
4. Error messages and handling
5. Mobile responsiveness

Key areas for screenshots:
1. Homepage and navigation
2. Booking process (step by step)
3. Admin dashboard views
4. Review submission and display
5. Room management interface
6. Analytics and reporting
7. Mobile device views
8. Error handling examples

Remember to:
- Capture full-page screenshots where relevant
- Include mobile and desktop views
- Highlight important interface elements
- Show both admin and user perspectives
- Include examples of successful operations and error states 