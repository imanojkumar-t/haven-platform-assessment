import pytest

from app import seed_data
from app.access_control import can_access_screening_report

MANAGERS = {m.id: m for m in seed_data.PROPERTY_MANAGERS}
REPORTS = {r.id: r for r in seed_data.SCREENING_REPORTS}


def allowed(manager_id, report_id):
    return can_access_screening_report(
        MANAGERS[manager_id],
        REPORTS[report_id],
        properties=seed_data.PROPERTIES,
        tenants=seed_data.TENANTS,
    )


@pytest.mark.parametrize("manager_id, report_id", [
    ("pm-001", "rep-001"),
    ("pm-002", "rep-002"),
])
def test_same_account_allowed(manager_id, report_id):
    assert allowed(manager_id, report_id) is True


@pytest.mark.parametrize("manager_id, report_id", [
    ("pm-001", "rep-002"),
    ("pm-002", "rep-001"),
])
def test_cross_account_denied(manager_id, report_id):
    assert allowed(manager_id, report_id) is False


def test_missing_property_data_fails_closed():
    assert can_access_screening_report(
        MANAGERS["pm-001"], REPORTS["rep-001"],
        properties=[], tenants=seed_data.TENANTS,
    ) is False


def test_missing_tenant_data_fails_closed():
    assert can_access_screening_report(
        MANAGERS["pm-001"], REPORTS["rep-001"],
        properties=seed_data.PROPERTIES, tenants=[],
    ) is False
