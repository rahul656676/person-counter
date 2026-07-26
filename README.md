# 🚶‍♂️ Person Counter (Computer Vision API)

A scalable, containerized Computer Vision microservice that counts people in images or video streams using OpenCV and FastAPI.

## 🏗 Architecture
Designed as a production-grade machine learning microservice ready for Kubernetes.
- **Inference Engine**: `detector.py` wraps OpenCV logic to identify human contours/cascades.
- **API Gateway**: `main.py` exposes FastAPI endpoints for client integration (e.g., uploading frames for detection).
- **Deployment Strategy**: Containerized via `Dockerfile` and orchestrated using the provided `deployment.yaml` and `service.yaml` manifests.

```mermaid
graph TD
    Client -->|POST /detect (Image)| FastAPI
    FastAPI --> OpenCV_Engine
    OpenCV_Engine -->|Bounding Boxes & Count| FastAPI
    FastAPI -->|JSON Response| Client
```

## 📦 Containerization & K8s
To run this in a cluster:
1. **Build Docker Image**: `docker build -t person-counter:latest .`
2. **Apply Manifests**: `kubectl apply -f deployment.yaml` & `kubectl apply -f service.yaml`
3. **Scale**: The service is stateless and can be scaled horizontally.

## 🛠 Local Execution
For local testing:
```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```
