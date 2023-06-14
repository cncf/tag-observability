Very rough brainstorming document for end user survey questions.

* What observability stack is in use for observability data throughout your company?
* What query languages are in use for BI or other analytics at your company?
* What language do you find the most intuitive, meaning it gives you the results you expect within a small number of attempts?
* What language is the least intuitive? Takes many attempts to get an answer you desire?
* For obs, do you typically write queries by hand or use a UI query builder?
* What language features do you use the most?
  * Filtering 
  * Aggregation 
  * Analytics 
  * ??
* What kind of telemetry data is the most difficult for your to query 
  * TEMPL list of telemetry types
* What kind of telemetry data is the easiest to query?
  * TEMPL list of telemetry types
* What kinds of telemetry data do you join together the most?
  * TEMPL list of telemetry types
* What kinds of telemetry data do you wish you could join together?
  * TEMPL list of telemetry types
* How often do you write custom code to join data from different sources?
  * Frequency
* How often do you join telemetry data with BI data?
* How easy is it to join telemetry and BI data?
* What query features are the most important to you?
  * Portability across providers?
  * Portability across infrastructure (telemetry sources, collectors, routers, query)
  * Templating e.g. timestamps, variables, global filters
  * Joining multiple data types
  * Joining multiple data sources
  * Real-time querying
  * Across narrow time ranges (hours or days)
  * Across wide time ranges (weeks, months)
  * Stream processing support
  * Offline processing support (batch)
  * Same language for alerting, querying, stream processing, etc
  * Analytical capabilities (regressions, statistics, etc)
  * ML model integration
  * Minimal syntax (very easy to write)
  * Ease of comprehension (possibly verbose, easy to understand a query from another user)
  * URI encodable
