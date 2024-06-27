# Grafana Trace Query Language DSL Survey Response

### **Short Description:**

A query language for fetching and analyzing distributed tracing telemetry fron Grafana
Tempo.

### Overview

1. **List any over-arching design goals for the DSL. For example URI friendliness, minimal syntax,
   advanced analytical capabilities, etc.**:

   TraceQL was primarily designed to be a minimal syntax distributed tracing and OpenTelemetry 
   native query language. We valued the interactivity and iterative exploration that other 
   DSLs have given to telemetry signals and we wanted a similar experience for distributed tracing.

1. **What deficiencies or omissions in other DSLs lead to your decision to design a new language?**:


1. **Were there any languages that inspired the DSL?**:

   PromQL/LogQL

1. **Are there specific observability use cases the language was designed for?**:

   The language was specifically designed to explore and gain insight from distributed tracing data. 
   We were particularly interested in directly integrating the unique structural nature of tracing 
   into the language.

1. **Are there specific observability use cases that were intentionally _omitted_ in the design?**:

   The language can search for single spans and simple structural relationships with very compact 
   and powerful expressions. Complex structural relationships are possible to express but can be 
   difficult to understand at first glance.

1. **Are there any particular strengths or weaknesses in the language after observing it in use?**:

    * **Strengths**:
      
      One strength is the succinct and direct ways you can ask for single spans and relationships 
      between them. Structural operators allow for powerful and intuitive ways to ask for things 
      like "errors beneath endpoint /foo":
      `{ span.url.path = "/foo" } >> { status = error }`
   
      Another strength would be the clear relationship with OpenTelemetry. The SDK, pipeline 
      (otel collector), data and query language all reflect the same object model and concepts to reduce confusion.
   
    * **Weaknesses**:

      Succinct structural operators can be powerful but can get confusing when asking for more complex relationships. 
      We can use the example above on finding a trace where `foo` calls `bar` but not through `baz`.
    
      Another one I'm struggling with a bit is how to express queries around links, events and arrays (sub 
      elements of a span with a many to 1 relationship to the span.) We structured the language around asserting 
      expressions on spans, but could we have done something else? What about something like event
      `{ name = "foo" && .attribute = "bar" }`? Current we've added support for querying event fields in the 
      TraceQL extensions, but we're noodling how to make those queries more expressive

1. **Is the language intended at-rest data and/or streaming data?**:

   At rest, but most operations could be performed on streaming data.

1. **Can users specify a source in the query language? E.g. a specific table or database?**:

   No

   1. **Can users join with other sources than the primary database? E.g. a CSV file, cloud databases, etc.?**:

      No

   1. **If joining of various time series sources is available, how are differing retentions handled?**:
   
      N/A

1. **How tightly coupled is the DSL to the data store model? (1 to 10 with 10 being extremely) tightly coupled)**:

   4

   1. **Is the DSL flexible enough to operate on data in different storage formats or contexts?**:

      Yes. We have intentionally exposed only 1 detail of the underlying format. It is generally format agnostic.

1. **What character sets are supported by the DSL?**:

   1. **What characters are special or reserved in the DSL**:

1. **Does the DSL allow for writing data or configuring the backing store or is it for querying only?**:

   Querying only

### Traces

1. **What tracing models are supported by the query language?**

   TraceQL primarily supports OpenTelemetry and uses the OTel translation layers to also 
   support Jaeger and Zipkin.

1. **What is the maximum duration of traces supported for querying? Minutes to hours to days?**

   No max duration.

1. **Are span links supported for supporting multiple traces that actually compose a longer trace?**

   Basic support is defined in the language, but not yet implemented.

1. **Are there limits to the # of spans per trace or dimensions per span in the model?**

   The language does not have these limitations. The backing implementation, Tempo, does have 
   total trace size limitations. Tempo stores traces contiguously for structural analysis, this 
   creates max size limits on the traces for practicality. In large installations this is often ~50MB.

   1. **Are there limits to the # of spans or traces at query time?**

      Same answer as above.

1. **Can users query for sub graphs of traces? E.g. say select only traces that visited service A then
   B then fanned out to C and E but not D and called B at least 5 times.**

   Yes. The language supports a set of structural operators that answer these questions.

1. **Are compound predicates supported such as traces that queried B from A with latencies over Xms?**

   Yes. `{ A } > { B && duration > Xms }`

1. **Can traces with different models be joined? E.g. one measures in seconds, another measures in millis.**

   The language does not restrict this, but the backing implementation stores all traces in the OTel format.

1. **Can incomplete traces be queried or only those that are considered or assumed complete?**

   Incomplete traces can be queried.

1. **What aggregations are available for traces and spans? Histograms, percentiles, max, min, sum?**

   TraceQL Metrics is in development now. A basic rate() function exists in the latest release in an 
   experimental state.

1. **Can attributes be typed at query time for analysis (sums, count bys, etc)**

   Yes.

   1. **If so, what happens to spans missing the attribute or have attributes with values of the wrong type?**

   They are ignored.

## Metadata

1. **Does the same DSL for telemetry apply to metadata as well?**

   No.

   1. **If not, in what ways do the APIs or DSL differ when querying for metadata?**

      Tempo provides a set of dedicated endpoints to query metadata. (Attribute names and values)

1. **Are regular expressions supported?**

   Yes.

   1. **If so, what dialect and features are supported? E.g. POSIX, PCRE, etc.**

      RE2 a subset of PCRE.

   1. **Are extraction groups to pull values or substrings out of the metadata supported?**

      No.

## References

* [Query with TraceQL](https://grafana.com/docs/tempo/latest/traceql/)
* [TraceQL Design Concepts](https://github.com/grafana/tempo/blob/main/docs/design-proposals/2022-04%20TraceQL%20Concepts.md)
* [TraceQL Extensions](https://github.com/grafana/tempo/blob/main/docs/design-proposals/2023-11%20TraceQL%20Extensions.md)
* [TraceQL Metrics](https://github.com/grafana/tempo/blob/main/docs/design-proposals/2023-11%20TraceQL%20Metrics.md)

## Thanks

Joe Elliott and the Grafana Tempo team