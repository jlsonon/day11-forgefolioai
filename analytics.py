"""
Analytics and Statistics for PortfolioForge
Track usage and provide insights
"""
import json
import os
from datetime import datetime
from typing import Dict, List, Any

class Analytics:
    """Simple analytics tracking for PortfolioForge"""
    
    def __init__(self, data_file: str = 'analytics.json'):
        self.data_file = data_file
        self.data = self._load_data()
    
    def _load_data(self) -> Dict[str, Any]:
        """Load analytics data from file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except:
                return self._init_data()
        return self._init_data()
    
    def _init_data(self) -> Dict[str, Any]:
        """Initialize analytics data structure"""
        return {
            'total_generations': 0,
            'templates_used': {},
            'professions': {},
            'daily_stats': {},
            'features_used': {
                'sample_profiles': 0,
                'template_selection': 0,
                'copy_to_clipboard': 0,
                'regenerate': 0
            },
            'start_date': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat()
        }
    
    def _save_data(self):
        """Save analytics data to file"""
        self.data['last_updated'] = datetime.now().isoformat()
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def track_generation(self, template_id: str, profession: str, features_used: List[str] = None):
        """Track a portfolio generation"""
        self.data['total_generations'] += 1
        
        # Track template usage
        if template_id not in self.data['templates_used']:
            self.data['templates_used'][template_id] = 0
        self.data['templates_used'][template_id] += 1
        
        # Track profession
        if profession not in self.data['professions']:
            self.data['professions'][profession] = 0
        self.data['professions'][profession] += 1
        
        # Track daily stats
        today = datetime.now().strftime('%Y-%m-%d')
        if today not in self.data['daily_stats']:
            self.data['daily_stats'][today] = 0
        self.data['daily_stats'][today] += 1
        
        # Track features used
        if features_used:
            for feature in features_used:
                if feature in self.data['features_used']:
                    self.data['features_used'][feature] += 1
        
        self._save_data()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get analytics statistics"""
        return {
            'total_generations': self.data['total_generations'],
            'most_popular_template': max(self.data['templates_used'].items(), key=lambda x: x[1])[0] if self.data['templates_used'] else None,
            'most_popular_profession': max(self.data['professions'].items(), key=lambda x: x[1])[0] if self.data['professions'] else None,
            'templates_used': self.data['templates_used'],
            'professions': self.data['professions'],
            'features_used': self.data['features_used'],
            'daily_stats': self.data['daily_stats'],
            'start_date': self.data['start_date'],
            'last_updated': self.data['last_updated']
        }
    
    def get_demo_stats(self) -> Dict[str, Any]:
        """Get demo-friendly statistics"""
        stats = self.get_stats()
        
        return {
            'total_portfolios_generated': stats['total_generations'],
            'most_popular_template': stats['most_popular_template'][0] if stats['most_popular_template'] else 'Modern Tech',
            'most_popular_profession': stats['most_popular_profession'] or 'Software Developer',
            'templates_available': len(stats['templates_used']),
            'professions_served': len(stats['professions']),
            'features_most_used': max(stats['features_used'].items(), key=lambda x: x[1])[0] if any(stats['features_used'].values()) else 'Template Selection',
            'daily_generations': sum(stats['daily_stats'].values()),
            'uptime_days': (datetime.now() - datetime.fromisoformat(stats['start_date'])).days + 1
        }

# Global analytics instance
analytics = Analytics()
