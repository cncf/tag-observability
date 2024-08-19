# TScript Query Language DSL Survey Response

### **Short Description:**

TScript is a DSL intended to operate on time series metrics, providing features independent of the
datastore.

1. **List any over-arching design goals for the DSL. For example URI friendliness, minimal syntax,
   advanced analytical capabilities, etc.**:

* Database independent: the manipulation of time series data should not depend on which database 
  returned the time series
* Easy to read: users should be able to quickly understand what the time series operation is doing
* Easy to write: users should be able to focus on the problem and not syntax
* Easy to add context aware help: easy for a system to understand what the user is doing to 
  provide help
* Easy to extend with additional functionality: easy to extend (for example, adding more time 
  series operations)
* Built-in alerting concepts

1. **What deficiencies or omissions in other DSLs lead to your decision to design a new language?**:

* Some DSLs hurt readability with nested functions and not multi-line
* Some overly complex for domain

1. **Were there any languages that inspired the DSL?**:

Python and Pandas inspired the DSL

1. **Are there specific observability use cases the language was designed for?**:

Only the use case for traditional time series metrics was considered.

1. **Are there specific observability use cases that were intentionally _omitted_ in the design?**:

No.

1. **Are there any particular strengths or weaknesses in the language after observing it in use?**:

In general, it is intuitive to use and easy to find functions to perform the type of 
manipulation users want.  One weakness is that the behavior of empty data is not intuitive 
to users.  There are multiple ways to deal with empty data which can lead to confusion.

1. **Is the language intended at-rest data and/or streaming data?**:

This is used for at-rest data.

1. **Can users specify a source in the query language? E.g. a specific table or database?**:

  1. **Can users join with other sources than the primary database? E.g. a CSV file, cloud databases, etc.?**:

  For TScript, the querying of the data is separate.  The data is expected to be in a dataframe 
  format when processing of TScript happens.

  1. **If joining of various time series sources is available, how are differing retentions handled?**:

  N/A

1. **How tightly coupled is the DSL to the data store model? (1 to 10 with 10 being extremely) tightly coupled)**:

The storage itself does not matter as long as the resulting data is put into a dataframe.

  1. **Is the DSL flexible enough to operate on data in different storage formats or contexts?**:

  Yes

1. **What character sets are supported by the DSL?**:

DSL consists of ASCII characters.

  1. **What characters are special or reserved in the DSL**:

  Parenthesis, arithmetic symbols, comparison operators, logical operators

1. **Does the DSL allow for writing data or configuring the backing store or is it for querying only?**:

This is only for querying.

## Data Models

### Metrics

1. What metric measurement types are supported? E.g. monotonic counters, gauges, deltas, rates,
   bucketed histograms, digests, booleans, etc.

The data is put into a Pandas Dataframe.  TScript itself has no knowledge of measurement types.

  1. How does the DSL handle changes to the measurement type over time for a single series?
     E.g. if a counter becomes a gauge during the query window?

  N/A

1. What values are supported as metrics? E.g. double precision floating point,
   integers, booleans, summaries (sum, min, max, count, etc.), histogram bucket counts,
   encoded digests, etc.

This is based on the backing datastore Goku. For this datastore, everything is exported 
before it is stored as a metric name, timestamp, value, and tags (kv pairs).  For example, 
histograms get exported into percentiles.  The system has no knowledge of what type of 
metric stored.


1. Does the language support custom or fixed temporal aggregation (downsampling, bucketing,
   windowing, consolidation) sizes?

Yes

  1. If so, are timestamps for the resulting values aligned to the start, end or middle of the
     window?

  Timestamps are aligned to the start of the window.

  1. Are boundaries inclusive or exclusive? E.g. A window from `(01:00 to 01:01]`

  `[01:00 to 01:01)`

  1. Are aggregation functions for downsampling fixed based on data types or are can users override
     the function? I.e. do queries focus on usability (user will get the correct answer for the data
     they are querying) or flexibility (users could choose a function not appropriate for the data
     type).

  Data type is all float so really comes down to user understanding of what the metric

  1. If aggregation is fixed, how is the correct aggregation type determined?

  User needs to know the type of data represented which is often part of the metric name 
  itself.  DSL does not have knowledge of this.

1. For DSLs that query over pre-computed temporal aggregates:

N/A

#### Interpolation

1. For DSLs that can aggregate "raw" data with misaligned timestamps:

  1. What interpolation scheme is used for various aggregation functions when series do not align
     on timestamp?

  TScript uses the Pandas interpolate function with the arguments method="linear" and 
  limit_area="inside"

  1. Can users select an interpolation scheme at query time?

  No

1. For DSLs that expect metrics to be bucketed at source:
  1. How is missing data for an interval emitted in the final output? (e.g. graph or JSON)

  Missing data is represented as a null which on a graph will show a discontinuous line.

  1. How is missing data represented internally during processing? E.g. as a null, a NaN, etc.

  `null`

  1. How is missing data handled for various aggregations? E.g. for a sum, if some series are missing
     data points are those missing points treated as zeros? Or the entire window omitted?

  This is configurable based on the function chosen.

    1. For averages, are missing values counted against the denominator?

    It depends on the function chosen.

#### Identifiers

1. What components constitute a time series identifier? E.g. metric name, namespace, tags, etc.

The query format is separate from TScript processing.  The query format is based on OpenTSDB 
like `aggregator:metric_name{k1=v1}`. This gets assigned a variable in TScript like m1 which 
can then be operated on in the DSL.

1. What character sets are supported by the identifiers?

ASCII characters are allowed.

1. For dimensional time series ID components (key/value pairs):
  1. If dimensional, are metric names a separate aspect from the dimensions or is the metric
     name simply another dimension?

  Metric names can be viewed as a table with dimensions the columns.

  1. Can dimensions have multiple values?

  Yes.

  1. Are dimension names (no value paired) supported?

  No

  1. Are dimensions required?

  Yes

  1. Are dimensions typed?

  No

1. Are regular expressions supported on identifier components (and which ones)?
  1. If so, what dialect and features are supported? E.g. POSIX, PCRE, etc.
  
  POSIX

  1. Are extraction groups to pull values or substrings out of labels supported?

  Yes

    1. If so can they be used in joins?

    Yes

## Permissions/Access Control

1. How does a query respond if a user is not allowed to access one or more components of a query
   but they are allowed access to other portions?

Access control is applied before access to DSL.

## References

## Thanks

Brian Overstreet, Principal engineer Pinterest