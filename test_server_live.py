"""
Verification script: tests all endpoints with test client and live responses
"""
from app import create_app
from database import db
from models import User, PGListing

app = create_app()

def run_checks():
    client = app.test_client()
    print("Testing Homepage ('/')...")
    res = client.get('/')
    assert res.status_code == 200
    assert b'Find Your Perfect' in res.data
    assert b'Featured Stays in Bangalore' in res.data
    print("[OK] Homepage")

    print("Testing Search Page ('/search')...")
    res = client.get('/search')
    assert res.status_code == 200
    assert b'Explore Accommodations in' in res.data
    assert b'id="search-map"' in res.data
    print("[OK] Search Page")

    print("Testing Search with Filters ('/search?area=Koramangala&max_rent=25000')...")
    res = client.get('/search?area=Koramangala&max_rent=25000')
    assert res.status_code == 200
    assert b'Aurum Luxe Coliving' in res.data
    print("[OK] Filtered Search")

    print("Testing PG Details Page ('/pg/1')...")
    res = client.get('/pg/1')
    assert res.status_code == 200
    assert b'Aurum Luxe Coliving' in res.data
    assert b'Facilities & Amenities' in res.data
    assert b'id="detail-map"' in res.data
    print("[OK] PG Details Page")

    print("Testing Locations Directory ('/locations')...")
    res = client.get('/locations')
    assert res.status_code == 200
    assert b'Koramangala' in res.data
    assert b'Whitefield' in res.data
    print("[OK] Locations Page")

    print("Testing About Page ('/about')...")
    res = client.get('/about')
    assert res.status_code == 200
    assert b'Our Mission' in res.data or b'OUR MISSION' in res.data
    print("[OK] About Page")

    print("Testing Contact Page ('/contact')...")
    res = client.get('/contact')
    assert res.status_code == 200
    assert b'Get in Touch' in res.data
    print("[OK] Contact Page")

    print("Testing Login Page ('/login')...")
    res = client.get('/login')
    assert res.status_code == 200
    assert b'admin@nivora.com' in res.data
    print("[OK] Login Page")

    print("Testing Register Page ('/register')...")
    res = client.get('/register')
    assert res.status_code == 200
    assert b'Join NIVORA' in res.data
    print("[OK] Register Page")

    print("Testing Admin Dashboard for Admin User...")
    import re
    res_get_login = client.get('/login')
    match = re.search(r'name="csrf_token" type="hidden" value="([^"]+)"', res_get_login.get_data(as_text=True))
    if not match:
        match = re.search(r'value="([^"]+)" id="csrf_token"', res_get_login.get_data(as_text=True))
    if not match:
        match = re.search(r'id="csrf_token" name="csrf_token" type="hidden" value="([^"]+)"', res_get_login.get_data(as_text=True))
    print("Match regex result:", match)
    csrf_token = match.group(1) if match else ''
    print(f"Extracted CSRF token: {csrf_token[:15]}...")
    
    res_post_login = client.post('/login', data={
        'csrf_token': csrf_token,
        'email': 'admin@nivora.com',
        'password': 'Admin@123'
    }, follow_redirects=True)
    print(f"Login POST status: {res_post_login.status_code}, redirect location: {res_post_login.headers.get('Location')}")
    assert res_post_login.status_code in (200, 302)
    
    res_admin = client.get('/admin/dashboard')
    assert res_admin.status_code == 200
    assert b'NIVORA Control Center' in res_admin.data
    assert b'Total PG Listings' in res_admin.data
    print("[OK] Admin Dashboard")

    print("Testing Admin Add PG Form ('/admin/pg/add')...")
    res_add = client.get('/admin/pg/add')
    assert res_add.status_code == 200
    assert b'Add PG Accommodation' in res_add.data
    print("[OK] Admin Add PG Form")

    print("Testing Admin Manage PGs ('/admin/pgs')...")
    res_manage = client.get('/admin/pgs')
    assert res_manage.status_code == 200
    assert b'Manage PG Accommodations' in res_manage.data
    print("[OK] Admin Manage PGs")

    print("Testing Admin Enquiries ('/admin/enquiries')...")
    res_enq = client.get('/admin/enquiries')
    assert res_enq.status_code == 200
    assert b'Tenant Enquiry Requests' in res_enq.data
    print("[OK] Admin Enquiries")

    print("\nALL 13 SYSTEM VALIDATION CHECKS PASSED PERFECTLY!")

if __name__ == '__main__':
    run_checks()
