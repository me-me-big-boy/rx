ARG PY_VERSION

FROM docker.io/python:${PY_VERSION} as builder

# Install PDM to install Python dependencies
RUN pip install pdm~=2.14

# Copy the Python project manifest and PDM lockfile into the container
COPY pyproject.toml pdm.lock /

# Install Python dependencies into a new virtualenv
RUN pdm install --check --frozen-lockfile

# ---

FROM docker.io/python:${PY_VERSION}-slim as api

# Activate the virtualenv
ENV PATH="/.venv/bin:$PATH"

# Install system packages needed for running Python dependencies
# - postgresql-client: required by psycopg2
RUN apt-get update \
  && apt-get install -y postgresql-client \
  && rm -rf /var/lib/apt/lists/*

# Copy virtualenv from the builder image
COPY --from=builder /.venv/ /.venv/

# Copy code into the container; can be overridden with a volume during dev
COPY . /api/

# Run all subsequent steps from the `/api` directory
WORKDIR /api/

# Ensure that the API is properly migrated
ENTRYPOINT ["./entry.sh"]

# Run the Gunicorn production server; can be overridden with command during dev
CMD ["gunicorn"]
