import streamlit as st

# Page Configuration
st.set_page_config(page_title="SME Tax Calculator", layout="wide", initial_sidebar_state="expanded")

# Main Title
st.title("🇪🇬 SME Tax Calculator & Planner")
st.markdown("### Automated Tax Model for Egyptian SMEs")
st.info("This tool calculates taxes based on Law 152/2020 (Simplified) and Law 91/2005 (General).")

# --- Sidebar: Financial Data Inputs ---
st.sidebar.header("1️⃣ Financial Data Entry")

# Input: Annual Turnover
turnover = st.sidebar.number_input(
    "Annual Turnover (Gross Revenue)", 
    min_value=0.0, 
    value=1500000.0, 
    step=10000.0,
    help="Total income from all sources before deductions."
)

# Input: Operating Expenses
expenses = st.sidebar.number_input(
    "Operating Expenses", 
    min_value=0.0, 
    value=900000.0, 
    step=10000.0,
    help="Deductible expenses like rent, salaries, utilities, etc."
)

# Input: Business Activity
activity = st.sidebar.selectbox("Business Sector", ["Trading", "Manufacturing", "Services", "Professional"])

# --- Tax Logic Engines ---

def calc_simplified_tax(rev):
    """
    Calculates Presumptive Tax based on Law 152/2020 thresholds.
    """
    if rev < 250000:
        return 1000, "Fixed Amount (Turnover < 250k)"
    elif rev < 500000:
        return 2500, "Fixed Amount (250k - 500k)"
    elif rev < 1000000:
        return 5000, "Fixed Amount (500k - 1M)"
    elif rev < 2000000:
        return rev * 0.005, "Rate 0.50% (1M - 2M)"
    elif rev < 3000000:
        return rev * 0.0075, "Rate 0.75% (2M - 3M)"
    elif rev <= 10000000:
        return rev * 0.01, "Rate 1.00% (3M - 10M)"
    else:
        return None, "Not Applicable (> 10M EGP)"

def calc_general_tax(rev, exp):
    """
    Calculates Corporate Income Tax (CIT) based on Law 91/2005.
    Formula: (Revenue - Expenses) * 22.5%
    """
    net_profit = rev - exp
    tax_amount = max(0, net_profit * 0.225)  # 22.5% Corporate Tax Rate
    return net_profit, tax_amount

# Perform Calculations
simple_tax_val, simple_desc = calc_simplified_tax(turnover)
profit, general_tax_val = calc_general_tax(turnover, expenses)

# --- Dashboard Display ---
st.markdown("---")

col1, col2 = st.columns(2)

# Column 1: Simplified Regime results
with col1:
    st.header("🏢 Simplified Regime (Law 152)")
    if simple_tax_val is not None:
        st.success(f"Tax Liability: EGP {simple_tax_val:,.2f}")
        st.caption(f"Calculation Basis: {simple_desc}")
    else:
        st.error("Turnover exceeds SME limit (10M EGP).")

# Column 2: General Regime results
with col2:
    st.header("📝 General Regime (Law 91)")
    st.warning(f"Tax Liability: EGP {general_tax_val:,.2f}")
    st.caption(f"Estimated Net Profit: EGP {profit:,.2f} (Tax Rate: 22.5%)")

# --- Recommendation & Analysis ---
st.markdown("---")
st.subheader("💡 Strategic Decision Support")

if simple_tax_val is not None:
    diff = general_tax_val - simple_tax_val
    if diff > 0:
        st.write(f"**Recommendation:** Opt for the **Simplified Regime**.")
        st.write(f"Potential Tax Saving: **EGP {diff:,.2f}**")
    elif diff < 0:
        st.write("**Recommendation:** The **General Regime** might be more beneficial due to low profit margins or losses.")
    else:
        st.write("Both regimes result in the same tax liability.")