import pytest
from app import create_app
from database import db
from models import User, PGListing, Enquiry
from config import TestingConfig

@pytest.fixture
def app():
    app = create_app(TestingConfig)
    with app.app_context():
        db.create_all()
        # Admin user
        admin = User(name='Admin', email='admin@test.com', phone='9800000001', role='admin')
        admin.set_password('AdminPass123')

        # Regular user
        user = User(name='Regular', email='regular@test.com', phone='9800000002', role='user')
        user.set_password('UserPass123')

        db.session.add_all([admin, user])
        db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_unauthorized_user_blocked_from_admin(client):
    """Test regular users and guests are blocked from admin routes"""
    # Guest access
    res = client.get('/admin/dashboard', follow_redirects=True)
    assert b'sign in with administrator credentials' in res.data or b'Sign In' in res.data

    # Regular user login
    client.post('/login', data={'email': 'regular@test.com', 'password': 'UserPass123'})
    res_user = client.get('/admin/dashboard', follow_redirects=True)
    assert b'Administrator privileges required' in res_user.data

def test_admin_can_add_and_delete_pg(client, app):
    """Test administrator can add a new PG accommodation and delete it"""
    # Login as admin
    client.post('/login', data={'email': 'admin@test.com', 'password': 'AdminPass123'})
    
    # Add PG
    res_add = client.post('/admin/pg/add', data={
        'name': 'Admin Created PG',
        'description': 'A beautiful test accommodation in Indiranagar',
        'address': '12th Main Road, Indiranagar',
        'area': 'Indiranagar',
        'city': 'Bangalore',
        'latitude': '12.9784',
        'longitude': '77.6408',
        'monthly_rent': '15000',
        'security_deposit': '20000',
        'gender_category': 'Girls',
        'room_type': 'Double Sharing',
        'availability': 'Immediate',
        'wifi_available': 'y',
        'food_available': 'y',
        'owner_name': 'Owner Admin',
        'owner_phone': '9876543210'
    }, follow_redirects=True)
    
    assert res_add.status_code == 200
    with app.app_context():
        pg = PGListing.query.filter_by(name='Admin Created PG').first()
        assert pg is not None
        assert pg.area == 'Indiranagar'
        assert pg.monthly_rent == 15000
        pg_id = pg.id

    # Delete PG
    res_del = client.post(f'/admin/pg/{pg_id}/delete', follow_redirects=True)
    assert res_del.status_code == 200
    with app.app_context():
        pg_after = db.session.get(PGListing, pg_id)
        assert pg_after is None
