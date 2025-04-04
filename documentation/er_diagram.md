# Hotel Booking System - Entity Relationship Diagram

## Database Schema

```mermaid
erDiagram
    ROOM ||--o{ BOOKING : "has"
    ROOM ||--o{ ROOM_IMAGE : "has"
    BOOKING ||--o{ REVIEW : "has"
    USER ||--o{ BOOKING : "manages"
    ROOM_TYPE ||--o{ ROOM : "categorizes"
    BOOKING ||--o{ PAYMENT : "has"
    
    ROOM {
        int id PK
        string room_number UK
        int room_type_id FK
        decimal price
        boolean availability
        text description
        int capacity
        datetime created_at
        datetime updated_at
    }

    ROOM_TYPE {
        int id PK
        string name UK
        text description
        decimal base_price
        int capacity
        datetime created_at
        datetime updated_at
    }

    ROOM_IMAGE {
        int id PK
        int room_id FK
        string image_path
        boolean is_primary
        datetime created_at
    }

    BOOKING {
        int id PK
        int room_id FK
        int user_id FK "Optional"
        string guest_name
        string guest_email
        string phone_number
        date check_in_date
        date check_out_date
        string status
        decimal total_price
        text special_requests
        datetime created_at
        datetime updated_at
        datetime cancelled_at
    }

    REVIEW {
        int id PK
        int booking_id FK
        string name
        int rating
        text review_text
        float sentiment_score
        string sentiment_category
        datetime created_at
        datetime updated_at
    }

    USER {
        int id PK
        string username UK
        string email UK
        string password_hash
        string role
        boolean is_active
        datetime last_login
        datetime created_at
        datetime updated_at
    }

    PAYMENT {
        int id PK
        int booking_id FK
        decimal amount
        string payment_method
        string transaction_id UK
        string status
        datetime payment_date
        datetime created_at
        datetime updated_at
    }
```

## Relationships Explanation

1. **ROOM and ROOM_TYPE** (Many-to-One)
   - Each room belongs to one room type
   - Each room type can have multiple rooms
   - Attributes like base_price and capacity are inherited from room type

2. **ROOM and BOOKING** (One-to-Many)
   - One room can have many bookings (over time)
   - Each booking is associated with exactly one room
   - Room availability is tracked in real-time

3. **BOOKING and REVIEW** (One-to-Many)
   - Each booking can have multiple reviews
   - Each review is associated with exactly one booking
   - Reviews include sentiment analysis results

4. **USER and BOOKING** (One-to-Many)
   - Users (admin/staff) can manage multiple bookings
   - Each booking can be managed by one user
   - Guest bookings may not have associated users

5. **ROOM and ROOM_IMAGE** (One-to-Many)
   - Each room can have multiple images
   - One image is marked as primary for display
   - Images are stored with paths to filesystem

6. **BOOKING and PAYMENT** (One-to-Many)
   - Each booking can have multiple payment records
   - Each payment is associated with exactly one booking
   - Supports partial payments and payment history

## Key Features

1. **Data Integrity**
   - Primary Keys (PK) for unique identification
   - Foreign Keys (FK) for relationships
   - Unique Keys (UK) for business rules

2. **Audit Trail**
   - created_at timestamps for all entities
   - updated_at timestamps for trackable changes
   - cancelled_at for booking cancellations

3. **Business Rules**
   - Room availability status
   - Booking status tracking
   - Payment status monitoring
   - User role management

4. **Analytics Support**
   - Review sentiment analysis
   - Booking history
   - Payment tracking
   - Room occupancy rates

## Database Constraints

1. **Room Management**
   - Unique room numbers
   - Valid room type reference
   - Price must be positive

2. **Booking Rules**
   - Valid date ranges
   - No overlapping bookings
   - Required guest information

3. **Review System**
   - Rating range (1-5)
   - Valid booking reference
   - Sentiment score range (-1 to 1)

4. **Payment Processing**
   - Unique transaction IDs
   - Valid payment methods
   - Amount validation

## Notes

1. **Scalability Considerations**
   - Separate room_type table for flexibility
   - Image paths stored separately
   - Payment history preservation

2. **Security Features**
   - Password hashing
   - Role-based access
   - Activity logging

3. **Performance Optimization**
   - Indexed foreign keys
   - Optimized date ranges
   - Status tracking fields 