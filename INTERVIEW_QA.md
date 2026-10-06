# Weather Data Analyzer: interview questions and answers

Answers describe this repository's current implementation. Suggested production changes are explicitly labeled as future work.

## 1. What input shape is accepted?

`analyze` requires a non-empty list containing only dictionaries. The HTTP endpoint expects a JSON object with a `rows` field; invalid top-level row collections raise `InputError` and become 422.

Source: [src/weather/analyze.py](src/weather/analyze.py).

## 2. How are invalid temperatures handled?

Each `temp_c` value is converted with `float`. Conversion failures, booleans, non-finite values, and temperatures outside [-100, 100] are skipped and counted. If every row is skipped, the function raises `InputError` instead of returning empty statistics.

Source: [src/weather/analyze.py](src/weather/analyze.py).

## 3. How is the median calculated?

Numeric temperatures are sorted. For odd counts the middle value is returned; for even counts the two middle values are averaged. The median is not rounded by the function.

Source: [src/weather/analyze.py](src/weather/analyze.py).

## 4. What do rows and skipped mean?

`rows` is the original input length, while `skipped` counts failed numeric conversions. The valid count is their difference. Aggregate statistics use only successfully converted temperatures.

Source: [src/weather/analyze.py](src/weather/analyze.py).

## 5. How are missing city names grouped?

Missing, null, and blank city values are normalized to `unknown`; other city strings are trimmed. The result includes city sample counts as well as means.

Source: [src/weather/analyze.py](src/weather/analyze.py).

## 6. Which values are rounded?

Overall mean and per-city means are rounded to four decimal places. Median, minimum, and maximum are returned from the underlying float values without that rounding step.

Source: [src/weather/analyze.py](src/weather/analyze.py).

## 7. Does numeric conversion reject non-finite values?

The function explicitly rejects non-finite values, booleans, and values outside its supported [-100, 100] Celsius range. Such rows increase `skipped`; a request with no valid values returns HTTP 422. Input is limited to 10,000 rows.

Source: [src/weather/analyze.py](src/weather/analyze.py).

## 8. What is the algorithmic cost?

The function collects values and groups, then sorts the values for the median. Sorting costs O(n log n) time and stored values use O(n) memory. Larger workloads could use bounded batches or a defined streaming summary strategy.

Source: [src/weather/analyze.py](src/weather/analyze.py).

## 9. How are the domain API and ops plane connected?

The app registers the ops router under `/v1`, alongside the domain endpoint. Creating or approving a job updates ops records; it does not call the domain function. There is no background worker or job executor.

Source: [src/weather/main.py](src/weather/main.py).

## 10. Does X-Tenant-Id authenticate a user?

No. It is a caller-supplied header defaulting to `default`. Workspace and job reads filter by that value, but a caller can choose another value. Real identity and authorization would need to precede this lab tenant selector.

Source: [src/weather/ops.py](src/weather/ops.py).

## 11. What survives a process restart?

Nothing in the ops dictionaries or audit list is persisted. Multiple server workers would also have separate state. Durable storage, transactions, and a shared job queue are future changes.

Source: [src/weather/ops.py](src/weather/ops.py).

## 12. What happens when a production job is approved?

Targets are trimmed and normalized to lowercase before policy checks. `prod` and `production`, including case/padding variants, create a `pending_approval` job and approval returns HTTP 403. Repeated lab approval is idempotent; approval changes a record only, without executing a workload.

Source: [src/weather/ops.py](src/weather/ops.py).

## 13. Are audit and metrics equally tenant-scoped?

Audit results filter events by the tenant and its workspace/job identifiers. `/v1/metrics` returns process-wide counters without tenant filtering, so it is not a tenant-specific dashboard. Domain requests are not automatically audited.

Source: [src/weather/ops.py](src/weather/ops.py).

## 14. What would you prioritize before a customer deployment?

Define authenticated identities and permission checks, durable state, typed domain inputs, bounded requests, concurrency behavior, and observable execution semantics. Use the existing tests as a baseline, then test failure and access boundaries rather than claiming the lab is production-ready.

Source: [src/weather/ops.py](src/weather/ops.py).
