# Observability Stack
Provides metrics collection and visualization for the data stack to ensure services remain healthy and performant.

## Components
* **Prometheus**: Scrapes time-series metrics from Trino, MinIO, and other endpoints. Configured via prometheus/prometheus.yml.
* **Grafana**: Visualizes the metrics. Prometheus is auto-provisioned as the default datasource so dashboards can be built immediately.

## Access
* **Prometheus**: http://localhost:9090
* **Grafana**: http://localhost:3000 (Default Login: admin / admin)
