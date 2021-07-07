# Observability Whitepaper

**We're in the public review phase!** Please read it, share your thoughts and suggest modifications. If you're feeling capable and generous, there is also a contributing section with instructions to what we still want to add to this whitepaper!

## Table of Contents
* [Executive Summary](#executive-summary)
* [Introduction](#introduction)
  * [Target Audience](#target-audience)
  * [Goals](#goals)
* [What is Observability?](#what-is-observability)
* [Observability Signals](#observability-signals)
  * [Metrics](#metrics)
  * [Logs](#logs)
  * [Traces](#traces)
  * [Profiles](#profiles)
  * [Dumps](#dumps)
* [Correlating Observability Signals](#correlating-observability-signals)
  * [Achieving multi-signal observability](#achieving-multi-signal-observability)
  * [Signal correlation](#signal-correlation)
  * [Practical applications](#practical-applications)
  * [Practical implementations](#practical-implementations)
* [Use cases](#use-cases)
  * [Implementing SLIs, SLOs and SLAs](#implementing-slis-slos-and-slas)
  * [Alerting on Observability data](#alerting-on-observability-data)
* [Gaps around Observability](#gaps-around-observability)
  * [Multi-signal correlation](#multi-signal-correlation)
* [Conclusion](#conclusion)
* [References](#references)
* [Contributors](#contributors)
* [Contributing](#contributing)

## Executive Summary

With the continuous growth of the system complexities and the data we process every second, we need better observability to understand the state of our workloads. On top of the observability tooling, it's now more common to expect every engineer responsible for running their software as a service to understand how to monitor and observe their applications. With higher customer expectations and stricter service level objectives, engineers must debug and find the root causes of problems faster than ever. 

This paper aims to get you quickly started with different kinds of observability you might need to work within the cloud-native world.

## Introduction

With the popularization of cloud computing, microservices and distributed systems, new applications are often designed and built to run on the cloud. Although this provides new strategies to build more resilient, better performant and more secure applications, it comes with the potential cost of losing control over the infrastructure supporting these workloads. Sysadmins, developers, and software operators must know the state of an application in production and the underlying infrastructure health where that application is running. Moreover, they should be able to externally observe these signals without adding, e.g. new instrumentation in the source or setting breakpoints on running production code.

Applications need to be designed and built to include and facilitate mechanisms that make them observable by some entity, e.g., whether this entity is another application or a human without access to the datacenter. The effort must be made early, beginning with design, and it often requires extra code or infrastructure automation and instrumentation. These cultural and process changes are often challenges or blockers for many organizations. On top of that, there are many methods and tools out in the market that suggest different approaches to reach a reasonable level of observability.

Community research[4] conducted by ClearPath Strategies and Honeycomb.io show that "Three in four teams have yet to begin or are early in their observability journeys" and that "There is momentum behind the shift toward achieving more observable systems". Once one reaches a satisfactory level of observability, there is no doubt of its benefits, but getting started can feel like a daunting task! Cultural changes, different tools, different objectives, different methods. So many details that need to be taken into consideration can make this journey quite confusing and painful. The purpose of this paper is to provide clarity so that more software and operations teams can gain the benefits of observability in their systems.

### Target Audience

The target audience of this paper is:

* Site Reliability Engineers
* DevOps Engineers
* Sysadmins
* Software Engineers
* Infrastructure Engineers
* Software Developers

This paper relates to any of the above roles from organizations that wish to deliver software that is both observable and integrates with their customers' existing observability systems while reaching a demonstrable level of reliability, security, and transparency. Additional organizational stakeholders such as Project, Product, Program Managers, and Architects responsible for designing and implementing such software may also be interested in this paper since observability is a multidisciplinary topic. Computer Science, Information Systems, Engineering (or related) students and people curious about the Observability domain may also find helpful information in this paper.

### Goals

Cloud computing adoption has helped small, big tech companies optimize cost, scale, and design more efficient products, but it came with its complexity. Since the infrastructure is now remote, ephemeral, and globally distributed, the control that Sysadmins once had over datacenters is now lost. Companies that once had a culture where Administrators and Developers had conflicting goals must change to a new culture where they now must work together as a single team aiming to build reliable software. Several new strategies and tools have emerged from observing the state of Cloud Native systems and helping such companies to keep their systems reliable in this new reality.

During the design and development of an observable system, it must be instrumented to send or expose telemetry data to a third party, usually a set of tools, responsible for providing meaningful information out of the exposed data. That telemetry data frequently comes in the form of metrics and logs, long used by software engineering teams, as well as traces, structured events, profiles, and crash dumps. Each signal has its purpose and best practices, and their misuse can lead to new problems when running software at scale, such as "alert fatigue" and "high cost".
Even though there are several new challenges, such as culture change, capacity planning, legal issues, and others, a lot of them were already tackled and solved by innovative companies that entered this new era early. Beginners can learn from their findings and mistakes and follow their best practices to tackle those same issues. This paper will provide the difference between observability signals and how they should be handled, list several different methods that successful companies used when tackling common issues, present several tools that fall under the observability scope and where they should fit in your observability stack, as well as show common known gaps that still wasn't solved or that a method still isn't very well consolidated in the market.

## What is Observability?

There is no doubt that observability is a desirable property of a system nowadays. Everybody is saying that, right? Some of you may have already started your observability journey, while others are reading this whitepaper right now just because everyone is saying that you should make your systems observable. The fact is that "Observability" has become a buzzword, and like every other buzzword, everyone wants to leave their mark while advocating for it, and what you have heard may have a different meaning from what it originated from. If you're going to level up your game on observability, let's try to make it clear its original purpose.

"In control theory, observability is a measure of how well internal states of a system can be inferred from knowledge of its external outputs" [9]. Being less theoretical, it is a function of a system with which humans and machines can observe, understand and act on the state of said system. So yes, observability, by definition, looks simple, but it gets complicated to decide which output(s) a system should have when implementing without an objective in mind. That's when things start to go sideways.

When getting started, it's easy just to copy someone else's work. That is one of the blessings and, at the same time, one of the curses of Open Source. There are so many examples online; helm charts, Ansible playbooks, Terraform modules, one can just run one of those scripts, and you have an observability stack up and running in just a couple of minutes. It is easy, and it works for others. Therefore it should work for me, right? Well, we're not trying to encourage you not to use those types of script, but you must keep in mind that observability is not just using all the pretty and shiny tools. You must be conscious about what outputs are coming out of your system and, more important than everything, you need to have an objective in mind! You may think: "Oh, I want to collect this particular data because you never know, I may need that in the future." and you repeat this thought for another data, and another, and another, and then you realize that you are building a data lake instead.

Observability can be used on literally all phases of the development lifecycle of a system. You can use it while testing your new feature, monitoring production resiliency, have insights about how your customers use your product, or making data-driven decisions about your product roadmap. Once you have your goal in mind, that's when you'll start thinking about the outputs, or what we like to call them, the signals.

## Observability Signals

As already mentioned, signals are the outputs that a system produces that a human, or machine, can infer knowledge from. Those signals will vary from system to system and depend on the objective you want to accomplish. It can be something that you want to measure at a certain point in time, like temperature or RAM usage, or an event that goes through many components of your distributed system that you'd like to trace down. You might want to know what function of your system is the most intensive on resources such as CPU, Memory or Disk at a random point in time or how your system broke at the exact time when it did. While some signals may overlap to infer knowledge, others are very specialized in certain aspects of a system. They can all be used together to provide different ways to observe the same piece of technology, or, as we recommend for starters, you can start with just one or a few and mature your way up to the others.

There is a really good chance that you have heard about the "Three Observability Pillars", which are metrics, logs, and traces. They are an industry standard and probably what you're going to start with. We like to think of them as the "primary signals" instead of "three pillars" for two reasons: (1) pillars carry an implicit meaning that if one of the pillars is missing, the whole structure is faded to crumble, which is not true. One can safely use just two or even just one signal and still fulfil its observability goals; (2) in the last year, more signals are becoming popular in the open-source communities like application profiles and crash dumps, and today's tooling and methodologies still don't fulfil all needs of the Tech Industry. New signals may arise in the near future, and those interested in this topic should keep an eye open for them.

![image](https://user-images.githubusercontent.com/24193764/121773601-55f86b80-cb53-11eb-8c8b-262a5aad781f.png)

All signals have different ways to be collected or instrumented. They have different resource costs to obtain, store, and analyze while providing different ways to observe the same system. Choosing between them or all of them is a game of trade-offs like all other tasks in engineering. In the next sections, we'll help you make this decision by digging deeper into each signal, starting with the people's favourites: metrics, logs and traces, and then the two new possible signals: application profiles and crash dumps.

___insert image with all 5 signals here___

### Metrics

Metrics are numeric representations of data. They fall into two main categories: data that is already numeric and data distilled into numbers. A typical example of the former would be temperature and a process counter for the latter. This differs from logs or traces, which focus on records or information about individual events.

Distilled data loses details, e.g. a process counter fails information about when specific increments happened. This trade-off makes metrics one of the most efficient signals: Subject matter experts chose what to distil and how. This reduces the load for retaining, emitting, transmitting, storing, and processing. It also reduces mental overload for human operators as they can get a quick overview of a situation.

Metrics also represent a point in time observations of the state of a system. This differs from logs or traces, which focus on records or information about individual events.

Metrics typically are either structured or semi-structured and are typically used in two ways:

* __Real-time monitoring and alerting__ - The most common use-case for metrics is to overview and drill down visual dashboards and to trigger alerts or notifications for either humans or automated systems that a monitored system has crossed a threshold or is behaving anomalously.
* __Trending and analysis__ - Metrics are also used for trend analysis over time and long-term planning purposes while also providing insights after an incident has occurred into fixing and monitoring underlying problems to prevent a recurrence.

The information provided by metrics is used to form insights around the overall behaviour and health of systems. Metrics often play a large role in the "what" is happening, sometimes the "why". For example, a metric can tell you the number of HTTP requests per second but not always why you have a spike or dip in requests. It can tell you why your load balancer is overloaded, though. In other words, metrics don't always reveal the root cause, often providing a high-level overview needed to orient and the jumping-off point to root-cause an issue.

### Logs

A log is a stream of textual entries describing usage patterns, activities, and operations within an operating system, application, server, or another device.

Logs can be categorized into different categories such as:
* __Application Logs__ - an application log is created when an event takes place inside an application. These logs help developers understand and measure how applications are behaving during development and after release.
* __Security Log__ - security logs are created in response to security events that take place on the system. These can include a variety of events such as failed log-ins, password changes, failed authentication requests, resource access, resource changes including files, devices, users, or other administrative changes. System Administrators can often configure which types of events are included in the security log.
* __System Log__ - system logs record events that occur within the operating system itself, such as kernel-level messages dealing with physical and logical devices, boot sequences, user or application authentication, and other activities, including faults and status messages.
* __Audit log__ - also called an audit trail, is essentially a record of events and changes. Typically, they capture events by recording who performed an activity, what activity was performed, and how the system responded. Often the system administrator will determine what is collected for the audit log based on business requirements.
* __Infrastructure log__ - is a vital part of infrastructure management, which involves managing the physical and logical equipment that affect an organization's IT foundation. This can be either on-premises or in the cloud and are obtained via APIs, Syslog, or other collected using host-based agents.

Logs can be useful in different scenarios - metrics, traces, security, debugging. Keeping a record of all application and system-related events makes it possible to understand and even reproduce step-by-step actions leading to a particular situation. These records are notably valuable when performing root-cause analysis providing information to understand the state of the application or system at the moment of the failure. 

Information stored in the logs is free from text, making them a challenge to derive meaning from. There have been many attempts at applying a schema to logs in the past 30 years, but none have been particularly successful. The reason for a schema makes extracting relevant information more accessible. Typically this is done by parsing, segmenting, and analyzing the text in the log file. The data from logs can also be converted to other observability signals, including metrics and traces. Once the data is a metric, it can be used for understanding the change over time. Log data can also be visualized and analyzed through log analytics technologies. 

Log levels allow expressing the importance of each log statement. One set of such log levels would be ERROR, WARNING, INFO, and DEBUG. With ERROR being the least-detailed level and DEBUG being the highest-detailed.
1. __ERROR__ communicates the occurrence and details about why a failure happened.
1. __WARNING__ is a high-level message that requires attention, although not a failure.
1. __INFO__ messages help us understand how the system is working.
1. __DEBUG__ is the level where very detailed information for each action is stored. Normally, only used during troubleshooting or for short periods due to storage or performance impact.

Use the multiple verbosity levels to generate detailed information to assist with troubleshooting and root-cause analysis.  

It's possible to forward the logs in multiple ways. The first suggestion is to configure the standard streams to send the logs directly to a central location. Second, write the logs to a message queue to be filtered or enriched before moving to their final destination.  The last approach is to use an open-source data collector application to send the logs to a central repository. Combine logs with other observability signals to have a complete view of your system.

Security is something we must have in mind when planning a logging solution. Encrypt log-related files or information at rest and in transit when sending it to a central repository. Do not store any personally identifiable information (PII) in any log. Finally, data that is truly important should not be kept solely in logs. Despite the usefulness of log statements, they are not guaranteed to be delivered. 

### Traces

Distributed tracing is the technique of understanding what happened during a distributed transaction, such as a request initiated by an end-user and its effects across all downstream microservices that were touched as a result.

Traces are typically a forest of "tracing data-points", or spans as they are normally called, and might be visualized as a Gantt chart like in the following example:

![image](https://user-images.githubusercontent.com/24193764/121788584-b82d8c80-cba4-11eb-94d3-b1dd74ccf482.png)

Traces typically represent one concrete instance of a transaction, making them a high-resolution signal in observability. Spans are highly contextualized, containing information about the span that initiated it. This makes it possible to establish a causal relationship between the different actors of a distributed system, such as services, queues, databases, and so on.

While many monitoring systems implemented their own proprietary way of trace context propagation, the industry reached a broad agreement that trace-context propagation should be done in a standardized way. This led to the creation of the W3C Distributed Tracing Working Group and the subsequent release of the W3C Trace Context Specification. Inspired by the de-facto standard B3 of the OpenZipkin project, W3C Trace Context defines standard HTTP headers and a value format to propagate context information that enables distributed tracing scenarios. The specification standardizes how context information is sent and modified between services. Context information uniquely identifies individual requests in a distributed system and also defines a means to add and propagate provider-specific context information.

Today, projects like OpenTelemetry or platforms like .NET are using W3C Trace Context as their standard propagation format, and it's to be expected that also cloud infrastructure providers will start supporting W3C Trace Context so that context won't break when passing through managed services like service gateways.

Instrumentation plays an essential role in distributed tracing, being responsible for creating the data points themselves and propagating the context from service to service. Without context propagation, we cannot link an incoming HTTP request with its downstream HTTP requests or a producer of a message and its consumers.

Instrumentation then has two main purposes for distributed tracing: context propagation and span mapping. In most cases, context propagation is done transparently by using libraries that can be integrated with HTTP clients and servers. In this part, projects, tools, and technologies like OpenTelemetry APIs/SDKs, OpenTracing, and OpenCensus can be used, among others.

![image](https://user-images.githubusercontent.com/24193764/121788568-9502dd00-cba4-11eb-9014-8fc8a9c31f05.png)
(Source: https://opentracing.io/docs/overview/)

### Profiles

As companies continue to optimize for cloud-native applications, it becomes increasingly important to understand performance metrics at the most granular level possible. Other tools will often show that a performance issue exists (i.e. latency, memory leak, etc.) Continuously collecting profiles allows us to drill down and see why a particular system is experiencing such problems.

There are several different profilers that can be used for other use cases/resources:
* CPU profilers
* Heap profilers
* GPU profilers
* Mutex profilers
* IO profilers
* Language-specific profilers (e.g. JVM Profiler)

And within each of these, there are many sub-types of profiling, all of them sharing the same goal of understanding the distribution of how a resource is allocated amongst a system.

Traditionally, profiling was seen as unsuitable for running in production due to the amount of overhead associated with that level of visibility into a system. However, due to the rise in popularity of sampling profilers, they are becoming increasingly popular in cloud environments; they only add a few percent overheads, making profiling in production a viable option.

The ability to add a "time" axis to profiling data takes the granularity and insight that comes with static profiles and enables people to understand and inspect their data from a fine-grained vantage point as well as a birds-eye-view. Understanding resources holistically becomes increasingly important in optimizing/debugging the cloud-native applications and planning for how to distribute resource allocations.  

Similar to how tracing extends your options to understand which part of your application is responsible for latency issues, profiling lets you drill even deeper and understand why those latency issues existed. Furthermore, it helps you understand which parts of code are using the most server resources.

Profiling data produced by runtimes typically includes statistics down to the line number, so they are great data to go from the "what" directly down to the "why" in terms of code.

___Insert an example image of a profile somewhere in the text___

### Dumps

In software development, core dump files are used to troubleshoot a program, i.e., a crashed process. Classically, the operating system, with the help of some configuration such as location, name convention or file size, writes an image of the process's memory at the time of the crash for analysis. In cloud-native, however, core dump files' collection of a large cluster can easily create a bottleneck in terms of storage or even network, depending on how the cluster's storage is attached to the cluster nodes. For example, processing-intensive applications could end up generating core dump files of double-digit Gigabyte size.

In Linux-based systems, core dump files can be set to be written anywhere in the system via a global setting (/proc/sys/kernel/core_pattern). From kernel 2.6+ there is a new method of dealing with core dumps, with so-called core dump handlers. This means, in other words, that instead of delegating to the operating system the collecting of the file, the crashing process' output is pushed to an application standard input, which in charge of writing the file. For example, in Ubuntu-based distributions, this can be done with the support of both systemd or abort. RedHat-based distributions use the so-called ABRT.

As of today, the cloud-native community still struggles with the collection of the core dumps. We would like to highlight at least two main reasons: Compared to a system, where the application developer had access to all knobs to configure name convention, size or even file collection location, in cloud-native the role of application and infrastructure owners is less clear and therefore (privileged) access to global system settings is less accessible. Further, an aspect inherent of cloud-native environments is data persistence: A crashing application, e.g., a pod, needs assistance when collecting its core dump file to be written to a persistent volume before restart. 

An RFC of approximately 5 years (https://lore.kernel.org/patchwork/patch/643798/) requested namespaced core_pattern support in the Linux kernel community, instead of having it as a global system setting. Also, the Docker community has an issue open with around the same age (https://github.com/moby/moby/issues/19289) asking for core_pattern support in Docker.

## Correlating Observability Signals

Undoubtedly the Observability space is complex. As you learned from previous sections, to know more about the state and behaviour of the software we run, we collect different data types, from different angles, with different intervals and pipelines:

* Metrics: Aggregatable numeric representation of state over a period of time.
* Logs: Structured or/and human-readable details representing a discrete event.
* Traces: Bits of metadata that can be bound to the lifecycle of a single entity in the system (e.g. request or transaction).

We also talk about the data that does not fit into the above categories, which is starting to earn their own "signal" badge, for example:

* Continues Profiling: Code-level consumption numbers (e.g., memory used, CPU time spent) for various resources across different program functions over time. 

The first question that comes to our mind is, why would we ever create so many types? Can't we have just one, "catch-them-all" thing? The problem is we can't, in the same way, we can't have a single bicycle that works efficiently on both asphalt roads and off-roads. Each type of signal is highly specialized for its purpose. __Metrics__ are centred around real-time, reliable and cheap monitoring, that supports the first response alerting - a foundation for the reliable system. We collect __log lines__ that give us more insight into smaller details about the running system for more context. At some point, the details form a request tree, so __distributed tracing__ comes into play with its spans and cross-process context propagation. Sometimes we need to dive even deeper, and we jump into __performance application profiles__ to check what piece of code is inefficient and use an unexpected amount of resources.

As you might have noticed already, having just one signal is rarely enough for a full, convenient observability story. For example, it's too expensive to put too many details into __metrics__ (cardinality), and it's too expensive to __trace__ every possible operation reliably with near-real-time latency required for alerting. That is why we see many organizations aiming to install and leverage multiple signals for their observability story.

### Achieving multi-signal observability

Multi-signal observability is doable, and many have already accomplished it. Still, when you take a step back and look at what one has to build to achieve this, you can find a few main challenges, missed opportunities or inefficiencies:

1. Different operational effort.

Unless you are willing to spend money on a SaaS solution, which will do some of the work for you, it's hard these days to have one team managing all observability systems. It's not uncommon to have a separate specialized team for installing, managing, and maintaining each observability signals, e.g. one for metrics system, one for logging stack, one for tracing. This is due to different design patterns, technologies, storage systems and installation methods each system requires. The fragmentation here is huge. This is what we aim to improve with open-source initiatives like [OpenTelemetry](https://opentelemetry.io/) for instrumenting and forwarding parts and [Observatorium](https://observatorium.io/) for scalable multi-signal backends.

2. Duplication of effort.

![image](https://user-images.githubusercontent.com/24193764/121791131-ecad4280-cbbc-11eb-9542-0b940f6a5846.png)

When we look at the payloads for each of the mentioned observability signals, there are visible overlaps. For example, let's take a look at the immediate collection of the data about the target visible in figure above. We see that the context about "where the data is about" (called typically "target metadata") will be the same for each of the signals. Yet because behind each of the signals, there is a standalone system, we tend to discover this information multiple times, often inconsistently, save this information in multiple places and (worse!) index and query it multiple times.

And it's not only for target metadata. Many events produce multiple signals: increment metrics, trigger logline and start tracing span. This means that metadata and context related to this particular event are duplicated across the system. In the open-source, there are slowly attempts to mitigate this effect, e.g. [Tempo](https://github.com/grafana/tempo) project.  

3. Integration between signals on ingestion level.

Given the multi-signal pipeline, it's often desired to supplement each system with additional data from another signal. Features like creating metrics from a particular collection of traces and log lines compatible with typical metric protocols (e.g. OpenMetrics/Prometheus) or similarly combining log lines into traces on the ingestion path. Initiatives like [OpenTelemetry collector's processor](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/spanmetricsprocessor) that produces RED metrics from trace spans and [Loki](https://grafana.com/blog/2020/10/28/loki-2.0-released-transform-logs-as-youre-querying-them-and-set-up-alerts-within-loki/) capabilities to transform logs to metrics are some existing movements in this area.

4. Integration between signals on usage level.

Similarly, on the "reading" level, it would be very useful to navigate quickly into another observability signal representing the same or related event. This is what we called the correlation of signals. Let's focus on this opportunity in detail. What's achievable right now?

### Signal Correlation

In order to link observability data together, let's look at common (as mentioned before, sometimes duplicated) data attached to all signals.

![image](https://user-images.githubusercontent.com/24193764/121791172-62191300-cbbd-11eb-93a5-6262d87c7873.png)

Thanks to the continuous form of collecting all observability signals, every piece of data is scoped to some timestamp. This allows us to filter data for signals within a __certain time window__, sometimes up to milliseconds. On the different dimension, thanks to the situation presented in the figure above, each of the observability signals is usually bound to a certain "target". To identify the target, __the target metadata__ has to be present, which in theory allows us to see metrics, profiles, traces and log lines from the certain target. To narrow it even further, it's not uncommon to add extra metadata to all signals about the __code component__ the observability data is gathered from, e.g. "factory". 

![image](https://user-images.githubusercontent.com/24193764/121791201-b15f4380-cbbd-11eb-9dd6-be55400d08a6.png)

This alone is quite powerful because it allows us to navigate quickly from each of those signals by selecting items from each signal related to a certain process or code component and time. Some frontends like Grafana already allows creating such links and side views with this in mind. 

But this is not the end. We sometimes have further details that are sometimes attached to tracing and logging. Particularly, distributed tracing gets its power from bounding all spans under a single __trace ID__. This information is carefully propagated from function to function, from process to process to link operations for the same user request. It's not uncommon to share the same information in your logline related to a request, sometimes called a __Request ID__ or __Operation ID__. With a simple trick of ensuring that those IDs between logging and tracing are exactly the same, we strongly link each other on such low-level scope. This allows us to easily navigate between log lines, trace spans and tags, bound to the individual request.

![image](https://user-images.githubusercontent.com/24193764/121791219-e2d80f00-cbbd-11eb-8696-09dfd226aff1.png)

While such a level of correlation might be good enough for some use cases, we might be missing an important one: Large Scale! Processes in such large systems do not handle a few requests. They perform trillions of operations for vastly different purposes and effects. Even if we can get all log lines or traces from a single process, even for a single second, how do you find the request, operation or trace ID that is relevant to your goal from thousands of concurrent requests being processed at that time? Powerful log query languages (e.g. [LogQL](https://grafana.com/docs/loki/latest/logql/)) allow you to grep logs for details like log levels, error statuses, message, code file, etc. However, this requires you to understand the available fields, their format, and how it maps to the situation in the process. 

Wouldn't it be better if the alert for a high number of certain errors or high latency of some endpoint let you know all the request IDs that were affected? Such alerts are probably based on __metrics__ and such metrics were incremented during some request flow, which most likely also produced a __log line or trace__ and had its __request, operation or trace ID__ assigned, right?

This sounds great, but as we know, such aggregated data like metrics or some logline that combines the result from multiple requests are by design aggregated (surprise!). For cost and focus reasons, we cannot pass all (sometimes thousands) requests ID that is part of the aggregation. But there is a useful fact about those requests we can leverage. In the context of such an aggregated metric or logline, all related requests are… somewhat equal! So there might be no need to keep all IDs. We can just attach one, representing an example case. This is what we call __exemplar__.

> [Exemplar](https://dictionary.cambridge.org/dictionary/english/exemplar): a typical or good example of something.

![image](https://user-images.githubusercontent.com/24193764/121791244-2a5e9b00-cbbe-11eb-82f5-aa4d87faa3f3.png)

We can use all links in the mix in a perfect observability system, which gives us smooth flexibility in how we inspect our system from multiple signal/viewpoints.

In theory, we could have exemplars attached to profiles too, but given its specialization and use cases (in-process performance debugging), it's in practice rare that we need to link to single request traces or log lines.

### Practical applications

We talked about ways you can navigate between signals, but is it really useful? Let's go through two basic examples, very briefly:

![image](https://user-images.githubusercontent.com/24193764/121791411-03a16400-cbc0-11eb-8183-e8124cf0947f.png)
* We got an alert about an unexpectedly high error rate exceeding our SLO. Alert is based on a counter of errors, and we see a spike of requests resulting in 501 errors (see also [Alerting on Observability data](#alerting-on-observability-data)). We take __exemplar__ to navigate to the example log line to learn the exact human-friendly error message. It appears the error is coming from an internal microservice behind many hops, so we navigate to traces thanks to the existence of a __request ID__ that is matching __trace ID__. Thanks to that, we know exactly what service/process is responsible for the problem and dig there more.

![image](https://user-images.githubusercontent.com/24193764/121791428-1c117e80-cbc0-11eb-9f12-39a2de1366f1.png)

* We debug slow requests. We manually triggered requests with trace sampling and obtained __trace ID__. Thanks to tracing view, we can see among a few processes on the way of requests, it was an ABC-1 request that is surprisingly slow for basic operations. Thanks to target metadata and time, we select relevant CPU usage metrics. We see high CPU usage, close to the machine limits, indicating CPU saturation. To learn why the CPU is so heavily used (especially if it's the only process in the container), we navigate to the CPU profile using the same __target metadata__ and __time__ selection. 

### Practical implementations

Is it achievable in practice? Yes, but in our experience, not many know how to build it. The fragmentation and vast amount of different vendors and projects fighting for this space might obfuscate the overview and hide some simple solutions. Fortunately, there is a big effort in open source communities to streamline and commoditize those approaches. Let's look at some open-source ways of achieving such a smooth, multi-signal correlation setup. For simplicity, let's assume you have chosen and defined some metrics, logging and tracing stack already (in practice, it's common to skip logging or tracing for cost efficiency).

From the high-level point of view, we need to ensure three elements:

1. Consistent __target__ metadata is attached to all signals.

That might feel like a hard task already, but there are some shortcuts we can make. This shortcut is called the __pull model__. For instance, consistent metadata is much easier in the Prometheus system, thanks to the single, centrally managed discovery service for target's metrics collection. Among many other benefits, the pull model allows metric clients (e.g. your Go or Python application) to care only about its own metric metadata, totally ignoring the environment it is running in. On the contrary, this is quite difficult to maintain for push model systems, which spans over popular logging and tracing collection pipelines (e.g. Logstash, non-pulling OpenTelemetry receivers, non-tailing plugins for Fluentd, Fluentbit). Imagine one application defining the node it's running on in key `node` and another mentioning this in the label `machine`, another one putting this into the `instance` tag.

In practice, we have a few choices:

* Suppose we stick to the push model (for some cases like batch jobs mandatory). In that case, we need to ensure that our client tracing, logging, and metrics implementations add correct and consistent target metadata. Standard code libraries across programming languages help, although it takes time (years!) to adopt those in practice by all 3rd party software we use (think about, e.g. Postgres). Yet, if you control your software, it's not impossible. Service Meshes might help a bit for standard entry/exit observability but will disable any open box observability. The other way to achieve this is to use processing plugins that, e.g. OpenTelemetry, offers to rewrite metadata on the fly (sometimes called relabelling). Unfortunately, it can be brittle in practice and hard to maintain over time.
* The second option is to use and prefer a pull model and define the target metadata on the admin/operator side. We already do this in open source in [Prometheus](https://prometheus.io/) or [Agent](https://github.com/grafana/agent) thanks to [OpenMetrics](https://openmetrics.io/) for continuously scraping metrics and [ConProf](https://github.com/conprof/conprof) for doing the same for profiles. Similarly, there are already many solutions to tail your logs from standard output/error, e.g. [Promtail](https://grafana.com/docs/loki/latest/clients/promtail/) or [OpenTelemetry tailing](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/logs/overview.md#via-file-or-stdout-logs) collector. Unfortunately, we are not aware of any implementation that offers tailing traces from some medium (yet).

2. Make Operation ID, Request ID or Trace ID the same thing and attach to the logging system. 

This part has to be ensured on the instrumentation level. Thanks to OpenTelemetry context propagation and APIs, we can do this pretty easily in our code by getting trace ID (ideally, only if the trace is sampled) and adding it to all log lines related to such a request. A very nice way to make it uniformly is to leverage middleware (HTTP) and [interceptors (gRPC)](https://github.com/grpc-ecosystem/go-grpc-middleware) coding paradigms. It's worth noting that even if you don't want to use a tracing system or your tracing sampling is very strict, it's still useful to generate and propagate request ID in your logging. This allows correlating log lines for the single request together.

3. Exemplars

Exemplars are somewhat new in the open-source space, so let's take a look at what is currently possible and how to adopt them. Adding exemplars to your logging system is pretty straightforward. We can add an exemplar in the form of a simple `exemplar-request=<traceID>` key-value label for log lines that aggregate multiple requests.

Adding exemplars for the metric system is another story. This might deserve a separate article I might write someday, but as you might imagine, we generally cannot add request or trace ID directly to the metric series metadata (e.g. Prometheus labels). This is because it would create another single-use, unique series with just one sample (causing unbounded "cardinality"). However, in open source, recently, we can use quite a novel pattern defined by [OpenMetrics, called Exemplar](https://github.com/OpenObservability/OpenMetrics/blob/main/specification/OpenMetrics.md#exemplars). It's additional information, attached to (any) series sample, outside of the main (highly indexed) labels. This is how it looks in the OpenMetrics text format scraped by, e.g. Prometheus:

```
# TYPE foo histogram
foo_bucket{le="0.01"} 0
foo_bucket{le="0.1"} 8 # {} 0.054
foo_bucket{le="1"} 11 # {trace_id="KOO5S4vxi0o"} 0.67
foo_bucket{le="10"} 17 # {trace_id="oHg5SJYRHA0"} 9.8 1520879607.789
foo_bucket{le="+Inf"} 17
foo_count 17
foo_sum 324789.3
foo_created  1520430000.123
```

Once defined, they get scraped together with metric samples (make sure to enable OpenMetrics format in your instrumentation client) by OpenMetrics compatible scraper (e.g. Prometheus). When that's done, you can query those exemplars by convenient [__Exemplars API__ defined by the Prometheus community](https://prometheus.io/docs/prometheus/latest/querying/api/#querying-exemplars):

```
curl -g 'http://localhost:9090/api/v1/query_exemplars?query=test_exemplar_metric_total&start=2020-09-14T15:22:25.479Z&end=020-09-14T15:23:25.479Z'
{
    "status": "success",
    "data": [
        {
            "seriesLabels": {
                "__name__": "test_exemplar_metric_total",
                "instance": "localhost:8090",
                "job": "prometheus",
                "service": "bar"
            },
            "exemplars": [
                {
                    "labels": {
                        "traceID": "EpTxMJ40fUus7aGY"
                    },
                    "value": "6",
                    "timestamp": 1600096945.479,
                }
            ]
        },
       (...)
```

Note that the `query` parameter is not for some magic ExemplarsQL language or something. This API expects any PromQL query that you might have used on your dashboard, alert or rule. The implementation is supposed to parse the query then and for all series that were used, will return all relevant exemplars for those series if present. 

This API got adopted pretty quickly by Grafana, where you can, even now, on the newest version of AGPLv3 licensed Grafana to render exemplars and allow a quick link to the trace view.

Of course, that's just the basics. There is whole infrastructure and logic in Prometheus done at the beginning of 2021 to support exemplars on scraping, storing, querying it and even replicating those in a remote write. [Thanos](http://thanos.io/) started to support exemplars, so the Grafana.

It's also worth mentioning that OpenTelemetry also inherited some form of exemplars from OpenCensus. Those are very similar to OpenMetrics one, just only attachable to histogram buckets. Yet, we are not aware of anyone using or relying on this part of Otel metric protocol anywhere, including relevant implementations like [Go](https://github.com/open-telemetry/opentelemetry-go/issues/559). This means that if you want to have a stable correlation, and an already working ecosystem, OpenMetrics might be the way forward. Plus, [OpenTelemetry slowly adopts OpenMetrics too](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/metrics/semantic_conventions/openmetrics-guidelines.md).

## Use Cases

### Box-based monitoring categories 

Monitoring can be split into 2 categories:
* Openbox monitoring
* Closedbox monitoring

Generally speaking, "closed" box monitoring refers to observing a system from the outside where the operator has no control or knowledge of the inner workings of the system. "open" box monitoring, on the other hand, refers to the more "traditional" concept of monitoring an application or system that you control and understanding how it functions, so you're able to make better decisions on how it should be observed through the Three Pillars of Observability.  

### Implementing SLIs, SLOs and SLAs

Implementing SLI, SLO and SLA metrics lets you measure service quality and customer happiness objectively. More so over, it provides a common set of terminologies between different functions like business, product and engineering within an org. Engineering time is a scarce resource within any organization, but everyone feels like their problem is a burning problem. SLOs make such conversations more data-driven because everyone understands the business consequences of breaching SLOs. While solving internal conflicts, it also makes you more customer-obsessed by providing meaningful abstractions that enable meaningful and actionable alerting.

Before we deep dive into the implementation details, we should get the definitions clear as they can be fairly confusing and sometimes be used interchangeably.

* Service Level Indicator (SLI): An SLI is a service level indicator—a carefully defined quantitative measure of some aspect of the level of service that is provided.
* Service Level Objective (SLO): An SLO is a service level objective: objective for how often you can afford for it to fail. a target value or range of values for a service level that is measured by an SLI
* Service Level Agreement (SLA): a business contract that includes consequences of violating the SLO. This is a targeted percentage
Error budget: tolerance for failed events over a period of time determined by SLO. This is 100% minus the SLO

In order for a proposed SLO to be useful and effective, you will need to get all stakeholders to agree to it. The product managers have to agree that this threshold is good enough for users—performance below this value is unacceptably low and worth spending engineering time to fix. The product developers need to agree that if the error budget has been exhausted, they will take some steps to reduce risk to users until the service is back in budget. The team responsible for the production environment who are tasked with defending this SLO have agreed that it is defensible without Herculean effort, excessive toil, and burnout—all of which are damaging to the long-term health of the team and service.

![image](https://user-images.githubusercontent.com/24193764/121790610-64786e80-cbb7-11eb-921d-6d82c8c7f906.png)

### Alerting on Observability data

Prior to the widespread adoption of metrics collection, most software systems relied solely on logs to troubleshoot and triage problems and gain visibility into their systems. In addition to log search and dashboard, logs also served as the primary Alert source for many teams and tools. This method still exists today in many modern observability systems, but generally should be avoided in favor of alerting on time series metrics. More specifically, we'll look at using your defined SLOs and errors budgets to perform actionable alerting.

There are many signals within your time-series data that you can alert on, and many of these will likely be application-specific. A recommended best practice is to use your team's SLOs to drive your alerts. As mentioned above, an SLO is a Service Level Objective, a target value or range of values for a service level that is measured by a service level indicator. For example, an SLO for a REST API maybe that "95% of requests must be served in less than 500 milliseconds". In order to have effective alerts for your team, you should also define error budgets. We'll look at ways to combine your SLO and error budgets to drive actionable alerting.

#### __Alerting in practice__
Constructing alerts can be very complex and it is easy to get overwhelmed with false positives and have alert fatigue. Alerts should be actionable and indicative of a problem someone needs to take action on. We'll look at two approaches below that you can implement, one being a simple approach and the other based on burn rate.

##### __Target Error Rate__

Alerting on a target error rate is the simplest approach you can take. Choose a small time window, say 10 minutes, and alert if the error rate in that window exceeds your SLO.

For example, if your SLO is 99.9%, alert if the error rate over the last 10 minutes is >= 0.1%. In Prometheus, this may look something like this (total HTTP request errors divided by the sum of all requests over the past 10 minutes):
```
(sum(rate(http_requests_total{code=~"5.*"}[10m])) / sum(rate(http_requests_total[10m]))) > 0.001
```
This has the advantage of being simple and straightforward to see what's happening in the alert logic and also delivering alerts quickly when errors are encountered. However, this alert is likely to fire on many events that don't violate your defined SLO.

##### __Burn Rate__

Alerting on burn rate is a more sophisticated method and one that will likely yield more actionable alerts. First, let's define what burn rate and error budgets are in a bit more detail.

Inherent in all SLO definitions is the concept of an error budget. By stating an SLO of 99.9%, you're saying that a .1% failure rate (i.e. your error budget) is acceptable for some predefined amount of time (your SLO window). "Burn rate is how fast, relative to the SLO, the service consumes the error budget" [8]. So, for example, if a "service uses a burn rate of 1, it means it's consuming error budget at a rate that leaves you with exactly 0 budget at the end of the SLO's time window. With an SLO of 99.9% over a time window of 30 days, a constant 0.1% error rate uses exactly all of the error budget: a burn rate of 1." [8]

![image](https://user-images.githubusercontent.com/24193764/121790715-74448280-cbb8-11eb-9b66-ea432377449f.png)
(Errors relative to burn rate[8])


| Burn rate | Error rate for a 99.9% SLO | time to exhaustion |
|-----------|----------------------------|--------------------|
| 1         | 0.1%                       | 30 days            |
| 2         | 0.2%                       | 15 days            |
| 10        | 1%                         | 3 days             |
| 1000      | 100%                       | 43 minutes         |
(Burn rates and time to complete budget exhaustion[8])

The burn rate will allow us to reduce the size of our window and create an alert with good detection time and high precision. For our example, assume keeping the alert window fixed at one hour and deciding that a 5% error budget spend is significant enough to notify someone, you can derive the burn rate to use for the alert.

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
## Gaps around Observability

### Multi-signal correlation

Hopefully, the section [Correlating Observability Signals](#correlating-observability-signals) explains well how to think about observability correlation, what it means and what is achievable right now. Yet let's quickly enumerate the pitfalls of today's multi-signal observability linking:

* Inconsistent metadata

 As mentioned previously, even slight inconsistency across labels might be annoying to deal with when used. Relabelling techniques or defaulting to a pull model can help.

* Lack of request ID or different ID to the Tracing ID in the logging signal.

As mentioned previously, this can be solved on the instrumentation side, which is sometimes hard to control. Middleware and service meshes can help too. 

* Tricky tracing sampling cases

Collecting all traces and spans for all your requests can be extremely expensive. That's why the project defines different sampling techniques allowing only "sample" (so collect) those traces that might be useful later on. It's non-trivial to say which ones are important, so complex sampling emerged. The main problem is to make sure correlation points like exemplars or direct trace ID in the logging system points to the sampled trace. It would be a poor user experience if our frontend systems would expose exemplar of the link that is a dead-end (no trace available in the storage). 

While this experience can be improved on the UI side (e.g., checking upfront if trace exists before rendering exemplar), it's not trivial and presents further complexity to the system. Ideally, we can check if a trace was sampled before injecting exemplar to logging on the metric system. If upfront sampling method was used, OpenTelemetry coding APIs allow getting sampling information via, e.g. `IsSampled` method. The problem appears if we talk about tail-based sampling or further processes that might analyze which trace is interesting or not. We are yet to see some better ideas to improve this small but annoying problem. If you have a 100% sampling or upfront sampling decision (ratio of request or user-chosen), this problem disappears.

* Exemplars are new in the ecosystem.

Prometheus user experience is especially great because having Prometheus/OpenMetrics exposition in your application is the standard. Software around the world uses this simple mechanism to add plentiful useful metrics. Because Prometheus exemplars are new, as are OpenTelemetry tracing libraries, it will take time for people to start "instrumenting their instrumentation" with exemplars. 

But! You can start from your own case by adding Prometheus exemplars support to your application. This correlation pattern is becoming a new standard (e.g. instrumented in Thanos), so help yourself and your users by adding them up and allow easy linking between tracing and metrics.

* Higher-level metric aggregations, downsampling.

Something that is yet to be added is the ability to add exemplars for recording rules and alerts that might aggregate further metrics with exemplars attached. This has been proposed, but the work has yet to be done. Similarly, the downsampling techniques that we discuss for further iterations of Prometheus have to think about downsampling exemplars.

* Native Correlation support in UIs.

Grafana is pioneering in multi-signal links, but many other UIs would use better correlation support given the ways shared in this article. Before the Grafana, the space was pretty fragmented (each signal usually had its own view, rarely thinking about other signals). Prometheus UI is no different. Extra support for linking to other signals or rendering exemplars are to be [added](https://github.com/prometheus/prometheus/issues/8797) there too.

## References

<!-- TODO: please add extra references here -->
1. HARTMANN, Richard. Talk given at Fosdem (Brussels), Feb 2019. Available at: https://archive.fosdem.org/2019/schedule/event/on_observability_2019/. Accessed on: June 24, 2021.
1. SRIDHARAN, Cindy. _Distributed Systems Observability_. **Chapter 04, The Three Pillars of Observability**. 2018. Available at: https://www.oreilly.com/library/view/distributed-systems-observability/9781492033431/ch04.html. Accessed on: June 24, 2021.
1. BEYER, Betsy; JONES, Chris; MURPHY, Niall; PETOFF, Jennifer. _Site Reliability Engineering_. O'Reilly Media, 2016. Available at: https://sre.google/sre-book/table-of-contents/. Accessed on: June 24, 2021.
1. BEYER, Betsy; MURPHY, Niall; RENSIN, David; KAWAHARA, Kent; THORNE, Stephen. _The Site Reliability Workbook_. O'Reilly Media, 2018. Available at: https://sre.google/workbook/table-of-contents/. Accessed on: June 24, 2021.
1. SRIDHARAN, Cindy. _Monitoring and Observability_. Sep 5, 2017. Available at: https://copyconstruct.medium.com/monitoring-and-observability-8417d1952e1c. Accessed on: June 24, 2011.
1. MCCARTHY, Kate; FONG-JONES, Liz; FISHER, Danyel; MAHON, Deirdre; PERKINS, Rachel. _Observability Maturity: Community Research Findings Q1, 2020_. April, 2020. Available at: https://www.honeycomb.io/wp-content/uploads/2020/04/observability-maturity-report-4-3-2020-1-1.pdf. Accessed on: June 24, 2021.
1. Kalman R. E., _On the General Theory of Control Systems_, Proc. 1st Int. Cong. of IFAC, Moscow 1960 1481, Butterworth, London 1961. Available at: https://www.sciencedirect.com/science/article/pii/S1474667017700948?via%3Dihub. Accessed on: June 24, 2021.

## Contributors

From the first words written until its completion, this whitepaper was a community effort. From synchronous discussion during our bi-weekly meeting, asynchronous discussions on [#tag-observability slack-channel](https://cloud-native.slack.com/archives/CTHCQKK7U) or comments and suggestions on our draft document, we had way more contributors that we have ever expected. Here is an alphabetic order of contributors that have helped us during those several months.

* [Alex Jones][Alex Jones]
* [Arthur Silva Sens][Arthur Silva Sens]
* [Bartłomiej Płotka][Bartłomiej Płotka]
* [Charles Pretzer][Charles Pretzer]
* [Daniel Khan][Daniel Khan]
* [David Grizzanti][David Grizzanti]
* [Debashish Ghatak][Debashish Ghatak]
* [Dominic Finn][Dominic Finn]
* [Frederic Branczyk][Frederic Branczyk]
* [Gibbs Cullen][Gibbs Cullen]
* [Jason Morgan][Jason Morgan]
* [Jonah Kowall][Jonah Kowall]
* [Juraci Paixão Kröhling][Juraci Paixão Kröhling]
* [Ken Finnigan][Ken Finnigan]
* [Krisztian Fekete][Krisztian Fekete]
* [Liz Fong-Jones][Liz Fong-Jones]
* [Matt Young][Matt Young]
* [Michael Hausenblas][Michael Hausenblas]
* [Rafael Natali][Rafael Natali]
* [Richard Anton][Richard Anton]
* [RichiH Hartmann][RichiH Hartmann]
* [Rob Skillington][Rob Skillington]
* [Ryan Perry][Ryan Perry]
* [Shelby Spees][Shelby Spees]
* [Shobhit Srivastava][Shobhit Srivastava]
* [Simone Ferlin][Simone Ferlin]
* [Tim Tischler][Tim Tischler]
* [Wiard van Rjj][Wiard van Rjj]

Thanks, all of you!

<!-- Please add other contributors here -->
[Alex Jones]:             https://github.com/AlexsJones
[Arthur Silva Sens]:      https://github.com/ArthurSens
[Bartłomiej Płotka]:      https://github.com/bwplotka
[Charles Pretzer]:        https://github.com/cpretzer
[Daniel Khan]:            https://github.com/danielkhan
[David Grizzanti]:        https://github.com/dgrizzanti
[Debashish Ghatak]:       @
[Dominic Finn]:           @
[Frederic Branczyk]:      https://github.com/brancz
[Gibbs Cullen]:           https://github.com/gibbscullen
[Jason Morgan]:           https://github.com/wmorgan
[Jonah Kowall]:           https://github.com/jkowall
[Juraci Paixão Kröhling]: https://github.com/jpkrohling
[Ken Finnigan]:           https://github.com/kenfinnigan
[Krisztian Fekete]:       https://github.com/fktkrt
[Liz Fong-Jones]:         https://github.com/lizthegrey
[Matt Young]:             https://github.com/halcyondude
[Michael Hausenblas]:     https://github.com/mhausenblas
[Rafael Natali]:          https://github.com/rafaelmnatali
[Richard Anton]:          @
[RichiH Hartmann]:        https://github.com/RichiH
[Rob Skillington]:        https://github.com/robskillington
[Ryan Perry]:             https://github.com/Rperry2174
[Shelby Spees]:           https://github.com/shelbyspees
[Shobhit Srivastava]:     @
[Simone Ferlin]:          https://github.com/sferlin
[Tim Tischler]:           @
[Wiard van Rjj]:          https://github.com/wiardvanrij


## Contributing

This whitepaper is still incomplete! If you want to help us, there are a few topics that we still want to include:

* *Improving your Observability - "Return on Investment"* - Implementing fine-grained Observability can be extremely expensive, especially if done naively. Usually, we recommend starting simple and iterate with more signals, more granularity and data sizes. Let's discuss those suggestions in a new section. Let's also enumerate how we should iterate and what criteria have to be met to proceed with observability expansion.
* Use cases
  * *Data Visualization and Exploration* - Building dashboards is pretty easy, but building **good** dashboards is another story. We'd like to tell best practices for dashboard-building and explain how the way we build them differs depending on what we want to achieve. E.g., analyze historical data, real-time monitoring.
* Gaps around Observability
  * *Machine Learning, Anomaly Detection, and Analytics* - There are some pretty strong and opposing opinions on whether ML/Analytics can be useful in the Observability space. We need someone with experience to explain to the community where and why it can be useful and where and why it cannot. 
  * *Monitoring Streaming APIs* - There are two very well known monitoring methodologies today. USE method to monitor compute resources and RED method to monitor request-based services. Both methodologies do not apply for Streaming APIs and, with the popularization of Remote Procedure Calls(RPC), we need to come up with a clear methodology to monitor them.
  * *eBPF* - eBPF is a revolutionary technology that can run sandboxed programs in the Linux kernel without changing kernel source code or loading a kernel module. With some creativity, it can help us achieve the long-time dream of observing systems without adding extra instrumentation. Even though the possibilities are endless, eBPF is not that popular. We'd like to tell our readers how eBPF and related tools can be a game-changer in the Observability space and why they're still not that popular.
  * *Observing short-lived systems* - Observability in the FaaS/Serverless space is still very weak, we'd like to tell our readers why it's so difficult to observe this kind of systems. How does Pull vs Push based models can interact with them and why performance overhead has been an issue for so long.

