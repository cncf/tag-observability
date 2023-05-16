# Query Standardization Working Group

A working group to research and analyze exising observability query languages with the goal of
recommending a standard, unified language for following teams and projects to implement.

* [Charter Document](https://docs.google.com/document/d/1JRQ4hoLtvWl6NqBu_RN8T7tFaFY5jkzdzsB9H-V370A/edit#)

## Mission

This working group will conduct research and analysis into various observability query languages and 
deliver a set of recommendations ready for a follow-up group or open source project to turn into an 
ad-hoc standard with a reference implementation. Research and analysis will incorporate information 
such as:

1) Common, uncommon and desired use cases across observability data
1) Input and output data models for query languages
1) Language design goals, caveats and examples mapped to use cases
1) Semantic details for language operations
1) Adoption, tooling and infrastructure around the DSLs
1) Survey end user sentiment regarding existing DSLs

Evaluation deliverables will be a set of documents including end-user surveys, interview notes, use 
cases, examples and semantic descriptions of query languages.

The standard query recommendation deliverables will include information on:

1) A document stating the design goals of a standard language along with benefits and trade-offs
1) Base data model definitions of observability data types to incorporate Semantic definitions of 
   operations on observability data
1) A schema for query results of the various types
1) Recommended APIs for querying observability data
1) A recommended query syntax

Creating an ad-hoc standard and reference implementation using the recommendations as a spec is out 
of scope for this proposed working group under the Observability TAG charter. A follow-up group will 
be responsible for finalizing the standard and potentially creating implementations after the work of 
this group is complete.

## How we communicate

* Chat: [CNCF Slack #tag-observability](https://slack.cncf.io)
* Meetings **TBD**
    * See [CNCF community calendar](https://www.cncf.io/community/calendar/) for invite links
    * Meeting Notes **TBD**
* Mailing List: `cncf-tag-observability@lists.cncf.io` ([join here](https://lists.cncf.io/g/cncf-tag-observability))
    * Sharing the main Observability list.

### Chairs (alphabetical order)

| Name         | Email                     | CNCF Slack    | GitHub     | Company   | Open Source         |
|--------------|---------------------------|---------------|------------|-----------|---------------------|
| Chris Larsen | clarsen@euphoriaaudio.com | @Chris Larsen | [manolama] | [Netflix] | [OpenTSDB], [Atlas] |
| Vijay Samuel | vijay.samuel.a@gmail.com  | @Vijay Samuel | [vjsamuel] | [Ebay]    |                     |

## Code of Conduct

We follow the [CNCF](https://www.cncf.io/)'s 
[Code of Conduct](https://github.com/cncf/foundation/blob/master/code-of-conduct.md).



[manolama]:       https://github.com/manolama
[Netflix]:        https://netflix.com
[OpenTSDB]:       https://github.com/OpenTSDB
[Atlas]:          https://github.com/Netflix/atlas
[vjsamuel]:       https://github.com/vjsamuel
[Ebay]:           https://www.ebay.com