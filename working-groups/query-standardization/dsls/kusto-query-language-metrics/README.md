# Kusto Query Language, Metrics Variant DSL Survey Response

### **Short Description:**

The Kusto Query Language for metrics(KQL-M) DSL is a variant of the Kusto Query Language (KQL) DSL that 
used in Azure Data Explorer, internal to Microsoft focusing on metrics data.

### Overview

1. **List any over-arching design goals for the DSL. For example URI friendliness, minimal syntax,
   advanced analytical capabilities, etc.**:

   Primary goals were around defining language with user-friendly syntax/semantics and sufficient analytical 
   capabilities (mostly around data filtering, aggregation, custom computations, and correlations). At 
   scale performance efficiency was also one of the goals.

1. **What deficiencies or omissions in other DSLs lead to your decision to design a new language?**:

   The primary language of comparison was PromQL, thus one of the goals was to gain corresponding functional 
   parity. Still, PromQL syntax was considered as a challenge for end users because it required extra learning. 
   Thus the syntax was inherited from another DBMS language which is very popular internally (it is also exposed 
   outside as Azure Data Explorer). Also worth mentioning is that PromQL philosophy of 'expression for a single 
   data point' contradicted to existing data and execution model. Thus the new language expression was 
   expected to define entire resultant data set (vectors shape).

1. **Were there any languages that inspired the DSL?**:

   Azure Data Explorer query language which is very popular inside Microsoft.

1. **Are there specific observability use cases the language was designed for?**:

   Alerting, dashboarding, data analytics, streaming.

1. **Are there specific observability use cases that were intentionally _omitted_ in the design?**:

   The language was strictly bounded to metrics data model and was not intended to perform correlations with 
   logs, traces, etc. Unifying these data models was considered as a risk, especially for target scenarios of 
   efficiency at scale.

1. **Are there any particular strengths or weaknesses in the language after observing it in use?**:

   Inheriting the KQL syntax was both good and bad for us. Users were accepting the language much easier 
   as the overall syntax and semantics were well known. Still, the difference of tabular vs. metrics data models 
   lead to some deviations in both syntax and semantics which caused confusions.

1. **Is the language intended at-rest data and/or streaming data?**:

   Both.

1. **Can users specify a source in the query language? E.g. a specific table or database?**:

   Not yet, but there are no blockers to introduce it in the future (as long as the source data can be represented 
   as time series).

    1. **Can users join with other sources than the primary database? E.g. a CSV file, cloud databases, etc.?**:

       Not yet.

    1. **If joining of various time series sources is available, how are differing retentions handled?**:

       N/A.

1. **How tightly coupled is the DSL to the data store model? (1 to 10 with 10 being extremely) tightly coupled)**:

   It is not really coupled to data store, but to the metrics data model (i.e. vectors of datapoints).

    1. **Is the DSL flexible enough to operate on data in different storage formats or contexts?**:

       Yes as long as data can be converted to time series/vector format.

1. **What character sets are supported by the DSL?**:

   UTF-8 for data.

    1. **What characters are special or reserved in the DSL**:

       See [Entity Names](https://learn.microsoft.com/en-us/azure/data-explorer/kusto/query/schema-entities/entity-names)

1. **Does the DSL allow for writing data or configuring the backing store or is it for querying only?**:

   Intentionally DQL only (i.e., read-only, no DDL/DML semantics).

## Metrics

1. **What metric measurement types are supported? E.g. monotonic counters, gauges, deltas, rates, bucketed 
   histograms, digests, booleans, etc.**

   The metric type is intentionally ignored as each datapoint represents point in time measurement. Still, datapoints 
   can be of several types (e.g., double, histograms, etc.). Type enforcement semantics are the only restriction and 
   it is up to user to make sense of the data (i.e., apply proper aggregations, vector functions, etc.).

   1. **How does the DSL handle changes to the measurement type over time for a single series? E.g. if a counter 
      becomes a gauge during the query window?**

      Does not matter, as datapoints do not hold such metadata.

1. **What values are supported as metrics? E.g. double precision floating point, integers, booleans, summaries 
   (sum, min, max, count, etc.), histogram bucket counts, encoded digests, etc.**

   Datapoints can be of type double, histogram, other.

1. **Does the language support custom or fixed temporal aggregation (downsampling, bucketing, windowing, 
   consolidation) sizes?**

   Custom temporal aggregation windows + function.

   1. **If so, are timestamps for the resulting values aligned to the start, end or middle of the window?**

      The result is a vector which represents datapoints requested from start to end time with a specific step.

   1. **Are boundaries inclusive or exclusive? E.g. A window from (01:00 to 01:01]**
   
      Inclusive.

   1. **Are aggregation functions for downsampling fixed based on data types or are can users override 
      the function? I.e. do queries focus on usability (user will get the correct answer for the data they are 
      querying) or flexibility (users could choose a function not appropriate for the data type).**

      Driven by type enforcement. E.g., 'histogram' aggregation function can be applied to 'double vectors' or 
      'histogram vectors'.
   
      1. **If aggregation is fixed, how is the correct aggregation type determined?**

         It depends on semantics of specific function. Incoming datatype may define output datatype, or 
         output can be fixed (e.g., 'percentile' function can take both histogram and double vectors, 
         but output is always double vector).

1. **For DSLs that query over pre-computed temporal aggregates:**
   
   1. **Can users manually select the aggregate to select from (e.g. choose between 1 minute 
      sampling, 1 hour sampling, etc.)?**
   
      N/A
   
   1. **If automatically selected, what rules determine the correct aggregate to query?**
   
      N/A

### Interpolation

1. **For DSLs that can aggregate "raw" data with misaligned timestamps:**

   1. **What interpolation scheme is used for various aggregation functions when series do not 
      align on timestamp?**

      Interpolation is not used implicitly. User may explicitly request interpolation as a vector 
      function though.

   1. **Can users select an interpolation scheme at query time?**

      Not yet.

1. **For DSLs that expect metrics to be bucketed at source:

   1. **How is missing data for an interval emitted in the final output? (e.g. graph or JSON)**

      Data can be bucketed at source and at query time. Double NaN is used to represent missing 
      datapoint in the final output.

   1. **How is missing data represented internally during processing? E.g. as a null, a NaN, etc.**

      Double NaN is used to represent missing datapoint internally.

   1. **How is missing data handled for various aggregations? E.g. for a sum, if some series are 
      missing data points are those missing points treated as zeros? Or the entire window omitted?**

      Missing datapoints are ignored upon aggregation. User must explicitly replace nulls with 
      something (via vector function) if they want different behavior.

      1. **For averages, are missing values counted against the denominator?**
      
         Not counted.

1. **If data retentions can differ between series, how does the DSL handle querying across series 
   that span different retention cutoffs? E.g. series A has data but B has already been truncated.**

   Missing data is represented by nulls (NaN).

### Identifiers

1. **What components constitute a time series identifier? E.g. metric name, namespace, tags, etc.**

   Account, namespace, metric name, tags (aka dimensions).

2. **What character sets are supported by the identifiers?**

   Alphanumeric

3. **For dimensional time series ID components (key/value pairs):**

   1. **If dimensional, are metric names a separate aspect from the dimensions or is the metric name 
      simply another dimension?**

      Metric name and dimensions are separate
   
   1. **Can dimensions have multiple values?**

      Single time series can have a single dimension value.

   1. **Are dimension names (no value paired) supported?**
   
      No. Dimensions must have a value.

   1. **Are dimensions required?**
   
      Optional.

   1. **Are dimensions typed?
   
      Yes, as strings.

1. **Are regular expressions supported on identifier components (and which ones)?**

   Intentionally prohibited now because of perf/security consolidations. Might be added later. 
   Multiple string functions like `strcat`, `substr`, `strlen`, `indexof`, etc. are available though.

   1. **If so, what dialect and features are supported? E.g. POSIX, PCRE, etc.**

      N/A

   1. **Are extraction groups to pull values or substrings out of labels supported?**

      N/A

      1. **If so can they be used in joins?**

         Joins are limited to 'full dimension values match'. Still, the user is able to define 
         arbitrary dimensions at query time. The value for these dimensions can be defined as expressions 
         on top of incoming data (both dimensions and datapoints).

## References

* [KQL Overview](https://learn.microsoft.com/en-us/azure/data-explorer/kusto/query/)

## Thanks

Sergey Mudrov and the Microsoft Observability teams.

