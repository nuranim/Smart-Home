import streamlit as st
import pandas as pd
import plotly.express as px

# Title of the Streamlit app
st.title('Smart Home Data')

# File uploader for Excel and CSV files
uploaded_file = st.file_uploader("Upload an Excel or CSV file", type=["xlsx", "xls", "csv"])

if uploaded_file:
    # Read the uploaded file
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file, parse_dates=True)
    else:
        df = pd.read_excel(uploaded_file, parse_dates=True)
    
    # Display the dataframe
    st.write("Data from the uploaded file:")
    st.write(df)
    
    # Check if there's a datetime column
    date_columns = df.select_dtypes(include=['datetime', 'object']).columns.tolist()
    
    if date_columns:
        date_column = st.selectbox("Select Date/Time Column", date_columns)
        df[date_column] = pd.to_datetime(df[date_column])
        
        # Filter options
        filter_option = st.selectbox("Filter by", ["All", "Day", "Week", "Month"])
        
        if filter_option == "Day":
            day = st.date_input("Select Day")
            filtered_df = df[df[date_column].dt.date == day]
        elif filter_option == "Week":
            week = st.date_input("Select Week (Starting Date)")
            filtered_df = df[df[date_column].dt.to_period('W') == pd.to_datetime(week).to_period('W')]
        elif filter_option == "Month":
            month = st.date_input("Select Month (Starting Date)")
            filtered_df = df[df[date_column].dt.to_period('M') == pd.to_datetime(month).to_period('M')]
        else:
            filtered_df = df
        
        # Display the filtered dataframe
        st.write("Filtered Data:")
        st.write(filtered_df)
    else:
        st.warning("No datetime column found in the dataset.")
        filtered_df = df
    
    # Select visualization type
    vis_type = st.selectbox("Select Visualization Type", ["Line Chart", "Bar Chart", "Scatter Plot"])
    
    # Select columns for visualization
    columns = filtered_df.columns.tolist()
    x_axis = st.selectbox("Select X-axis column", columns)
    y_axis = st.selectbox("Select Y-axis column", columns)
    
    if vis_type == "Line Chart":
        st.write("Line Chart")
        fig = px.line(filtered_df, x=x_axis, y=y_axis, title=f"Line Chart of {y_axis} vs {x_axis}")
        st.plotly_chart(fig)
    
    elif vis_type == "Bar Chart":
        st.write("Bar Chart")
        fig = px.bar(filtered_df, x=x_axis, y=y_axis, title=f"Bar Chart of {y_axis} vs {x_axis}")
        st.plotly_chart(fig)
    
    elif vis_type == "Scatter Plot":
        st.write("Scatter Plot")
        fig = px.scatter(filtered_df, x=x_axis, y=y_axis, title=f"Scatter Plot of {y_axis} vs {x_axis}")
        st.plotly_chart(fig)

# Run the Streamlit app with `streamlit run app.py` in the terminal
