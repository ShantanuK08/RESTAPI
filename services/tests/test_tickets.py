import unittest
import requests

class TestTicketsAPI(unittest.TestCase):
    url = "http://127.0.0.1:5000/tickets"
    

    def test_01_get_tickets(self):
        """Test the GET /tickets endpoint returns 1 record"""
        response = requests.get(self.url)
        
        # Assert status code is 200 (OK)
        self.assertEqual(response.status_code, 200)    
       
        # Convert the response JSON to a list and check the length
        tickets = response.json()
        self.assertEqual(len(tickets), 4)

    def test_02_get_ticket_not_found(self):
        """Test that a GET request for a non-existent ticket returns 404"""
        response = requests.get(self.url + '/999')  # Assuming ID 999 doesn't exist
        self.assertEqual(response.status_code, 404)
        self.assertIn("Ticket not found", response.json().get("error"))


    def test_03_create_ticket(self):
        """Test the POST /tickets endpoint to create a new ticket"""
        url = "http://127.0.0.1:5000/tickets"
        data = {
            "name": "John Doe",
            "from": "City A",
            "to": "City B",
            "day": "Monday"
        }
        
        response = requests.post(url, json=data)
        
        # Assert status code is 201 (Created)
        self.assertEqual(response.status_code, 201, f"Expected status code 201 but got {response.status_code}")
        
        # Assert the response message indicates successful creation
        self.assertEqual(response.json().get("message"), "Ticket created successfully")
        
        # Optionally, you can verify that the created ticket is actually present by querying the tickets list
        response_get = requests.get(url)
        tickets = response_get.json()
        self.assertGreater(len(tickets), 0, "Expected at least one ticket to be created")


    def test_04_get_ticket_not_found(self):
        """Test that a GET request for a non-existent ticket returns 404"""
        # Try to get the details of ticket with ID 2 (which doesn't exist)
        response = requests.get(f"{self.url}/1")
        
        # Assert status code is 404 (Not Found)
        self.assertEqual(response.status_code, 404, f"Expected status code 404 but got {response.status_code}")
        
        # Assert that the error message is as expected
        response_data = response.json()
        self.assertIn("Ticket not found", response_data["error"], f"Expected error message, but got: {response_data}")

    def test_05_update_existing_ticket(self):
        """Test that a PUT request successfully updates an existing ticket"""
        data = {
            "name": "John",
            "from": "City A",
            "to": "City B",
            "day": "Tuesday"
        }

        # Sending PUT request to update ticket with ID 1 (which exists in the database)
        response = requests.put(f"{self.url}/1", json=data)

        # Assert status code is 200 (OK)
        self.assertEqual(response.status_code, 200, f"Expected status code 200 but got {response.status_code}")

        # Assert the success message
        response_data = response.json()
        self.assertIn("Ticket updated successfully", response_data["message"], f"Expected 'Ticket updated successfully' message, but got: {response_data}")


    def test_06_get_updated_ticket(self):
        """Test that a GET request after updating a ticket should return the correct ticket"""
        
        # Sending a PUT request to update ticket with ID 1
        update_data = {
            "name": "John",
            "from": "City A",
            "to": "City B",
            "day": "Tuesday"
        }
        response = requests.put(f"{self.url}/1", json=update_data)
        
        # Assert status code is 200 (OK) after update
        self.assertEqual(response.status_code, 200, f"Expected status code 200 but got {response.status_code}")
        
        # Assert the success message after update
        response_data = response.json()
        self.assertIn("Ticket updated successfully", response_data["message"], f"Expected 'Ticket updated successfully' message, but got: {response_data}")
        
        # Now sending a GET request to fetch the updated ticket with ID 1
        get_response = requests.get(f"{self.url}/2")

        # Assert status code is 200 (OK)
        self.assertEqual(get_response.status_code, 200, f"Expected status code 200 but got {get_response.status_code}")
        
        # Assert that the returned ticket matches the updated details
        ticket = get_response.json()
        self.assertEqual(ticket["name"], "John Doe", f"Expected name 'John Doe' but got {ticket['name']}")
        self.assertEqual(ticket["from"], "City A", f"Expected 'from' as 'City A' but got {ticket['from']}")
        self.assertEqual(ticket["to"], "City B", f"Expected 'to' as 'City B' but got {ticket['to']}")
        self.assertEqual(ticket["day"], "Tuesday", f"Expected day 'Tuesday' but got {ticket['day']}")

        
        


    def test_07_get_updated_ticket(self):
        """Test that a GET request after updating a ticket should return the correct ticket"""
        
        # Sending a PUT request to update ticket with ID 1
        update_data = {
            "name": "John",
            "from": "City A",
            "to": "City B",
            "day": "Tuesday"
        }
        response = requests.put(f"{self.url}/3", json=update_data)
        
        # Assert status code is 200 (OK) after update
        self.assertEqual(response.status_code, 200, f"Expected status code 200 but got {response.status_code}")
        
        # Assert the success message after update
        response_data = response.json()
        self.assertIn("Ticket updated successfully", response_data["message"], f"Expected 'Ticket updated successfully' message, but got: {response_data}")
        
        # Now sending a GET request to fetch the updated ticket with ID 1
        get_response = requests.get(f"{self.url}/3")

        # Assert status code is 200 (OK)
        self.assertEqual(get_response.status_code, 200, f"Expected status code 200 but got {get_response.status_code}")
        
        # Assert that the returned ticket matches the updated details
        ticket = get_response.json()
        self.assertEqual(ticket["name"], "John", f"Expected name 'John' but got {ticket['name']}")
        self.assertEqual(ticket["from"], "City A", f"Expected 'from' as 'City A' but got {ticket['from']}")
        self.assertEqual(ticket["to"], "City B", f"Expected 'to' as 'City B' but got {ticket['to']}")
        self.assertEqual(ticket["day"], "Tuesday", f"Expected day 'Tuesday' but got {ticket['day']}")

    def test_08_get_ticket_not_found(self):
        """Test that a GET request for a non-existent ticket returns 404 and 'Ticket not found' error"""
        
        # Make a GET request to retrieve ticket with ID 2 (when no records exist in the database)
        response = requests.get(f"{self.url}/4")
        
        # Assert that the status code is 404 (Not Found), since no tickets exist in the database
        self.assertEqual(response.status_code, 404, f"Expected status code 404 but got {response.status_code}")
        
        # Assert that the response contains the correct error message
        response_data = response.json()
        self.assertIn("Ticket not found", response_data["error"], f"Expected 'Ticket not found' message, but got: {response_data['error']}")







        

if __name__ == '__main__':
    unittest.main()
