# Glossary

* **asl:** [Atlas Stack Language](dsl-survey/atlas-stack-language/overview.yaml) - A language created
  by Netflix for the Atlas time series service.
* **dsl:** [Domain Specific Language](https://en.wikipedia.org/wiki/Domain-specific_language) -
  A language specialized to a particular domain.
* **fingerprint:** A unique identifier used identify patterns in logs or traces that are similar
  though with slightly different parameters. For example, a log entries like "user bob failed auth
  from IP 0.0.0.0" and "user alice failed auth from IP 1.2.3.4" should have the same fingerprint
  though the parameters (user, IP and timestamp) differ.
* **log:** A timestamped record of an event that occurred in a system. Logs are often used to record
  events that are not expected to occur frequently and describe process behavior.
* **metric:** A measurement of a particular value at a particular time associated with a unique
  identifier. A set of data points over time is a time series.
* **namespace:** A logical grouping of data in a system. Namespaces are often used to separate
  data from different sources or for different purposes.
* **profile:** A view of CPU, GPU, memory or other compute resource usage by a process or set of
  processes.
* **promql:** [Prometheus Query Language](dsl-survey/promql/overview.yaml) - The query language
  for the Prometheus time series database.
* **trace:** A collection of duration measurements across distributed systems. Traces are often
  used to understand the flow of a request through a system.
* **uql:** Lightstep [Unified Query Language](dsl-survey/lightstep-unified-query-language/overview.yaml) -
  A language for joining different telemetry types in the Lightstep SAAS product
* **dql:** [Dynatrace Query Langage](https://www.dynatrace.com/support/help/observe-and-explore/query-data/dynatrace-query-language)
  Query language for joining different telemetry types in Dynatrace Saas