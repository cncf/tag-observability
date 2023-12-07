# New Relic Query Language DSL Survey Response

### **Short Description:**

New Relic Query Language (NRQL) is a SQL-like query language for querying time series data. It is 
capable of working with events, metrics, spans and log data.

### Overview

1. **List any over-arching design goals for the DSL. For example URI friendliness, minimal syntax, 
     advanced analytical capabilities, etc.**:

   The primary original design goal is to be a familiar language to those who have worked with SQL databases. 
   NRQL was fairly early to the game of observability-specific languages (~2013), and this was the largest 
   audience to target for an easy transition, while avoiding misconceptions about behavior (e.g. FACET != GROUP_BY).

   Today, the language is attempting to strike a balance between being familiar to SQL writers and 
   maintaining its original structure for continuity, while being approachable to anyone. Both attempts to 
   make syntax and features simple and intuitive, while having depth for less intuitive problems if the user 
   seeks it out. Common questions should be simple queries.

1. **What deficiencies or omissions in other DSLs lead to your decision to design a new language?**:

   We chose not to explicitly tie ourselves to SQL because NRQL is a distributed language from the ground up. 
   Many features available in SQL cannot be developed with the same semantics or at all, and SQL is far too 
   intertwined with other products to be agile for our own customer needs. Additionally, we wanted to make more 
   observability-specific features (e.g. TIMESERIES, SINCE / UNTIL clauses, etc) which don't exist in SQL.

   There were not many distributed languages at the time, and other observability-specific languages like 
   PromQL were fledgling at the time. We don't know of any other DSLs which were explicitly reviewed as options 
   beyond SQL.

1. **Were there any languages that inspired the DSL?**:

   As mentioned above, SQL was definitely the inspiration.

1. **Are there specific observability use cases the language was designed for?**:

   The language was originally designed with Event data in timeseries as the primary use-case. Only later were 
   Metric aggregate, and Log types added. The language continues to evolve for the latter two use-cases.

   The language was built from the ground up with scale in mind. It was developed with the core premise that it 
   would be executed in a cluster of many workers, instead a single host. That premise significantly reduces the 
   feature set (e.g. always including a LIMIT, no table JOIN, etc), and drives the fundamental behavior that 
   answers are commonly approximations such as FACET (approximate top-k) instead of GROUP BY (complete answer). 
   Though many answers are still complete, such as the average.

   The language was also built from the ground up with a flexible schema in mind. The execution model and 
   query language is designed with a flexible column type system (e.g. a column could both be a String and a 
   numeric mixed among the rows). The goal is to make sending data of any shape as easy as possible, and 
   making the query language as low-barrier as possible to make that data useful.

1. **Are there specific observability use cases that were intentionally _omitted_ in the design?**:

   The language is read-only. It has omitted any use-cases related to language based mutations of the data or 
   writing.

   Without just reiterating the contrapositive of the above, I don't know of any other specific observability 
   use-cases that were intentionally omitted, within the language itself.

   The product as a whole package (NRDB) did clearly intentionally omit the use-case of Business Analytics (BI) 
   in the original design, with a significant bend toward debugging and incident response. Query execution 
   explicitly prioritized fast answers over complete or complex answers, which could have easily indirectly 
   had an impact on the features developed.

   Since that original conception NRDB has grown and we've continued to grow our support of BI, similar to 
   Metric aggregates and Logs.

   Similarly, the language was not originally designed explicitly for streaming execution, but has since developed 
   significantly in this space. Although NRQL when executed at-rest vs Streaming has different limitations 
   and features available due to data model constraints.

1. **Are there any particular strengths or weaknesses in the language after observing it in use?**:

   A weakness _and_ strength of the language is lack of brevity. The language is fairly verbose, as are all 
   SQL-ish languages.
   
   Other languages like PromQL can in many cases express the same result in far fewer characters which can be 
   really nice for a language expert working. Particularly nested aggregations in comparison with PromQL.
   
   But, it comes as a strength because I've found novice query writers have a much easier time interpreting others' 
   queries and learning NRQL in comparison to PromQL which can be extremely terse.

   Another weakness is that the user must personally understand semantic differences between operating with 
   Events and Metric aggregation types when writing a query. The language does not provide enough structural 
   differences to help guide users from common pit-falls when working with Metric aggregations, due to the 
   Event-based origins. It is something we're still contending with and iterating on.

   Another major weakness is that NRQL stagnated for many years after inception, which has made it fall behind 
   in basic features. In the past the language was organizationally orphaned, and left behind in prioritization 
   of scaling and growth. It was only developed when absolutely required. That has since changed but there has 
   been a lot of catching up to do!

   A strength of the language is that it is fairly easy to write a correct and optimized query. It tends to 
   be the case that your first attempt is semantically very close to your goal. The brevity of other languages 
   like PromQL make wrong or subtly complex queries equally easy to write.

1. **Is the language intended at-rest data and/or streaming data?**:

   The original language design was intended for at-rest data. It has since been fully integrated as a language 
   for streaming data as well, but there are some constraints or disabled features in streaming. For example, 
   the TIMESERIES clause only makes sense for an at-rest query.

1. **Can users specify a source in the query language? E.g. a specific table or database?**:

   Yes, in NRQL it is referred to as an Event type, and is contained in the FROM clause of the query.

   1. **Can users join with other sources than the primary database? E.g. a CSV file, cloud databases, etc.?**:

      Yes, a user can JOIN the results of another query from any other source queryable. That does include our 
      recently released lookup feature which allows the user to query against uploaded CSV files via 
      `FROM lookup(fileName)...`. Lookup files can be joined against or just queried directly.

   1. **If joining of various time series sources is available, how are differing retentions handled?**:

      Today, users can query different sources with differing retention and it is up to the user to know if 
      any of the result is incomplete due to retention boundaries.

1. **How tightly coupled is the DSL to the data store model? (1 to 10 with 10 being extremely) tightly coupled)**:

   If we're speaking just the language, 4. Generally the language itself isn't very tightly coupled to the 
   data store model.

   There are some niche language features like the RAW keyword, or EXTRAPOLATE keyword which might not make 
   sense in an uncoupled setting.  
   
   The language is applicable to multiple execution models (at-rest and streaming), and multiple data types 
   (Events, Metrics, Logs, and indirectly Traces).

   If you include the full execution system, possibly a 7-8, since we do have quite a few quirks to the 
   execution model which are coupled fairly tightly with our at-rest storage mechanisms, file formats, etc, 
   to enable optimizations within the language.

   1. **Is the DSL flexible enough to operate on data in different storage formats or contexts?**:

      Yes! We execute on dozens of different file formats today depending on the context the data is in, 
      or data being stored. Streaming, Metrics as Events, Metrics as native aggregations, At-Rest, At-Rest 
      while actively writing, CVSs in lookups, data being ingested and filtered, etc. All of these systems 
      are built upon constructs of full or partial NRQL strings for execution.

1. **What character sets are supported by the DSL?**:

   The language supports Unicode end-to-end either directly or escaped as `\uXXXX`. Generally it operates in UTF-8.

   1. **What characters are special or reserved in the DSL**:

      I think I'd need more context to understand what context these are being reserved from? Of course, any 
      language construct like `+` is reserved without being contained in a String Literal. There are a variety 
      of reserved column names which serve specific purposes in the languages such as `timestamp`. Any column 
      names can be contained in `back-ticks` to avoid the reservation.

1. **Does the DSL allow for writing data or configuring the backing store or is it for querying only?**:

   Generally, it is read-only. There are specific contexts where query execution is used to select data during 
   data deletions via a given `WHERE` clause. But explicit delete by match when used in that use-case specific 
   tool is the only case where it's used for non-reading. Another gray area would be the use of NRQL in 
   streaming contexts to aggregate into a new data stream.

   To be specific though, the language has no mutation specific keywords, operators, etc. But, it has been used 
   for non-reading use-cases across NewRelic in specific use-cases.

## References

* [Introduction to NRQL](https://docs.newrelic.com/docs/query-your-data/nrql-new-relic-query-language/get-started/introduction-nrql-new-relics-query-language/)

## Thanks

Ashton Hunger and the NRQL team.

