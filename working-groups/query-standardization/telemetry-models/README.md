# Telemetry Models

These are detailed descriptions of telemetry models used in observability systems for
input, processing and egress. We intend to capture a number of the most common models
encountered in the existing observability space to determine what a standard language
should support.

Each telemetry type must have an `overview.yaml` file with a description of the type
along with common uses and attributes. An `implementations.yaml` file must be present
that lists implementations pertaining to the collected query languages. Implementations
should call out the languages involved and any implicit behavior that may not be readily
apparent to end users.

## overview.yaml

* **id:** _String_ - A short unique identifier for the telemetry type.
* **description:** _String_ - A short description of the telemetry type in the multiline 
  folded style. Supports Markdown.
* **attributes:** _List of Objects_ - A list of attributes associated with the majority
  of implementations of the telemetry type. E.g. timestamps, labels, etc.
  * **attribute:** _String_ - The name of the attribute.
    **description:** _String_ - A description of the attribute in the multiline folded style.
    Supports markdown.
* **uses:** _List of Objects_ - A list of common uses for the telemetry type.
  * **title:** _String_ - A common use for the telemetry type.
    **description:** _String_ - A description of the use in the multiline folded style.
    Supports markdown.

TODO - still waffling about archtypes, subtypes, etc.

## implementations.yaml

TODO