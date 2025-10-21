# IntelliCV-AI Main Application Docker Container
# ============================================
# Consolidated main.py with admin AI integration
# Clean Welcome → Login/Registration → Profile → CV upload flow

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements_sandbox.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY main.py .
COPY Home.py .
COPY pages/ ./pages/
COPY static/ ./static/
COPY auth/ ./auth/
COPY utils/ ./utils/
COPY fragments/ ./fragments/
COPY shared_infrastructure_final/ ./shared_infrastructure_final/
COPY .env* ./

# Create necessary directories
RUN mkdir -p logs data temp

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8501/healthz || exit 1

# Environment variables
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Labels
LABEL maintainer="IntelliCV-AI Team"
LABEL description="IntelliCV-AI Intelligent Career Platform - Main Application"
LABEL version="2.0-consolidated"

# Command to run the application
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]