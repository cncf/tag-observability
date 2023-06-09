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
   1. If so, are timestamps for the resulting values aligned to the start, end or middle of the 
      window?
   1. Are boundaries inclusive or exclusive? E.g. A window from `(01:00 to 01:01]`
   1. Are aggregation functions fixed based on data type or customizable by the user?
1. What metric measurement types are supported? E.g. monotonic counters, gauges, deltas, rates,
   bucketed histograms, digests, booleans, etc.
   1. How does the DSL handle changes to the measurement type? E.g. if a counter becomes a gauge during
      the query window?
1. Are time series identifiers dimensional (tags, i.e. key/value pairs) or single-stringed?
   1. If dimensional, are metric names a separate aspect from the dimensions or is the metric
      name simply another dimension?
   1. Can dimensions have multiple values?
   1. Are dimension names (no value paired) supported?
   1. Are dimensions required?
   1. Are dimensions typed?
1. What character sets are supported by the identifiers?
1. What values are supported by the metrics? E.g. double precision floating point,
   integers, booleans, summaries (sum, min, max, count, etc.), histogram bucket counts,
   encoded digests, etc.
1. How is missing data for an interval reported? Is it null or a NaN?
1. How is missing data handled for various aggregations? E.g. for a sum, if some series are missing
   data points are those missing points treated as zeros? Or the entire window omitted?
   1. For averages, are missing values counted against the denominator?

### Logs

1. What must the overall log event model look like? A timestamp and a message field? Key value maps with
   information like host name, log level, timestamp and a message field? Or just a straight message field?
1. How are multi-line log messages handled (e.g. stack traces)? Are they treated as a single event or
   multiple events?
1. Are fields extracted automatically from structured log messages (e.g. JSON or XML) or can fields be
   extracted with a query time hint?
1. Can the DSL include surrounding lines in results when predicate matches are found?
1. Can log lines (particularly exceptions) be grouped based on automatic "fingerprinting" of content or
   can users provide a template? E.g. "user bob failed auth from IP 0.0.0.0" and "user alice failed auth from IP 1.2.3.4"
   should have the same finger print though the parameters (user and IP) differ.
1. Does the DSL support "diffing" meaning over two periods of time, were the more or fewer entries, more or fewer
   of a particular finger print, etc.
1. Is full text searching supported?
1. Are regular expressions supported?
1. Can users generate metrics from logs?
   1. Can basic graphs be generated based on log level, fingerprint frequencies, etc.?
   1. Or can users write extraction queries to parse fields from logs and apply aggregations to them?
   1. What types of aggregations are supported? E.g. sum, min, max, count by, percentiles?
   1. See the metrics section for more questions about aggregations and metrics generated.
   1. When converting values to types (numeric or boolean, etc.) what happens when some lines have the wrong
      type or are missing? 
1. Can the DSL generate a DAG from trace IDs written to logs?
   1. If tracing is supported, can users query with parent/child or flow relationships?
1. What kind of output formats are supported? Raw log lines, tables, etc.?
1. Is enrichment supported, e.g. merging data from external sources to replace, say, customer IDs.

### Events

1. What is the maximum duration of events supported? Days, months, years?
1. What model must events follow?
1. Refer to logs questions.

### Traces

1. What is the maximum duration of traces supported? Minutes to hours to days?
1. Are multiple roots supported in traces or only one?
1. Are there limits to the # of spans per trace or dimensions per span?
1. Can users query for sub graphs of traces? E.g. say select only traces that visited service A then
   B then fanned out to C and E but not D and called B at least 5 times.
1. Can traces with different models be joined? E.g. one measures in seconds, another measures in millis.
1. Can incomplete traces be queried or only those that are considered or assumed complete?
1. Can attributes be typed at query time for analysis (sums, count bys, etc)
   1. If so, what happens to spans missing the attribute or have attributes with values of the wrong type?

### Profiles

1. What kind of filters are allowed? E.g. by duration, core, thread, function, environment variables?
1. Can users query by DAG, e.g. only show profiles where a user function wound up calling a sys call?
2. Can users create "diffs" with previous intervals based on similar attributes?