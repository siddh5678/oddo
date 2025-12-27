"""
Maintenance Team Model
Teams that handle maintenance requests, composed of technicians
"""
from .base import BaseModel


class MaintenanceTeam(BaseModel):
    """Maintenance team with many-to-many technicians"""
    
    def __init__(self, env=None):
        super().__init__(env)
        self._name = 'maintenance.team'
    
    def create(self, vals):
        """Create maintenance team"""
        defaults = {
            'name': vals.get('name', ''),
            'technician_ids': vals.get('technician_ids', []),  # List of employee IDs
            'description': vals.get('description', ''),
            'active': vals.get('active', True),
        }
        defaults.update(vals)
        return super().create(defaults)
    
    def get_team_technicians(self, team_id):
        """Get all technicians in a team"""
        team = self.browse([team_id])
        if not team:
            return []
        
        team_record = team[0]
        technician_ids = team_record.get('technician_ids', [])
        
        if self.env and technician_ids:
            employee_model = self.env.get('employee')
            if employee_model:
                return employee_model.browse(technician_ids)
        return []
    
    def add_technician(self, team_id, technician_id):
        """Add a technician to the team"""
        team = self.browse([team_id])
        if team:
            team_record = team[0]
            technician_ids = team_record.get('technician_ids', [])
            if technician_id not in technician_ids:
                technician_ids.append(technician_id)
                self.write([team_id], {'technician_ids': technician_ids})
            return True
        return False
    
    def remove_technician(self, team_id, technician_id):
        """Remove a technician from the team"""
        team = self.browse([team_id])
        if team:
            team_record = team[0]
            technician_ids = team_record.get('technician_ids', [])
            if technician_id in technician_ids:
                technician_ids.remove(technician_id)
                self.write([team_id], {'technician_ids': technician_ids})
            return True
        return False

