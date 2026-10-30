import pytest
from app import create_app
from database import db
from models import User
from config import TestingConfig

@pytest.fixture
def app():
    app = create_app(TestingConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_user_registration_and_hashing(client, app):
    """Test user registration hashes password and creates user in database"""
    response = client.post('/register', data={
        'name': 'Test User',
        'email': 'newuser@example.com',
        'phone': '9876543210',
        'password': 'Password123',
        'confirm_password': 'Password123'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    with app.app_context():
        user = User.query.filter_by(email='newuser@example.com').first()
        assert user is not None
        assert user.name == 'Test User'
        assert user.password_hash != 'Password123'
        assert user.check_password('Password123') is True
        assert user.check_password('WrongPass') is False

def test_duplicate_registration_prevention(client, app):
    """Test registering with an already existing email is rejected"""
    with app.app_context():
        u = User(name='Existing', email='existing@example.com', phone='9876543210')
        u.set_password('Secret123')
        db.session.add(u)
        db.session.commit()

    response = client.post('/register', data={
        'name': 'Existing Duplicate',
        'email': 'existing@example.com',
        'phone': '9876543210',
        'password': 'Password123',
        'confirm_password': 'Password123'
    }, follow_redirects=True)

    assert b'already exists' in response.data

def test_user_login_logout(client, app):
    """Test logging in with valid and invalid credentials"""
    with app.app_context():
        u = User(name='Login User', email='login@example.com', phone='9876543210')
        u.set_password('ValidPassword')
        db.session.add(u)
        db.session.commit()

    # Invalid login
    res_fail = client.post('/login', data={
        'email': 'login@example.com',
        'password': 'InvalidPassword'
    }, follow_redirects=True)
    assert b'Invalid email or password' in res_fail.data

    # Valid login
    res_success = client.post('/login', data={
        'email': 'login@example.com',
        'password': 'ValidPassword'
    }, follow_redirects=True)
    assert b'Welcome back' in res_success.data

    # Logout
    res_logout = client.get('/logout', follow_redirects=True)
    assert b'signed out safely' in res_logout.data

