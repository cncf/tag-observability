# Grafana Log Query Language DSL Survey Response

### **Short Description:**

A PromQL inspired query language for fetching and analyzing logging telemetry from Grafana
Loki.

### Overview

1. **List any over-arching design goals for the DSL. For example URI friendliness, minimal syntax,
   advanced analytical capabilities, etc.**:

   LogQL is a syntax heavily inspired by PromQL but for logs. The key design was to use pipe to 
   add processing log pipeline to the query like you would using `|`. Metric queries would only 
   be possible on pipeline using similar Prometheus function `avg by()`. `fn_over_time(select + pipeline [range])`

1. **What deficiencies or omissions in other DSLs lead to your decision to design a new language?**:

   We choose this DSL direction because it was already known by the Prometheus community, people would 
   only need to extend their knowledge to new log operator `|`, `|=`, etc…

1. **Were there any languages that inspired the DSL?**:

   PromQL, SPL

1. **Are there specific observability use cases the language was designed for?**:

   Log search and analytics.

1. **Are there specific observability use cases that were intentionally _omitted_ in the design?**:

   Are there any particular strengths or weaknesses in the language after observing it in use? 
   Metric queries forcing the users to go back to the first character is something we didn’t realize and is annoying.

1. **Is the language intended at-rest data and/or streaming data?**:

   Both.

1. **Can users specify a source in the query language? E.g. a specific table or database?**:

   They can specify a stream which is like tag search. So they can search within a source of logs but not 
   a connection or table as in SQL language

    1. **Can users join with other sources than the primary database? E.g. a CSV file, cloud databases, etc.?**:

       We thought about it but never got to it.

    1. **If joining of various time series sources is available, how are differing retentions handled?**:

       N/A

1. **How tightly coupled is the DSL to the data store model? (1 to 10 with 10 being extremely) tightly coupled)**:

   8 coupled

   1. **Is the DSL flexible enough to operate on data in different storage formats or contexts?**:

      Yes we’re actually currently reworking the format and storage right now and will keep the same language

1. **What character sets are supported by the DSL?**:

   Same as Prometheus

   1. **What characters are special or reserved in the DSL**:

      Same as Prometheus

1. **Does the DSL allow for writing data or configuring the backing store or is it for querying only?**:

   Querying only

### Logs

1. What does the incoming log event model look like for the DSL?

   Ts nano + line + resource labels (+ fields)

   Fields are experimental right now, and labels are indexes for searching sources.

1. Are log entries with multiple lines treated differently than single lines?

   No.

1. Is there special handling for stack traces? E.g. searching by line?

   No stacktraces are simply multiple entries with different line same timestamps.

1. Are fields extracted automatically from structured log messages (e.g. JSON or XML) or can fields be
   extracted with a query time hint?

   Fields can be extracted at query time using multiple parsers.
   Labels and Fields labels can also be extracted at collection time, labels are indexed not fields.
   We support popular log format parser and token parser for unstructured logs.

1. Can the DSL include surrounding lines in results when predicate matches are found?

   Not using a single query.

1. Is full text searching supported?

   Yes we support contains, regexes and other types of full search.

   1. If so, what types of queries are supported? E.g. proximity, phrase, fuzzy, etc.

      Contains words, regexes, wildcards and their respective negation.

1. Are regular expressions supported?

   Yes.

   1. If so, what dialect and features are supported? E.g. POSIX, PCRE, etc.

      Google RE2.

   1. Are extraction groups to pull values or substrings out of labels or lines supported?

      Yes.
   
1. Can users generate metrics from logs?

   Yes using over time functions.

   1. Can basic graphs be generated based on log level, fingerprint frequencies, etc.?

      Yes.
   
   1. Or can users write extraction queries to parse fields from logs and apply aggregations to them?

      Yes.
   
   1. What types of aggregations are supported? E.g. sum, min, max, count by, percentiles?

      Count, sum, rate, bytes_rate, min, max, quantile, stddev, stdvar, avg, first, last.

   1. When converting values to types (numeric or boolean, etc.) what happens when some lines have the wrong
      type or are missing?

      By default we error out to warn the users, but you can overpass it and it will just discard those lines.
   
1. Can the DSL generate a DAG from trace IDs written to logs?

   Not for now.

   1. If tracing is supported, can users query with parent/child or flow relationships?

      No.

1. What kind of output formats are supported? Raw log lines, tables, etc.?

   Raw log lines, then grafana support different views

1. Is enrichment supported, e.g. merging data from external sources to replace, say, customer IDs.

   No but grafana does that.

#### Correlation

1. Can log lines (particularly exceptions) be grouped based on automatic "fingerprinting" of content or
   can users provide a template? E.g. "user bob failed auth from IP 0.0.0.0" and "user alice failed auth from IP 1.2.3.4"
   should have the same fingerprint though the parameters (user and IP) differ.

   We have experimental support for patterns in the backend otherwise Grafana also supports this and 
   allows grouping at query time. You can also provide a pattern search.

1. Does the DSL support "diffing" meaning over two periods of time, were the more or fewer entries, more or fewer
   of a particular fingerprint, etc.

   No.

### Events

1. What is the maximum duration of events supported? Days, months, years?

   No limits.

1. What model must events follow?

   Same as logs.

## Metadata

1. **Does the same DSL for telemetry apply to metadata as well?**

   No metadata can be used in DSL but they are queried via other API without DSL.

   1. **If not, in what ways do the APIs or DSL differ when querying for metadata?**

      [Metadata APIs](https://grafana.com/docs/loki/latest/reference/loki-http-api/#query-labels)

1. **Are regular expressions supported?**

   Yes.

    1. **If so, what dialect and features are supported? E.g. POSIX, PCRE, etc.**

       RE2 a subset of PCRE.

    1. **Are extraction groups to pull values or substrings out of the metadata supported?**

       Yes.

## Permissions/Access Control

1. How does a query respond if a user is not allowed to access one or more components of a query
   but they are allowed access to other portions?

   It hides the data.

1. Do permissions apply to both metadata and data queries?

   Yes

## References

* [LogQL: Log Query Language](https://grafana.com/docs/loki/latest/query/)

## Thanks

Cyril Tovena and the Grafana Loki team