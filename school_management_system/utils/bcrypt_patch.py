"""
Monkey patch for passlib.handlers.bcrypt to fix compatibility issues with newer bcrypt versions.
"""
import sys
import logging
import importlib
from types import ModuleType

logger = logging.getLogger(__name__)

def apply_patch():
    """
    Apply monkey patch to fix compatibility issues between passlib and bcrypt.
    """
    try:
        # Import the modules we need to patch
        import bcrypt
        import passlib.handlers.bcrypt
        
        # Direct patch of the problematic function in passlib.handlers.bcrypt
        # This is the PyBcryptBackend._load_backend_mixin method that's causing the error
        def create_patched_method(cls):
            def patched_load_backend_mixin(name, dryrun):
                logger.info(f"Using patched _load_backend_mixin for {name} backend")
                # Skip the version check that's causing the error
                return cls._finalize_backend_mixin(name, dryrun)
            return patched_load_backend_mixin
        
        # Apply the patch to all backend mixins
        for backend_name, backend_cls in passlib.handlers.bcrypt.bcrypt._backend_mixin_map.items():
            if hasattr(backend_cls, '_load_backend_mixin'):
                logger.info(f"Patching {backend_name} backend")
                # Create a bound method for this specific class
                backend_cls._load_backend_mixin = create_patched_method(backend_cls)
        
        # Also patch the bcrypt module to have __about__ attribute
        if not hasattr(bcrypt, '__about__'):
            about_module = ModuleType('__about__')
            about_module.__version__ = getattr(bcrypt, '__version__', '5.0.0')
            bcrypt.__about__ = about_module
            
        logger.info("Bcrypt patch applied successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to apply bcrypt patch: {e}")
        return False
