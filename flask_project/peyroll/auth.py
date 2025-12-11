"""Authentication blueprint: registration, login, logout, and session helpers.

Includes:
- Session-based user loading
- CSRF token scaffolding
- Basic password policy validation
- Simple rate limiting for login attempts
"""
import functools
import logging
import sqlite3
import secrets
import time
import hmac
from urllib.parse import urlparse
from typing import Optional

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from .database import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

# Rate limiter configuration (seconds, attempts)
RATE_LIMIT_WINDOW = 600  # 10 minutes
RATE_LIMIT_MAX_ATTEMPTS = 5

def login_required(view):
    """Redirect unauthenticated users to the login page, preserving a safe 'next' URL.

    Wraps the view to enforce authentication using g.user. If not authenticated,
    redirects to auth.login with a safe next parameter.
    functools.wraps decorator in Python is used when writing decorators to preserve the original function's metadata on the wrapper function. 
    """
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            next_param = request.full_path if request.query_string else request.path
            # Remove trailing '?' if present
            if next_param.endswith('?'):
                next_param = next_param[:-1]
            return redirect(url_for('auth.login', next=next_param))
        return view(*args, **kwargs)
    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    """Load the current user into g.user from session['user_id'].

    Clears the session if the referenced user no longer exists, preventing stale sessions.
    """
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
        if user is None:
            # Clear potentially stale session user_id
            session.clear()
            g.user = None
        else:
            g.user = user


@bp.before_app_request
def ensure_csrf_token():
    """Ensure a CSRF token exists in the session for form submissions.

    Note: This scaffolding expects templates to include the token.
    """
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_urlsafe(32)

def _is_safe_next(next_url: str) -> bool:
    """Return True if next_url is a safe internal relative path.

    Disallows absolute URLs and protocol-relative paths; only allows paths starting with '/'.
    """
    if not next_url:
        return False
    parsed = urlparse(next_url)
    if parsed.scheme or parsed.netloc:
        return False
    return parsed.path.startswith('/')

def _validate_password(password: str) -> Optional[str]:
    """Validate password against a basic policy.

    Policy:
    - Minimum 8 characters
    - At least one letter and one digit
    - Maximum length of 128

    Returns:
        str | None: Error message if invalid; otherwise None.
    """
    # Basic policy: min 8 chars, at least one letter and one digit, reasonable max length
    if len(password) < 8:
        return 'Password must be at least 8 characters long.'
    if not any(c.isalpha() for c in password):
        return 'Password must contain at least one letter.'
    if not any(c.isdigit() for c in password):
        return 'Password must contain at least one digit.'
    if len(password) > 128:
        return 'Password must be at most 128 characters long.'
    return None


@bp.route('/register', methods=('GET', 'POST'))
def register():
    """Register a new user account.

    On POST: validates input, enforces password policy, hashes password,
    and attempts to create a new user. On success, flashes a message and redirects to login.
    On failure, flashes an error and re-renders the form.

    Returns:
        Response: Registration form or redirect to login.
    """
    if request.method == 'POST':
        token_form = request.form.get('csrf_token')
        token_session = session.get('csrf_token')
        if not token_form or not token_session or not hmac.compare_digest(token_form, token_session):
            flash('Invalid CSRF token. Please try again.', 'error')
            return render_template('auth/register.html', csrf_token=session.get('csrf_token'))
        username = (request.form.get('username') or '').strip().lower()
        password = request.form.get('password') or ''
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        else:
            pw_err = _validate_password(password)
            if pw_err:
                error = pw_err
            else:
                confirm = request.form.get('confirm_password')
                if confirm is not None and confirm != password:
                    error = 'Passwords do not match.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except sqlite3.IntegrityError:
                error = "Username not available."
            else:
                flash('Registration successful. Please log in.', 'success')
                return redirect(url_for("auth.login"))

        if error:
            flash(error, 'error')

    return render_template('auth/register.html', csrf_token=session.get('csrf_token'))


@bp.route('/login', methods=('GET', 'POST'))
def login():
    """Authenticate a user and start a session with basic rate limiting.

    On POST: validates credentials, enforces a session-based rate limit, and logs in
    the user on success. Resets rate limiter on success. Supports an optional 'next'
    parameter for safe redirection.

    Returns:
        Response: Login form (with errors if any) or redirect to the next page or staff index.
    """
    next_param = request.args.get('next') or request.form.get('next')
    if request.method == 'POST':
        token_form = request.form.get('csrf_token')
        token_session = session.get('csrf_token')
        if not token_form or not token_session or not hmac.compare_digest(token_form, token_session):
            flash('Invalid CSRF token. Please try again.', 'error')
            return render_template('auth/login.html', next=next_param, csrf_token=session.get('csrf_token'))
        # Simple session-based rate limiting (scaffolding; consider Flask-Limiter)
        now = int(time.time())
        attempts = session.get('login_attempts', 0)
        window_start = session.get('login_window_start', now)
        if now - window_start > RATE_LIMIT_WINDOW:
            attempts = 0
            window_start = now
        if attempts >= RATE_LIMIT_MAX_ATTEMPTS:
            logging.getLogger(__name__).warning(
                "Login rate limit exceeded from IP %s; attempts=%s", request.remote_addr, attempts
            )
            flash('Too many login attempts. Try again later.', 'error')
            return render_template('auth/login.html', next=next_param, csrf_token=session.get('csrf_token'))
        username = (request.form.get('username') or '').strip().lower()
        password = request.form.get('password') or ''
        db = get_db()
        error = None

        if not username or not password:
            error = 'Invalid username or password.'
        else:
            user = db.execute(
                'SELECT * FROM user WHERE username = ?', (username,)
            ).fetchone()
            if user is None or not check_password_hash(user['password'], password):
                error = 'Invalid username or password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            # Reset login rate limiter on success
            session['login_attempts'] = 0
            session['login_window_start'] = int(time.time())
            flash('Logged in successfully.', 'success')
            # Redirect to next if safe
            if _is_safe_next(next_param):
                return redirect(next_param)
            return redirect(url_for('staff.index'))

        # Increment rate limiter counters on failure
        attempts += 1
        session['login_attempts'] = attempts
        session['login_window_start'] = window_start
        flash(error, 'error')

    return render_template('auth/login.html', next=next_param, csrf_token=session.get('csrf_token'))

# Note: logout supports GET and POST; prefer POST with CSRF token in production.

@bp.route('/logout', methods=('GET', 'POST'))
def logout():
    """Log out the current user by clearing the session.

    For GET requests, flashes a warning suggesting POST for better CSRF protection.
    Redirects to the home page.
    """
    if request.method == 'POST':
        token_form = request.form.get('csrf_token')
        token_session = session.get('csrf_token')
        if not token_form or not token_session or not hmac.compare_digest(token_form, token_session):
            flash('Invalid CSRF token. Logout aborted.', 'error')
            return redirect(url_for('pages.home'))
    session.clear()
    if request.method == 'GET':
        flash('Logged out. For better security, use POST logout with CSRF.', 'warning')
    return redirect(url_for('pages.home'))
