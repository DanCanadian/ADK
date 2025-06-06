"""Example workflow integrating MetricsCollector and ReportGenerator."""
from src.core.metrics import MetricsCollector
from src.core.reporting import ReportGenerator


def main() -> None:
    collector = MetricsCollector()
    collector.add(impressions=1200, clicks=160, cost=80.0, conversions=20, revenue=320.0)
    metrics = collector.collect()

    reporter = ReportGenerator()
    reporter.export_csv(metrics, "ads_metrics.csv")
    print("Metrics exported to ads_metrics.csv")


if __name__ == "__main__":
    main()
