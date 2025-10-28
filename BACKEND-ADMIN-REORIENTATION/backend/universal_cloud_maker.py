# Universal Cloud Maker Service (Backend)
# Consolidates all cloud-generating logic (job cloud, word cloud, job title cloud, peer group cloud, etc.)
# Exposes endpoints for user portal to request any cloud type and overlay options.

# Key Features:
# - Input: Cloud type, user data, peer data, overlay options
# - Output: Cloud data for visualization
# - Supports overlays (e.g., job titles vs. peer similarities, user word cloud vs. peer average)
# - Integrates with ai_data_loader and UnifiedAIEngine

from .ai_data_loader import ai_data_loader

class UniversalCloudMaker:
    def __init__(self, ai_data_loader, ai_engine):
        self.ai_data_loader = ai_data_loader
        self.ai_engine = ai_engine

    def generate_cloud(self, cloud_type, user_data, peer_data=None, overlay=None):
        # Generate base cloud
        base_cloud = self.ai_engine.generate_cloud(cloud_type, user_data)
        overlay_cloud = None
        if overlay and peer_data:
            overlay_cloud = self.ai_engine.generate_cloud(overlay, peer_data)
        # Combine clouds if overlay specified
        if overlay_cloud:
            combined = self.ai_engine.overlay_clouds(base_cloud, overlay_cloud)
            return combined
        return base_cloud

# Expose endpoints for user portal to request cloud generation and overlays
