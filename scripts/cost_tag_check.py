"""
Cost-tagging check.

Idempotency key: (resource address, required tag key). Violations are stored
in a dict keyed that way, sorted before printing, with no timestamps, so an
unchanged plan always gives identical output and the same exit code.
"""
import json
import sys

REQUIRED_TAG = "landlord_account_id"
CHECKED_ACTIONS = {"create", "update"}


def _effective_tags(after):
    return {**(after.get("tags_all") or {}), **(after.get("tags") or {})}


def check_plan(plan_path: str) -> int:
    try:
        with open(plan_path) as f:
            plan = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read plan {plan_path}: {exc}", file=sys.stderr)
        return 2

    violations = {}
    checked = 0
    for rc in plan.get("resource_changes", []):
        if rc.get("mode", "managed") != "managed":
            continue
        change = rc.get("change") or {}
        if not CHECKED_ACTIONS & set(change.get("actions") or []):
            continue
        after = change.get("after")
        if not isinstance(after, dict) or ("tags" not in after and "tags_all" not in after):
            continue
        checked += 1
        value = _effective_tags(after).get(REQUIRED_TAG)
        if not (isinstance(value, str) and value.strip()):
            violations[(rc["address"], REQUIRED_TAG)] = rc.get("type", "")

    if violations:
        print(f"FAIL: {len(violations)} resource(s) missing '{REQUIRED_TAG}' tag:")
        for (address, _tag), rtype in sorted(violations.items()):
            print(f"  - {address} ({rtype})")
        return 1

    print(f"OK: {checked} taggable resource(s) checked, all have '{REQUIRED_TAG}'.")
    return 0


if __name__ == "__main__":
    sys.exit(check_plan(sys.argv[1]))
