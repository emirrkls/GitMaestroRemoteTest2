from datetime import datetime

class HotelReservationSystem:
    def __init__(self):
        self.rooms = {
            "101": {"type": "standard", "price_per_night": 100.0, "is_booked": False},
            "102": {"type": "standard", "price_per_night": 100.0, "is_booked": False},
            "201": {"type": "deluxe", "price_per_night": 250.0, "is_booked": False},
            "301": {"type": "suite", "price_per_night": 500.0, "is_booked": False}
        }
        self.reservations = {}
        self.reservation_counter = 1

    def book_room(self, guest_name, room_id, checkin_str, checkout_str):
        if room_id not in self.rooms:
            raise KeyError("Room does not exist")
            
        if self.rooms[room_id]["is_booked"]:
            raise ValueError("Room is already booked")

        fmt = "%Y-%m-%d"
        checkin_date = datetime.strptime(checkin_str, fmt)
        checkout_date = datetime.strptime(checkout_str, fmt)

        nights = (checkout_date - checkin_date).days
        if nights <= 0:
            raise ValueError("Check-out must be after check-in")
        
        res_id = f"RES-{self.reservation_counter}"
        self.reservation_counter += 1
        
        self.reservations[res_id] = {
            "guest_name": guest_name,
            "room_id": room_id,
            "checkin": checkin_date,
            "checkout": checkout_date,
            "nights": nights,
            "status": "ACTIVE"
        }
        
        self.rooms[room_id]["is_booked"] = True
        return res_id

    def cancel_reservation(self, res_id):
        if res_id not in self.reservations:
            return False
            
        res = self.reservations[res_id]
        if res["status"] == "CANCELLED":
            return False
            
        res["status"] = "CANCELLED"
        self.rooms[res["room_id"]]["is_booked"] = False
        
        return True

    def generate_invoice(self, res_id, extra_charges=None):
        if res_id not in self.reservations:
            raise KeyError("Reservation not found")
            
        res = self.reservations[res_id]
        room = self.rooms[res["room_id"]]
        
        base_cost = room["price_per_night"] * res["nights"]
        
        # Simulate an automatic cleaning fee added to extra charges
        if extra_charges is None:
            extra_charges = []
        extra_charges = list(extra_charges) + [25.0]
        
        total_extras = sum(extra_charges)
        total_amount = base_cost + total_extras
        
        return {
            "guest_name": res["guest_name"],
            "base_cost": base_cost,
            "extras": total_extras,
            "total_amount": total_amount
        }
