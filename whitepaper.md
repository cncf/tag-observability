# Observability Whitepaper

> NOTE: This is a "tip" version of the observability whitepaper. This is where
> we develop future v1.1+ versions with the community. For 1.0 version see [here](https://github.com/cncf/tag-observability/blob/whitepaper-v1.0.0/whitepaper.md).

Welcome to the community-driven version 1.0 of the observability whitepaper.
Led by TAG Observability in the CNCF ecosystem, it was released in October 2023.

This version of our whitepaper is only a start! There are many more topics to cover and things to add.

See [the contributing section](#contributing) on proposing changes to this paper and helping us grow this knowledge base for all the CNCF users.

## Table of Contents
* [Executive Summary](#executive-summary)
* [Introduction](#introduction)
  * [Target Audience](#target-audience)
  * [Goals](#goals)
  * [Non Goals](#non-goals)
* [What is Observability?](#what-is-observability)
* [Observability Signals](#observability-signals)
  * [Metrics](#metrics)
    * [Metric Cardinality](#metric-cardinality)
  * [Logs](#logs)
  * [Traces](#traces)
  * [Profiles](#profiles)
  * [Dumps](#dumps)
* [Correlating Observability Signals](#correlating-observability-signals)
  * [Signal correlation](#signal-correlation)
  * [Practical applications](#practical-applications)
  * [Practical implementations](#practical-implementations)
* [Use cases](#use-cases)
  * [Box-based Monitoring Categories](#box-based-monitoring-categories)
  * [Implementing SLIs, SLOs and SLAs](#implementing-slis-slos-and-slas)
  * [Alerting on Observability data](#alerting-on-observability-data)
  * [Root Cause Analysis](#root-cause-analysis)
* [Current Gaps around Observability](#current-gaps-around-observability)
  * [Automatic and non-intrusive instrumentation in OSS](#automatic-and-non-intrusive-instrumentation-in-oss)
  * [Standardized query layer](#standardized-query-layer)
  * [More Observability Databases in OSS](#more-observability-databases-in-oss)
  * [Monitoring for Streaming APIs](#monitoring-for-streaming-apis)
* [References](#references)
* [Contributors](#contributors)
* [Contributing](#contributing)

## Executive Summary

With the continuous growth of the system complexities and the data we process every second, we need better observability to understand the state of our workloads. On top of the observability tooling, it's now more common to expect every engineer responsible for running their software as a service to understand how to monitor and observe their applications. With higher customer expectations and stricter service level objectives, engineers must debug and find the root causes of problems faster than ever.

This paper aims to get you quickly started with cloud-native observability. We will give a high-level overview of different kinds and patterns for observability you might need to work when running your workloads in the cloud.

## Introduction

With the popularization of cloud computing, microservices and distributed systems, new applications are often designed and built to run on the cloud. Although this provides new strategies to build more resilient, better performant and more secure applications, it comes with the potential cost of losing control over the infrastructure supporting these workloads. Sysadmins, developers, and software operators must know the state of an application in production and the underlying infrastructure health where that application is running. Moreover, they should be able to externally observe these signals without adding, e.g. new instrumentation in the source or setting breakpoints on running production code.

Applications must be designed and built to include and facilitate mechanisms that make them observable by some entity, e.g., whether this entity is another application or a human without access to the data center. The effort must be made early, beginning with design, and it often requires extra code or infrastructure automation and instrumentation. These cultural and process changes are often challenges or blockers for many organizations. On top of that, many methods and tools out in the market suggest different approaches to reach a reasonable level of observability.

Once one reaches a satisfactory level of observability, there is no doubt of its benefits, but getting started can feel daunting! Cultural changes, different tools, different objectives, different methods. So many details that need to be considered can make this journey confusing and painful. This paper aims to provide clarity so that more software and operations teams can gain the benefits of observability in their systems.

### Target Audience

The target audience of this paper is:

* Site Reliability Engineers
* DevOps Engineers
* Sysadmins
* Software Engineers
* Infrastructure Engineers
* Software Developers

This paper relates to any of the above roles from organizations that wish to deliver observable software that integrates with their customers' existing observability systems while reaching a demonstrable level of reliability, security, and transparency. Additional organizational stakeholders such as Project, Product, Program Managers, and Architects responsible for designing and implementing such software may also be interested in this paper since observability is a multidisciplinary topic. Computer Science, Information Systems, and Engineering (or related) students and people curious about the Observability domain may also find helpful information in this paper.

### Goals

Cloud computing adoption has helped small, big tech companies optimize cost, scale, and design more efficient products, but it came with its complexity. Since the infrastructure is now remote, temporary, and globally distributed, Sysadmins's control over data centers is now lost. Companies that once had a culture where Administrators and Developers had conflicting goals must change to a new culture where they now must work together as a single team aiming to build reliable software. Several new strategies and tools have emerged from observing the state of Cloud Native systems and helping such companies to keep their systems reliable in this new reality.

During the design and development of an observable system, it must be instrumented to send or expose telemetry data to a third party, usually a set of tools, responsible for providing meaningful information out of the exposed data. An alternative can be autoinstrumentation, for example through the Java runtime, pprof, or eBPF. That telemetry data frequently comes in the form of metrics and logs, long used by software engineering teams, as well as traces, structured events, profiles, and crash dumps. Each signal has its purpose and best practices, and their misuse can lead to new problems when running software at scale, such as "alert fatigue" and "high cost".

Even though there are several new challenges, such as culture change, capacity planning, legal issues, and others, many of them were already tackled and solved by innovative companies that entered this new era early. Beginners can learn from their findings and mistakes and follow their best practices to tackle those same issues. This paper will provide the difference between observability signals and how they should be handled, list several different methods that successful companies used when tackling common issues, present several tools that fall under the observability scope and where they should fit in your observability stack, as well as show commonly known gaps that are still unsolved or that a method still isn't very well consolidated in the market.

### Non Goals

This document is not meant to provide low-level installation guides or configuration details for specific observability projects. It's also not meant to be a detailed deep dive into various standards like W3C context propagation, the Prometheus Exposition format (OpenMetrics), or OpenTelemetry protocol (OTLP).

Instead, we give you a general overview and references to valuable materials like project documentation pieces.

## What is Observability?

There is no doubt that observability is a desirable property of a system. Everybody is saying that, right? Some of you may have already started your observability journey, while others are reading this whitepaper right now just because everyone is saying that you should make your systems observable. The fact is that "Observability" has become a buzzword, and like every other buzzword, everyone wants to leave their mark while advocating for it, and what you have heard may have a different meaning from what it originated from. If you're going to level up your game on observability, let's try to make it clear its original purpose.

In control theory, "observability is a measure of how well internal states of a system can be inferred from knowledge of its external outputs."<sup>[[7]](#references)</sup> Being less theoretical, it is a function of a system with which humans and machines can observe, understand and act on the state of said system. So yes, observability, by definition, looks simple, but it gets complicated to decide which output(s) a system should have when implemented without an objective in mind. That's when things start to go sideways.

When getting started, copying someone else's work is easy. That is one of the blessings and, simultaneously, one of the curses of Open Source. There are many examples online; helm charts, Ansible playbooks, and Terraform modules. One can just run one of those scripts, and you have an observability stack up and running in just a few minutes. It is easy, and it works for others. Therefore it should work for me, right? While we're not trying to encourage you not to use those scripts, you must remember that observability is not just using all the pretty and shiny tools. You must be conscious about what outputs are coming out of your system, and, more important than everything, you need to have an objective in mind! You may think: "Oh, I want to collect this particular data because you never know, I may need that in the future." and you repeat this thought for another data, and another, and another, and then you realize that you are building a data lake instead.

Observability can be used in literally all phases of the development lifecycle of a system. You can use it while testing your new feature, monitoring production resiliency, having insights about how your customers use your product, or making data-driven decisions about your product roadmap. Once you have either of those goals in mind, you'll start thinking about the outputs, or what we call them, the signals.

## Observability Signals

As mentioned, signals are a system's outputs that a human or machine can infer knowledge from. Those signals will vary from system to system and depend on the objective you want to accomplish. It can be something you want to measure at a certain point, like temperature or RAM usage, or an event that goes through many components of your distributed system that you'd like to trace down. You might want to know what function of your system is the most intensive on resources such as CPU, Memory or Disk at a random point in time or how your system broke at the exact time when it did. While some signals may overlap to infer knowledge, others specialise in certain system aspects. They can all be used together to provide different ways to observe the same piece of technology, or, as we recommend for starters, you can start with just one or a few and mature your way up to the others.

There is a really good chance that you have heard about the "Three Observability Pillars", which are metrics, logs, and traces. They are commonly mentioned and probably what you're going to start with. We like to think of them as the "primary signals" instead of "three pillars" for two reasons:

Pillars carry an implicit meaning of being foundational. They are a safe place to start, yet are not always required at the same time. In fact, basing on one or two signals with a small mix of others can be a valid trade-off to improve cost efficiency (e.g. metrics and logs with ad-hoc tracing).
Recently, more signals are becoming popular in open-source communities like application profiles (continuous profiling) and crash dumps. New signals with new semantics may also arise in the near future, and those interested in this topic should keep an eye open for them.

![Figure 1](/assets/primary-signals.png)

_Figure 1 shows three primary signals that help to categorize the data we can observe from the workloads. Note that not all metrics are semantically aggregatable, but they generally can be aggregatable in an easier way (or represent a group of events by itself). Lower volume scale also refers to typical volume–you can produce too much data with metrics, but it's a little harder than with logs and traces._

All signals have different ways of being collected or instrumented. They have different resource costs to obtain, store, and analyze while providing different ways to observe the same system. Choosing between them or all of them is a game of trade-offs like all other tasks in engineering. In the next sections, we will help you make this decision by digging deeper into each signal, starting with the people's favourites: metrics, logs, and traces, and then the two newly emerging signals: application profiles and crash dumps.

### Metrics

Metrics are numeric representations of data. They fall into two main categories: Already numeric data and data distilled (aggregated) into numbers. An example of the former would be temperature, for the latter– a counter of HTTP requests observed on the webserver.

Numbers are the most efficient way to store data and all established industries trend towards metrics-first over time. As an example, your rent, water, heating, cooling, and power bills are metrics-only, and the bank account you pay them from is metrics-only as well.

Let’s look at a typical example use case for metrics–a gauge that measures the heap memory usage of a host (e.g. virtual machine). Let’s call it “heap-memory-bytes”. The metric consists of a name, a set of labels (sometimes called attributes or tags) and a numerical value for each point in time (e.g. one value per second). Each metric instance, with a certain name and labels, is often called “timeseries” or “stream”.

The “heap-memory-bytes” would allow us to view the heap memory usage of each host over time. We could also perform additional aggregations on top, e.g. the average heap memory usage per data center.

| Metric name       | Label key | Label value | Label key   | Label Value | Value at time t0 | .. at t1 |
|-------------------|-----------|-------------|-------------|-------------|------------------|----------|
| heap-memory-bytes | host      | host123     | data-center | c1          | 11231            | 11200    |
| heap-memory-bytes | host      | host234     | data-center | c1          | 300203           | 412103   |

_Table 1 shows two timeseries for one example metric. Their metric names, labels and values for certain timestamps are represented in a tabular view with columns._

Distilled data lose some details. Metrics represent point-in-time observations of the state of a system, which means that, in our "heap-memory-bytes" example, we don't know the heap value between the observed interval (between t0 and t1). We also cannot answer anything more granular than the host, e.g. what process IDs are used and how many heap bytes. This differs from logs or traces, which focus on records or information about individual events with more details (e.g. "the process A allocated 20 bytes on the host B").

If used as intended (see [cardinality issue](#metric-cardinality)), this trade-off makes metrics one of the most efficient signals for "known unknowns":

* Metrics are efficient in terms of predictable processing cost (for retaining, emitting, transmitting and storing), because the volume does **not** scale with higher traffic. For example, there is always one "heap-memory-bytes" metric per host, no matter how many allocations or processes are running).
* Smaller amounts of data with clear dimensions also reduce mental overload for human operators as they can get a quick overview of a situation (e.g. when the memory saturation occurred).

The industry also figured out different types of metrics useful for different observations. Various data models describe multiple types, but we can outline three core types that are commonly supported:

* Gauge: Metric representing a single numerical value that can arbitrarily go up and down. Gauges are typically used for measured values like temperatures or current memory usage, but also "counts" that can go up and down, like the number of concurrent requests.
* Counter: Cumulative metric representing a single monotonically increasing counter whose value can only increase or be reset to zero on restart. For example, a counter can represent the number of requests served, tasks completed, or errors.
* Histogram: The histogram samples observations (like request durations or response sizes) and counts them in configurable or exponential buckets. It also provides a sum of all observed values. Allows advanced analysis of distributed observations like percentiles and heatmaps.

Metrics are typically either structured or semi-structured and generally are used in two ways:

* __Real-time monitoring and alerting__ - The most common use-case for metrics is to overview and drill down visual dashboards. It's also used to trigger alerts or notifications for either humans or automated systems that a monitored system has crossed a threshold or is behaving anomalously.
* __Trending and analysis__ - Metrics are also used for trend analysis over time and long-term planning purposes while also providing insights after an incident has occurred into fixing and monitoring underlying problems to prevent a recurrence.

The information provided by metrics is used to form insights into systems' overall behaviour and health. Metrics often play a large role in the "what" is happening and sometimes the "why". For example, a metric can tell you the number of HTTP requests per second but not always why you have a spike or dip in requests. However, it can tell you why your load balancer is overloaded (e.g. too many requests causing CPU spikes).

In other words, metrics don't always reveal the root cause, but they provide a high-level overview and a starting point to find the root cause of an issue. The next step of the investigation might involve looking [correlated information](#correlating-observability-signals), for example, other related metrics (e.g. to look for higher latency root cause, we could check the temperature of the server), traces, logs–jumping back and forth is quite common.

In the CNCF ecosystem, we see two popular metric data models: [Prometheus](https://prometheus.io/docs/concepts/data_model/) and [OpenTelemetry (metrics)](https://opentelemetry.io/docs/specs/otel/metrics/data-model/).

#### Metric Cardinality

An important characteristic of the metrics you collect about your workloads is their [cardinality](https://www.robustperception.io/cardinality-is-key/). Generally, for metrics, cardinality means the number of unique metric series collected over a certain period. Table 1 represents the cardinality of two for the t0-t1 period. However, if we had 100 data centers, with 10 000 hosts each, we would likely produce 1 million metric series (cardinality of 1 000 000) over the same duration.

While the 1 million number seems large for a single metric name, it can easily fit a single node database. For example, Prometheus can scale into the tens of millions of active series. It is also significantly cheaper to process than the number of logs or trace events representing every memory allocation.

Every efficient metric storage backend or vendor scales with metric cardinality, i.e. the true cost grows with cardinality. Given the typical interval for metrics varies between 1s and 1 minute, the number of samples could also represent cardinality for a certain duration. This is why you see some vendors and systems charging per sample. Many systems also have certain limits to how large cardinality can be over a specific time.

How much cardinality is too much? There is no single number, as it depends on your needs and how much money you are willing to spend on metrics. The cardinality might be too large when you need to pay more (or you have to scale your metric storage), and the expensive dimensions (those with many unique values) do not give you enough value for the price tag.

For example, let’s imagine that we want to expand our “heap-memory-bytes” to track memory per application. The first idea would be to add a “PID” label to our metric representing the process ID.

| Metric name       | Label key | Label value | Label key | Label value | Label key   | Label Value | Value at time t0 | .. at t1 |
|-------------------|-----------|-------------|-----------|-------------|-------------|-------------|------------------|----------|
| heap-memory-bytes | host      | host123     | PID       | 22          | data-center | c1          | 3445             | 3445     |
| heap-memory-bytes | host      | host123     | PID       | 24          | data-center | c1          | 231              | 190      |
| heap-memory-bytes | host      | host123     | PID       | 44          | data-center | c1          | 51331            | 22340    |
| …                 |           |             |           |             |             |             |                  |          |
| heap-memory-bytes | host      | host234     | PID       | 34          | data-center | c1          | 300203           | 412103   |
| …                 |           |             |           |             |             |             |                  |          |

_Table 2 shows multiple time series for one example metric with an extra, potentially dangerous, PID label._

This metric implementation goes into a grey area as the cardinality of such a metric could be practically unbounded (around 4 million PIDs are possible in 64-bit systems, and every application restart might take a new unique PID). Suppose we host 100 applications with three replicas on average in each zone for one day. In that case, the PID label might bring our metric cardinality for that single metric into the billions potentially.

In our example, since we are interested in memory used by certain application replicas, we don’t need a PID as long as we can identify a certain application. If we would be able to identify a replica by some ID (e.g. like pod name in Kubernetes) and we add “replica ID” instead of “PID label”, we could reduce cardinality to a maximum of 300 million series for “heap-memory-bytes” (typically less). If we further remove the host label (do we care on which host the application’s replica uses how much memory?), we could reduce the cardinality (and thus cost) to just 30 000, so 300 (number of all replicas) * 100 (number of data centers)!

Adding the “PID” label has the potential for unbounded cardinality, but it all depends on your infrastructure characteristics. It might be a decision worth the buck, but it might also be an accidental metric cardinality explosion (a surprising amount of series causing scalability issues or cost spikes).

Metric cardinality is often called the Achilles heel of metrics. This can be misleading, as every piece of observability data has its cost. The efficiency of metrics comes from stable dimensions and their values over time.

High cardinality problems often occur because users try to overuse their cheap and efficient metric storages and pipelines for observability data with non-metric characteristics. Suppose we end up with highly unique labels (high cardinality) that cause metrics to have short-living series (a few samples). In that case, we should consider emitting events (logs, traces or profiles) instead of metric samples.

### Logs

Logs are one or more textual entries describing usage patterns, activities, and operations within an operating system, application, server, or another device.

Logs can be categorized into different categories, such as:
* __Application Logs__ - an application log is created when an event occurs inside an application. These logs help developers understand and measure how applications behave during development and after release.
* __Security Log__ - security logs are created in response to security events in the system. These can include various events such as failed log-ins, password changes, failed authentication requests, resource access, resource changes including files, devices, users, or other administrative changes. System Administrators can often configure which events are included in the security log.
* __System Log__ - system logs record events within the operating system, such as kernel-level messages dealing with physical and logical devices, boot sequences, user or application authentication, and other activities, including faults and status messages.
* __Audit log__ - also called an audit trail, is essentially a record of events and changes. Typically, they capture events by recording who performed an activity, what activity was performed, and how the system responded. Often the system administrator will determine what is collected for the audit log based on business requirements.
* __Infrastructure log__ - is a vital part of infrastructure management, which involves managing the physical and logical equipment that affects an organization's IT foundation. This can be either on-premises or in the cloud and is obtained via APIs, Syslog, or others collected using host-based agents.

Logs can be useful in different scenarios - to derive metrics or traces, for security audits, or for debugging. Keeping a record of all application and system-related events makes it possible to understand and even reproduce step-by-step actions leading to a particular situation. These records are notably valuable when performing root-cause analysis providing information to understand the state of the application or system at the moment of the failure.

Information stored in the logs is freeform text, making it challenging to derive meaning. Many attempts have been at applying a schema to logs in the past 30 years, but they have yet to be particularly successful. The reason for a schema makes extracting relevant information more accessible. Typically this is done by parsing, segmenting, and analyzing the text in the log file. Log data can also be converted to other observability signals, including metrics and traces. Once the data is a metric, it can be used for understanding the change over time. Log data can also be visualized and analyzed through log analytics technologies.

Log levels allow expressing the importance of each log statement. One set of such log levels would be ERROR, WARNING, INFO, and DEBUG. With ERROR being the least-detailed level and DEBUG being the highest-detailed.
1. __ERROR__ communicates the occurrence and details why a failure happened.
1. __WARNING__ is a high-level message that requires attention, although not a failure.
1. __INFO__ messages help us understand how the system works.
1. __DEBUG__ is the level where detailed information for each action is stored. Normally, only used during troubleshooting or for short periods due to storage or performance impact.

Use the multiple verbosity levels to generate detailed information to assist with troubleshooting and root-cause analysis.

It's possible to forward the logs in multiple ways. The first suggestion is configuring the standard streams to send the logs directly to a central location. Second, write the logs to a message queue to be filtered or enriched before reaching their final destination. The last approach uses an open-source data collector application to send the logs to a central repository. Combine logs with other observability signals to have a complete view of your system.

Security is something we must have in mind when planning a logging solution. Encrypt log-related files or information at rest and in transit when sending it to a central repository. Do not store any personally identifiable information (PII) in any log. Finally, truly important data should not be kept solely in logs. Despite the usefulness of log statements, they are not guaranteed to be delivered.

### Traces

Distributed tracing is the technique of understanding what happened during a distributed transaction, such as a request initiated by an end-user and its effects across all downstream microservices and data stores that were touched as a result.

Traces are typically trees of "tracing data-points", or spans as they are normally called, and might be visualized as a Gantt chart like in the following example:

![Image 1](/assets/tracing.png)

_Image 1 shows the Jaeger project UI, which visualisate spans for a given trace._

Traces typically represent one concrete transaction instance, the path a computer took through a specific program, making them a detailed and thus expensive signal in observability. Spans are highly contextualized. Among other things, spans record information about the "parent" span that initiated it. This makes it possible to establish a causal relationship between the different actors of a distributed system, such as services, queues, databases, and so on.

The key mechanism to persist the relationship across different actors is context propagation. While many monitoring systems implemented their own proprietary way of trace context propagation, the industry agreed that trace-context propagation should be standardized. This led to the creation of the W3C Distributed Tracing Working Group and the subsequent release of the W3C Trace Context Specification. W3C Trace Context defines standard HTTP headers and a value format to propagate context information that enables distributed tracing scenarios. The specification standardizes how context information is sent and modified between services. Context information uniquely identifies individual requests in a distributed system and defines a means to add and propagate provider-specific context information.

Today, projects like [OpenTelemetry](https://opentelemetry.io/) or platforms like .NET are using W3C Trace Context as their standard propagation format. Exemplars, trace and span IDs attached to logs and Prometheus metrics, also follow the same format. More cloud-native projects are following this path and in the absence of other design goals, the W3C standard is recommended for use. Once cloud infrastructure providers support it context won't break when passing through managed services like service gateways.

Instrumentation is important for all observability signals, but given the complexity, it plays an essential role in distributed tracing. Instrumentation creates data points and propagates the context from service to service. Without context propagation, we cannot link an incoming HTTP request with its downstream HTTP requests or a message producer and its consumers.

Instrumentation has two main purposes for distributed tracing: context propagation and span mapping. In most cases, context propagation is done transparently using libraries that can be integrated with HTTP clients and servers. In this part, projects, tools, and technologies like OpenTelemetry APIs/SDKs, can be used, among others.

![Figure 2](/assets/trace-spans.png)

_Figure 2 shows span relations across network calls._

### Profiles

As companies continue to optimize for cloud-native applications, it becomes increasingly important to understand performance metrics at the most granular level possible. Other tools often show that a performance issue exists (i.e. latency, memory leak, etc.) Continuously collecting profiles allows us to drill down and see why a particular system is experiencing such problems.

There are several different profilers that can be used for other use cases/resources:
* CPU Profilers
* Heap Profilers
* GPU Profilers
* Mutex profilers
* IO profilers
* Language-specific profilers (e.g. Go pprof, JVM Profiler, and the pprof support currently being added to Java)

And within each of these, there are many sub-types of profiling, all sharing the same goal of understanding the distribution of how a resource is allocated in a system.

Traditionally, profiling was seen as unsuitable for running in production due to the amount of overhead associated with that level of visibility into a system. However, due to the popularity of sampling profilers, they are becoming increasingly popular in cloud environments; they only add a few per cent overhead, making profiling in production a viable option.

Adding a "time" axis to profiling data takes the granularity and insight that comes with static profiles and enables people to understand and inspect their data from a fine-grained vantage point and a birds-eye-view. Understanding resources holistically becomes increasingly important in optimizing/debugging cloud-native applications and planning for how to distribute resource allocations.

Similar to how tracing extends your options to understand which part of your application is responsible for latency issues, profiling lets you drill even deeper and understand why those latency issues exist. Furthermore, it helps you understand which parts of the code use the most server resources.

Profiling data produced by runtimes typically includes statistics down to the line number, so they are great data to go from the "what" directly down to the "why" in terms of code.

![Image 2](/assets/profile.png)

_Image 2 shows an example icicle graph for a CPU profile of an application written in Go. It includes a kernel operation done by the Syscall call. This profile highlights that 35% of CPU time was used to compute hash, indicating potential optimization opportunities. [Source](https://pprof.me/9ce2c2d/)._

### Dumps

In software development, core dump files are used to troubleshoot a program, i.e., a crashed process. Classically, the operating system, with the help of some configuration such as location, name convention or file size, writes an image of the process's memory at the time of the crash for analysis. In cloud-native, however, core dump files' collection of a large cluster can easily create a bottleneck in storage or even the network, depending on how the cluster's storage is attached to the cluster nodes. For example, processing-intensive applications could generate core dump files of double-digit Gigabyte size.
In Linux-based systems, core dump files can be written anywhere via a global setting (/proc/sys/kernel/core_pattern). From kernel 2.6+, there is a new method of dealing with core dumps, with so-called core dump handlers. This means, in other words, that instead of delegating to the operating system the collecting of the file, the crashing process output is pushed to an application standard input, which is in charge of writing the file. For example, in Debian-based distributions, this can be done with the support of both systemd or abort. RedHat-based distributions use the so-called ABRT.
As of today, the cloud-native community still needs help with collecting the core dumps. We want to highlight at least two main reasons: Compared to a system where the application developer had access to all knobs to configure name convention, size or even file collection location, in cloud-native, the role of application and infrastructure owners is less clear and therefore (privileged) access to global system settings is less accessible. Further, data persistence is inherent to cloud-native environments: A crashing application, e.g., a pod, needs assistance collecting its core dump file to be written to a persistent volume before restarting.
An RFC of approximately six years (https://lore.kernel.org/patchwork/patch/643798/) requested namespaced core_pattern support in the Linux kernel community instead of having it as a global system setting. Also, the Docker community has an issue open with people around the same age (https://github.com/moby/moby/issues/19289) asking for core_pattern support in Docker.

## Correlating Observability Signals

Undoubtedly the observability space is complex. As you learned from previous sections, to know more about the state and behaviour of the software we run, we collect different data types, from different angles, with different intervals and pipelines: metrics, logs, traces, profiles and core dumps.

The first question that comes to mind is, why would we ever create so many types? Can't we have just one "catch-them-all" thing? The problem is we can't. In the same way, we can't have a single bicycle that works efficiently on both asphalt roads and off-roads. Each type of signal is highly specialized for its purpose. __Metrics__ are centered around reliable and cheap monitoring and analytics at scale -- a foundation for the reliable system. We collect __log lines__ that give us more insight into smaller details about the running system for more context. At some point, the details form a request tree, so __distributed tracing__ comes into play with its spans and cross-process context propagation. Sometimes we must dive deeper and jump into __performance application profiles__ to check what piece of code is inefficient and uses an unexpected amount of resources. Capturing __core dumps__ offers valuable insights into application crashes.

Having just one signal is rarely enough for a full, convenient observability story. For example, it might be too expensive to put too many details into __metrics__ (cardinality), and it's too expensive to __trace__ every possible operation reliably with near-real-time latency required for alerting. That is why many organizations aim to install and leverage multiple signals for their observability story.

There are a few challenges to overcome when building a multi-signal observability story. Unless you go with a larger vendor, you'll likely need separate systems for each observability signal. This is due to the different performance characteristics and usage patterns of each signal, requiring different storage systems and likely other installation methods.

Furthermore, given we might have up to four or more observability signals, the users of our observability system might have quite a large learning curve to understand four or more different UIs, and APIs to retrieve each signal. It is not uncommon to see users trying to take shortcuts and, for example, rarely use tracing or profiling if they are familiar only with metrics and logging.

Instead of keeping each observability signal in a silo, there is a way to allow seamless transitions between different signals. In this section, we will dive into signal correlations and how they can help with observability use experience.

**Recommendation**: All of this can be a lot to take in. If you need to decide where to start today, start with what you already have. In any cloud-native or networking environments you can likely start with metrics and with logs in more traditional setups. Work towards getting metrics into good shape, and then branch out into other signal types. This will likely have both the shortest time to value and the best cost efficiency for you.

### Signal Correlation

There are two basic ways to correlate data: By building correlations yourself, or by leveraging already existing data.

Whenever you can, you should use the same metadata structure for all your obseravbility signals. For example, if you are using Kubernetes or Prometheus you're already using labels for your metrics. Use the same labels for your logs whenever you can.

If you have to build it yourself, let's look at common data attached to all signals:

![Figure 3](/assets/correlation1.png)

_Figure 3 shows common links between four observability signals._

Thanks to the continuous collection of all observability signals, every piece of data is scoped to some timestamp. This allows us to filter data for signals within a __certain time window__, sometimes up to milliseconds. On the different dimension, thanks to the situation presented in the figure above, each of the observability signals is usually bound to a certain "target". To identify the target, __the target metadata__ has to be present, which in theory, allows us to see metrics, profiles, traces, and log lines from the target. To narrow it further, adding extra metadata to all signals about the __code component__ the observability data is gathered from, e.g. "factory", is not uncommon.

![Figure 4](/assets/correlation2.png)

_Figure 4 shows how to jump across different observability signals using consistent target metadata._

The flow presented in Figure 4 alone is quite powerful because it allows us to navigate quickly from each signal by selecting items from each signal related to a certain process or code component and time. With this in mind, some frontends like Grafana already allow such links and side views to be created.

But this is not the end. We sometimes have further details that are sometimes attached to tracing and logging. Distributed tracing gets its power from bounding all spans under a single __trace ID__. This information is carefully propagated from function to function, from process to process to link operations for the same user request. It's not uncommon to share the same information related to a request in your logline, sometimes called a __Request ID__ or __Operation ID__. With a simple trick of ensuring that those IDs between logging and tracing are the same, we strongly link each other on such low-level scope. This allows us to navigate between log lines easily and trace spans and tags bound to the individual request.

![Figure 5](/assets/correlation3.png)

_Figure 5 shows how to jump between logs and traces using request or operation ID._

While such a level of correlation might be good enough for some use cases, we might be missing an important one: Large Scale! Processes in such large systems do not handle a few requests. They perform trillions of operations for vastly different purposes and effects. Even if we can get all log lines or traces from a single process, even for a second, how do you find the request, operation or trace ID relevant to your goal from thousands of concurrent requests being processed then? Powerful logging languages (e.g. [LogQL](https://grafana.com/docs/loki/latest/logql/)) allow you to grep logs for details like log levels, error statuses, messages, code files, etc. However, this requires you to understand the available fields, their format, and how it maps to the situation.

Wouldn't it be better if the alert for a high number of certain errors or high latency of some endpoint let you know all the affected request IDs? Such alerts are probably based on __metrics__, and such metrics were incremented during some request flow, which most likely also produced a __log line or trace__ and had its __request, operation or trace ID__ assigned, right?

This sounds great, but as we know, such aggregated data, like metrics or some logline that combines the result from multiple requests, are, by design, aggregated (surprise!). We cannot pass all (sometimes thousands) requests ID that is part of the aggregation for cost and focus reasons. But there is a useful fact about those requests we can leverage. All related requests are somewhat equal in the context of such an aggregated metric or logline! So there might be no need to keep all IDs. We can just attach one representing an example case. This is what we call __exemplar__.

> [Exemplar](https://dictionary.cambridge.org/dictionary/english/exemplar): a typical or good example of something.

![Figure 6](/assets/correlation4.png)

_Figure 6 shows all possible links using target metadata, request or operation ID or exemplars._

We can use all links in the mix in a perfect observability system, giving us smooth flexibility in inspecting our system from multiple signals or viewpoints.

In theory, we could have exemplars attached to profiles too. Still, given its specialization and use cases (in-process performance debugging), it's rare that we need to link a single profile to a single request or operation, which then can give us a trace of a log line.

### Practical applications

We discussed ways you can navigate between signals, but is it useful? Let's go through two basic examples very briefly:

![Figure 7](/assets/correlation5.png)

_Figure 7 shows an example troubleshooting story that starts from the alert and utilizes smooth observability correlations._

* We got an alert about an unexpectedly high error rate exceeding our SLO. Alert is based on a counter of errors, and we see a spike of requests resulting in 501 errors. We take __exemplar__ to navigate to the example log line to learn the exact human-friendly error message. It appears the error is coming from an internal microservice behind many hops, so we navigate to traces thanks to the existence of a __request ID__ that matches __trace ID__. Thanks to that, we know exactly what service/process is responsible for the problem and dig deeper.

   ![Figure 8](/assets/correlation6.png)

   _Figure 8 shows a different example troubleshooting story that starts from the trace and utilizes target metadata correlation._

* We debug slow requests. We manually triggered requests with trace sampling and obtained __trace ID__. Thanks to the tracing view, we can see among a few processes in the way of requests, it was an ABC-1 request that is surprisingly slow for basic operations. Thanks to target metadata and time, we select relevant CPU usage metrics. We see high CPU usage, close to the machine limits, indicating CPU saturation. To learn why the CPU is so heavily used (especially if it's the only process in the container), we navigate to the CPU profile using the same __target metadata__ and __time__ selection.

### Practical Implementations

Multi-signal observability with rich correlation is still developing. Don't worry if you or the projects you use only implemented only one aspect of it. This section guides you through some semantic conventions that could link signals in a typical system. Your opinionated system might have even more links.
Let's iterate on items we have to implement to ensure the links mentioned in Figure 3 and Figure 6:

1. Consistent __target__ metadata is attached to all signals.

   We need consistent metadata to switch between observability signals from the same target (e.g., the same application). This might mean leveraging pull-based systems like Prometheus or OpenTelemetry Prometheus receiver (metrics), log tailing collectors (OpenTelemetry, Fluentd, Fluentbit etc.) and ensuring a set of consistent target labels or attributes, e.g. "cluster", "environment", "pod" and "container_name" are attached by your collector or agent. When dealing with push-based collections like [OTLP](https://opentelemetry.io/docs/specs/otel/protocol/) (metrics, logs and tracing), the instrumented application typically attaches the target information, thus ensuring consistency.

2. Consider making Operation ID, Request ID or Trace ID the same unique ID and attach it to the logging system (not only tracing!).

   Try to combine your tracing and logging client instrumentation so the tracing library generates Trace ID (which essentially represents a unique request coming through different microservices). The same Trace ID can be attached to your logline when logging an event connected to the request.

3. Instrument exemplars.

   To enable exameplars, we typically have to change client instrumentation. This is because we must inject Trace ID (when valid) to related metrics, e.g. histogram of request latencies. Many Prometheus clients (e.g. [Go](https://github.com/prometheus/client_golang/blob/v1.16.0/examples/exemplars/main.go)) and [OpenTelemetry SDKs](https://opentelemetry.io/docs/specs/otel/metrics/data-model/#exemplars) support exemplars, so it's the matter of changing corresponding instrumentation code. In the future, we might see more libraries and auto-instrumentation solutions that inject exemplars automatically.

## Use Cases

Let's go through more advanced use and categorization of observability and its signals.

### Box-based Monitoring Categories

Sometimes monitoring is called a system that can detect known unknowns -- as opposed to observability which emphasizes being able to find and reason about unknown unknowns as well.

Monitoring, traditionally, was a system admin or human operator (ops) concern. The software wasn't developed with monitoring in mind, and ops folks had to infer the state of the system from external signals (sometimes by "provoking" signals, AKA probing, e.g. with [blackbox exporter](https://github.com/prometheus/blackbox_exporter)). This is what we refer to as close-box monitoring.

The modern way is to make monitoring a developer concern, i.e. instrumenting code becomes part of the dev process, and of course, now monitoring also benefits the dev process (debugging, optimization). This means we have to open that software box (so the open-box name came), where instrumentation is the key step to increase your observability qualities.

While open-box monitoring requires more complex instrumentation, it allows more accurate and efficient signals from your application. The close-box monitoring is still a valid option if you can't change your application for monitoring needs or when you want accurately measure a user experience.

### Implementing SLIs, SLOs and SLAs

Implementing SLI, SLO, and SLA metrics lets you objectively measure service quality and customer happiness. More so over, it provides a common set of terminologies between different functions like business, product and engineering within an org. Engineering time is a scarce resource within any organization, but everyone feels like their problem is a burning problem. SLOs make such conversations more data-driven because everyone understands the business consequences of breaching SLOs. While solving internal conflicts also makes you more customer-obsessed by providing meaningful abstractions that enable meaningful and actionable alerting.

Before diving deep into the implementation details, we should clarify the definitions as they can be fairly confusing and sometimes be used interchangeably.

* Service Level Indicator (SLI): An SLI is a carefully defined quantitative measure (usually metric) of some aspect of the level of service that is provided, e.g. tail latency or error rate at the moment.
* Service Level Objective (SLO): An SLO is an objective for how often you can afford it to fail. A target value or range of values for a service level that an SLI measures. SLO is often quite restrictive at the start and adjusted later on. It’s helpful not only to finalize SLA later on but also to set development goals.
* Service Level Agreement (SLA): An SLA is a business contract that includes consequences for violating the SLO or a slightly relaxed version of the SLO.
* Error budget: Tolerance for failed events over a period determined by SLO. This is 100% minus the SLO over a certain time frame, e.g. one month.

Read more in [Google SRE Book](https://sre.google/sre-book/service-level-objectives/).

For a proposed SLO to be useful and effective, all stakeholders must agree to it. The product managers must agree that this threshold is good enough for users—performance below this value is unacceptably low and worth spending engineering time fixing. The product developers need to agree that if the error budget has been exhausted, they will take some steps to reduce risk to users until the service is back within budget. The team responsible for the production environment tasked with defending this SLO have agreed that it is defensible without Herculean effort, excessive toil, and burnout—all of which are damaging to the team's long-term health and service.

![Figure 9](/assets/slo.png)

_Figure 9 shows the steps required to define SLI, SLO and SLAs._

### Alerting on Observability data

Alerting on Observability data provides users with the ability to detect issues in the system that is being monitored. Before the widespread adoption of metrics collection, most software systems relied solely on logs to troubleshoot and triage problems and gain visibility into their systems. In addition to log search and dashboard, logs and probes served as the primary alert source for many teams and tools. This method still exists today in many modern observability systems but generally should be avoided in favour of alerting on time series metrics. More specifically, we'll look at using your defined SLOs and error budgets to perform actionable alerting.

There are many signals within your time-series data that you can alert on, and many of these will likely be application-specific. A recommended best practice is to use your team's SLOs to drive your alerts. As mentioned above, an SLO is a Service Level Objective, a target value or range of values for a service level measured by a service level indicator. For example, an SLO for a REST API may be that "95% of requests must be served in less than 500 milliseconds". You should also define error budgets to have effective alerts for your team. We'll look at ways to combine your SLO and error budgets to drive actionable alerting.

#### __Alerting in practice__

Constructing alerts can be very complex, and it is easy to get overwhelmed with false positives and have alert fatigue. Alerts should be actionable and indicate a problem someone needs to act on.

There are also different severity of alerts–not every alert is equally important, e.g. there is a difference between "paging" and "ticketing" alerts. The terminology here varies a lot. Some people say "alerts" when they specifically mean "pages", i.e. human intervention needed urgently enough to wake somebody up.

The usefulness of "ticketing" alerts is often underestimated, i.e. alerts that need attention eventually but not urgently (as things break in large-scale systems all the time, and they are designed to tolerate those breakages to a certain extent), so they can be part of normal work during business hours, for example replacing a broken non-critical disk.

We'll look at three approaches below that you can implement, one being a simpler approach, the second based on burn rate and the last one based on ML models.

##### __Target Error Rate__

Alerting on a target error rate is a common approach. Choose a small time window, say 10 minutes, and alert if the error rate in that window exceeds your SLO.

For example, if your SLO is 99.9%, alert if the error rate over the last 10 minutes is >= 0.1%. In Prometheus, this may look something like this (total HTTP request errors divided by the sum of all requests over the past 10 minutes):

```
(sum(rate(http_requests_total{code=~"5.*"}[10m])) / sum(rate(http_requests_total[10m]))) > 0.001
```

This has the advantage of being simple to see what's happening in the alert logic and delivering alerts quickly when errors occur. However, this alert will likely fire on many events that don't violate your defined SLO.

##### __Burn Rate__

Alerting on burn rate is a more sophisticated method that will likely yield more actionable alerts. First, let's define burn rate and error budgets in more detail.

Inherent in all SLO definitions is the concept of an error budget. By stating an SLO of 99.9%, you're saying that a .1% failure rate (i.e. your error budget) is acceptable for some predefined time (your SLO window). "Burn rate is how fast, relative to the SLO, the service consumes the error budget"<sup>[[8]](#references)</sup>. So, for example, if a "service uses a burn rate of 1, it means it's consuming error budget at a rate that leaves you with exactly 0 budget at the end of the SLO's time window. With an SLO of 99.9% over a time window of 30 days, a constant 0.1% error rate uses exactly all of the error budget: a burn rate of 1."<sup>[[8]](#references)</sup>

![Figure 10](/assets/burn-rate.png)

_Figure 10 shows errors relative to burn rate._

| Burn rate | Error rate for a 99.9% SLO | time to exhaustion |
|-----------|----------------------------|--------------------|
| 1         | 0.1%                       | 30 days            |
| 2         | 0.2%                       | 15 days            |
| 10        | 1%                         | 3 days             |
| 1000      | 100%                       | 43 minutes         |

_Table 3 shows burn rates and time to complete budget exhaustion._

The burn rate will allow us to reduce the size of our window and create an alert with good detection time and high precision. For our example, assume keeping the alert window fixed at one hour and deciding that a 5% error budget spend is significant enough to notify someone; you can then derive the burn rate to use for the alert.

For burn rate–based alerts, the time taken for an alert to fire is:

```
(1 - SLO / error ratio) * alerting windows size * burn rate
```

And the error budget consumed by the time the alert fires is:

```
(burn rate * alerting window size) / time period
```

So, five percent of a 30-day error budget spent over one hour requires a burn rate of 36. The alerting rule now becomes:

```
(sum(rate(http_requests_total{code=~"5.*"}[1h])) / sum(rate(http_requests_total[1h]))) > 36 * .001
```

##### Anomaly Detection

Let us start this section with a word of warning: You will find correlations in any sufficiently large data set. For example, for almost two hundred years the number of pirates on the seas and global warming were inversely proportional until the sharp rise in warming in recent years. 

While threshold-based alerting provides users with a mechanism to configure alerts based on known values, they can be rigid and unable to adapt to variations in the data caused by seasonality, ongoing rollouts and other scenarios.

The usage of machine learning techniques and statistical models helps understand several months' worth of behavioural patterns and use that to determine if the current sample that is observed is anomalous or not. Several scholarly works and open-source implementations exist to adopt anomaly detection as a mechanism to detect issues in the system that is being observed. See the [eBay user story](https://tech.ebayinc.com/engineering/sherlock.io-an-upgraded-machine-learning-monitoring-system) on this subject.

With ML-based dynamic thresholds come complexities. There are disputes if such alerts can be reliable enough for paging humans or automatic remediations. However, there is no doubt they can be extremely valuable as troubleshooting suggestions and hints.

### Root Cause Analysis

Once the observability system detects an issue, one needs to be able to triage the issue. Root cause analysis is usually done manually or through automated techniques to look at the various signals available through logs, metrics and traces and determine the most viable source of the issue. Sophisticated techniques that rely on event-graph-based approaches to process data from several microservices and develop a recommendation for the root cause greatly reduce the time to triage massively distributed systems.

## Current Gaps around Observability

In this section, we explore areas in the CNCF Ecosystem related to observability that require more work. Think about this section as the room for an amazing project, standard, blog post or even business!

Perhaps one has answers to some of those and can contribute to this whitepaper. You’re welcome to do so (please see [Contributions](#contributions) for that).

We could work towards closing those gaps in the CNCF open-source space with time. Here are a few:

### Automatic and non-intrusive instrumentation in OSS

Application owners must often modify source code and reference different agents to collect observability signals. And we can see that there are a lot more signals coming. There is room for more solutions that will automatically infer open box signals and integrate with the collection pipelines.

### Standardized query layer

Various domain-specific languages (DSL) exist for observability data systems with little consistency or interoperability between them. Observability is a foundational aspect of the development experience, and a wealth of telemetry ingestion, storage and processing systems are available. Switching to another vendor or tool remains challenging as users must often write bespoke tools to migrate data and queries. To do so, users must spend time learning the intricacies of a different observability system with non-obvious differences from the previous system. The OpenTelemetry (OTel) initiative makes it possible to interoperate across Open Source projects/vendors from client compatibility and an ingestion perspective. With OTel as an inspiration, work is still necessary to standardize how data is queried out and standardize the schema/terminology used to represent the data.

### More Observability Databases in OSS

We acknowledge that not all observability signals are easy to implement using only the OSS, and non-AGPL software, especially under CNCF. While we see mature metric databases ([Prometheus](https://prometheus.io), [Thanos](https://thanos.io) and [Cortex](https://cortexmetrics.io), we don’t have logging, tracing and profiling databases under the CNCF umbrella. However, there are a lot of nice solutions outside of the CNCF, some with less or more permissive licenses.

### Monitoring for Streaming APIs

There are a few very well-known monitoring methodologies today. For example, the [USE method](https://www.brendangregg.com/usemethod.html) described by Brendan Gregg to monitor the compute resources and the [RED method](https://www.weave.works/blog/the-red-method-key-metrics-for-microservices-architecture/ invented by Tom Wilkie to monitor request-based services.

Unfortunately, both methodologies are hard to implement for Streaming APIs. With the popularization of streaming Remote Procedure Calls (RPC), e.g. gRPC, we must develop a new or updated methodology and tools to monitor those.

## References

1. HARTMANN, Richard. Talk given at Fosdem (Brussels), Feb 2019. Available at: https://archive.fosdem.org/2019/schedule/event/on_observability_2019/. Accessed on: June 24, 2021.
2. SRIDHARAN, Cindy. _Distributed Systems Observability_. **Chapter 04, The Three Pillars of Observability**. 2018. Available at: https://www.oreilly.com/library/view/distributed-systems-observability/9781492033431/ch04.html. Accessed on: June 24, 2021.
3. BEYER, Betsy; JONES, Chris; MURPHY, Niall; PETOFF, Jennifer. _Site Reliability Engineering_. O'Reilly Media, 2016. Available at: https://sre.google/sre-book/table-of-contents/. Accessed on: June 24, 2021.
4. BEYER, Betsy; MURPHY, Niall; RENSIN, David; KAWAHARA, Kent; THORNE, Stephen. _The Site Reliability Workbook_. O'Reilly Media, 2018. Available at: https://sre.google/workbook/table-of-contents/. Accessed on: June 24, 2021.
5. SRIDHARAN, Cindy. _Monitoring and Observability_. Sep 5, 2017. Available at: https://copyconstruct.medium.com/monitoring-and-observability-8417d1952e1c. Accessed on: June 24, 2011.
6. MCCARTHY, Kate; FONG-JONES, Liz; FISHER, Danyel; MAHON, Deirdre; PERKINS, Rachel. _Observability Maturity: Community Research Findings Q1, 2020_. April, 2020. Available at: https://www.honeycomb.io/wp-content/uploads/2020/04/observability-maturity-report-4-3-2020-1-1.pdf. Accessed on: June 24, 2021.
7. Kalman R. E., _On the General Theory of Control Systems_, Proc. 1st Int. Cong. of IFAC, Moscow 1960 1481, Butterworth, London 1961. Available at: https://www.sciencedirect.com/science/article/pii/S1474667017700948?via%3Dihub. Accessed on: June 24, 2021.
8. Li et al., "Situation-Aware Multivariate Time Series Anomaly Detection Through Active Learning and Contrast VAE-Based Models in Large Distributed Systems," in IEEE Journal on Selected Areas in Communications, vol. 40, no. 9, pp. 2746-2765, Sept. 2022, doi: 10.1109/JSAC.2022.3191341.
9. H. Wang et al., "Groot: An Event-graph-based Approach for Root Cause Analysis in Industrial Settings," 2021 36th IEEE/ACM International Conference on Automated Software Engineering (ASE), Melbourne, Australia, 2021, pp. 419-429, doi: 10.1109/ASE51524.2021.9678708.

## Contributors

From the first words written until its completion, this whitepaper was a community effort. From synchronous discussion during our bi-weekly meeting, asynchronous discussions on [#tag-observability slack-channel](https://cloud-native.slack.com/archives/CTHCQKK7U) or comments and suggestions on multiple draft documents, we had way more contributors than we have ever expected. Here is an alphabetic order of contributors that have helped us.

* [Alex Jones](https://github.com/AlexsJones)
* [Alois Reitbauer](https://github.com/AloisReitbauer)
* [Arthur Silva Sens](https://github.com/ArthurSens)
* [Bartłomiej Płotka](https://github.com/bwplotka)
* [Björn Rabenstein](https://github.com/beorn7)
* [Charles Pretzer](https://github.com/cpretzer)
* [Daniel Khan](https://github.com/danielkhan)
* [David Grizzanti](https://github.com/dgrizzanti)
* [Debashish Ghatak](https://github.com/wallydrag) 
* [Dominic Finn](https://github.com/dofinn)
* [Frederic Branczyk](https://github.com/brancz)  
* [Gibbs Cullen](https://github.com/gibbscullen)
* [Gil Raphaelli](https://github.com/graphaelli) 
* [Goutham Veeramachaneni](https://github.com/gouthamve) 
* [Gregor Zeitlinger](https://github.com/zeitlinger)  
* [Jaana Dogan](https://github.com/rakyll)
* [Jason Morgan](https://github.com/wmorgan)
* [Jonah Kowall](https://github.com/jkowall)
* [Juraci Paixão Kröhling](https://github.com/jpkrohling)  
* [Ken Finnigan](https://github.com/kenfinnigan)
* [Krisztian Fekete](https://github.com/krisztianfekete) 
* [Liz Fong-Jones](https://github.com/lizthegrey)  
* [Matt Young](https://github.com/halcyondude)
* [Michael Hausenblas](https://github.com/mhausenblas)  
* [Nicolas Takashi](https://github.com/nicolastakashi)
* [Rafael Natali](https://github.com/rafaelmnatali) 
* [Richard Anton](https://github.com/ranton256) 
* [RichiH "RichiH" Hartmann](https://github.com/RichiH)
* [Rob Skillington](https://github.com/robskillington)
* [Ryan Perry](https://github.com/Rperry2174)
* [Shelby Spees](https://github.com/shelbyspees)
* [Shobhit Srivastava]( https://github.com/SinisterLight)
* [Simone Ferlin](https://github.com/sferlin)
* [Tim Tischler](https://github.com/tischler)
* [Vijay Samuel](https://github.com/vjsamuel)
* [Wiard van Rjj](https://github.com/wiardvanrij)  

Thanks, all of you!

## Contributing

Found a typo or misleading information in this paper? Looking for more information? Help us to evolve and maintain this paper! Here is how you can get involved:

* See existing [GH issues marked for v1.1 version](https://github.com/cncf/tag-observability/labels/cn-o11y-whitepaper-v1.1).
* For ideas, typos, and contributions, create a PR or add [GH issue](https://github.com/cncf/tag-observability/labels/cn-o11y-whitepaper-v1.1) against this file. Make sure they are using US English grammar. Ideally run it through [Grammarly](https://www.grammarly.com/)(free version is fine) or similar tools. Make sure to have clear message goals in mind, what you want to share, focus on full OSS tools and avoid very short sections (try to integrate with existing ones if possible).
* Feel free to join our [TAG Observability Meetings or Slack](https://github.com/cncf/tag-observability/#how-we-communicate) to share feedback and questions!
