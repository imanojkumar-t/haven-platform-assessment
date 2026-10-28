from app.models import PropertyManager, ScreeningReport, Property, Tenant


def _unique(records, record_id):
    """Return the single record with this id, or None if absent or ambiguous."""
    if record_id is None:
        return None
    matches = [r for r in records if r.id == record_id]
    return matches[0] if len(matches) == 1 else None


def can_access_screening_report(
    actor: PropertyManager,
    report: ScreeningReport,
    *,
    properties: list[Property],
    tenants: list[Tenant],
) -> bool:
    # The boundary is the landlord account, not the tenant or property.
    # Fail closed on every missing, ambiguous or unresolvable link.
    if actor is None or report is None:
        return False
    if actor.landlord_account_id is None:
        return False

    tenant = _unique(tenants, report.tenant_id)
    if tenant is None:
        return False

    prop = _unique(properties, tenant.property_id)
    if prop is None or prop.landlord_account_id is None:
        return False

    return prop.landlord_account_id == actor.landlord_account_id
