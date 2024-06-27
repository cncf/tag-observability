# Piped Processing Language DSL Survey Response

### **Short Description:**

PPL (Pipe Processing Language) is a query language used in OpenSearch, allowing users to interact with their data in a more expressive and readable manner. It features a structure similar to Unix's pipe commands, where operations are chained together using a pipe symbol (|). This design enables users to perform complex queries in a more intuitive way, such as filtering, transforming, and aggregating data. By leveraging PPL, developers can enhance their ability to extract insights from large datasets within the OpenSearch ecosystem.

The PPL (Pipe Processing Language) architecture within OpenSearch is built to facilitate querying and data manipulation in a way that resembles Unix's pipe commands.

### Overview

1. **Design Goals**:

    * **URI Friendliness**: 
      * Enables intuitive querying through RESTful API - Using [POST API](https://github.com/opensearch-project/sql/blob/main/docs/user/ppl/interfaces/endpoint.rst#post)
    * **Minimal Syntax**:
      * Human-readable and concise.
    * **Advanced Analytical Capabilities**:
      * Supports aggregation, filtering, etc. (See additional details in the following sections below)
    * **Easily extensible :** 
      * support simple and build in extension mechanics

   1. **Deficiencies in Other DSLs**:

       * Emphasize the pipe based data transformation patterns common to realtime analytics and batch processing
       * A need for a simpler, more consistent querying language led to the design of PPL.

       **Simplicity and Readability**: PPL introduces a more human-readable syntax, similar to the SQL language, allowing users to write queries in a more intuitive and straightforward manner.
       This enhances the usability for both newcomers and seasoned professionals.

       **Flexibility**: It offers various operators and functions that enable complex data processing tasks, like filtering, transforming, and aggregating data.
       This allows for more sophisticated analyses without the need for additional tools.

       **Performance Optimization**: PPL's query execution is optimized, enabling faster processing of large-scale data. It can leverage OpenSearch's distributed architecture to parallelize operations, thus speeding up query responses.
        
       [For Additional Info please review](https://github.com/opensearch-project/sql/blob/main/docs/user/ppl/RFC_%20Pipe%20Processing%20Language.pdf)
    
Integration with OpenSearch: Being tightly integrated with OpenSearch, PPL allows for seamless interaction with other features and plugins in the OpenSearch ecosystem.

Consistency across Observability Tools: By standardizing the query language, PPL ensures a consistent experience across various observability tools within the OpenSearch suite, minimizing the learning curve when transitioning between different tools.

Enhanced Debugging and Error Handling: PPL provides more informative error messages and debugging features, making it easier to identify and fix issues in queries.

1. **Languages that Inspired the DSL**:

    * SQL, and other structured query languages.
    * Splunk Query Language

1. **Observability Use Cases Designed For**:

    * Analyzing logs, metrics, and tracing data.

1. **Observability Use Cases Omitted**:

    * Joins are currently not supported in a full extent - Work In Progress

1. **Strengths and Weaknesses**:

    * **Strengths**: Flexibility, ease of learning.
    * **Weaknesses**: May lack some specific functionalities of other DSLs.

1. **Intended for At-Rest and/or Streaming Data**:

    1. _**At-Rest Data**:_
       At-rest data refers to data that is stored persistently on disk, and it's not in active use or transit.

       **Querying**: PPL enables querying this at-rest data, allowing users to perform analyses on historical data, generate reports, and derive insights.
       
       **Performance**: PPL's syntax and optimizations are designed to handle large-scale at-rest data efficiently.
       
       **Integration with OpenSearch**: Since PPL is integrated with OpenSearch, it can interact seamlessly with data indexed and stored within OpenSearch clusters.
   2. _**Streaming Data:**_
      Streaming data refers to data that is continuously generated, often by various sources like sensors, applications, or online services.

       **Real-Time Analysis**: PPL can be used to analyze streaming data as it arrives. This is essential for real-time monitoring, alerting, and decision-making.
       
       **Combination with At-Rest Data**: PPL's ability to handle both streaming and at-rest data enables complex analyses that combine real-time data with historical data. This integration can lead to more comprehensive insights.
       
       **Adaptability**: Since streaming data often comes in unbounded and fast-paced, PPL's flexibility in query formulation helps in adapting to the dynamic nature of this data.

1. **Source Specification**:

    * Users can specify indices or aliases or generic data-sources that abstract the tables as a logical raw data .

1. **Joining with Other Sources**:

    * Joining multiple indices is supported; joining with external sources like CSV is not yet supported.

1. **Differing Retentions in Time Series Sources**:

    * Query federation from Prometheus is supported
    * This would depend on the OpenSearch data management setup.

1. **Coupling to the Data Store Model (1 to 10)**:

    * 4, It's designed for OpenSearch but with some level of abstraction.

1. **Flexibility Across Different Storage Formats or Contexts**:

    * PPL is specific to OpenSearch and the underlying data structures it supports.
    * Work in progress to allow data read from object storage 

1. **Character Sets Supported**:

    * UTF-8.

1. **Special or Reserved Characters**:

    * Special characters like parentheses, commas, etc., have specific uses in PPL.

1. **Writing Data or Configuring the Backing Store**:

    * PPL is for querying only.

* * *

### **Metrics**

* **Supported Metric Measurement Types**:
    * Gauges, rates, counters, etc. PPL can work with different metric types both in OpenSearch and in Prometheus .
* **Handling Changes to Measurement Type Over Time**:
    * Changes in measurement type are handled at the data level; PPL queries the data as-is without managing type changes.
* **Supported Values as Metrics**:
    *  Double precision floating-point, integers, booleans, summary statistics, histogram bucket counts, etc.
* **Temporal Aggregation**:
    *  Supports custom aggregation with functions like
        * [COUNT](https://github.com/opensearch-project/sql/blob/main/docs/user/ppl/cmd/stats.rst#count)
        * [SUM](https://github.com/opensearch-project/sql/blob/main/docs/user/ppl/cmd/stats.rst#sum)
        * [AVG](https://github.com/opensearch-project/sql/blob/main/docs/user/ppl/cmd/stats.rst#avg)
        * [MAX](https://github.com/opensearch-project/sql/blob/main/docs/user/ppl/cmd/stats.rst#max)
        * [MIN](https://github.com/opensearch-project/sql/blob/main/docs/user/ppl/cmd/stats.rst#min)
        * [VAR_SAMP](https://github.com/opensearch-project/sql/blob/main/docs/user/ppl/cmd/stats.rst#var-samp)
        * [VAR_POP](https://github.com/opensearch-project/sql/blob/main/docs/user/ppl/cmd/stats.rst#var-pop)
        * [STDDEV_SAMP](https://github.com/opensearch-project/sql/blob/main/docs/user/ppl/cmd/stats.rst#stddev-samp)
        * [STDDEV_POP](https://github.com/opensearch-project/sql/blob/main/docs/user/ppl/cmd/stats.rst#stddev-pop)
        * [TAKE](https://github.com/opensearch-project/sql/blob/main/docs/user/ppl/cmd/stats.rst#take)
* **Timestamp Alignment**:
    * Typically aligned to the start of the window.
* **Boundaries**:
    *  Inclusive of the start, exclusive of the end.
* **Aggregation Functions for Downsampling**:
    * N/A - can use OpenSearch specific engine downsampling via [rollup](https://opensearch.org/docs/latest/im-plugin/index-rollups/index/)
* **Determining Correct Aggregation Type if Fixed**:
    * Not applicable as it's not fixed.
* **Querying Over Pre-Computed Temporal Aggregates**:
    * Both manual and automatic selection is supported, depending on the query and time range.

**Interpolation**

* **Interpolation Scheme**:
    * Depends on the OpenSearch settings and query configuration (schema on read).
* **User Selection of Interpolation Scheme**:
    *  Not typically user-configurable at query time.
* **Handling Missing Data**:
    * Represented internally as null, NaN, etc., depending on the context.
* **Handling Missing Data for Aggregations**:
    * Specific behavior depends on the aggregation function and data type.
* **Querying Across Different Retention Cutoffs**:
    * Managed at the data level; PPL doesn’t inherently handle this scenario.

**Identifiers**

* **Time Series Identifier Components**:
    * Metric name, namespace, tags, etc., depending on how the data is modeled (See [Simple Schema For Observability](https://github.com/opensearch-project/opensearch-catalog/tree/main/docs/schema/observability/metrics) ).
* **Supported Character Sets**:
    *  Typically UTF-8.
* **Dimensional Time Series ID Components**:
    * Metric names can be separate or a dimension; dimensions can have multiple values (Also See API access to Prometheus ).
* **Dimension Names, Requirements, and Types**:
    * Supported based on how they are defined in the data model.
* **Regular Expressions**:
    * Supported
* **Extraction Groups**:
    * Depending on the data and query structure, they may be supported.

*Keep in mind that OpenSearch PPL provides a querying interface, and some of the behaviors related to data modeling, aggregation, interpolation, and handling missing data might be influenced more by how the data is indexed, stored, and managed within OpenSearch rather than the PPL itself.*
*Information might vary depending on the specific version or configuration of OpenSearch being used.*
* * *
**Logs**

* **Incoming Log Event Model:**
    * Typically key-value maps with information like hostname, log level, timestamp, and message field.
    * Structured logs (e.g., JSON) are also common via [Simple Schema for Observability](https://github.com/opensearch-project/opensearch-catalog/tree/main/docs/schema/observability/logs) .
* **Multiline Log Entries:**
    * Can be handled, and behavior may vary depending on the configuration and specific requirements.
* **Special Handling for Stack Traces:**
    * No specific handling within PPL, but OpenSearch can index stack traces, and searching can be performed on specific lines or content.
    * Using [Simple Schema for Observability](https://github.com/opensearch-project/opensearch-catalog/tree/main/docs/schema/observability/logs) stack Trace has a structured field.
* **Field Extraction:**
    * Automatic extraction from structured log messages like JSON is supported, and [query-time field extraction](https://github.com/opensearch-project/sql/issues/359) is  possible.
* **Including Surrounding Lines in Results:**
    *  Not directly supported in PPL (supported within OpenSearch Dashboards ).
* **Full Text Searching**:
    *  Supported, including proximity, phrase, fuzzy queries, etc.
        * [MATCH](https://github.com/opensearch-project/sql/blob/main/docs/user/ppl/functions/relevance.rst#match)
        * [MATCH_PHRASE](https://github.com/opensearch-project/sql/blob/main/docs/user/ppl/functions/relevance.rst#match-phrase)
        * [MATCH_PHRASE_PREFIX](https://github.com/opensearch-project/sql/blob/main/docs/user/ppl/functions/relevance.rst#match-phrase-prefix)
        * [MULTI_MATCH](https://github.com/opensearch-project/sql/blob/main/docs/user/ppl/functions/relevance.rst#multi-match)
        * [SIMPLE_QUERY_STRING](https://github.com/opensearch-project/sql/blob/main/docs/user/ppl/functions/relevance.rst#simple-query-string)
        * [MATCH_BOOL_PREFIX](https://github.com/opensearch-project/sql/blob/main/docs/user/ppl/functions/relevance.rst#match-bool-prefix)
        * [QUERY_STRING](https://github.com/opensearch-project/sql/blob/main/docs/user/ppl/functions/relevance.rst#query-string)
* **Regular Expressions:**
    * Supported
* **Extraction Groups:**
    *  Can be implemented using regular expressions and other mechanisms.
* **Generating Metrics from Logs:**
    * Supported via appropriate queries and aggregations.
* **Basic Graphs Generation:**
    *  Possible through aggregations and visualizations in tools like OpenSearch Dashboards.
* **Writing Extraction Queries:**
    *  Supported; fields can be parsed from logs and aggregations applied.
* **Aggregations Supported**:
    *  Sum, min, max, count by, percentiles, etc.
* **Handling Wrong Types or Missing Values**:
    *  Behavior can vary; consult OpenSearch documentation for details.
* **Generating a DAG from Trace IDs**:
    *  Not inherently supported by PPL, but trace data can be queried and analyzed with external tools.
* **Tracing Support:**
    * Querying based on [Simple Schema for Observability Trace](https://github.com/opensearch-project/opensearch-catalog/tree/main/docs/schema/observability/traces)type
* **Output Formats Supported:**
    * Raw log lines, tables, etc., depending on the client and tools used.
* **Enrichment Support:**
    *  Merging or augmenting data can be achieved through ingestion pipelines or other pre-processing mechanisms.
* **Correlation and Fingerprinting:**
    *  Automatic fingerprinting is not directly provided in PPL, but custom solutions can be developed based on requirements (see [data-prepper](https://github.com/opensearch-project/data-prepper)).
* **Diffing Support:**
    * Comparisons over time can be done using appropriate queries and time filters, but specific "diffing" functionality is not inherently part of PPL.

* * *
**Events**

* **Maximum Duration of Events Supported:**
    * This depends on the data model and can potentially range from seconds to years.
* **Event Model**:
    *  Events must follow a structured data model, including start time and end time. Details can be similar to logs.

**Traces (Distributed Tracing)**

* **Tracing Models Supported:**
    * Simple schema for Observability Supported both by Observability Plugin & Ingestion pipelines such as data-prepper & fluent-bit
* **Maximum Duration of Traces Supported:**
    *  Depending on the model, various durations are possible.
* **Span Links:**
    * If the data includes links between spans, these can be queried.
    * [Observability-Dashboard](https://github.com/opensearch-project/dashboards-observability/wiki#trace-analytics) support these graphs out of the box.
* **Limits:**
    * May be constrained by the data model, indexing, and storage strategies.
* **Querying Sub Graphs:**
    *  Not direct API, possible through complex querying of the [span data](https://github.com/opensearch-project/opensearch-catalog/blob/main/schema/observability/traces/traces.mapping) index.
* **Compound Predicates:**
    * Predicates support:
      * [Basic Operators](https://github.com/opensearch-project/sql/blob/main/docs/user/ppl/functions/expressions.rst#basic-predicate-operator)
    * Supported based on how trace data is stored - mostly using the [span data](https://github.com/opensearch-project/opensearch-catalog/blob/main/schema/observability/traces/traces.mapping) index
* **Joining Different Models:**
    * Not directly supported - work in progress...
* **Querying Incomplete Traces:**
    * Partially supported - depending on data partiality
* **Aggregations for Traces and Spans:**
    *  Similar to logs; histograms, percentiles, max, min, sum, etc.
    * Using OpenSearch [Transformation API](https://opensearch.org/docs/latest/im-plugin/index-transforms/index/) this can be materialized
* **Attributes Typing at Query Time:**
    *  Supported, with handling similar to logs.

**Profiles (System Resources Measurement)**

* **Supported Profiles and Models**:
    * OpenSearch does not natively handle system profiles but can index and query profile data.
    * Future support is being added using the OpenTelemetry semantic convention
* **Filters:**
    *  By duration, core, thread, function, environment variables, etc.
* **Querying by DAG:**
    * Partly Supported by leveraging the data-prepper ingestion time services graph enrichment.
* **Creating "Diffs"**:
    *  Can be partially achieved with appropriate queries - specific "diffing" functionality is not inherently part of PPL.
* **Aggregating Multiple Profiles**:
    *  Supported through appropriate query and aggregation techniques.

**Metadata**

* **Applying DSL for Telemetry to Metadata:**
    * The DSL may be used to query metadata if it is stored and indexed in a compatible manner.
    * Specifically PPL supports a pluggable extension for adding DSL support for a specific datasource - [See Prometheus connector](https://github.com/opensearch-project/sql/blob/main/docs/user/ppl/admin/prometheus_connector.rst#ppl-query-support-for-prometheus-connector)
* **APIs or DSL Differences for Metadata:**
    * Might vary based on how metadata is managed and queried.
* **Regular Expressions Supported:**
    * Yes, similar to logs.
* **Extraction Groups:**
    *  Supported as in logs and other query types.

* * *

**Advanced Features**
 -  
 - 

## References

* [Main](https://github.com/opensearch-project/sql/tree/main/docs/user/ppl)
* [Commands](https://github.com/opensearch-project/sql/tree/main/docs/user/ppl/cmd)
* [Functions](https://github.com/opensearch-project/sql/tree/main/docs/user/ppl/functions)
* [Datatypes](https://github.com/opensearch-project/sql/blob/main/docs/user/ppl/general/datatypes.rst)
* [DataSources](https://github.com/opensearch-project/sql/blob/main/docs/user/ppl/admin/datasources.rst)


