#!/usr/bin/env python3
"""
Configuration Loader
Load and validate configuration from config.yaml
"""

import os
import logging
from pathlib import Path


class ConfigLoader:
    """Load and manage system configuration"""
    
    def __init__(self, config_path="config.yaml"):
        """
        Initialize config loader
        
        Args:
            config_path: Path to config.yaml file
        """
        self.config_path = config_path
        self.config = None
        self.logger = logging.getLogger(__name__)
        
        # Try to load config
        self.load()
    
    def load(self):
        """Load configuration from YAML file"""
        try:
            import yaml
            
            if not os.path.exists(self.config_path):
                self.logger.warning(f"Config file not found: {self.config_path}")
                self.logger.info("Using default configuration")
                self.config = self.get_default_config()
                return
            
            with open(self.config_path, 'r') as f:
                self.config = yaml.safe_load(f)
            
            self.logger.info(f"Configuration loaded from {self.config_path}")
            
        except ImportError:
            self.logger.warning("PyYAML not installed. Using default configuration")
            self.logger.info("Install with: pip3 install pyyaml")
            self.config = self.get_default_config()
            
        except Exception as e:
            self.logger.error(f"Error loading config: {e}")
            self.logger.info("Using default configuration")
            self.config = self.get_default_config()
    
    def get_default_config(self):
        """Get default configuration"""
        return {
            'system': {
                'log_level': 'INFO',
                'cooldown_seconds': 5,
            },
            'camera': {
                'device_id': 0,
                'width': 640,
                'height': 480,
                'fps': 30,
            },
            'models': {
                'blazeface_path': 'models/blazeface.tflite',
                'tinycnn_path': 'models/tinycnn_mrdavid.tflite',
            },
            'detection': {
                'confidence_threshold': 0.7,
                'optimize_speed': True,
            },
            'recognition': {
                'confidence_threshold': 0.75,
                'padding': 0.2,
            },
            'serial': {
                'port': '/dev/ttyAMA0',
                'baudrate': 115200,
                'timeout': 1,
            },
            'greeting': {
                'enabled': True,
                'cooldown': 5,
            },
            'paths': {
                'log_dir': 'logs',
                'models_dir': 'models',
                'face_crops_dir': 'face_crops',
            }
        }
    
    def get(self, key_path, default=None):
        """
        Get configuration value by key path
        
        Args:
            key_path: Dot-separated key path (e.g., 'camera.width')
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        if self.config is None:
            return default
        
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def get_camera_config(self):
        """Get camera configuration"""
        return self.get('camera', {})
    
    def get_detection_config(self):
        """Get detection configuration"""
        return self.get('detection', {})
    
    def get_recognition_config(self):
        """Get recognition configuration"""
        return self.get('recognition', {})
    
    def get_serial_config(self):
        """Get serial configuration"""
        return self.get('serial', {})
    
    def get_model_paths(self):
        """Get model paths"""
        return {
            'blazeface': self.get('models.blazeface_path', 'models/blazeface.tflite'),
            'tinycnn': self.get('models.tinycnn_path', 'models/tinycnn_mrdavid.tflite'),
        }
    
    def validate(self):
        """Validate configuration"""
        errors = []
        
        # Check required paths
        models_dir = self.get('paths.models_dir', 'models')
        if not os.path.exists(models_dir):
            errors.append(f"models directory not found: {models_dir}")
        
        # Check confidence thresholds
        det_thresh = self.get('detection.confidence_threshold', 0.7)
        if not 0.0 <= det_thresh <= 1.0:
            errors.append(f"Invalid detection threshold: {det_thresh}")
        
        rec_thresh = self.get('recognition.confidence_threshold', 0.75)
        if not 0.0 <= rec_thresh <= 1.0:
            errors.append(f"Invalid recognition threshold: {rec_thresh}")
        
        # Check camera settings
        cam_width = self.get('camera.width', 640)
        cam_height = self.get('camera.height', 480)
        if cam_width <= 0 or cam_height <= 0:
            errors.append(f"Invalid camera dimensions: {cam_width}x{cam_height}")
        
        # Check serial settings
        baudrate = self.get('serial.baudrate', 115200)
        if baudrate not in [9600, 19200, 38400, 57600, 115200]:
            errors.append(f"Unusual baudrate: {baudrate}")
        
        if errors:
            self.logger.warning("Configuration validation warnings:")
            for error in errors:
                self.logger.warning(f"  - {error}")
        else:
            self.logger.info("Configuration validated successfully")
        
        return len(errors) == 0
    
    def save(self, output_path=None):
        """
        Save current configuration to file
        
        Args:
            output_path: Output file path (default: self.config_path)
        """
        if output_path is None:
            output_path = self.config_path
        
        try:
            import yaml
            
            with open(output_path, 'w') as f:
                yaml.dump(self.config, f, default_flow_style=False, indent=2)
            
            self.logger.info(f"Configuration saved to {output_path}")
            return True
            
        except ImportError:
            self.logger.error("PyYAML not installed. Cannot save config")
            return False
            
        except Exception as e:
            self.logger.error(f"Error saving config: {e}")
            return False
    
    def print_config(self):
        """Print configuration summary"""
        print("\n" + "=" * 70)
        print("Configuration Summary")
        print("=" * 70)
        
        # System
        print("\n[System]")
        print(f"  Log Level: {self.get('system.log_level', 'INFO')}")
        print(f"  Cooldown: {self.get('system.cooldown_seconds', 5)}s")
        
        # Camera
        print("\n[Camera]")
        cam = self.get_camera_config()
        print(f"  Device: {cam.get('device_id', 0)}")
        print(f"  Resolution: {cam.get('width', 640)}x{cam.get('height', 480)}")
        print(f"  FPS: {cam.get('fps', 30)}")
        
        # Models
        print("\n[models]")
        models = self.get_model_paths()
        print(f"  BlazeFace: {models['blazeface']}")
        print(f"  TinyCNN: {models['tinycnn']}")
        
        # Detection
        print("\n[Detection]")
        det = self.get_detection_config()
        print(f"  Confidence: {det.get('confidence_threshold', 0.7)}")
        print(f"  Optimize Speed: {det.get('optimize_speed', True)}")
        
        # Recognition
        print("\n[Recognition]")
        rec = self.get_recognition_config()
        print(f"  Confidence: {rec.get('confidence_threshold', 0.75)}")
        print(f"  Target: {rec.get('target_person', 'Mr. David')}")
        
        # Serial
        print("\n[Serial]")
        ser = self.get_serial_config()
        print(f"  Port: {ser.get('port', '/dev/ttyAMA0')}")
        print(f"  Baudrate: {ser.get('baudrate', 115200)}")
        
        print("\n" + "=" * 70)


# Test code
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    print("=" * 70)
    print("Configuration Loader - Test Mode")
    print("=" * 70)
    print()
    
    # Load configuration
    config = ConfigLoader("config.yaml")
    
    # Print configuration
    config.print_config()
    
    # Validate
    print("\nValidating configuration...")
    is_valid = config.validate()
    
    if is_valid:
        print("✓ Configuration is valid")
    else:
        print("⚠ Configuration has warnings (see above)")
    
    # Test getting specific values
    print("\n" + "=" * 70)
    print("Testing Configuration Access")
    print("=" * 70)
    
    print(f"\nCamera width: {config.get('camera.width')}")
    print(f"Detection threshold: {config.get('detection.confidence_threshold')}")
    print(f"Serial port: {config.get('serial.port')}")
    print(f"models directory: {config.get('paths.models_dir')}")
    
    print("\n" + "=" * 70)
    print("✓ Configuration loader ready!")
    print("=" * 70)
