"""Project profile detection and management."""
import yaml
from pathlib import Path
from typing import Optional

class ProfileManager:
    def __init__(self, profiles_dir: str = "profiles"):
        self.profiles_dir = Path(profiles_dir)
    
    def detect_profile(self, project_path: str) -> str:
        """Auto-detect project profile based on files and structure."""
        path = Path(project_path)
        
        # Check for medical app indicators
        medical_indicators = ["burn", "clinic", "ecg", "patient", "medical", "hipaa"]
        if any(indicator in str(path).lower() for indicator in medical_indicators):
            return "medical"
        
        # Check for game indicators
        game_indicators = ["mendelian", "game", "sprite", "scene", "unity", "godot", "ios"]
        if any(indicator in str(path).lower() for indicator in game_indicators):
            return "game"
        
        # Check file extensions for Swift/iOS
        if path.is_file() and path.suffix in [".swift", ".m", ".mm"]:
            return "game"
        
        return "general"
    
    def load_profile(self, profile_name: str) -> dict:
        """Load profile configuration."""
        profile_path = self.profiles_dir / f"{profile_name}.yaml"
        if not profile_path.exists():
            profile_path = self.profiles_dir / "general.yaml"
        
        with open(profile_path) as f:
            return yaml.safe_load(f)
    
    def get_handoff_template(self, profile_name: str, analysis: str) -> str:
        """Get formatted handoff template for profile."""
        profile = self.load_profile(profile_name)
        template = profile.get("handoff_template", "{analysis}")
        return template.format(analysis=analysis)
