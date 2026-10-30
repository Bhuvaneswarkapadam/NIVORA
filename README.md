# NIVORA
# NIVORA – Premium PG Finder & Accommodation Discovery

> **Find Your Place. Feel at Home.**  
> A full-stack web application designed for students, working professionals, and newcomers relocating to Bangalore. Discover verified paying guest (PG) accommodations, co-living spaces, and shared flats with real location-based discovery, distance sorting, transparent rents, interactive Leaflet maps, and direct host enquiries.

---

## 1. Project Overview & Objectives

**NIVORA** eliminates the friction, inflated broker commissions, and misleading listings typical of urban relocation in Bangalore. The platform provides:
- **Location-Based Discovery:** Real geographic coordinates for 15 primary Bangalore tech corridors and residential hubs.
- **Precision Distance Sorting:** Calculates true distance (in kilometers) using the Haversine formula from the user's current GPS location or selected landmark.
- **Interactive Leaflet & OpenStreetMap Mapping:** Live pins, custom price markers, and interactive popups with direct links to listing details.
- **Transparent Accommodation Details:** Honest breakdowns of monthly rent, security deposit, gender categories (Boys, Girls, Co-living), room sharing, meal inclusion, and verified facilities (Wi-Fi, AC, Laundry, Parking, 24/7 CCTV, Daily Housekeeping, Ensuite Bathrooms).
- **Direct Owner Communications:** Click-to-call, validated WhatsApp enquiry chat links, and in-platform enquiry routing with status tracking.
- **Administrator Management Suite:** Complete control over listings, multiple photo uploads with secure file sanitization, verified badges, user accounts, and tenant enquiry pipelines.

---

## 2. Technology Stack

- **Backend:** Python 3 (tested on 3.14), Flask, Flask-SQLAlchemy, Flask-Login, Flask-WTF, WTForms.
- **Database:** SQLite 3 with SQLAlchemy ORM.
- **Frontend:** Semantic HTML5, CSS3, Modern JavaScript (ES6+), Bootstrap 5.3, Font Awesome 6 Icons.
- **Maps & Geolocation:** Leaflet.js, OpenStreetMap, Browser Geolocation API, Haversine formula.
- **Security:** Werkzeug password hashing (pbkdf2:sha256), CSRF protection across all forms, role-based authorization (`@admin_required`), parameterized ORM queries, safe file uploads with extension whitelist and timestamp collision protection.
- **Testing:** Pytest automated test suite.

---

## 3. Project Structure

```
NIVORA/
├── app.py                      # Flask application factory, public, auth & admin routes
├── config.py                   # Environment configuration & security settings
├── database.py                 # SQLAlchemy db instance
├── forms.py                    # Flask-WTF forms with CSRF & input validators
├── models.py                   # User, PGListing, PGPhoto, Favourite, Enquiry models
├── requirements.txt            # Python dependencies
├── pytest.ini                  # Pytest configuration
├── seed.py                     # Database initialization & Bangalore demo seeder
├── generate_assets.py          # SVG graphics generator for brand logo & properties
├── .env.example                # Environment variables template
├── .gitignore                  # Git exclusions
├── README.md                   # Documentation
│
├── instance/
│   └── nivora.db               # SQLite database file
│
├── templates/
│   ├── base.html               # Master layout with luxury black & gold navbar and footer
│   ├── index.html              # Homepage with hero search, popular hubs, featured stays
│   ├── search.html             # Advanced filter sidebar, PG cards, interactive Leaflet map
│   ├── pg_details.html         # Image gallery, amenities, house rules, map, enquiry form
│   ├── about.html              # Mission, relocation pillars, Bangalore coverage
│   ├── contact.html            # Contact info, Bangalore headquarters, feedback form
│   ├── locations.html          # Directory of all 15 Bangalore tech corridors
│   ├── login.html              # Sign in with demo credential shortcuts
│   ├── register.html           # User registration with password validation
│   ├── profile.html            # User dashboard: profile edit, password, enquiry history
│   ├── favorites.html          # Saved PGs wishlist with fast removal
│   ├── 404.html                # Custom Not Found page
│   ├── 500.html                # Custom Server Error page
│   │
│   └── admin/
│       ├── dashboard.html      # Metrics: Total listings, verified stays, users, enquiries
│       ├── manage_pgs.html     # Inventory table, toggle verified badge, delete listings
│       ├── add_pg.html         # Add accommodation with photo uploads & auto-coordinates
│       ├── edit_pg.html        # Edit accommodation & gallery management
│       ├── manage_users.html   # User directory with roles and activity counts
│       └── enquiries.html      # Tenant enquiry pipeline with status updater
│
├── static/
│   ├── css/
│   │   ├── style.css           # Design system: brand palette, luxury typography, cards
│   │   ├── responsive.css      # Mobile, tablet, and responsive breakpoints
│   │   ├── auth.css            # Split authentication cards and form styling
│   │   └── admin.css           # Control center stats cards and data tables
│   │
│   ├── js/
│   │   ├── main.js             # Sticky navbar, toast notifications, favourites AJAX
│   │   ├── map.js              # Leaflet engine, gold price markers, GPS geolocation
│   │   ├── search.js           # Dynamic budget range slider, view mode toggler
│   │   └── validation.js       # Client-side input validation and phone sanitization
│   │
│   ├── images/
│   │   ├── logo.svg            # Official NIVORA vector brand logo
│   │   ├── favicon.svg         # Crisp mobile & desktop favicon
│   │   └── pg/                 # Accommodation architectural illustrations & photos
│   │
│   └── uploads/                # User and admin uploaded property photos
│
└── tests/
    ├── test_auth.py            # Authentication, hashing, duplicate prevention tests
    ├── test_search.py          # Area filters, budget, gender, Haversine distance tests
    └── test_admin.py           # Authorization, listing management, deletion tests
```

---

## 4. Installation & Quick Start

### Step 1: Clone or Navigate to the Workspace
```bash
cd c:\Users\WINDOWS\Desktop\NIVORA
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Initialize and Seed Database
Run the seed script to create all SQLite database tables and populate 12 sample accommodations across Bangalore's major neighborhoods along with test accounts:
```bash
python seed.py --reset
```

### Step 4: Run the Flask Web Application
```bash
python app.py
```
The server will start at: **`http://127.0.0.1:5000`**

### Step 5: Open in Google Chrome or Browser
Simply open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 5. Demo Credentials

The database seeder pre-configures credentials for instant evaluation:

| Role | Email | Password | Access Capabilities |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin@nivora.com` | `Admin@123` | Full Admin Portal, Add/Edit/Delete PGs, Photo Uploads, Verify Listings, Manage Enquiries & Users |
| **Resident User** | `user@example.com` | `User@123` | Save Favourites, Submit Enquiries, View Enquiry History, Manage Profile & Password |

---

## 6. Key Features & How to Use

### A. Real Bangalore Location Search
- Select any of Bangalore's 15 primary areas (e.g., *Koramangala, Indiranagar, HSR Layout, Whitefield, Bellandur, Electronic City, BTM Layout, Jayanagar, Marathahalli, Sarjapur Road, Hebbal, Rajajinagar, Yelahanka, Bommanahalli, Mahadevapura*).
- Click **"Find PGs Near My Location"** in the Hero or Search page:
  - Prompts browser for standard HTML5 geolocation permission.
  - Automatically calculates distance to each PG using the exact stored coordinates.
  - Places a marker on the map for your position and orders accommodations by shortest distance.

### B. Interactive Leaflet Map
- Fully integrated with OpenStreetMap tiles.
- Custom gold markers render rent prices directly on the map.
- Clicking any pin displays a rich popup featuring the accommodation photo, monthly rent, sharing type, area, and an instant link to full details.
- Toggle between **Split View**, **List View**, and **Map View** with one click.

### C. Advanced Multi-Filter Engine
- **Budget Slider:** Select maximum rent from ₹5,000 to ₹35,000+.
- **Gender:** Filter between *Boys PG*, *Girls PG*, and *Co-living*.
- **Sharing Type:** Filter by *Single Sharing (Private)*, *Double Sharing*, *Triple Sharing*, or *Four Sharing*.
- **Food:** Filter by meals included.
- **Facilities Checkboxes:** Combine filters for Wi-Fi, AC, Laundry, Parking, 24/7 CCTV, Housekeeping, and Attached Bathroom.

### D. Saving Favourites
- Click the heart icon on any PG card to instantly save or remove it from your wishlist via AJAX.
- View and manage your saved properties at `/favorites`.

### E. Direct Owner WhatsApp & Enquiry Pipeline
- Each listing includes a validated **WhatsApp Owner** button that pre-formats a polite message with property details directly to the host's phone number.
- Users and guests can also submit an on-page enquiry form which stores the inquiry in SQLite and appears in the user's dashboard and the Admin portal.

### F. Admin Management
- Access `/admin/dashboard` when logged in as an administrator.
- **Add Accommodation:** `/admin/pg/add` features automatic coordinate auto-fill whenever a Bangalore area is selected from the dropdown, plus multi-image file uploads saved to `static/uploads/`.
- **Verify Stays:** Toggle the verified badge with a single click.
- **Track Enquiries:** Change status between *Pending*, *In Review*, *Contacted*, and *Resolved*.

---

## 7. Running Automated Tests

Run the full pytest suite inside the project root:
```bash
python -m pytest -v
```

All 10 unit and integration tests will execute, verifying:
1. Regular users and guests are forbidden from accessing admin routes.
2. Administrators can add and delete accommodation listings.
3. User registration securely hashes passwords using Werkzeug.
4. Duplicate email registrations are rejected.
5. User login and logout session state.
6. Haversine distance calculations produce accurate geographic distances in kilometers.
7. Filtering by Bangalore area works accurately.
8. Filtering by budget rent works accurately.
9. Filtering by gender category works accurately.
10. The Leaflet `/api/pgs` JSON marker endpoint delivers properly structured responses.

---

## 8. License & Attribution

Designed and developed for **NIVORA** – Bangalore's premier accommodation discovery platform. Built with Python, Flask, Bootstrap 5, and Leaflet.js.

