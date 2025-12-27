# Quick Start Guide - GearGuard+

## Prerequisites

- Python 3.7 or higher
- No external dependencies required (uses only Python standard library)

## Installation Steps

### 1. Verify Python Installation

Open a terminal/command prompt and check Python version:

```bash
python --version
```

If Python is not installed:
- **Windows**: Download from [python.org](https://www.python.org/downloads/) or use Microsoft Store
- **Mac/Linux**: Usually pre-installed, or use `brew install python3` (Mac)

### 2. Navigate to Project Directory

```bash
cd path/to/oddo-2025
```

Or if you're already in the project directory:
```bash
cd C:\Users\ranpa\OneDrive\Desktop\oddo-2025
```

### 3. Run the Application

You have two options:

#### Option A: Basic Demo (Recommended for first run)
```bash
python app.py
```

This will:
- Initialize the system
- Create demo data (employees, teams, equipment, requests)
- Display dashboard KPIs
- Show predictive alerts
- Display technician workloads

#### Option B: Full Workflow Demo
```bash
python demo.py
```

This demonstrates:
- Complete maintenance workflow
- Health score updates
- Overdue detection
- Request completion
- All dashboard features

## Expected Output

You should see output like:

```
============================================================
GearGuard+ Maintenance Management System
============================================================

📦 Setting up demo data...
✅ Demo data created

🔧 Equipment: Production Line Conveyor Belt
   Initial Health Score: 100/100

📝 Creating corrective maintenance request...
✅ Request created (ID: 1)
   State: new
   Overdue: True

📊 Updated Health Score: 90/100

============================================================
DASHBOARD KPIs
============================================================
Total Equipment: 2
Open Requests: 2
Overdue Requests: 1
Critical Health Equipment: 0
...
```

## Troubleshooting

### Python Not Found

**Windows:**
1. Install Python from [python.org](https://www.python.org/downloads/)
2. During installation, check "Add Python to PATH"
3. Restart your terminal after installation

**Alternative (Windows):**
```bash
py app.py
```

### Module Import Errors

If you see `ModuleNotFoundError`:
1. Make sure you're in the project root directory
2. Check that all files are present:
   - `models/` folder with all Python files
   - `app.py` in root directory

### Permission Errors

If you get permission errors:
- Make sure you have read/write access to the project folder
- Try running as administrator (Windows) or with sudo (Linux/Mac)

## Next Steps

After running the demo:

1. **Explore the Code:**
   - Check `models/` folder for business logic
   - Review `views/` folder for XML view definitions
   - Examine `app.py` for application setup

2. **Customize:**
   - Modify demo data in `app.py`
   - Adjust health score algorithm in `models/equipment.py`
   - Add new features following the existing patterns

3. **Integration:**
   - The system can be integrated into Odoo framework
   - Can be adapted to use database backend
   - XML views can be rendered in web framework

## Project Structure

```
oddo-2025/
├── models/              # Business logic and data models
│   ├── base.py          # Base ORM class
│   ├── equipment.py     # Equipment/Asset management
│   ├── maintenance_request.py  # Core workflow
│   ├── maintenance_team.py      # Team management
│   ├── employee.py      # Employee/Technician model
│   └── dashboard.py     # Analytics and KPIs
├── views/               # XML view definitions
├── app.py              # Main application entry
├── demo.py             # Full workflow demonstration
├── README.md           # Complete documentation
├── ARCHITECTURE.md     # Technical architecture
└── manifest.json       # Module configuration
```

## Support

For questions or issues:
1. Check `README.md` for detailed documentation
2. Review `ARCHITECTURE.md` for technical details
3. Examine the code comments for implementation details

