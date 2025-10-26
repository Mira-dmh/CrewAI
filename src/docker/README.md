# Docker Deployment for CrewAI Job Assistant

This directory contains Docker configuration files for deploying the CrewAI Job Assistant application.

## Files

- `Dockerfile` - Container image definition
- `docker-compose.yml` - Multi-container orchestration
- `README.md` - This documentation

## Quick Start

### Prerequisites

- Docker installed and running
- Docker Compose (included with Docker Desktop)
- Environment variables configured in root `.env` file

### Build and Run

1. **Navigate to the project root** (not this docker directory):
   ```bash
   cd /path/to/CrewAI
   ```

2. **Copy environment template**:
   ```bash
   cp .env.example .env
   # Edit .env with your OpenAI API key
   ```

3. **Build and start with Docker Compose**:
   ```bash
   docker-compose -f src/docker/docker-compose.yml up -d
   ```

4. **Access the application**:
   - Open your browser to: http://localhost:8501

### Alternative: Build from this directory

If you want to run Docker Compose from this directory:

```bash
cd src/docker
docker-compose up -d
```

## Docker Commands

### Building the image manually:
```bash
# From project root
docker build -f src/docker/Dockerfile -t crewai-job-assistant .
```

### Running the container manually:
```bash
docker run -d \
  -p 8501:8501 \
  --env-file .env \
  -v $(pwd)/src/data:/app/src/data \
  -v $(pwd)/src/outputs:/app/src/outputs \
  --name crewai-app \
  crewai-job-assistant
```

### Viewing logs:
```bash
docker-compose -f src/docker/docker-compose.yml logs -f
```

### Stopping the application:
```bash
docker-compose -f src/docker/docker-compose.yml down
```

## Configuration

### Environment Variables

The application requires these environment variables in the root `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key_here
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

### Volume Mounts

The Docker setup mounts these directories for data persistence:
- `src/data` - Application data and user files
- `src/outputs` - Generated outputs and session data

### Health Checks

The container includes health checks to monitor application status:
- **Endpoint**: http://localhost:8501/_stcore/health
- **Interval**: 30 seconds
- **Timeout**: 10 seconds
- **Retries**: 3
- **Start Period**: 40 seconds

## Troubleshooting

### Common Issues

1. **Port already in use**:
   ```bash
   # Change port in docker-compose.yml or stop conflicting service
   lsof -ti:8501 | xargs kill
   ```

2. **Permission errors**:
   ```bash
   # Ensure Docker has access to the project directory
   # On macOS: Docker Desktop > Settings > Resources > File sharing
   ```

3. **Environment variables not loading**:
   ```bash
   # Verify .env file exists in project root
   ls -la ../../.env
   ```

4. **Build context issues**:
   ```bash
   # Ensure you're building from the correct context
   # The Dockerfile expects the project root as build context
   ```

### Debugging

1. **Check container logs**:
   ```bash
   docker-compose -f src/docker/docker-compose.yml logs crewai-job-assistant
   ```

2. **Access container shell**:
   ```bash
   docker-compose -f src/docker/docker-compose.yml exec crewai-job-assistant /bin/bash
   ```

3. **Verify health status**:
   ```bash
   docker inspect crewai-job-assistant | grep -i health
   ```

## Production Deployment

For production deployments:

1. **Use production environment file**:
   ```bash
   cp .env.example .env.production
   # Configure production settings
   ```

2. **Enable nginx reverse proxy** (uncomment in docker-compose.yml):
   ```yaml
   nginx:
     image: nginx:alpine
     # ... configuration
   ```

3. **Scale containers**:
   ```bash
   docker-compose -f src/docker/docker-compose.yml up -d --scale crewai-job-assistant=3
   ```

## Security Considerations

- Keep `.env` files secure and never commit them to version control
- Use Docker secrets for sensitive data in production
- Regularly update the base Python image for security patches
- Consider using multi-stage builds to reduce image size

## Support

For issues with Docker deployment:
1. Check the main project README.md
2. Verify all prerequisites are installed
3. Ensure environment variables are correctly configured
4. Check Docker logs for detailed error messages