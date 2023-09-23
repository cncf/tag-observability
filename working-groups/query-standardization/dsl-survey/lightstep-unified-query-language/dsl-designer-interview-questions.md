# DSL Designer Interview Questions

The following is a list of questions we would like query language designers to answer to
the best of their abilities. The goal is to share design goals, tradeoffs and implicit 
assumptions or behaviors that may be used to inform a standardization recommendation. We're
also looking at behavior when the query is invalid or encounters unexpected data issues. Some
questions are open-ended as we're looking for subtle descriptions of design decisions.

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
1. How tightly coupled is the DSL to the data store model? (1 to 10 with 10 being extremely)
   tightly coupled)
   1. Is the DSL flexible enough to operate on data in different storage formats or contexts?
1. What character sets are supported by the DSL?
   1. What characters are special or reserved in the DSL?
1. Does the DSL allow for writing data or configuring the backing store or is it for querying only?

## Data Models

Please answer any of the following questions about telemetry and data models that pertain to the
DSL. Include information about what models are supported by the DSL and any aspects of the DSL
that are tightly coupled to the models.

### Metrics

For the purpose of this interview, metrics are defined as numerical measurements associated with
an identifier (typically a metric name and key/value pair dimensions or tags; see the 
[identifiers](#identifiers) section) and a timestamp (sometimes a time range). Metric query results 
are generally numerical time series or a single number.

1. What metric measurement types are supported? E.g. monotonic counters, gauges, deltas, rates,
   bucketed histograms, digests, booleans, etc.

   Supported metric kinds
   * Delta / Cumulatives
   * Gauges 
   
   1. How does the DSL handle changes to the measurement type over time for a single series?
      E.g. if a counter becomes a gauge during the query window?

      Currently, if the underlying metric kind were to change that would affect calculation aligner stages. For example, using a rate aligner over a gauge would still be computable but might be nonsensical given the context of the metric. However, using latest aligner over counter kind is not allowed. 

1. What values are supported as metrics? E.g. double precision floating point,
   integers, booleans, summaries (sum, min, max, count, etc.), histogram bucket counts,
   encoded digests, etc.

   Supported metric values
   * int64
   * float64
   * histogram (distribution)


1. Does the language support custom or fixed temporal aggregation (downsampling, bucketing, 
   windowing, consolidation) sizes?
   
   UQL supports custom temporal aggregation with a minumum period of 1s via the following aligners:
   
   * `delta` - calculates the change in the metric across the input period, outputting a point every output period.
   * `rate` - rate calculates the change per-second of the input tables, outputting a point every output period.
   * `latest` - aligns gauge metrics to the output period by using the nearest point before an output point.
   * `reduce` - reduce performs temporal aggregation for a metric using the supplied reducer.

   There two pieces to alignment the input period (lookback window) and output period (point spacing) that are optional if the last aligner or required if an intermediary. Lastly the `reduce` function takes in a reducer function (min, max, mean, distribution, std_dev, sum, count, count_nonzero).

   1. If so, are timestamps for the resulting values aligned to the start, end or middle of the 
      window?

      Timestamps are aligned to the start of the query window. 

   1. Are boundaries inclusive or exclusive? E.g. A window from `(01:00 to 01:01]`

      [01:00 to 01:01)

   1. Are aggregation functions for downsampling fixed based on data types or are can users override
      the function? I.e. do queries focus on usability (user will get the correct answer for the data
      they are querying) or flexibility (users could choose a function not appropriate for the data
      type).

      Metric kinds, delta and cumulative, do not support the `latest` aligner. Gauge metric kind supports all other aligners. Metric values like int64 and float64 support are supported in all aligners and reducer functions. A distribution/histogram metric value only supported by the detla aligner.

      1. If aggregation is fixed, how is the correct aggregation type determined?
1. For DSLs that query over pre-computed temporal aggregates:
   1. Can users manually select the aggregate to select from (e.g. choose between 1 minute 
      sampling, 1 hour sampling, etc.)?
   1. If automatically selected, what rules determine the correct aggregate to query?

#### Interpolation

1. For DSLs that can aggregate "raw" data with misaligned timestamps:
   1. What interpolation scheme is used for various aggregation functions when series do not align
      on timestamp?

      This depends on the aligners mentioned above but the idea is that points are temporally aggregated and snapped to the output period. 

   1. Can users select an interpolation scheme at query time?

      Yes, for example `reduce` is required to have a reducer which can be one of any of the reducers above.

1. For DSLs that expect metrics to be bucketed at source:
   1. How is missing data for an interval emitted in the final output? (e.g. graph or JSON)
   2. How is missing data represented internally during processing? E.g. as a null, a NaN, etc.
   1. How is missing data handled for various aggregations? E.g. for a sum, if some series are missing
   data points are those missing points treated as zeros? Or the entire window omitted?
      1. For averages, are missing values counted against the denominator?
1. If data retentions can differ between series, how does the DSL handle querying across series that
   span different retention cutoffs? E.g. series A has data but B has already been truncated.

#### Identifiers

1. What components constitute a time series identifier? E.g. metric name, namespace, tags, etc.
1. What character sets are supported by the identifiers?
1. For dimensional time series ID components (key/value pairs):
   1. If dimensional, are metric names a separate aspect from the dimensions or is the metric
      name simply another dimension?

      Metric names are separate from the dimensions.

   1. Can dimensions have multiple values?
      
      Dimensions 

   1. Are dimension names (no value paired) supported?

      No, dimensions must have a key and value. 

   1. Are dimensions required?
      
      Just the metric name is required. Dimensions can be grouped away as well.
      
      ```
         metric requests
         | rate
         | group_by [], sum # collapses all dimensions
      ```

   1. Are dimensions typed?
      
      Yes, dimensions are typed. For example, if a metric had a dimension `code` that was a string for one time series but an int for another time series of the same name, they would be considered two different time series.

1. Are regular expressions supported on identifier components (and which ones)?
   
   Regular expresions are supported on string value dimensions.

   ```
   metric requests
   | filter website.name =~ ".*aol.*"
   | delta
   | group_by [website.name]
   ```

   1. If so, what dialect and features are supported? E.g. POSIX, PCRE, etc.
      
      [RE2](https://github.com/google/re2/wiki/Syntax) - with the flags `s` on by default (`.` matches `\n` character). Matches must be fully anchored meaning in order for the input `SELECT * FROM table`` to match the regular expression would need to be "SELECT.*" instead of "SELECT". 

   1. Are extraction groups to pull values or substrings out of labels supported? 

      Currently extracting groups is not supported but UQL will support this in the future.

      1. If so can they be used in joins?

### Logs

Logs are typically structured (e.g. JSON) or unstructured strings associated with a single timestamp
when the log entry was generated. 

1. What does the incoming log event model look like for the DSL? 
   1. A timestamp and a message field? 
   1. Key value maps with information like host name, log level, timestamp and a message field? 
   1. Or just a straight message field?

   Model is that a log is a document with fields and values that are typed. int, float, strings, arrays, maps.

1. Are log entries with multiple lines treated differently than single lines?

   No difference.

1. Is there special handling for stack traces? E.g. searching by line?

   No special handling.

1. Are fields extracted automatically from structured log messages (e.g. JSON or XML) or can fields be
   extracted with a query time hint?

   Currently, there is no query time extraction of fields. That being said we can see it fitting easily into the language.

1. Can the DSL include surrounding lines in results when predicate matches are found?

   Not at this time. But this sounds more like a function of the system rather than the language. 

1. Is full text searching supported?
   1. If so, what types of queries are supported? E.g. proximity, phrase, fuzzy, etc.

   Currently, we have 3 predicates:
      * `phrase_match(attr, terms)` - deprecated and is meant for a very specialized tokenized field
      * `contains(attr, terms)` - case-insensitive search on any field/attribute 
      * `attr =~ ".*"` - regular expression search on any field/attribute 
1. Are regular expressions supported?
   1. If so, what dialect and features are supported? E.g. POSIX, PCRE, etc.
      
      See metrics section.

   1. Are extraction groups to pull values or substrings out of labels or lines supported?

      See metrics section.

1. Can users generate metrics from logs?
   
   Yes at query time, as well as, the system supports generating metrics at ingest time.

   ```
   logs count
   | filter host.name =~ "foo.*"
   | delta
   | group_by [severity_text], sum
   ```

   1. Can basic graphs be generated based on log level, fingerprint frequencies, etc.?

   `logs` time series queries can be grouped by an arbitrary attribute. Fingerprint/pattern aggregation is not supported at this time.

   1. Or can users write extraction queries to parse fields from logs and apply aggregations to them?
   1. What types of aggregations are supported? E.g. sum, min, max, count by, percentiles?

   The same aggregations as metrics since it is a time series query. Furthermore, the language supports (not yet implemented in the system) arbitrary numeric attributes as distributions. For example, the following query would aggregate on the attribute `duration` and produce a distribution/histogram of `duration` values and then output the p99 by k8s.cluster.name:

      ```
      logs duration
      | delta
      | group_by [k8s.cluster.name], sum
      | point percentile(value, 99)
      ```

   1. See the metrics section for more questions about aggregations and metrics generated.
   1. When converting values to types (numeric or boolean, etc.) what happens when some lines have the wrong
      type or are missing?

      Casting is currently not supported. Aggregations on an attribute where not all log lines have the attribute defined, will result in additional group that's attribute value is undefined. For example, the following query will create n groups where `service` is defined and one additional group where service is undefined.

      ```
      logs count
      | delta
      | group_by [service], sum
      ```

      To avoid the undefined group, a filter predicate of `defined(attr)` would be required:

      ```
      logs count
      | delta
      | filter defined(service)
      | group_by [service], sum
      ```

1. Can the DSL generate a DAG from trace IDs written to logs?
   1. If tracing is supported, can users query with parent/child or flow relationships?
1. What kind of output formats are supported? Raw log lines, tables, etc.?

   Raw log lines are supported with the following query:

   ```
   logs
   | filter host.name == "host-123"
   ```

   All other time series visualizations are supported with the following query:

   ```
   logs count
   | delta
   | filter host.name == "host-123"
   | group_by [], sum
   ```

1. Is enrichment supported, e.g. merging data from external sources to replace, say, customer IDs.

   Enrichment is currently not supported a this time. 

#### Correlation

1. Can log lines (particularly exceptions) be grouped based on automatic "fingerprinting" of content or
   can users provide a template? E.g. "user bob failed auth from IP 0.0.0.0" and "user alice failed auth from IP 1.2.3.4"
   should have the same fingerprint though the parameters (user and IP) differ.

   "fingerprinting" or pattern matching is not supported at this time as a filter predicate or group.

1. Does the DSL support "diffing" meaning over two periods of time, were the more or fewer entries, more or fewer
   of a particular fingerprint, etc.

   Diffing via `logs` time series queries can be used with the `time_shift` stage and joined with a time series from now or any other time.
   ```
   with
      a = logs count
         | time_shift 4h 
         | delta
         | filter host.name == "host-123"
         | group_by [], sum;
      b = logs count
         | delta
         | filter host.name == "host-123"
         | group_by [], sum;
      join b - a
   ```
   

### Events

Events are typically structured similarly to logs but are different in that they have a start time
and end time. Examples include holidays, software builds, deployments, incidents, etc. Queries for
a time range return all events that overlap with the range and are often overlayed with other telemetry
results such as metrics.

1. What is the maximum duration of events supported? Days, months, years?
1. What model must events follow?
1. Refer to logs questions.

Currently only logs are supported in UQL.

### Traces

For this interview, traces refer to distributed tracing where an originating operation passes a context
to downstream processes that emit spans recording the duration of the operation and associated metadata.
The trace is composed of the spans and their relationships to each other.

1. What tracing models are supported by the query language?

OpenTelemetry model is supported by UQL. From a query model perspective, spans can be queried and turned into time series like:

```
spans count
| delta
| group_by [service.name], sum
```

And that same query could be used to return span exemplars. Another query model, is bringing back a list of traces. The following query will assemble a sample of traces from spans that match the predice:

```
spans_sample service.name == "web"
| assemble
```

1. What is the maximum duration of traces supported for querying? Minutes to hours to days?

This depends on the model. For time series queries from span data, this would be based on the entire retention period (up to 14 days in product). For assembling a list of sampled traces, this can be for the entire retention period but the spans assembled for a trace need to be within +- 30 minutes a part.

1. Are span links supported for supporting multiple traces that actually compose a longer trace?

This currently is not supported but we don't think there is anything in the language that is preventing this.

1. Are there limits to the # of spans per trace or dimensions per span in the model?

   For time series model, number of spans per trace or dimensions per span does not matter. For assembling a list of traces, the spans per trace are limited to 4,000. 

   1. Are there limits to the # of spans or traces at query time?

   See above. 

1. Can users query for sub graphs of traces? E.g. say select only traces that visited service A then
   B then fanned out to C and E but not D and called B at least 5 times.

   We have designs for this but it currently not implemented.

1. Are compound predicates supported such as traces that queried B from A with latencies over Xms?

   Compound predicates are supported. The following query will find all spans with the service.name web and latency greater than 100 milliseconds:

   ```
   spans count 
   | delta
   | filter service.name == "web" && latency > 100ms
   | group_by [operation], sum
   ```

   Relationship predicates have been designed but are currently not supported in UQL.

1. Can traces with different models be joined? E.g. one measures in seconds, another measures in millis.

Different models are normalized through our ingest path and not at query time.

1. Can incomplete traces be queried or only those that are considered or assumed complete?

Incomplete traces can be queried.

1. What aggregations are available for traces and spans? Histograms, percentiles, max, min, sum? 

All time series aggregations are available to for spans time series queries. In addition, any numeric attribute can be turned into a histogram for querying.

```
spans my.numeric.attribute
| delta
| group_by [], sum
| point percentile(value, 99)

spans my.numeric.attribute
| delta
| group_by [], sum
| point dist_count(value)
```

1. Can attributes be typed at query time for analysis (sums, count bys, etc)

   Yes, only for numeric attributes.

   1. If so, what happens to spans missing the attribute or have attributes with values of the wrong type?

   Spans missing the attribute or that are not a numeric type are skipped. 

### Profiles

Profiles are measurements of CPU, memory, disk, network, or other system resources by a process or set of
processes. They typically have a start and end time during which measurements are sampled so as not to
impact the process under measurement. 

1. What kind of profiles and models are supported by the language?

ServiceNow Cloud Observability does not support profiles at this time. With some design this could be supported in UQL.

1. What kind of filters are allowed? E.g. by duration, core, thread, function, environment variables?
1. Can users query by DAG, e.g. only show profiles where a user function wound up calling a sys call?
1. Can users create "diffs" with previous intervals based on similar attributes?
1. Can multiple profiles of the same type (cpu, memory, etc.) from different sources (instances) with
   the same process be aggregated?

## Metadata

For the purpose of this interview, we primarily refer to metadata as information about the data
in storage that is often used in UIs to assist in discovery. E.g. a list of values for a particular
metric tag or a list of extracted keys in a log index.

1. Does the same DSL for telemetry apply to metadata as well?

   Currently, it does not but could with design.

   1. If not, in what ways do the APIs or DSL differ when querying for metadata?
1. Are regular expressions supported?
   1. If so, what dialect and features are supported? E.g. POSIX, PCRE, etc.
   1. Are extraction groups to pull values or substrings out of the metadata supported?

## Permissions/Access Control

1. How does a query respond if a user is not allowed to access one or more components of a query
   but they are allowed access to other portions?
1. Do permissions apply to both metadata and data queries?