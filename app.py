import streamlit as st
import pandas as pd
import os
import google.generativeai as genai
from io import BytesIO

st.set_page_config(page_title="Data Transformer | By Anas Ahmed", page_icon=":page_facing_up:", layout="centered")

def css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
css("./style.css")


api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')
chat = model.start_chat(history=[])

st.title("Data Transformer | By Anas Ahmed")
st.write("Transform your data files between CSV and Excel formats with powerful features including data cleaning, visualization, and AI-powered analysis!")

uploaded_files = st.file_uploader("Upload your files (CSV OR EXCEL):", accept_multiple_files=True, type=["csv", "xlsx"])
if uploaded_files:
    progress_bar = st.progress(0)
    for i in range(100):
        progress_bar.progress(i + 1)
    st.success("📂 File(s) Uploaded Successfully!")
    
    # Add file selector
    file_names = [file.name for file in uploaded_files]
    selected_file_name = st.selectbox("Select a file to preview:", file_names)
    
    # Process only the selected file
    uploaded_file = next(file for file in uploaded_files if file.name == selected_file_name)
    
    st.divider()
    file = uploaded_file.name
    file_extension = os.path.splitext(file)[1].lower()
    if file_extension == ".csv":
        df = pd.read_csv(uploaded_file)
    elif file_extension == ".xlsx":
        df = pd.read_excel(uploaded_file)
    else:
        st.error(f"Unsupported file format: {file_extension}")

    st.write(f"File: {file}")
    st.write(f"File size: {round(uploaded_file.size/1024,2)} KB")

    st.subheader("Ask AI")
    with st.expander("💬 AI Data Assistant", expanded=True):
        
        if "chat_messages" not in st.session_state:
            st.session_state.chat_messages = []
        
        # Create context about the data
        try:
            data_info = f"""
            File Name: {file}
            Number of Rows: {len(df)}
            Number of Columns: {len(df.columns)}
            Columns: {', '.join(df.columns.tolist())}
            Data : {df.to_string()}
            Basic Statistics: {df.describe().to_string()}
            """
        except Exception as e:
            data_info = df.to_string()
        
        # Display chat messages from history
        for message in st.session_state.chat_messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask a question about your data..."):
            # Display user message
            st.chat_message("user").markdown(prompt)
            # Add user message to chat history
            st.session_state.chat_messages.append({"role": "user", "content": prompt})
            
            # Generate AI response
            with st.chat_message("assistant"):
                with st.spinner("processing..."):
                    try:
                        ai_prompt = f"""
                        Based on this data information:
                        {data_info}
                        
                        Please answer this question: {prompt}
                        
                        Provide a clear and concise answer to the question.
                        """
                        
                        response = chat.send_message(ai_prompt)
                        st.markdown(response.text)
                        # Add assistant response to chat history
                        st.session_state.chat_messages.append(
                            {"role": "assistant", "content": response.text}
                        )
                    except Exception as e:
                        error_message = f"Sorry, I couldn't process that request. Error: {str(e)}"
                        st.error(error_message)
                        st.session_state.chat_messages.append(
                            {"role": "assistant", "content": error_message}
                        )
        
        if st.button("Clear Chat History"):
            st.session_state.chat_messages = []
            st.rerun()
            
    st.write("complete Preview of the selected file")
    st.write(df)

    # Data cleaning options
    st.subheader("Data Cleaning Options")
    col1, col2 = st.columns(2)
    with col1:
        # Remove rows with missing values
        if st.button(f"Remove rows with missing values for {file}"):
            try:
                numeric_columns = df.select_dtypes(include=['number']).columns
                df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].mean())
                non_numeric_columns = df.select_dtypes(exclude=['number']).columns
                df[non_numeric_columns] = df[non_numeric_columns].fillna('')
                st.success("Missing values handled successfully.")
            except Exception as e:
                st.error(f"Error handling missing values: {str(e)}")
    
    with col2:
        # Remove duplicate rows
        if st.button(f"Remove duplicate rows for {file}"):
            try:
                initial_rows = len(df)
                df.drop_duplicates(inplace=True)
                rows_removed = initial_rows - len(df)
                st.success(f"Removed {rows_removed} duplicate rows.")
            except Exception as e:
                st.error(f"Error removing duplicates: {str(e)}")
    
    st.subheader("select columns to convert")
    st.text("only selected columns will be added to the converted file")
    selected_columns = st.multiselect(f"Select columns for {file}", df.columns, default=df.columns )
    df = df[selected_columns]

    st.subheader("Visual extractions from the selected file")
    numeric_data = df.select_dtypes(include=['number'])
    if not numeric_data.empty and len(numeric_data.columns) >= 2:
        st.bar_chart(numeric_data.iloc[:, :2])
    else:
        st.warning("Insufficient numeric columns for visualization. Need at least 2 numeric columns.")

    st.subheader("conversion options")
    conversion_type = st.radio(f"convert {file} to:", ["CSV", "EXCEL"],key=file)
    if st.button(f"Convert {file} to {conversion_type}"):
        buffer = BytesIO()
        if conversion_type == "CSV":
            df.to_csv(buffer, index=False)
            file_name = file.replace(file_extension, ".csv")
            mime_type = "text/csv"
        
        elif conversion_type == "EXCEL":
            df.to_excel(buffer, index=False)
            file_name = file.replace(file_extension, ".xlsx")
            mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        buffer.seek(0)
        st.download_button(
            label=f"Download {file_name} as {conversion_type} file",
            data=buffer,
            file_name=file_name,
            mime=mime_type
        )

st.markdown("""
<div class="footer">
    Made by: <a href="https://github.com/anasahmed07" target="_blank" style="color: #3498db; text-decoration: none;">
        Anas Ahmed (GitHub)
    </a>
</div>
""", unsafe_allow_html=True)