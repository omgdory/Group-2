"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""

import pytest
from src import app
from src import status
from flask import json #for test case 3


@pytest.fixture(autouse=True) # ensures that test 10 starts with a clean slate every time
def reset_counters():
    """Reset counters before each test"""
    from src.counter import COUNTERS
    COUNTERS.clear()
    yield
    COUNTERS.clear()

@pytest.fixture()
def client():
    """Fixture for Flask test client"""
    return app.test_client()

@pytest.mark.usefixtures("client")
class TestCounterEndpoints:
    """Test cases for Counter API"""

    def test_create_counter(self, client):
        """It should create a counter"""
        result = client.post('/counters/foo')
        assert result.status_code == status.HTTP_201_CREATED

    
    # ===========================
    # Feature: Create a new counter (POST /counters/<name>)
    # Author: Dorian Akhavan
    # Date: 2025-02-04
    # Description: Create a counter and check that the status indicates creation
    # ===========================
    def test_create_new_counter(self, client):
        """It should create a counter (NOT the same as the example above)"""
        result = client.post('/new_counters/bar')
        assert result.status_code == status.HTTP_201_CREATED


    # ===========================  
    # Test: Delete Counter (DELETE /counters/<name>)  
    # Author: Franklin La Rosa Diaz  
    # Date: 2025-02-02  
    # Description: Ensure that when `delete()` removes an existing counter,  
    # it produces the correct HTTP response. Otherwise, it raises an error.  
    # It also raises an error when there is an attempt to delete a non-existent counter.  
    # =========================== 
    def test_delete_counter(self, client):
        """It should delete a counter"""
        # Create a counter
        client.post('/counters/foo')
        # Delete it
        result = client.delete('/counters/foo')
        # Check deletion 
        assert result.status_code == status.HTTP_204_NO_CONTENT
        # Delete again to check it passes
        result = client.delete('/counters/foo')
        # Check deletion  when counter doesn't exist
        assert result.status_code == status.HTTP_404_NOT_FOUND

    """
    Name: Jose Alarcon, NSHE: 5005581810, CS472 GitHub Lab
    Description: This file gathers git commits on a specific project.
    It then prints this information for easy parsing to .txt file
    """
    def test_prevent_duplicate_counters(self, client):
        # return "409 Conflict" if a duplicate counter is created
        client.post('/counters/foo')  # counter
        result = client.post('/counters/foo')

        assert result.status_code == status.HTTP_409_CONFLICT
        assert result.json == {"error": "Counter foo already exists"}

    # ===========================
    # Test: Test Increment Counter (PUT/counter/<name>)
    # Author: Ashley Arellano
    # Date: 2025-02-03
    # Description: Ensure that when `put()` increments a given, existing 
    # counter, it produces the correct HTTP response. Otherwise, raises an
    # error. It also raises an error when there is an attempt to 
    # increment a non-existent counter.
    # ===========================
    def test_increment_counter(self,client):
        #Test case 5 when there EXISTS a counter able to be incremented
        name = '/counters/test_case_5_allowed'
        #Create counter 
        client.post(name)
        #Testing increment counter in ALLOWED case
        result = client.put(name)
        assert result.status_code == status.HTTP_200_OK

    # ===========================
    # Test: Prevent updating non-existent counter (PUT/counter/<name>)
    # Author: Charles Joseph Ballesteros
    # Date: 2025-02-03
    # Description: Asserts that the counter does not increment if the counter
    # doesn't exist.
    # ===========================
    def test_nonexistent_counter(self, client):
        name = 'counters/test_case_6_non_existent'
        result = client.put(name)
        assert result.status_code == status.HTTP_404_NOT_FOUND


    # TODO 3: i will do this later 
    # - i will do this later 
    # ===========================
    # Test: Retrieve an existing counter
    # Author: [Abdulrahman Alharbi]
    # Date: [02.03.2025]
    # Description: i will do this later 
    # ===========================
    def test_get_existing_counter(self, client):
        """It should retrieve an existing counter"""
        
        # Correct endpoint for creating a counter
        name = "/counters/test_counter"
        client.post(name)
        # Now send a GET request to retrieve it
        response = client.get(name)
        # Ensure the request was successful
        assert response.status_code == 200
        
        # Convert response to JSON only if the request was successful
        if response.is_json:
            data = response.get_json()
        else:
            pytest.fail(f"Expected JSON response but got: {response.data}")
        # Assertions
        assert "test_counter" in data

    # ===========================
    # Test: Return 404 for non-existent counter (GET /counters)
    # Author: Aviendha Andrus
    # Date: 2025-02-06
    # Description: Returns a 404 error when attempting to retrieve a 
    # counter that does not exist.
    # ===========================
    def test_get_nonexistent_counter(self, client):
        """It should return 404 when retrieving a non-existent counter"""
        name = '/counters/non_existent'
        result = client.get(name)
        assert result.status_code == status.HTTP_404_NOT_FOUND
        assert result.json == {"error": "Counter not found"}
    
    # ===========================
    # Feature: Reset all counters	POST /counters/reset
    # Author: Allison Kameda
    # Date: 2025-02-07
    # Description: Reset all the counters to 0
    # ===========================
    def test_reset_counters(self, client):
        """It should reset all counters to 0"""
        # Create counters
        client.post('/counters/foo')
        client.post('/counters/bar')
        
        # Verify counters are created
        result = client.get('/counters')
        assert result.status_code == status.HTTP_200_OK
        data = result.get_json()
        assert len(data) == 2
        assert 'foo' in data
        assert 'bar' in data
        assert data['foo'] == 0
        assert data['bar'] == 0
        
        # Reset all counters
        result = client.post('/counters/reset')
        assert result.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify all counters have been reset
        result = client.get('/counters')
        assert result.status_code == status.HTTP_200_OK
        data = result.get_json()
        assert len(data) == 0  # No counters should be left

    # ===========================
    # Test: Lists all the counters
    # Author: Christopher Liscano
    # Date: 2025-02-04
    # Description: Should output all the counters
    # ===========================
    def test_list_counters(self, client):
        """It should list all counters"""
        # create some test counters
        client.post('/counters/foo')
        client.post('/counters/bar')
        # get list of counters
        result = client.get('/counters')
        # check response
        assert result.status_code == status.HTTP_200_OK
        data = result.get_json()
        assert isinstance(data, dict)
        assert len(data) == 2
        assert 'foo' in data
        assert 'bar' in data
        assert data['foo'] == 0
        assert data['bar'] == 0

    
    # ===========================
    # Test: Prevent deleting non-existent counter 	DELETE /counters/<name>
    # Author: Sameer Issa
    # Date: 2025-02-05
    # Description: Assert that counter can't be deleted if counter doesn't exist
    # ===========================
    def test_deleting_nonexistant_counter(self, client):
        name = '/counters/test_case_8'
        response = client.delete(name)
        # assert the counter does not exist
        assert response.status_code == status.HTTP_404_NOT_FOUND

  # ===========================
    # Test: Handle invalid HTTP methods     (Unsupported HTTP Methods)
    # Author: Ethan Zambrano
    # Date: 2025-02-07
    # Description: Confirm that invalid HTTP methods like 'PATCH', 'TRACE', 'CONNECT' return
    #              a 405 Method Not Allowed when used on the endpoints (/counters).
    #              ALSO, some servers may return 404 (route is not defined) or 500 (internal error).
    # ===========================
    def test_invalid_http_methods(self, client):
        """It should return 405 Method Not Allowed (or 404/500 whenever applicable) for invalid HTTP methods"""
        name = '/counters'
        
        # List of invalid methods to test
        invalid_methods = ['PATCH', 'TRACE', 'CONNECT']

        for method in invalid_methods:
            result = client.open(name, method=method)

            # Ensure 200 is not returned for an invalid HTTP method
            assert result.status_code != 200, f"Unexpected 200 OK for {method}"

            # Allow only expected failure status codes: 404, 405, or 500.
            assert result.status_code in {404, 405, 500}, f"Unexpected status code {result.status_code} for {method}"
