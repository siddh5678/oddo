# GearGuard+ Web Interface Guide

## 🎨 Beautiful Web UI Now Available!

Your GearGuard+ system now includes a **modern, interactive web interface** perfect for hackathon demonstrations!

## Quick Start

### 1. Install Flask
```bash
pip install Flask
```

### 2. Start the Web Server
```bash
python web_app.py
```

### 3. Open in Browser
Navigate to: **http://127.0.0.1:5000**

## Features

### 📊 Dashboard
- Real-time KPIs (Total Equipment, Open Requests, Overdue, Critical)
- Predictive Maintenance Alerts with severity indicators
- Preventive vs Corrective maintenance charts
- Requests per team statistics
- Technician workload balancing visualization

### 🔧 Equipment Management
- **List View**: See all equipment with health scores
- **Detail View**: Complete equipment information
  - Health score with visual progress bar
  - Maintenance history
  - Quick stats
- **Create/Edit**: Add new equipment with all details

### 🛠️ Maintenance Requests
- **Kanban-style List**: Filter by state (New, In Progress, Repaired)
- **Detail View**: Complete request information
  - Action buttons (Start, Complete, Scrap)
  - Overdue warnings
  - Duration tracking
- **Create Request**: Easy form with auto-assignment

### 👥 Teams
- View all maintenance teams
- See assigned technicians
- Team descriptions

## UI Highlights

### Modern Design
- Bootstrap 5 styling
- Responsive design (works on mobile/tablet)
- Clean, professional interface
- Color-coded status indicators

### Interactive Features
- Health score progress bars
- State-based action buttons
- Overdue warnings
- Flash messages for actions
- Form validation

### Visual Indicators
- **Health Scores**: Color-coded (Green ≥70, Yellow 40-69, Red <40)
- **Request States**: Badge colors (New=Blue, In Progress=Yellow, Repaired=Green, Scrap=Red)
- **Overdue**: Red highlighting and badges
- **Workload**: Status badges (Low/Medium/High)

## Navigation

The web interface includes:
- **Top Navigation Bar**: Quick access to all sections
- **Dashboard**: Home page with overview
- **Equipment**: Asset management
- **Maintenance Requests**: Workflow management
- **Teams**: Team organization

## Workflow Example

1. **View Dashboard** → See overall system status
2. **Check Equipment** → Review health scores
3. **Create Request** → Add new maintenance request
4. **Start Maintenance** → Change state to "In Progress"
5. **Complete Repair** → Enter duration and mark as repaired
6. **View Updated Health** → See health score recalculation

## API Endpoints

The web app also exposes REST API endpoints:

- `GET /api/dashboard/kpis` - Get KPIs as JSON
- `GET /api/dashboard/alerts` - Get predictive alerts
- `GET /api/equipment/<id>/health` - Get equipment health score

## Technical Details

- **Framework**: Flask (lightweight, fast)
- **Templates**: Jinja2 (server-side rendering)
- **Styling**: Bootstrap 5 + Custom CSS
- **Icons**: Bootstrap Icons
- **Backend**: Your existing models (no changes needed!)

## Troubleshooting

**Port already in use?**
- Change port in `web_app.py`: `app.run(port=5001)`

**Flask not found?**
- Install: `pip install Flask`
- Or: `python -m pip install Flask`

**Browser shows errors?**
- Check terminal for error messages
- Make sure all templates are in `templates/` folder
- Verify static files are in `static/` folder

## Demo Tips for Hackathon

1. **Start with Dashboard**: Shows all key features at once
2. **Create Equipment**: Demonstrate form handling
3. **Create Request**: Show auto-assignment feature
4. **Complete Workflow**: Start → Complete → Show health update
5. **Highlight Alerts**: Show predictive maintenance in action

## Next Steps

- The web UI uses your existing models - no code changes needed!
- All business logic remains in the models
- Web interface is just a presentation layer
- Easy to extend with more features

Enjoy your beautiful web interface! 🚀

