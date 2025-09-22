# Stage 1: The Builder Stage
# We'll use this stage to install our dependencies.
FROM python:3.11-slim as builder

# Set the working directory for this stage.
WORKDIR /app

# Install Poetry, our dependency manager.
RUN pip install poetry

# Copy only the files needed for dependency management.
COPY pyproject.toml poetry.lock ./

# Install project dependencies into a virtual environment.
RUN poetry install --no-dev --no-root && \
    poetry export -f requirements.txt --output requirements.txt --without-hashes

# Stage 2: The Final Production Stage
# We'll use a minimal base image to run our application.
FROM python:3.11-slim

# Set the working directory in the final image.
WORKDIR /app

# Create a non-root user for security.
RUN groupadd --gid 1000 app && \
    useradd --uid 1000 --gid app --shell /bin/sh --create-home app

# Copy the dependencies from the builder stage.
COPY --from=builder /app/requirements.txt ./requirements.txt

# Install the production dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source code and configuration files.
# The --chown flag sets the ownership of the files to our non-root user.
COPY --chown=app:app ./src ./src
COPY --chown=app:app ./config ./config
COPY --chown=app:app ./main.sh ./main.sh
COPY --chown=app:app ./README.md ./README.md

# Make the main script executable.
RUN chmod +x /app/main.sh

# Switch to the non-root user.
USER app

# The command to run the application when the container starts.
ENTRYPOINT ["/app/main.sh"]
