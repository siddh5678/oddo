# GearGuard+ Architecture Documentation

## System Overview

GearGuard+ is a comprehensive maintenance management system built with Python following Odoo-style ORM patterns. The system implements rule-based intelligence for predictive maintenance without requiring heavy ML infrastructure.

## Architecture Patterns

### ORM Layer (models/base.py)

The base model class implements a lightweight ORM with:
- **CRUD Operations**: Create, Read, Update, Delete
- **Domain-based Search**: Filter records using domain expressions
- **Relationship Handling**: Support for many2one, one2many, many2many
- **Computed Fields**: Dynamic field computation
- **Environment Context**: Models can access other models through environment

### Model Structure

Each model follows this pattern:
```python
class ModelName(BaseModel):
    def __init__(self, env=None):
        super().__init__(env)
        self._name = 'model.name'
    
    def create(self, vals):
        # Validation and defaults
        # Auto-computation
        return super().create(vals)
```

## Core Models

### 1. Equipment (models/equipment.py)

**Purpose**: Track assets with health scoring

**Key Features**:
- Health score computation (0-100)
- Breakdown tracking
- Overdue request detection
- Scrap/unscrap workflow

**Health Score Algorithm**:
```python
health_score = 100
health_score -= (breakdown_count * 15)  # Last 30 days
health_score -= (overdue_count * 10)
health_score = max(0, min(100, health_score))
```

**Computed Fields**:
- `health_score`: Real-time calculation
- `maintenance_requests_count`: Total requests
- `open_requests_count`: Open requests
- `maintenance_requests_ids`: One2many relationship

### 2. Maintenance Request (models/maintenance_request.py)

**Purpose**: Core workflow engine for maintenance operations

**State Machine**:
```
New → In Progress → Repaired
                  → Scrap
```

**Business Rules**:
1. **Auto-Assignment**: Team assigned from equipment
2. **Technician Validation**: Must be team member
3. **Duration Mandatory**: Required before closing
4. **Overdue Detection**: Automatic based on scheduled_date
5. **Equipment Scrap**: Cascades to equipment model

**Workflow Methods**:
- `action_start()`: New → In Progress
- `action_repair(duration)`: Complete with duration
- `action_scrap()`: Scrap equipment

### 3. Maintenance Team (models/maintenance_team.py)

**Purpose**: Organize technicians into teams

**Relationships**:
- Many2many with Employee (technicians)
- One2many with Equipment
- One2many with Maintenance Request

### 4. Employee (models/employee.py)

**Purpose**: Track employees and technicians

**Fields**:
- Basic info (name, email, phone)
- Department
- `is_technician`: Boolean flag
- Active status

### 5. Dashboard (models/dashboard.py)

**Purpose**: Analytics and KPIs

**Methods**:
- `get_kpis()`: Key performance indicators
- `get_preventive_vs_corrective()`: Maintenance type distribution
- `get_requests_per_team()`: Team workload
- `get_technician_workloads()`: Individual workloads
- `get_predictive_alerts()`: Alert generation

## Innovation Features

### 1. Predictive Maintenance Alerts

**Trigger Conditions**:
- 3+ corrective breakdowns in last 30 days
- Health score < 40

**Implementation**:
```python
def get_predictive_alerts(self):
    # Scan all equipment
    # Check breakdown frequency
    # Check health scores
    # Generate alerts with severity levels
```

### 2. Technician Workload Balancing

**Purpose**: Optimize work distribution

**Calculation**:
```python
workload = count(open_requests where technician_id = X)
```

**Usage**: Display in dashboard to help managers assign work evenly

### 3. Equipment Health Score

**Real-time Computation**:
- Updates when requests are completed
- Considers recent breakdowns (30-day window)
- Factors in overdue maintenance

**Status Categories**:
- Good: ≥70
- Warning: 40-69
- Critical: <40

## View Layer (XML)

### View Types

1. **Tree/List View**: Tabular data display
2. **Form View**: Detailed record editing
3. **Kanban View**: Card-based workflow visualization
4. **Calendar View**: Time-based scheduling
5. **Search View**: Filtering and grouping

### Key View Features

**Kanban**:
- Grouped by state
- Color-coded request types
- Overdue badges
- Quick create

**Form**:
- State-based action buttons
- Smart buttons for related records
- Computed field display
- Validation messages

**Calendar**:
- Preventive maintenance only
- Color-coded by equipment
- Click to view details

## Business Logic Highlights

### Auto-Assignment Logic

```python
# In MaintenanceRequest.create()
if equipment_id and not maintenance_team_id:
    equipment = equipment_model.browse([equipment_id])
    team_id = equipment[0].get('maintenance_team_id')
    if team_id:
        defaults['maintenance_team_id'] = team_id
```

### Validation Rules

**Technician Assignment**:
```python
def validate_technician_assignment(self, request_id, technician_id, team_id):
    team_technicians = self.get_team_technicians(team_id)
    if technician_id not in [t['id'] for t in team_technicians]:
        raise ValueError("Technician must be team member")
```

**Duration Requirement**:
```python
def action_repair(self, request_id, duration=None):
    if not duration or duration <= 0:
        raise ValueError("Duration is mandatory")
```

### Overdue Detection

```python
def _check_overdue(self, request_id):
    today = datetime.now().strftime('%Y-%m-%d')
    is_overdue = (
        scheduled_date < today and 
        state in ['new', 'in_progress']
    )
```

## Data Flow

### Creating a Maintenance Request

1. User creates request with equipment
2. System auto-assigns team from equipment
3. System checks overdue status
4. Request appears in Kanban grouped by state

### Completing Maintenance

1. User starts request (New → In Progress)
2. User completes with duration
3. System validates duration > 0
4. System updates request state (In Progress → Repaired)
5. System recomputes equipment health score
6. Dashboard updates KPIs

### Health Score Update

1. Equipment health score computed on:
   - Equipment creation
   - Request completion
   - Manual refresh
2. Algorithm considers:
   - Breakdowns in last 30 days
   - Current overdue requests
3. Score updates equipment record
4. Alerts generated if score < 40

## Extension Points

### Adding New Models

1. Create model class inheriting from BaseModel
2. Implement create, read, write, unlink as needed
3. Add computed fields using `_compute_*` methods
4. Create XML views
5. Register in models/__init__.py

### Adding New Workflows

1. Add state to STATES list
2. Implement action methods
3. Update XML views with new buttons
4. Add validation logic

### Customizing Health Score

Modify `Equipment._compute_health_score()`:
- Adjust penalty weights
- Add new factors
- Change time windows
- Add equipment-specific rules

## Performance Considerations

### Optimization Strategies

1. **Lazy Computation**: Health scores computed on-demand
2. **Caching**: Dashboard data can be cached
3. **Indexing**: Domain searches can be optimized with indexes
4. **Batch Operations**: Multiple updates in single transaction

### Scalability

- Models are stateless (except records)
- Environment pattern allows dependency injection
- Can be extended to use database backend
- XML views can be rendered server-side or client-side

## Testing Strategy

### Unit Tests
- Model methods
- Business logic
- Validation rules

### Integration Tests
- Workflow completion
- Auto-assignment
- Health score updates

### Demo Script
- `demo.py`: Complete workflow demonstration
- `app.py`: Basic setup and dashboard

## Deployment

### Requirements
- Python 3.7+
- No external dependencies (standard library only)

### Setup
```bash
python app.py  # Basic demo
python demo.py  # Full workflow demo
```

### Integration
- Can be integrated into Odoo framework
- Can be adapted to Django/Flask
- Can use database backend (PostgreSQL, MySQL)

## Code Quality

### Standards
- PEP 8 compliant
- Type hints where appropriate
- Docstrings for all methods
- Clear variable names
- Modular design

### Comments
- Complex logic explained
- Business rules documented
- Algorithm rationale provided

## Future Enhancements

1. **Database Backend**: Replace in-memory storage
2. **API Layer**: REST/GraphQL endpoints
3. **Real-time Updates**: WebSocket support
4. **Mobile App**: Field technician interface
5. **IoT Integration**: Sensor data ingestion
6. **ML Integration**: Advanced predictive models
7. **Reporting**: Advanced analytics and exports

