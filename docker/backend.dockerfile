##########################
# Build REST API Service #
##########################

# Read the version from docker-compose
ARG BACKEND_VERSION
# These variables are used by Flask!
ARG DATABASE_HOST
ARG DATABASE_NAME
ARG DATABASE_USER
ARG DATABASE_PASSWORD

FROM python:alpine${BACKEND_VERSION}

# Define working directory
WORKDIR /service

# Copy the project files
COPY backend/ .

# Set up the project
RUN pip install -r requirements.txt

# Run the service
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]