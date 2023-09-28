# Prometheus Query Language DSL Survey Response

### **Short Description:**

The Prometheus Query Language (PromQL) DSL is widely used for metrics and alerting, originating from
the Prometheus monitoring solution. A number of vendors have adopted the language for interoperability
and various extensions exist to work with non-metric data types.

### Overview

1. **List any over-arching design goals for the DSL. For example URI friendliness, minimal syntax,
   advanced analytical capabilities, etc.**:

   * Optimize for common metrics-based systems monitoring use cases. Don't try to solve every use 
     case under the sun that isn't systems monitoring or close to it.
   * Support not only dashboarding and ad-hoc querying, but also fully integrate alerting use cases 
     with the query language.
   * VECTOR MATH! Leverage the dimensional data model (labels) not only for flexible data selection, 
     but especially also for correlating / joining entire sets of metrics together on compatible label 
     sets without a lot of syntax: binary arithmetic, binary filter operators, binary set operators. Very 
     important for quickly calculating sets of ratios, sums, etc. between correlated series 
     (e.g. 100 disk usages divided by their respective disk sizes to get 100 labeled disk usage ratios).
   * Terse, functional syntax that's quick to write and read.
   * Functional language used only for reading, writes are handled out of band (e.g. via scrapes).
   * Deep analytical capabilities kept to a minimum (at least for a start), again, mainly focused on live 
     systems monitoring use cases and less on deep data crunching / ML / statistics.
   * Absolute timestamps (e.g. begin and end of a graph range) mostly kept out of the language 
     (the PromQL query text) itself and sent as a separate set of parameters. PromQL expressions mostly 
     just look backward some time range from the current evaluation step along the range of a graph 
     (or from a single evaluation step in the case of an instant query or rule query).

1. **What deficiencies or omissions in other DSLs lead to your decision to design a new language?**:

   Prometheus was created at SoundCloud in 2012, coming from multiple years of Google.

   * In 2012, most open-source TSDBs didn't have any query language at all. And alerting systems like 
     Nagios didn't even really have time series.
   * Graphite was the closest thing to having a time series query language, but:
     
     * It mixed data calculation and display concerns to a large degree.
     * It didn't allow any kind of complex math between sets of correlated series (vector math).
     * It didn't support a dimensional data model or the scale and dynamism that we needed.
     * It wasn't meant for alerting in any way, although some people bolted alerting on top of it.

  * A SQL-style language seemed very cumbersome for the way we wanted to deal both with vector math 
    (automatic joins on all labels) and time parameters. InfluxDB later tried a SQL-style language for 
    TSDB data and ended up regretting it.

1. **Were there any languages that inspired the DSL?**:

   PromQL and Prometheus were heavily inspired by Google's Borgmon monitoring system that we had used 
   at Google in the years before joining SoundCloud. Basically we missed a similar system for our job 
   at SoundCloud and started building Prometheus and PromQL with a very similar architecture and design. 
   PromQL has diverged from and added to the Borgmon query language in major ways by now, but especially 
   the core principles such as the dimensional data model and the vector math / correlation of time series 
   are basically the same.

1. **Are there specific observability use cases the language was designed for?**:

   Metrics-based systems monitoring in dynamic environments with a lot of dimensionality in the metrics 
   data, as well as potentially many short-lived time series (e.g. Kubernetes pods appearing and disappearing, etc.).

1. **Are there specific observability use cases that were intentionally _omitted_ in the design?**:

   Prometheus and PromQL are 100% focused on time series / metrics. So no traces, logs, events, and the 
   like, for which you'll still want to run some other system.

1. **Are there any particular strengths or weaknesses in the language after observing it in use?**:

   **Strengths:**

   Mainly just refer back to the design goals here, which I think have been largely fulfilled and have been 
   very useful for flexible and powerful queries on dimensional data. Especially the syntactically brief but 
   powerful vector math / binary operators were new at the time and are still awesome (modulo the caveats 
   mentioned below).

   **Weaknesses:**

   * PromQL looks and works differently from many other languages, especially if you are expecting something SQL-like 
     or something where the query text itself contains all absolute timestamps / time ranges for the overall query as 
     well (these are sent separately from the query text for PromQL). This can make it a bit of a learning hurdle at 
     first. However, I think this was probably necessary.
   * It's too easy to write PromQL expressions that accidentally turn out empty (without returning an error or warning). 
     For example, by referencing a metric or label combination for which there is simply no data. Or when getting binary 
     operator matching modifiers slightly wrong between sets of time series (vectors) that don't have compatible label 
     sets. This can get annoying especially when you build very deeply nested queries, and you don't know which part 
     makes the entire query result become empty. I've built tools like https://promlens.com/ (now OSS, part of the 
     Prometheus project) to help visualize the structure and data within each part of a query to help with this 
     and some other issues. Unless one introduces a super rigid schema into the expected data and the selection process 
     though, I'm not sure how to 100% "fix" this without making everything super verbose or cumbersome in other ways.
   * Related to the above point, alerting rule outputs are considered "ok" if their PromQL expression returns an empty 
     result (on the flip side, any output series that do get returned are treated as alerts). This means that in the 
     worst case your alerting rules will silently fail if you are accidentally producing empty outputs vs. things 
     actually being ok.
   * PromQL is relatively weak on the "deep statistics" front, e.g. doing more ML-y or deeper statistical analysis on 
     data. More focused on live monitoring.
   * Some more namespacing for metrics or labels (and/or well-known metric or label names) might have helped to build 
     automatic and standardized tooling (dashboards, alerts, etc.) around things.

1. **Is the language intended at-rest data and/or streaming data?**:

   At-rest data, though it's usually processing very recent data (e.g. to alert on what has happened in the last few minutes).

1. **Can users specify a source in the query language? E.g. a specific table or database?**:

   Not directly as part of the language itself, but there's ways to configure Prometheus to query external databases for 
   certain vector selectors (see https://www.robustperception.io/promql-queries-against-sql-databases-using-a-read-adapter/ - 
   this is not super common though).

    1. **Can users join with other sources than the primary database? E.g. a CSV file, cloud databases, etc.?**:

       See above, it's not common but can be done.

    1. **If joining of various time series sources is available, how are differing retentions handled?**:

       This depends on the operation. Generally, a PromQL selector will select whatever data is available for the specified 
       filters and time ranges and not return an error or anything like that if it goes outside of a retention window where 
       old data has already been deleted (which it knows nothing about) - that part of the data range will just be empty, 
       and then it depends on whether you just display the data from both sources (one will be gappy, the other not) or 
       try to join them together somehow (in which case the entire result might become empty, but only for the respective 
       time range where data from one source is missing).

1. **How tightly coupled is the DSL to the data store model? (1 to 10 with 10 being extremely) tightly coupled)**:

   The interface between the PromQL query engine and the underlying TSDB is relatively simple and allows for switching out 
   or extending the underlying TSDB implementation with something compatible (which has been done in multiple projects, e.g. 
   Thanos, Cortex/Mimir, or M3).

   The PromQL<->TSDB interface only requires:

   * Getting all label values for a set of matchers (within a given time range)
   * Getting all label names for a set of matchers (within a given time range)
   * Getting all series samples for a set of matchers (within a given time range)

   1. **Is the DSL flexible enough to operate on data in different storage formats or contexts?**:

      Generally PromQL does not care about the storage format at all, as long as it can access the TSDB via the 
      interface outlined above.

1. **What character sets are supported by the DSL?**:

   Generally, PromQL strings and label values can contain any Unicode characters, whereas metric names 
   ("[a-zA-Z_:][a-zA-Z0-9_:]*") and label names ("[a-zA-Z_][a-zA-Z0-9_]*") are more restricted in their character set. 
   See: https://prometheus.io/docs/concepts/data_model/ for details.

   There are ongoing discussions for potentially allowing arbitrary characters via some escaping scheme.

    1. **What characters are special or reserved in the DSL**:

       See: https://prometheus.io/docs/concepts/data_model/

1. **Does the DSL allow for writing data or configuring the backing store or is it for querying only?**:

   PromQL is for querying / reading only. Writes happen via a different path, e.g. data being scraped by Prometheus 
   or being deleted automatically after some configured retention time has passed.

## Metrics

1. **What metric measurement types are supported? E.g. monotonic counters, gauges, deltas, rates, bucketed
   histograms, digests, booleans, etc.**

   * Cumulative / monotonic counters (can occasionally reset to 0 when the process that tracks the counter restarts)
   * Gauges
   * "Classic" histograms: Histogram buckets exposed as one time series per bucket
   * Native exponential histograms: Still experimental but getting more stable, entire histogram stored directly in 
     the sample value of a single series.
   * Summaries (which are really just a bunch of gauges containing counts, sums, and quantiles, so nothing in PromQL 
     actually knows that they represent a "Summary" metric in aggregate)

   1. **How does the DSL handle changes to the measurement type over time for a single series? E.g. if a counter
      becomes a gauge during the query window?**

      From the point of PromQL, counters, gauges, classic histograms, and so on are all just float64 values, and 
      the TSDB currently does not even permanently store the metric type for those. The only exception to this are 
      the new native histograms, where a sample value can now not just be a float64, but an entire encoded histogram. 
      Behavior of various PromQL functions if a series switches between float64 and native histogram over time is 
      still not 100% fleshed out, as native histograms are still being added / experimental.

1. **What values are supported as metrics? E.g. double precision floating point, integers, booleans, summaries
   (sum, min, max, count, etc.), histogram bucket counts, encoded digests, etc.**

   * Float64 for counters, gauges, etc.
   * Entire exponential histograms (buckets) for native histograms.



## References

* [Querying Prometheus](https://prometheus.io/docs/prometheus/latest/querying/basics/)

## Thanks

Julius Volz and the Prometheus developers.

