print("Loading test_model_manager.py")
"""
Test module for ModelManager
"""
import os
import sys
from pathlib import Path

print("Current file:", __file__)
print("Current directory:", os.getcwd())

# Add the project root to Python path
project_root = Path(__file__).parent.absolute()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

print("Python path:", sys.path)

# Import using absolute path
print("Attempting to import ModelManager...")
from src.model_manager import ModelManager
print("Import successful")

def test_model_loading():
    """Test model loading functionality"""
    print("\nStarting model loading test...")
    
    try:
        print("Creating ModelManager instance...")
        manager = ModelManager()
        print("ModelManager instance created successfully")
        
        print("\nAttempting to load model...")
        success = manager.load_model()
        
        if success:
            print("Model loaded successfully!")
            return True
            
    except Exception as e:
        print(f"\nError during test:")
        print(f"Error type: {type(e)}")
        print(f"Error message: {str(e)}")
        raise

if __name__ == "__main__":
    test_model_loading()
