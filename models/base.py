"""
Base model classes following Odoo-style ORM patterns
"""
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional


class BaseModel:
    """
    Base model class with Odoo-style ORM functionality
    Provides common methods for all models
    """
    
    def __init__(self, env=None):
        self.env = env or {}
        self._name = self.__class__.__name__.lower()
        self._records = []
        self._next_id = 1
    
    def create(self, vals: Dict[str, Any]) -> 'BaseModel':
        """Create a new record"""
        record = {
            'id': self._next_id,
            **vals
        }
        self._next_id += 1
        self._records.append(record)
        return self
    
    def search(self, domain: List = None) -> List[Dict]:
        """Search records based on domain"""
        if domain is None:
            return self._records.copy()
        
        results = []
        for record in self._records:
            if self._match_domain(record, domain):
                results.append(record)
        return results
    
    def browse(self, ids: List[int]) -> List[Dict]:
        """Browse records by IDs"""
        if isinstance(ids, int):
            ids = [ids]
        return [r for r in self._records if r.get('id') in ids]
    
    def write(self, ids: List[int], vals: Dict[str, Any]) -> bool:
        """Update records"""
        if isinstance(ids, int):
            ids = [ids]
        for record in self._records:
            if record.get('id') in ids:
                record.update(vals)
        return True
    
    def unlink(self, ids: List[int]) -> bool:
        """Delete records"""
        if isinstance(ids, int):
            ids = [ids]
        self._records = [r for r in self._records if r.get('id') not in ids]
        return True
    
    def _match_domain(self, record: Dict, domain: List) -> bool:
        """Match record against domain criteria"""
        if not domain:
            return True
        
        # Simple domain matching (field, operator, value)
        for condition in domain:
            if len(condition) != 3:
                continue
            field, operator, value = condition
            
            record_value = record.get(field)
            
            if operator == '=':
                if record_value != value:
                    return False
            elif operator == '!=':
                if record_value == value:
                    return False
            elif operator == 'in':
                if record_value not in value:
                    return False
            elif operator == 'not in':
                if record_value in value:
                    return False
            elif operator == '<':
                if record_value >= value:
                    return False
            elif operator == '>':
                if record_value <= value:
                    return False
            elif operator == '<=':
                if record_value > value:
                    return False
            elif operator == '>=':
                if record_value < value:
                    return False
        
        return True
    
    def _compute_field(self, record: Dict, field_name: str, compute_func) -> Any:
        """Compute a field value"""
        return compute_func(record)
    
    def _get_related(self, record: Dict, field_name: str, related_model: str) -> Any:
        """Get related record from another model"""
        related_id = record.get(field_name)
        if related_id and self.env:
            model = self.env.get(related_model)
            if model:
                related_records = model.browse([related_id])
                return related_records[0] if related_records else None
        return None

