"""Streamlit web application for the calculator."""

import streamlit as st
from average_price_calculator import PriceData, calculate_average_price_safe

# Page configuration
st.set_page_config(
    page_title="Average Price Calculator",
    page_icon="💰",
    layout="wide",
)

# Title
st.title("💰 Average Price Calculator")
st.markdown(
    """
Calculate the weighted average price after additional purchases.
Useful for investment portfolio calculations.
"""
)

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    precision = st.slider("Decimal Precision", 2, 10, 6)
    st.markdown("---")
    st.markdown("### Example Values")
    if st.button("Load Example"):
        st.session_state.initial_qty = 4.37562
        st.session_state.initial_price = 3.602
        st.session_state.new_qty = 2.93867
        st.session_state.new_price = 2.11

# Input form
with st.form("calculator_form"):
    col1, col2 = st.columns(2)

    with col1:
        initial_qty = st.number_input(
            "Initial Quantity",
            value=st.session_state.get("initial_qty", 4.37562),
            min_value=0.0,
            step=0.00001,
            format="%.5f",
            key="initial_qty_input",
        )
        initial_price = st.number_input(
            "Initial Price",
            value=st.session_state.get("initial_price", 3.602),
            min_value=0.0,
            step=0.01,
            format="%.3f",
            key="initial_price_input",
        )

    with col2:
        new_qty = st.number_input(
            "New Quantity",
            value=st.session_state.get("new_qty", 2.93867),
            min_value=0.0,
            step=0.00001,
            format="%.5f",
            key="new_qty_input",
        )
        new_price = st.number_input(
            "New Price",
            value=st.session_state.get("new_price", 2.11),
            min_value=0.0,
            step=0.01,
            format="%.2f",
            key="new_price_input",
        )

    calculate = st.form_submit_button("🚀 Calculate", type="primary")

# Calculation and results
if calculate:
    try:
        # Create and validate data
        data = PriceData(
            initial_quantity=initial_qty,
            initial_price=initial_price,
            new_quantity=new_qty,
            new_price=new_price,
        )

        # Calculate
        result = calculate_average_price_safe(data, precision)

        # Display results
        st.success("Calculation successful!")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "📈 Average Price",
                f"${result.average_price:.{precision}f}",
                delta=None,
            )

        with col2:
            st.metric(
                "📦 Total Quantity",
                f"{result.total_quantity:.{precision}f}",
            )

        with col3:
            st.metric(
                "💰 Total Investment",
                f"${result.total_investment:.{precision}f}",
            )

        # Detailed calculation
        with st.expander("📝 Show Detailed Calculation"):
            formula = (
                rf"\text{{Average Price}} = "
                rf"\frac{{({initial_qty} \times {initial_price}) "
                rf"+ ({new_qty} \times {new_price})}}"
                rf"{{{initial_qty} + {new_qty}}}"
            )
            st.latex(formula)

            calculation_text = f"""
            Initial Investment = {initial_qty} x {initial_price} = {initial_qty * initial_price:.{precision}f}
            New Investment = {new_qty} x {new_price} = {new_qty * new_price:.{precision}f}
            Total Investment = {result.total_investment:.{precision}f}
            Total Quantity = {initial_qty} + {new_qty} = {result.total_quantity:.{precision}f}
            Average Price = {result.total_investment:.{precision}f} ÷ {result.total_quantity:.{precision}f} = {result.average_price:.{precision}f}
            """
            st.code(calculation_text)

        # JSON output
        with st.expander("📄 Show JSON Output"):
            st.json(data.model_dump())
            st.json(result.model_dump())

    except (ValueError, ZeroDivisionError) as e:
        st.error(f"❌ Error: {e}")

# Footer
st.markdown("---")
st.caption(
    "Built with Python, Pydantic, and Streamlit | "
    "[GitHub](https://github.com/aramasala/average-price-calculator)"
)
