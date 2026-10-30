import os
import math
from functools import wraps
from datetime import datetime, timezone
from pathlib import Path
from flask import (
    Flask, render_template, redirect, url_for, flash, request, jsonify, abort, current_app
)
from flask_login import (
    LoginManager, login_user, logout_user, login_required, current_user
)
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename

from config import Config
from database import db
from models import User, PGListing, PGPhoto, Favourite, Enquiry, haversine_distance
from forms import (
    RegistrationForm, LoginForm, ProfileUpdateForm, ChangePasswordForm,
    PGListingForm, EnquiryForm, ContactForm, BANGALORE_AREAS
)

# Custom admin decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please sign in with administrator credentials.', 'warning')
            return redirect(url_for('login', next=request.url))
        if not current_user.is_admin:
            flash('Access denied: Administrator privileges required.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Ensure required runtime folders exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.instance_path, exist_ok=True)

    # Initialize extensions
    db.init_app(app)
    csrf = CSRFProtect(app)
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'warning'

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Helper context processor
    @app.context_processor
    def inject_global_data():
        return {
            'now': datetime.now(timezone.utc),
            'bangalore_areas': [area[0] for area in BANGALORE_AREAS],
            'unread_enquiries_count': Enquiry.query.filter_by(status='Pending').count() if current_user.is_authenticated and current_user.is_admin else 0
        }

    # Template filters
    @app.template_filter('currency_inr')
    def currency_inr(value):
        try:
            return f"₹{int(value):,}"
        except (ValueError, TypeError):
            return f"₹{value}"

    # Helper function for safe image uploads
    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

    def save_uploaded_photo(file_storage):
        if not file_storage or file_storage.filename == '':
            return None
        if not allowed_file(file_storage.filename):
            return None
        filename = secure_filename(file_storage.filename)
        # Prepend unique timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        unique_name = f"{timestamp}_{filename}"
        save_path = Path(app.config['UPLOAD_FOLDER']) / unique_name
        file_storage.save(save_path)
        return f"uploads/{unique_name}"

    # ==========================================
    # PUBLIC ROUTES
    # ==========================================

    @app.route('/')
    def index():
        featured_pgs = PGListing.query.order_by(PGListing.verified.desc(), PGListing.id.desc()).limit(6).all()
        
        # Calculate listing count per popular Bangalore area
        popular_locations = [
            {'name': 'Koramangala', 'tagline': 'Startup Capital & Cafes', 'badge': 'Trending'},
            {'name': 'HSR Layout', 'tagline': 'Tech Hub & Tree Lined Sectors', 'badge': 'High Demand'},
            {'name': 'Indiranagar', 'tagline': 'Premium Nightlife & Metro', 'badge': 'Luxury'},
            {'name': 'BTM Layout', 'tagline': 'Affordable & Student Friendly', 'badge': 'Budget Friendly'},
            {'name': 'Whitefield', 'tagline': 'ITPL & Outer Metro Line', 'badge': 'Tech Corridor'},
            {'name': 'Bellandur', 'tagline': 'EcoWorld & Outer Ring Road', 'badge': 'Near Offices'},
            {'name': 'Electronic City', 'tagline': 'Infosys & Tech Campuses', 'badge': 'Tech Hub'},
            {'name': 'Jayanagar', 'tagline': 'Serene, Traditional & Green', 'badge': 'Peaceful'},
            {'name': 'Marathahalli', 'tagline': 'Ring Road Transit & Malls', 'badge': 'Great Transit'},
            {'name': 'Sarjapur Road', 'tagline': 'Gated Living & Tech Park', 'badge': 'Family & Coliving'}
        ]
        
        for loc in popular_locations:
            loc['count'] = PGListing.query.filter_by(area=loc['name']).count()

        total_pgs = PGListing.query.count()
        total_areas = len(BANGALORE_AREAS)
        
        return render_template(
            'index.html',
            featured_pgs=featured_pgs,
            popular_locations=popular_locations,
            total_pgs=total_pgs,
            total_areas=total_areas
        )

    @app.route('/search')
    def search():
        query_area = request.args.get('area', '').strip()
        search_keyword = request.args.get('q', '').strip()
        min_rent = request.args.get('min_rent', type=int)
        max_rent = request.args.get('max_rent', type=int)
        gender = request.args.get('gender', '').strip()
        room_type = request.args.get('room_type', '').strip()
        food = request.args.get('food', '').strip()
        sort_by = request.args.get('sort', 'newest').strip()
        
        # Geolocation parameters (from browser or selected area)
        user_lat = request.args.get('lat', type=float)
        user_lon = request.args.get('lon', type=float)
        location_label = request.args.get('location_name', '').strip()

        # Facility filters
        wifi = request.args.get('wifi') == '1'
        ac = request.args.get('ac') == '1'
        laundry = request.args.get('laundry') == '1'
        parking = request.args.get('parking') == '1'
        cctv = request.args.get('cctv') == '1'
        housekeeping = request.args.get('housekeeping') == '1'
        attached_washroom = request.args.get('attached_washroom') == '1'

        query = PGListing.query

        # Area / keyword search
        if query_area:
            query = query.filter(PGListing.area.ilike(f"%{query_area}%"))
        
        if search_keyword:
            keyword_filter = (
                PGListing.name.ilike(f"%{search_keyword}%") |
                PGListing.description.ilike(f"%{search_keyword}%") |
                PGListing.address.ilike(f"%{search_keyword}%") |
                PGListing.area.ilike(f"%{search_keyword}%")
            )
            query = query.filter(keyword_filter)

        # Budget filter
        if min_rent is not None:
            query = query.filter(PGListing.monthly_rent >= min_rent)
        if max_rent is not None:
            query = query.filter(PGListing.monthly_rent <= max_rent)

        # Gender & Room type
        if gender and gender.lower() != 'all':
            query = query.filter(PGListing.gender_category == gender)
        if room_type and room_type.lower() != 'all':
            query = query.filter(PGListing.room_type == room_type)
        if food == 'yes':
            query = query.filter(PGListing.food_available.is_(True))

        # Facility checkboxes
        if wifi:
            query = query.filter(PGListing.wifi_available.is_(True))
        if ac:
            query = query.filter(PGListing.ac_available.is_(True))
        if laundry:
            query = query.filter(PGListing.laundry_available.is_(True))
        if parking:
            query = query.filter(PGListing.parking_available.is_(True))
        if cctv:
            query = query.filter(PGListing.cctv_available.is_(True))
        if housekeeping:
            query = query.filter(PGListing.housekeeping_available.is_(True))
        if attached_washroom:
            query = query.filter(PGListing.attached_washroom.is_(True))

        # Fetch base results
        results = query.all()

        # Calculate distances if user coordinates available
        for pg in results:
            if user_lat and user_lon:
                pg.calculated_distance = pg.distance_from(user_lat, user_lon)
            else:
                pg.calculated_distance = None

        # Sorting
        if sort_by == 'rent_asc':
            results = sorted(results, key=lambda p: p.monthly_rent)
        elif sort_by == 'rent_desc':
            results = sorted(results, key=lambda p: p.monthly_rent, reverse=True)
        elif sort_by == 'distance' and user_lat and user_lon:
            results = sorted(results, key=lambda p: (p.calculated_distance is None, p.calculated_distance))
        else:
            # Default: recently updated/added first, verified first
            results = sorted(results, key=lambda p: (not p.verified, -p.id))

        # Prepare JSON data for Leaflet Map markers
        map_pgs_data = [pg.to_dict(user_lat, user_lon) for pg in results]

        return render_template(
            'search.html',
            pgs=results,
            total_results=len(results),
            map_pgs_data=map_pgs_data,
            selected_area=query_area,
            search_keyword=search_keyword,
            min_rent=min_rent or '',
            max_rent=max_rent or '',
            selected_gender=gender,
            selected_room_type=room_type,
            selected_food=food,
            sort_by=sort_by,
            user_lat=user_lat or '',
            user_lon=user_lon or '',
            location_label=location_label,
            wifi=wifi,
            ac=ac,
            laundry=laundry,
            parking=parking,
            cctv=cctv,
            housekeeping=housekeeping,
            attached_washroom=attached_washroom
        )

    @app.route('/api/pgs')
    def api_pgs():
        """JSON endpoint returning filtered PGs for dynamic Leaflet map updates"""
        area = request.args.get('area', '').strip()
        user_lat = request.args.get('lat', type=float)
        user_lon = request.args.get('lon', type=float)

        query = PGListing.query
        if area:
            query = query.filter(PGListing.area.ilike(f"%{area}%"))
        
        pgs = query.all()
        return jsonify([pg.to_dict(user_lat, user_lon) for pg in pgs])

    @app.route('/pg/<int:pg_id>', methods=['GET', 'POST'])
    def pg_details(pg_id):
        pg = db.get_or_404(PGListing, pg_id)
        enquiry_form = EnquiryForm()

        # Prepopulate enquiry form if user is logged in
        if current_user.is_authenticated and request.method == 'GET':
            enquiry_form.name.data = current_user.name
            enquiry_form.email.data = current_user.email
            enquiry_form.phone.data = current_user.phone

        if enquiry_form.validate_on_submit():
            enquiry = Enquiry(
                user_id=current_user.id if current_user.is_authenticated else None,
                pg_id=pg.id,
                name=enquiry_form.name.data.strip(),
                email=enquiry_form.email.data.strip(),
                phone=enquiry_form.phone.data.strip(),
                message=enquiry_form.message.data.strip(),
                status='Pending'
            )
            db.session.add(enquiry)
            db.session.commit()
            flash('Your enquiry has been sent to the property owner! They will contact you shortly.', 'success')
            return redirect(url_for('pg_details', pg_id=pg.id))

        # Check if favourited by current user
        is_favourited = False
        if current_user.is_authenticated:
            is_favourited = current_user.has_favourited(pg.id)

        # Similar / nearby PGs in same area
        similar_pgs = PGListing.query.filter(
            PGListing.area == pg.area,
            PGListing.id != pg.id
        ).limit(3).all()

        return render_template(
            'pg_details.html',
            pg=pg,
            enquiry_form=enquiry_form,
            is_favourited=is_favourited,
            similar_pgs=similar_pgs
        )

    @app.route('/api/toggle-favourite/<int:pg_id>', methods=['POST'])
    def toggle_favourite(pg_id):
        if not current_user.is_authenticated:
            return jsonify({'success': False, 'message': 'Please login to save favourites.'}), 401
        
        pg = db.get_or_404(PGListing, pg_id)
        fav = Favourite.query.filter_by(user_id=current_user.id, pg_id=pg.id).first()
        
        if fav:
            db.session.delete(fav)
            db.session.commit()
            return jsonify({'success': True, 'favourited': False, 'message': 'Removed from saved PGs.'})
        else:
            new_fav = Favourite(user_id=current_user.id, pg_id=pg.id)
            db.session.add(new_fav)
            db.session.commit()
            return jsonify({'success': True, 'favourited': True, 'message': 'Saved to your favourites!'})

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/contact', methods=['GET', 'POST'])
    def contact():
        form = ContactForm()
        if form.validate_on_submit():
            flash('Thank you for contacting NIVORA. Our support desk will reach out within 24 hours.', 'success')
            return redirect(url_for('contact'))
        return render_template('contact.html', form=form)

    @app.route('/locations')
    def locations():
        loc_stats = []
        for code, label in BANGALORE_AREAS:
            count = PGListing.query.filter_by(area=code).count()
            loc_stats.append({
                'name': code,
                'count': count
            })
        return render_template('locations.html', locations=loc_stats)

    # ==========================================
    # AUTHENTICATION ROUTES
    # ==========================================

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('profile'))
        
        form = RegistrationForm()
        if form.validate_on_submit():
            existing_user = User.query.filter_by(email=form.email.data.lower().strip()).first()
            if existing_user:
                flash('An account with this email address already exists. Please log in.', 'danger')
                return render_template('register.html', form=form)
            
            user = User(
                name=form.name.data.strip(),
                email=form.email.data.lower().strip(),
                phone=form.phone.data.strip(),
                role='user'
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()

            login_user(user)
            flash(f'Welcome to NIVORA, {user.name}! Your account has been created.', 'success')
            return redirect(url_for('profile'))
            
        return render_template('register.html', form=form)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            if current_user.is_admin:
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('profile'))

        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data.lower().strip()).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember.data)
                flash(f'Welcome back, {user.name}!', 'success')
                
                next_page = request.args.get('next')
                if next_page and next_page.startswith('/'):
                    return redirect(next_page)
                if user.is_admin:
                    return redirect(url_for('admin_dashboard'))
                return redirect(url_for('profile'))
            else:
                flash('Invalid email or password. Please verify your credentials.', 'danger')

        return render_template('login.html', form=form)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('You have been signed out safely.', 'info')
        return redirect(url_for('index'))

    # ==========================================
    # USER DASHBOARD & PROFILE
    # ==========================================

    @app.route('/profile', methods=['GET', 'POST'])
    @login_required
    def profile():
        profile_form = ProfileUpdateForm(prefix='profile')
        password_form = ChangePasswordForm(prefix='password')

        if profile_form.submit.data and profile_form.validate_on_submit():
            current_user.name = profile_form.name.data.strip()
            current_user.phone = profile_form.phone.data.strip()
            db.session.commit()
            flash('Your profile details have been successfully updated.', 'success')
            return redirect(url_for('profile'))

        if password_form.submit.data and password_form.validate_on_submit():
            if current_user.check_password(password_form.current_password.data):
                current_user.set_password(password_form.new_password.data)
                db.session.commit()
                flash('Your password was changed successfully.', 'success')
                return redirect(url_for('profile'))
            else:
                flash('The current password entered is incorrect.', 'danger')

        if request.method == 'GET':
            profile_form.name.data = current_user.name
            profile_form.phone.data = current_user.phone

        user_enquiries = Enquiry.query.filter_by(user_id=current_user.id).order_by(Enquiry.id.desc()).all()
        user_favourites = [fav.pg for fav in current_user.favourites.all()]

        return render_template(
            'profile.html',
            profile_form=profile_form,
            password_form=password_form,
            enquiries=user_enquiries,
            favourites=user_favourites
        )

    @app.route('/favorites')
    @login_required
    def favorites():
        saved_pgs = [fav.pg for fav in current_user.favourites.all()]
        return render_template('favorites.html', pgs=saved_pgs)

    # ==========================================
    # ADMIN ROUTES
    # ==========================================

    @app.route('/admin')
    @app.route('/admin/dashboard')
    @admin_required
    def admin_dashboard():
        total_users = User.query.count()
        total_pgs = PGListing.query.count()
        verified_pgs = PGListing.query.filter_by(verified=True).count()
        total_enquiries = Enquiry.query.count()
        pending_enquiries = Enquiry.query.filter_by(status='Pending').count()

        recent_enquiries = Enquiry.query.order_by(Enquiry.id.desc()).limit(8).all()
        recent_pgs = PGListing.query.order_by(PGListing.id.desc()).limit(6).all()

        return render_template(
            'admin/dashboard.html',
            total_users=total_users,
            total_pgs=total_pgs,
            verified_pgs=verified_pgs,
            total_enquiries=total_enquiries,
            pending_enquiries=pending_enquiries,
            recent_enquiries=recent_enquiries,
            recent_pgs=recent_pgs
        )

    @app.route('/admin/pgs')
    @admin_required
    def manage_pgs():
        search_query = request.args.get('q', '').strip()
        area_filter = request.args.get('area', '').strip()

        query = PGListing.query
        if search_query:
            query = query.filter(
                (PGListing.name.ilike(f"%{search_query}%")) |
                (PGListing.address.ilike(f"%{search_query}%"))
            )
        if area_filter:
            query = query.filter_by(area=area_filter)

        pgs = query.order_by(PGListing.id.desc()).all()
        return render_template('admin/manage_pgs.html', pgs=pgs, search_query=search_query, area_filter=area_filter)

    @app.route('/admin/pg/add', methods=['GET', 'POST'])
    @admin_required
    def add_pg():
        form = PGListingForm()
        if form.validate_on_submit():
            pg = PGListing(
                name=form.name.data.strip(),
                description=form.description.data.strip(),
                address=form.address.data.strip(),
                area=form.area.data,
                city=form.city.data.strip(),
                latitude=form.latitude.data,
                longitude=form.longitude.data,
                monthly_rent=form.monthly_rent.data,
                security_deposit=form.security_deposit.data,
                gender_category=form.gender_category.data,
                room_type=form.room_type.data,
                food_available=form.food_available.data,
                wifi_available=form.wifi_available.data,
                ac_available=form.ac_available.data,
                laundry_available=form.laundry_available.data,
                parking_available=form.parking_available.data,
                cctv_available=form.cctv_available.data,
                housekeeping_available=form.housekeeping_available.data,
                attached_washroom=form.attached_washroom.data,
                availability=form.availability.data,
                rules=form.rules.data.strip() if form.rules.data else None,
                verified=form.verified.data,
                is_sample=False,
                owner_id=current_user.id,
                owner_name=form.owner_name.data.strip(),
                owner_phone=form.owner_phone.data.strip(),
                owner_email=form.owner_email.data.strip() if form.owner_email.data else None
            )
            db.session.add(pg)
            db.session.flush()

            # Handle uploaded photos
            photos_uploaded = request.files.getlist(form.photos.name)
            saved_count = 0
            for idx, photo_file in enumerate(photos_uploaded):
                saved_path = save_uploaded_photo(photo_file)
                if saved_path:
                    db.session.add(PGPhoto(
                        pg_id=pg.id,
                        image_path=saved_path,
                        is_primary=(idx == 0),
                        caption=f"{pg.name} Photo"
                    ))
                    saved_count += 1

            db.session.commit()
            flash(f"Accommodation '{pg.name}' has been added successfully with {saved_count} photos.", 'success')
            return redirect(url_for('manage_pgs'))

        return render_template('admin/add_pg.html', form=form)

    @app.route('/admin/pg/<int:pg_id>/edit', methods=['GET', 'POST'])
    @admin_required
    def edit_pg(pg_id):
        pg = db.get_or_404(PGListing, pg_id)
        form = PGListingForm(obj=pg)

        if form.validate_on_submit():
            form.populate_obj(pg)
            
            # Handle additional photos if uploaded
            photos_uploaded = request.files.getlist(form.photos.name)
            has_existing = len(pg.photos) > 0
            for idx, photo_file in enumerate(photos_uploaded):
                saved_path = save_uploaded_photo(photo_file)
                if saved_path:
                    db.session.add(PGPhoto(
                        pg_id=pg.id,
                        image_path=saved_path,
                        is_primary=(not has_existing and idx == 0),
                        caption=f"{pg.name} Photo"
                    ))

            db.session.commit()
            flash(f"Accommodation '{pg.name}' updated successfully.", 'success')
            return redirect(url_for('manage_pgs'))

        return render_template('admin/edit_pg.html', form=form, pg=pg)

    @app.route('/admin/pg/<int:pg_id>/delete', methods=['POST'])
    @admin_required
    def delete_pg(pg_id):
        pg = db.get_or_404(PGListing, pg_id)
        name = pg.name
        db.session.delete(pg)
        db.session.commit()
        flash(f"Listing '{name}' was deleted.", 'info')
        return redirect(url_for('manage_pgs'))

    @app.route('/admin/pg/<int:pg_id>/toggle-verified', methods=['POST'])
    @admin_required
    def toggle_verified_pg(pg_id):
        pg = db.get_or_404(PGListing, pg_id)
        pg.verified = not pg.verified
        db.session.commit()
        status_str = "verified" if pg.verified else "unverified"
        flash(f"'{pg.name}' is now marked as {status_str}.", 'success')
        return redirect(request.referrer or url_for('manage_pgs'))

    @app.route('/admin/users')
    @admin_required
    def manage_users():
        users = User.query.order_by(User.id.desc()).all()
        return render_template('admin/manage_users.html', users=users)

    @app.route('/admin/enquiries')
    @admin_required
    def manage_enquiries():
        status_filter = request.args.get('status', '').strip()
        query = Enquiry.query
        if status_filter:
            query = query.filter_by(status=status_filter)
        enquiries = query.order_by(Enquiry.id.desc()).all()
        return render_template('admin/enquiries.html', enquiries=enquiries, status_filter=status_filter)

    @app.route('/admin/enquiry/<int:enquiry_id>/status', methods=['POST'])
    @admin_required
    def update_enquiry_status(enquiry_id):
        enquiry = db.get_or_404(Enquiry, enquiry_id)
        new_status = request.form.get('status', 'Pending')
        if new_status in ['Pending', 'In Review', 'Contacted', 'Resolved']:
            enquiry.status = new_status
            db.session.commit()
            flash(f"Enquiry #{enquiry.id} updated to '{new_status}'.", 'success')
        return redirect(url_for('manage_enquiries'))

    # ==========================================
    # ERROR HANDLERS
    # ==========================================

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        db.session.rollback()
        return render_template('500.html'), 500

    @app.errorhandler(403)
    def access_forbidden(e):
        flash('You do not have permission to access that resource.', 'danger')
        return redirect(url_for('index'))

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
