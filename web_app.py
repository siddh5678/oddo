"""
GearGuard+ Web Application
Flask-based web interface for the maintenance management system
"""
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from app import GearGuardApp
from datetime import datetime, timedelta
from models.user import User
import json

app = Flask(__name__)
app.secret_key = 'gearguard-secret-key-2025-change-in-production'

# Initialize the application
gear_app = GearGuardApp()

# Initialize demo data on startup
def initialize_demo_data():
    """Initialize demo data for the application"""
    try:
        # Check if data already exists
        request_model = gear_app.env['maintenance.request']
        existing_requests = request_model.search([])
        
        if not existing_requests:
            print("=" * 70)
            print("Initializing Demo Data...")
            print("=" * 70)
            
            # Setup demo data
            demo_data = gear_app.setup_demo_data()
            
            # Create default admin user if not exists
            existing_user = User.get_by_username('admin')
            if not existing_user:
                User.create('admin', 'admin@gearguard.com', 'admin123', 'Administrator', 'admin')
                print("✓ Default admin user created: username='admin', password='admin123'")
            
            print("✓ Demo data created successfully!")
            print("  - Employees: Created")
            print("  - Teams: Created")
            print("  - Equipment: Created")
            print("  - Maintenance Requests: Created")
            print("=" * 70)
        else:
            print("Demo data already exists. Skipping initialization.")
    except Exception as e:
        print(f"Error initializing demo data: {e}")

# Initialize on startup
initialize_demo_data()


def login_required(f):
    """Decorator to require login"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def index():
    """Dashboard home page"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    dashboard_data = gear_app.get_dashboard_data()
    return render_template('dashboard.html', **dashboard_data)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Please enter both username and password', 'error')
            return render_template('login.html')
        
        user = User.get_by_username(username)
        
        if user and User.verify_password(user, password):
            if not user.get('is_active', 1):
                flash('Your account is inactive. Please contact administrator.', 'error')
                return render_template('login.html')
            
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['full_name'] = user.get('full_name', user['username'])
            session['role'] = user.get('role', 'user')
            
            User.update_last_login(user['id'])
            flash(f'Welcome back, {session["full_name"]}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
    
    # If already logged in, redirect to dashboard
    if 'user_id' in session:
        return redirect(url_for('index'))
    
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """User registration page"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        full_name = request.form.get('full_name')
        
        # Validation
        if not username or not email or not password:
            flash('Please fill in all required fields', 'error')
            return render_template('signup.html')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('signup.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long', 'error')
            return render_template('signup.html')
        
        # Check if username or email already exists
        if User.get_by_username(username):
            flash('Username already exists. Please choose another.', 'error')
            return render_template('signup.html')
        
        if User.get_by_email(email):
            flash('Email already registered. Please use another email.', 'error')
            return render_template('signup.html')
        
        # Create user
        user = User.create(username, email, password, full_name, 'user')
        
        if user:
            flash('Account created successfully! Please login.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Error creating account. Please try again.', 'error')
    
    # If already logged in, redirect to dashboard
    if 'user_id' in session:
        return redirect(url_for('index'))
    
    return render_template('signup.html')


@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out successfully', 'info')
    return redirect(url_for('login'))


@app.route('/equipment')
@login_required
def equipment_list():
    """List all equipment"""
    equipment_model = gear_app.env['equipment']
    equipments = equipment_model.search([])
    
    # Add computed fields
    for equip in equipments:
        equip['maintenance_requests_count'] = equipment_model._get_maintenance_requests_count(equip['id'])
        equip['open_requests_count'] = equipment_model._get_open_requests_count(equip['id'])
        equip['health_status'] = equipment_model.get_health_status(equip['id'])
    
    return render_template('equipment_list.html', equipments=equipments)


@app.route('/equipment/<int:equipment_id>')
@login_required
def equipment_detail(equipment_id):
    """Equipment detail page"""
    equipment_model = gear_app.env['equipment']
    equipment = equipment_model.browse([equipment_id])
    
    if not equipment:
        flash('Equipment not found', 'error')
        return redirect(url_for('equipment_list'))
    
    equip = equipment[0]
    equip['maintenance_requests_count'] = equipment_model._get_maintenance_requests_count(equipment_id)
    equip['open_requests_count'] = equipment_model._get_open_requests_count(equipment_id)
    equip['health_status'] = equipment_model.get_health_status(equipment_id)
    
    # Get assigned employee details
    if equip.get('assigned_employee_id'):
        employee_model = gear_app.env['employee']
        assigned_employee = employee_model.browse([equip['assigned_employee_id']])
        equip['assigned_employee'] = assigned_employee[0] if assigned_employee else None
    else:
        equip['assigned_employee'] = None
    
    # Get maintenance requests
    request_model = gear_app.env['maintenance.request']
    requests = request_model.search([('equipment_id', '=', equipment_id)])
    
    return render_template('equipment_detail.html', equipment=equip, requests=requests)


@app.route('/equipment/create', methods=['GET', 'POST'])
@login_required
def equipment_create():
    """Create new equipment"""
    if request.method == 'POST':
        equipment_model = gear_app.env['equipment']
        
        # Get teams and employees for dropdowns
        team_model = gear_app.env['maintenance.team']
        employee_model = gear_app.env['employee']
        
        vals = {
            'name': request.form.get('name'),
            'serial_number': request.form.get('serial_number'),
            'department': request.form.get('department'),
            'location': request.form.get('location'),
            'purchase_date': request.form.get('purchase_date') or False,
            'warranty_end_date': request.form.get('warranty_end_date') or False,
        }
        
        if request.form.get('maintenance_team_id'):
            vals['maintenance_team_id'] = int(request.form.get('maintenance_team_id'))
        if request.form.get('assigned_employee_id'):
            vals['assigned_employee_id'] = int(request.form.get('assigned_employee_id'))
        
        equipment_model.create(vals)
        flash('Equipment created successfully!', 'success')
        return redirect(url_for('equipment_list'))
    
    # GET request - show form
    team_model = gear_app.env['maintenance.team']
    employee_model = gear_app.env['employee']
    teams = team_model.search([])
    employees = employee_model.search([])
    
    return render_template('equipment_form.html', equipment=None, teams=teams, employees=employees)


@app.route('/requests')
@login_required
def requests_list():
    """List all maintenance requests"""
    view_type = request.args.get('view', 'list')  # 'list' or 'kanban'
    
    request_model = gear_app.env['maintenance.request']
    requests = request_model.search([])
    
    # Add equipment names and technician names
    equipment_model = gear_app.env['equipment']
    employee_model = gear_app.env['employee']
    
    for req in requests:
        if req.get('equipment_id'):
            equip = equipment_model.browse([req['equipment_id']])
            req['equipment_name'] = equip[0]['name'] if equip else 'Unknown'
        else:
            req['equipment_name'] = 'N/A'
        
        if req.get('technician_id'):
            tech = employee_model.browse([req['technician_id']])
            req['technician_name'] = tech[0]['name'] if tech else 'Unknown'
        else:
            req['technician_name'] = 'Unassigned'
    
    # Filter by state if provided
    state_filter = request.args.get('state')
    if state_filter:
        requests = [r for r in requests if r.get('state') == state_filter]
    
    # Group by state for Kanban
    if view_type == 'kanban':
        kanban_data = {
            'new': [],
            'in_progress': [],
            'repaired': [],
            'scrap': []
        }
        for req in requests:
            state = req.get('state', 'new')
            if state in kanban_data:
                kanban_data[state].append(req)
        return render_template('requests_kanban.html', kanban_data=kanban_data, current_state=state_filter, view_type=view_type)
    
    return render_template('requests_list.html', requests=requests, current_state=state_filter, view_type=view_type)


@app.route('/requests/<int:request_id>')
@login_required
def request_detail(request_id):
    """Maintenance request detail page"""
    request_model = gear_app.env['maintenance.request']
    req = request_model.browse([request_id])
    
    if not req:
        flash('Request not found', 'error')
        return redirect(url_for('requests_list'))
    
    req_data = req[0]
    
    # Get equipment info
    if req_data.get('equipment_id'):
        equipment_model = gear_app.env['equipment']
        equipment = equipment_model.browse([req_data['equipment_id']])
        req_data['equipment'] = equipment[0] if equipment else None
    
    # Get team technicians for dropdown
    if req_data.get('maintenance_team_id'):
        team_technicians = request_model.get_team_technicians(req_data['maintenance_team_id'])
        req_data['team_technicians'] = team_technicians
    else:
        req_data['team_technicians'] = []
    
    return render_template('request_detail.html', request=req_data)


@app.route('/requests/create', methods=['GET', 'POST'])
@login_required
def request_create():
    """Create new maintenance request"""
    if request.method == 'POST':
        request_model = gear_app.env['maintenance.request']
        
        vals = {
            'subject': request.form.get('subject'),
            'equipment_id': int(request.form.get('equipment_id')) if request.form.get('equipment_id') else False,
            'request_type': request.form.get('request_type', 'corrective'),
            'scheduled_date': request.form.get('scheduled_date') or False,
            'description': request.form.get('description', ''),
        }
        
        if request.form.get('technician_id'):
            vals['technician_id'] = int(request.form.get('technician_id'))
        
        request_model.create(vals)
        flash('Maintenance request created successfully!', 'success')
        return redirect(url_for('requests_list'))
    
    # GET request - show form
    equipment_model = gear_app.env['equipment']
    employee_model = gear_app.env['employee']
    equipments = equipment_model.search([('is_scrapped', '=', False)])
    technicians = employee_model.get_technicians()
    
    return render_template('request_form.html', request=None, equipments=equipments, technicians=technicians)


@app.route('/requests/<int:request_id>/action', methods=['POST'])
@login_required
def request_action(request_id):
    """Perform action on maintenance request"""
    action = request.form.get('action')
    request_model = gear_app.env['maintenance.request']
    
    try:
        if action == 'start':
            request_model.action_start(request_id)
            flash('Maintenance started!', 'success')
        elif action == 'repair':
            duration = float(request.form.get('duration', 0))
            if duration <= 0:
                flash('Duration must be greater than 0', 'error')
                return redirect(url_for('request_detail', request_id=request_id))
            request_model.action_repair(request_id, duration=duration)
            flash('Maintenance completed!', 'success')
        elif action == 'scrap':
            request_model.action_scrap(request_id)
            flash('Equipment marked as scrapped!', 'warning')
        else:
            flash('Invalid action', 'error')
    except ValueError as e:
        flash(str(e), 'error')
    
    return redirect(url_for('request_detail', request_id=request_id))


@app.route('/teams')
@login_required
def teams_list():
    """List all maintenance teams"""
    team_model = gear_app.env['maintenance.team']
    teams = team_model.search([])
    
    # Add technician names
    employee_model = gear_app.env['employee']
    for team in teams:
        technician_ids = team.get('technician_ids', [])
        technicians = employee_model.browse(technician_ids) if technician_ids else []
        team['technicians'] = [{'id': t['id'], 'name': t['name']} for t in technicians]
    
    return render_template('teams_list.html', teams=teams)


@app.route('/teams/create', methods=['GET', 'POST'])
@login_required
def team_create():
    """Create new maintenance team"""
    if request.method == 'POST':
        team_model = gear_app.env['maintenance.team']
        employee_model = gear_app.env['employee']
        
        # Get team name (either from select or custom input)
        team_name = request.form.get('name', '').strip()
        if not team_name:
            team_name = request.form.get('custom_name', '').strip()
        
        vals = {
            'name': team_name,
            'description': request.form.get('description', ''),
            'active': True,
        }
        
        # Get selected technician IDs
        technician_ids = []
        for key, value in request.form.items():
            if key.startswith('technician_') and value == 'on':
                tech_id = int(key.replace('technician_', ''))
                technician_ids.append(tech_id)
        
        vals['technician_ids'] = technician_ids
        
        team_model.create(vals)
        flash('Team created successfully!', 'success')
        return redirect(url_for('teams_list'))
    
    # GET request - show form
    employee_model = gear_app.env['employee']
    technicians = employee_model.get_technicians()
    
    return render_template('team_form.html', team=None, technicians=technicians)


@app.route('/teams/<int:team_id>/edit', methods=['GET', 'POST'])
@login_required
def team_edit(team_id):
    """Edit maintenance team"""
    team_model = gear_app.env['maintenance.team']
    team = team_model.browse([team_id])
    
    if not team:
        flash('Team not found', 'error')
        return redirect(url_for('teams_list'))
    
    team_data = team[0]
    
    if request.method == 'POST':
        # Get team name (either from select or custom input)
        team_name = request.form.get('name', '').strip()
        if not team_name or team_name == 'CUSTOM':
            team_name = request.form.get('custom_name', '').strip()
        
        vals = {
            'name': team_name,
            'description': request.form.get('description', ''),
        }
        
        # Get selected technician IDs
        technician_ids = []
        for key, value in request.form.items():
            if key.startswith('technician_') and value == 'on':
                tech_id = int(key.replace('technician_', ''))
                technician_ids.append(tech_id)
        
        vals['technician_ids'] = technician_ids
        
        team_model.write([team_id], vals)
        flash('Team updated successfully!', 'success')
        return redirect(url_for('teams_list'))
    
    # GET request - show form
    employee_model = gear_app.env['employee']
    all_technicians = employee_model.get_technicians()
    
    # Get current team technicians
    current_technician_ids = team_data.get('technician_ids', [])
    
    return render_template('team_form.html', 
                         team=team_data, 
                         technicians=all_technicians,
                         current_technician_ids=current_technician_ids)


@app.route('/team-assignment-guide')
@login_required
def team_assignment_guide():
    """Team assignment guide page"""
    return render_template('team_assignment_info.html')


@app.route('/calendar')
@login_required
def calendar_view():
    """Calendar view showing equipment maintenance status by date"""
    from datetime import datetime, timedelta
    from calendar import monthrange
    
    # Get month and year from query params or use current
    year = int(request.args.get('year', datetime.now().year))
    month = int(request.args.get('month', datetime.now().month))
    
    # Get all maintenance requests
    request_model = gear_app.env['maintenance.request']
    equipment_model = gear_app.env['equipment']
    
    all_requests = request_model.search([])
    
    # Build calendar data structure
    # Format: {date: {equipment_id: {'status': 'red'/'green', 'equipment_name': '...', 'request_id': ...}}}
    calendar_data = {}
    
    for req in all_requests:
        equipment_id = req.get('equipment_id')
        if not equipment_id:
            continue
        
        equipment = equipment_model.browse([equipment_id])
        if not equipment:
            continue
        
        equip_name = equipment[0].get('name', 'Unknown')
        state = req.get('state', 'new')
        scheduled_date = req.get('scheduled_date')
        repaired_date = req.get('repaired_date')
        
        # Red status: Active/pending requests (new, in_progress) on scheduled date
        if scheduled_date and state in ['new', 'in_progress']:
            if scheduled_date not in calendar_data:
                calendar_data[scheduled_date] = {}
            calendar_data[scheduled_date][equipment_id] = {
                'status': 'red',
                'equipment_name': equip_name,
                'request_id': req.get('id'),
                'subject': req.get('subject', ''),
                'state': state
            }
        
        # Green status: Repaired requests on repair date
        if repaired_date and state == 'repaired':
            if repaired_date not in calendar_data:
                calendar_data[repaired_date] = {}
            # Only show green if not already red (repair takes priority)
            if equipment_id not in calendar_data[repaired_date] or calendar_data[repaired_date][equipment_id]['status'] != 'red':
                calendar_data[repaired_date][equipment_id] = {
                    'status': 'green',
                    'equipment_name': equip_name,
                    'request_id': req.get('id'),
                    'subject': req.get('subject', ''),
                    'state': 'repaired'
                }
    
    # Get all equipment for the month view
    all_equipment = equipment_model.search([('is_scrapped', '=', False)])
    
    # Calculate calendar grid
    # monthrange returns (weekday of first day, number of days)
    # weekday: 0=Monday, 6=Sunday
    # We need to convert to Sunday=0 format for our calendar
    first_weekday, days_in_month = monthrange(year, month)
    # Convert Monday=0 to Sunday=0 format
    first_day = (first_weekday + 1) % 7  # Sunday=0, Monday=1, ..., Saturday=6
    today = datetime.now().date()
    
    # Previous and next month
    if month == 1:
        prev_month, prev_year = 12, year - 1
    else:
        prev_month, prev_year = month - 1, year
    
    if month == 12:
        next_month, next_year = 1, year + 1
    else:
        next_month, next_year = month + 1, year
    
    return render_template('calendar.html', 
                         calendar_data=calendar_data,
                         year=year,
                         month=month,
                         days_in_month=days_in_month,
                         first_day=first_day,
                         today=today,
                         prev_month=prev_month,
                         prev_year=prev_year,
                         next_month=next_month,
                         next_year=next_year,
                         all_equipment=all_equipment)


@app.route('/api/dashboard/kpis')
def api_kpis():
    """API endpoint for dashboard KPIs"""
    dashboard_data = gear_app.get_dashboard_data()
    return jsonify(dashboard_data['kpis'])


@app.route('/api/dashboard/alerts')
def api_alerts():
    """API endpoint for predictive alerts"""
    dashboard_data = gear_app.get_dashboard_data()
    return jsonify(dashboard_data['alerts'])


@app.route('/api/equipment/<int:equipment_id>/health')
def api_equipment_health(equipment_id):
    """API endpoint for equipment health score"""
    equipment_model = gear_app.env['equipment']
    equipment_model._compute_health_score(equipment_id)
    equipment = equipment_model.browse([equipment_id])
    
    if equipment:
        return jsonify({
            'health_score': equipment[0].get('health_score', 100),
            'status': equipment_model.get_health_status(equipment_id)
        })
    return jsonify({'error': 'Equipment not found'}), 404


if __name__ == '__main__':
    print("=" * 70)
    print("GearGuard+ Web Application")
    print("=" * 70)
    print("\nStarting web server...")
    print("Open your browser and navigate to: http://127.0.0.1:5000")
    print("\nPress Ctrl+C to stop the server\n")
    app.run(debug=True, host='0.0.0.0', port=5000)

