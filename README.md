# GearGuard+ Maintenance Management System

Enterprise-grade predictive and proactive asset management system for hackathon demonstration.

## Overview

GearGuard+ transforms reactive maintenance into predictive and proactive asset management through intelligent health scoring, automated workflows, and workload balancing.

## Key Features

### Core Modules

1. **Equipment / Asset Management**
   - Comprehensive asset tracking with serial numbers, departments, locations
   - Health score computation (0-100) based on breakdowns and overdue requests
   - Smart buttons for quick access to maintenance history
   - Scrap/unscrap functionality

2. **Maintenance Team**
   - Team-based organization
   - Many-to-many relationship with technicians
   - Automatic team assignment from equipment

3. **Maintenance Request** (Core Workflow)
   - Request types: Preventive and Corrective
   - State workflow: New → In Progress → Repaired → Scrap
   - Auto-assignment of maintenance teams from equipment
   - Technician validation (must be team member)
   - Mandatory duration before closing
   - Overdue detection and visual indicators
   - Calendar view for preventive maintenance

### Innovation Layer

1. **Equipment Health Score**
   - Rule-based calculation:
     - Base: 100 points
     - Penalty: -15 per breakdown in last 30 days
     - Penalty: -10 per overdue request
   - Visual progress bar display
   - Status categories: Good (≥70), Warning (40-69), Critical (<40)

2. **Predictive Maintenance Alerts**
   - Triggers:
     - 3+ corrective breakdowns in last 30 days
     - Health score < 40
   - Displayed in dashboard with severity levels

3. **Technician Workload Balancing**
   - Real-time workload calculation (open tasks per technician)
   - Visual workload indicators
   - Helps distribute work evenly

4. **Management Dashboard**
   - KPIs: Total equipment, open requests, overdue requests, critical equipment
   - Charts: Preventive vs Corrective ratio, requests per team
   - Technician workload distribution
   - Predictive alerts summary

## Architecture

### Technology Stack
- **Backend**: Python with Odoo-style ORM patterns
- **Frontend**: XML views (Kanban, Form, Calendar, Tree)
- **Logic**: Rule-based intelligence (no heavy ML)

### Project Structure

```
oddo-2025/
├── models/
│   ├── __init__.py
│   ├── base.py              # Base ORM model class
│   ├── employee.py          # Employee/Technician model
│   ├── maintenance_team.py  # Maintenance team model
│   ├── equipment.py         # Equipment/Asset model
│   ├── maintenance_request.py  # Core workflow model
│   └── dashboard.py         # Dashboard analytics
├── views/
│   ├── employee_views.xml
│   ├── maintenance_team_views.xml
│   ├── equipment_views.xml
│   ├── maintenance_request_views.xml
│   └── dashboard_views.xml
├── app.py                   # Main application entry point
├── manifest.json           # Module manifest
└── README.md
```

## Quick Start

### Prerequisites
- Python 3.7 or higher
- No external dependencies required

### Running the Application

**Option 1: Web Interface (Recommended for Hackathon Demo)**
```bash
pip install Flask
python web_app.py
```
Then open your browser to: **http://127.0.0.1:5000**

**Option 2: Command Line - Basic Demo**
```bash
python app.py
```

**Option 3: Command Line - Full Workflow Demo**
```bash
python demo.py
```

**Note**: If `python` doesn't work, try `py` (Windows) or `python3` (Mac/Linux)

### What You'll See

The application will:
1. Initialize the system
2. Create demo data (employees, teams, equipment, requests)
3. Display dashboard KPIs and alerts
4. Show technician workloads
5. Demonstrate complete maintenance workflows

See `QUICKSTART.md` for detailed setup instructions and troubleshooting.

### Key Workflows

#### Creating Equipment
```python
equipment = env['equipment'].create({
    'name': 'Production Line Conveyor Belt',
    'serial_number': 'CONV-001',
    'department': 'Production',
    'maintenance_team_id': team_id,
    'location': 'Factory Floor A',
})
```

#### Creating Maintenance Request
```python
request = env['maintenance.request'].create({
    'subject': 'Routine inspection',
    'equipment_id': equipment_id,
    'request_type': 'preventive',
    'scheduled_date': '2025-01-20',
})
# Team is auto-assigned from equipment
```

#### Workflow Actions
```python
# Start maintenance
request.action_start(request_id)

# Complete repair (duration required)
request.action_repair(request_id, duration=2.5)

# Scrap equipment
request.action_scrap(request_id)
```

## Business Logic Highlights

### Auto-Assignment
- Maintenance team is automatically assigned from equipment when creating a request
- Ensures proper team responsibility

### Validation Rules
- Technicians must be members of the assigned maintenance team
- Duration is mandatory before closing a request
- Prevents incomplete data entry

### Health Score Calculation
- Real-time computation based on:
  - Recent breakdown frequency
  - Overdue maintenance count
- Automatically updates when requests are completed

### Overdue Detection
- Automatic detection when scheduled date passes
- Visual indicators in Kanban and list views
- Prevents missed maintenance windows

## UI/UX Features

### Kanban View
- Grouped by state (New, In Progress, Repaired, Scrap)
- Color-coded request types
- Overdue badges
- Quick create functionality

### Calendar View
- Preventive maintenance schedule
- Color-coded by equipment
- Easy scheduling visualization

### Form Views
- State-based action buttons
- Smart buttons for related records
- Health score progress bars
- Contextual help messages

### Dashboard
- Real-time KPIs
- Visual charts and graphs
- Alert summaries
- Workload distribution

## Innovation Points for Judging

1. **Predictive Intelligence**: Rule-based health scoring that predicts equipment failure risk
2. **Workflow Automation**: Auto-assignment, validation, and state management
3. **Workload Balancing**: Helps optimize technician assignment
4. **Visual Analytics**: Comprehensive dashboard with actionable insights
5. **Enterprise-Ready**: Production-quality code with proper error handling

## Future Enhancements

- Integration with IoT sensors for real-time health monitoring
- Machine learning for predictive failure analysis
- Mobile app for field technicians
- Integration with inventory management
- Advanced reporting and analytics

## License

LGPL-3

## Author

GearGuard+ Team - Hackathon 2025

