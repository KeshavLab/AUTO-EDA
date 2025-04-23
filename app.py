import streamlit as st
import pandas as pd
import sqlite3
import seaborn as sns
import matplotlib.pyplot as plt

from eda_tool.data_loader import load_data
from eda_tool.eda_summary import dataset_summary
from eda_tool.missing_values import plot_missing_values
from eda_tool.outlier_detection import detect_outliers
from eda_tool.visualization import (
    plot_histograms, plot_correlation_matrix, 
    plot_countplots, plot_boxplots, plot_kde
)
from eda_tool.chatbot import chatbot_response
from eda_tool.report_generator import generate_pdf_report, generate_markdown_report  # Auto Report Generation
from auth.auth_utils import authenticate_user, save_user  # Authentication functions

# Set Streamlit Page Config
st.set_page_config(page_title="Auto EDA", layout="wide")

# --- SESSION STATE FOR AUTH ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# --- AUTHENTICATION SYSTEM ---
def login():
    """Displays login form and authenticates users."""
    st.title("🔑 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if authenticate_user(username, password):
            st.session_state.authenticated = True
            st.session_state.username = username
            st.success("✅ Login successful!")
            st.rerun()
        else:
            st.error("❌ Invalid username or password.")

def register():
    """Displays registration form for new users."""
    st.title("📝 Register")
    username = st.text_input("Choose a Username")
    password = st.text_input("Choose a Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        if password != confirm_password:
            st.error("❌ Passwords do not match!")
        elif save_user(username, password):
            st.success("✅ Registration successful! Please login.")
        else:
            st.error("❌ Username already exists. Try a different one.")

# --- SHOW LOGIN/REGISTER IF NOT AUTHENTICATED ---
if not st.session_state.authenticated:
    auth_option = st.sidebar.radio("🔐 Select Option", ["Login", "Register"])
    login() if auth_option == "Login" else register()
    st.stop()

# --- MAIN APP AFTER LOGIN ---
st.title(f"🔍 Auto EDA - Welcome, {st.session_state.username}!")

# Upload file section
st.sidebar.header("📂 Upload Dataset")
uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

def auto_clean_data(df):
    """Automatically cleans dataset by removing duplicates, standardizing column names, and handling missing values."""
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")  # Standardize column names
    df.drop_duplicates(inplace=True)  # Remove duplicates
    for col in df.select_dtypes(include=['number']).columns:
        df[col].fillna(df[col].median(), inplace=True)  # Fill missing numerical values with median
    return df

# Load dataset if uploaded
df = load_data(uploaded_file) if uploaded_file else None

if df is not None:
    st.success("✅ Data loaded successfully!")

    # --- CHATBOT SECTION ---
    st.sidebar.header("🤖 AI Chatbot")
    with st.sidebar.expander("💬 Ask the AI Chatbot"):
        user_query = st.text_input("Type your question:")
        if user_query and st.button("Ask Chatbot"):
            with st.spinner("🤖 Thinking..."):
                response = chatbot_response(user_query, df)
            st.sidebar.markdown(f"**🧠 Chatbot:** {response}")

    st.sidebar.markdown("---")

    # --- MAIN APP SECTIONS ---
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Data Preview", "🔍 EDA Summary", "🚨 Outliers", "📈 Visualizations", "🧹 Auto Data Cleaning", "📜 Report Generation"
    ])

    # --- DATA PREVIEW ---
    with tab1:
        st.subheader("📊 Data Preview")
        st.dataframe(df.head())

    # --- DATA SUMMARY ---
    with tab2:
        st.subheader("🔍 EDA Summary")
        if st.button("Generate Summary"):
            summary = dataset_summary(df)
            st.json(summary)
        
        with st.expander("🔎 View Missing Values Heatmap"):
            fig = plot_missing_values(df)
            if fig:
                st.pyplot(fig)
            else:
                st.write("✅ No missing values detected!")

    # --- OUTLIER DETECTION ---
    with tab3:
        st.subheader("🚨 Outlier Detection")
        numeric_cols = df.select_dtypes(include=['number']).columns
        selected_col = st.selectbox("Select a column for outlier detection", numeric_cols)

        if selected_col:
            outlier_df, summary_dict = detect_outliers(df, selected_col)

            with st.expander("📊 View Outlier Summary"):
                st.json(summary_dict)

            if not outlier_df.empty:
                st.warning(f"⚠️ {len(outlier_df)} outliers detected in **{selected_col}**")
                st.dataframe(outlier_df)
            else:
                st.success(f"✅ No outliers detected in **{selected_col}**!")

    # --- VISUALIZATIONS ---
    with tab4:
        st.subheader("📈 Data Visualizations")
        vis_option = st.selectbox(
            "Choose Visualization", 
            ["Histograms", "Correlation Matrix", "Count Plots", "Box Plots", "KDE Plots"]
        )

        def display_figures(figs):
            """Handles displaying single or multiple figures."""
            if isinstance(figs, list):
                for fig in figs:
                    st.pyplot(fig)
            elif figs is not None:
                st.pyplot(figs)

        if st.button("Generate Plot"):
            if vis_option == "Histograms":
                display_figures(plot_histograms(df))
            elif vis_option == "Correlation Matrix":
                display_figures(plot_correlation_matrix(df))
            elif vis_option == "Count Plots":
                display_figures(plot_countplots(df))
            elif vis_option == "Box Plots":
                display_figures(plot_boxplots(df))
            elif vis_option == "KDE Plots":
                display_figures(plot_kde(df))

    # --- AUTO DATA CLEANING ---
    with tab5:
        st.subheader("🧹 Auto Data Cleaning")
        if st.button("Clean Data"):
            cleaned_df = auto_clean_data(df)
            st.success("✅ Data cleaned successfully!")
            st.dataframe(cleaned_df.head())

            csv = cleaned_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Cleaned Dataset",
                data=csv,
                file_name="cleaned_data.csv",
                mime="text/csv"
            )

    # --- REPORT GENERATION ---
    with tab6:
        st.subheader("📜 Auto Report Generation")
        report_format = st.radio("Choose Report Format:", ["PDF", "Markdown"])
        
        if st.button("Generate Report"):
            with st.spinner("📝 Generating Report..."):
                missing_fig = plot_missing_values(df)
                outlier_info = {col: detect_outliers(df, col)[0].shape[0] for col in df.select_dtypes(include=['number']).columns}
                visualizations = [plot_histograms(df), plot_correlation_matrix(df)]

                if report_format == "PDF":
                    pdf_file = generate_pdf_report(df, dataset_summary(df), missing_fig, outlier_info, visualizations)
                    with open(pdf_file, "rb") as file:
                        st.download_button("📥 Download PDF Report", file, file_name=pdf_file, mime="application/pdf")

                elif report_format == "Markdown":
                    md_file = generate_markdown_report(df, dataset_summary(df), "Check missing values heatmap", outlier_info)
                    with open(md_file, "rb") as file:
                        st.download_button("📥 Download Markdown Report", file, file_name=md_file, mime="text/markdown")

# --- LOGOUT BUTTON ---
if st.sidebar.button("🚪 Logout"):
    st.session_state.authenticated = False
    st.rerun()
