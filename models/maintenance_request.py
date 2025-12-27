"""
Maintenance Request Model
Core workflow model for maintenance operations
"""
from datetime import datetime, timedelta
from .base import BaseModel


class MaintenanceRequest(BaseModel):
    """Maintenance request with state workflow"""
    
    # State selection
    STATES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('repaired', 'Repaired'),
        ('scrap', 'Scrap'),
    ]
    
    REQUEST_TYPES = [
        ('preventive', 'Preventive'),
        ('corrective', 'Corrective'),
    ]
    
    def __init__(self, env=None):
        super().__init__(env)
        self._name = 'maintenance.request'
    
    def create(self, vals):
        """Create maintenance request with auto-assignment logic"""
        defaults = {
            'subject': vals.get('subject', ''),
            'equipment_id': vals.get('equipment_id', False),
            'request_type': vals.get('request_type', 'corrective'),
            'scheduled_date': vals.get('scheduled_date', False),
            'technician_id': vals.get('technician_id', False),
            'maintenance_team_id': vals.get('maintenance_team_id', False),
            'duration': vals.get('duration', 0.0),
            'description': vals.get('description', ''),
            'state': 'new',
            'create_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'repaired_date': False,  # Date when request was repaired
            'is_overdue': False,
        }
        
        # Auto-assign maintenance team from equipment
        if defaults['equipment_id'] and not defaults['maintenance_team_id']:
            if self.env:
                equipment_model = self.env.get('equipment')
                if equipment_model:
                    equipment = equipment_model.browse([defaults['equipment_id']])
                    if equipment:
                        team_id = equipment[0].get('maintenance_team_id')
                        if team_id:
                            defaults['maintenance_team_id'] = team_id
        
        defaults.update(vals)
        record = super().create(defaults)
        
        # Check overdue status
        self._check_overdue(record._records[-1]['id'])
        
        return record
    
    def _check_overdue(self, request_id):
        """Check and update overdue status"""
        request = self.browse([request_id])
        if not request:
            return False
        
        request_record = request[0]
        scheduled_date = request_record.get('scheduled_date')
        state = request_record.get('state', 'new')
        
        if not scheduled_date:
            return False
        
        # Check if overdue (scheduled date passed and still not repaired/scrap)
        today = datetime.now().strftime('%Y-%m-%d')
        is_overdue = (
            scheduled_date < today and 
            state in ['new', 'in_progress']
        )
        
        self.write([request_id], {'is_overdue': is_overdue})
        return is_overdue
    
    def action_start(self, request_id):
        """Start maintenance (New -> In Progress)"""
        request = self.browse([request_id])
        if not request:
            return False
        
        current_state = request[0].get('state', 'new')
        if current_state != 'new':
            return False
        
        self.write([request_id], {'state': 'in_progress'})
        self._check_overdue(request_id)
        return True
    
    def action_repair(self, request_id, duration=None):
        """
        Complete repair (In Progress -> Repaired)
        Duration is mandatory before closing
        """
        request = self.browse([request_id])
        if not request:
            return False
        
        current_state = request[0].get('state', 'new')
        if current_state not in ['new', 'in_progress']:
            return False
        
        # Duration is mandatory
        current_duration = request[0].get('duration', 0.0)
        if duration:
            current_duration = duration
        
        if not current_duration or current_duration <= 0:
            raise ValueError("Duration is mandatory before closing a maintenance request")
        
        self.write([request_id], {
            'state': 'repaired',
            'duration': current_duration,
            'repaired_date': datetime.now().strftime('%Y-%m-%d'),  # Track repair date
            'is_overdue': False,
        })
        
        # Update equipment health score
        equipment_id = request[0].get('equipment_id')
        if equipment_id and self.env:
            equipment_model = self.env.get('equipment')
            if equipment_model:
                equipment_model._compute_health_score(equipment_id)
        
        return True
    
    def action_scrap(self, request_id):
        """
        Scrap equipment (In Progress -> Scrap)
        Also marks equipment as scrapped
        """
        request = self.browse([request_id])
        if not request:
            return False
        
        current_state = request[0].get('state', 'new')
        if current_state not in ['new', 'in_progress']:
            return False
        
        self.write([request_id], {'state': 'scrap'})
        
        # Mark equipment as scrapped
        equipment_id = request[0].get('equipment_id')
        if equipment_id and self.env:
            equipment_model = self.env.get('equipment')
            if equipment_model:
                equipment_model.action_scrap(equipment_id)
        
        return True
    
    def get_technician_workload(self, technician_id):
        """
        Get workload for a technician (count of open requests)
        Used for workload balancing
        """
        if not technician_id:
            return 0
        
        open_requests = self.search([
            ('technician_id', '=', technician_id),
            ('state', 'in', ['new', 'in_progress'])
        ])
        
        return len(open_requests)
    
    def get_team_technicians(self, team_id):
        """Get technicians available for a team"""
        if not self.env or not team_id:
            return []
        
        team_model = self.env.get('maintenance.team')
        if not team_model:
            return []
        
        return team_model.get_team_technicians(team_id)
    
    def validate_technician_assignment(self, request_id, technician_id, team_id):
        """
        Validate that technician belongs to the assigned team
        """
        if not technician_id or not team_id:
            return True  # No validation needed if not assigned
        
        team_technicians = self.get_team_technicians(team_id)
        technician_ids = [t.get('id') for t in team_technicians]
        
        if technician_id not in technician_ids:
            raise ValueError(f"Technician must be a member of the assigned maintenance team")
        
        return True
    
    def write(self, ids, vals):
        """Override write to validate technician assignment"""
        if isinstance(ids, int):
            ids = [ids]
        
        # Validate technician assignment if both are being set
        if 'technician_id' in vals or 'maintenance_team_id' in vals:
            for request_id in ids:
                request = self.browse([request_id])
                if request:
                    request_record = request[0]
                    technician_id = vals.get('technician_id', request_record.get('technician_id'))
                    team_id = vals.get('maintenance_team_id', request_record.get('maintenance_team_id'))
                    
                    if technician_id and team_id:
                        self.validate_technician_assignment(request_id, technician_id, team_id)
        
        return super().write(ids, vals)
    
    def get_preventive_requests(self, start_date=None, end_date=None):
        """Get preventive maintenance requests for calendar view"""
        domain = [
            ('request_type', '=', 'preventive'),
            ('state', '!=', 'scrap'),
        ]
        
        if start_date:
            domain.append(('scheduled_date', '>=', start_date))
        if end_date:
            domain.append(('scheduled_date', '<=', end_date))
        
        return self.search(domain)
    
    def _get_team_technician_ids(self, team_id):
        """Get technician IDs for a team (for domain filtering)"""
        if not team_id:
            return []
        
        team_technicians = self.get_team_technicians(team_id)
        return [t.get('id') for t in team_technicians]
    
    def read(self, ids, fields=None):
        """Override read to include computed fields"""
        if isinstance(ids, int):
            ids = [ids]
        
        records = self.browse(ids)
        result = []
        
        for record in records:
            record_dict = record.copy()
            request_id = record.get('id')
            team_id = record.get('maintenance_team_id')
            
            # Add computed field for team technicians (for domain filtering)
            if team_id:
                record_dict['team_technician_ids'] = self._get_team_technician_ids(team_id)
            else:
                record_dict['team_technician_ids'] = []
            
            if fields:
                # Filter to requested fields
                record_dict = {k: v for k, v in record_dict.items() if k in fields}
            
            result.append(record_dict)
        
        return result

