from django_prometheus.middleware import (
    Metrics,
    PrometheusAfterMiddleware,
    PrometheusBeforeMiddleware,
)
from prometheus_client import Counter

from shared.utils.request import get_user_agent_browser

prefix = "floppaverse"

# Define prometheus metrics here
django_views_exceptions = Counter(
    f"{prefix}_django_views_exceptions",
    "Total number of exceptions encountered in Django views",
)
chat_msgs_sent = Counter(
    f"{prefix}_chat_msgs_sent_total", "Total number of chat messages sent"
)

EXTENDED_METRICS = [
    "django_http_requests_latency_seconds_by_view_method",
    "django_http_responses_total_by_status_view_method",
    "django_http_requests_total_by_view_transport_method",
]


class FloppaverseCustomMetrics(Metrics):
    def register_metric(self, metric_cls, name, documentation, labelnames=(), **kwargs):
        if name in EXTENDED_METRICS:
            try:
                labelnames.append("user_agent_browser")
            except Exception as e:
                print(f"Cannot append user agent info to {name}. Exception: {e}")
        return super().register_metric(
            metric_cls, name, documentation, labelnames=labelnames, **kwargs
        )


class FloppaverseMetricsBeforeMiddleware(PrometheusBeforeMiddleware):
    metrics_cls = FloppaverseCustomMetrics


class FloppaverseMetricsAfterMiddleware(PrometheusAfterMiddleware):
    metrics_cls = FloppaverseCustomMetrics

    def label_metric(self, metric, request, response=None, **labels):
        new_labels = labels
        if metric._name in EXTENDED_METRICS:
            browser = get_user_agent_browser(request)
            new_labels = {"user_agent_browser": browser}
            new_labels.update(labels)
        return super().label_metric(metric, request, response=response, **new_labels)
