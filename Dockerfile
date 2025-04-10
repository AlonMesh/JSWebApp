# -------------------
# STAGE 1: Backend (Python) dependencies
# -------------------
    FROM python:3.9-slim AS backend

    # Set working directory
    WORKDIR /app
    
    # Copy and install backend dependencies
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt
    
    # Copy backend code
    COPY server/ ./server/
    
    
    # -------------------
    # STAGE 2: Frontend (React) build
    # -------------------
    FROM node:18 AS frontend
    
    # Set working directory for React
    WORKDIR /client
    
    # Install frontend dependencies
    COPY client/package*.json ./
    RUN npm install
    
    # Copy the full frontend source and build it
    COPY client/ ./
    RUN npm run build
    
    
    # -------------------
    # STAGE 3: Final image with both backend & built frontend
    # -------------------
    FROM python:3.9-slim
    
    # Set working directory in final image
    WORKDIR /app
    
    # Copy backend files and reinstall Python dependencies
    COPY --from=backend /app /app
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt
    
    # Copy built React app into expected static directory
    COPY --from=frontend /client/build /app/client/build
    
    # Expose port for Uvicorn server
    EXPOSE 8000
    
    # Run FastAPI app
    CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000"]
    