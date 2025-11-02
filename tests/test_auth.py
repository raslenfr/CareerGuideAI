"""
Simple test script to verify authentication system.
Run this with: python test_auth.py
"""

import requests
import json

BASE_URL = "http://127.0.0.1:5000/api/auth"

def test_signup():
    """Test user signup."""
    print("\n=== Testing Signup ===")
    
    signup_data = {
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/signup", json=signup_data)
        data = response.json()
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(data, indent=2)}")
        
        if data.get('success'):
            print("✅ Signup successful!")
            return data.get('user')
        else:
            print(f"❌ Signup failed: {data.get('error')}")
            return None
            
    except Exception as e:
        print(f"❌ Error during signup: {e}")
        return None


def test_login(email, password):
    """Test user login."""
    print("\n=== Testing Login ===")
    
    login_data = {
        "email": email,
        "password": password
    }
    
    try:
        response = requests.post(f"{BASE_URL}/login", json=login_data)
        data = response.json()
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(data, indent=2)}")
        
        if data.get('success'):
            print("✅ Login successful!")
            return data.get('user')
        else:
            print(f"❌ Login failed: {data.get('error')}")
            return None
            
    except Exception as e:
        print(f"❌ Error during login: {e}")
        return None


def test_login_wrong_password(email):
    """Test login with wrong password."""
    print("\n=== Testing Login with Wrong Password ===")
    
    login_data = {
        "email": email,
        "password": "wrongpassword"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/login", json=login_data)
        data = response.json()
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(data, indent=2)}")
        
        if not data.get('success'):
            print("✅ Correctly rejected wrong password!")
        else:
            print("❌ ERROR: Wrong password was accepted!")
            
    except Exception as e:
        print(f"❌ Error during login test: {e}")


def check_backend():
    """Check if backend is running."""
    print("=== Checking Backend Status ===")
    try:
        response = requests.get("http://127.0.0.1:5000/")
        if response.status_code == 200:
            print("✅ Backend is running!")
            return True
        else:
            print(f"❌ Backend returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        print("Make sure Flask server is running on port 5000")
        return False


if __name__ == "__main__":
    print("=" * 50)
    print("Authentication System Test")
    print("=" * 50)
    
    # Check if backend is running
    if not check_backend():
        exit(1)
    
    # Test signup
    user = test_signup()
    
    if user:
        # Test login with correct credentials
        test_login("testuser@example.com", "testpass123")
        
        # Test login with wrong password
        test_login_wrong_password("testuser@example.com")
    
    print("\n" + "=" * 50)
    print("Test Complete!")
    print("=" * 50)
    print("\nTo view the database:")
    print("1. Download DB Browser for SQLite: https://sqlitebrowser.org/")
    print("2. Open Backend/instance/course_recommendation.db")
    print("3. Browse the 'users' table to see registered users")

