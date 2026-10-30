# Haven — Platform Infrastructure Assessment

Haven is a multi-tenant real estate platform.

## Domain model

```
LandlordAccount  (the billing unit)
  └── Property
        └── Tenant
              └── ScreeningReport  (SSN, credit score)

PropertyManager  (scoped to exactly one LandlordAccount)
```

`tenant_id` is not the billing unit. A Property Manager's access boundary is their landlord
account, not a single property or tenant. Resources today are tagged with `tenant_id` out of
habit — that's the wrong key for cost attribution, and an access check written against "does
this tenant belong to this manager" misses the actual boundary.

## What not to modify

`app/seed_data.py`, `app/models.py`, `fixtures/plan.json`, `terraform/terraform.tfstate` — the
assignment's checks assume this data is unchanged.

`terraform/terraform.tfstate` is checked in deliberately, not an accident — it's a seeded state
representing 4 already-provisioned landlord media buckets, standing in for a real AWS account so
B0 can be reproduced with `terraform plan` instead of just reasoned about. See `terraform/main.tf`
for how to use it.

## Where things are

| Path | Task |
|---|---|
| `terraform/main.tf` | B0 |
| `terraform/lifecycle.tf` | B1 |
| `app/access_control.py`, `scripts/cost_tag_check.py` | B2 — stubs to implement |


## here is the link to the screen recording 

https://drive.google.com/file/d/1hyoVPFWW7hpdqlLy3igWdA88WMe6K2oC/view?usp=sharing


## here is the link of explaining heaven multi tenant real estate platform assessment

https://drive.google.com/file/d/1dYHLcL0f0DOKfak2ylItE0OKsu4cLQX_/view?usp=drive_link

## with audio 

https://drive.google.com/file/d/1sYW_8BYeGsCksxpft8g8twbni7vXNnR7/view?usp=sharing
