# Full-Stack-Event-Management-with-Ticket-Booking-Platform
# GatherGo - Event Management with Ticket Booking Platform

GatherGo is a full-stack Event Management and Ticket Booking platform. Users can discover events, select interactive seat layouts, book tickets, simulate payments, view digital confirmed tickets with real-time QR code generation, and view booking history via a personalized dashboard. Organizers and Administrators have complete CRUD portals to manage events, venues, bookings, payments, and users.

---

## 🚀 Technology Stack

### Frontend
- **HTML5 & CSS3**: Elegant custom styles featuring dark mode glassmorphic interfaces and responsive layouts.
- **JavaScript (ES6)**: Modern client logic handling states, sessions, QR ticket rendering, and dynamic page binds.
- **Fetch API**: Smooth AJAX integration to backend endpoints.

### Backend
- **Django**: Fast python backend framework utilizing function-based views.
- **Django REST Framework (DRF)**: Handles API decorators, request data parsing, and JSON response formatting.
- **PyMongo**: Direct interface with MongoDB Atlas database (bypassing local SQL).
- **python-dotenv**: Securely loads database secrets.

### Database
- **MongoDB Atlas**: Cloud-hosted NoSQL cluster holding collections for `users`, `events`, `venues`, `bookings`, `payments`, and auto-incrementing `counters`.

---

## 📂 Project Folder Structure

```text
EventManagementSystem/
│
├── Backend/
│   ├── __init__.py
│   ├── asgi.py
│   ├── db.py               # MongoDB connection and database seeding configuration
│   ├── settings.py         # Django settings, CORS headers, and DRF setup
│   ├── urls.py             # Route mappings for all 20 REST APIs
│   ├── views.py            # Function-based CRUD views
│   └── wsgi.py
│
├── Frontend/
│   ├── index.html          # Home / Hero Search page
│   ├── login.html          # Login console
│   ├── register.html       # Signup form
│   ├── events.html         # Interactive category event browser
│   ├── event_details.html  # Event information and reviews module
│   ├── booking.html        # Seat selection and booking calculator
│   ├── payment.html        # simulated checkout gateway
│   ├── booking_history.html# Digital ticket vault and QR code scanner
│   ├── user_dashboard.html # Attendee dashboard analytics
│   ├── organizer_dashboard.html # Organizer CRUD panel
│   ├── admin_dashboard.html# Global administrative database management
│   ├── style.css           # Global glassmorphic stylesheet
│   └── script.js           # Client API integrations and auth checks
│
├── manage.py
└── .env                    # Secure environment secrets
```

---

## 🛠️ Installation & Setup

### 1. Prerequisite
Ensure you have **Python 3.8+** installed.

### 2. Configure Environment variables
Create a `.env` file at the root of the project (if not present) and add your MongoDB connection string:
```env
MONGODB_URI=your url...
SECRET_KEY=django-insecure-event-booking-platform-key-2026-secret
DEBUG=True
```

### 3. Setup Virtual Environment
Open terminal in the project root directory and run:
```powershell
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\activate

# Install required dependencies
pip install django djangorestframework django-cors-headers pymongo python-dotenv dnspython
```

### 4. Seed and Start the Django Server
The database connection includes automatic self-seeding on launch. Simply run:
```powershell
python EventManagementSystem/manage.py runserver
```
The server will boot up on `http://127.0.0.1:8000` and automatically verify the connection and seed initial sample data into your MongoDB Atlas cluster.

### 5. Launch Frontend
Since the frontend uses HTML5/JS files, you can open `EventManagementSystem/Frontend/index.html` directly in any web browser, or use a local development server like VS Code Live Server.

---

## 🔑 Default Roles & Accounts for Testing
On launching, the system seeds sample accounts into the MongoDB Atlas database for immediate testing:

1. **Attendee / User**:
   - **Email**: `rahul@gmail.com` | **Password**: `rahul123`
2. **Event Organizer**:
   - **Email**: `organizer@gmail.com` | **Password**: `organizer123` *(Matches seeded events under organizer name "Tech Events Pvt Ltd")*
3. **Administrator**:
   - **Email**: `admin@gmail.com` | **Password**: `admin123`

---

## 📡 API Reference Checklist (20 APIs)

### 1. User Management (4 APIs)
- `POST /users/add/` : Register a user (generates numeric `user_id` starting from 101).
- `GET /users/` : Retrieve all users (or filter by query `?email=...`).
- `PUT /users/update/<id>/` : Update user profile by ID.
- `DELETE /users/delete/<id>/` : Remove user record by ID.

### 2. Event Management (4 APIs)
- `POST /events/add/` : Add event (generates numeric `event_id` starting from 201).
- `GET /events/` : Get events list (supports `?search=...` and `?category=...`).
- `PUT /events/update/<id>/` : Modify event details.
- `DELETE /events/delete/<id>/` : Delete event.

### 3. Venue Management (4 APIs)
- `POST /venues/add/` : Create venue (generates numeric `venue_id` starting from 301).
- `GET /venues/` : Get venues list.
- `PUT /venues/update/<id>/` : Update venue fields.
- `DELETE /venues/delete/<id>/` : Delete venue.

### 4. Ticket Booking (4 APIs)
- `POST /bookings/add/` : Create a ticket booking (decreases event ticket availability).
- `GET /bookings/` : Get bookings list (supports `?user_name=...` filter).
- `PUT /bookings/update/<id>/` : Update status (cancelling a booking restores event tickets).
- `DELETE /bookings/delete/<id>/` : Remove booking.

### 5. Payment Management (4 APIs)
- `POST /payments/add/` : Add payment (success status updates booking status to "Confirmed").
- `GET /payments/` : Get payments log list (supports `?user_name=...` filter).
- `PUT /payments/update/<id>/` : Edit payment transaction records.
- `DELETE /payments/delete/<id>/` : Delete transaction.

---

## ✨ Implemented Bonus Features (20 / 20 Marks)

1. **Event Search & Category Filters (4 Marks)**: Interactive query filters in `events.html` searching by title/venue and filtering by Category dropdown.
2. **Seat Selection Layout (4 Marks)**: Custom visual theater seating grid in `booking.html` allowing users to select up to 5 seats dynamically.
3. **QR Code Ticket Generation (4 Marks)**: Renders live scannable digital tickets containing structured booking verification payloads using secure QR APIs.
4. **Event Reminder Notifications (4 Marks)**: Slides in responsive micro-notification banners warning users of upcoming bookings.
5. **Event Reviews & Ratings (4 Marks)**: Star rating reviews module allowing attendees to rate and submit comments on event detail pages.
