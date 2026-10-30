import pytest
from app import create_app
from database import db
from models import PGListing, haversine_distance
from config import TestingConfig

@pytest.fixture
def app():
    app = create_app(TestingConfig)
    with app.app_context():
        db.create_all()
        # Seed test PGs
        pg1 = PGListing(
            name='Koramangala Luxe Stay',
            description='Prime luxury PG in Koramangala 4th block',
            address='80 Feet Road, Koramangala',
            area='Koramangala',
            city='Bangalore',
            latitude=12.9348,
            longitude=77.6259,
            monthly_rent=18000,
            security_deposit=20000,
            gender_category='Co-living',
            room_type='Single Sharing',
            food_available=True,
            wifi_available=True,
            ac_available=True,
            owner_name='Host One',
            owner_phone='9845012345',
            verified=True
        )
        pg2 = PGListing(
            name='BTM Budget Nest',
            description='Affordable student PG in BTM',
            address='7th Cross, BTM 2nd Stage',
            area='BTM Layout',
            city='Bangalore',
            latitude=12.9152,
            longitude=77.6125,
            monthly_rent=8500,
            security_deposit=10000,
            gender_category='Boys',
            room_type='Triple Sharing',
            food_available=True,
            wifi_available=True,
            ac_available=False,
            owner_name='Host Two',
            owner_phone='9845012346',
            verified=False
        )
        db.session.add_all([pg1, pg2])
        db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_haversine_distance_calculation():
    """Test distance formula calculation between two known Bangalore coordinates"""
    # Koramangala to BTM Layout (approx 2.6 km)
    dist = haversine_distance(12.9348, 77.6259, 12.9152, 77.6125)
    assert dist is not None
    assert 2.0 <= dist <= 3.5

def test_search_by_area(client):
    """Test searching by Bangalore area filter"""
    res = client.get('/search?area=Koramangala')
    assert res.status_code == 200
    assert b'Koramangala Luxe Stay' in res.data
    assert b'BTM Budget Nest' not in res.data

def test_search_by_budget(client):
    """Test filtering by maximum rent"""
    res = client.get('/search?max_rent=10000')
    assert res.status_code == 200
    assert b'BTM Budget Nest' in res.data
    assert b'Koramangala Luxe Stay' not in res.data

def test_search_by_gender(client):
    """Test filtering by gender category"""
    res = client.get('/search?gender=Boys')
    assert res.status_code == 200
    assert b'BTM Budget Nest' in res.data
    assert b'Koramangala Luxe Stay' not in res.data

def test_api_pgs_json(client):
    """Test /api/pgs JSON endpoint for Leaflet map integration"""
    res = client.get('/api/pgs?area=Koramangala')
    assert res.status_code == 200
    data = res.get_json()
    assert len(data) == 1
    assert data[0]['name'] == 'Koramangala Luxe Stay'
    assert data[0]['monthly_rent'] == 18000

