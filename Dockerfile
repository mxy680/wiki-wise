FROM python:3.8

# Install wkhtmltopdf
RUN apt-get update && apt-get install -y wkhtmltopdf

# Set working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Run Streamlit app
CMD ["streamlit", "run", "app.py"]
