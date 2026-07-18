import os
import pymongo
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB connection string from environment or default
MONGODB_URI = os.getenv("MONGODB_URI")
if not MONGODB_URI:
    raise ValueError("MONGODB_URI environment variable not found in .env file.")

print(f"Connecting to MongoDB Atlas...")
client = pymongo.MongoClient(MONGODB_URI)
db = client['event_booking_db']

def get_next_sequence_value(sequence_name):
    """
    Generate auto-incrementing numeric IDs for collections (e.g. users, events, venues).
    """
    counter = db.counters.find_one_and_update(
        {'_id': sequence_name},
        {'$inc': {'sequence_value': 1}},
        upsert=True,
        return_document=pymongo.ReturnDocument.AFTER
    )
    return counter['sequence_value']

def seed_database():
    """
    Seeds the database with sample data if it's empty, and initializes counters.
    """
    # 1. Seed Counters
    # We initialize counters to match sample data starting values so that:
    # - Users start at 101
    # - Events start at 201
    # - Venues start at 301
    # - Bookings start at 401
    # - Payments start at 501
    
    # Initialize counters if not present
    counter_init = [
        {'_id': 'user_id', 'sequence_value': 101},
        {'_id': 'event_id', 'sequence_value': 201},
        {'_id': 'venue_id', 'sequence_value': 301},
        {'_id': 'booking_id', 'sequence_value': 401},
        {'_id': 'payment_id', 'sequence_value': 501}
    ]
    for c in counter_init:
        if db.counters.count_documents({'_id': c['_id']}) == 0:
            db.counters.insert_one(c)
            print(f"Initialized counter: {c['_id']} to {c['sequence_value']}")

    # 2. Seed Users
    if db.users.count_documents({}) == 0:
        sample_user = {
            "user_id": 101,
            "full_name": "Rahul Sharma",
            "email": "rahul@gmail.com",
            "phone": "9876543210",
            "city": "Hyderabad",
            "password": "rahul123"
        }
        db.users.insert_one(sample_user)
        print("Seeded sample user.")

    # 3. Seed Venues
    if db.venues.count_documents({}) == 0:
        sample_venue = {
            "venue_id": 301,
            "venue_name": "Bangalore International Convention Center",
            "location": "Whitefield",
            "city": "Bangalore",
            "capacity": 1000,
            "contact_person": "Anil Kumar"
        }
        db.venues.insert_one(sample_venue)
        print("Seeded sample venue.")

    # 4. Seed Events
    if db.events.count_documents({}) == 0:
        sample_event = {
            "event_id": 201,
            "event_name": "Tech Innovation Summit 2026",
            "category": "Conference",
            "organizer_name": "Tech Events Pvt Ltd",
            "event_date": "2026-09-15",
            "event_time": "10:00",
            "venue": "Bangalore International Convention Center",
            "ticket_price": 1500,
            "available_tickets": 500
        }
        db.events.insert_one(sample_event)
        
        # Add some extra events for variety
        db.events.insert_many([
            {
                "event_id": 202,
                "event_name": "Acoustic Rock Night",
                "category": "Music Concert",
                "organizer_name": "Live Nation",
                "event_date": "2026-08-20",
                "event_time": "18:30",
                "venue": "BICC Arena",
                "ticket_price": 800,
                "available_tickets": 300
            },
            {
                "event_id": 203,
                "event_name": "UI/UX Design Masterclass",
                "category": "Workshop",
                "organizer_name": "Creative Guild",
                "event_date": "2026-07-28",
                "event_time": "11:00",
                "venue": "Innovators Hub",
                "ticket_price": 1200,
                "available_tickets": 45
            }
        ])
        # Update event counter
        db.counters.update_one({'_id': 'event_id'}, {'$set': {'sequence_value': 203}})
        print("Seeded sample events.")

    # 5. Seed Bookings
    if db.bookings.count_documents({}) == 0:
        sample_booking = {
            "booking_id": 401,
            "user_name": "Rahul Sharma",
            "event_name": "Tech Innovation Summit 2026",
            "booking_date": "2026-08-20",
            "number_of_tickets": 2,
            "total_amount": 3000,
            "booking_status": "Confirmed"
        }
        db.bookings.insert_one(sample_booking)
        print("Seeded sample booking.")

    # 6. Seed Payments
    if db.payments.count_documents({}) == 0:
        sample_payment = {
            "payment_id": 501,
            "booking_id": 401,
            "user_name": "Rahul Sharma",
            "amount": 3000,
            "payment_method": "UPI",
            "payment_status": "Success",
            "transaction_id": "TXN987654321",
            "payment_date": "2026-08-20"
        }
        db.payments.insert_one(sample_payment)
        print("Seeded sample payment.")

# Run seeding function when this module is imported or on server startup
try:
    seed_database()
except Exception as e:
    print(f"Error seeding database: {e}")
