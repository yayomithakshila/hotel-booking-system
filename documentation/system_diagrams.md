# Hotel Booking System - System Diagrams

## 1. High-Level System Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        B[Web Browser]
        M[Mobile Browser]
    end

    subgraph "Presentation Layer"
        UI[User Interface]
        AD[Admin Dashboard]
        CB[Chatbot Interface]
    end

    subgraph "Application Layer"
        WS[Web Server - Flask]
        subgraph "Core Services"
            BM[Booking Management]
            RM[Room Management]
            AM[Authentication]
            RV[Review System]
            CH[Chatbot Handler]
        end
        subgraph "Utility Services"
            EM[Email Service]
            SA[Sentiment Analysis]
            AN[Analytics Engine]
        end
    end

    subgraph "Data Layer"
        DB[(PostgreSQL Database)]
        FS[File Storage]
    end

    B --> UI
    M --> UI
    UI --> WS
    AD --> WS
    CB --> WS
    
    WS --> BM
    WS --> RM
    WS --> AM
    WS --> RV
    WS --> CH
    
    BM --> DB
    RM --> DB
    AM --> DB
    RV --> DB
    
    RV --> SA
    BM --> EM
    RV --> AN
    RM --> AN
```

## 2. Database Schema

```mermaid
erDiagram
    ROOM {
        int id PK
        string room_number
        string room_type
        boolean availability
        decimal price
    }
    
    BOOKING {
        int id PK
        int room_id FK
        string guest_name
        string guest_email
        date check_in_date
        date check_out_date
        string status
    }
    
    REVIEW {
        int id PK
        int booking_id FK
        string name
        int rating
        text review_text
        datetime created_at
    }
    
    USER {
        int id PK
        string username
        string password_hash
        string role
        datetime last_login
    }

    ROOM ||--o{ BOOKING : "has"
    BOOKING ||--o{ REVIEW : "has"
    USER ||--o{ BOOKING : "manages"
```

## 3. Component Interaction Flow

```mermaid
sequenceDiagram
    participant C as Client
    participant UI as User Interface
    participant S as Server (Flask)
    participant DB as Database
    participant E as Email Service
    participant A as Analytics

    C->>UI: Access Booking Page
    UI->>S: Request Available Rooms
    S->>DB: Query Room Status
    DB-->>S: Return Available Rooms
    S-->>UI: Display Room Options
    
    C->>UI: Submit Booking
    UI->>S: Send Booking Data
    S->>DB: Validate & Save Booking
    S->>E: Send Confirmation Email
    E-->>C: Deliver Email
    DB-->>S: Confirm Save
    S-->>UI: Show Success Message
    
    Note over C,UI: After Stay
    C->>UI: Submit Review
    UI->>S: Send Review Data
    S->>A: Analyze Sentiment
    S->>DB: Save Review & Analysis
    DB-->>S: Confirm Save
    S-->>UI: Show Thank You Message
```

## 4. Admin Dashboard Architecture

```mermaid
graph LR
    subgraph "Admin Interface"
        L[Login]
        D[Dashboard]
        B[Booking Management]
        R[Room Management]
        A[Analytics]
        RV[Review Management]
    end

    subgraph "Admin Services"
        AM[Authentication]
        BM[Booking Handler]
        RM[Room Handler]
        AN[Analytics Engine]
        RH[Review Handler]
    end

    subgraph "Data Storage"
        DB[(Database)]
        C[Cache]
    end

    L --> AM
    AM --> D
    D --> B
    D --> R
    D --> A
    D --> RV
    
    B --> BM
    R --> RM
    A --> AN
    RV --> RH
    
    BM --> DB
    RM --> DB
    AN --> DB
    RH --> DB
    
    AN --> C
```

## 5. Security Implementation

```mermaid
graph TB
    subgraph "Security Layers"
        F[Frontend Security]
        M[Middleware Security]
        B[Backend Security]
        D[Data Security]
    end

    subgraph "Frontend"
        IV[Input Validation]
        XP[XSS Protection]
        CS[CSRF Tokens]
    end

    subgraph "Middleware"
        AF[Authentication]
        AZ[Authorization]
        RT[Rate Limiting]
    end

    subgraph "Backend"
        SE[Session Management]
        PE[Password Encryption]
        AL[Audit Logging]
    end

    subgraph "Data"
        DE[Data Encryption]
        BA[Backup System]
        AC[Access Control]
    end

    F --> IV
    F --> XP
    F --> CS
    
    M --> AF
    M --> AZ
    M --> RT
    
    B --> SE
    B --> PE
    B --> AL
    
    D --> DE
    D --> BA
    D --> AC
```

## 6. Deployment Architecture

```mermaid
graph TB
    subgraph "Client Side"
        C[Client Browser]
    end

    subgraph "Server Infrastructure"
        LB[Load Balancer]
        
        subgraph "Web Servers"
            W1[Web Server 1]
            W2[Web Server 2]
        end
        
        subgraph "Application Servers"
            A1[App Server 1]
            A2[App Server 2]
        end
        
        subgraph "Database Servers"
            M[Master DB]
            S1[Slave DB 1]
            S2[Slave DB 2]
        end
        
        subgraph "Cache Layer"
            R[Redis Cache]
        end
    end

    C --> LB
    LB --> W1
    LB --> W2
    W1 --> A1
    W1 --> A2
    W2 --> A1
    W2 --> A2
    A1 --> M
    A2 --> M
    M --> S1
    M --> S2
    A1 --> R
    A2 --> R
```

These diagrams provide a comprehensive visualization of the hotel booking system's architecture, including:

1. High-Level System Architecture: Shows the overall system structure and component interactions
2. Database Schema: Illustrates the database design and relationships
3. Component Interaction Flow: Demonstrates the booking and review process flow
4. Admin Dashboard Architecture: Details the admin interface and its components
5. Security Implementation: Shows the security measures at different layers
6. Deployment Architecture: Illustrates the production deployment setup

Each diagram is created using Mermaid.js syntax and can be rendered in any Markdown viewer that supports Mermaid diagrams. The diagrams help visualize:

- System components and their relationships
- Data flow between components
- User interaction patterns
- Security implementation
- Deployment structure

These diagrams can be used in your thesis to explain the system's architecture and functionality. 