# Career Site Jobs Aggregator - ATS Salary Data

Open jobs from Greenhouse, Lever, Ashby, Workday, Workable, SmartRecruiters, Recruitee and Personio in one schema with normalized salaries.

[![Run on Apify](https://img.shields.io/badge/Run%20on-Apify-0f9f74)](https://apify.com/datagrit/career-site-jobs-aggregator) [![Docs](https://img.shields.io/badge/docs-getdatagrit.github.io-0e1726)](https://getdatagrit.github.io/career-site-jobs-aggregator/)

**from $2.80 per 1,000 results + $10 per run (pay per result; the rate depends on your Apify plan).** Export as JSON, CSV or Excel, call it through the API, or schedule it on Apify.

## What it does

Give it a list of companies and it returns their open jobs straight from each company's own applicant tracking system (ATS): Greenhouse, Lever, Ashby, Workable, SmartRecruiters, Recruitee, Personio and Workday, all in one schema. Every posting comes with a structured salary (min, max, currency, period and yearly equivalents) whenever the employer publishes one, either in the ATS pay fields or as a pay range in the job description. It is built for recruiters, job boards, sales teams tracking hiring signals and anyone who monitors a fixed list of employers.

## Quick start

1. Open [Career Site Jobs Aggregator - ATS Salary Data on Apify Store](https://apify.com/datagrit/career-site-jobs-aggregator) and click **Try for free**.
2. Fill in the input form (or paste the JSON below) and run it.
3. Download the dataset, or fetch it from the API.

```json
{
  "companies": [
    "https://jobs.ashbyhq.com/ramp",
    "robinhood",
    "https://greatminds.recruitee.com"
  ],
  "onlyWithSalary": true,
  "maxItems": 50
}
```

## Input

| Field | Type | What it does |
|---|---|---|
| `companies` | array | One entry per company, in any of these forms: a job board URL (boards.greenhouse.io/robinhood, jobs.lever.co/palantir, jobs.ashbyhq.com/ramp, apply.workable.com/huggingface, careers.smartrecruiters.com/BoschGroup, greatminds.recruitee.com, gokarla-gmbh.jobs.personio.de, nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite), a company careers page URL (the Actor reads the page once and uses the job board it links to most often), a bare slug such as robinhood (tried on Greenhouse, Lever, Ashby, Workable, Recruitee, Personio and SmartRecruiters in that order; the first board with open postings wins), or ats:slug such as lever:palantir to skip the guessing. Workday needs the full career site URL. Companies that are not found are listed in the run status; if none is found the run fails. With no company at all the Actor runs a small free example (Ramp on Ashby, up to 10 postings, not charged per result) and says so in the run status. |
| `keywords` | array | Optional. Keep a posting when a word of its title starts with any of these terms (case-insensitive), so engineer also matches Engineering. Leave empty for all roles. |
| `excludeKeywords` | array | Optional. Drop a posting when a word of its title starts with any of these terms, for example intern or senior. |
| `departments` | array | Optional. Keep only postings whose department or team contains a word starting with one of these terms, for example engineering or sales. Workday career sites do not publish a department, so their postings never match this filter. |
| `locations` | array | Optional. Keep only postings where one of the listed locations contains a word starting with one of these terms, for example london, germany or new york. The check runs on the locations field of each result. |
| `remoteOnly` | boolean | Keep only postings with workplaceType remote. Hybrid roles are excluded. Lever, Ashby, SmartRecruiters and Recruitee publish the workplace type; for Greenhouse, Workable (postings not flagged remote), Personio and Workday it is remote when a location of the posting says Remote (Greenhouse: its main location). |
| `employmentTypes` | array | Optional. Keep only these normalized employment types: full_time, part_time, contract, temporary, internship, other. Greenhouse does not publish an employment type, so its postings never match this filter. |
| `onlyWithSalary` | boolean | Skip postings without a salary range, either from the ATS pay fields or (when Read salary from description is on) from a pay range written in the job description. |
| `salaryFromDescription` | boolean | When the ATS has no pay field for a posting, look for an explicit pay range in the job description (for example 184,000 USD - 287,500 USD or $28.50 - $34.00 per hour). Only ranges with a currency and a clear period are used; single amounts, bonuses, stipends and funding figures are ignored. salarySource tells you where each salary came from. |
| `minAnnualSalary` | integer | Keep only postings whose top salary, converted to a yearly amount (hourly x 2080, daily x 260, weekly x 52, monthly x 12), reaches this value. Amounts are never converted between currencies, so set Salary currencies together with this filter. 0 disables it. Postings without a yearly amount are skipped by this filter. |
| `salaryCurrencies` | array | Optional. Keep only postings with a salary range in one of these currencies (three-letter codes such as USD, CAD, GBP or EUR). A posting with ranges in several currencies matches when any of them is listed, and its salary fields are then given in that currency. |
| `postedWithinDays` | integer | Keep only postings published in the last N days, by the postedAt field. 0 disables the filter. |
| `onlyNewSinceLastRun` | boolean | Return only postings that earlier runs with the same companies and the same filters have not delivered to you. The Actor remembers the postings it actually returned, per job board and per filter combination, in a storage on your account; postings dropped by your filters or cut off by a result limit are not remembered and can still come later. Changing a filter starts a separate feed. The first run returns everything that matches. |
| `includeDescription` | boolean | Adds the plain-text job description, cut to 8000 characters. Off by default to keep the dataset small. SmartRecruiters postings have no description in the list the Actor reads, so it stays empty for them. |
| `maxItemsPerCompany` | integer | Stop reading a company after this many results, so one large employer does not use up Maximum results. 0 means no per-company limit. |
| `maxItems` | integer | Stop after this many postings in total across all companies. |
| `proxyConfiguration` | object | Optional proxy. Leave disabled: the job board APIs the Actor reads are public and need none. |

## Output

| Field | Type | Description |
|---|---|---|
| `company` | string | Company name as the ATS publishes it; the board slug (Workday: the tenant) when the ATS publishes no name. On the single status row (found = false) it lists the boards that were read, comma-separated. |
| `companySlug` | string | Identifier of the job board on its ATS, as used in the board URL (Workday: tenant/site). |
| `ats` | string | Applicant tracking system the posting was read from. |
| `boardUrl` | string | Public job board of the company on its ATS. |
| `jobId` | string | Identifier of the posting on its ATS (Workable: shortcode; Workday: last part of the posting path). Unique within one board. |
| `requisitionId` | string | Internal requisition or reference number when the ATS publishes one (Greenhouse, Workable, SmartRecruiters, Workday). |
| `title` | string | Job title. |
| `department` | string | Department as published by the ATS (Greenhouse: all departments joined with "; "; SmartRecruiters: department, else job function). Workday career sites publish none. |
| `team` | string | Team when the ATS publishes one (Lever, Ashby). |
| `location` | string | Main location text of the posting. |
| `locations` | array | Every location listed for the posting (main, secondary and office locations), without duplicates. The Locations filter checks this list. |
| `workplaceType` | string | remote, hybrid or onsite. Taken from the ATS where it publishes one (Lever, Ashby, SmartRecruiters, Recruitee, Workable remote flag); otherwise remote or hybrid when a location says so, else null (unknown). |
| `employmentType` | string | Normalized employment type. null when the ATS publishes none (Greenhouse). |
| `postedAt` | string | When the posting was first published, ISO 8601 (Workday: posting start date at 00:00 UTC; Personio: creation date). |
| `updatedAt` | string | Last update time when the ATS publishes it (Greenhouse, Recruitee). |
| `daysSincePosted` | integer | Whole days between postedAt and the run. |
| `url` | string | Public page of the posting. |
| `applyUrl` | string | Separate application link when the ATS publishes one (Lever, Ashby, Workable, Recruitee); null when the application form is on the posting page. |
| `hasSalary` | boolean | True when a salary range was found for the posting. |
| `salaryMin` | number | Lowest amount of the salary range in salaryCurrency per salaryPeriod. With several ranges (zones, levels) it is the lowest of those in the same currency and period. |
| `salaryMax` | number | Highest amount of the salary range in salaryCurrency per salaryPeriod. |
| `salaryCurrency` | string | Currency of salaryMin and salaryMax (three-letter code). With Salary currencies set, the first listed currency the posting pays in. |
| `salaryPeriod` | string | Period of salaryMin and salaryMax. null when the ATS gives a range without a period. |
| `salaryAnnualMin` | integer | salaryMin as a yearly amount (hour x 2080, day x 260, week x 52, month x 12), same currency. |
| `salaryAnnualMax` | integer | salaryMax as a yearly amount, same currency. Minimum annual salary filters on this field. |
| `salaryCurrencies` | array | Every currency in which the posting publishes a range (for example USD and CAD zones). |
| `salarySource` | string | ats = pay fields of the ATS (Greenhouse pay ranges, Lever salaryRange, Ashby compensation, Recruitee salary); description = explicit pay range found in the job description text. |
| `salaryText` | string | The ranges as published: pay zone summaries, the ATS salary summary or the matched text from the description. |
| `equityMentioned` | boolean | True when the ATS pay data has an equity component or the pay notes or description mention equity, stock options or RSUs. null when no text was available (SmartRecruiters). |
| `bonusMentioned` | boolean | True when the ATS pay data has a bonus component or the pay notes or description mention a bonus. null when no text was available. |
| `description` | string | Plain-text job description, cut to 8000 characters. Only with Include description text. |
| `found` | boolean | true for postings; false only on the single status row written when a run returns no postings. |
| `scrapedAt` | string | When the run read the posting, ISO 8601. |

Sample record:

```json
{
  "company": "Robinhood",
  "companySlug": "robinhood",
  "ats": "greenhouse",
  "boardUrl": "https://job-boards.greenhouse.io/robinhood",
  "jobId": "7489697",
  "requisitionId": "JR108060",
  "title": "Engineering Manager, Credit Cards & Banking",
  "department": "Engineering",
  "team": "Mobile",
  "location": "Menlo Park, CA; New York, NY",
  "locations": [
    "New York, NY (HQ)",
    "Remote (US)"
  ],
  "workplaceType": "hybrid",
  "employmentType": "full_time",
  "postedAt": "2026-09-25T17:03:21.000Z",
  "updatedAt": "2026-09-29T08:35:46.000Z",
  "daysSincePosted": 5,
  "url": "https://jobs.ashbyhq.com/ramp/34413f8d-26bf-4bbc-8ade-eb309a0e2245",
  "applyUrl": "https://jobs.ashbyhq.com/ramp/34413f8d-26bf-4bbc-8ade-eb309a0e2245/application",
  "hasSalary": true,
  "salaryMin": 180000,
  "salaryMax": 270000,
  "salaryCurrency": "USD",
  "salaryPeriod": "year",
  "salaryAnnualMin": 180000,
  "salaryAnnualMax": 270000,
  "salaryCurrencies": [
    "USD",
    "CAD"
  ],
  "salarySource": "ats",
  "salaryText": "Zone 1 (Menlo Park, CA; New York, NY): 180K-270K USD/year",
  "equityMentioned": true,
  "bonusMentioned": false,
  "description": null,
  "found": true,
  "scrapedAt": "2026-10-01T08:00:00.000Z"
}
```

## Call it from code

Runnable examples are in [`examples/`](examples). Replace `YOUR_APIFY_TOKEN` with the token from your Apify account settings.

```bash
curl -X POST "https://api.apify.com/v2/acts/datagrit~career-site-jobs-aggregator/run-sync-get-dataset-items?token=YOUR_APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"companies":["https://jobs.ashbyhq.com/ramp","robinhood","https://greatminds.recruitee.com"],"onlyWithSalary":true,"maxItems":50}'
```

## FAQ

**How does it find the ATS?**  
A board URL is read directly. A careers page is fetched once and the job board it links to most often is read. A bare slug is tried on Greenhouse, Lever, Ashby, Workable, Recruitee, Personio (the .de host) and SmartRecruiters in that order, and the first board with open postings wins. The run status lists which board each slug and careers page was matched to, and says when an earlier ATS had a board with that slug but no open postings. Use `ats:slug` or the board URL to pick the board yourself.

**What if a company is not found?**  
The run status lists companies not found, pages without a supported ATS link, boards with no open postings and boards that could not be read. If none of the companies is found, the run fails so a typo never looks like an empty result. SmartRecruiters returns an empty list both for a company without open roles and for an id that does not exist, so such entries are listed separately; if no other company is found the run fails.

**Are there limits?**  
Workday lists at most 2,000 postings per career site; very large Lever and SmartRecruiters boards are read up to 5,000 and 10,000 postings. Any such cut is reported in the run status. Workday needs one extra request per posting for its details, so Workday boards are slower than the others.

**How often should I run it?**  
Daily with only-new mode is typical; each filter combination keeps its own memory of delivered postings.

**Something looks wrong.**  
Open an issue with the input you used; changes at the source are fixed quickly.

## More from datagrit

- [Ashby Salary Scraper - Startup Job Pay Ranges](https://github.com/getdatagrit/ashby-salary-scraper) - Ashby job postings with normalized annual salary ranges, equity flags and new-since-last-run detection.
- [Greenhouse Salary Scraper - Job Pay Ranges](https://github.com/getdatagrit/greenhouse-salary-scraper) - Greenhouse job postings with published pay ranges by zone, annualised pay, filters and new-since-last-run detection.
- [Hacker News Who Is Hiring: Jobs & Hiring History](https://github.com/getdatagrit/hacker-news-hiring-history) - Turn Hacker News Who is hiring threads into job rows with salary, stack, work mode and visa, plus how many months each company has been hiring.
- [TED Contract Expiry Radar - Recompete Leads](https://github.com/getdatagrit/ted-contract-expiry-radar) - Find EU public contracts approaching expiry from TED award notices: incumbent, buyer, value, end date and renewal options.
- [UK Contract Expiry Radar - Recompete Leads](https://github.com/getdatagrit/uk-contract-expiry-radar) - UK public contracts ending soon with incumbent supplier, buyer, value and contact - recompete leads from Contracts Finder award notices.

All Actors: [https://getdatagrit.github.io/](https://getdatagrit.github.io/) · [Apify Store](https://apify.com/datagrit)

---

This repository holds documentation and usage examples. Questions, bug reports and feature requests: use the **Issues** tab of the Actor page on [Apify Store](https://apify.com/datagrit/career-site-jobs-aggregator). Examples are MIT licensed.
