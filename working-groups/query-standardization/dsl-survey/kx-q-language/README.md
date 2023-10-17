# Google Monitoring Query Language DSL Survey Response

### **Short Description:**

Q is the programming language of the time series database kdb+. It was designed by 
[Arthur Whitney](https://en.wikipedia.org/wiki/Arthur_Whitney_(computer_scientist)) as "a general-purpose 
programming language that would solve all problems and be interpreted, but fast."
[1](https://queue.acm.org/detail.cfm?id=1531242ents/Product%20Marketing/Working%20Folder/SWPOK/CNCF%20working%20group%20Survey%20Submitted.docx#_ftn1)
It was developed in the late 1980’s for Morgan Stanley with the express goal of enabling highly-scalable, 
low-latency real-time analytics on streaming financial data (i.e. structured time series-data) as digital 
feeds replaced video screens in trading rooms.  t subsequently became developed into a commercial offering 
by KX, and has been adopted across many other industries, for example Formula 1, telecommunications, 
healthcare, and manufacturing.

### Overview

1. **List any over-arching design goals for the DSL. For example URI friendliness, minimal syntax, 
     advanced analytical capabilities, etc.**:

   * **Array Programming** - A carefully designed set of computing primitives facilitates elegant and 
     efficient code. The array-programming paradigm leads to shorter, neater code, which tends to be 
     easier to write and maintain. Array-based lists are a fundamental data structure. Lists are 
     ordered and provide efficient random access, modification and append. It maps well to commodity 
     hardware, naturally enabling high performance computation.
   * **Integrated Data Management** - Q stores data in its accompanying kdb+ database and can operate 
     on it in situ. As a result, there is no need for the latency and overhead-inducing data transfer 
     of other languages. Tables are efficiently stored as a collection of lists representing columns. 
     As a typical analytical query uses a small subset of all columns, less data is read in kdb. 
     This means improved performance compared to a traditional row-based RDBMS.
   * **Efficiency** - Dictionaries and tables are first-class entities in q. They are both built from 
     and extend lists, allowing for highly uniform, expressive, and efficient code. Foreign keys are 
     defined within tables, enabling automatic relational joins. Different kinds of joins are built 
     up from basic operations, notably the as-of join and its windowing variants.
   * **Streaming Analytics** - Q can act on data as it arrives in the system, combining analytic 
     processing of historical data with real-time. This enables immediate reporting and alerting. 
     Roll-ups and aggregations can be efficiently computed online, making intermediate results 
     immediately available to users.
   * **Developer Friendly** - Q interoperates with third-party languages like Python, R, MATLAB, ANSI SQL, 
     etc. Developers can reuse existing functionality and incorporate popular libraries such as machine 
     learning libraries like Scikit-Learn, Keras, PyTorch and Theano. Finally, q is an interpreted 
     language which facilitates fast development and debugging at implementation time.

1. **What deficiencies or omissions in other DSLs lead to your decision to design a new language?**:

   Other languages neither had the appropriate vocabulary and primitives for dealing with time-series 
   data, nor could they scale to maintain high performance for the large data volumes faced by trading 
   environments in large financial institutions. Since then, those big data requirements have extended 
   to multiple industries (automotive, manufacturing, telco, healthcare, etc) which obtain similar benefits 
   from the high performance and scalability of q.
  
   On one hand, databases working with, say, SQL, were inefficient for aggregating and analyzing the 
   largest data volumes, and in particular streaming analytics with in-memory context (noting the recent trend 
   to "streaming SQL").  On the other hand, computing languages that do analytics – Python, MATLAB, etc, are 
   not optimized for big data management – they are not databases.

   Q – with kdb – uniquely bridges both.
 
   Q is optimized for time series data processing and time-series analytics with temporal datatypes including 
   nanosecond precision timestamps and primitives in areas like aggregation, windowing, sorting that make 
   development easier and execution faster. A complete listing of q’s functionality appears here  

   Many independent benchmarks testify to the best-in-class attributes of of q and kdb. For example, 
   see [Benchmarking Specialized Databases for High-frequency Data from Imperial 
   College](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4342004), and 
   [STAC-M3](https://www.stacresearch.com/m3), and 
   [DBOps](https://h2oai.github.io/db-benchmark/) reports.

1. **Were there any languages that inspired the DSL?**:

   Q is based on APL and the principles of array programming and the use of vectors for capturing and 
   processing time series data most efficiently. The motivations and consideration in developing the language 
   are explained in some detail in an interview with is creator, Arthur Whitney, in this article from the Queue 
   magazine of Association for Computing Machinery.

1. **Are there specific observability use cases the language was designed for?**:

   Q was designed initially for processing high volume financial exchange data and extend to cover structured 
   time series generally but also providing support for unstructured data and for reference data. Typical use 
   cases include:
   
   * Anomaly Detection
   * Pre-and Post trade Analytics
   * Predictive Healthcare
   * Backtesting and Trading Strategies
   * Observability and Monitoring  
   * Predictive Maintenance
   * Risk Management
   
   What some call [Applied Observability](https://www.techopedia.com/how-does-applied-observability-help-redefine-data-democratization#:~:text=Applied%20observability%20is%20the%20systematic,scenarios%20associated%20with%20different%20strategies)- 
   the systematic collection and analysis of data from multiple sources within an organization's systems to 
   offer data-backed insights to explain the possible outcomes and scenarios associated with different 
   strategies – reflects an ideal use case for q adoption. Q facilitates aggregation from multiple sources, 
   primarily but not exclusively through the unit of time, in conjunction with in-memory analysis.
 
   Paraphrasing one industry leader whose business is continuous markets observability – "we see no limits 
   to all conceivable data in the universe, capturing it in real-time to record a 'continuous stream of 
   truth'," and ChatGPT-like "ask any question of any dataset at any time to get an answer instantaneously. 
   The only limit is our imagination and in the questions we can think of to ask" such as "why did something 
   happen? Or why did something happen the way it happened? Or what were the small events that led to the 
   big event? And which factors influenced each event? If you know the answer to the question 'why'……. ," 
   the world is your oyster.

   And thus, they get observability nirvana. "We can know everything about everything all of the time. In the
   world of machine generated data and AI, as soon as something changes, everything changes. Our customers 
   are the first to acquire, interpret, and act on, new information. We see and interpret the world of 
   machine generated data through simultaneously a data microscope and a data telescope."

1. **Are there specific observability use cases that were intentionally _omitted_ in the design?**:

   As above, the initial design focus was expressly on structured, time-series and vector data, analyzing 
   data denominated by time and/or as vectors. As the language evolved it provided support for unstructured 
   data and continues to evolve through supporting vector embeddings and indexing for datasets serving 
   Generative AI use cases. Anything is possible with q, especially when interoperability with other 
   environments is included, and so no use case was intentionally omitted.
   
   That being said, observability carries multiple meanings so we need to be careful to delineate. [Monte 
   Carlo Data](https://www.montecarlodata.com/blog-what-is-data-observability/), for example, claim data 
   observability, but their observability essentializes data quality, freshness, volume, schema and 
   lineage, which addresses a different phase of the pipeline to q and kdb.

   For pipeline applications monitoring, [dedicated observability capabilities are 
   available](https://code.kx.com/insights/1.7/enterprise/configuration/observability.html).

1. **Are there any particular strengths or weaknesses in the language after observing it in use?**:

   The strengths of the language are centered on q’s simplicity and ability to store and compute with great 
   efficiency. Quoting an advocate, ["not a single byte of code or data is wasted in the pursuit of ultimate 
   efficiency."](https://www.youtube.com/watch?v=8eoysfqO3UY) In practise, this means q:

   * comes with a small memory footprint (700kB) that exploits L1/2 CPU caches (up to 100 times faster than RAM)
   * exploits vector instructions from Intel and ARM chipsets
   * avoids pre-emptive locks that limit performance and cause thread or process convoying
   * automatically distributes database operations across CPU cores
   * natively supports array operations and parallel computation, which are much more prevalent in applications as a result of the column-store representation of data
   * handles streaming data architectures, batch architectures, and micro-batch hybrid architectures efficiently, exploiting the characteristics of each
   
   A key characteristic of q is its syntax and terseness. On q’s terseness, this interview with 
   [Arther Whitney](http://archive.vector.org.uk/issues/v262.pdf) in Vector Magazine articulates well his 
   position on its advantages for the speed of development and debugging ("It is a lot easier to find your 
   errors in four lines of code than in four hundred" - _page 32_). See the anecdote on his pursuit of 
   conciseness in a college project (_Page 31_) for a very human story.

   While an asset to those with a capability to learn and appreciate the benefits of the terse language q, 
   others prefer expressive languages like Python. In response, KX has developed integrated support for 
   Python ([PyKX](https://code.kx.com/pykx/2.0/index.html)), R, MATLAB, ANSI SQL and more to enable 
   developer to access the power of q from within the syntax of their language of choice, and to reuse 
   existing libraries and functions within q processes where appropriate.

1. **Is the language intended at-rest data and/or streaming data?**:

   The language excels when performing analytics on streaming data combined with historical data for context. 
   This typifies many time-critical use cases in capital markets for trading, real-time risk monitoring and 
   compliance, and providing key data for immediate use organization-wide. Formula 1 and racecar teams use 
   it track-side for similar reasons. Those adopting it for AI projects have deployed real-time inference 
   for ML and AI processing, where in-memory context gives it online "feature store" advantages.

   However, a significant proportion of projects run on historical, at-rest data, also simulated data. One 
   recent example is an agent-based simulation of a billion "virtual patients" by clinical trials 
   organization, Syneos. For discriminative and predictive AI, with at-rest model training and inferred 
   real-time modes, the dual use makes it a powerhouse for both modes, meaning adopters can deploying 
   agility and fluidity between both modes. That’s another discussion.

1. **Can users specify a source in the query language? E.g. a specific table or database?**:

   1. **Can users join with other sources than the primary database? E.g. a CSV file, cloud databases, etc.?**:

      Q includes [interfaces](https://code.kx.com/q/interfaces/) to a wide variety of languages and storage 
      media, include object storage provided by the main cloud service providers.

   1. **If joining of various time series sources is available, how are differing retentions handled?**:

      Q provides a range in built-in [joining](https://code.kx.com/q/basics/joins/) (Keyed, AsOf and Implicit types) 
      and windowing  (Sliding, Tumbling) functions that simplify the correlation of data across diverse data sets. 
      These functions are presented as primitives within the language for time-based processing.

1. **How tightly coupled is the DSL to the data store model? (1 to 10 with 10 being extremely) tightly coupled**:

   **9** – q is the integrated programming language of kdb. The reason why not a 10, though we see this as a benefit, 
   is the ability to run q in uncoupled though optimized instances, critical given the commodification of cloud data 
   stores.
   
   Python interoperability (aka PyKX), that enables q to operate on remote data, not necessarily stored in kdb. 
   PyKX, through Snowpark, is currently how q integrates with Snowflake for example. In such instances, Python and 
   q share memory space for memory efficiency. For those that prefer, and many do, Python can simply interact directly 
   with the database layer.
   
   [ANSI SQL](https://code.kx.com/insights/1.6/core/sql.html) is also supported.

   1. **Is the DSL flexible enough to operate on data in different storage formats or contexts?**:

      Q operates optimally with the kdb database for speed purposes, to act on data in-flight and in-situ in the 
      database, obviating the need to transfer data for processing elsewhere. However, it can and does operate on 
      data storage remotely, as discussed in earlier questions.

1. **What character sets are supported by the DSL?**:

   1. **What characters are special or reserved in the DSL**:

      As noted, a benefit of q is its terseness, but this does mean that characters take on meaning in the language. 
      It is probably simplest to point to the documentation at this stage, i.e., https://code.kx.com/q/basics/syntax/. 
      However, it is important to assess the style and use case. For example, when running 
      [q regex (regular expressions)](https://code.kx.com/q/basics/regex/), certain characters - `?, *, []` – carry 
      special meaning.

1. **Does the DSL allow for writing data or configuring the backing store or is it for querying only?**:

   Q is coupled with kdb+ as its data store and together include the following design features
   
   * stores table data in column format, optimising bulk writes and data compression operations
   * memory-maps partitioned files of ‘column’ data for efficient reads without intermediate data transformations.
   * supports a wide variety of data types for compact storage.
   * and more
   
   For reference, the following cheat sheet nicely summarizes, visually, key capabilities.

   ![q cheat sheet](kdb_table_manipulation.png)

## References

* [The Q Language](https://code.kx.com/q/learn/startingkdb/language/)

## Thanks

Ian O'Dwyer, Stephen Elliot and the KX team.

