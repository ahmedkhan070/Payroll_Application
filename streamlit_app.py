import streamlit as st
import pandas as pd

st.set_page_config(page_title="Payroll Management System", layout="wide")

# -------------------------
# Hardcoded Users
# -------------------------
USERS = {
    "admin": {
        "password": "admin123",
        "role": "Admin"
    },
    "hr": {
        "password": "hr123",
        "role": "HR Officer"
    },
    "payroll": {
        "password": "pay123",
        "role": "Payroll Officer"
    },
    "employee": {
        "password": "emp123",
        "role": "Employee"
    }
}

# -------------------------
# Session Storage
# -------------------------
if "employees" not in st.session_state:
    st.session_state.employees = [
        {
            "ID": 1,
            "Name": "Ali",
            "Department": "IT",
            "Designation": "Developer",
            "Salary": 50000
        },
        {
            "ID": 2,
            "Name": "Sara",
            "Department": "HR",
            "Designation": "HR Officer",
            "Salary": 45000
        }
    ]

if "attendance" not in st.session_state:
    st.session_state.attendance = []

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# -------------------------
# Login
# -------------------------
def login():

    st.title("Payroll Management System")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if username in USERS and USERS[username]["password"] == password:

            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = USERS[username]["role"]

            st.rerun()

        else:
            st.error("Invalid Credentials")


# -------------------------
# Employee Management
# -------------------------
def employee_management():

    st.header("Employee Management")

    df = pd.DataFrame(st.session_state.employees)
    st.dataframe(df, use_container_width=True)

    st.subheader("Add Employee")

    with st.form("add_employee"):

        emp_id = st.number_input("Employee ID", min_value=1)
        name = st.text_input("Name")
        dept = st.text_input("Department")
        desig = st.text_input("Designation")
        salary = st.number_input("Salary", min_value=0)

        submit = st.form_submit_button("Add Employee")

        if submit:

            st.session_state.employees.append({
                "ID": int(emp_id),
                "Name": name,
                "Department": dept,
                "Designation": desig,
                "Salary": salary
            })

            st.success("Employee Added Successfully")


# -------------------------
# Attendance
# -------------------------
def attendance_management():

    st.header("Attendance Management")

    employee_names = [
        emp["Name"]
        for emp in st.session_state.employees
    ]

    employee = st.selectbox(
        "Employee",
        employee_names
    )

    status = st.selectbox(
        "Status",
        ["Present", "Absent", "On Leave"]
    )

    if st.button("Save Attendance"):

        st.session_state.attendance.append({
            "Employee": employee,
            "Status": status
        })

        st.success("Attendance Saved")

    if len(st.session_state.attendance) > 0:

        st.subheader("Attendance Records")

        st.dataframe(
            pd.DataFrame(st.session_state.attendance),
            use_container_width=True
        )


# -------------------------
# Payroll
# -------------------------
def payroll_processing():

    st.header("Payroll Processing")

    payroll_data = []

    for emp in st.session_state.employees:

        basic = emp["Salary"]

        house_allowance = basic * 0.10
        medical_allowance = basic * 0.05

        gross = (
            basic +
            house_allowance +
            medical_allowance
        )

        tax = gross * 0.05

        net_salary = gross - tax

        payroll_data.append({
            "Employee": emp["Name"],
            "Basic Salary": basic,
            "Gross Salary": gross,
            "Tax": tax,
            "Net Salary": net_salary
        })

    payroll_df = pd.DataFrame(payroll_data)

    st.dataframe(
        payroll_df,
        use_container_width=True
    )

    st.metric(
        "Total Payroll",
        f"{payroll_df['Net Salary'].sum():,.0f}"
    )


# -------------------------
# Reports
# -------------------------
def reports():

    st.header("Payroll Report")

    total_employees = len(
        st.session_state.employees
    )

    total_salary = sum(
        emp["Salary"]
        for emp in st.session_state.employees
    )

    st.metric(
        "Total Employees",
        total_employees
    )

    st.metric(
        "Total Basic Salaries",
        f"{total_salary:,.0f}"
    )


# -------------------------
# Employee Portal
# -------------------------
def employee_portal():

    st.header("Employee Self Service")

    employee = st.session_state.employees[0]

    st.write("### Profile")

    st.write(
        f"Name: {employee['Name']}"
    )

    st.write(
        f"Department: {employee['Department']}"
    )

    st.write(
        f"Designation: {employee['Designation']}"
    )

    st.write(
        f"Salary: {employee['Salary']}"
    )

    st.write("### Attendance")

    if len(st.session_state.attendance) > 0:

        df = pd.DataFrame(
            st.session_state.attendance
        )

        st.dataframe(df)

    else:
        st.info("No attendance records")


# -------------------------
# Main App
# -------------------------
if not st.session_state.logged_in:

    login()

else:

    st.sidebar.title("Menu")

    st.sidebar.write(
        f"User: {st.session_state.username}"
    )

    st.sidebar.write(
        f"Role: {st.session_state.role}"
    )

    if st.sidebar.button("Logout"):

        st.session_state.logged_in = False
        st.rerun()

    role = st.session_state.role

    st.title("Payroll Dashboard")

    if role == "Admin":

        employee_management()
        attendance_management()
        payroll_processing()
        reports()

    elif role == "HR Officer":

        employee_management()
        attendance_management()

    elif role == "Payroll Officer":

        payroll_processing()
        reports()

    elif role == "Employee":

        employee_portal()
