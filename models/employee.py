"""
Employee Model
Represents employees who can be assigned to equipment or maintenance teams
"""
from .base import BaseModel


class Employee(BaseModel):
    """Employee model for technicians and equipment assignees"""
    
    def __init__(self, env=None):
        super().__init__(env)
        self._name = 'employee'
    
    def create(self, vals):
        """Create employee with default values"""
        defaults = {
            'name': vals.get('name', ''),
            'email': vals.get('email', ''),
            'phone': vals.get('phone', ''),
            'department': vals.get('department', ''),
            'is_technician': vals.get('is_technician', False),
            'active': vals.get('active', True),
        }
        defaults.update(vals)
        return super().create(defaults)
    
    def get_technicians(self):
        """Get all active technicians"""
        return self.search([('is_technician', '=', True), ('active', '=', True)])

