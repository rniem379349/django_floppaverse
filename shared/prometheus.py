from django_prometheus.middleware import (
    Metrics,
    PrometheusAfterMiddleware,
    PrometheusBeforeMiddleware,
)
from prometheus_client import Counter

from shared.utils.request import get_user_agent

metric_prefix = "floppaverse"

# Define/modify prometheus metrics here
chat_msgs_sent = Counter(
    f"{metric_prefix}_chat_msgs_sent_total", "Total number of chat messages sent"
)

# django-prometheus metrics to be extended
METRICS_TO_UPDATE_WITH_USER_AGENT_DATA = [
    "django_http_requests_latency_seconds_by_view_method",
    "django_http_responses_total_by_status_view_method",
    "django_http_requests_total_by_view_transport_method",
]


class UserAgentLabelConstructor:
    label_names = {
        "browser": "user_agent_browser",
        "os": "user_agent_os",
        "device": "user_agent_device",
        "is_mobile": "user_agent_is_mobile",
        "is_bot": "user_agent_is_bot",
    }

    def __init__(self, request):
        super().__init__()
        self.user_agent = self.get_user_agent_data(request)

    def get_user_agent_data(self, request):
        return get_user_agent(request)

    def construct_user_agent_browser_label(self):
        return {self.label_names["browser"]: self.user_agent.browser.family}

    def construct_user_agent_os_label(self):
        return {self.label_names["os"]: self.user_agent.os.family}

    def construct_user_agent_device_label(self):
        return {self.label_names["device"]: self.user_agent.device.family}

    def construct_is_mobile_label(self):
        return {self.label_names["is_mobile"]: self.user_agent.is_mobile}

    def construct_is_bot_label(self):
        return {self.label_names["is_bot"]: self.user_agent.is_bot}

    def construct_user_agent_labels(self):
        labels = dict()
        browser = self.construct_user_agent_browser_label()
        os = self.construct_user_agent_os_label()
        device = self.construct_user_agent_device_label()
        is_mobile = self.construct_is_mobile_label()
        is_bot = self.construct_is_bot_label()
        labels.update(os, **browser, **device, **is_mobile, **is_bot)
        return labels


class FloppaverseCustomMetrics(Metrics):
    def register_metric(self, metric_cls, name, documentation, labelnames=(), **kwargs):
        if name in METRICS_TO_UPDATE_WITH_USER_AGENT_DATA:
            try:
                for label_name in UserAgentLabelConstructor.label_names.values():
                    labelnames.append(label_name)
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
        if metric._name in METRICS_TO_UPDATE_WITH_USER_AGENT_DATA:
            label_constructor = UserAgentLabelConstructor(request)
            ua_labels = label_constructor.construct_user_agent_labels()
            new_labels.update(ua_labels)
        return super().label_metric(metric, request, response=response, **new_labels)
