# pip install apify-client
import os
from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("datagrit/career-site-jobs-aggregator").call(run_input={
    "companies": [
        "https://jobs.ashbyhq.com/ramp",
        "robinhood",
        "https://greatminds.recruitee.com"
    ],
    "onlyWithSalary": True,
    "maxItems": 50
})
items = client.dataset(run["defaultDatasetId"]).list_items().items
print(len(items), "records")
print(items[0] if items else None)
