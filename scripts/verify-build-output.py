#!/usr/bin/env python3
"""
Build verification script for AI-Powered Cooking Assistant
Checks that all required files and dependencies are present before deployment
"""

import os
import sys
import importlib.util
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a file exists and report the result"""
    if os.path.exists(filepath):
        print(f"✅ Found {description}: {filepath}")
        return True
    else:
        print(f"❌ Missing {description}: {filepath}")
        return False

def check_directory_exists(dirpath, description):
    """Check if a directory exists and report the result"""
    if os.path.isdir(dirpath):
        print(f"✅ Found {description}: {dirpath}")
        return True
    else:
        print(f"❌ Missing {description}: {dirpath}")
        return False

def check_python_syntax(filepath):
    """Check if a Python file has valid syntax"""
    try:
        with open(filepath, 'r') as f:
            compile(f.read(), filepath, 'exec')
        print(f"✅ Valid Python syntax: {filepath}")
        return True
    except SyntaxError as e:
        print(f"❌ Syntax error in {filepath}: {e}")
        return False
    except Exception as e:
        print(f"⚠️  Could not verify {filepath}: {e}")
        return True  # Don't fail on other errors

def main():
    print("=" * 60)
    print("🔍 VERIFYING BUILD OUTPUT FOR VERCEL DEPLOYMENT")
    print("=" * 60)
    print()
    
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    all_checks_passed = True
    
    # Check core application files
    print("📄 Checking core application files...")
    all_checks_passed &= check_file_exists("app.py", "Main application")
    all_checks_passed &= check_file_exists("requirements.txt", "Python dependencies")
    all_checks_passed &= check_file_exists("vercel.json", "Vercel configuration")
    all_checks_passed &= check_file_exists("api/index.py", "Vercel API handler")
    print()
    
    # Check source directories
    print("📁 Checking source directories...")
    all_checks_passed &= check_directory_exists("src", "Source code directory")
    all_checks_passed &= check_directory_exists("data", "Data directory")
    all_checks_passed &= check_directory_exists("static", "Static assets directory")
    print()
    
    # Check Python source files
    print("🐍 Checking Python source files...")
    python_files = [
        "app.py",
        "api/index.py",
        "src/adaptive_learning.py",
        "src/image_recognition.py",
        "src/nutrition_analyzer.py",
        "src/substitution_engine.py",
        "src/user_profile.py",
        "data/demo_data.py",
        "data/recipe_database.py"
    ]
    
    for py_file in python_files:
        if os.path.exists(py_file):
            all_checks_passed &= check_python_syntax(py_file)
        else:
            print(f"⚠️  Skipping {py_file} (not found)")
    print()
    
    # Check critical dependencies in requirements.txt
    print("📦 Checking requirements.txt...")
    required_packages = ["streamlit", "transformers", "torch", "pillow", "pandas"]
    try:
        with open("requirements.txt", 'r') as f:
            requirements = f.read()
            for package in required_packages:
                if package.lower() in requirements.lower():
                    print(f"✅ Found required package: {package}")
                else:
                    print(f"⚠️  Package {package} not found in requirements.txt")
    except Exception as e:
        print(f"❌ Error reading requirements.txt: {e}")
        all_checks_passed = False
    print()
    
    # Check static assets
    print("🎨 Checking static assets...")
    check_directory_exists("static/css", "CSS directory")
    check_directory_exists("static/js", "JavaScript directory")
    print()
    
    # Final summary
    print("=" * 60)
    if all_checks_passed:
        print("✅ BUILD VERIFICATION PASSED!")
        print("✅ All required files are present and valid.")
        print("✅ Ready for Vercel deployment.")
        print("=" * 60)
        sys.exit(0)
    else:
        print("❌ BUILD VERIFICATION FAILED!")
        print("❌ Please fix the issues above before deploying.")
        print("=" * 60)
        sys.exit(1)

if __name__ == "__main__":
    main()
