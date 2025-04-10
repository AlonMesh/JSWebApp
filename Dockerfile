FROM python:3.9-slim as backend

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server/ ./server/

FROM node:18 as frontend

WORKDIR /client

COPY client/package.json client/package-lock.json ./
RUN npm install
COPY client/ ./
RUN npm run build

FROM python:3.9-slim

RUN pip install fastapi uvicorn

WORKDIR /app

COPY --from=backend /app /app

COPY --from=frontend /client/build ./client/build

ENV PORT=8000
EXPOSE $PORT

CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000"]
