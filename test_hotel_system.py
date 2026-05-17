import unittest
from hotel_system import HotelReservationSystem

class TestHotelReservationSystem(unittest.TestCase):
    def setUp(self):
        self.hotel = HotelReservationSystem()

    def test_negative_nights_validation(self):
        # Booking with checkout BEFORE checkin should raise an error, not create a negative invoice
        try:
            res_id = self.hotel.book_room("Alice", "101", "2026-06-10", "2026-06-05")
            invoice = self.hotel.generate_invoice(res_id)
            if invoice["base_cost"] <= 0:
                self.fail("System allowed booking with negative/zero nights, resulting in invalid cost.")
        except ValueError:
            pass

    def test_cancel_frees_room(self):
        # Book a room, cancel it, then try to book it again.
        res_id1 = self.hotel.book_room("Bob", "201", "2026-07-01", "2026-07-05")
        self.hotel.cancel_reservation(res_id1)
        
        # Should be able to book the same room again.
        try:
            res_id2 = self.hotel.book_room("Charlie", "201", "2026-07-10", "2026-07-12")
            self.assertIsNotNone(res_id2)
        except ValueError as e:
            self.fail(f"Could not book room after cancellation. Reason: {e}")

    def test_invoice_extra_charges_isolation(self):
        # Generate an invoice for Dave
        res_id_dave = self.hotel.book_room("Dave", "301", "2026-08-01", "2026-08-02")
        invoice1 = self.hotel.generate_invoice(res_id_dave)
        self.assertEqual(invoice1["total_amount"], 525.0)
        
        # Generate an invoice for Eve
        res_id_eve = self.hotel.book_room("Eve", "102", "2026-08-05", "2026-08-06")
        invoice2 = self.hotel.generate_invoice(res_id_eve)
        self.assertEqual(invoice2["total_amount"], 125.0, "Extra charges leaked from previous invoice!")

if __name__ == '__main__':
    unittest.main()
