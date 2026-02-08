"""
Test script for authentication endpoints

Usage:
    python test_auth.py
"""
import requests
import json


BASE_URL = "http://localhost:8000"


def test_register():
    """Test user registration"""
    print("\n1. Testing user registration...")

    response = requests.post(
        f"{BASE_URL}/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "Test1234",
            "confirm_password": "Test1234",
            "name": "Test User"
        }
    )

    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    if response.status_code == 201:
        print("✓ Registration successful")
        return response.json()
    else:
        print("✗ Registration failed")
        return None


def test_login():
    """Test user login"""
    print("\n2. Testing user login...")

    response = requests.post(
        f"{BASE_URL}/api/v1/auth/login",
        json={
            "email": "test@example.com",
            "password": "Test1234"
        }
    )

    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    if response.status_code == 200:
        print("✓ Login successful")
        return response.json()
    else:
        print("✗ Login failed")
        return None


def test_get_profile(access_token):
    """Test getting user profile"""
    print("\n3. Testing get profile...")

    response = requests.get(
        f"{BASE_URL}/api/v1/auth/me",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    if response.status_code == 200:
        print("✓ Get profile successful")
        return response.json()
    else:
        print("✗ Get profile failed")
        return None


def test_update_profile(access_token):
    """Test updating user profile"""
    print("\n4. Testing update profile...")

    response = requests.put(
        f"{BASE_URL}/api/v1/auth/me",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"name": "Updated Test User"}
    )

    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    if response.status_code == 200:
        print("✓ Update profile successful")
        return response.json()
    else:
        print("✗ Update profile failed")
        return None


def test_refresh_token(refresh_token):
    """Test token refresh"""
    print("\n5. Testing token refresh...")

    response = requests.post(
        f"{BASE_URL}/api/v1/auth/refresh",
        json={"refresh_token": refresh_token}
    )

    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    if response.status_code == 200:
        print("✓ Token refresh successful")
        return response.json()
    else:
        print("✗ Token refresh failed")
        return None


def test_logout(access_token):
    """Test user logout"""
    print("\n6. Testing logout...")

    response = requests.post(
        f"{BASE_URL}/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    print(f"Status Code: {response.status_code}")

    if response.status_code == 204:
        print("✓ Logout successful")
        return True
    else:
        print("✗ Logout failed")
        return False


def test_invalid_credentials():
    """Test login with invalid credentials"""
    print("\n7. Testing invalid credentials...")

    response = requests.post(
        f"{BASE_URL}/api/v1/auth/login",
        json={
            "email": "test@example.com",
            "password": "WrongPassword123"
        }
    )

    print(f"Status Code: {response.status_code}")

    if response.status_code == 401:
        print("✓ Invalid credentials handled correctly")
        return True
    else:
        print("✗ Invalid credentials not handled correctly")
        return False


def test_password_validation():
    """Test password validation"""
    print("\n8. Testing password validation...")

    response = requests.post(
        f"{BASE_URL}/api/v1/auth/register",
        json={
            "email": "weak@example.com",
            "password": "weak",
            "confirm_password": "weak",
            "name": "Weak Password User"
        }
    )

    print(f"Status Code: {response.status_code}")

    if response.status_code == 422:
        print("✓ Weak password rejected correctly")
        return True
    else:
        print("✗ Weak password validation failed")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("Authentication System Test Suite")
    print("=" * 60)

    # Test registration
    register_result = test_register()
    if not register_result:
        print("\n⚠ Skipping remaining tests (registration required)")
        return

    # Test login
    login_result = test_login()
    if not login_result:
        print("\n⚠ Skipping remaining tests (login required)")
        return

    access_token = login_result.get("access_token")
    refresh_token = login_result.get("refresh_token")

    # Test get profile
    test_get_profile(access_token)

    # Test update profile
    test_update_profile(access_token)

    # Test token refresh
    test_refresh_token(refresh_token)

    # Test logout
    test_logout(access_token)

    # Test error cases
    test_invalid_credentials()
    test_password_validation()

    print("\n" + "=" * 60)
    print("Test Suite Complete")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n✗ Error: Could not connect to server at", BASE_URL)
        print("Make sure the FastAPI server is running:")
        print("  cd fastapi-backend && uvicorn main:app --reload")
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
