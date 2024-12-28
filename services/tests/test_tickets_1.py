import requests

url = "http://127.0.0.1:5000/tickets"

def test_get_tickets():
    """Test the GET /tickets endpoint returns 1 record"""
    response = requests.get(url)
    
    # Assert status code is 200 (OK)
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
    
    # Convert the response JSON to a list and check the length
    tickets = response.json()
    assert len(tickets) == 19, f"Expected 4 tickets but got {len(tickets)}"


def test_get_ticket_not_found():
    """Test that a GET request for a non-existent ticket returns 404"""
    response = requests.get(f"{url}/999")  # Assuming ID 999 doesn't exist
    assert response.status_code == 404, f"Expected status code 404 but got {response.status_code}"
    assert "Ticket not found" in response.json().get("error"), "Expected 'Ticket not found' error"


def test_create_ticket():
    """Test the POST /tickets endpoint to create a new ticket"""
    data = {
        "name": "John Doe",
        "from": "City A",
        "to": "City B",
        "day": "Monday"
    }
    
    response = requests.post(url, json=data)
    
    # Assert status code is 201 (Created)
    assert response.status_code == 201, f"Expected status code 201 but got {response.status_code}"
    
    # Assert the response message indicates successful creation
    assert response.json().get("message") == "Ticket created successfully", "Ticket creation failed"
    
    # Optionally, verify the ticket is created
    response_get = requests.get(url)
    tickets = response_get.json()
    assert len(tickets) > 0, "Expected at least one ticket to be created"


def test_get_ticket_details():
    """Test that a GET request for a specific ticket returns the correct data"""
    response = requests.get(f"{url}/2")
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
    
    ticket = response.json()
    assert ticket["name"] == "John Doe", f"Expected 'name' to be 'John Doe' but got {ticket['name']}"
    assert ticket["from"] == "City A", f"Expected 'from' to be 'City A' but got {ticket['from']}"
    assert ticket["to"] == "City B", f"Expected 'to' to be 'City B' but got {ticket['to']}"
    assert ticket["day"] == "Monday", f"Expected 'day' to be 'Monday' but got {ticket['day']}"


def test_update_existing_ticket():
    """Test that a PUT request successfully updates an existing ticket"""
    data = {
        "name": "John",
        "from": "City A",
        "to": "City B",
        "day": "Tuesday"
    }

    response = requests.put(f"{url}/1", json=data)
    
    # Assert status code is 200 (OK)
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
    
    # Assert the success message
    response_data = response.json()
    assert "Ticket updated successfully" in response_data["message"], f"Expected 'Ticket updated successfully' but got: {response_data}"


def test_get_updated_ticket():
    """Test that a GET request after updating a ticket returns the correct updated ticket"""
    update_data = {
        "name": "John",
        "from": "City A",
        "to": "City B",
        "day": "Tuesday"
    }
    # Update ticket
    response = requests.put(f"{url}/2", json=update_data)
    
    # Assert status code is 200 (OK) after update
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
    
    # Now, get the updated ticket details
    get_response = requests.get(f"{url}/2")
    assert get_response.status_code == 200, f"Expected status code 200 but got {get_response.status_code}"
    
    ticket = get_response.json()
    assert ticket["name"] == "John", f"Expected 'name' to be 'John' but got {ticket['name']}"
    assert ticket["from"] == "City A", f"Expected 'from' to be 'City A' but got {ticket['from']}"
    assert ticket["to"] == "City B", f"Expected 'to' to be 'City B' but got {ticket['to']}"
    assert ticket["day"] == "Tuesday", f"Expected 'day' to be 'Tuesday' but got {ticket['day']}"


def test_delete_ticket():
    """Test DELETE /tickets/2 endpoint to delete a ticket"""
    # Initially, check how many tickets are present
    response_get = requests.get(url)
    tickets_before = response_get.json()
    
    ticket_count_before = len(tickets_before)
    
    # Delete ticket with ID 2
    response_delete = requests.delete(f"{url}/2")
    
    assert response_delete.status_code == 200, f"Expected status code 200 but got {response_delete.status_code}"
    assert response_delete.json()["message"] == "Ticket deleted successfully", "Ticket deletion failed"
    
    # Verify that the ticket count has decreased by 1
    response_get = requests.get(url)
    tickets_after = response_get.json()
    ticket_count_after = len(tickets_after)
    
    assert ticket_count_after == ticket_count_before - 1, "Ticket was not deleted successfully"


def test_get_ticket_not_found_after_deletion():
    """Test GET /tickets/2 after deletion to ensure the ticket is not found"""
    response = requests.get(f"{url}/2")
    assert response.status_code == 404, f"Expected status code 404 but got {response.status_code}"
    assert "Ticket not found" in response.json().get("error"), "Expected 'Ticket not found' error"


