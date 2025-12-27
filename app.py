"""
GearGuard+ Maintenance Management System
Main application entry point
"""
from models import (
    Equipment, MaintenanceTeam, MaintenanceRequest, 
    Employee, Dashboard
)


class Environment:
    """Application environment holding all models"""
    
    def __init__(self):
        self.models = {}
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize all models with environment reference"""
        self.models['employee'] = Employee(env=self)
        self.models['maintenance.team'] = MaintenanceTeam(env=self)
        self.models['equipment'] = Equipment(env=self)
        self.models['maintenance.request'] = MaintenanceRequest(env=self)
        self.models['dashboard'] = Dashboard(env=self)
    
    def get(self, model_name):
        """Get a model by name"""
        return self.models.get(model_name)
    
    def __getitem__(self, model_name):
        """Allow dict-style access"""
        return self.get(model_name)


class GearGuardApp:
    """Main application class"""
    
    def __init__(self):
        self.env = Environment()
    
    def setup_demo_data(self):
        """Create demo data for testing"""
        # Create employees/technicians
        emp1 = self.env['employee'].create({
            'name': 'John Technician',
            'email': 'john@company.com',
            'department': 'Maintenance',
            'is_technician': True,
        })
        
        emp2 = self.env['employee'].create({
            'name': 'Sarah Engineer',
            'email': 'sarah@company.com',
            'department': 'Maintenance',
            'is_technician': True,
        })
        
        emp3 = self.env['employee'].create({
            'name': 'Mike Operator',
            'email': 'mike@company.com',
            'department': 'Production',
            'is_technician': False,
        })
        
        # Create maintenance teams
        team1 = self.env['maintenance.team'].create({
            'name': 'Electrical Team',
            'technician_ids': [emp1._records[-1]['id'], emp2._records[-1]['id']],
            'description': 'Handles electrical equipment maintenance',
        })
        
        team2 = self.env['maintenance.team'].create({
            'name': 'Mechanical Team',
            'technician_ids': [emp2._records[-1]['id']],
            'description': 'Handles mechanical equipment maintenance',
        })
        
        # Create equipment
        equip1 = self.env['equipment'].create({
            'name': 'Production Line Conveyor Belt',
            'serial_number': 'CONV-001',
            'department': 'Production',
            'maintenance_team_id': team1._records[-1]['id'],
            'assigned_employee_id': emp3._records[-1]['id'],
            'location': 'Factory Floor A',
            'purchase_date': '2020-01-15',
            'warranty_end_date': '2023-01-15',
        })
        
        equip2 = self.env['equipment'].create({
            'name': 'HVAC System Unit 1',
            'serial_number': 'HVAC-001',
            'department': 'Facilities',
            'maintenance_team_id': team2._records[-1]['id'],
            'location': 'Building 1',
            'purchase_date': '2019-06-20',
            'warranty_end_date': '2022-06-20',
        })
        
        equip3 = self.env['equipment'].create({
            'name': 'CNC Machine Center',
            'serial_number': 'CNC-001',
            'department': 'Manufacturing',
            'maintenance_team_id': team1._records[-1]['id'],
            'location': 'Factory Floor B',
            'purchase_date': '2021-03-10',
            'warranty_end_date': '2024-03-10',
        })
        
        equip4 = self.env['equipment'].create({
            'name': 'Compressor Unit 2',
            'serial_number': 'COMP-002',
            'department': 'Production',
            'maintenance_team_id': team2._records[-1]['id'],
            'location': 'Factory Floor A',
            'purchase_date': '2020-08-15',
            'warranty_end_date': '2023-08-15',
        })
        
        # Get current date for calendar demo
        from datetime import datetime, timedelta
        today = datetime.now()
        current_year = today.year
        current_month = today.month
        current_day = today.day
        
        # Create maintenance requests with various dates for calendar demo
        # RED indicators - Active/Pending requests (new or in_progress)
        req1 = self.env['maintenance.request'].create({
            'subject': 'Routine inspection - Conveyor Belt',
            'equipment_id': equip1._records[-1]['id'],
            'request_type': 'preventive',
            'scheduled_date': f'{current_year}-{current_month:02d}-{min(current_day + 5, 28):02d}',  # 5 days from today
            'technician_id': emp1._records[-1]['id'],
            'description': 'Monthly preventive maintenance check',
            'state': 'new',
        })
        
        req2 = self.env['maintenance.request'].create({
            'subject': 'Belt replacement needed',
            'equipment_id': equip1._records[-1]['id'],
            'request_type': 'corrective',
            'scheduled_date': f'{current_year}-{current_month:02d}-{min(current_day + 3, 28):02d}',  # 3 days from today
            'technician_id': emp1._records[-1]['id'],
            'description': 'Belt showing signs of wear',
            'state': 'in_progress',
        })
        
        req3 = self.env['maintenance.request'].create({
            'subject': 'HVAC Filter Replacement',
            'equipment_id': equip2._records[-1]['id'],
            'request_type': 'preventive',
            'scheduled_date': f'{current_year}-{current_month:02d}-{min(current_day + 7, 28):02d}',  # 7 days from today
            'technician_id': emp2._records[-1]['id'],
            'description': 'Quarterly filter replacement',
            'state': 'new',
        })
        
        req4 = self.env['maintenance.request'].create({
            'subject': 'CNC Calibration Check',
            'equipment_id': equip3._records[-1]['id'],
            'request_type': 'preventive',
            'scheduled_date': f'{current_year}-{current_month:02d}-{min(current_day + 10, 28):02d}',  # 10 days from today
            'technician_id': emp1._records[-1]['id'],
            'description': 'Monthly calibration verification',
            'state': 'in_progress',
        })
        
        # GREEN indicators - Repaired requests (with repaired_date)
        # Create some past repaired requests
        req5 = self.env['maintenance.request'].create({
            'subject': 'Compressor Oil Change',
            'equipment_id': equip4._records[-1]['id'],
            'request_type': 'preventive',
            'scheduled_date': f'{current_year}-{current_month:02d}-{max(current_day - 5, 1):02d}',  # 5 days ago
            'technician_id': emp2._records[-1]['id'],
            'description': 'Regular oil change maintenance',
            'state': 'repaired',
            'repaired_date': f'{current_year}-{current_month:02d}-{max(current_day - 5, 1):02d}',
            'duration': 2.5,
        })
        
        req6 = self.env['maintenance.request'].create({
            'subject': 'Conveyor Belt Repair',
            'equipment_id': equip1._records[-1]['id'],
            'request_type': 'corrective',
            'scheduled_date': f'{current_year}-{current_month:02d}-{max(current_day - 3, 1):02d}',  # 3 days ago
            'technician_id': emp1._records[-1]['id'],
            'description': 'Fixed belt alignment issue',
            'state': 'repaired',
            'repaired_date': f'{current_year}-{current_month:02d}-{max(current_day - 2, 1):02d}',  # Repaired 2 days ago
            'duration': 4.0,
        })
        
        req7 = self.env['maintenance.request'].create({
            'subject': 'HVAC System Cleaning',
            'equipment_id': equip2._records[-1]['id'],
            'request_type': 'preventive',
            'scheduled_date': f'{current_year}-{current_month:02d}-{max(current_day - 8, 1):02d}',  # 8 days ago
            'technician_id': emp2._records[-1]['id'],
            'description': 'Deep cleaning of HVAC unit',
            'state': 'repaired',
            'repaired_date': f'{current_year}-{current_month:02d}-{max(current_day - 7, 1):02d}',  # Repaired 7 days ago
            'duration': 3.5,
        })
        
        req8 = self.env['maintenance.request'].create({
            'subject': 'CNC Spindle Maintenance',
            'equipment_id': equip3._records[-1]['id'],
            'request_type': 'preventive',
            'scheduled_date': f'{current_year}-{current_month:02d}-{max(current_day - 12, 1):02d}',  # 12 days ago
            'technician_id': emp1._records[-1]['id'],
            'description': 'Spindle lubrication and inspection',
            'state': 'repaired',
            'repaired_date': f'{current_year}-{current_month:02d}-{max(current_day - 11, 1):02d}',  # Repaired 11 days ago
            'duration': 1.5,
        })
        
        # Add more equipment for better demo
        equip5 = self.env['equipment'].create({
            'name': 'Water Pump System',
            'serial_number': 'PUMP-001',
            'department': 'Utilities',
            'maintenance_team_id': team2._records[-1]['id'],
            'location': 'Building 2',
            'purchase_date': '2022-01-10',
            'warranty_end_date': '2025-01-10',
        })
        
        equip6 = self.env['equipment'].create({
            'name': 'Server Rack Unit 1',
            'serial_number': 'SRV-001',
            'department': 'IT',
            'maintenance_team_id': team1._records[-1]['id'],
            'location': 'Server Room',
            'purchase_date': '2021-05-15',
            'warranty_end_date': '2024-05-15',
        })
        
        # Add more requests for better Kanban demo
        req9 = self.env['maintenance.request'].create({
            'subject': 'Pump inspection overdue',
            'equipment_id': equip5._records[-1]['id'],
            'request_type': 'preventive',
            'scheduled_date': f'{current_year}-{current_month:02d}-{max(current_day - 2, 1):02d}',  # 2 days ago
            'technician_id': emp2._records[-1]['id'],
            'description': 'Monthly pump inspection',
            'state': 'new',
        })
        
        req10 = self.env['maintenance.request'].create({
            'subject': 'Server cooling fan replacement',
            'equipment_id': equip6._records[-1]['id'],
            'request_type': 'corrective',
            'scheduled_date': f'{current_year}-{current_month:02d}-{min(current_day + 2, 28):02d}',  # 2 days from today
            'technician_id': emp1._records[-1]['id'],
            'description': 'Fan making noise, needs replacement',
            'state': 'in_progress',
        })
        
        req11 = self.env['maintenance.request'].create({
            'subject': 'Routine server maintenance',
            'equipment_id': equip6._records[-1]['id'],
            'request_type': 'preventive',
            'scheduled_date': f'{current_year}-{current_month:02d}-{min(current_day + 15, 28):02d}',  # 15 days from today
            'description': 'Quarterly server maintenance check',
            'state': 'new',
        })
        
        print("Demo data created successfully!")
        print(f"Calendar demo: Check dates around {current_year}-{current_month:02d} for red (pending) and green (repaired) indicators")
        return {
            'employees': [emp1, emp2, emp3],
            'teams': [team1, team2],
            'equipment': [equip1, equip2, equip3, equip4, equip5, equip6],
            'requests': [req1, req2, req3, req4, req5, req6, req7, req8, req9, req10, req11],
        }
    
    def get_dashboard_data(self):
        """Get dashboard data"""
        dashboard = self.env['dashboard']
        return {
            'kpis': dashboard.get_kpis(),
            'preventive_vs_corrective': dashboard.get_preventive_vs_corrective(),
            'requests_per_team': dashboard.get_requests_per_team(),
            'technician_workloads': dashboard.get_technician_workloads(),
            'alerts': dashboard.get_predictive_alerts(),
        }


if __name__ == '__main__':
    app = GearGuardApp()
    
    print("=" * 60)
    print("GearGuard+ Maintenance Management System")
    print("=" * 60)
    print()
    
    # Setup demo data
    demo_data = app.setup_demo_data()
    
    # Display dashboard
    print("\n" + "=" * 60)
    print("DASHBOARD KPIs")
    print("=" * 60)
    dashboard_data = app.get_dashboard_data()
    kpis = dashboard_data['kpis']
    print(f"Total Equipment: {kpis['total_equipment']}")
    print(f"Open Requests: {kpis['open_requests']}")
    print(f"Overdue Requests: {kpis['overdue_requests']}")
    print(f"Critical Health Equipment: {kpis['critical_equipment']}")
    
    print("\n" + "=" * 60)
    print("PREDICTIVE ALERTS")
    print("=" * 60)
    alerts = dashboard_data['alerts']
    if alerts:
        for alert in alerts:
            print(f"\n⚠️  {alert['equipment_name']}")
            print(f"   Health Score: {alert['health_score']}/100")
            print(f"   Breakdowns (30 days): {alert['breakdown_count']}")
            print(f"   Reasons: {', '.join(alert['reasons'])}")
    else:
        print("No alerts - all equipment operating normally")
    
    print("\n" + "=" * 60)
    print("TECHNICIAN WORKLOADS")
    print("=" * 60)
    workloads = dashboard_data['technician_workloads']
    for workload in workloads:
        print(f"{workload['technician_name']}: {workload['workload']} open tasks")
    
    print("\n" + "=" * 60)
    print("SYSTEM READY")
    print("=" * 60)

