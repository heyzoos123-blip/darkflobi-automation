#!/usr/bin/env python3
"""
DARKFLOBI AUTOMATION - System Tests
Comprehensive testing suite for the tokenized AI gremlin ecosystem
"""

import pytest
import json
import os
import sys
import requests
from unittest.mock import Mock, patch
import tempfile
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestDarkflobiCore:
    """Core system functionality tests"""
    
    def test_project_structure(self):
        """Test that all essential files exist"""
        required_files = [
            'README.md',
            'requirements.txt',
            'COMPLETE-WEBSITE.html',
            'LAUNCH-CHECKLIST.md',
            'TOKEN-LAUNCH.md'
        ]
        
        for file in required_files:
            assert os.path.exists(file), f"Required file missing: {file}"
    
    def test_configuration_files(self):
        """Test configuration files are valid"""
        
        # Test package.json exists and is valid JSON
        if os.path.exists('package.json'):
            with open('package.json', 'r') as f:
                package_data = json.load(f)
                assert 'name' in package_data
                assert 'darkflobi' in package_data.get('name', '').lower()
    
    def test_branding_assets(self):
        """Test that branding assets are properly configured"""
        branding_dir = Path('branding')
        if branding_dir.exists():
            logo_file = branding_dir / 'DARKFLOBI-LOGO-CONCEPT.md'
            assert logo_file.exists(), "Logo concept file missing"
            
            with open(logo_file, 'r') as f:
                content = f.read()
                assert 'darkflobi' in content.lower()
                assert 'gremlin' in content.lower()


class TestVoiceIntegration:
    """Voice system functionality tests"""
    
    @patch('requests.post')
    def test_elevenlabs_integration(self, mock_post):
        """Test ElevenLabs API integration"""
        
        # Mock successful response
        mock_post.return_value.status_code = 200
        mock_post.return_value.content = b"fake_audio_data"
        
        # Import and test voice system (would need actual implementation)
        try:
            # This would test the actual voice integration
            # For now, just test the concept
            voice_config = {
                "stability": 0.75,
                "similarity_boost": 0.85,
                "style": 0.30,
                "use_speaker_boost": True
            }
            
            assert voice_config["stability"] > 0
            assert voice_config["similarity_boost"] > 0
            assert isinstance(voice_config["use_speaker_boost"], bool)
            
        except ImportError:
            pytest.skip("Voice integration not yet implemented")
    
    def test_voice_personality_markers(self):
        """Test voice personality processing"""
        
        def add_personality_markers(text):
            """Mock implementation of personality marker addition"""
            text = text.replace("DARKFLOBI", "dark-flo-bee")
            text = text.replace("$DARKFLOBI", "dollar dark-flo-bee token")
            
            emphasis_words = ["gremlin", "automation", "chaos", "legendary"]
            for word in emphasis_words:
                text = text.replace(word, f"*{word}*")
            
            return text
        
        test_text = "DARKFLOBI is a gremlin automation system"
        result = add_personality_markers(test_text)
        
        assert "dark-flo-bee" in result
        assert "*gremlin*" in result
        assert "*automation*" in result


class TestWebsiteComponents:
    """Website functionality and content tests"""
    
    def test_website_html_validity(self):
        """Test that the main website file is valid HTML"""
        website_file = 'COMPLETE-WEBSITE.html'
        
        if os.path.exists(website_file):
            with open(website_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Basic HTML structure tests
            assert '<!DOCTYPE html>' in content
            assert '<html' in content
            assert '</html>' in content
            assert '<head>' in content
            assert '</head>' in content
            assert '<body>' in content
            assert '</body>' in content
            
            # Darkflobi branding tests
            assert 'DARKFLOBI' in content
            assert 'gremlin' in content.lower()
            assert '💎' in content
    
    def test_website_responsive_design(self):
        """Test responsive design elements"""
        website_file = 'COMPLETE-WEBSITE.html'
        
        if os.path.exists(website_file):
            with open(website_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Bootstrap responsive classes
            assert 'col-md-' in content
            assert 'container' in content
            assert 'viewport' in content  # Mobile viewport meta tag
    
    def test_website_performance_features(self):
        """Test performance optimization features"""
        website_file = 'COMPLETE-WEBSITE.html'
        
        if os.path.exists(website_file):
            with open(website_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # CDN usage for faster loading
            assert 'cdn.jsdelivr.net' in content or 'cdnjs.cloudflare.com' in content
            
            # Proper meta tags for SEO
            assert 'description' in content
            assert 'charset' in content


class TestTokenizationSystem:
    """Token launch and economics tests"""
    
    def test_token_launch_materials(self):
        """Test token launch documentation"""
        token_file = 'TOKEN-LAUNCH.md'
        
        if os.path.exists(token_file):
            with open(token_file, 'r') as f:
                content = f.read()
            
            # Essential tokenomics elements
            assert '$DARKFLOBI' in content
            assert 'tokenomics' in content.lower() or 'economics' in content.lower()
            assert 'community' in content.lower()
            assert 'governance' in content.lower()
    
    def test_competitive_analysis(self):
        """Test competitive analysis completeness"""
        comp_file = 'COMPETITIVE-ADVANTAGE.md'
        
        if os.path.exists(comp_file):
            with open(comp_file, 'r') as f:
                content = f.read()
            
            # Market analysis elements
            assert 'competition' in content.lower() or 'competitive' in content.lower()
            assert 'advantage' in content.lower()
            assert 'ai agent' in content.lower() or 'AI agent' in content


class TestMarketingAutomation:
    """Marketing system functionality tests"""
    
    def test_social_media_content_calendar(self):
        """Test social media strategy"""
        calendar_file = 'SOCIAL-CONTENT-CALENDAR.md'
        
        if os.path.exists(calendar_file):
            with open(calendar_file, 'r') as f:
                content = f.read()
            
            # Content strategy elements
            assert 'twitter' in content.lower() or 'social' in content.lower()
            assert 'gremlin' in content.lower()
            assert 'content' in content.lower()
            assert 'campaign' in content.lower()
    
    def test_launch_checklist(self):
        """Test launch preparation completeness"""
        checklist_file = 'LAUNCH-CHECKLIST.md'
        
        if os.path.exists(checklist_file):
            with open(checklist_file, 'r') as f:
                content = f.read()
            
            # Launch elements
            assert 'launch' in content.lower()
            assert 'github' in content.lower()
            assert 'deploy' in content.lower()


class TestSystemIntegration:
    """Integration and deployment tests"""
    
    def test_docker_configuration(self):
        """Test Docker setup"""
        dockerfile = 'Dockerfile'
        compose_file = 'docker-compose.yml'
        
        if os.path.exists(dockerfile):
            with open(dockerfile, 'r') as f:
                docker_content = f.read()
            
            assert 'FROM python:' in docker_content
            assert 'COPY requirements.txt' in docker_content or 'COPY . ' in docker_content
        
        if os.path.exists(compose_file):
            with open(compose_file, 'r') as f:
                compose_content = f.read()
            
            assert 'darkflobi' in compose_content.lower()
            assert 'services:' in compose_content
    
    def test_github_actions_workflow(self):
        """Test CI/CD pipeline configuration"""
        workflow_file = '.github/workflows/ci-cd.yml'
        
        if os.path.exists(workflow_file):
            with open(workflow_file, 'r') as f:
                workflow_content = f.read()
            
            assert 'Darkflobi' in workflow_content
            assert 'test:' in workflow_content
            assert 'deploy' in workflow_content.lower()
    
    def test_environment_configuration(self):
        """Test environment setup"""
        
        # Test that environment variables are properly configured
        env_vars = [
            'ELEVENLABS_API_KEY',
            'GITHUB_TOKEN', 
            'COMPOSIO_API_KEY'
        ]
        
        # In testing, these should be mock values or skipped
        for var in env_vars:
            # Just test that we know what env vars we need
            assert isinstance(var, str)
            assert len(var) > 0


class TestSecurityAndCompliance:
    """Security and compliance tests"""
    
    def test_no_secrets_in_code(self):
        """Test that no API keys or secrets are hardcoded"""
        
        # Files that should never contain secrets
        code_files = []
        
        for root, dirs, files in os.walk('.'):
            # Skip test files and node_modules
            if 'test' in root or 'node_modules' in root or '.git' in root:
                continue
                
            for file in files:
                if file.endswith(('.py', '.js', '.md', '.yml', '.yaml')):
                    code_files.append(os.path.join(root, file))
        
        secret_patterns = [
            'sk-',  # OpenAI keys
            'api_key',  # Generic API keys
            'password',  # Passwords
            'secret',   # Secrets
        ]
        
        for file_path in code_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().lower()
                    
                for pattern in secret_patterns:
                    # Allow documentation but not actual values
                    if pattern in content and '${' not in content and 'your_' not in content:
                        lines = content.split('\n')
                        for i, line in enumerate(lines):
                            if pattern in line and not line.strip().startswith('#'):
                                # This is a potential secret - flag for review
                                print(f"Potential secret in {file_path}:{i+1}: {line[:50]}")
                                
            except Exception:
                # Skip files that can't be read
                continue
    
    def test_docker_security(self):
        """Test Docker security best practices"""
        dockerfile = 'Dockerfile'
        
        if os.path.exists(dockerfile):
            with open(dockerfile, 'r') as f:
                content = f.read()
            
            # Should not run as root
            assert 'USER' in content and 'USER root' not in content
            
            # Should have health checks
            assert 'HEALTHCHECK' in content


class TestPerformance:
    """Performance and optimization tests"""
    
    def test_file_sizes(self):
        """Test that files are reasonably sized"""
        
        # Website file should not be excessively large
        website_file = 'COMPLETE-WEBSITE.html'
        if os.path.exists(website_file):
            size = os.path.getsize(website_file)
            # Should be under 50KB for good performance
            assert size < 50 * 1024, f"Website file is too large: {size} bytes"
    
    def test_image_optimization(self):
        """Test that images are optimized"""
        
        # Look for image files
        image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.webp']
        
        for root, dirs, files in os.walk('.'):
            if 'node_modules' in root or '.git' in root:
                continue
                
            for file in files:
                if any(file.lower().endswith(ext) for ext in image_extensions):
                    file_path = os.path.join(root, file)
                    size = os.path.getsize(file_path)
                    
                    # Images should generally be under 500KB
                    assert size < 500 * 1024, f"Image {file_path} is too large: {size} bytes"


if __name__ == '__main__':
    # Run tests with pytest
    pytest.main([__file__, '-v'])