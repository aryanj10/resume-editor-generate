# Use a base image with Python
FROM python:3.10-slim

# Install system dependencies (LaTeX and basic tools)
RUN apt-get update && apt-get install -y --no-install-recommends \
    texlive-xetex \
    texlive-latex-recommended \
    texlive-fonts-recommended \
    texlive-latex-base \
    ghostscript \
    poppler-utils \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*


# Set working directory
WORKDIR /app

# Copy requirements and install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Set the Streamlit port and disable browser auto-open
ENV STREAMLIT_PORT=8080
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Expose the port
EXPOSE 8080

# Run Streamlit
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8080", "--server.address=0.0.0.0", "--server.enableCORS=false"]

