from datetime import datetime, timezone
import math
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from database import db

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance in kilometers between two points
    on the earth (specified in decimal degrees)
    """
    if None in (lat1, lon1, lat2, lon2):
        return None
    try:
        # Convert decimal degrees to radians
        lat1, lon1, lat2, lon2 = map(math.radians, [float(lat1), float(lon1), float(lat2), float(lon2)])
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.asin(math.sqrt(a))
        r = 6371.0  # Radius of earth in kilometers
        return round(c * r, 2)
    except Exception:
        return None


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')  # 'user' or 'admin'
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    favourites = db.relationship('Favourite', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    enquiries = db.relationship('Enquiry', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    owned_pgs = db.relationship('PGListing', backref='owner', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self):
        return self.role == 'admin'

    def has_favourited(self, pg_id):
        return self.favourites.filter_by(pg_id=pg_id).first() is not None

    def __repr__(self):
        return f'<User {self.email} ({self.role})>'


class PGListing(db.Model):
    __tablename__ = 'pg_listings'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    area = db.Column(db.String(100), nullable=False, index=True)
    city = db.Column(db.String(60), nullable=False, default='Bangalore')
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    
    monthly_rent = db.Column(db.Integer, nullable=False, index=True)
    security_deposit = db.Column(db.Integer, nullable=False, default=0)
    gender_category = db.Column(db.String(30), nullable=False, index=True)  # 'Boys', 'Girls', 'Co-living'
    room_type = db.Column(db.String(40), nullable=False, index=True)        # 'Single Sharing', 'Double Sharing', 'Triple Sharing', 'Four Sharing'
    
    # Amenities & Facilities
    food_available = db.Column(db.Boolean, default=True)
    wifi_available = db.Column(db.Boolean, default=True)
    ac_available = db.Column(db.Boolean, default=False)
    laundry_available = db.Column(db.Boolean, default=True)
    parking_available = db.Column(db.Boolean, default=True)
    cctv_available = db.Column(db.Boolean, default=True)
    housekeeping_available = db.Column(db.Boolean, default=True)
    attached_washroom = db.Column(db.Boolean, default=True)
    
    availability = db.Column(db.String(50), default='Immediate')  # 'Immediate', 'Within 7 Days', 'Within 15 Days', 'Full'
    rules = db.Column(db.Text, nullable=True)
    verified = db.Column(db.Boolean, default=False, index=True)
    is_sample = db.Column(db.Boolean, default=False)  # Clearly labels demo/sample records
    
    # Owner details
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    owner_name = db.Column(db.String(120), nullable=False)
    owner_phone = db.Column(db.String(20), nullable=False)
    owner_email = db.Column(db.String(120), nullable=True)
    
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    photos = db.relationship('PGPhoto', backref='pg', lazy='select', cascade='all, delete-orphan')
    favourites = db.relationship('Favourite', backref='pg', lazy='dynamic', cascade='all, delete-orphan')
    enquiries = db.relationship('Enquiry', backref='pg', lazy='dynamic', cascade='all, delete-orphan')

    @property
    def primary_photo(self):
        """Returns primary photo or first available photo, else default placeholder"""
        if self.photos:
            for p in self.photos:
                if p.is_primary:
                    return p.image_path
            return self.photos[0].image_path
        return 'images/pg/placeholder.svg'

    @property
    def photo_list(self):
        if self.photos:
            return [p.image_path for p in self.photos]
        return ['images/pg/placeholder.svg']

    @property
    def whatsapp_url(self):
        """Constructs clean WhatsApp click-to-chat URL if owner_phone is valid"""
        if not self.owner_phone:
            return None
        # Clean phone number to digits only
        digits = ''.join(c for c in self.owner_phone if c.isdigit())
        if len(digits) == 10:
            digits = '91' + digits
        msg = f"Hello, I found your listing '{self.name}' on NIVORA and would like more details."
        import urllib.parse
        encoded_msg = urllib.parse.quote(msg)
        return f"https://wa.me/{digits}?text={encoded_msg}"

    def distance_from(self, user_lat, user_lon):
        return haversine_distance(user_lat, user_lon, self.latitude, self.longitude)

    def to_dict(self, user_lat=None, user_lon=None):
        """Dictionary representation suitable for JSON APIs / Leaflet Map markers"""
        dist = self.distance_from(user_lat, user_lon) if user_lat and user_lon else None
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'address': self.address,
            'area': self.area,
            'city': self.city,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'monthly_rent': self.monthly_rent,
            'security_deposit': self.security_deposit,
            'gender_category': self.gender_category,
            'room_type': self.room_type,
            'food_available': self.food_available,
            'wifi_available': self.wifi_available,
            'ac_available': self.ac_available,
            'laundry_available': self.laundry_available,
            'parking_available': self.parking_available,
            'cctv_available': self.cctv_available,
            'housekeeping_available': self.housekeeping_available,
            'attached_washroom': self.attached_washroom,
            'availability': self.availability,
            'verified': self.verified,
            'is_sample': self.is_sample,
            'primary_photo': self.primary_photo,
            'photos': self.photo_list,
            'distance_km': dist,
            'owner_name': self.owner_name,
            'owner_phone': self.owner_phone,
            'whatsapp_url': self.whatsapp_url
        }

    def __repr__(self):
        return f'<PGListing {self.name} in {self.area}>'


class PGPhoto(db.Model):
    __tablename__ = 'pg_photos'

    id = db.Column(db.Integer, primary_key=True)
    pg_id = db.Column(db.Integer, db.ForeignKey('pg_listings.id', ondelete='CASCADE'), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    is_primary = db.Column(db.Boolean, default=False)
    caption = db.Column(db.String(150), nullable=True)

    def __repr__(self):
        return f'<PGPhoto {self.image_path} for PG {self.pg_id}>'


class Favourite(db.Model):
    __tablename__ = 'favourites'
    __table_args__ = (db.UniqueConstraint('user_id', 'pg_id', name='uq_user_pg_favourite'),)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    pg_id = db.Column(db.Integer, db.ForeignKey('pg_listings.id', ondelete='CASCADE'), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<Favourite User:{self.user_id} PG:{self.pg_id}>'


class Enquiry(db.Model):
    __tablename__ = 'enquiries'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True, index=True)
    pg_id = db.Column(db.Integer, db.ForeignKey('pg_listings.id', ondelete='CASCADE'), nullable=False, index=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(30), default='Pending')  # 'Pending', 'In Review', 'Contacted', 'Resolved'
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<Enquiry #{self.id} for PG:{self.pg_id} by {self.name} [{self.status}]>'
