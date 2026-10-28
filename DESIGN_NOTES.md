# Design Notes

## B2 — idempotency key

State exactly what key your `cost_tag_check.py` uses to decide a plan has already been
checked/reported on. Use the word "idempotency" in your explanation.

<!-- Your answer here -->

## Any other decision with a non-obvious alternative

<!-- Your answer here -->

## B2 design notes

### Idempotency
The idempotency key is the pair (resource address, required tag key), for example
`aws_s3_bucket.listing_media` + `landlord_account_id`. Violations are stored in a dict
keyed by that pair, so a resource can never be reported twice. They are sorted by key
before printing, and the output contains no timestamps or other run-dependent data.
The script only reads the plan file and never writes anything. Rerunning it on an
unchanged plan therefore produces identical output and the same exit code. I verified
this by running it twice (see TERMINAL_LOG.md) and with an automated test that compares
the stdout and exit code of two runs.

### Decisions that had a real alternative
1. **Access boundary is the landlord account.** The check walks report -> tenant ->
   property -> landlord account and compares it to the manager's account. The
   alternative, checking tenant or property ownership directly, misses the real boundary
   described in the README.
2. **Fail closed.** A missing tenant, a missing property, a duplicate ID or a missing
   account ID all return False. The alternative (treating unresolved data as allowed or
   raising errors) risks exposing SSN and credit data.
3. **Required tag is `landlord_account_id` only.** `tenant_id` is never consulted, so a
   resource tagged only with `tenant_id` fails. Having both tags passes.
4. **Only resources with a `tags` or `tags_all` key are checked.** Alternative: fail
   every created or updated resource without one. I rejected that because it would
   false-flag resource types that cannot be tagged.
5. **Actions checked are create and update.** A replace (delete + create) is covered
   because it includes create. Delete-only, no-op and read changes are skipped because
   those resources will not be (re)billed from this change.
6. **`tags_all` is merged with `tags`**, so provider default_tags count. Explicit tags
   win on conflict. A stricter alternative would require the tag on the resource itself.
