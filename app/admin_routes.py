from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from app import db
from app.models import Subject, Pin, Image, HomeContent, SiteSettings
from functools import wraps
import os
import time
import re
from werkzeug.utils import secure_filename
from sqlalchemy import func
import base64
import uuid

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


# Admin required decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            if request.is_json:
                return jsonify({'error': 'Unauthorized'}), 401
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function


# ==================== ADMIN LOGIN ====================
@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'Kelex789590':
            session['admin_logged_in'] = True
            return redirect(url_for('admin.dashboard'))
        return render_template('admin_login.html', error='Invalid credentials')
    return render_template('admin_login.html')


@admin_bp.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin.login'))


# ==================== ADMIN DASHBOARD ====================
@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    return render_template('admin_dashboard.html')


@admin_bp.route('/')
@admin_required
def index():
    return render_template('admin_dashboard.html')


# ==================== HOME CONTENT MANAGEMENT ====================
@admin_bp.route('/get_home_content')
@admin_required
def get_home_content():
    sections = ['hero_title', 'hero_text', 'moving_tagline', 'whatsapp_link',
                'telegram_link', 'vip_text', 'vip_number', 'need_help_text',
                'support_email', 'footer_text']
    content = {}
    for section in sections:
        home = HomeContent.query.filter_by(section=section).first()
        content[section] = home.content if home else ''
    return jsonify(content)


@admin_bp.route('/update_home_content', methods=['POST'])
@admin_required
def update_home_content():
    data = request.json
    for key, value in data.items():
        home = HomeContent.query.filter_by(section=key).first()
        if home:
            home.content = value
        else:
            home = HomeContent(section=key, content=value, content_type='text')
            db.session.add(home)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Home content updated!'})


# ==================== SUBJECT MANAGEMENT ====================
@admin_bp.route('/get_subjects')
@admin_required
def get_subjects():
    subjects = Subject.query.order_by(Subject.display_order, Subject.name).all()
    return jsonify([{
        'id': s.id,
        'name': s.name,
        'exam_type': s.exam_type,
        'has_practical': s.has_practical,
        'icon': s.icon,
        'pin_count': Pin.query.filter_by(subject_id=s.id).count()
    } for s in subjects])


@admin_bp.route('/add_subject', methods=['POST'])
@admin_required
def add_subject():
    name = request.form.get('name', '').strip()
    exam_type = request.form.get('exam_type')
    icon = request.form.get('icon', 'fa-book')
    has_practical = request.form.get('has_practical') == 'true'

    if not name:
        return jsonify({'success': False, 'error': 'Subject name required'})

    existing = Subject.query.filter_by(name=name).first()
    if existing:
        return jsonify({'success': False, 'error': 'Subject already exists'})

    subject = Subject(
        name=name,
        exam_type=exam_type,
        icon=icon,
        has_practical=has_practical,
        show_on_homepage=True
    )
    db.session.add(subject)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Subject added!'})


@admin_bp.route('/update_subject/<int:id>', methods=['POST'])
@admin_required
def update_subject(id):
    subject = Subject.query.get_or_404(id)
    name = request.form.get('name')
    icon = request.form.get('icon')
    has_practical = request.form.get('has_practical') == 'true'
    exam_type = request.form.get('exam_type')

    if name:
        subject.name = name
    if icon:
        subject.icon = icon
    subject.has_practical = has_practical
    if exam_type:
        subject.exam_type = exam_type

    db.session.commit()
    return jsonify({'success': True, 'message': 'Subject updated!'})


@admin_bp.route('/delete_subject/<int:id>', methods=['POST'])
@admin_required
def delete_subject(id):
    subject = Subject.query.get_or_404(id)
    subject_name = subject.name

    pins = Pin.query.filter_by(subject_id=id).all()
    pin_count = len(pins)

    for pin in pins:
        for img in pin.images:
            if img.image_path:
                filepath = os.path.join('app/static', img.image_path)
                if os.path.exists(filepath):
                    try:
                        os.remove(filepath)
                    except:
                        pass
            db.session.delete(img)
        db.session.delete(pin)

    db.session.delete(subject)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': f'Subject "{subject_name}" deleted. {pin_count} PIN(s) also removed.'
    })


# ==================== PIN MANAGEMENT ====================
def save_base64_image(base64_data, pin_id):
    """Save base64 image to disk and return path"""
    try:
        # Extract the base64 data (remove data:image/png;base64, prefix)
        if ',' in base64_data:
            base64_string = base64_data.split(',')[1]
        else:
            base64_string = base64_data

        # Decode base64
        image_data = base64.b64decode(base64_string)

        # Generate unique filename
        filename = f"pin_{pin_id}_{uuid.uuid4().hex[:8]}.png"

        # Ensure upload directory exists - FIXED PATH
        upload_dir = os.path.join('app/static/uploads/pins')
        os.makedirs(upload_dir, exist_ok=True)

        # Save file
        filepath = os.path.join(upload_dir, filename)
        with open(filepath, 'wb') as f:
            f.write(image_data)

        # Return CORRECT path for database (with /static/)
        return f'/static/uploads/pins/{filename}'  # FIXED: Added /static/
    except Exception as e:
        print(f"Error saving image: {str(e)}")
        return None

def extract_and_save_images(html_content, pin_id):
    """Extract base64 images from HTML and save them as files"""
    # Find all base64 images in the HTML
    pattern = r'src="(data:image/[^;]+;base64,[^"]+)"'
    matches = re.findall(pattern, html_content)

    saved_paths = []
    for idx, base64_img in enumerate(matches):
        saved_path = save_base64_image(base64_img, pin_id)
        if saved_path:
            saved_paths.append(saved_path)
            # Replace base64 with FULL file path in HTML
            html_content = html_content.replace(base64_img, saved_path)  # FIXED: Use full path directly

    return html_content, saved_paths


@admin_bp.route('/get_all_pins')
@admin_required
def get_all_pins():
    try:
        pins = Pin.query.order_by(Pin.id.desc()).all()
        result = []
        for p in pins:
            subject_name = p.subject_name
            if not subject_name and p.subject:
                subject_name = p.subject.name
            if not subject_name:
                subject_name = 'Unknown'

            result.append({
                'id': p.id,
                'pin_code': p.pin_code,
                'subject_name': subject_name,
                'views': p.views,
                'is_active': p.is_active if hasattr(p, 'is_active') else True,
            })
        return jsonify(result)
    except Exception as e:
        print(f"Error in get_all_pins: {str(e)}")
        return jsonify([])


@admin_bp.route('/get_pin/<int:id>')
@admin_required
def get_pin(id):
    pin = Pin.query.get_or_404(id)
    return jsonify({
        'id': pin.id,
        'pin_code': pin.pin_code,
        'subject_name': pin.subject_name or (pin.subject.name if pin.subject else ''),
        'answer_text': pin.answer_text,
        'posted_by': getattr(pin, 'posted_by', 'AnswerPoint'),
        'header_color': getattr(pin, 'header_color', '#ffffff'),
        'answer_text_color': getattr(pin, 'answer_text_color', '#1f2937'),
        'views': pin.views,
        'is_active': pin.is_active if hasattr(pin, 'is_active') else True,
    })


@admin_bp.route('/get_pin_answer/<int:id>')
@admin_required
def get_pin_answer(id):
    pin = Pin.query.get_or_404(id)
    return jsonify({
        'success': True,
        'answer_text': pin.answer_text or '',
        'pin_code': pin.pin_code,
        'subject_name': pin.subject_name or '',
        'posted_by': getattr(pin, 'posted_by', 'AnswerPoint'),
        'header_color': getattr(pin, 'header_color', '#ffffff'),
        'answer_text_color': getattr(pin, 'answer_text_color', '#1f2937')
    })


@admin_bp.route('/check_pin/<pin_code>')
@admin_required
def check_pin(pin_code):
    pin = Pin.query.filter_by(pin_code=pin_code).first()
    return jsonify({'exists': pin is not None})


@admin_bp.route('/create_pin_simple', methods=['POST'])
@admin_required
def create_pin_simple():
    try:
        pin_code = request.form.get('pin_code', '').strip()
        subject_name = request.form.get('subject_name', '').strip()
        posted_by = request.form.get('posted_by', 'AnswerPoint')
        header_color = request.form.get('header_color', '#ffffff')
        answer_text_color = request.form.get('answer_text_color', '#1f2937')
        answer_text = request.form.get('answer_text', '')

        # Validation
        if not pin_code or len(pin_code) != 3:
            return jsonify({'success': False, 'message': 'PIN must be exactly 3 digits'})
        if not subject_name:
            return jsonify({'success': False, 'message': 'Subject name is required'})
        if not answer_text or answer_text == '<p><br></p>':
            return jsonify({'success': False, 'message': 'Answer content is required'})

        # Check if PIN exists
        existing = Pin.query.filter_by(pin_code=pin_code).first()
        if existing:
            return jsonify({'success': False, 'message': f'PIN {pin_code} already exists!'})

        # Create PIN - NO subject_id being set!
        pin = Pin(
            pin_code=pin_code,
            subject_name=subject_name,
            posted_by=posted_by,
            header_color=header_color,
            answer_text_color=answer_text_color,
            answer_text=answer_text,
            is_active=True,
            views=0
        )
        db.session.add(pin)
        db.session.flush()

        # Extract and save images from answer_text
        processed_html, saved_images = extract_and_save_images(answer_text, pin.id)
        pin.answer_text = processed_html

        # Save image records to database
        for img_path in saved_images:
            image = Image(
                pin_id=pin.id,
                image_path=img_path
            )
            db.session.add(image)

        db.session.commit()

        return jsonify({'success': True, 'message': 'PIN created successfully!', 'pin_id': pin.id})

    except Exception as e:
        print(f"Error creating PIN: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@admin_bp.route('/update_pin_full', methods=['POST'])
@admin_required
def update_pin_full():
    try:
        pin_id = request.form.get('pin_id')
        if not pin_id:
            return jsonify({'success': False, 'message': 'PIN ID is required'})

        pin = Pin.query.get_or_404(int(pin_id))

        # Update fields
        pin.pin_code = request.form.get('pin_code', pin.pin_code)
        pin.subject_name = request.form.get('subject_name', pin.subject_name)
        pin.posted_by = request.form.get('posted_by', pin.posted_by)
        pin.header_color = request.form.get('header_color', pin.header_color)
        pin.answer_text_color = request.form.get('answer_text_color', pin.answer_text_color)

        answer_text = request.form.get('answer_text', pin.answer_text)

        # Extract and save new images
        processed_html, saved_images = extract_and_save_images(answer_text, pin.id)
        pin.answer_text = processed_html

        # Save new image records (NO file_name)
        for img_path in saved_images:
            # Check if image already exists
            existing = Image.query.filter_by(pin_id=pin.id, image_path=img_path).first()
            if not existing:
                image = Image(
                    pin_id=pin.id,
                    image_path=img_path
                )
                db.session.add(image)

        db.session.commit()
        return jsonify({'success': True, 'message': 'PIN updated successfully!'})

    except Exception as e:
        print(f"Error updating PIN: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})


@admin_bp.route('/delete_pin/<int:id>', methods=['POST'])
@admin_required
def delete_pin(id):
    pin = Pin.query.get_or_404(id)

    # Delete associated image files
    for img in pin.images:
        if img.image_path:
            filepath = os.path.join('app/static', img.image_path)
            if os.path.exists(filepath):
                try:
                    os.remove(filepath)
                except:
                    pass
        db.session.delete(img)

    db.session.delete(pin)
    db.session.commit()
    return jsonify({'success': True, 'message': 'PIN deleted!'})


@admin_bp.route('/toggle_pin/<int:id>', methods=['POST'])
@admin_required
def toggle_pin(id):
    pin = Pin.query.get_or_404(id)
    pin.is_active = not pin.is_active
    db.session.commit()
    return jsonify({'success': True, 'message': f'PIN {"activated" if pin.is_active else "deactivated"}!'})


@admin_bp.route('/upload_temp_image', methods=['POST'])
@admin_required
def upload_temp_image():
    file = request.files.get('image')
    if file and file.filename:
        filename = secure_filename(f"temp_{int(time.time())}_{file.filename}")
        upload_dir = 'app/static/uploads/temp'
        os.makedirs(upload_dir, exist_ok=True)
        filepath = os.path.join(upload_dir, filename)
        file.save(filepath)
        return jsonify({'success': True, 'url': f'/static/uploads/temp/{filename}'})
    return jsonify({'success': False, 'error': 'No file uploaded'})


# ==================== TIMETABLE MANAGEMENT ====================
@admin_bp.route('/get_timetable_text')
@admin_required
def get_timetable_text():
    waec = SiteSettings.query.filter_by(setting_key='waec_timetable_text').first()
    neco = SiteSettings.query.filter_by(setting_key='neco_timetable_text').first()
    return jsonify({
        'waec': waec.setting_value if waec else '',
        'neco': neco.setting_value if neco else ''
    })


@admin_bp.route('/save_timetable_text', methods=['POST'])
@admin_required
def save_timetable_text():
    data = request.json
    waec = SiteSettings.query.filter_by(setting_key='waec_timetable_text').first()
    neco = SiteSettings.query.filter_by(setting_key='neco_timetable_text').first()

    if waec:
        waec.setting_value = data.get('waec', '')
    else:
        waec = SiteSettings(setting_key='waec_timetable_text', setting_value=data.get('waec', ''))
        db.session.add(waec)

    if neco:
        neco.setting_value = data.get('neco', '')
    else:
        neco = SiteSettings(setting_key='neco_timetable_text', setting_value=data.get('neco', ''))
        db.session.add(neco)

    db.session.commit()
    return jsonify({'success': True, 'message': 'Timetable saved!'})


# ==================== SITE SETTINGS ====================
@admin_bp.route('/get_site_settings')
@admin_required
def get_site_settings():
    site_name = SiteSettings.query.filter_by(setting_key='site_name').first()
    admin_email = SiteSettings.query.filter_by(setting_key='admin_email').first()
    return jsonify({
        'site_name': site_name.setting_value if site_name else 'AnswerPoint',
        'admin_email': admin_email.setting_value if admin_email else ''
    })


@admin_bp.route('/update_site_settings', methods=['POST'])
@admin_required
def update_site_settings():
    data = request.json

    site_name = SiteSettings.query.filter_by(setting_key='site_name').first()
    if site_name:
        site_name.setting_value = data.get('site_name', 'AnswerPoint')
    else:
        site_name = SiteSettings(setting_key='site_name', setting_value=data.get('site_name', 'AnswerPoint'))
        db.session.add(site_name)

    admin_email = SiteSettings.query.filter_by(setting_key='admin_email').first()
    if admin_email:
        admin_email.setting_value = data.get('admin_email', '')
    else:
        admin_email = SiteSettings(setting_key='admin_email', setting_value=data.get('admin_email', ''))
        db.session.add(admin_email)

    db.session.commit()
    return jsonify({'success': True, 'message': 'Settings saved!'})


# ==================== STATISTICS ====================
@admin_bp.route('/stats')
@admin_required
def stats():
    total_pins = Pin.query.count()
    total_subjects = Subject.query.count()
    total_views = db.session.query(func.sum(Pin.views)).scalar() or 0
    total_images = Image.query.count()
    active_pins = Pin.query.filter_by(is_active=True).count()

    return jsonify({
        'total_pins': total_pins,
        'total_subjects': total_subjects,
        'total_views': total_views,
        'total_images': total_images,
        'active_pins': active_pins
    })
