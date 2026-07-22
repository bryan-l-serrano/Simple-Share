# FTP Web File Manager

A simple Flask web application for browsing and uploading files.

## Features

- Browse files in an upload directory
- Upload files with automatic conflict renaming
- Delete files via API

## Quick Start

### With Docker Compose (recommended)

```bash
docker compose up --build
```

The app will be available at http://localhost:3000/files.

### With Docker

```bash
docker build -t ftp-manager .
docker run -p 3000:3000 -v ./config.yaml:/app/config.yaml -v ./share:/app/share ftp-manager
```

### Locally

```bash
pip install -r requirements.txt
python main.py
```

## Configuration

Edit `config.yaml`:

```yaml
port: 3000
upload_folder: "./share"
```

## Endpoints

| Method | Path       | Description              |
|--------|------------|--------------------------|
| GET    | /          | Redirect to /files       |
| GET    | /files     | List files (landing page)|
| GET    | /upload    | Upload form              |
| POST   | /upload    | Upload a file            |
| DELETE | /files/{f} | Delete a file            |
