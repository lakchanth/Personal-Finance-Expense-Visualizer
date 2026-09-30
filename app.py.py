import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page Configuration
st.set_page_config(page_title="Expense Visualizer", page_icon="💰", layout="centered")

st.title("💳 Personal Finance & Smart Expense Visualizer")
st.write("Track your daily spending and visualize your budget instantly.")

# File uploader to allow custom CSV uploads
uploaded_file = st.file_uploader("Upload your own expenses CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    # Fallback to the default sample dataset if none uploaded
    try:
        df = pd.read_csv("expenses.csv")
        st.info("Currently displaying default sample data. Upload your own CSV above to track personal expenses.")
    except FileNotFoundError:
        st.error("Could not find 'expenses.csv'. Please make sure it is in the same folder as app.py.")
        st.stop()

# Show raw data toggle
if st.checkbox("Show raw expense data"):
    st.subheader("Raw Data")
    st.dataframe(df)

# Ensure Amount is numeric
df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')

# Key Metrics Summary
total_spent = df['Amount'].sum()
total_categories = df['Category'].nunique()

col1, col2 = st.columns(2)
col1.metric("Total Spending", f"${total_spent:.2f}")
col2.metric("Expense Categories", total_categories)

st.divider()

# Group data by Category
category_totals = df.groupby('Category')['Amount'].sum().reset_index()

# Visualizations layout
st.subheader("📊 Spending Breakdown")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# 1. Pie Chart
ax1.pie(category_totals['Amount'], labels=category_totals['Category'], autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
ax1.set_title("Spending Share by Category")

# 2. Bar Chart
ax2.bar(category_totals['Category'], category_totals['Amount'], color='skyblue')
ax2.set_title("Total Amount per Category")
ax2.set_xlabel("Category")
ax2.set_ylabel("Amount ($)")
plt.xticks(rotation=45)

st.pyplot(fig)