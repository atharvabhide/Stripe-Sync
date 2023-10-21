import streamlit as st
import requests

OUTWARD_API_BASE_URL = "http://127.0.0.1:8080"

def init_vars():
    '''
    Initialize vars dict

    Returns:
        dict: vars dict
    '''
    vars = {
        "action": None,
        "create_button": None,
        "read_button": None,
        "read_customer_button": None,
        "update_button": None,
        "delete_button": None,
        "customer_id": None,
        "customer_name": None,
        "customer_email": None,
        "update_customer_id": None,
        "update_customer_name": None,
        "update_customer_email": None
    }
    return vars

def create_customer(name: str, email: str):
    '''
    Create a customer

    Args:
    -----
        name (str): Customer name
        email (str): Customer email

    Returns:
        requests.Response: Response object
    '''
    data = {"name": name, "email": email}
    response = requests.post(f"{OUTWARD_API_BASE_URL}/customers/", json=data)
    return response

def read_customers():
    '''
    Read all customers

    Returns:
        list: List of customers
    '''
    response = requests.get(f"{OUTWARD_API_BASE_URL}/customers/")
    return response.json()

def read_customer(customer_id: str):
    '''
    Read a customer

    Args:
    -----
        customer_id (str): Customer ID

    Returns:
        dict: Customer object
    '''
    response = requests.get(f"{OUTWARD_API_BASE_URL}/customers/{customer_id}")
    return response.json()

def update_customer(customer_id: str, name: str, email: str):
    '''
    Update a customer

    Args:
    -----
        customer_id (str): Customer ID
        name (str): Customer name
        email (str): Customer email

    Returns:
        requests.Response: Response object
    '''
    data = {"name": name, "email": email}
    response = requests.put(f"{OUTWARD_API_BASE_URL}/customers/{customer_id}", json=data)
    return response

def delete_customer(customer_id: str):
    '''
    Delete a customer

    Args:
    -----
        customer_id (str): Customer ID

    Returns:
        requests.Response: Response object
    '''
    response = requests.delete(f"{OUTWARD_API_BASE_URL}/customers/{customer_id}")
    return response

def handle_action(vars: dict):
    '''
    Handle action

    Args:
    -----
        vars (dict): vars dict
    '''
    if vars["action"] == "Create Customer" and vars["create_button"]:
        if vars["customer_name"] and vars["customer_email"]:
            response = create_customer(vars["customer_name"], vars["customer_email"])
            if response.status_code == 201:
                st.success("Customer created successfully")
            else:
                st.error("Error creating customer")

    if vars["action"] == "Read Customers" and vars["read_button"]:
        response = read_customers()
        st.subheader("Customers:")
        st.json(response)

    if vars["action"] == "Read Customer" and vars["read_customer_button"]:
        if vars["customer_id"]:
            response = read_customer(vars["customer_id"])
            if response.get("id"):
                st.subheader("Customer:")
                st.json(response)
            else:
                st.error("Customer not found")

    if vars["action"] == "Update Customer" and vars["update_button"]:
        if vars["update_customer_id"]:
            customer_name = read_customer(vars["update_customer_id"])["name"]
            customer_email = read_customer(vars["update_customer_id"])["email"]
            if not vars["update_customer_name"]:
                vars["update_customer_name"] = customer_name
            if not vars["update_customer_email"]:
                vars["update_customer_email"] = customer_email
            response = update_customer(vars["update_customer_id"], vars["update_customer_name"], vars["update_customer_email"])
            if response.status_code == 200:
                st.success("Customer updated successfully")
            else:
                st.error("Error updating customer")

    if vars["action"] == "Delete Customer" and vars["delete_button"]:
        if vars["delete_customer_id"]:
            response = delete_customer(vars["delete_customer_id"])
            if response.status_code == 204:
                st.success("Customer deleted successfully")
            else:
                st.error("Error deleting customer")

if __name__ == "__main__":
    st.title("Zenskar Outward Sync App")
    st.markdown("This app allows you to perform the outward sync i.e. migrating changes from local system to Stripe.")
    st.markdown("Please select an action from the sidebar to get started.")

    action = st.selectbox("Select Action:", ("Create Customer", "Read Customers", "Read Customer", "Update Customer", "Delete Customer"))
    vars = init_vars()

    if action == "Create Customer":
        st.subheader("Create Customer")
        vars["action"] = action
        vars["customer_name"] = st.text_input("Customer Name:")
        vars["customer_email"] = st.text_input("Customer Email:")
        vars["create_button"] = st.button("Create")

    if action == "Read Customers":
        st.subheader("Read Customers")
        vars["action"] = action
        vars["read_button"] = st.button("Read")

    if action == "Read Customer":
        st.subheader("Read Customer")
        vars["action"] = action
        vars["customer_id"] = st.text_input("Customer ID:")
        vars["read_customer_button"] = st.button("Read")

    if action == "Update Customer":
        st.subheader("Update Customer")
        vars["action"] = action
        vars["update_customer_id"] = st.text_input("Customer ID:")
        vars["update_customer_name"] = st.text_input("New Name:")
        vars["update_customer_email"] = st.text_input("New Email:")
        vars["update_button"] = st.button("Update")

    if action == "Delete Customer":
        st.subheader("Delete Customer")
        vars["action"] = action
        vars["delete_customer_id"] = st.text_input("Customer ID:")
        vars["delete_button"] = st.button("Delete")

    handle_action(vars)