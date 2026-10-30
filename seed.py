"""
NIVORA Database Seeder
Populates initial Bangalore PG listings, admin account, and demo user.
All demo accommodations are clearly marked as sample data.
"""

from datetime import datetime, timezone
from app import create_app
from database import db
from models import User, PGListing, PGPhoto, Favourite, Enquiry

BANGALORE_LOCATIONS_META = {
    'Koramangala': {'lat': 12.9352, 'lng': 77.6245, 'desc': 'Startup hub, vibrant cafes, co-working spaces and premium nightlife.'},
    'Indiranagar': {'lat': 12.9784, 'lng': 77.6408, 'desc': 'Upscale residential neighborhood with 100ft road shopping and gourmet dining.'},
    'HSR Layout': {'lat': 12.9121, 'lng': 77.6446, 'desc': 'Well-planned tech haven between Koramangala and Bellandur tech corridor.'},
    'BTM Layout': {'lat': 12.9166, 'lng': 77.6101, 'desc': 'Student friendly, affordable stay with incredible street food and connectivity.'},
    'Whitefield': {'lat': 12.9698, 'lng': 77.7499, 'desc': 'ITPL tech cluster, metro connectivity, malls and modern luxury apartments.'},
    'Electronic City': {'lat': 12.8452, 'lng': 77.6602, 'desc': 'Major tech district hosting Infosys, Wipro, and elevated expressway.'},
    'Bellandur': {'lat': 12.9304, 'lng': 77.6784, 'desc': 'Center of Outer Ring Road tech parks (EcoWorld, EcoSpace, Prestige Tech Park).'},
    'Marathahalli': {'lat': 12.9591, 'lng': 77.6974, 'desc': 'Bridge to Whitefield with budget-friendly shopping, transport and PG hubs.'},
    'Jayanagar': {'lat': 12.9308, 'lng': 77.5838, 'desc': 'Classic South Bangalore tree-lined boulevards, quiet parks and cultural food.'},
    'Sarjapur Road': {'lat': 12.9098, 'lng': 77.6853, 'desc': 'Booming corridor for IT professionals, international schools and gated campuses.'},
    'Bommanahalli': {'lat': 12.9015, 'lng': 77.6231, 'desc': 'Affordable tech neighbor to Hosur Road and Silk Board.'},
    'Hebbal': {'lat': 13.0358, 'lng': 77.5970, 'desc': 'North Bangalore gateway with Manyata Tech Park and expressway to airport.'},
    'Rajajinagar': {'lat': 12.9982, 'lng': 77.5530, 'desc': 'West Bangalore commercial hub, World Trade Center and Orion Mall.'},
    'Yelahanka': {'lat': 13.1007, 'lng': 77.5963, 'desc': 'Serene northern suburb with universities and research institutes.'},
    'Mahadevapura': {'lat': 12.9868, 'lng': 77.6888, 'desc': 'Prime connectivity to Bagmane Tech Park and Phoenix Marketcity.'}
}

SAMPLE_PGS = [
    {
        'name': 'Aurum Luxe Coliving & Suites',
        'description': 'Experience signature luxury living in Koramangala 4th Block. Fully serviced suites designed for tech founders and young professionals. Features ergonomic workstations, high-speed fiber internet, gourmet healthy dining, and a rooftop sky lounge with sunset coffee bar. [Demo Listing]',
        'address': '#428, 80 Feet Road, 4th Block, Koramangala',
        'area': 'Koramangala',
        'city': 'Bangalore',
        'latitude': 12.9348,
        'longitude': 77.6259,
        'monthly_rent': 18500,
        'security_deposit': 25000,
        'gender_category': 'Co-living',
        'room_type': 'Single Sharing',
        'food_available': True,
        'wifi_available': True,
        'ac_available': True,
        'laundry_available': True,
        'parking_available': True,
        'cctv_available': True,
        'housekeeping_available': True,
        'attached_washroom': True,
        'availability': 'Immediate',
        'rules': 'No smoking indoors. Visitors allowed in rooftop lounge until 10 PM. Quiet hours after 11 PM.',
        'verified': True,
        'is_sample': True,
        'owner_name': 'Rohan Varma (Demo Host)',
        'owner_phone': '+91 98450 12345',
        'owner_email': 'rohan.aurum@example.com',
        'photos': [
            'images/pg/pg1_main.svg',
            'images/pg/pg1_room.svg',
            'images/pg/pg1_lounge.svg'
        ]
    },
    {
        'name': 'The Ivy Executive Stay for Women',
        'description': 'Exclusively curated for female working professionals and scholars in Indiranagar. Round-the-clock female security personnel, biometric smart entry, chef-prepared North and South Indian meals, and serene reading balconies. Minutes walk from 100ft Road and metro station. [Demo Listing]',
        'address': '#112, 12th Main Rd, HAL 2nd Stage, Indiranagar',
        'area': 'Indiranagar',
        'city': 'Bangalore',
        'latitude': 12.9712,
        'longitude': 77.6415,
        'monthly_rent': 16000,
        'security_deposit': 20000,
        'gender_category': 'Girls',
        'room_type': 'Double Sharing',
        'food_available': True,
        'wifi_available': True,
        'ac_available': True,
        'laundry_available': True,
        'parking_available': True,
        'cctv_available': True,
        'housekeeping_available': True,
        'attached_washroom': True,
        'availability': 'Immediate',
        'rules': 'Strict female-only premises. Biometric access 24/7. Main gate closes at 11:30 PM with prior notice option.',
        'verified': True,
        'is_sample': True,
        'owner_name': 'Mrs. Meenakshi Sundaram (Demo Host)',
        'owner_phone': '+91 98860 67890',
        'owner_email': 'meenakshi.ivy@example.com',
        'photos': [
            'images/pg/pg2_main.svg',
            'images/pg/pg2_room.svg'
        ]
    },
    {
        'name': 'Nexus Tech Living for Men',
        'description': 'Modern, high-energy PG located in Sector 3 HSR Layout. Ideal for developers and startup employees seeking high-speed uninterrupted 300 Mbps Wi-Fi, power backup, gaming zone, and gym access. Daily nutritious home-cooked meals included. [Demo Listing]',
        'address': '#789, 14th Main, Sector 3, HSR Layout',
        'area': 'HSR Layout',
        'city': 'Bangalore',
        'latitude': 12.9135,
        'longitude': 77.6398,
        'monthly_rent': 11500,
        'security_deposit': 15000,
        'gender_category': 'Boys',
        'room_type': 'Double Sharing',
        'food_available': True,
        'wifi_available': True,
        'ac_available': False,
        'laundry_available': True,
        'parking_available': True,
        'cctv_available': True,
        'housekeeping_available': True,
        'attached_washroom': True,
        'availability': 'Immediate',
        'rules': 'Boys only accommodation. Alcohol and illegal substances strictly prohibited. Guests welcome in common area.',
        'verified': True,
        'is_sample': True,
        'owner_name': 'Karthik Reddy (Demo Host)',
        'owner_phone': '+91 97410 45678',
        'owner_email': 'karthik.nexus@example.com',
        'photos': [
            'images/pg/pg3_main.svg',
            'images/pg/pg3_room.svg'
        ]
    },
    {
        'name': 'Zenith Heights Premium PG',
        'description': 'Elevated urban living right opposite Ecoworld Tech Park Bellandur. Cut your daily commute to zero! Spacious air-conditioned single and twin rooms with private balconies, daily housekeeping, 3-tier security, and cafeteria with unlimited buffet breakfast & dinner. [Demo Listing]',
        'address': '#56/2, Green Glen Layout, Bellandur',
        'area': 'Bellandur',
        'city': 'Bangalore',
        'latitude': 12.9288,
        'longitude': 77.6745,
        'monthly_rent': 14500,
        'security_deposit': 18000,
        'gender_category': 'Co-living',
        'room_type': 'Double Sharing',
        'food_available': True,
        'wifi_available': True,
        'ac_available': True,
        'laundry_available': True,
        'parking_available': True,
        'cctv_available': True,
        'housekeeping_available': True,
        'attached_washroom': True,
        'availability': 'Within 7 Days',
        'rules': 'Respect co-residents quiet hours. Professional demeanor expected. Pets allowed upon prior management review.',
        'verified': True,
        'is_sample': True,
        'owner_name': 'Ananya Sen (Demo Host)',
        'owner_phone': '+91 99001 23456',
        'owner_email': 'zenith.bellandur@example.com',
        'photos': [
            'images/pg/pg4_main.svg',
            'images/pg/pg4_room.svg'
        ]
    },
    {
        'name': 'BTM Comfort Residency',
        'description': 'Pocket-friendly, neat and hygienic PG accommodation located in BTM 2nd Stage, near Udupi Garden. Walking distance from coaching institutes and bus terminals. Unlimited Wi-Fi, South and North Indian meal options, and regular water supply. [Demo Listing]',
        'address': '#23, 7th Cross, 2nd Stage, BTM Layout',
        'area': 'BTM Layout',
        'city': 'Bangalore',
        'latitude': 12.9152,
        'longitude': 77.6125,
        'monthly_rent': 8500,
        'security_deposit': 10000,
        'gender_category': 'Boys',
        'room_type': 'Triple Sharing',
        'food_available': True,
        'wifi_available': True,
        'ac_available': False,
        'laundry_available': True,
        'parking_available': True,
        'cctv_available': True,
        'housekeeping_available': True,
        'attached_washroom': True,
        'availability': 'Immediate',
        'rules': 'No loud music after 10:30 PM. Gate locked at 11 PM for safety.',
        'verified': False,
        'is_sample': True,
        'owner_name': 'Suresh Gowda (Demo Host)',
        'owner_phone': '+91 98440 98765',
        'owner_email': 'suresh.btm@example.com',
        'photos': [
            'images/pg/pg5_main.svg'
        ]
    },
    {
        'name': 'Silicon Oasis Coliving Suites',
        'description': 'Luxury studio style co-living in the heart of Whitefield near ITPL. Designed for digital nomads, tech consultants and corporate leaders. Smart TV in room, ergonomic chair and study table, weekly linen change, and gym on premise. [Demo Listing]',
        'address': '#88, EPIP Zone, Near ITPL Main Gate, Whitefield',
        'area': 'Whitefield',
        'city': 'Bangalore',
        'latitude': 12.9734,
        'longitude': 77.7288,
        'monthly_rent': 21000,
        'security_deposit': 30000,
        'gender_category': 'Co-living',
        'room_type': 'Single Sharing',
        'food_available': False,
        'wifi_available': True,
        'ac_available': True,
        'laundry_available': True,
        'parking_available': True,
        'cctv_available': True,
        'housekeeping_available': True,
        'attached_washroom': True,
        'availability': 'Immediate',
        'rules': 'Fully modular independent living. Kitchenette with microwave and induction provided in room.',
        'verified': True,
        'is_sample': True,
        'owner_name': 'Pooja Hegde (Demo Host)',
        'owner_phone': '+91 96110 33445',
        'owner_email': 'pooja.silicon@example.com',
        'photos': [
            'images/pg/pg6_main.svg',
            'images/pg/pg6_room.svg'
        ]
    },
    {
        'name': 'TechVille Elite Men\'s PG',
        'description': 'Premium men\'s PG in Electronic City Phase 1, just 5 minutes from Infosys Gate 1. Includes 3 meals a day, laundry service, high-speed fiber internet, and indoor table tennis room. Ideal for tech professionals in E-City. [Demo Listing]',
        'address': '#34, Neeladri Road, Electronic City Phase 1',
        'area': 'Electronic City',
        'city': 'Bangalore',
        'latitude': 12.8488,
        'longitude': 77.6534,
        'monthly_rent': 9500,
        'security_deposit': 12000,
        'gender_category': 'Boys',
        'room_type': 'Double Sharing',
        'food_available': True,
        'wifi_available': True,
        'ac_available': False,
        'laundry_available': True,
        'parking_available': True,
        'cctv_available': True,
        'housekeeping_available': True,
        'attached_washroom': True,
        'availability': 'Immediate',
        'rules': 'Non-alcoholic premise. 24-hour warden on duty.',
        'verified': True,
        'is_sample': True,
        'owner_name': 'Mahesh Kumar (Demo Host)',
        'owner_phone': '+91 94480 77889',
        'owner_email': 'mahesh.techville@example.com',
        'photos': [
            'images/pg/pg7_main.svg'
        ]
    },
    {
        'name': 'Serene Haven Ladies Residence',
        'description': 'A peaceful, secure home for working women and students in Jayanagar 4th Block. Serene surroundings, spacious ventilated rooms, RO purified water, organic home-style meals, and CCTV surveillance throughout the common areas. [Demo Listing]',
        'address': '#14, 11th Main, 4th Block, Jayanagar',
        'area': 'Jayanagar',
        'city': 'Bangalore',
        'latitude': 12.9288,
        'longitude': 77.5812,
        'monthly_rent': 13000,
        'security_deposit': 15000,
        'gender_category': 'Girls',
        'room_type': 'Double Sharing',
        'food_available': True,
        'wifi_available': True,
        'ac_available': False,
        'laundry_available': True,
        'parking_available': True,
        'cctv_available': True,
        'housekeeping_available': True,
        'attached_washroom': True,
        'availability': 'Within 15 Days',
        'rules': 'Girls only residence. Visiting hours for family 9 AM - 7 PM in reception.',
        'verified': True,
        'is_sample': True,
        'owner_name': 'Lakshmi Narayan (Demo Host)',
        'owner_phone': '+91 94490 11223',
        'owner_email': 'lakshmi.haven@example.com',
        'photos': [
            'images/pg/pg8_main.svg'
        ]
    },
    {
        'name': 'Marathahalli Urban Nest',
        'description': 'Strategically situated near Kalamandir Marathahalli with swift bus and auto connectivity to Embassy Tech Village and Outer Ring Road. Budget friendly twin and four sharing options with delicious Andhra style meals. [Demo Listing]',
        'address': '#67, Outer Ring Road, Near Kalamandir, Marathahalli',
        'area': 'Marathahalli',
        'city': 'Bangalore',
        'latitude': 12.9555,
        'longitude': 77.6985,
        'monthly_rent': 7500,
        'security_deposit': 8000,
        'gender_category': 'Boys',
        'room_type': 'Triple Sharing',
        'food_available': True,
        'wifi_available': True,
        'ac_available': False,
        'laundry_available': True,
        'parking_available': True,
        'cctv_available': True,
        'housekeeping_available': True,
        'attached_washroom': False,
        'availability': 'Immediate',
        'rules': 'Affordable community living. Cleanliness in shared spaces expected from all residents.',
        'verified': False,
        'is_sample': True,
        'owner_name': 'Venkat Rao (Demo Host)',
        'owner_phone': '+91 97310 99887',
        'owner_email': 'venkat.nest@example.com',
        'photos': [
            'images/pg/pg9_main.svg'
        ]
    },
    {
        'name': 'Sarjapur Grand Coliving Manor',
        'description': 'Upscale co-living property along Sarjapur Road near Wipro Corporate Office. Contemporary interiors, modular workstations, gym facility, community movie nights, and private chef dinners. Perfect blend of community and privacy. [Demo Listing]',
        'address': '#210, Doddakannelli, Sarjapur Road',
        'area': 'Sarjapur Road',
        'city': 'Bangalore',
        'latitude': 12.9115,
        'longitude': 77.6890,
        'monthly_rent': 17500,
        'security_deposit': 22000,
        'gender_category': 'Co-living',
        'room_type': 'Single Sharing',
        'food_available': True,
        'wifi_available': True,
        'ac_available': True,
        'laundry_available': True,
        'parking_available': True,
        'cctv_available': True,
        'housekeeping_available': True,
        'attached_washroom': True,
        'availability': 'Immediate',
        'rules': 'Professional co-living code of conduct. Pet friendly on designated floors.',
        'verified': True,
        'is_sample': True,
        'owner_name': 'Divya Patel (Demo Host)',
        'owner_phone': '+91 98800 55443',
        'owner_email': 'divya.manor@example.com',
        'photos': [
            'images/pg/pg10_main.svg'
        ]
    },
    {
        'name': 'Manyata View Executive PG for Women',
        'description': 'Located opposite Manyata Embassy Business Park in Hebbal. Super quick commute for tech employees. Features fingerprint access, 24/7 power backup, hygienic kitchen with customized food plans, and spacious wardrobes. [Demo Listing]',
        'address': '#45, Nagawara Ring Road, Hebbal',
        'area': 'Hebbal',
        'city': 'Bangalore',
        'latitude': 13.0410,
        'longitude': 77.6180,
        'monthly_rent': 12500,
        'security_deposit': 15000,
        'gender_category': 'Girls',
        'room_type': 'Double Sharing',
        'food_available': True,
        'wifi_available': True,
        'ac_available': True,
        'laundry_available': True,
        'parking_available': True,
        'cctv_available': True,
        'housekeeping_available': True,
        'attached_washroom': True,
        'availability': 'Immediate',
        'rules': 'Ladies only PG. Safety first with on-site supervisor and emergency alarms.',
        'verified': True,
        'is_sample': True,
        'owner_name': 'Shalini Krishnan (Demo Host)',
        'owner_phone': '+91 99800 66778',
        'owner_email': 'shalini.manyata@example.com',
        'photos': [
            'images/pg/pg11_main.svg'
        ]
    },
    {
        'name': 'Metro Link Residency Rajajinagar',
        'description': 'Charming PG located 300 meters from Rajajinagar Metro Station. Quick transit to Majestic, Malleshwaram, and Central Bangalore. Clean rooms, high speed Wi-Fi, daily sanitization, and delicious homemade Karnataka meals. [Demo Listing]',
        'address': '#19, 10th Main, 2nd Block, Rajajinagar',
        'area': 'Rajajinagar',
        'city': 'Bangalore',
        'latitude': 12.9965,
        'longitude': 77.5515,
        'monthly_rent': 10000,
        'security_deposit': 12000,
        'gender_category': 'Co-living',
        'room_type': 'Double Sharing',
        'food_available': True,
        'wifi_available': True,
        'ac_available': False,
        'laundry_available': True,
        'parking_available': True,
        'cctv_available': True,
        'housekeeping_available': True,
        'attached_washroom': True,
        'availability': 'Immediate',
        'rules': 'Peaceful residential zone. Respect neighborhood serenity.',
        'verified': True,
        'is_sample': True,
        'owner_name': 'Basavaraj Patil (Demo Host)',
        'owner_phone': '+91 94800 22334',
        'owner_email': 'basavaraj.metro@example.com',
        'photos': [
            'images/pg/pg12_main.svg'
        ]
    }
]


def seed_database(drop_existing=False):
    app = create_app()
    with app.app_context():
        if drop_existing:
            print("Dropping all existing database tables...")
            db.drop_all()

        print("Creating all tables if they do not exist...")
        db.create_all()

        # 1. Create Default Admin User
        admin_user = User.query.filter_by(email='admin@nivora.com').first()
        if not admin_user:
            admin_user = User(
                name='NIVORA Admin',
                email='admin@nivora.com',
                phone='+91 98000 00001',
                role='admin'
            )
            admin_user.set_password('Admin@123')
            db.session.add(admin_user)
            print("Created default admin: admin@nivora.com / Admin@123")

        # 2. Create Demo User
        demo_user = User.query.filter_by(email='user@example.com').first()
        if not demo_user:
            demo_user = User(
                name='Aditya Sharma',
                email='user@example.com',
                phone='+91 98765 43210',
                role='user'
            )
            demo_user.set_password('User@123')
            db.session.add(demo_user)
            print("Created demo user: user@example.com / User@123")

        db.session.commit()

        # 3. Seed Sample PG Listings
        if PGListing.query.count() == 0:
            print(f"Seeding {len(SAMPLE_PGS)} Bangalore sample PG accommodations...")
            for pg_data in SAMPLE_PGS:
                photos = pg_data.pop('photos', [])
                pg = PGListing(**pg_data)
                pg.owner_id = admin_user.id
                db.session.add(pg)
                db.session.flush()  # to obtain pg.id

                # Add photos
                for idx, photo_path in enumerate(photos):
                    photo = PGPhoto(
                        pg_id=pg.id,
                        image_path=photo_path,
                        is_primary=(idx == 0),
                        caption=f"View of {pg.name}"
                    )
                    db.session.add(photo)

            db.session.commit()
            print("PG listings seeded successfully.")

        # 4. Seed a couple of demo favourites & enquiries for demo_user
        if Favourite.query.count() == 0 and demo_user:
            first_pg = PGListing.query.first()
            second_pg = PGListing.query.offset(1).first()
            if first_pg:
                db.session.add(Favourite(user_id=demo_user.id, pg_id=first_pg.id))
            if second_pg:
                db.session.add(Favourite(user_id=demo_user.id, pg_id=second_pg.id))
            
            # Seed enquiry
            if first_pg:
                db.session.add(Enquiry(
                    user_id=demo_user.id,
                    pg_id=first_pg.id,
                    name=demo_user.name,
                    email=demo_user.email,
                    phone=demo_user.phone,
                    message="Hi, I am relocating to Bangalore next week for an IT job. Is a single room available from the 1st?",
                    status='Pending'
                ))
            db.session.commit()
            print("Demo favourites and enquiry seeded.")

        print("NIVORA Database Initialization Complete!")


if __name__ == '__main__':
    import sys
    drop = '--reset' in sys.argv
    seed_database(drop_existing=drop)

