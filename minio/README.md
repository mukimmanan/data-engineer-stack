# MinIO Object Storage (S3 Compatible)
MinIO acts as the foundational Data Lake storage layer, behaving exactly like AWS S3 for local development.

## Configuration
* **Auto-Provisioning**: The init-minio.sh script automatically creates standard data lake buckets on startup: staging, aw, curated, logging, and ackup.
* **Data Persistence**: Data is persisted to the local ./data directory on your host machine.
* **Region**: Configured as us-east-1 to ensure compatibility with Trino and Spark AWS SDKs.

## Access
* **UI Console**: http://localhost:9001
* **API Endpoint**: http://localhost:9000
