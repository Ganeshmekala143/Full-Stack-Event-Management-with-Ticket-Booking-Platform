from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .db import db, get_next_sequence_value
import datetime

# ----------------- MODULE 1: USER MANAGEMENT -----------------

@api_view(['POST'])
def add_user(request):
    """
    POST /users/add/
    Add a new user. Generates user_id starting from 101.
    """
    data = request.data
    
    # Required fields validation
    required_fields = ['full_name', 'email', 'phone', 'city', 'password']
    for field in required_fields:
        if field not in data or not str(data[field]).strip():
            return Response({"error": f"Field '{field}' is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    # Check duplicate email
    if db.users.find_one({'email': data['email']}):
        return Response({"error": "Email is already registered."}, status=status.HTTP_400_BAD_REQUEST)
    
    user_id = get_next_sequence_value('user_id')
    user_doc = {
        "user_id": user_id,
        "full_name": data['full_name'],
        "email": data['email'],
        "phone": data['phone'],
        "city": data['city'],
        "password": data['password'] # For educational project simplicity, stored plain-text
    }
    db.users.insert_one(user_doc)
    
    # Return user details excluding mongo _id
    user_doc.pop('_id', None)
    return Response(user_doc, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_users(request):
    """
    GET /users/
    Retrieve all users. Supports email filtering via query params: ?email=...
    """
    email = request.query_params.get('email')
    if email:
        user = db.users.find_one({'email': email}, {'_id': 0})
        if user:
            return Response(user, status=status.HTTP_200_OK)
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
    users = list(db.users.find({}, {'_id': 0}))
    return Response(users, status=status.HTTP_200_OK)

@api_view(['PUT'])
def update_user(request, pk):
    """
    PUT /users/update/<id>/
    Update an existing user by user_id (pk).
    """
    try:
        user_id = int(pk)
    except ValueError:
        return Response({"error": "Invalid ID format."}, status=status.HTTP_400_BAD_REQUEST)

    user = db.users.find_one({'user_id': user_id})
    if not user:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
    data = request.data
    update_fields = {}
    for field in ['full_name', 'email', 'phone', 'city', 'password']:
        if field in data:
            update_fields[field] = data[field]
            
    if update_fields:
        db.users.update_one({'user_id': user_id}, {'$set': update_fields})
        
    updated_user = db.users.find_one({'user_id': user_id}, {'_id': 0})
    return Response(updated_user, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_user(request, pk):
    """
    DELETE /users/delete/<id>/
    Delete user by user_id (pk).
    """
    try:
        user_id = int(pk)
    except ValueError:
        return Response({"error": "Invalid ID format."}, status=status.HTTP_400_BAD_REQUEST)

    result = db.users.delete_one({'user_id': user_id})
    if result.deleted_count > 0:
        return Response({"message": "User deleted successfully."}, status=status.HTTP_200_OK)
    return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)


# ----------------- MODULE 2: EVENT MANAGEMENT -----------------

@api_view(['POST'])
def add_event(request):
    """
    POST /events/add/
    Add a new event. Generates event_id starting from 201.
    """
    data = request.data
    required_fields = ['event_name', 'category', 'organizer_name', 'event_date', 'event_time', 'venue', 'ticket_price', 'available_tickets']
    for field in required_fields:
        if field not in data or data[field] is None:
            return Response({"error": f"Field '{field}' is required."}, status=status.HTTP_400_BAD_REQUEST)

    event_id = get_next_sequence_value('event_id')
    event_doc = {
        "event_id": event_id,
        "event_name": data['event_name'],
        "category": data['category'],
        "organizer_name": data['organizer_name'],
        "event_date": data['event_date'],
        "event_time": data['event_time'],
        "venue": data['venue'],
        "ticket_price": float(data['ticket_price']),
        "available_tickets": int(data['available_tickets'])
    }
    db.events.insert_one(event_doc)
    
    event_doc.pop('_id', None)
    return Response(event_doc, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_events(request):
    """
    GET /events/
    Retrieve all events. Supports optional query parameters for search and category filters.
    - search: event_name or venue search
    - category: Music Concert, Workshop, etc.
    """
    query = {}
    search = request.query_params.get('search')
    category = request.query_params.get('category')
    
    if search:
        query['$or'] = [
            {'event_name': {'$regex': search, '$options': 'i'}},
            {'venue': {'$regex': search, '$options': 'i'}}
        ]
    if category:
        query['category'] = category
        
    events = list(db.events.find(query, {'_id': 0}))
    return Response(events, status=status.HTTP_200_OK)

@api_view(['PUT'])
def update_event(request, pk):
    """
    PUT /events/update/<id>/
    Update event details by event_id (pk).
    """
    try:
        event_id = int(pk)
    except ValueError:
        return Response({"error": "Invalid ID format."}, status=status.HTTP_400_BAD_REQUEST)

    event = db.events.find_one({'event_id': event_id})
    if not event:
        return Response({"error": "Event not found."}, status=status.HTTP_404_NOT_FOUND)

    data = request.data
    update_fields = {}
    for field in ['event_name', 'category', 'organizer_name', 'event_date', 'event_time', 'venue', 'ticket_price', 'available_tickets']:
        if field in data:
            if field == 'ticket_price':
                update_fields[field] = float(data[field])
            elif field == 'available_tickets':
                update_fields[field] = int(data[field])
            else:
                update_fields[field] = data[field]

    if update_fields:
        db.events.update_one({'event_id': event_id}, {'$set': update_fields})

    updated_event = db.events.find_one({'event_id': event_id}, {'_id': 0})
    return Response(updated_event, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_event(request, pk):
    """
    DELETE /events/delete/<id>/
    Delete event by event_id (pk).
    """
    try:
        event_id = int(pk)
    except ValueError:
        return Response({"error": "Invalid ID format."}, status=status.HTTP_400_BAD_REQUEST)

    result = db.events.delete_one({'event_id': event_id})
    if result.deleted_count > 0:
        return Response({"message": "Event deleted successfully."}, status=status.HTTP_200_OK)
    return Response({"error": "Event not found."}, status=status.HTTP_404_NOT_FOUND)


# ----------------- MODULE 3: VENUE MANAGEMENT -----------------

@api_view(['POST'])
def add_venue(request):
    """
    POST /venues/add/
    Add a new venue. Generates venue_id starting from 301.
    """
    data = request.data
    required_fields = ['venue_name', 'location', 'city', 'capacity', 'contact_person']
    for field in required_fields:
        if field not in data or data[field] is None:
            return Response({"error": f"Field '{field}' is required."}, status=status.HTTP_400_BAD_REQUEST)

    venue_id = get_next_sequence_value('venue_id')
    venue_doc = {
        "venue_id": venue_id,
        "venue_name": data['venue_name'],
        "location": data['location'],
        "city": data['city'],
        "capacity": int(data['capacity']),
        "contact_person": data['contact_person']
    }
    db.venues.insert_one(venue_doc)

    venue_doc.pop('_id', None)
    return Response(venue_doc, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_venues(request):
    """
    GET /venues/
    Retrieve all venues.
    """
    venues = list(db.venues.find({}, {'_id': 0}))
    return Response(venues, status=status.HTTP_200_OK)

@api_view(['PUT'])
def update_venue(request, pk):
    """
    PUT /venues/update/<id>/
    Update venue details by venue_id (pk).
    """
    try:
        venue_id = int(pk)
    except ValueError:
        return Response({"error": "Invalid ID format."}, status=status.HTTP_400_BAD_REQUEST)

    venue = db.venues.find_one({'venue_id': venue_id})
    if not venue:
        return Response({"error": "Venue not found."}, status=status.HTTP_404_NOT_FOUND)

    data = request.data
    update_fields = {}
    for field in ['venue_name', 'location', 'city', 'capacity', 'contact_person']:
        if field in data:
            if field == 'capacity':
                update_fields[field] = int(data[field])
            else:
                update_fields[field] = data[field]

    if update_fields:
        db.venues.update_one({'venue_id': venue_id}, {'$set': update_fields})

    updated_venue = db.venues.find_one({'venue_id': venue_id}, {'_id': 0})
    return Response(updated_venue, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_venue(request, pk):
    """
    DELETE /venues/delete/<id>/
    Delete venue by venue_id (pk).
    """
    try:
        venue_id = int(pk)
    except ValueError:
        return Response({"error": "Invalid ID format."}, status=status.HTTP_400_BAD_REQUEST)

    result = db.venues.delete_one({'venue_id': venue_id})
    if result.deleted_count > 0:
        return Response({"message": "Venue deleted successfully."}, status=status.HTTP_200_OK)
    return Response({"error": "Venue not found."}, status=status.HTTP_404_NOT_FOUND)


# ----------------- MODULE 4: TICKET BOOKING MANAGEMENT -----------------

@api_view(['POST'])
def add_booking(request):
    """
    POST /bookings/add/
    Creates a booking. Automatically deducts available tickets from event.
    """
    data = request.data
    required_fields = ['user_name', 'event_name', 'booking_date', 'number_of_tickets', 'total_amount']
    for field in required_fields:
        if field not in data or data[field] is None:
            return Response({"error": f"Field '{field}' is required."}, status=status.HTTP_400_BAD_REQUEST)

    num_tickets = int(data['number_of_tickets'])
    
    # Retrieve the event
    event = db.events.find_one({'event_name': data['event_name']})
    if not event:
        return Response({"error": f"Event '{data['event_name']}' not found."}, status=status.HTTP_404_NOT_FOUND)
        
    if event['available_tickets'] < num_tickets:
        return Response({"error": f"Not enough tickets available. Only {event['available_tickets']} left."}, status=status.HTTP_400_BAD_REQUEST)

    # Deduct tickets from Event
    db.events.update_one({'event_id': event['event_id']}, {'$inc': {'available_tickets': -num_tickets}})

    booking_id = get_next_sequence_value('booking_id')
    booking_doc = {
        "booking_id": booking_id,
        "user_name": data['user_name'],
        "event_name": data['event_name'],
        "booking_date": data['booking_date'],
        "number_of_tickets": num_tickets,
        "total_amount": float(data['total_amount']),
        "booking_status": data.get('booking_status', 'Pending') # Defaults to Pending until paid
    }
    db.bookings.insert_one(booking_doc)

    booking_doc.pop('_id', None)
    return Response(booking_doc, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_bookings(request):
    """
    GET /bookings/
    Retrieve bookings. Can filter by user_name.
    """
    query = {}
    user_name = request.query_params.get('user_name')
    if user_name:
        query['user_name'] = user_name

    bookings = list(db.bookings.find(query, {'_id': 0}))
    return Response(bookings, status=status.HTTP_200_OK)

@api_view(['PUT'])
def update_booking(request, pk):
    """
    PUT /bookings/update/<id>/
    Update booking details. If cancelled, restores the tickets.
    """
    try:
        booking_id = int(pk)
    except ValueError:
        return Response({"error": "Invalid ID format."}, status=status.HTTP_400_BAD_REQUEST)

    booking = db.bookings.find_one({'booking_id': booking_id})
    if not booking:
        return Response({"error": "Booking not found."}, status=status.HTTP_404_NOT_FOUND)

    data = request.data
    update_fields = {}
    for field in ['user_name', 'event_name', 'booking_date', 'number_of_tickets', 'total_amount', 'booking_status']:
        if field in data:
            update_fields[field] = data[field]

    # Handle ticket restoration on Cancellation
    if 'booking_status' in update_fields and update_fields['booking_status'] == 'Cancelled' and booking['booking_status'] != 'Cancelled':
        # Find event and restore tickets
        event = db.events.find_one({'event_name': booking['event_name']})
        if event:
            db.events.update_one({'event_id': event['event_id']}, {'$inc': {'available_tickets': booking['number_of_tickets']}})

    # Handle ticket re-booking if status changes from Cancelled back to Confirmed/Pending
    elif 'booking_status' in update_fields and update_fields['booking_status'] in ['Confirmed', 'Pending'] and booking['booking_status'] == 'Cancelled':
        event = db.events.find_one({'event_name': booking['event_name']})
        if event:
            if event['available_tickets'] < booking['number_of_tickets']:
                return Response({"error": "Cannot restore booking, no tickets available."}, status=status.HTTP_400_BAD_REQUEST)
            db.events.update_one({'event_id': event['event_id']}, {'$inc': {'available_tickets': -booking['number_of_tickets']}})

    if update_fields:
        db.bookings.update_one({'booking_id': booking_id}, {'$set': update_fields})

    updated_booking = db.bookings.find_one({'booking_id': booking_id}, {'_id': 0})
    return Response(updated_booking, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_booking(request, pk):
    """
    DELETE /bookings/delete/<id>/
    Deletes booking and restores tickets if the booking was not already Cancelled.
    """
    try:
        booking_id = int(pk)
    except ValueError:
        return Response({"error": "Invalid ID format."}, status=status.HTTP_400_BAD_REQUEST)

    booking = db.bookings.find_one({'booking_id': booking_id})
    if not booking:
        return Response({"error": "Booking not found."}, status=status.HTTP_404_NOT_FOUND)

    # Restore tickets if it wasn't cancelled
    if booking['booking_status'] != 'Cancelled':
        event = db.events.find_one({'event_name': booking['event_name']})
        if event:
            db.events.update_one({'event_id': event['event_id']}, {'$inc': {'available_tickets': booking['number_of_tickets']}})

    db.bookings.delete_one({'booking_id': booking_id})
    return Response({"message": "Booking deleted successfully."}, status=status.HTTP_200_OK)


# ----------------- MODULE 5: PAYMENT MANAGEMENT -----------------

@api_view(['POST'])
def add_payment(request):
    """
    POST /payments/add/
    Log a payment and update the corresponding ticket booking status to "Confirmed".
    """
    data = request.data
    required_fields = ['booking_id', 'user_name', 'amount', 'payment_method', 'payment_status', 'transaction_id', 'payment_date']
    for field in required_fields:
        if field not in data or data[field] is None:
            return Response({"error": f"Field '{field}' is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        booking_id = int(data['booking_id'])
    except ValueError:
        return Response({"error": "booking_id must be a numeric value."}, status=status.HTTP_400_BAD_REQUEST)

    payment_id = get_next_sequence_value('payment_id')
    payment_doc = {
        "payment_id": payment_id,
        "booking_id": booking_id,
        "user_name": data['user_name'],
        "amount": float(data['amount']),
        "payment_method": data['payment_method'],
        "payment_status": data['payment_status'],
        "transaction_id": data['transaction_id'],
        "payment_date": data['payment_date']
    }
    db.payments.insert_one(payment_doc)

    # If payment was successful, update booking status to Confirmed
    if data['payment_status'] == 'Success':
        db.bookings.update_one({'booking_id': booking_id}, {'$set': {'booking_status': 'Confirmed'}})

    payment_doc.pop('_id', None)
    return Response(payment_doc, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_payments(request):
    """
    GET /payments/
    Retrieve all payments. Can filter by user_name.
    """
    query = {}
    user_name = request.query_params.get('user_name')
    if user_name:
        query['user_name'] = user_name

    payments = list(db.payments.find(query, {'_id': 0}))
    return Response(payments, status=status.HTTP_200_OK)

@api_view(['PUT'])
def update_payment(request, pk):
    """
    PUT /payments/update/<id>/
    Update payment details by payment_id (pk).
    """
    try:
        payment_id = int(pk)
    except ValueError:
        return Response({"error": "Invalid ID format."}, status=status.HTTP_400_BAD_REQUEST)

    payment = db.payments.find_one({'payment_id': payment_id})
    if not payment:
        return Response({"error": "Payment record not found."}, status=status.HTTP_404_NOT_FOUND)

    data = request.data
    update_fields = {}
    for field in ['booking_id', 'user_name', 'amount', 'payment_method', 'payment_status', 'transaction_id', 'payment_date']:
        if field in data:
            if field == 'amount':
                update_fields[field] = float(data[field])
            elif field == 'booking_id':
                update_fields[field] = int(data[field])
            else:
                update_fields[field] = data[field]

    # If status changes to Success, make sure booking status is updated too
    if 'payment_status' in update_fields and update_fields['payment_status'] == 'Success':
        booking_id = update_fields.get('booking_id', payment['booking_id'])
        db.bookings.update_one({'booking_id': booking_id}, {'$set': {'booking_status': 'Confirmed'}})

    if update_fields:
        db.payments.update_one({'payment_id': payment_id}, {'$set': update_fields})

    updated_payment = db.payments.find_one({'payment_id': payment_id}, {'_id': 0})
    return Response(updated_payment, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_payment(request, pk):
    """
    DELETE /payments/delete/<id>/
    Delete payment record by payment_id (pk).
    """
    try:
        payment_id = int(pk)
    except ValueError:
        return Response({"error": "Invalid ID format."}, status=status.HTTP_400_BAD_REQUEST)

    result = db.payments.delete_one({'payment_id': payment_id})
    if result.deleted_count > 0:
        return Response({"message": "Payment record deleted successfully."}, status=status.HTTP_200_OK)
    return Response({"error": "Payment record not found."}, status=status.HTTP_404_NOT_FOUND)
