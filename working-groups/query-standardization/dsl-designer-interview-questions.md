# DSL Designer Interview Questions

The following is a list of questions we would like query language designers to answer to
the best of their abilities. The goal is to share design goals, tradeoffs and implicit 
assumptions or behaviors that may be used to inform a standardization recommendation. Some
questions are open-ended as we're looking for subtle discussions about design decisions.

Please answer to the existing query language as available to end users. Upcoming work
or features can be included but please call that out clearly. Ideas about a future standard
should be saved for the groups work post analysis.

**Note**
Please do not divulge proprietary information or anything that would be considered a trade secret.
The results of these interview questions will be shared with the working group and the public
in an open source repo.

## Overview

1. What deficiencies or omissions in other DSLs lead to your decision to design a new language?
2. Were there any languages that inspired the DSL?
3. List any over-arching design goals for the DSL. For example URI friendliness, minimal syntax,
   advanced analytical capabilities, etc.
4. Are there specific observability use cases the language was designed for?
5. Are there specific observability use cases that were intentionally omitted in the design?
6. Is the language intended at-rest data and/or streaming data?

## Data Models

Please answer any of the following questions about telemetry and data models that pertain to the
DSL.

### Metrics

For the purpose of this interview, metrics are defined as numerical measurements associated with
an identifier (typically a metric name and key/value pair dimensions or tags) and a timestamp
(sometimes a time range). Metric query results are generally numerical time series or a single
number.

1. Does the language support custom or fixed temporal aggregation (downsampling, bucketing, 
   windowing) sizes?
   2. If so, are timestamps for the resulting values aligned to the start, end or middle of the 
      window?
   3. Are boundaries inclusive or exclusive? E.g. A window from `(01:00 to 01:01]`
   4. Are aggregation functions fixed based on data type or customizable by the user?
4. What metric measurement types are supported? E.g. monotonic counters, gauges, deltas, rates,
   bucketed histograms, digests, booleans, etc.
5. Are time series identifiers dimensional (tags, i.e. key/value pairs) or single-stringed?
   6. If dimensional, are metric names a separate aspect from the dimensions or is the metric
      name simply another dimension?
   7. Can dimensions have multiple values?
   8. Are dimension names (no value paired) supported?
   9. Are dimensions required?
   10. Are dimensions typed?
1. What character sets are supported by the identifiers?
2. What values are supported by the metrics? E.g. double precision floating point,
   integers, booleans, summaries (sum, min, max, count, etc.), histogram bucket counts,
   encoded digests, etc.

### Logs


### Events


### Traces


### Profiles