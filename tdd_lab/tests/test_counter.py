import pytest
from src import app
from src import status
    
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