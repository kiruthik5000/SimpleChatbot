# 1️⃣ Base image
FROM python:3.10-slim

# 2️⃣ Set working directory
WORKDIR /app

# 3️⃣ Install system dependencies (optional if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 4️⃣ Copy dependencies list first (for better caching)
COPY requirements.txt .

# 5️⃣ Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 6️⃣ Copy the rest of your code
COPY . .

# 7️⃣ Expose FastAPI port
EXPOSE 8000

# 8️⃣ Run FastAPI app with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
