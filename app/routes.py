from flask import Blueprint, render_template, request, jsonify, session, send_from_directory, abort
from app import db
from app.models import Subject, Pin, Image, HomeContent, ExamTimetable, SiteSettings
import os

# ==================== BLUEPRINT INITIALIZATION ====================
main_bp = Blueprint('main', __name__)

# ==================== IMAGE SERVING ROUTES ====================

@main_bp.route('/static/uploads/<path:filename>')
def serve_upload(filename):
    """Serve uploaded files from static/uploads directory"""
    base_dir = os.path.dirname(os.path.dirname(__file__))  # Go to project root
    upload_folder = os.path.join(base_dir, 'static', 'uploads')

    # Try different possible paths
    possible_paths = [
        os.path.join(upload_folder, filename),
        os.path.join(upload_folder, 'pins', filename),
        os.path.join(upload_folder, 'images', filename),
    ]

    for file_path in possible_paths:
        if os.path.exists(file_path):
            directory = os.path.dirname(file_path)
            actual_filename = os.path.basename(file_path)
            return send_from_directory(directory, actual_filename)

    print(f"❌ Image not found: {filename}")
    abort(404)


@main_bp.route('/static/uploads/pins/<path:filename>')
def serve_pin_image(filename):
    """Serve images from pins subfolder"""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    # Try multiple possible locations
    possible_locations = [
        os.path.join(base_dir, 'app', 'static', 'uploads', 'pins', filename),
        os.path.join(base_dir, 'static', 'uploads', 'pins', filename),
        os.path.join(base_dir, 'app', 'static', 'uploads', filename),
        os.path.join(base_dir, 'static', 'uploads', filename),
    ]

    for file_path in possible_locations:
        if os.path.exists(file_path):
            directory = os.path.dirname(file_path)
            actual_filename = os.path.basename(file_path)
            print(f"✅ Serving image: {file_path}")
            return send_from_directory(directory, actual_filename)

    print(f"❌ Pin image not found: {filename}")
    abort(404)


@main_bp.route('/debug/check_image_paths')
def check_image_paths():
    """Debug: Check what image paths are stored in database"""
    pins_with_images = Pin.query.filter(Pin.answer_text.like('%<img%')).all()

    results = []
    for pin in pins_with_images:
        # Extract image src from answer_text
        import re
        images = re.findall(r'src="([^"]+)"', pin.answer_text)
        for img in images:
            # Check if file exists
            base_dir = os.path.dirname(os.path.dirname(__file__))
            # Try to find the file
            filename = img.split('/')[-1]
            possible_paths = [
                os.path.join(base_dir, 'app', 'static', 'uploads', 'pins', filename),
                os.path.join(base_dir, 'static', 'uploads', 'pins', filename),
                os.path.join(base_dir, 'app', 'static', 'uploads', filename),
                os.path.join(base_dir, 'static', 'uploads', filename),
            ]
            exists = any(os.path.exists(p) for p in possible_paths)

            results.append({
                'pin_id': pin.id,
                'pin_code': pin.pin_code,
                'image_src': img,
                'filename': filename,
                'file_exists': exists,
                'checked_paths': possible_paths
            })

    return jsonify({
        'total_pins_with_images': len(pins_with_images),
        'images': results
    })


@main_bp.route('/uploads/<path:filename>')
def serve_uploads(filename):
    """Serve files from uploads directory (alternative path)"""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    upload_folder = os.path.join(base_dir, 'uploads')
    file_path = os.path.join(upload_folder, filename)

    if os.path.exists(file_path):
        return send_from_directory(upload_folder, filename)

    # Also check in pins subfolder
    pins_path = os.path.join(upload_folder, 'pins', filename)
    if os.path.exists(pins_path):
        return send_from_directory(os.path.join(upload_folder, 'pins'), filename)

    abort(404)


# ==================== DEBUG ENDPOINTS ====================

@main_bp.route('/debug_images')
def debug_images():
    """Debug endpoint to find where images are stored"""
    import os
    base_dir = os.path.dirname(os.path.dirname(__file__))

    debug_info = {
        'base_directory': base_dir,
        'paths_checked': []
    }

    folders_to_check = [
        ('static/uploads', os.path.join(base_dir, 'static', 'uploads')),
        ('static/uploads/pins', os.path.join(base_dir, 'static', 'uploads', 'pins')),
        ('static/uploads/images', os.path.join(base_dir, 'static', 'uploads', 'images')),
        ('uploads', os.path.join(base_dir, 'uploads')),
        ('uploads/pins', os.path.join(base_dir, 'uploads', 'pins')),
        ('images', os.path.join(base_dir, 'images')),
    ]

    for folder_name, folder_path in folders_to_check:
        info = {
            'path': folder_path,
            'exists': os.path.exists(folder_path),
            'files': []
        }

        if os.path.exists(folder_path):
            try:
                files = os.listdir(folder_path)
                info['file_count'] = len(files)
                info['files'] = files[:20]  # Show first 20 files
            except Exception as e:
                info['error'] = str(e)

        debug_info['paths_checked'].append(info)

    # Search for the specific missing image
    target_images = ['pin_2_950fee39.png', '950fee39.png']
    debug_info['searching_for'] = target_images

    for target in target_images:
        debug_info[target] = {'found': False, 'locations': []}
        for folder_name, folder_path in folders_to_check:
            full_path = os.path.join(folder_path, target)
            if os.path.exists(full_path):
                debug_info[target]['found'] = True
                debug_info[target]['locations'].append(full_path)

    return jsonify(debug_info)


# ==================== MAIN ROUTES ====================

@main_bp.route('/')
def index():
    """Home page"""
    # Get home content
    hero_title = HomeContent.query.filter_by(section='hero_title').first()
    hero_text = HomeContent.query.filter_by(section='hero_text').first()
    moving_tagline = HomeContent.query.filter_by(section='moving_tagline').first()
    announcement = HomeContent.query.filter_by(section='announcement').first()
    instructions = HomeContent.query.filter_by(section='instructions').first()
    whatsapp_link = HomeContent.query.filter_by(section='whatsapp_link').first()
    telegram_link = HomeContent.query.filter_by(section='telegram_link').first()
    footer_text = HomeContent.query.filter_by(section='footer_text').first()
    vip_text = HomeContent.query.filter_by(section='vip_text').first()
    vip_number = HomeContent.query.filter_by(section='vip_number').first()
    need_help_text = HomeContent.query.filter_by(section='need_help_text').first()
    hot_updates_text = HomeContent.query.filter_by(section='hot_updates_text').first()
    support_email = HomeContent.query.filter_by(section='support_email').first()

    # Get site settings
    primary_color = SiteSettings.query.filter_by(setting_key='primary_color').first()
    secondary_color = SiteSettings.query.filter_by(setting_key='secondary_color').first()
    site_name = SiteSettings.query.filter_by(setting_key='site_name').first()

    # Get all subjects
    all_subjects = Subject.query.filter_by(show_on_homepage=True).order_by(Subject.display_order, Subject.name).all()

    # Get exam timetables
    waec_timetable_text = SiteSettings.query.filter_by(setting_key='waec_timetable_text').first()
    neco_timetable_text = SiteSettings.query.filter_by(setting_key='neco_timetable_text').first()

    waec_timetable = ExamTimetable.query.filter_by(exam_type='WAEC', year=2026).order_by(ExamTimetable.date).all()
    neco_timetable = ExamTimetable.query.filter_by(exam_type='NECO', year=2026).order_by(ExamTimetable.date).all()

    return render_template('index.html',
                           hero_title=hero_title.content if hero_title else "AnswerPoint",
                           hero_text=hero_text.content if hero_text else "",
                           moving_tagline=moving_tagline.content if moving_tagline else "🔥 100% VERIFIED WAEC & NECO ANSWERS — JOIN OUR FREE WHATSAPP & TELEGRAM CHANNELS! 🔥",
                           announcement=announcement.content if announcement else "",
                           instructions=instructions.content if instructions else "",
                           hot_updates_text=hot_updates_text.content if hot_updates_text else "2026 WAEC MAY/JUNE FINAL EXAMINATION TIMETABLE",
                           whatsapp_link=whatsapp_link.content if whatsapp_link else "#",
                           telegram_link=telegram_link.content if telegram_link else "#",
                           vip_text=vip_text.content if vip_text else "Want early VIP answers before the exam?",
                           vip_number=vip_number.content if vip_number else "08065582389",
                           support_email=support_email.content if support_email else "support@answerpoint.com",
                           footer_text=footer_text.content if footer_text else "Powered By AnswerPoint",
                           need_help_text=need_help_text.content if need_help_text else "Need Help? We're Here for You!",
                           primary_color=primary_color.setting_value if primary_color else "#1e3a8a",
                           secondary_color=secondary_color.setting_value if secondary_color else "#1d4ed8",
                           site_name=site_name.setting_value if site_name else "AnswerPoint",
                           waec_subjects=all_subjects,
                           waec_timetable=waec_timetable,
                           neco_timetable=neco_timetable,
                           waec_timetable_text=waec_timetable_text.setting_value if waec_timetable_text else "",
                           neco_timetable_text=neco_timetable_text.setting_value if neco_timetable_text else "")


@main_bp.route('/get_answer', methods=['POST'])
def get_answer():
    """Get answer for a PIN with proper image path handling"""
    pin_code = request.form.get('pin_code', '').strip()

    print(f"🔍 Looking for PIN: {pin_code}")

    if not pin_code or len(pin_code) != 3 or not pin_code.isdigit():
        return jsonify({'success': False, 'error': 'Invalid PIN'})

    pin = Pin.query.filter_by(pin_code=pin_code).first()

    if not pin:
        print(f"❌ PIN not found: {pin_code}")
        return jsonify({'success': False, 'error': 'PIN not found'})

    print(f"✅ PIN found: {pin_code}")

    pin.views += 1
    db.session.commit()

    # Get answer text
    answer_text = pin.answer_text
    if not answer_text:
        answer_text = '<p>No answer content available for this PIN.</p>'

    # IMPROVED IMAGE PATH FIXING
    if answer_text and '<img' in answer_text:
        import re

        # Function to clean and fix image paths
        def fix_image_path(match):
            src = match.group(1)
            original_src = src

            # Remove quotes if present
            src = src.strip('\'"')

            # Skip external URLs, data URIs, and absolute URLs
            if src.startswith(('http://', 'https://', 'data:', '//')):
                return f'src="{src}"'

            # Clean up the path
            # Remove leading slashes, dots, and common problem patterns
            src = re.sub(r'^\.?/\.?/?', '', src)
            src = re.sub(r'^static/uploads/static/uploads/', 'static/uploads/', src)
            src = re.sub(r'^uploads/uploads/', 'uploads/', src)

            # Check for filename patterns (PIN images are like: pin_123_abc.png)
            filename = src.split('/')[-1]

            # Determine correct path based on file location
            if filename.startswith('pin_') or 'pin_' in filename:
                # PIN images should be in pins folder
                corrected_path = f'/static/uploads/pins/{filename}'
            elif src.startswith('pins/') or '/pins/' in src:
                # Already pointing to pins folder but might need correction
                corrected_path = f'/static/uploads/{src}'
                corrected_path = corrected_path.replace('/static/uploads/pins//', '/static/uploads/pins/')
            elif src.startswith('static/uploads/'):
                # Good path but might need leading slash
                corrected_path = f'/{src}'
            elif src.startswith('uploads/'):
                corrected_path = f'/static/{src}'
            else:
                # Default fallback - try both locations
                corrected_path = f'/static/uploads/{filename}'

            # Remove any double slashes
            corrected_path = re.sub(r'/(?=/)', '', corrected_path)

            print(f"📸 Fixed image path: {original_src} -> {corrected_path}")
            return f'src="{corrected_path}"'

        # Apply the fix to all img src attributes
        answer_text = re.sub(r'src=["\']([^"\' ]+)["\']', fix_image_path, answer_text)

        # Also handle background images and other URLs
        answer_text = re.sub(r'url\(["\']?([^"\'\)]+)["\']?\)',
                            lambda m: f'url("{fix_image_path(m).replace("src=", "").strip()}")',
                            answer_text)

        print(f"✅ Fixed {answer_text.count('<img')} images in PIN {pin_code}")

    return jsonify({
        'success': True,
        'answer_text': answer_text,
        'subject_name': pin.subject_name or 'Unknown',
        'posted_by': getattr(pin, 'posted_by', 'AnswerPoint'),
        'pin_code': pin.pin_code,
        'answer_text_color': getattr(pin, 'answer_text_color', '#1f2937')
    })

@main_bp.route('/subjects')
def subjects():
    """View all subjects"""
    exam_type = request.args.get('exam', 'all')
    search = request.args.get('search', '')

    query = Subject.query
    if exam_type != 'all':
        query = query.filter_by(exam_type=exam_type)
    if search:
        query = query.filter(Subject.name.contains(search))

    subjects_list = query.order_by(Subject.name).all()

    return render_template('subjects.html', subjects=subjects_list, exam_type=exam_type, search=search)


# ==================== API ENDPOINTS ====================

@main_bp.route('/api/home_content')
def api_home_content():
    """API endpoint for home content"""
    sections = ['hero_title', 'hero_text', 'announcement', 'instructions',
                'whatsapp_link', 'telegram_link', 'footer_text', 'moving_tagline',
                'vip_text', 'vip_number', 'need_help_text', 'hot_updates_text', 'support_email']
    content = {}
    for section in sections:
        home_content = HomeContent.query.filter_by(section=section).first()
        content[section] = home_content.content if home_content else ''
    return jsonify(content)


@main_bp.route('/api/timetable')
def api_timetable():
    """API endpoint for timetable text"""
    waec_text = SiteSettings.query.filter_by(setting_key='waec_timetable_text').first()
    neco_text = SiteSettings.query.filter_by(setting_key='neco_timetable_text').first()

    return jsonify({
        'waec': waec_text.setting_value if waec_text else '',
        'neco': neco_text.setting_value if neco_text else ''
    })


@main_bp.route('/api/subjects')
def api_subjects():
    """API endpoint for subjects"""
    subjects = Subject.query.filter_by(show_on_homepage=True).order_by(Subject.display_order, Subject.name).all()
    return jsonify([{
        'id': s.id,
        'name': s.name,
        'exam_type': s.exam_type,
        'has_practical': s.has_practical,
        'icon': s.icon
    } for s in subjects])


@main_bp.route('/get_subjects_api')
def get_subjects_api():
    """API endpoint to get all subjects"""
    subjects = Subject.query.order_by(Subject.name).all()
    return jsonify([{
        'id': s.id,
        'name': s.name,
        'icon': s.icon or 'fa-book',
        'has_practical': s.has_practical or False,
        'exam_type': s.exam_type
    } for s in subjects])


@main_bp.route('/get_timetable_html')
def get_timetable_html():
    """Get timetable HTML for display"""
    waec_entries = ExamTimetable.query.filter_by(exam_type='WAEC', year=2026).order_by(ExamTimetable.date).all()
    neco_entries = ExamTimetable.query.filter_by(exam_type='NECO', year=2026).order_by(ExamTimetable.date).all()

    html = '<div class="bg-gray-900 p-3 border border-gray-700">'
    html += '<div class="flex items-center gap-1.5 mb-3 pb-2 border-b border-gray-700">'
    html += '<i class="fas fa-calendar-alt text-yellow-300"></i>'
    html += '<span class="text-white font-bold uppercase">Exam Timetable 2026</span></div>'

    if waec_entries:
        html += '<div class="mb-3"><div class="flex items-center gap-1 mb-2"><i class="fas fa-graduation-cap text-yellow-300"></i><span class="text-yellow-200 font-semibold uppercase">WAEC</span></div>'
        for entry in waec_entries:
            html += f'<div class="bg-gray-800 p-2 border-l-2 border-yellow-500 mb-1"><div class="font-bold text-yellow-100">{entry.subject}</div>'
            if entry.paper:
                html += f'<div class="text-gray-300 text-xs">{entry.paper}</div>'
            html += f'<div class="text-yellow-300/70 text-xs">{entry.date} | {entry.time}</div></div>'
        html += '</div>'

    if neco_entries:
        html += '<div><div class="flex items-center gap-1 mb-2"><i class="fas fa-school text-yellow-300"></i><span class="text-yellow-200 font-semibold uppercase">NECO</span></div>'
        for entry in neco_entries:
            html += f'<div class="bg-gray-800 p-2 border-l-2 border-yellow-500 mb-1"><div class="font-bold text-yellow-100">{entry.subject}</div>'
            if entry.paper:
                html += f'<div class="text-gray-300 text-xs">{entry.paper}</div>'
            html += f'<div class="text-yellow-300/70 text-xs">{entry.date} | {entry.time}</div></div>'
        html += '</div>'

    if not waec_entries and not neco_entries:
        waec_text = SiteSettings.query.filter_by(setting_key='waec_timetable_text').first()
        neco_text = SiteSettings.query.filter_by(setting_key='neco_timetable_text').first()

        if waec_text and waec_text.setting_value:
            html += '<div class="mb-3"><div class="font-bold text-yellow-100 mb-2">WAEC Timetable</div>'
            html += f'<pre class="text-xs text-gray-300 whitespace-pre-wrap">{waec_text.setting_value}</pre></div>'

        if neco_text and neco_text.setting_value:
            html += '<div><div class="font-bold text-yellow-100 mb-2">NECO Timetable</div>'
            html += f'<pre class="text-xs text-gray-300 whitespace-pre-wrap">{neco_text.setting_value}</pre></div>'

        if not waec_text and not neco_text:
            html += '<p class="text-gray-400 text-center py-4">No timetable entries added yet. Admin can add them.</p>'

    html += '</div>'
    return html


@main_bp.route('/api/stats')
def api_stats():
    """API endpoint for statistics"""
    total_subjects = Subject.query.count()
    total_pins = Pin.query.count()
    from sqlalchemy import func
    total_views = db.session.query(func.sum(Pin.views)).scalar() or 0
    total_images = Image.query.count()

    return jsonify({
        'total_subjects': total_subjects,
        'total_pins': total_pins,
        'total_views': total_views,
        'total_images': total_images
    })