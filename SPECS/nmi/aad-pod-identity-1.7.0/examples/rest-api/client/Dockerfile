# Use a lean image
FROM appropriate/curl

# Set the working directory to /app
WORKDIR /app

# Copy the script into the container at /app
ADD script.sh /app

# Install jq (to parse JSON)
RUN apk add --update jq && rm -rf /var/cache/apk/*

# Define environment variable
ENV RESOURCE "MISSING"

# Run shell script
CMD ["sh", "script.sh"]