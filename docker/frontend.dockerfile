#########################
# Build web application #
#########################

# Read the version from docker-compose
ARG FRONTEND_VERSION
ARG BACKEND_SERVICE_HOST
ARG BACKEND_SERVICE_PORT

# Build the app in image ‘builder’ (docker multi-stage builds)
FROM node:lts-alpine${FRONTEND_VERSION} as builder

# Define working directory
WORKDIR /app

# Copy the project files
COPY frontend/ .

# Set up the project and build in production mode
RUN npm install
RUN npm run build --omit=dev

#############################
# Serve the web application #
#############################

# Use nginx server to deliver the application
FROM nginx:alpine${FRONTEND_VERSION}

# Transfer the output of the build step
COPY --from=builder /app/dist/gamomagic/ /usr/share/nginx/html/

# Replace the default nginx configuration
COPY docker/frontend.nginx.conf /etc/nginx/conf.d/default.conf