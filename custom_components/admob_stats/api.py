"""AdMob API client."""
import logging
from datetime import datetime, timedelta
from typing import Any

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

_LOGGER = logging.getLogger(__name__)


class AdMobAPI:
    """AdMob API client."""

    def __init__(self, client_id: str, client_secret: str, refresh_token: str, publisher_id: str) -> None:
        """Initialize the API client."""
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self.publisher_id = publisher_id
        self._service = None

    def _get_service(self):
        """Get or create the AdMob API service."""
        if self._service is None:
            credentials = Credentials(
                token=None,
                refresh_token=self.refresh_token,
                token_uri="https://oauth2.googleapis.com/token",
                client_id=self.client_id,
                client_secret=self.client_secret,
                scopes=["https://www.googleapis.com/auth/admob.report"],
            )
            self._service = build("admob", "v1", credentials=credentials)
        return self._service

    def test_connection(self) -> bool:
        """Test the connection to AdMob API."""
        try:
            service = self._get_service()
            account_name = f"accounts/{self.publisher_id}"
            service.accounts().get(name=account_name).execute()
            return True
        except Exception as err:
            _LOGGER.error("Error testing connection: %s", err)
            raise

    def _generate_report(self, start_date: datetime, end_date: datetime) -> dict[str, Any]:
        """Generate a report for the given date range."""
        service = self._get_service()
        account_name = f"accounts/{self.publisher_id}"

        date_range = {
            "start_date": {"year": start_date.year, "month": start_date.month, "day": start_date.day},
            "end_date": {"year": end_date.year, "month": end_date.month, "day": end_date.day},
        }

        report_spec = {
            "date_range": date_range,
            "dimensions": ["DATE"],
            "metrics": ["ESTIMATED_EARNINGS", "IMPRESSIONS", "AD_REQUESTS", "CLICKS"],
            "sort_conditions": [{"dimension": "DATE", "order": "DESCENDING"}],
        }

        try:
            response = service.accounts().networkReport().generate(
                parent=account_name, body={"report_spec": report_spec}
            ).execute()
            return response
        except HttpError as err:
            _LOGGER.error("HTTP error generating report: %s", err)
            return {}

    def _parse_metrics(self, response: dict[str, Any]) -> dict[str, Any]:
        """Parse all metrics from API response."""
        if not response:
            return {"earnings": 0.0, "impressions": 0, "ad_requests": 0, "clicks": 0}

        total_earnings = 0.0
        total_impressions = 0
        total_ad_requests = 0
        total_clicks = 0

        for item in response:
            if "row" in item:
                metric_values = item["row"].get("metricValues", {})

                earnings = metric_values.get("ESTIMATED_EARNINGS", {})
                total_earnings += float(earnings.get("microsValue", "0")) / 1_000_000

                impressions = metric_values.get("IMPRESSIONS", {})
                total_impressions += int(impressions.get("integerValue", "0"))

                ad_requests = metric_values.get("AD_REQUESTS", {})
                total_ad_requests += int(ad_requests.get("integerValue", "0"))

                clicks = metric_values.get("CLICKS", {})
                total_clicks += int(clicks.get("integerValue", "0"))

        return {
            "earnings": round(total_earnings, 2),
            "impressions": total_impressions,
            "ad_requests": total_ad_requests,
            "clicks": total_clicks,
        }

    def get_stats(self) -> dict[str, Any]:
        """Get AdMob statistics."""
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)
        first_of_month = today.replace(day=1)
        last_month_end = first_of_month - timedelta(days=1)
        last_month_start = last_month_end.replace(day=1)

        return {
            "today": self._parse_metrics(self._generate_report(
                datetime.combine(today, datetime.min.time()),
                datetime.combine(today, datetime.min.time())
            )),
            "yesterday": self._parse_metrics(self._generate_report(
                datetime.combine(yesterday, datetime.min.time()),
                datetime.combine(yesterday, datetime.min.time())
            )),
            "this_month": self._parse_metrics(self._generate_report(
                datetime.combine(first_of_month, datetime.min.time()),
                datetime.combine(today, datetime.min.time())
            )),
            "last_month": self._parse_metrics(self._generate_report(
                datetime.combine(last_month_start, datetime.min.time()),
                datetime.combine(last_month_end, datetime.min.time())
            )),
        }
