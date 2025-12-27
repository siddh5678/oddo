"""
Equipment / Asset Management Model
Core model for tracking equipment with health scoring
"""
from datetime import datetime, timedelta
from .base import BaseModel


class Equipment(BaseModel):
    """Equipment model with health score computation"""
    
    def __init__(self, env=None):
        super().__init__(env)
        self._name = 'equipment'
    
    def create(self, vals):
        """Create equipment with computed health score"""
        defaults = {
            'name': vals.get('name', ''),
            'serial_number': vals.get('serial_number', ''),
            'department': vals.get('department', ''),
            'assigned_employee_id': vals.get('assigned_employee_id', False),
            'maintenance_team_id': vals.get('maintenance_team_id', False),
            'purchase_date': vals.get('purchase_date', False),
            'warranty_end_date': vals.get('warranty_end_date', False),
            'location': vals.get('location', ''),
            'is_scrapped': vals.get('is_scrapped', False),
            'health_score': 100,  # Initial health score
            'active': vals.get('active', True),
        }
        defaults.update(vals)
        record = super().create(defaults)
        # Compute initial health score
        self._compute_health_score(record._records[-1]['id'])
        return record
    
    def _compute_health_score(self, equipment_id):
        """
        Compute equipment health score (0-100)
        Based on:
        - Breakdown count (corrective maintenance requests)
        - Overdue maintenance requests
        - Recent maintenance frequency
        """
        equipment = self.browse([equipment_id])
        if not equipment:
            return 0
        
        equipment_record = equipment[0]
        
        # Get maintenance request model
        if not self.env:
            return 100
        
        request_model = self.env.get('maintenance.request')
        if not request_model:
            return 100
        
        # Count corrective breakdowns in last 30 days
        thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        corrective_requests = request_model.search([
            ('equipment_id', '=', equipment_id),
            ('request_type', '=', 'corrective'),
            ('create_date', '>=', thirty_days_ago),
            ('state', 'in', ['repaired', 'scrap'])
        ])
        
        breakdown_count = len(corrective_requests)
        
        # Count overdue requests
        today = datetime.now().strftime('%Y-%m-%d')
        overdue_requests = request_model.search([
            ('equipment_id', '=', equipment_id),
            ('scheduled_date', '<', today),
            ('state', 'in', ['new', 'in_progress'])
        ])
        
        overdue_count = len(overdue_requests)
        
        # Calculate health score
        # Base score: 100
        # Penalty: -15 per breakdown in last 30 days
        # Penalty: -10 per overdue request
        # Minimum: 0
        
        health_score = 100
        health_score -= (breakdown_count * 15)
        health_score -= (overdue_count * 10)
        health_score = max(0, min(100, health_score))
        
        # Update equipment record
        self.write([equipment_id], {'health_score': health_score})
        
        return health_score
    
    def get_health_status(self, equipment_id):
        """Get health status category"""
        equipment = self.browse([equipment_id])
        if not equipment:
            return 'unknown'
        
        health_score = equipment[0].get('health_score', 100)
        
        if health_score >= 70:
            return 'good'
        elif health_score >= 40:
            return 'warning'
        else:
            return 'critical'
    
    def get_maintenance_requests_count(self, equipment_id):
        """Get count of maintenance requests for equipment"""
        if not self.env:
            return 0
        
        request_model = self.env.get('maintenance.request')
        if not request_model:
            return 0
        
        return len(request_model.search([('equipment_id', '=', equipment_id)]))
    
    def get_open_requests_count(self, equipment_id):
        """Get count of open maintenance requests"""
        if not self.env:
            return 0
        
        request_model = self.env.get('maintenance.request')
        if not request_model:
            return 0
        
        return len(request_model.search([
            ('equipment_id', '=', equipment_id),
            ('state', 'in', ['new', 'in_progress'])
        ]))
    
    def action_scrap(self, equipment_id):
        """Mark equipment as scrapped"""
        self.write([equipment_id], {'is_scrapped': True, 'active': False})
        return True
    
    def action_unscrap(self, equipment_id):
        """Unmark equipment as scrapped"""
        self.write([equipment_id], {'is_scrapped': False, 'active': True})
        return True
    
    def _get_maintenance_requests_ids(self, equipment_id):
        """Get all maintenance requests for equipment (one2many)"""
        if not self.env:
            return []
        
        request_model = self.env.get('maintenance.request')
        if not request_model:
            return []
        
        return request_model.search([('equipment_id', '=', equipment_id)])
    
    def _get_maintenance_requests_count(self, equipment_id):
        """Computed field: count of all maintenance requests"""
        requests = self._get_maintenance_requests_ids(equipment_id)
        return len(requests)
    
    def _get_open_requests_count(self, equipment_id):
        """Computed field: count of open maintenance requests"""
        if not self.env:
            return 0
        
        request_model = self.env.get('maintenance.request')
        if not request_model:
            return 0
        
        return len(request_model.search([
            ('equipment_id', '=', equipment_id),
            ('state', 'in', ['new', 'in_progress'])
        ]))
    
    def read(self, ids, fields=None):
        """Override read to include computed fields"""
        if isinstance(ids, int):
            ids = [ids]
        
        records = self.browse(ids)
        result = []
        
        for record in records:
            record_dict = record.copy()
            equip_id = record.get('id')
            
            # Add computed fields
            record_dict['maintenance_requests_count'] = self._get_maintenance_requests_count(equip_id)
            record_dict['open_requests_count'] = self._get_open_requests_count(equip_id)
            record_dict['maintenance_requests_ids'] = self._get_maintenance_requests_ids(equip_id)
            
            if fields:
                # Filter to requested fields
                record_dict = {k: v for k, v in record_dict.items() if k in fields}
            
            result.append(record_dict)
        
        return result

