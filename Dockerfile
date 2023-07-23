FROM python:3.11-slim as base

RUN adduser --disabled-password reflex

ARG OPENAI_KEY
FROM base as build

WORKDIR /language_app
ENV VIRTUAL_ENV=/language_app/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY . .

# Install gcc and python3-dev for psutil
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install wheel --default-timeout=100 \
    && pip install -r requirements.txt --default-timeout=100

FROM base as runtime

RUN apt-get update && apt-get install -y \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_19.x | bash - \
    && apt-get update && apt-get install -y \
    nodejs \
    unzip \
    && rm -rf /var/lib/apt/lists/*

RUN npm install -g n
RUN n latest
RUN npm install -g npm@latest
RUN npm install -g yarn

ENV PATH="/language_app/venv/bin:$PATH"

FROM runtime as init

WORKDIR /language_app
ENV BUN_INSTALL="/language_app/.bun"
COPY --from=build /language_app/ /language_app/
RUN reflex init

# RUN yarn install --update-checksums --cwd /language_app/.web

FROM runtime

COPY --chown=reflex --from=init /language_app/ /language_app/
USER reflex
WORKDIR /language_app

# RUN reflex export --no-zip

EXPOSE 3000
EXPOSE 8000

CMD ["reflex", "run" , "--env", "prod"]
