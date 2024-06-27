# Google Monitoring Query Language DSL Survey Response

### **Short Description:**

Monitoring Query Language (MQL) DSL designed for fetching and analyzing Google Cloud Monitoring 
time series data. A variant is used internally for Google's Monarch monitoring system. The DSL
has a piped based syntax with support for alert conditions.

### Overview

1. **List any over-arching design goals for the DSL. For example URI friendliness, minimal syntax, 
     advanced analytical capabilities, etc.**:

   * Low verbosity
   * Minimal reserved words/characters
   * Perfect compatibility with Monarch's data model
   * Support for highly complex queries and common patterns

1. **What deficiencies or omissions in other DSLs lead to your decision to design a new language?**:
   
    MQL was in development for several years before it was made generally available. At the time of it's  
    conception, there were basically no options available except its internal predecessor, which was a 
    python library whose syntax didn't scale well to complex queries. We needed queries that were easier 
    to read and write but there were no other options available - so we created a new language.

1. **Were there any languages that inspired the DSL?**:

   MQL's internal predecessor was also a piped language. Other syntaxes for chains of operations 
   (e.g. operations connected by periods, like many programming languages) were considered, but presumably 
   the piped syntax was kept to reduce the learning curve for new users.

1. **Are there specific observability use cases the language was designed for?**:

   Real time alerting.

1. **Are there specific observability use cases that were intentionally _omitted_ in the design?**:

   Not specifically. MQL is flexible enough that it could be extended to support data structures for other 
   use cases such as logging or traces. But it's not clear to me that any use cases were omitted.

1. **Are there any particular strengths or weaknesses in the language after observing it in use?**:

   * **Strengths**:
     
     Even though time series data models have a somewhat steep learning curve, we observed that exposing the 
     data model in its entirety gives users a level of power and freedom that they ultimately come to appreciate. 
     Hiding or glossing over features of the data model can lead to surprises that users find frustrating.

     Most of the other strengths are downstream from this first strength, e.g. Monarch's early engineers made 
     many good decisions about their data model, so exposing that data model directly to users allows them to 
     benefit directly from those good decisions.

   * **Weaknesses**: 

     MQL achieves terse syntax through aggressive syntactic sugar. There are often a dozen or more ways to express 
     the same operation. This results in a huge amount of confusion, because users, who are usually inexperienced, 
     are often familiar with only one way to express an operation; when they see a second or third way, they don't 
     understand what it means. This really increases the learning curve for both reading and writing. We 
     encourage very little usage of MQL's syntactic sugar, and the sugar we do recommend can be applied uniformly to 
     all queries in a standard way.

     MQL's goal of achieving perfect suitability for Monarch was too narrow in scope. Despite the many 
     good decisions made by early Monarch engineers, Monarch of course has some quirks (e.g. no null values, 
     confusing semantics about stream kinds), and these are exposed directly to users of MQL. MQL could have acted 
     as a shim layer that hides some of these quirks, but it doesn't. Ideally, a good observability language would 
     be designed without a particular engine in mind.

1. **Is the language intended at-rest data and/or streaming data?**:

   At rest, but it could easily support streaming data.

1. **Can users specify a source in the query language? E.g. a specific table or database?**:

   Table, yes. Database, no, although this could be extended.

   1. **Can users join with other sources than the primary database? E.g. a CSV file, cloud databases, etc.?**:

      Not currently, but this could be supported.

   1. **If joining of various time series sources is available, how are differing retentions handled?**:

      This is not handled at the query level. Different processes manage removing data that is out of retention so 
      that the query path can remain ignorant of this aspect.

1. **How tightly coupled is the DSL to the data store model? (1 to 10 with 10 being extremely) tightly coupled)**:

   2 or 3. There are some aspects of the language that are more coupled than I'd like (e.g. handling of stream kinds), 
   but otherwise this language makes only a few assumptions about the data store model.

   1. **Is the DSL flexible enough to operate on data in different storage formats or contexts?**:

      Storage formats, yes.

1. **What character sets are supported by the DSL?**:

   ASCII for syntax, UTF-8 for data identifiers.

   1. **What characters are special or reserved in the DSL**:

      Common mathematical characters with support for quoting. See the 
      [MQL Lexical Grammar](https://cloud.google.com/monitoring/mql/reference#lexical-elements).

1. **Does the DSL allow for writing data or configuring the backing store or is it for querying only?**:

   The language itself only supports querying, but Monarch is able to write query results back to the data store; this 
   cannot be done on an ad-hoc basis and needs to be configured. MQL has no support for modifying configuration.

## References

* [MQL Overview](https://cloud.google.com/monitoring/mql)
* [About the MQL Language](https://cloud.google.com/monitoring/mql/query-language)
* [Monarc: Google’s Planet-Scale In-Memory Time Series Databaseh](https://www.vldb.org/pvldb/vol13/p3181-adams.pdf)

## Thanks

Sam Karlinski, John Banning and the Google Monarch Team

