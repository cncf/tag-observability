# Query Standardization Working Group

This directory is a repository for the research and recommendations of the query standardization
working group.

## Data Formats

The primary aim is to create data that is easy to edit, understand and share. Instead of a DBMS,
the group will use YAML files for data such as query language definitions. The files are 
editable in any browser and GIT provides attribution. Multi-line support is available for easy
reading and Markdown can be used for eventual display in a UI. Schemas can be implemented for
each data type for eventual programmatic use or import into a DBMS.

## Directory Layout

### dsl_survey

Contains subdirectories for each existing query language with details about the
language and grammar. Additional languages and fields can be added over time.

### telemetry_models

This is a collection of various observability data types along with implementations
for OpenTelemetry as well as other systems. These models inform the various query
languages and in choosing a standard we need to account for the various models.

### use_cases

These are various use cases for observability data. A unified language should account
for all common use cases and as many uncommon cases as possible.

## YAML

YAML is a nice format for a GIT repo in that it has a structure, has wide programmatic
support, and allows for multi-line fields that we can use for verbose descriptions
containing Markdown for display purposes.

Note that all YAML files should adhere to roughly 100 characters as the max line width.