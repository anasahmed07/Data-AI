# Data Transformer

Data Transformer is a Streamlit application that allows users to transform data files between CSV and Excel formats. It includes features for data cleaning, visualization, and AI-powered analysis using Google's Generative AI.

## Features

- **File Upload**: Upload multiple CSV or Excel files.
- **Data Preview**: Preview the uploaded file and its details.
- **AI Data Assistant**: Ask questions about your data and get AI-powered responses.
- **Data Cleaning**: Remove rows with missing values and duplicate rows.
- **Column Selection**: Select specific columns for conversion.
- **Data Visualization**: Visualize numeric data using bar charts.
- **File Conversion**: Convert files between CSV and Excel formats.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/data-transformer.git
   cd data-transformer
   ```

2. Create a virtual environment using `uv` and install the required packages:

   ```bash
   uv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   uv install -r requirements.txt
   ```

## Usage

1. Run the Streamlit app:

   ```bash
   streamlit run app.py
   ```

2. Open your web browser and go to `http://localhost:8501` to access the application.

## Configuration

- Ensure you have a valid Google API key and add it to your Streamlit secrets:

  ```plaintext
  [secrets]
  GOOGLE_API_KEY = "your_google_api_key"
  ```

## Dependencies

- `pandas`
- `streamlit`
- `google-generativeai`
- `openpyxl`

## License

This project is licensed under the MIT License.

## Author

- Anas Ahmed - [GitHub](https://github.com/anasahmed07)
