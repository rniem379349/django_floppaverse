# django-floppaverse
A Django web app with blog, chat and notification functionality.
Features a prometheus/grafana stack for monitoring and automatic alerts.

## Features
### Web app
- `Django` - web app framework (chat/blog/user management),
- `redis` - to facilitate chat/notifications using `django-channels`,
- `postgres` - SQL database.
### Devops setup
- Github actions CI/CD pipeline (workflows defined in `.github/workflows`),
- Prometheus metric scraping - targets are:
    1. Django app (using `django-prometheus`),
    2. Server (through `node-exporter`),
    3. Grafana dashboarding tool,
    4. Prometheus itself.
- Loki for log aggregation,
- Grafana for constructing dashboards with visualisations of Prometheus metrics and logs,
- Alertmanager for sending alerts when Prometheus detects certain conditions (alerts are defined in `docker/prometheus/*.rules.yml` files),
- MailHog for local SMTP server setup (allows for local alert email testing).

## Deployment
1. Clone the repo
2. Run `docker compose build && docker compose up`
