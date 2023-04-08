# Pull base image
FROM python:3.9-slim-bullseye


# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1



# Set work directory
WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy project
COPY ./src /code/src

CMD ["uvicorn", "src.app.main:app", "--host", "0.0,0.0","--port","80"]
