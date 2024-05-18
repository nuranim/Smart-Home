import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Customizing the page layout and title
st.set_page_config(page_title='Smart Home Energy Management System', layout='wide')

# Custom CSS to remove the white bar at the bottom
st.markdown("""
    <style>
    .css-1outpf7, .css-12oz5g7, .css-18e3th9, .css-1d391kg {
        padding: 0 !important;
        margin: 0 !important;
    }
    footer {
        visibility: hidden;
        height: 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and description
st.title('Smart Home Data Visualization')
st.markdown("""
This application visualizes data from a Smart Home Energy Management System. 
Upload your dataset to get started.
""")

# Sidebar for file upload
st.sidebar.title("Upload Data")
uploaded_file = st.sidebar.file_uploader("Upload an Excel or CSV file", type=["xlsx", "xls", "csv"])

if uploaded_file:
    # Read the uploaded file
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file, parse_dates=True)
    else:
        df = pd.read_excel(uploaded_file, parse_dates=True)
    
    # Display the dataframe
    st.write("### Data from the uploaded file:")
    st.dataframe(df.head())
    
    # Check if there's a datetime column
    date_columns = df.select_dtypes(include=['datetime', 'object']).columns.tolist()
    
    if date_columns:
        st.sidebar.title("Data Filtering")
        date_column = st.sidebar.selectbox("Select Date/Time Column", date_columns)
        
        # Attempt to convert to datetime
        try:
            df[date_column] = pd.to_datetime(df[date_column], format='%Y-%m-%d %H:%M:%S')
        except:
            df[date_column] = pd.to_datetime(df[date_column])
        
        # Filter options
        filter_option = st.sidebar.selectbox("Filter by", ["All", "Day", "Week", "Month"])
        
        if filter_option == "Day":
            day = st.sidebar.date_input("Select Day")
            filtered_df = df[df[date_column].dt.date == day]
        elif filter_option == "Week":
            week = st.sidebar.date_input("Select Week (Starting Date)")
            filtered_df = df[df[date_column].dt.to_period('W') == pd.to_datetime(week).to_period('W')]
        elif filter_option == "Month":
            month = st.sidebar.date_input("Select Month (Starting Date)")
            filtered_df = df[df[date_column].dt.to_period('M') == pd.to_datetime(month).to_period('M')]
        else:
            filtered_df = df
        
        # Display the filtered dataframe
        st.write("### Filtered Data:")
        st.dataframe(filtered_df)
    else:
        st.warning("No datetime column found in the dataset.")
        filtered_df = df
    
    # Visualization selection
    st.sidebar.title("Visualization")
    vis_type = st.sidebar.selectbox("Select Visualization Type", ["Line Chart", "Bar Chart", "Scatter Plot"])
    
    # Select columns for visualization
    columns = filtered_df.columns.tolist()
    x_axis = st.sidebar.selectbox("Select X-axis column", columns)
    y_axis = st.sidebar.selectbox("Select Y-axis column", columns)
    
    if vis_type == "Line Chart":
        st.write("### Line Chart")
        fig = px.line(filtered_df, x=x_axis, y=y_axis, title=f"Line Chart of {y_axis} vs {x_axis}")
        st.plotly_chart(fig)
    
    elif vis_type == "Bar Chart":
        st.write("### Bar Chart")
        fig = px.bar(filtered_df, x=x_axis, y=y_axis, title=f"Bar Chart of {y_axis} vs {x_axis}")
        st.plotly_chart(fig)
    
    elif vis_type == "Scatter Plot":
        st.write("### Scatter Plot")
        fig = px.scatter(filtered_df, x=x_axis, y=y_axis, title=f"Scatter Plot of {y_axis} vs {x_axis}")
        st.plotly_chart(fig)

    # Adding a footer with a customized message
    st.markdown("""
    <style>
    .footer {
        font-size: 0.9rem;
        text-align: center;
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f8f9fa;
        padding: 1rem;
        box-shadow: 0px -2px 10px rgba(0,0,0,0.1);
    }
    </div>
    """, unsafe_allow_html=True)
else:
    st.info("Awaiting file upload. Please upload an Excel or CSV file to proceed.")
    
