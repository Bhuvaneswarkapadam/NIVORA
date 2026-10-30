from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, MultipleFileField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField, FloatField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, NumberRange, Regexp

BANGALORE_AREAS = [
    ('BTM Layout', 'BTM Layout'),
    ('HSR Layout', 'HSR Layout'),
    ('Marathahalli', 'Marathahalli'),
    ('Koramangala', 'Koramangala'),
    ('Indiranagar', 'Indiranagar'),
    ('Whitefield', 'Whitefield'),
    ('Electronic City', 'Electronic City'),
    ('Bellandur', 'Bellandur'),
    ('Jayanagar', 'Jayanagar'),
    ('Sarjapur Road', 'Sarjapur Road'),
    ('Bommanahalli', 'Bommanahalli'),
    ('Hebbal', 'Hebbal'),
    ('Rajajinagar', 'Rajajinagar'),
    ('Yelahanka', 'Yelahanka'),
    ('Mahadevapura', 'Mahadevapura'),
]

GENDER_CHOICES = [
    ('Co-living', 'Co-living (Unisex)'),
    ('Boys', 'Boys Only'),
    ('Girls', 'Girls Only'),
]

ROOM_TYPE_CHOICES = [
    ('Single Sharing', 'Single Sharing (Private Room)'),
    ('Double Sharing', 'Double Sharing (2 Beds)'),
    ('Triple Sharing', 'Triple Sharing (3 Beds)'),
    ('Four Sharing', 'Four Sharing (4 Beds)'),
]

AVAILABILITY_CHOICES = [
    ('Immediate', 'Available Immediately'),
    ('Within 7 Days', 'Available Within 7 Days'),
    ('Within 15 Days', 'Available Within 15 Days'),
    ('Full', 'Currently Occupied / Full'),
]


class RegistrationForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email Address', validators=[DataRequired(), Email(), Length(max=120)])
    phone = StringField('Phone Number', validators=[
        DataRequired(),
        Length(min=10, max=15),
        Regexp(r'^[0-9+\-\s]{10,15}$', message="Please enter a valid phone number (10-15 digits).")
    ])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, message="Password must be at least 6 characters.")])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message="Passwords must match.")
    ])
    submit = SubmitField('Create Account')


class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Keep me signed in')
    submit = SubmitField('Sign In')


class ProfileUpdateForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    phone = StringField('Phone Number', validators=[
        DataRequired(),
        Length(min=10, max=15),
        Regexp(r'^[0-9+\-\s]{10,15}$', message="Please enter a valid phone number.")
    ])
    submit = SubmitField('Update Profile')


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    confirm_new_password = PasswordField('Confirm New Password', validators=[
        DataRequired(),
        EqualTo('new_password', message="New passwords must match.")
    ])
    submit = SubmitField('Change Password')


class PGListingForm(FlaskForm):
    name = StringField('PG Name', validators=[DataRequired(), Length(min=3, max=150)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=10)])
    address = StringField('Full Address', validators=[DataRequired(), Length(min=5, max=255)])
    area = SelectField('Bangalore Area', choices=BANGALORE_AREAS, validators=[DataRequired()])
    city = StringField('City', default='Bangalore', validators=[DataRequired()])
    latitude = FloatField('Latitude', validators=[DataRequired(), NumberRange(min=12.0, max=14.0)])
    longitude = FloatField('Longitude', validators=[DataRequired(), NumberRange(min=77.0, max=78.5)])
    
    monthly_rent = IntegerField('Monthly Rent (₹)', validators=[DataRequired(), NumberRange(min=1000, max=200000)])
    security_deposit = IntegerField('Security Deposit (₹)', validators=[DataRequired(), NumberRange(min=0, max=500000)])
    
    gender_category = SelectField('Gender Category', choices=GENDER_CHOICES, validators=[DataRequired()])
    room_type = SelectField('Room Type', choices=ROOM_TYPE_CHOICES, validators=[DataRequired()])
    availability = SelectField('Availability Status', choices=AVAILABILITY_CHOICES, default='Immediate')
    
    # Facilities
    food_available = BooleanField('Food Included (Breakfast / Dinner)')
    wifi_available = BooleanField('High-speed Wi-Fi', default=True)
    ac_available = BooleanField('Air Conditioning (AC)')
    laundry_available = BooleanField('Washing Machine / Laundry', default=True)
    parking_available = BooleanField('Two-Wheeler / Car Parking', default=True)
    cctv_available = BooleanField('24/7 CCTV & Biometric Security', default=True)
    housekeeping_available = BooleanField('Daily / Regular Housekeeping', default=True)
    attached_washroom = BooleanField('Attached Bathroom', default=True)
    
    rules = TextAreaField('House Rules & Policy', validators=[Optional()])
    verified = BooleanField('Mark as Verified Listing')
    
    # Owner details
    owner_name = StringField('Owner / Caretaker Name', validators=[DataRequired(), Length(max=120)])
    owner_phone = StringField('Owner Phone / WhatsApp', validators=[
        DataRequired(),
        Length(min=10, max=15),
        Regexp(r'^[0-9+\-\s]{10,15}$', message="Enter valid phone number.")
    ])
    owner_email = StringField('Owner Email', validators=[Optional(), Email()])
    
    # Photos upload
    photos = MultipleFileField('Upload PG Photos (JPG, PNG, WEBP)', validators=[
        Optional(),
        FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'Images only!')
    ])
    submit = SubmitField('Save PG Listing')


class EnquiryForm(FlaskForm):
    name = StringField('Your Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Your Email', validators=[DataRequired(), Email()])
    phone = StringField('Your Phone Number', validators=[
        DataRequired(),
        Length(min=10, max=15),
        Regexp(r'^[0-9+\-\s]{10,15}$', message="Enter valid phone number.")
    ])
    message = TextAreaField('Message / Preferred Move-in Date', validators=[DataRequired(), Length(min=5, max=1000)])
    submit = SubmitField('Send Enquiry to Owner')


class ContactForm(FlaskForm):
    name = StringField('Your Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[Optional(), Length(min=10, max=15)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10, max=2000)])
    submit = SubmitField('Send Message')

