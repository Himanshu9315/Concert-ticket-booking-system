from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

class Event:
    events = []

    def __init__(self, name, date, total_tickets):
        self.name = name
        self.date = date
        self.total_tickets = total_tickets
        self.available_tickets = total_tickets
        Event.events.append(self)

    def __str__(self):
        return f"Event: {self.name} | Date: {self.date} | Available Tickets: {self.available_tickets}"

class Ticket:
    def __init__(self, event, user):
        self.event = event
        self.user = user
        self.is_booked = True

    def __str__(self):
        return f"Ticket for '{self.event.name}' booked by {self.user.name} ({self.user.phone_number})"

    def save_as_pdf(self):
        filename = f"ticket_{self.user.name}_{self.event.name}.pdf"
        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter
        # Add content to the PDF
        c.drawString(1 * inch, height - 1 * inch, "Ticket Confirmation")
        c.drawString(1 * inch, height - 1.5 * inch, f"Event: {self.event.name}")
        c.drawString(1 * inch, height - 2 * inch, f"Date: {self.event.date}")
        c.drawString(1 * inch, height - 2.5 * inch, f"Booked By: {self.user.name}")
        c.drawString(1 * inch, height - 3 * inch, f"Email: {self.user.email}")
        c.drawString(1 * inch, height - 3.5 * inch, f"Phone Number: {self.user.phone_number}")
        c.drawString(1 * inch, height - 4 * inch, f"Aadhar Number: {self.user.aadhar_number}")
        c.save()
        print(f"Ticket saved as PDF: {filename}")

class User:
    def __init__(self, name, email, phone_number, aadhar_number):
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.aadhar_number = aadhar_number
        self.booked_tickets = []

    def book_ticket(self, event, booking_manager):
        if event.available_tickets > 0:
            ticket = booking_manager.create_ticket(event, self)
            self.booked_tickets.append(ticket)
            event.available_tickets -= 1
            ticket.save_as_pdf()
            return ticket
        else:
            raise Exception("You missed out! No tickets available")

    def cancel_ticket(self, ticket, booking_manager):
        if ticket in self.booked_tickets:
            self.booked_tickets.remove(ticket)
            ticket.event.available_tickets += 1
            booking_manager.remove_ticket(ticket)
            return True
        else:
            raise Exception("Ticket not found in your bookings")

class BookingManager:
    def __init__(self):
        self.tickets = []

    def create_ticket(self, event, user):
        ticket = Ticket(event, user)
        self.tickets.append(ticket)
        return ticket

    def remove_ticket(self, ticket):
        if ticket in self.tickets:
            self.tickets.remove(ticket)
            return True
        else:
            raise Exception("Ticket not found in the booking manager")

    def view_events(self):
        for event in Event.events:
            print(event)

    def view_user_bookings(self, user):
        if user.booked_tickets:
            for ticket in user.booked_tickets:
                print(ticket)
        else:
            print("No bookings found")

# Example Usage
def main():
    event1 = Event("Coldplay Concert", "18-01-2024", 100)
    event2 = Event("Ed Sheeran Concert", "15-02-2024", 100)
    event3 = Event("Arijit Singh Concert", "27-01-2024", 100)
    event4 = Event("Karan Aujla", "17-12-2024", 100)
    booking_manager = BookingManager()

    print("Events Available:")
    booking_manager.view_events()

    name = input("Enter your name: ")
    email = input("Enter your email: ")
    phone_number = input("Enter your phone number: ")
    aadhar_number = input("Enter your Aadhar Number: ")
    user = User(name, email, phone_number, aadhar_number)

    event_name = input("Choose your event: ")
    event = next((e for e in Event.events if e.name.lower() == event_name.lower()), None)
    if event is None:
        print("Event not found")
        return

    try:
        ticket = user.book_ticket(event, booking_manager)
        print(f"Ticket booked successfully for {user.name}")
    except Exception as e:
        print(f"Error: {e}")

    print('\nYour Bookings:')
    booking_manager.view_user_bookings(user)

    cancel = input("Do you want to cancel the ticket? (yes/no): ")
    if cancel.lower() == "yes":
        if user.booked_tickets:
            ticket_to_cancel = user.booked_tickets[0]
            user.cancel_ticket(ticket_to_cancel, booking_manager)
            print(f"Successfully cancelled: {ticket_to_cancel}")
        else:
            print("No tickets to cancel")

    print("\nAvailable Events after bookings:")
    booking_manager.view_events()

if __name__ == "__main__":
    main()
