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

1. List any over-arching design goals for the DSL. For example URI friendliness, minimal syntax,
   advanced analytical capabilities, etc.
1. What deficiencies or omissions in other DSLs lead to your decision to design a new language?
1. Were there any languages that inspired the DSL?
1. Are there specific observability use cases the language was designed for?
1. Are there specific observability use cases that were intentionally _omitted_ in the design?
1. Are there any particular strengths or weaknesses in the language after observing it in use?
1. Is the language intended at-rest data and/or streaming data?
1. Can users specify a source in the query language? E.g. a specific table or database?
   1. Can users join with other sources than the primary database? E.g. a CSV file, cloud 
      databases, etc.?
   1. If joining of various time series sources is available, how are differing retentions 
      handled? 

## Data Models

Please answer any of the following questions about telemetry and data models that pertain to the
DSL.

### Metrics

For the purpose of this interview, metrics are defined as numerical measurements associated with
an identifier (typically a metric name and key/value pair dimensions or tags) and a timestamp
(sometimes a time range). Metric query results are generally numerical time series or a single
number.

1. What metric measurement types are supported? E.g. monotonic counters, gauges, deltas, rates,
   bucketed histograms, digests, booleans, etc.
   1. How does the DSL handle changes to the measurement type over time for a single series?
      E.g. if a counter becomes a gauge during the query window?
1. What values are supported as metrics? E.g. double precision floating point,
   integers, booleans, summaries (sum, min, max, count, etc.), histogram bucket counts,
   encoded digests, etc.
1. Does the language support custom or fixed temporal aggregation (downsampling, bucketing, 
   windowing, consolidation) sizes?
   1. If so, are timestamps for the resulting values aligned to the start, end or middle of the 
      window?
   1. Are boundaries inclusive or exclusive? E.g. A window from `(01:00 to 01:01]`
   1. Are aggregation functions for downsampling fixed based on data types or are can users override
      the function? I.e. do queries focus on usability (user will get the correct answer for the data
      they are querying) or flexibility (users could choose a function not appropriate for the data
      type).
      1. If aggregation is fixed, how is the correct aggregation type determined?
1. For DSLs that query over pre-computed temporal aggregates:
   1. Can users manually select the aggregate to select from (e.g. choose between 1 minute 
      sampling, 1 hour sampling, etc.)?
   1. If automatically selected, what rules determine the correct aggregate to query?

**Interpolation**

1. For DSLs that can aggregate "raw" data with misaligned timestamps:
   1. What interpolation scheme is used for various aggregation functions when series do not align
      on timestamp?
   1. Can users select an interpolation scheme at query time?
1. For DSLs that expect metrics to be bucketed at source:
   1. How is missing data for an interval emitted in the final output? (e.g. graph or JSON)
   2. How is missing data represented internally during processing? E.g. as a null, a NaN, etc.
   1. How is missing data handled for various aggregations? E.g. for a sum, if some series are missing
   data points are those missing points treated as zeros? Or the entire window omitted?
      1. For averages, are missing values counted against the denominator?
1. If data retentions can differ between series, how does the DSL handle querying across series that
   span different retention cutoffs? E.g. series A has data but B has already been truncated.

**Identifiers**

1. What components constitute a time series identifier? E.g. metric name, namespace, tags, etc.
1. What character sets are supported by the identifiers?
1. For dimensional time series ID components (key/value pairs):
   1. If dimensional, are metric names a separate aspect from the dimensions or is the metric
      name simply another dimension?
   1. Can dimensions have multiple values?
   1. Are dimension names (no value paired) supported?
   1. Are dimensions required?
   1. Are dimensions typed?
1. Are regular expressions supported on identifier components (and which ones)?
   1. If so, what dialect and features are supported? E.g. POSIX, PCRE, etc.
   1. Are extraction groups to pull values or substrings out of labels supported? 
      1. If so can they be used in joins?

### Logs

1. What does the incoming log event model look like for the DSL? 
   1. A timestamp and a message field? 
   1. Key value maps with information like host name, log level, timestamp and a message field? 
   1. Or just a straight message field?
1. Are log entries with multiple lines treated differently than single lines?
1. Is there special handling for stack traces? E.g. searching by line?
1. Are fields extracted automatically from structured log messages (e.g. JSON or XML) or can fields be
   extracted with a query time hint?
1. Can the DSL include surrounding lines in results when predicate matches are found?
1. Is full text searching supported?
   1. If so, what types of queries are supported? E.g. proximity, phrase, fuzzy, etc.
1. Are regular expressions supported?
   1. If so, what dialect and features are supported? E.g. POSIX, PCRE, etc.
   1. Are extraction groups to pull values or substrings out of labels or lines supported?
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

**Correlation**

1. Can log lines (particularly exceptions) be grouped based on automatic "fingerprinting" of content or
   can users provide a template? E.g. "user bob failed auth from IP 0.0.0.0" and "user alice failed auth from IP 1.2.3.4"
   should have the same finger print though the parameters (user and IP) differ.
1. Does the DSL support "diffing" meaning over two periods of time, were the more or fewer entries, more or fewer
   of a particular finger print, etc.

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

## Metadata

For the purpose of this interview, we primarily refer to metadata as information about the data
in storage that is often used in UIs to assist in discovery. E.g. a list of values for a particular
metric tag or a list of extracted keys in a log index.

1. Does the same DSL for telemetry apply to metadata as well?
   1. If not, in what ways do the APIs or DSL differ when querying for metadata?
1. Are regular expressions supported?
   1. If so, what dialect and features are supported? E.g. POSIX, PCRE, etc.
   1. Are extraction groups to pull values or substrings out of the metadata supported?

## Permissions

1. How does a query respond if a user is not allowed to access one or more components of a query
   but they are allowed access to other portions?
1. Do permissions apply to both metadata and data queries?