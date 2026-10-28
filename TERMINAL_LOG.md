# TERMINAL_LOG

## Setup
Python 3.14.2
Terraform v1.14.5
on darwin_arm64

Your version of Terraform is out of date! The latest version
is 1.17.0. You can update by downloading from https://developer.hashicorp.com/terraform/install

## B2 part 1 + 2: pytest
============================= test session starts ==============================
platform darwin -- Python 3.14.2, pytest-9.2.0, pluggy-1.7.0 -- /Users/manojkumar/haven-platform-assessment/.venv/bin/python
cachedir: .pytest_cache
rootdir: /Users/manojkumar/haven-platform-assessment
collecting ... collected 13 items

tests/test_access_control_seed.py::test_same_account_allowed[pm-001-rep-001] PASSED [  7%]
tests/test_access_control_seed.py::test_same_account_allowed[pm-002-rep-002] PASSED [ 15%]
tests/test_access_control_seed.py::test_cross_account_denied[pm-001-rep-002] PASSED [ 23%]
tests/test_access_control_seed.py::test_cross_account_denied[pm-002-rep-001] PASSED [ 30%]
tests/test_access_control_seed.py::test_missing_property_data_fails_closed PASSED [ 38%]
tests/test_access_control_seed.py::test_missing_tenant_data_fails_closed PASSED [ 46%]
tests/test_cost_tag_check.py::test_passes_when_tagged PASSED             [ 53%]
tests/test_cost_tag_check.py::test_tenant_id_only_fails PASSED           [ 61%]
tests/test_cost_tag_check.py::test_generic_across_resource_types PASSED  [ 69%]
tests/test_cost_tag_check.py::test_noop_read_delete_skipped PASSED       [ 76%]
tests/test_cost_tag_check.py::test_replace_is_checked PASSED             [ 84%]
tests/test_cost_tag_check.py::test_idempotent_same_output_and_exit PASSED [ 92%]
tests/test_cost_tag_check.py::test_real_fixture_flags_exactly_the_two_bad_resources PASSED [100%]

============================== 13 passed in 0.09s ==============================

## B2 cost-tag check, run 1
FAIL: 2 resource(s) missing 'landlord_account_id' tag:
  - aws_lambda_function.mls_feed_sync (aws_lambda_function)
  - aws_s3_bucket.listing_media (aws_s3_bucket)
exit=1

## B2 cost-tag check, run 2 (idempotency: identical output and exit code)
FAIL: 2 resource(s) missing 'landlord_account_id' tag:
  - aws_lambda_function.mls_feed_sync (aws_lambda_function)
  - aws_s3_bucket.listing_media (aws_s3_bucket)
exit=1
