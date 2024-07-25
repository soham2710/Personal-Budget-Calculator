import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Initialize session state to store income and expense data
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=['Date', 'Type', 'Category', 'Amount'])

# Title of the application
st.title('Personal Budget Tracker')

# Form to add income and expenses
with st.form(key='income_expense_form'):
    date = st.date_input('Date')
    transaction_type = st.selectbox('Type', ['Income', 'Expense'])
    category = st.selectbox('Category', ['Salary', 'Business', 'Food', 'Rent', 'Entertainment', 'Other'])
    amount = st.number_input('Amount', min_value=0.0, format="%.2f")
    submit_button = st.form_submit_button(label='Add')

    if submit_button:
        new_data = pd.DataFrame([[date, transaction_type, category, amount]], 
                                columns=['Date', 'Type', 'Category', 'Amount'])
        st.session_state.data = pd.concat([st.session_state.data, new_data], ignore_index=True)

# Display the data
st.subheader('Transaction Data')
st.dataframe(st.session_state.data)

# Calculate total income, total expense, and balance
total_income = st.session_state.data[st.session_state.data['Type'] == 'Income']['Amount'].sum()
total_expense = st.session_state.data[st.session_state.data['Type'] == 'Expense']['Amount'].sum()
balance = total_income - total_expense

st.subheader('Summary')
st.write(f"Total Income: ${total_income:.2f}")
st.write(f"Total Expense: ${total_expense:.2f}")
st.write(f"Balance: ${balance:.2f}")

# Visualize monthly spending with charts
if not st.session_state.data.empty:
    st.subheader('Monthly Spending')
    
    try:
        st.session_state.data['Date'] = pd.to_datetime(st.session_state.data['Date'])
        st.session_state.data['Month'] = st.session_state.data['Date'].dt.to_period('M')
        monthly_expense = st.session_state.data[st.session_state.data['Type'] == 'Expense'].groupby('Month')['Amount'].sum()

        fig, ax = plt.subplots()
        monthly_expense.plot(kind='bar', ax=ax)
        ax.set_title('Monthly Expense')
        ax.set_xlabel('Month')
        ax.set_ylabel('Amount')
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Error while plotting: {e}")
        
