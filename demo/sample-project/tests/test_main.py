"""
Tests for the main application.
"""

import pytest
import json
from main import app


@pytest.fixture
def client():
    """Test client fixture."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home_endpoint(client):
    """Test home endpoint."""
    response = client.get('/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'


def test_create_user_valid(client):
    """Test creating user with valid data."""
    user_data = {
        'name': 'John Doe',
        'email': 'john@example.com',
        'age': 30
    }
    response = client.post('/users', 
                          data=json.dumps(user_data),
                          content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'created'


def test_create_user_invalid(client):
    """Test creating user with invalid data."""
    user_data = {
        'name': 'John Doe'
        # Missing required email field
    }
    response = client.post('/users', 
                          data=json.dumps(user_data),
                          content_type='application/json')
    assert response.status_code == 400