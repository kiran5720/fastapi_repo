FROM python:3.11

# Set the working directory in the container
WORKDIR /home/fastapi/app

# Copy the requirements file into the container
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application into the container(Copies all FastAPI project files into the container.)
COPY . .

# Expose the port FastAPI runs on
EXPOSE 8000

# Command to run the FastAPI app
CMD ["uvicorn", "app.main2:app", "--host", "0.0.0.0", "--port", "8000"]
