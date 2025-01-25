# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app
RUN chmod +x /entrypoint.sh
# Install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY entrypoint.sh ./entrypoint.sh
ENTRYPOINT ["sh", "-c", "./entrypoint.sh"]

# Expose the port that FastAPI will run on
EXPOSE 8000
# Command to run the FastAPI app using Uvicorn

CMD ["/bin/bash", "entrypoint.sh"]
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

