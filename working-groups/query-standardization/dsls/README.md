# DSL Survey

This directory contains the results of existing observability query language research
and analysis. Each DSL will have a directory with files for various operators or functions.
The `overview.yaml` files should include designer interview results.

## Schema

One directory per DSL. Each directory should have an `overview.yaml` file with overarching
information regarding the language. Operators and functions should be organized into files
like `predicates`, `logical`, `aggregations`, etc.

### overview.yaml

* **title:** _String_  - Full name for the DSL
* **abbreviation:** _String_ - Abbreviation for the DSL  
* **copyright:** _String_ - Name of the copyright owner.
* **license:** _String_ - Name of the license the language is available under. `proprietary` 
  if not open source.
* **isOSS:** _Boolean_ - Whether or not the DSL is open source.
* **paradigms:** _List of Strings_ - Programing language design paradigms the DSL uses.
* **inspiration:** _List of Strings_ - Other languages that inspired the DSL.
* **description:** _String_ - A general description of the DSL with the multiline folded style. 
  Supports Markdown.
* **supportedTelemetryTypes:** _List of Objects_ - A list of telemetry types supported by the 
  DSL with models involved and callouts for global language behavior.
  * **type:** _String_ - The telemetry type as defined in [Telemetry Models].
  * **models:** _List of Strings_ - A list of model IDs as defined in [Telemetry Models]. The list should
    be a union of all models of the given type that are supported in any part of the DSL.
  * **callouts:** _List of Objects_ - A list of [Callouts] for the telemetry type, describing
    implicit behavior, differences or common issues users face when working with this telemetry
    type in the DSL.
* **designCallouts:** _List of Objects_ - A list of [Callouts] describing explicit design goals 
  or decisions. The `title` should be the name of the goal or decision.
* **caveats:** _List of Objects_ - A list of [Callouts] describing caveats, limitations or
  issues that commonly trip up users of the DSL.
* **contexts:** _List of Strings_ - A list of contexts in which the DSL is used. E.g.
  `streaming` for stream processing of data, `online` for low latency real-time queries against a
  data store and `offline` for batch or big-data queries.
* **references:** _List of Strings_ - A list of references to documentation, papers, etc.
  that describe the DSL.

### Operators or Functions

* **title:** _String_ - The title of the operator or function.
* **term:** _String_ - The gramatical term for the operator function.
* **description:** _String_ - A description of the operator or function with the multiline folded style. 
  Supports Markdown.
* **callouts:** _List of Objects_ - A list of [Callouts] describing caveats regarding the operator
  or function.
* **inputs:** _List of Objects_ - A list of [Definitions] describing inputs to a function such
  as a piped or stack function.
* **outputs:** _List of Objects_ - A list of [Definitions] describing the outputs or results of 
  a function or operation.
* **arguments** _List of Objects_ - A list of [Definitions] describing the function.

### Callout Schema

* **title:** _String_ - The name or short description of the callout. Should be less than
  256 characters.
* **description:** _String_ - A description of the callout with the multiline folded style. 
  Supports Markdown.

### Definition

* **name:** _String_ - The name of the definition.
* **type:** _String_ - A type of data defined in models or elsewhere in the DSL.
* **description:** _String_ - A description of the definition with the multiline folded style. 
  Supports Markdown.

[Telemetry Models]: ../telemetry-models/README.md
[Callouts]: #callout-schema
[Definitions]: #definition