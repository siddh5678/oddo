"""
Management Dashboard Model
KPIs, charts, and analytics for maintenance management
"""
from datetime import datetime, timedelta
from .base import BaseModel


class Dashboard(BaseModel):
    """Dashboard with KPIs and analytics"""
    
    def __init__(self, env=None):
        super().__init__(env)
        self._name = 'dashboard'
    
    def get_kpis(self):
        """Get key performance indicators"""
        if not self.env:
            return {}
        
        equipment_model = self.env.get('equipment')
        request_model = self.env.get('maintenance.request')
        
        if not equipment_model or not request_model:
            return {}
        
        # Total equipment (active, not scrapped)
        total_equipment = len(equipment_model.search([
            ('is_scrapped', '=', False),
            ('active', '=', True)
        ]))
        
        # Open requests
        open_requests = len(request_model.search([
            ('state', 'in', ['new', 'in_progress'])
        ]))
        
        # Overdue requests
        today = datetime.now().strftime('%Y-%m-%d')
        overdue_requests = len(request_model.search([
            ('scheduled_date', '<', today),
            ('state', 'in', ['new', 'in_progress'])
        ]))
        
        # Equipment with critical health (< 40)
        critical_equipment = len(equipment_model.search([
            ('health_score', '<', 40),
            ('is_scrapped', '=', False),
            ('active', '=', True)
        ]))
        
        return {
            'total_equipment': total_equipment,
            'open_requests': open_requests,
            'overdue_requests': overdue_requests,
            'critical_equipment': critical_equipment,
        }
    
    def get_preventive_vs_corrective(self):
        """Get chart data: Preventive vs Corrective maintenance"""
        if not self.env:
            return {'preventive': 0, 'corrective': 0}
        
        request_model = self.env.get('maintenance.request')
        if not request_model:
            return {'preventive': 0, 'corrective': 0}
        
        preventive = len(request_model.search([
            ('request_type', '=', 'preventive')
        ]))
        
        corrective = len(request_model.search([
            ('request_type', '=', 'corrective')
        ]))
        
        return {
            'preventive': preventive,
            'corrective': corrective,
        }
    
    def get_requests_per_team(self):
        """Get chart data: Requests per maintenance team"""
        if not self.env:
            return []
        
        team_model = self.env.get('maintenance.team')
        request_model = self.env.get('maintenance.request')
        
        if not team_model or not request_model:
            return []
        
        teams = team_model.search([])
        result = []
        
        for team in teams:
            team_id = team.get('id')
            team_name = team.get('name', 'Unknown')
            
            request_count = len(request_model.search([
                ('maintenance_team_id', '=', team_id)
            ]))
            
            result.append({
                'team_id': team_id,
                'team_name': team_name,
                'request_count': request_count,
            })
        
        return result
    
    def get_technician_workloads(self):
        """Get workload distribution across technicians"""
        if not self.env:
            return []
        
        employee_model = self.env.get('employee')
        request_model = self.env.get('maintenance.request')
        
        if not employee_model or not request_model:
            return []
        
        technicians = employee_model.get_technicians()
        result = []
        
        for technician in technicians:
            technician_id = technician.get('id')
            workload = request_model.get_technician_workload(technician_id)
            
            result.append({
                'technician_id': technician_id,
                'technician_name': technician.get('name', 'Unknown'),
                'workload': workload,
            })
        
        # Sort by workload descending
        result.sort(key=lambda x: x['workload'], reverse=True)
        
        return result
    
    def get_predictive_alerts(self):
        """
        Get predictive maintenance alerts
        Triggers:
        - 3+ corrective breakdowns in last 30 days
        - Health score < 40
        """
        if not self.env:
            return []
        
        equipment_model = self.env.get('equipment')
        request_model = self.env.get('maintenance.request')
        
        if not equipment_model or not request_model:
            return []
        
        alerts = []
        thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        
        # Get all active equipment
        all_equipment = equipment_model.search([
            ('is_scrapped', '=', False),
            ('active', '=', True)
        ])
        
        for equipment in all_equipment:
            equipment_id = equipment.get('id')
            equipment_name = equipment.get('name', 'Unknown')
            health_score = equipment.get('health_score', 100)
            
            # Check breakdown count
            breakdowns = request_model.search([
                ('equipment_id', '=', equipment_id),
                ('request_type', '=', 'corrective'),
                ('create_date', '>=', thirty_days_ago),
                ('state', 'in', ['repaired', 'scrap'])
            ])
            
            breakdown_count = len(breakdowns)
            
            # Generate alert if conditions met
            alert_reasons = []
            if breakdown_count >= 3:
                alert_reasons.append(f"{breakdown_count} corrective breakdowns in last 30 days")
            
            if health_score < 40:
                alert_reasons.append(f"Health score critical: {health_score}/100")
            
            if alert_reasons:
                alerts.append({
                    'equipment_id': equipment_id,
                    'equipment_name': equipment_name,
                    'health_score': health_score,
                    'breakdown_count': breakdown_count,
                    'reasons': alert_reasons,
                    'severity': 'critical' if health_score < 40 else 'warning',
                })
        
        return alerts

