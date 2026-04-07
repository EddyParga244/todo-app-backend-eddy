from flask_jwt_extended import create_access_token

# Register tests
def test_register_success(client):
    response = client.post('/api/auth/register', json={
        "email": "test@test.com",
        "password": "Test123!"
    })
    assert response.status_code == 201
    
def test_register_duplicate_email(client):
    client.post('/api/auth/register', json={
        "email": "test@test.com",
        "password": "Test123!"
    })
    response = client.post('/api/auth/register', json={
        "email": "test@test.com",
        "password": "Test123!"
    })
    assert response.status_code == 409

def test_register_no_email(client):
    response = client.post('/api/auth/register', json={
        "email": "",
        "password": "Test123!"
    })
    assert response.status_code == 400

def test_register_invalid_password(client):
    response = client.post('/api/auth/register', json={
        "email": "test@test.com",
        "password": "123"
    })
    assert response.status_code == 400

# Login tests
def test_login_success(client):
    client.post('/api/auth/register', json={
        "email": "test@test.com",
        "password": "Test123!"
    })
    response = client.post('/api/auth/login', json={
        "email": "test@test.com",
        "password": "Test123!"
    })
    data = response.get_json()
    token = data['access_token']
    assert response.status_code == 200 and token is not None

def test_login_without_email_and_password(client):
    client.post('/api/auth/register', json={
        "email": "test@test.com",
        "password": "Test123!"
    })
    response = client.post('/api/auth/login', json={
        "email": "",
        "password": ""
    })
    assert response.status_code == 400

def test_login_without_email(client):
    client.post('/api/auth/register', json={
        "email": "test@test.com",
        "password": "Test123!"
    })
    response = client.post('/api/auth/login', json={
        "email": "",
        "password": "Test123!"
    })
    assert response.status_code == 400

def test_login_without_password(client):
    client.post('/api/auth/register', json={
        "email": "test@test.com",
        "password": "Test123!"
    })
    response = client.post('/api/auth/login', json={
        "email": "test@test.com",
        "password": ""
    })
    assert response.status_code == 400

def test_login_email_not_found(client):
    response = client.post('/api/auth/login', json={
        "email": "test@test.com",
        "password": "Test123!"
    })
    assert response.status_code == 404

def test_login_wrong_password(client):
    client.post('/api/auth/register', json={
        "email": "test@test.com",
        "password": "Test123!"
    })
    response = client.post('/api/auth/login', json={
        "email": "test@test.com",
        "password": "SuperTest345!"
    })
    assert response.status_code == 401

def test_login_wrong_schema(client):
    client.post('/api/auth/register', json={
        "email": "test@test.com",
        "password": "test"
    })
    response = client.post('/api/auth/login', json={
        "email": "test@test.com",
        "password": "test"
    })
    assert response.status_code == 400

# Logout tests
def test_logout_success(client):
    client.post('/api/auth/register', json={
        "email": "test@test.com",
        "password": "Test123!"
    })
    login_response = client.post('/api/auth/login', json={
        "email": "test@test.com",
        "password": "Test123!"
    })
    data = login_response.get_json()
    token = data['access_token']
    cookies = login_response.headers.getlist('Set-Cookie')
    response = client.delete('/api/auth/logout', headers={
        'Cookie: ': '; '.join(cookies),
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 200

def test_logout_without_token(client):
    client.post('/api/auth/register', json={
        "email": "test@test.com",
        "password": "Test123!"
    })
    login_response = client.post('/api/auth/login', json={
        "email": "test@test.com",
        "password": "Test123!"
    })
    cookies = login_response.headers.getlist('Set-Cookie')
    response = client.delete('/api/auth/logout', headers={
        'Cookie: ': '; '.join(cookies),
    })
    assert response.status_code == 401

def test_logout_without_cookie(app, client):
    with app.app_context():
        token = create_access_token(identity="test@test.com")
    response = client.delete('/api/auth/logout', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 400

# Change password tests
def test_change_password_success(client):
    client.post('/api/auth/register', json={
        "email": "test@test.com",
        "password": "Test123!"
    })
    login_response = client.post('/api/auth/login', json={
        "email": "test@test.com",
        "password": "Test123!"
    })
    data = login_response.get_json()
    token = data['access_token']
    cookies = login_response.headers.getlist('Set-Cookie')
    response = client.patch('/api/auth/change-password', headers={
        'Cookie: ': '; '.join(cookies),
        'Authorization': f'Bearer {token}'
    }, json={
        "current_password": "Test123!",
        "new_password": "Test456!"
    })
    assert response.status_code == 200

def test_change_password_wrong_current_password(client):
    client.post('/api/auth/register', json={
        "email": "test@test.com",
        "password": "Test123!"
    })
    login_response = client.post('/api/auth/login', json={
        "email": "test@test.com",
        "password": "Test123!"
    })
    data = login_response.get_json()
    token = data['access_token']
    cookies = login_response.headers.getlist('Set-Cookie')
    response = client.patch('/api/auth/change-password', headers={
        'Cookie: ': '; '.join(cookies),
        'Authorization': f'Bearer {token}'
    }, json={
        "current_password": "TestAbc!",
        "new_password": "Test456!"
    })
    assert response.status_code == 400

def test_change_password_without_token(client):
    client.post('/api/auth/register', json={
        "email": "test@test.com",
        "password": "Test123!"
    })
    login_response = client.post('/api/auth/login', json={
        "email": "test@test.com",
        "password": "Test123!"
    })
    cookies = login_response.headers.getlist('Set-Cookie')
    response = client.patch('/api/auth/change-password', headers={
        'Cookie: ': '; '.join(cookies),
    }, json={
        "current_password": "Test123!",
        "new_password": "Test456!"
    })
    assert response.status_code == 401

def test_change_password_wrong_current_password_schema(client):
    client.post('/api/auth/register', json={
        "email": "test@test.com",
        "password": "Test123!"
    })
    login_response = client.post('/api/auth/login', json={
        "email": "test@test.com",
        "password": "Test123!"
    })
    data = login_response.get_json()
    token = data['access_token']
    cookies = login_response.headers.getlist('Set-Cookie')
    response = client.patch('/api/auth/change-password', headers={
        'Cookie: ': '; '.join(cookies),
        'Authorization': f'Bearer {token}'
    }, json={
        "current_password": "Test",
        "new_password": "Test456!"
    })
    assert response.status_code == 400

# Refresh tests
def test_refresh_success(client):
    client.post('/api/auth/register', json={
        "email": "test@test.com",
        "password": "Test123!"
    })
    login_response = client.post('/api/auth/login', json={
        "email": "test@test.com",
        "password": "Test123!"
    })
    cookies = login_response.headers.getlist('Set-Cookie')
    response = client.post('/api/auth/refresh', headers={
        'Cookie: ': '; '.join(cookies)
    })
    new_data = response.get_json()
    new_token = new_data['access_token']
    assert response.status_code == 200 and new_token is not None

def test_refresh_token_not_found(client):
    response = client.post('/api/auth/refresh')
    assert response.status_code == 401

# Delete account tests
def test_delete_account_success(client):
    client.post('/api/auth/register', json={
        "email": "test@test.com",
        "password": "Test123!"
    })
    login_response = client.post('/api/auth/login', json={
        "email": "test@test.com",
        "password": "Test123!"
    })
    data = login_response.get_json()
    token = data['access_token']
    cookies = login_response.headers.getlist('Set-Cookie')
    response = client.delete('/api/auth/delete', headers={
        'Cookie: ': '; '.join(cookies),
        'Authorization': f'Bearer {token}'
    }, json={
        "password": "Test123!"
    })
    assert response.status_code == 200

def test_delete_account_wrong_password(client):
    client.post('/api/auth/register', json={
        "email": "test@test.com",
        "password": "Test123!"
    })
    login_response = client.post('/api/auth/login', json={
        "email": "test@test.com",
        "password": "Test123!"
    })
    data = login_response.get_json()
    token = data['access_token']
    cookies = login_response.headers.getlist('Set-Cookie')
    response = client.delete('/api/auth/delete', headers={
        'Cookie: ': '; '.join(cookies),
        'Authorization': f'Bearer {token}'
    }, json={
        "password": "Test345!"
    })
    assert response.status_code == 401

def test_delete_account_without_token(client):
    client.post('/api/auth/register', json={
        "email": "test@test.com",
        "password": "Test123!"
    })
    login_response = client.post('/api/auth/login', json={
        "email": "test@test.com",
        "password": "Test123!"
    })
    cookies = login_response.headers.getlist('Set-Cookie')
    response = client.delete('/api/auth/delete', headers={
        'Cookie: ': '; '.join(cookies),
    }, json={
        "password": "Test123!"
    })
    assert response.status_code == 401
