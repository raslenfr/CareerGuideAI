"""Simple test without unicode characters for Windows"""
import requests
import json

def test_signup():
    print("\n=== Testing Signup ===")
    
    url = "http://127.0.0.1:5000/api/auth/signup"
    data = {
        "name": "John Doe",
        "email": "john@example.com",
        "password": "password123"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_signup()

