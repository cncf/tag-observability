# Use Cases

Use cases are intended to capture the various ways that observability data is used. We intend
to capture as many use cases from observability end users as possible, then evaluate the various
DSLs against this data set and use it to inform our recommendation for a standard.

Use cases are organized by **common** uses, meaning those that almost every observability user
has such as alerting if a static CPU usage threshold is exceeded or searching for exceptions
across a fleet of servers. **Uncommon** uses are those that typically involve intricate queries,
require exporting data for analysis with other tools, or are impossible in existing DSLs. These
are useful to capture as we want to ensure a standard could eventually satisfy more complex
uses.

Uses cases are further subdivided by **single type**, those that involve a single telemetry
type such as plotting a graph of a metric, or **multi type** that involve combining multiple
types in a single query, such as alerting if there was an exception in a log and there were
HTTP 500 metrics detected in the same interval.

Each use case should have an individual file scoped to that specific use case.

## Schema

* **title:** _String_ - The title of the use case. Should be less than 512 characters.
* **description:** _String_ - A description of the use case in the multiline folded style.
  Supports Markdown. The description should explicitly define the objectives of the use, why
  it is important.
* **inputs:** _List of Strings_ - A list of telemetry types ingested by the use case.
* **outputs:** _List of Objects_ - A list of outputs that satisfy objectives of the use case.
  * **title:** _String_ - A short description of the output.
  * **description:** _String_ - Details about the output in the multiline folded style.
    Supports Markdown.
* **example_description:** _String_ - A description of the example queries in the multiline
  folded style. Supports Markdown.
* **examples:** _List of Objects_ - A list of example queries in various languages that 
  satisfy the use case.

### Examples Schema

* **language:** _String_ - The name of the language the example is written in.
* **query:** _String_ - The query in the multiline folded style. Supports Markdown.
* **callouts:** _List of Objects_ - A list of [Callouts] describing caveats regarding the example.
* **references:** _List of Strings_ - A list of references regarding the example such as 
  documentation or source code.

[Callouts]: ../dsl-survey/README.md#callout-schema