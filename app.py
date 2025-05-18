# app.py (Streamlit UI)
import streamlit as st
from bank_module import acc_hold, create_account, check_credentials

st.set_page_config(page_title="Banking Simulator", layout="centered")
st.title("🏦 Banking Simulator")

if 'user' not in st.session_state:
    st.session_state.user = None

# Login / Signup View
if st.session_state.user is None:
    tab1, tab2 = st.tabs(["Login", "Create Account"])

    with tab1:
        st.subheader("🔐 Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if check_credentials(username, password):
                st.session_state.user = username
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid credentials")

    with tab2:
        st.subheader("📝 Create Account")
        fname = st.text_input("First Name")
        sname = st.text_input("Last Name")
        age = st.number_input("Age", min_value=18, step=1)
        deposit = st.number_input("Initial Deposit", min_value=1)
        new_username = st.text_input("New Username")
        new_password = st.text_input("Password", type="password", key="create_pw")
        pin = st.text_input("Transaction PIN (4-digit)", key="create_pin")
        confirm_pin = st.text_input("Confirm PIN", type="password", key="confirm_pin")

        if st.button("Create Account"):
            if pin != confirm_pin:
                st.error("PIN mismatch")
            elif len(pin) != 4 or not pin.isdigit():
                st.error("PIN must be 4 digits")
            else:
                success, msg = create_account(fname, sname, age, deposit, new_username, new_password, pin)
                if success:
                    st.success(msg)
                else:
                    st.error(msg)

# Logged-in View
else:
    acc = acc_hold(st.session_state.user)
    st.sidebar.success(f"Logged in as {acc.fn} {acc.sn}")
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

    option = st.selectbox("Choose an action", ["View Balance", "Deposit", "Withdraw", "Transfer", "View Details", "Transaction History"])

    if option == "View Balance":
        st.subheader("💰 Balance Inquiry")
        st.info(acc.get_inquiry())

    elif option == "Deposit":
        st.subheader("📥 Deposit")
        amt = st.number_input("Amount to Deposit", min_value=1)
        if st.button("Confirm Deposit"):
            acc.deposit(amt)
            st.success(f"Deposited Rs {amt}")

    elif option == "Withdraw":
        st.subheader("📤 Withdraw")
        amt = st.number_input("Amount to Withdraw", min_value=1)
        if st.button("Confirm Withdrawal"):
            success, msg = acc.withdraw(amt)
            if success:
                st.success(msg)
            else:
                st.error(msg)

    elif option == "Transfer":
        st.subheader("🔄 Transfer Funds")
        recipient = st.text_input("Recipient Username")
        amt = st.number_input("Amount to Transfer", min_value=1)
        if st.button("Confirm Transfer"):
            success, msg = acc.transfer(recipient, amt)
            if success:
                st.success(msg)
            else:
                st.error(msg)

    elif option == "View Details":
        st.subheader("👤 User Details")
        st.code(acc.get_details())

    elif option == "Transaction History":
        st.subheader("📜 Transaction History")
        st.text(acc.get_history())
