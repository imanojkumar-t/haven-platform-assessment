import json
import subprocess
import sys

from scripts.cost_tag_check import check_plan


def _plan(tmp_path, changes):
    p = tmp_path / "plan.json"
    p.write_text(json.dumps({"resource_changes": changes}))
    return str(p)


def _rc(addr, tags, actions=("create",), rtype="aws_s3_bucket", mode="managed"):
    return {"address": addr, "type": rtype, "mode": mode,
            "change": {"actions": list(actions), "after": {"tags": tags, "tags_all": tags}}}


def test_passes_when_tagged(tmp_path):
    assert check_plan(_plan(tmp_path, [_rc("a.ok", {"landlord_account_id": "LA1"})])) == 0


def test_tenant_id_only_fails(tmp_path, capsys):
    assert check_plan(_plan(tmp_path, [_rc("a.bad", {"tenant_id": "t1"})])) == 1
    assert "a.bad" in capsys.readouterr().out


def test_generic_across_resource_types(tmp_path, capsys):
    plan = _plan(tmp_path, [_rc("aws_sqs_queue.q", {}, rtype="aws_sqs_queue"),
                            _rc("aws_s3_bucket.b", {})])
    assert check_plan(plan) == 1
    out = capsys.readouterr().out
    assert "aws_sqs_queue.q" in out and "aws_s3_bucket.b" in out


def test_noop_read_delete_skipped(tmp_path):
    plan = _plan(tmp_path, [_rc("a.noop", {}, actions=("no-op",)),
                            _rc("a.read", {}, actions=("read",)),
                            _rc("a.del", {}, actions=("delete",))])
    assert check_plan(plan) == 0


def test_replace_is_checked(tmp_path):
    assert check_plan(_plan(tmp_path, [_rc("a.r", {}, actions=("delete", "create"))])) == 1


def test_idempotent_same_output_and_exit(tmp_path):
    plan = _plan(tmp_path, [_rc("a.b", {"tenant_id": "t1"}), _rc("a.a", {})])
    run = lambda: subprocess.run([sys.executable, "scripts/cost_tag_check.py", plan],
                                 capture_output=True, text=True)
    r1, r2 = run(), run()
    assert (r1.stdout, r1.returncode) == (r2.stdout, r2.returncode)
    assert r1.stdout.count("a.a") == 1


def test_real_fixture_flags_exactly_the_two_bad_resources(capsys):
    assert check_plan("fixtures/plan.json") == 1
    out = capsys.readouterr().out
    assert "aws_s3_bucket.listing_media" in out
    assert "aws_lambda_function.mls_feed_sync" in out
    assert "aws_s3_bucket.landlord_media[0]" not in out
    assert "aws_lambda_function.screening_report_export" not in out
