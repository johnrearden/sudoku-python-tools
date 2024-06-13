FROM ubuntu:20.04 as builder_image

LABEL maintainer="John Rearden <reardenjohn@gmail.com>"

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y && apt-get install -y \
    curl python3.9 python3.9-dev python3.9-venv python3-pip \
    python3-wheel build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN apt upgrade -y

# Create and activate virtual environment
RUN python3 -m venv /home/myuser/venv
ENV PATH='/home/myuser/venv/bin:$PATH'

# Install requirements
COPY requirements.txt .
RUN pip3 install --no-cache-dir wheel
RUN pip3 install --no-cache-dir -r requirements.txt

# Next stage in multi-stage build
FROM ubuntu:20.04 as runner_image
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    python3.9 python3.9-venv && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home myuser
COPY --from=builder_image /home/myuser/venv /home/myuser/venv

USER myuser
RUN mkdir /home/myuser/code
WORKDIR /home/myuser/code
COPY . .

ENV PYTHONUNBUFFERED=1
ENV VIRTUAL_ENV=/home/myuser/venv
ENV PATH='/home/myuser/venv/bin:$PATH'

CMD ["python3", "main.py"]
