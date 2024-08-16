# Datadog Query Language DSL Survey Response

### **Short Description:**

Datadog has two major data platforms, which support slightly-different querying interfaces + 
querying DSLs. We have done some work to build some interfaces that support the same 
querying functionality over both platforms, but there are significant differences in their 
implementations, which the keen-eyed will be able to spot while using the product and 
especially when looking at our APIs.

* Metrics Platform stores time series data points each tagged with an arbitrary collection 
  of values and associated with a metric name that is unique to your org
* Events Platform stores infinite streams of arbitrary-structured data documents, each of 
  which can have tags as well as various depths of nested document structure

In general, I’ll attempt to answer these questions for both platforms, but where there are 
differences I’ll refer to “metrics” or “events”.

Around each of these DSLs we have built query APIs, which describe complete queries using 
JSON parameters. In these APIs, one of the values in the JSON would be something like 
“query” or “search” which would contain a string containing the DSL. So, properly speaking, 
the Datadog query system includes these API parameters around the DSLs - the DSLs alone 
are not sufficient to express all possible queries.

1. **List any over-arching design goals for the DSL. For example URI friendliness, minimal syntax,
   advanced analytical capabilities, etc.**:

User-friendliness, legibility, being able to read queries as if they were a sentence, 
supporting advanced querying capabilities, and being able to parse and translate into a 
UI representation

1. **What deficiencies or omissions in other DSLs lead to your decision to design a new language?**:

Metrics original implementation was done before there existed a wide range of observability 
products on the market. Events platform started from Lucene, but dropped a few features and 
made a few additions that weren’t available in Lucene.

1. **Were there any languages that inspired the DSL?**:

I think metrics took some inspiration from another observability tool that was around at the 
time of the company’s founding (the 2010-2012 period), but I don’t know the name. Events 
syntax is inspired by Lucene.

1. **Are there specific observability use cases the language was designed for?**:

Metrics -> time series filtering and aggregation; Events -> Log monitoring and distributed 
tracing (though we also use it for a fair few other products)

1. **Are there specific observability use cases that were intentionally _omitted_ in the design?**:

None intentionally omitted, some almost certainly accidentally omitted

1. **Are there any particular strengths or weaknesses in the language after observing it in use?**:

This is a tough one for me to answer because I don’t have much experience with other 
observability querying languages to compare with. In general, I think the strengths and 
weaknesses in our query systems are more properties of the systems themselves, than of the languages used as interfaces to those systems.

1. **Is the language intended at-rest data and/or streaming data?**:

I might not understand the question, but I think both. At least, by the time we’re querying it, 
the data is usually at rest, but for example the events query language can be used to 
filter the live event stream and this is used for features like intake-time processing and 
our “live tail” view.

1. **Can users specify a source in the query language? E.g. a specific table or database?**:

No, that’s specified as an out-of-band parameter.

Unless you count the metric name. But we treat “metrics” in its entirety as one source, and 
then metric names are like namespaces / sub-tables within that source.

  1. **Can users join with other sources than the primary database? E.g. a CSV file, cloud databases, etc.?**:

  As of relatively recently, yes. We added support for query-time joins to events and are in 
  the process of working on it for metrics. These joins are defined using query API parameters 
  and are not expressed within the DSLs themselves

  1. **If joining of various time series sources is available, how are differing retentions handled?**:

  I believe that they are simply not handled - I think we would just treat any periods where one 
  source didn’t have retained data as a missing / empty data set

1. **How tightly coupled is the DSL to the data store model? (1 to 10 with 10 being extremely) tightly coupled)**:

Metrics - probably a 8 or a 9; Events - more like a 5 or 6.

  1. **Is the DSL flexible enough to operate on data in different storage formats or contexts?**:

  Yes

1. **What character sets are supported by the DSL?**:

Unicode, in general I think we use UTF-8

  1. **What characters are special or reserved in the DSL**:

  Metrics -> `\s\t\n(){},&|!^*=:-”`
  Events -> `\s\t\n()[]{}!"”“:+-~*?\\`

1. **Does the DSL allow for writing data or configuring the backing store or is it for querying only?**:

No, querying only

## Data Models

### Metrics

1. What metric measurement types are supported? E.g. monotonic counters, gauges, deltas, rates,
   bucketed histograms, digests, booleans, etc.

count / rate / gauge / distribution 
[(global value distributions, implemented using sketches)](https://docs.datadoghq.com/metrics/types/?tab=distribution#metric-types)

Metric types are documented here: https://docs.datadoghq.com/metrics/types

  1. How does the DSL handle changes to the measurement type over time for a single series?
     E.g. if a counter becomes a gauge during the query window?

  The DSL doesn’t have a way of handling this - I think the query system might make a bit of a 
  mess of it. I think what would happen is the query would treat the metric as if all values 
  had the last-known measurement type

1. What values are supported as metrics? E.g. double precision floating point,
   integers, booleans, summaries (sum, min, max, count, etc.), histogram bucket counts,
   encoded digests, etc.

doubles, ints, and histogram bucket counts (sketches)

1. Does the language support custom or fixed temporal aggregation (downsampling, bucketing,
   windowing, consolidation) sizes?

It has a set of fixed bucket sizes which can be used, but accepts a bucket size parameter that 
can be any value. It will snap the incoming size parameter to the nearest member of the set of 
allowed sizes. The set spans a relatively wide range - from 1 second up to one week, including 
“nice” round intervals along the way (e.g. 10s, 1min, 10min, 1hr, 4hr, and so on)

  1. If so, are timestamps for the resulting values aligned to the start, end or middle of the
     window?

  Result timestamps are always aligned to the starts of the windows

  1. Are boundaries inclusive or exclusive? E.g. A window from `(01:00 to 01:01]`

  Inclusive of the start, exclusive of the end `[01:00 to 01:01)`

  1. Are aggregation functions for downsampling fixed based on data types or are can users override
     the function? I.e. do queries focus on usability (user will get the correct answer for the data
     they are querying) or flexibility (users could choose a function not appropriate for the data
     type).

  Users can override. They definitely can (and do) choose functions not appropriate for their data type.

  1. If aggregation is fixed, how is the correct aggregation type determined?

  N/A

1. For DSLs that query over pre-computed temporal aggregates:

N/A

#### Interpolation

1. For DSLs that can aggregate "raw" data with misaligned timestamps:

  1. What interpolation scheme is used for various aggregation functions when series do not align
     on timestamp?

  I’ll be honest I always forget exactly how the defaults work, but they’re documented here: 
  https://docs.datadoghq.com/metrics/guide/interpolation-the-fill-modifier-explained/. I think 
  it does linear interpolation, but only up to a certain size of gap, beyond which we just 
  leave a gap in the data.

  1. Can users select an interpolation scheme at query time?

  Yes, using the fill modifier https://docs.datadoghq.com/dashboards/functions/interpolation/


1. For DSLs that expect metrics to be bucketed at source:
  1. How is missing data for an interval emitted in the final output? (e.g. graph or JSON)

  I’m not sure if Datadog expects metrics to be bucketed at source, but: it’s represented as null

  1. How is missing data represented internally during processing? E.g. as a null, a NaN, etc.

  I think usually `NaN`, sometimes `null`

  1. How is missing data handled for various aggregations? E.g. for a sum, if some series are missing
     data points are those missing points treated as zeros? Or the entire window omitted?

  It depends on the metric type - for count metrics missing values are treated as zero, but 
  for gauge and rate metrics they’re treated as missing and the output window is also omitted

    1. For averages, are missing values counted against the denominator?

    I don’t know. I _think_ no but I am not certain about that at all unfortunately

1. If data retentions can differ between series, how does the DSL handle querying across series that
   span different retention cutoffs? E.g. series A has data but B has already been truncated.

I think that for metrics, retention is always 15 months, so this isn’t a concern (events are 
another matter, but those aren’t being considered here)

#### Identifiers

1. What components constitute a time series identifier? E.g. metric name, namespace, tags, etc.

The metric name and one unique set of tags form the unique time series identifier internally. 
Usually when querying in the DSL the metric name is treated as the identifier

1. What character sets are supported by the identifiers?

* Metric names must start with a letter.
* Metric names must only contain ASCII alphanumerics, underscores, and periods.
* Other characters, including spaces, are converted to underscores.
* Unicode is not supported.
* Metric names must not exceed 200 characters. Fewer than 100 is preferred from a UI perspective.

(source: https://docs.datadoghq.com/metrics/custom_metrics/#naming-custom-metrics)

1. For dimensional time series ID components (key/value pairs):
  1. If dimensional, are metric names a separate aspect from the dimensions or is the metric
     name simply another dimension?

  Yes, metric names are a separate aspect from the other dimensions (we call the other 
  dimensions “tags”)

  1. Can dimensions have multiple values?

  Yes. More accurately you can have multiple repetitions of the same `key:` on the same metric 
  time series at once, e.g. `partition:0`, `partition:1`, `partition:2`

  1. Are dimension names (no value paired) supported?

  Yes

  1. Are dimensions required?

  No

  1. Are dimensions typed?

  They’re always treated as strings, which I think means no they are not typed, because the 
  values in `key:value` pairs can’t be interpreted as numeric

1. Are regular expressions supported on identifier components (and which ones)?

No

### Logs

1. What does the incoming log event model look like for the DSL?

Basically arbitrary JSON documents, closest to option 2. In reality, we have a parsing / 
processing stage at intake that is configurable by users, where they can define how to parse 
incoming log messages into JSON documents. I think the default is to save a string with a 
timestamp and message.

1. Are log entries with multiple lines treated differently than single lines?

No, I think we coalesce the multiple lines together into the single log message. Although, I 
believe this somewhat depends on the instrumentation. It’s possible for logs to be sent to us 
as distinct lines that get treated as if they were different messages. I’ve seen this before 
with some messy stack trace logs for instance.

1. Is there special handling for stack traces? E.g. searching by line?

No, when stack traces are working correctly they’re treated as one long message (one that 
contains line breaks)

1. Are fields extracted automatically from structured log messages (e.g. JSON or XML) or can fields be
   extracted with a query time hint?

They are extracted at intake time by our processing system. This is fully configurable and a 
lot of mappings are applied there.

1. Can the DSL include surrounding lines in results when predicate matches are found?

No

1. Is full text searching supported?
  1. If so, what types of queries are supported? E.g. proximity, phrase, fuzzy, etc.

Yes. Phrase searches are supported, but I think not proximity or fuzzy search.

1. Are regular expressions supported?

No. These are supported at intake time (using a Grok parser) but not at query time.

1. Can users generate metrics from logs?

Yes

  1. Can basic graphs be generated based on log level, fingerprint frequencies, etc.?

  Yes

  1. Or can users write extraction queries to parse fields from logs and apply aggregations to them?

  Yes

  1. What types of aggregations are supported? E.g. sum, min, max, count by, percentiles?

  count | sum | avg | min | max | count unique | percentiles

  1. When converting values to types (numeric or boolean, etc.) what happens when some lines have the wrong
     type or are missing?

  I think there is a clever system for coercing types into the one that’s needed, but once in 
  a while it bites us and a customer is confused by their query results. I think non-coerceable 
  values are just omitted from the aggregation

1. Can the DSL generate a DAG from trace IDs written to logs?
  1. If tracing is supported, can users query with parent/child or flow relationships?

Traces are supported as a distinct data type in Datadog - this system does allow users to query 
with parent/child & flow relationships (docs here: https://docs.datadoghq.com/tracing/trace_explorer/trace_queries/) 
but it’s not based on the data from Logs, it’s a different corpus. It does use the same events 
query system though.

1. What kind of output formats are supported? Raw log lines, tables, etc.?

Raw log lines, time series, tables, various other visualization types

1. Is enrichment supported, e.g. merging data from external sources to replace, say, customer IDs.

Yes, at intake time since a long time, and recently we added query time enrichment as well.

#### Correlation

1. Can log lines (particularly exceptions) be grouped based on automatic "fingerprinting" of content or
   can users provide a template? E.g. "user bob failed auth from IP 0.0.0.0" and "user alice failed auth from IP 1.2.3.4"
   should have the same fingerprint though the parameters (user and IP) differ.

Yes. We call this “log patterns”: https://docs.datadoghq.com/logs/explorer/analytics/patterns/

1. Does the DSL support "diffing" meaning over two periods of time, were the more or fewer entries, more or fewer
   of a particular fingerprint, etc.

No, I don’t think so

### Events

I think Datadog doesn’t really support “events” according to this definition. We do have 
“events” as a distinct thing (a product, not referring to the platform) but that’s more 
intended for backend / service management events, and these are generally also treated as 
point-in-time things, like Logs. https://docs.datadoghq.com/service_management/events/. 
The data for events (the product) is stored in the events platform, a naming clash which 
causes some internal confusion from time to time.

### Traces

1. What tracing models are supported by the query language? 

I don’t really understand the question here. Our tracing model is documented here: 
https://docs.datadoghq.com/tracing/

1. What is the maximum duration of traces supported for querying? Minutes to hours to days?

I think it’s on the order of “hours”. We support long-running or asynchronous data jobs, for example.

1. Are span links supported for supporting multiple traces that actually compose a longer trace?

Yes, although I think the support right now is somewhat wonky

1. Are there limits to the # of spans per trace or dimensions per span in the model?
  1. Are there limits to the # of spans or traces at query time?

  Not that I know of - sometimes really large traces give us headaches on the UI side

1. Can users query for sub graphs of traces? E.g. say select only traces that visited service A then
   B then fanned out to C and E but not D and called B at least 5 times.

Yes, we call this Trace Queries: https://docs.datadoghq.com/tracing/trace_explorer/trace_queries/ 

1. Are compound predicates supported such as traces that queried B from A with latencies over Xms?

Yes, I think this feature was added recently to trace queries

1. Can traces with different models be joined? E.g. one measures in seconds, another measures in millis.

I don’t think we support traces with different models, but I don’t know which model we _do_ use.

1. Can incomplete traces be queried or only those that are considered or assumed complete?

You can query over individual spans, which I think is possible to do before the trace is fully 
complete. So, I think the answer here is “yes, incomplete traces can be queried”

1. What aggregations are available for traces and spans? Histograms, percentiles, max, min, sum?

count | sum | avg | min | max | percentiles

1. Can attributes be typed at query time for analysis (sums, count bys, etc)
  1. If so, what happens to spans missing the attribute or have attributes with values of the wrong type?

Yes, generally span attributes can be treated as numeric at query time. The type coercion logic is 
the same clever rules used by Logs

### Profiles

1. What kind of profiles and models are supported by the language?

Wall time, memory usage, allocations, and more depending on the language runtime being profiled

https://docs.datadoghq.com/profiler/profile_types/?code-lang=go 

1. What kind of filters are allowed? E.g. by duration, core, thread, function, environment variables?

Yes, all of the above I believe

1. Can users query by DAG, e.g. only show profiles where a user function wound up calling a sys call?

We aggregate profiles together, and in the profile aggregation and exploration view it’s 
possible to query over profile structure. But, I think this does not include sampling only 
certain profiles based on their structural characteristics. I might be wrong though, the 
profiling product has a large depth of features. 
https://docs.datadoghq.com/profiler/profile_visualizations/ 

1. Can users create "diffs" with previous intervals based on similar attributes?

Yes, in the profiling compare view (this is powered by an API, not by the profiling query DSL, I think)  
https://docs.datadoghq.com/profiler/compare_profiles

1. Can multiple profiles of the same type (cpu, memory, etc.) from different sources (instances) with
   the same process be aggregated?

Yes. The main profile viewer is based on aggregated profiles

## Metadata

1. Does the same DSL for telemetry apply to metadata as well?
  1. If not, in what ways do the APIs or DSL differ when querying for metadata?

Generally not - the APIs are generally somewhat simpler in terms of their query options than 
the DSLs are.

1. Are regular expressions supported?

No

## Permissions/Access Control

1. How does a query respond if a user is not allowed to access one or more components of a query
   but they are allowed access to other portions?

I believe the entire query would error out with a 403 error, but I’m not 100% sure that’s the 
case. For some Logs queries I think that some data is simply not considered present or 
available, for users who don’t have access to that data. So, the query system would simply 
omit this Logs data from that user’s queries.

1. Do permissions apply to both metadata and data queries?

Yes, we hide the metadata from the metadata APIs based on the same rules as we hide the 
data itself

## References

## Thanks

Mark Hintz, staff engineer covering graphing and query interfaces