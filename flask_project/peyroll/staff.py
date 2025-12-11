# flask_project/peyroll/staff.py

"""Staff management blueprint: list, create, update, and delete employees.

Provides routes and helpers for managing employees. Uses safe input parsing,
foreign key validation, and consistent user feedback via flash messages.
All mutating routes require authentication.
"""

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    session,
)
from werkzeug.exceptions import abort

from .database import get_db
from .auth import login_required

bp = Blueprint("staff", __name__)

# Helpers for safe parsing and validation

def _to_int(value, default=None):
    """Safely convert a value to int.

    Returns default if the value is None, empty, or not an integer.
    """
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _to_float_nonneg(value, default=None):
    """Safely convert a value to a non-negative float.

    Returns default if the value is invalid or negative.
    """
    try:
        v = float(value)
        return v if v >= 0 else default
    except (TypeError, ValueError):
        return default


def _fetch_departments_roles(db):
    """Fetch lists of departments and roles for form selects."""
    departments = db.execute('SELECT id, department_name FROM departments').fetchall()
    roles = db.execute('SELECT id, role_name FROM roles').fetchall()
    return departments, roles


def _validate_fk(db, department_id, role_id):
    """Validate that provided foreign keys exist.

    Returns an error message string when invalid; otherwise None.
    """
    dep = db.execute('SELECT id FROM departments WHERE id = ?', (department_id,)).fetchone()
    if dep is None:
        return 'Selected department does not exist.'
    role = db.execute('SELECT id FROM roles WHERE id = ?', (role_id,)).fetchone()
    if role is None:
        return 'Selected role does not exist.'
    return None

@bp.route("/staff")
@bp.route("/staff/index")
# @login_required
def index():
    """List employees with joined department and role metadata."""
    db = get_db()
    employees = db.execute(
        'SELECT emp.id emp_id, employee_name, department_id, department_name, join_date, role_id, role_name'
        ' FROM employee emp JOIN roles r ON emp.role_id = r.id'
        ' JOIN departments d ON emp.department_id = d.id'
        ' ORDER BY department_id ASC'
    ).fetchall()
    return render_template("staff/index.html", employees=employees)


@bp.route("/staff/create", methods=("GET", "POST"))
@login_required
def create():
    """Create a new employee.

    Validates input, ensures foreign keys exist, and handles DB errors.
    Renders the form with errors on validation failure.
    """
    db = get_db()
    departments, roles = _fetch_departments_roles(db)

    if request.method == "POST":
        employee_name = (request.form.get("employee_name") or "").strip()
        department_id = _to_int(request.form.get("department_id"))
        role_id = _to_int(request.form.get("role_id"))
        weekly_salary = _to_float_nonneg(request.form.get("weekly_salary"), default=0.0)
        commission_per_sale = _to_float_nonneg(request.form.get("commission_per_sale"), default=0.0)
        hour_rate = _to_float_nonneg(request.form.get("hour_rate"), default=0.0)

        error = None

        if not employee_name:
            error = "Employee name is required."
        elif department_id is None or role_id is None:
            error = "Department and role are required."
        else:
            # Validate foreign keys exist
            error = _validate_fk(db, department_id, role_id)

        if error:
            flash(error, category="error")
            return render_template("staff/create.html", roles=roles, departments=departments, csrf_token=session.get('csrf_token'))

        try:
            db.execute(
                "INSERT INTO employee(employee_name, weekly_salary, commission_per_sale, hour_rate, role_id, department_id) VALUES (?, ?, ?, ?, ?, ?)",
                (employee_name, weekly_salary or 0.0, commission_per_sale or 0.0, hour_rate or 0.0, role_id, department_id),
            )
            db.commit()
        except Exception:
            current_app.logger.exception("Failed to create employee")
            flash("Failed to create employee.", category="error")
            return render_template("staff/create.html", roles=roles, departments=departments, csrf_token=session.get('csrf_token'))

        current_app.logger.info(f"New employee {employee_name} was hired")
        flash(f"New employee {employee_name} was hired", category="success")
        return redirect(url_for("staff.index"))

    return render_template("staff/create.html", roles=roles, departments=departments, csrf_token=session.get('csrf_token'))

def get_employee(id):
    """Return an employee by id or abort with 404 if not found."""
    employee = get_db().execute(
        'SELECT * FROM employee WHERE id = ?', (id,)
    ).fetchone()

    if employee is None:
        current_app.logger.warning(f"Employee id {id} not found")
        abort(404, f"Employee id: {id} doesn't exist.")

    return employee


@bp.route('/staff/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    """Update an existing employee.

    Performs the same validations as create() and persists changes.
    """
    employee = get_employee(id)
    db = get_db()
    departments, roles = _fetch_departments_roles(db)

    if request.method == 'POST':
        employee_name = (request.form.get("employee_name") or "").strip()
        department_id = _to_int(request.form.get("department_id"))
        role_id = _to_int(request.form.get("role_id"))
        weekly_salary = _to_float_nonneg(request.form.get("weekly_salary"), default=0.0)
        commission_per_sale = _to_float_nonneg(request.form.get("commission_per_sale"), default=0.0)
        hour_rate = _to_float_nonneg(request.form.get("hour_rate"), default=0.0)

        error = None
        if not employee_name:
            error = 'Employee name is required.'
        elif department_id is None or role_id is None:
            error = 'Department and role are required.'
        else:
            error = _validate_fk(db, department_id, role_id)

        if error is not None:
            flash(error, category='error')
            return render_template("staff/update.html", roles=roles, departments=departments, employee=employee, csrf_token=session.get('csrf_token'))

        try:
            db.execute(
                'UPDATE employee SET employee_name = ?, department_id = ?, role_id = ?, weekly_salary = ?, commission_per_sale = ?, hour_rate = ? WHERE id = ?',
                (employee_name, department_id, role_id, weekly_salary or 0.0, commission_per_sale or 0.0, hour_rate or 0.0, id)
            )
            db.commit()
        except Exception:
            current_app.logger.exception("Failed to update employee %s", id)
            flash('Failed to update employee.', category='error')
            return render_template("staff/update.html", roles=roles, departments=departments, employee=employee, csrf_token=session.get('csrf_token'))

        flash('Employee updated successfully.', category='success')
        return redirect(url_for('staff.index'))

    return render_template("staff/update.html", roles=roles, departments=departments, employee=employee, csrf_token=session.get('csrf_token'))


@bp.route('/staff/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    """Delete an employee by id with basic error handling."""
    get_employee(id)
    db = get_db()
    try:
        db.execute('DELETE FROM employee WHERE id = ?', (id,))
        db.commit()
    except Exception:
        current_app.logger.exception("Failed to delete employee %s", id)
        flash('Failed to delete employee.', category='error')
        return redirect(url_for('staff.index'))
    flash('Employee deleted successfully.', category='success')
    return redirect(url_for('staff.index'))
