# Use the Nginx official image as the base image
FROM nginx:1.21-alpine

# Copy the Nginx configuration file
COPY /default.conf /etc/nginx/conf.d/default.conf

# Expose port 80 for HTTP traffic
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]