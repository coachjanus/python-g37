import re

def test_register_success(client):
    resp = client.post('/auth/register', data={'username': 'newuser', 'password': 'Password1'}, follow_redirects=True)
    assert resp.status_code == 200
    assert b'Registration successful' in resp.data


def test_register_username_taken(client):
    client.post('/auth/register', data={'username': 'dupuser', 'password': 'Password1'}, follow_redirects=True)
    resp = client.post('/auth/register', data={'username': 'dupuser', 'password': 'Password1'}, follow_redirects=True)
    assert resp.status_code == 200
    assert b'Username not available' in resp.data


def test_register_password_policy(client):
    r1 = client.post('/auth/register', data={'username': 'weak1', 'password': 'short'}, follow_redirects=True)
    assert b'Password must be at least 8 characters long' in r1.data
    r2 = client.post('/auth/register', data={'username': 'weak2', 'password': 'Password'}, follow_redirects=True)
    assert b'Password must contain at least one digit' in r2.data
    r3 = client.post('/auth/register', data={'username': 'weak3', 'password': '12345678'}, follow_redirects=True)
    assert b'Password must contain at least one letter' in r3.data


def test_login_success_sets_session_and_redirects(client):
    client.post('/auth/register', data={'username': 'loginuser', 'password': 'Password1'}, follow_redirects=True)
    resp = client.post('/auth/login', data={'username': 'loginuser', 'password': 'Password1'}, follow_redirects=False)
    assert resp.status_code in (301, 302)
    assert '/staff' in resp.headers.get('Location', '')


def test_login_invalid_credentials_generic_error(client):
    client.post('/auth/register', data={'username': 'baduser', 'password': 'Password1'}, follow_redirects=True)
    resp = client.post('/auth/login', data={'username': 'baduser', 'password': 'wrongpass'}, follow_redirects=True)
    assert resp.status_code == 200
    assert b'Invalid username or password' in resp.data


def test_next_parameter_safe_redirect(client):
    client.post('/auth/register', data={'username': 'nextuser', 'password': 'Password1'}, follow_redirects=True)
    resp = client.post('/auth/login', data={'username': 'nextuser', 'password': 'Password1', 'next': '/staff'}, follow_redirects=False)
    assert resp.status_code in (301, 302)
    assert resp.headers['Location'].endswith('/staff')
    resp2 = client.post('/auth/login', data={'username': 'nextuser', 'password': 'Password1', 'next': 'https://evil.com'}, follow_redirects=False)
    assert resp2.status_code in (301, 302)
    assert 'evil.com' not in resp2.headers.get('Location', '')


def test_login_required_redirects_with_next(client):
    resp = client.get('/staff', follow_redirects=False)
    assert resp.status_code in (301, 302)
    loc = resp.headers['Location']
    assert loc.startswith('/auth/login')
    assert 'next=%2Fstaff' in loc or 'next=/staff' in loc


def test_rate_limiter_blocks_after_max_attempts(client):
    client.post('/auth/register', data={'username': 'rluser', 'password': 'Password1'}, follow_redirects=True)
    for _ in range(5):
        client.post('/auth/login', data={'username': 'rluser', 'password': 'wrongpass'}, follow_redirects=True)
    resp = client.post('/auth/login', data={'username': 'rluser', 'password': 'wrongpass'}, follow_redirects=True)
    assert b'Too many login attempts' in resp.data


def test_logout_get_and_post(client):
    client.post('/auth/register', data={'username': 'outuser', 'password': 'Password1'}, follow_redirects=True)
    client.post('/auth/login', data={'username': 'outuser', 'password': 'Password1'}, follow_redirects=False)
    rget = client.get('/auth/logout', follow_redirects=False)
    assert rget.status_code in (301, 302)
    rpost = client.post('/auth/logout', follow_redirects=False)
    assert rpost.status_code in (301, 302)
