# 可观测性白皮书

_这是一项正在进行的工作。_ 从事于白皮书工作的的人们, 请在 [Issues](https://github.com/cncf/tag-observability/issues/new) 和 [Pull Requests](https://github.com/cncf/tag-observability/pulls) 探讨白皮书。 讨论正发生在 [CNCF’s slack](https://slack.cncf.io/) (#tag-observability channel)中。

## 目录

* [概要](#概要)
* [介绍](#介绍)
  * [目标受众](#目标受众)
  * [目标内容](#目标内容)
* [可观测性是什么?](#可观测性是什么)
* [可观测性信号](#可观测性信号)
  * [Metrics](#Metrics)
  * [Logs](#Logs)
  * [Traces](#Traces)
  * [Profiles](#Profiles)
  * [Dumps](#Dumps)
* [关联可观测性](#关联可观测性)
  * [实现多信号的可观测性](#实现多信号的可观测性)
  * [信号之间的关联](#信号之间的关联)
  * [实际应用](#实际应用)
  * [实际操作](#实际操作)
* [用户案例](#用户案例)
  * [实现SLIs、SLOs和SLAs](#实现SLIsSLOs和SLAs)
  * [可观测性数据告警](#可观测性数据告警)
* [可观测性的差距](#可观测性的差距)
  * [多个信号之间的关联性](#多个信号之间的关联性)
* [结论](#结论)
* [引用](#引用)
* [贡献者列表](#贡献者列表)
* [可贡献内容](#可贡献内容)

## 概要

随着系统复杂度以及每时每刻我们需要处理的数据不断增长，我们需要更好的可观测性来让我们明确当前系统的负载状态。在可观测性工具之上，现在更多的是希望每个负责将软件作为服务运行的工程师都能够理解如何去监视和观察他们的应用程序。更高的用户期望和更严格的服务水平目标， 工程师们相比以前，需要更快的 debug并找到问题的根本原因。

这篇 paper 旨在帮助您快速了解在云原生环境中可能需要的各种可观测性。

## 介绍

随着云计算、微服务和分布式系统的普及，新多应用程序通常会被设计、构建以及运行在云上。虽然提供了一种新的方式来构建更具有弹性、性能、安全性的应用程序, 但随之而来的是增加了能够支撑应用工作的基础设施的控制的潜在成本。系统管理员、开发者和软件使用者必须知道关于应用在生产中的状态以及在应用之下的底层基础设施的运行状况。除此之外,他们应该在软件之外可以观测到这些信号, 而不需要例如在代码中添加新的仪器或在生产中正在运行的代码中添加断点。

这些应用需要设计和构建一些包含和促使外部用户可以观测到的方式(埋点)。例如, 无论这个实体是另外一个应用还是一个无法访问数据中心的人。这些需要更早,并且从设计开始, 而且这通常需要额外的代码或者插桩方式以及对应的仪表盘。 对于许多组织来说, 这种文化和处理流程变化往往意味着挑战和阻碍。除此之外,在市场上还存在许多方式和工具可以提供不同的方法来达到较为合理的可观测性水平。

ClearPath Strategies 和 Honeycomb.io 进行的社区研究[4]报告显示 “ 75%的团队尚未开始或刚开始他们的可观测性路程”以及在“实现更多可观测性系统的转变存在着更多的动力”。能够达到了一个令人满意的可观测性水平， 毫无疑问是很有利的。但刚开始可能感觉会是一项艰巨的任务！文化变化，不同的工具，不同的目标，不同的方法。所以太多的细节可能会让这段旅程变得相当混论和痛苦。这篇 paper 的目的是提供清晰的说明，以便更多的软件和使用团队可以在他们的系统中获取到可观测性的好处。

### 目标受众

这篇 paper 的适用对象为:

* SRE 工程师
* DevOps 工程师
* 系统管理员
* 软件工程师
* 基础设施工程师
* 软件开发者

这篇 paper 涉及到上述的角色，是希望可以交付既具备可观测性和与客户现存的可观测系统集成的软件，同时达到可以证明可靠性，安全性和透明度的水平。负责设计和实现这类软件的其他人员，例如项目经理、产品经理和架构师，也可能对这篇 paper 感兴趣。因为可观测性是一个多学科主题，计算机科学、信息系统、工程学(或相关学科)的学生和对可观测性领域感兴趣的人也可以在这里找到有用的信息。

### 目标内容

云计算帮助了大小不一的科技公司优化了成本、规模，并设计出更加高效的产品，但同时也带来了复杂性。由于基础设施变成远程的、短暂的、全球分布，系统管理员不再像以前那样对数据中心拥有较强的的控制力。以前存在和拥有管理员及开发者目标不一致的企业文化的公司，是时候做出改变了，他们现在必须作为一个单一的团队一起工作，以此来构建可靠的软件。

在可观测性系统的设计以及开发中，他需要将遥感测试数据发送或暴露给第三方，通常是一套工具集，负责从暴露出的这些数据中提取出有意义的信息。遥感数据通常以 metrics 、 logs、traces、具备结构化的 events，profiles 和系统崩溃时候的 dumps 文件的形式出现，这些数据被软件工程团队长期使用。
尽管仍然存在一些新的挑战，比如文化改变、能力规划、法律问题等，但很多已经被早期进入这个领域的公司解决掉了。初学者可以从他们的调研和错误中去学习，并遵循他们的最佳实践来解决问题。这篇 paper 将提供可观测性信号之间的差异，以及如何去处理他们，列出了业内公司在处理常见问题时使用的几种不同方法，除了给定可观测性范围内的几种工具，以及他们在可观测性领域的重要性以外, 同时也展示出目前业内仍未解决的一些问题，或者某种方式仍旧没得到好的运用。

## 可观测性是什么

毫无疑问，可观测性是当今系统的一个令人向往的特性。每个人都在说，对吧？你们当中的一些人可能已经开始了你的可观测旅程，而其他人正在阅读这份儿白皮书，因为每个人都在说你应该让你的系统具备可观测性。事实上，“可观测性”已经成为一个流行的词汇，就像其他的词汇一样，每个人都希望在提议它的同时再其之上留下自己的印记，你听到的可能和他的起源有一些不同的定义。如果你想让你的游戏更具备可观测性，让我们来试着明确它的最初目的。

”在控制理论中，可观测性是一种如何从当前外部输出的知识中推断衡量其内部状态的一种方法“[9]。它是一个系统系统的功能, 通过这个系统, 人类以及可以观测、理解并依据当前系统的状态做出不同的举动。所以是的, 从定义上来看很简单，但是在没有目标的情况下，决定系统应该有哪些输出就变得及其复杂了，那时候就开始变得糟糕了。

在一开始的时候，抄袭别人的作品是很容易的，这是开源带来的好处之一，同时也是缺点之一。 在网上有很多这样的例子:  helm charts, Ansible playbooks, Terraform modules。仅仅运行其中一个脚本, 你就可以在几分钟之内完成一套可观测性技术栈的搭建并让他运行起来。这很简单，对其他人来说也有用，所以对我也是有用的，对吗？ 我们并不是想要鼓励你不要使用这些脚本，但是你需要注意的是: 可观测性不仅仅是去使用这些看起来好看和闪亮的工具。你必须意识到你的系统会产生什么样的结果，更加重要的是，你需要在脑海里有一个目标。你可能会想：“ 噢, 我想收集这个特殊的数据, 因为你永远不知道, 可能在未来会需要它。”  然后你对另外一些数据有类似的想法，一个接着一个，然后你意识到你正在建立一个数据湖。

可观测性可以用在系统开发生命周期内的所有阶段。你可以在测试新特性、监测产品弹性、了解客户使用如何时候用你的产品或依据数据驱动去制定产品规划路线。一旦你确定了目标之后，就会考虑输出一些数据，或者我们喜欢将它成为 “信号”。

## 可观测性信号

如之前所述，信号是由系统产生的输出数据，人类或机器可以从中推断内容。这些信号是什么会因为系统而异，也取决于你想要达成的目标。它可能是你想要在某个时刻测量的东西，例如温度或者 RAM 使用情况，或者在分布式系统中你想要追踪的众多组件发生的事件。你可能想知道在某个随机时间点，系统的哪个功能消耗了较多的 CPU、Mem 或者磁盘等资源，或者在特定的时间点，系统是如何崩溃的。虽然一些信号可能一起来还原业务现场，但是其他信号在系统的某些方面非常专业。他们可以一起使用，提供观察同一个技术的不同方式。或者正如我们对初学者的建议，你可以从一个或几个信号开始，然后逐步完善其他技术。

你可能听过“可观测性三大支柱”， 即 metrics, logs, traces。 我们喜欢把它们当作是“主要的信号”，而不是“三大支柱”，原因有两个：（1）支柱隐含的意义是如果有一个缺失，整个结构就会蜕化而崩溃，这是不正确的。人们可以安全的使用两个甚至于一个信号, 仍然可以实现可观测性目标。（2）去年开始，越来越多的信号在开源社区流行起来，比如 applicaiton profiles 和 crash dumps，而现存的工具和方法仍旧不能满足科技行业的所有需求。在不久的将来可能会出现新的信号，对这个话题感兴趣的人应该密切关注。

![image](https://user-images.githubusercontent.com/24193764/121773601-55f86b80-cb53-11eb-8c8b-262a5aad781f.png)

所有的信号都有不同的收集和测量方式，他们花费不同的资源来获取、存储和分析。同时提供不同的方法来观测相同的系统。选择其中一部分或者全部选择，就像工程学中的其他任务一样，是一个权衡的游戏。在下一节中, 我们将深入研究每个信号, 从人们最喜欢的 metrics，logs 和 traces 开始，然后是两个存在可能性的新的信号:  applicaiton profiles 和 crash dumps。

___insert image with all 5 signals here___

### Metrics

Metrics是数据的数值表现。他们主要分为两类: 已经是数值的数据和被转换为数值的数据。前者的典型案例是 温度，后者则是 process counter。这与 logs 或者 traces 不同，后者侧重于单个事件的记录或信息。

转换过的数据丢失了细节，例如 process counter 会丢失有关特定增量发生时间的信息，这种权衡使 metrics 变成最有效的信号之一：你可以选择提取什么以及如何去提取，这减少了关于为保留、发射、转发、存储和处理的负载，还减少了人们的心里压力，因为这样可以快速了解情况。

Metrics 还表示系统在某个时刻的可观测状态，与 logs 和 traces 不同，后者更侧重于单个 Event 的记录和信息.

Metrics 通常是结构化或者半结构化的, 通常以两种方式使用:

* _实时的监控和告警_ - Metrics 最常见的使用是概述和深入可视化仪表盘，并触发告警或通知，无论是人为或者自动化系统，监控系统已经超过了阈值或当前行为出现异常状况。
* _趋势和分析_ - Metrics 也用于长期的趋势分析和长期计划，同时也在事件发生后提供解决和监控潜在问题的建议，杜绝相关情况再次发生。

Metrics 提供的信息用于衡量关于系统整体行为和健康状态。Metrics 通常在 “发生了什么”中扮演重要角色，有时候是“为什么”。例如，某个指标可以告诉你每秒钟 HTTP 请求量的大小，但通常不可以告诉你为什么请求出现了峰值或者下降。不过，它可以告诉你为什么 负载均衡过重。换句话说，metrics 通常不会告诉你根本原因，通常提供了一个需要定位的高级视角和问题产生的根本原因的开始。

### Logs

logs是用户描述 在操作系统、应用程序、服务器或其他设备中,使用的模式、活动和操作的一系列文本对象流。

logs可以被分为不同的种类：

* _应用logs_  - 当应用程序内部发生事件时，会创建应用程序logs。这些logs可以帮助开发者了解和衡量应用程序在开发中及发布后的行为方式。
* _系统logs_ - 系统logs记录操作系统本身发生的事件，例如处理物理和逻辑设备的内核级消息、引导序列、用户或者应用程序身份样真以及其他活动，包括故障和状态消息。
* _安全logs_ - 安全logs是为了响应系统上发生的安全事件而创建的，这些可能包括各种事件，例如登陆失败、密码修改、身份验证请求失败、资源访问、资源更改(包括文件、设备和用户)或其他管理更改。系统管理员通常可以配置安全logs中包含哪些类型的事件。
* _审计logs_ - 审计logs也称为审计追踪，本质上是事件和变化的记录。通常，他们通过记录谁执行了活动、执行了哪些活动以及系统如何响应来捕获事件。通常系统管理员会根据业务需求决定为审计logs收集什么。
* _基础设施logs_ - 基础设施logs是基础设施管理的重要组成部分，在本地或者云上，涉及管理影响组织 IT基础的物理设备和逻辑设备，并且可以通过 API、系统logs或者其他使用基于主机之上的代理收集的方式去获取。

logs在不同的场景下都很有用 - metrics, traces, 安全, debug。保存关于应用和系统相关的所有事件记录，可以确定甚至重现出导致出现特定情况的分步操作。这些记录在去做根因分析时非常有价值，这些分析提供了在故障发生时，了解应用或者系统的信息。

存储在logs中的信息与文本内容无关，所以很难从中获取到有意义的信息。在过去的30年里，很多人尝试将 schema 应用到logs里，但是都没有特别成功。原因在于 schema 让提供一些相关信息变得更加容易。 一般是将logs文件中的文本信息通过解析、分段 和分析来实现的。logs里的数据也可以转换成其他的可观测性信号，包括 metrics 和 traces。一旦数据被转换为 metrics，就可以用来了解随着时间变化的内容。logs数据还可以通过logs分析技术来进行可视化和分析。

logs级别是可以用来标识每条logs数据的重要性。其中一组logs级别是 ERROR，INFO 和 DEBUG。其中 ERROR 是最不详细的logs级别，DEBUG 则是最详细的logs级别。

1. __ERROR__  传递故障发生的原因以及相关详细信息。
2. __WARNING__  是一个需要注意的高级别消息, 虽然它不是一个失败。
3. __INFO__  适用于帮助我们理解系统是如何运行的。
4. __DEBUG__  是用于表示存储每个操作非常详细信息的一个级别。一般而言，仅仅在问题排查，或者因为存储或性能有影响的时候被短暂使用。

使用多个详细级别来生成详细信息，从而帮助我们进行问题排查和分析问题根本原因。

转发logs的方式有多种选项。第一个建议是配置标准流，把logs直接发送到中心位置。然后，在logs被转发到最终目的地之前，将logs写入需要过滤或者富化的消息队列中。最后一种方式则是使用开源数据收集器应用来把logs发送到集中式存储中。把logs与其他的可观测性信号结合起来，可以获得系统的全局视图。

在规划logs解决方案的时候，我们必须牢记安全性。把静态或者传输中的logs文件发送到集中式存储时需要对其进行加密，不要在任何logs数据中存储个人身份信息。 虽然logs的数据很有用，但是对于重要数据不应该只保存在logs中，因为logs数据是不可以被用于交付的。

### Traces

分布式追踪是一种用于理解分布式事务过程中发生的技术, 例如终端用户发起的一次请求以及对其下游微服务造成的影响。

Traces 通常是一组被称为 “tracing 数据点”或者是一组可以用甘特图来表示被称作为 span，如下图所示:

![image](https://user-images.githubusercontent.com/24193764/121788584-b82d8c80-cba4-11eb-94d3-b1dd74ccf482.png)

Traces 通常用于表示事务的一个具体实例，使它们称为可观测性中的高分辨率信号。Spans 是高度上下文的，其中包含了关于初始化它的 span 的信息。这使得在分布式系统的不同参与者(例如服务，队列，数据库等)之间建立因果关系成为一种可能。

虽然很多监控系统实现了他们自己独有的 trace context 透传的方式，但业内达成了广泛的共识：trace context 传播应该以标准化的方式去执行。这促进了成立了 W3C 分布式追踪工作小组和制定并更新了 W3C Trace Context 规范的后续版本。受OpenZipkin 项目真实意义标准 B3启发，W3C Trace Context 定义了标准 HTTP Headers 和 值的格式来传播 context 信息，从而支持分布式跟踪的场景。该规范规定了如何在 services 之间发送和修改 context 信息。Context 信息唯一标识了分布式系统内的各个请求，还定义了添加和传播 provider-specific 的 context 信息的方式。

现在，像 OpenTelemetry 这样的项目或者像 .net 这样的平台都在使用 W3C Trace Context 作为他们的标准传播格式，而且可以预期的是，云基础设施厂商也将开始支持 W3C Trace Context，这样在通过像 service gateways 这样的托管服务时，不会出现 context 被中断的情况。

插桩(组件埋点)在分布式追踪中扮演者重要的角色，它负责创建数据点本身以及将 context 在服务间进行传递。如果没有 context 传播，我们就无法将传入的 HTTP 请求与它的下游 HTTP 请求或消息的生产者及消费者连接起来。

插桩在分布式追踪有两个主要目的：Context 传播 和 span mapping。大多数情况下, 通常可以使用与 Http 客户端/服务器端 集成的库透明的进行传播。在这一部分中，项目、工具和技术可以使用像 OpenTelemetry API/SDKS 、Open Tracing 及 Open Census 等都可以使用。

![image](https://user-images.githubusercontent.com/24193764/121788568-9502dd00-cba4-11eb-9014-8fc8a9c31f05.png)
(Source: https://opentracing.io/docs/overview/)

### Profiles

随着公司对云原生应用程序不断的进行优化，尽可能在细粒度级别上去了解性能 metrics 变得愈来愈重要。其他工具通常会明显存在性能问题(例如延迟、内存泄漏等)。 持续收集 profiles 使我们可以深入了解某个特定的系统会遇到这样问题的原因。

有一些不同的profiles 可以用在不同的用例和资源上:

* CPU Profilers
* Heap Profilers
* GPU Profilers
* Mutex profilers
* IO profilers
* 特定语言的 profilers(例如 JVM Profiler)

在每种类型的 profiling 中，都有许多子类型，他们拥有一个共同的目标，那就是理解资源是如何在系统中被分配的。

在过去，profiling 被认为是不适合在生产环境中运行，因为与系统要求的不同级别的可见性相关消耗太大。然而, 由于采样 profilers 的普及，他们在云环境中变得越来越普遍；它们仅仅增加了几个百分点的性能消耗，使得在生产环境中进行 profiling 变成一个可行的选择。

采用静态 profies 的粒度和洞察力为 profiling 数据添加“时间”轴的能力，使得人们能够从一个细粒度的有利位置和鸟瞰图去理解和检查他们的数据。在优化/调试云原生应用以及规划如何去分配资源时，全面的去理解资源变得愈来愈重要。

与 tracing 是如何扩展你的选项并用于理解应用程序的哪个部分导致延迟问题的发生的作用类似，profiling 可以让你更加深入的挖掘并理解那些导致延迟问题存在的原因。另外，它还可以帮助你了解哪些代码使用了最多的服务器资源。

运行期生成的 profiling 数据通常包括统计到行号，因此他们是从 “是什么” 到 “为什么”的重要数据。

___Insert an example image of a profile somewhere in the text___

### Dumps

在软件开发中，核心的 dump 文件是用于排除程序故障。例如，一个崩溃的进程。通常，操作系统会在一些配置(例如位置、命名约定或文件大小)的帮助下，会写入进程崩溃时的内存镜像中用于分析。然而，在云原生中，大型集群的核心 dump 文件集合很容易在存储甚至网络方面存在瓶颈，具体取决于集群的存储是如何连接到集群节点中去的。例如，处理密集型的应用程序最终可能会生成两位数 Gb 大小的核心 dump 文件。

基于 Linux 衍生的系统中, 可以通过全局系统变量(/proc/sys/kernel/core_parrern)将核心的 dump file 设置和写入到系统中的任何位置。从内核2.6以后，有一种处理核心 dump file 的新方法，即所谓的核心 dump 处理程序。这意味着，不是将文件的收集工作下发给操作系统，而是将崩溃的进程输出推送到负责写入文件的应用程序的标准输入流中。例如，在基于Ubuntu 的发行版中，这些可以在 systemd 或 abort 的支持下完成。基于 RedHat 的发行版去使用所谓的 ABRT。

直到现在，云原生社区仍然在努力收集核心 dumps。我们想强调只有两个主要的原因：与一些应用开发者可以访问所有可选项的配置来约定名称、大小甚至文件集合位置的系统相比，在云原生环境中，应用和基础设施的所有者角色不是那么明确，因此(有特权的去)访问系统全局配置的权限较低。另外一方面，云原生环境一个固有的问题是数据的持久化：崩溃的应用(例如 Pod)在重启之前要收集的核心 dump 文件并写入持久卷时需要帮助。

一个大约5年前的RFC（https://lore.kernel.org/patchwork/patch/643798/），请求Linux 内核社区中支持 core_pattern 的命名空间，而不是将其作为系统全局变量设置。除此之外，Docker 社区有一个开放问题（https://github.com/moby/moby/issues/19289），要求在 Docker 中提供 core_pattern 支持。

## 关联可观测性

可观测性的技术栈无疑是复杂的。正如在前面章节所学到的，为了我们了解更多关于软件运行状态和行为，我们需要从不同的角度，以不同的间隔和管道来收集不同类型的数据：

* Metrics: 在一段时间内用可聚合的数字表示的状态。
* Logs: 一种用于表示离散事件, 具备结构化/人类可读的细节数据。
* Traces: 可以绑定到系统中单个实体的生命周期的 元数据位（例如 request 或 transaction）。

我们还讨论了不属于上述类别的数据，他们开始获得了属于自己的 “信号”徽章，例如：

* Continues Profiling: 随着时间的推移, 跨越不同程序不同功能的各项资源的 Code-level 数字消耗值(例如: 使用的内存、消耗的 CPU 时间)。

我们想到的第一个问题是，为什么我们要创造这么多类型(的数据)呢？我们为什么不能只有一个 “抓到所有(包含所有特性)”的数据吗？ 问题在于我们做不到，类似的，我们不能有一辆既可以在柏油路又能在越野路上都可以有效工作的自行车，每一种信号都有他们独特的用途。_Metrics_ 以实时、可靠、廉价的监控为中心，是支持快速、可靠告警的基础。我们收集 _log lines_，是为了让我们更加深入的了解运行时系统的细节以便获得更多的上下文(细节)。 在某些时候，更多的细节来自于请求树，所以_distributed tracing_ 开始发挥其 spans 和 跨进程 context 传播的作用。另外一些时候，我们会跳到 _应用性能profiles_ 来检查哪些代码效率低下并使用了意想不到数量的资源。

正如你可能已经注意到的那些一样，只有一个种类的信号对于一个具备完整性、方便性的可观测性故事来说是不够的。例如，吧太多的细节放入到 _metrics_ (基数)中成本过高，并且在告警所需要操作的的接近实时延迟的情况下，较为可靠的 _trace_ 比较昂贵。 这也就是为什么我们看到许多组织致力于去为他们的可观测性接入和使用多个信号的原因。

### 实现多信号的可观测性

具备多信号的可观测性是可行的，已经有很多人实现了它。然而，当你后退一步去查看实现这一目标必须做些什么的时候，你会发现一些主要的挑战、错失掉的机会或者低效率:

1. 不同的实操内容。

除非你愿意花钱在能够帮你完成一些工作的 SaaS 解决方案上, 否则现在让一个团队去管理所有的可观测性系统是很困难的。拥有一个独立且专业的团队来安装、管理和维护每个可观测性信号的情况并不少见，例如一些人用于 metrics 系统(的日常迭代和维护),  一些人用于 logging 技术栈， 一些在 tracing 上。这源于每个系统需要不同的设计模式、技术、存储系统和安装方式。这种分裂是巨大的。这就是我们意在通过开源计划改进的目标, 例如用于检测和转发组件的 [OpenTelemetry](https://opentelemetry.io/)和用于可扩展多信号的 [Obsevatorium](https://observatorium.io/) 后端。

2. 重复的工作。

![image](https://user-images.githubusercontent.com/24193764/121791131-ecad4280-cbbc-11eb-9542-0b940f6a5846.png)

当我们查看每个被提到的可观测性信号的有效载荷时，会发现有明显的重叠。例如，让我们看看上图中关于目标的即时数据集合。我们可以看到关于 “数据在哪儿”(通常称为“目标元数据”)的上下文对于每个信号而言都是相同的(内容)。然而，由于每个信号背后都有一个独立的系统，我们往往会重复发现这样的数据，通常是不一致的，将这样的信息保存在多个地方，(更糟糕的是)被多次索引和查询。

它不仅仅作用于目标元数据。很多事件产生了多个信号：metrics 增量，触发 logline 和开启一个 span 的追踪。这意味着与当前特定事件有关的元数据和 context 在整个系统中都是重复的。在开源软件中，人们正在尝试慢慢减少这种影响, 例如 [Tempo](https://github.com/grafana/tempo)项目。

3. 在摄取级别的信号之间的集成。

鉴于多信号管道，通常希望使用来自另外一个信号的额外数据来补充每个系统。诸如，从与典型的 metrics 协议 (例如OpenMetrics/Prometheus)兼容的特定 traces 和 logs 集合创建 metrics，或类似将 logs 合并到采集路径上的 trace 中。诸如 [OpenTelemetry collector's processor](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/spanmetricsprocessor) 之类的倡议，它从 trace spans 和 [Loki](https://grafana.com/blog/2020/10/28/loki-2.0-released-transform-logs-as-youre-querying-them-and-set-up-alerts-within-loki/) 将 traces 和 logs 转换为 metrics，这些都是现在这个领域在这方面正在做的一些事情。

4. 在使用级别上的信号之间的集成。

类似的，在“读取”的层面上，从一个信号快速跳转到另外一个具备相同或相关事件的可观测信号将非常有用。这就是我们所说的信号相关性。让我们详细说说这些细节，现在有什么可以实现的?

### 信号之间的关联

为了能够将可观测性数据链接在一起, 让我们看一下附加在所有信号的常见(如上述中有时候可重复的)数据。

![image](https://user-images.githubusercontent.com/24193764/121791172-62191300-cbbd-11eb-93a5-6262d87c7873.png)

由于收集所有可观测性信号的连续格式，每条数据都被限定在某个时间戳之内。这允许我们在_特定的时间窗(有时持续几毫秒)_ 内过滤信号数据。在不同的维度上，如上图所示，每个可观测性信号通常绑定到某个 “目标”上。为了识别目标， _目标元数据_ 必须存在，这在理论上允许我们看到来自特定目标的 metrics、profiles、traces 和 logs 。为了进一步的缩小范围，将额外的元数据添加到有关_code component_的所有信号中，并且从中收集可观测性数据的情况并不少，例如 “factory”。

![image](https://user-images.githubusercontent.com/24193764/121791201-b15f4380-cbbd-11eb-9dd6-be55400d08a6.png)

就这一种方式就已经非常强大,因为它允许我们通过从每个信号中选择与某个进程或代码组件和时间相关的选项来快速导航到每个信号。一些前端，如 Grafana 已经允许我们创建这样的链接和 side views。

但这还不是最后，我们有时候会有更多的细节，这些细节有时候会被附加到 traces 和 logs 中。特别是，分布式链路追踪强大之处在于将所有 span 限定在一个 _trace ID_下。 对于同一个用户请求，这个信息会从函数到函数、从进程传播到另外一个进程，用于链接相同用户请求的操作。在 logs 中共享与请求相关的相同信息并不罕见，有时候被称为 _Request ID_ 或 _Operation ID_。通过确保 logs 和 traces 之间的 id 完全相同的简单技巧，我们可以在这样低级别的范围内将彼此紧密的联系起来。这使得我们能够轻松的在绑定到单个请求中的 logs, trace spans and tags 之间相互跳转。

![image](https://user-images.githubusercontent.com/24193764/121791219-e2d80f00-cbbd-11eb-8696-09dfd226aff1.png)

虽然这种级别的相互联系对于某些用例来说已经足够好了，但我们可能忽略了一个重要的问题：大规模集群下的系统。在这样的系统中，程序不会处理少量的请求。他们为完全不同的目的请求和小伙执行数万亿次操作。 即便我们可以从单个进程中获取到所有的 logs 和 traces，但是如何从但是正在处理的数千个并发请求中到与你的目标相关的请求、操作或者 trace id，即使是一秒钟的数据量。强大的 logging 语言 [LogQL](https://grafana.com/docs/loki/latest/logql/) 允许你筛选 logs 用于获取 log level、error statuses, message, code file等详细信息。但是，这要求你了解可用字段、格式以及它是如何映射到处理过程中的。

如果针对某些 endpoint 的大量错误或者高延迟的警报让你知道所有受影响的 request IDs，不是一件更好的事儿吗？这样的警报可能基于 _metrics_并且这类 metrics 在某些请求流期间增加，很可能这时候也产生了 _logs 或 traces_，并且为其也分配了 _request, operation 或 trace ID_, 对吗?

这听起来很棒，但正如我们所知，这些 metrics 或者聚合多个请求结果的 logs 在设计上是聚合的。因为成本和关注点的原因，我们不能通过聚合中的所有(有时候是数千个)请求 ID，但有一个是有用的事实，关于这些我们可以利用的请求，有一个有用的事实。 在这样的一个聚合 metrics 或 logs 的上下文中，所有相关的请求 ..... 有点儿相等! 因此，可能不需要保留所有的 ID，我们可以只附加上一个，代表一类实例的案例。这就是我们所说的 _exemplar_。

> [Exemplar](https://dictionary.cambridge.org/dictionary/english/exemplar): 一个典型的案例或好的事例

![image](https://user-images.githubusercontent.com/24193764/121791244-2a5e9b00-cbbe-11eb-82f5-aa4d87faa3f3.png)

我们可以在一个完美的可观测性系统中使用 已经混合了的 links，这使得我们在多个信号/veiwpoints 方面具备平滑的灵活性。

理论上，我们可以将 exampars 也附加到 profiles 中，但是考虑到它的专业性和用途(进程性能调试)，实际上我们很少需要链接到单个请求的 trace 或 log 上。

### 实际应用

我们讨论了在多个信号之间相互跳转的方法, 但是它真的是有用的吗? 让我们简单的看两个基本案例:

![image](https://user-images.githubusercontent.com/24193764/121791411-03a16400-cbc0-11eb-8183-e8124cf0947f.png)

* 我们收到了一个关于超出 SLO (service level objectives) 的意外高错误率的告警。告警来源于错误的计数器值，我们看到请求暴增导致 501 errors。我们使用_exemplar_ 导航到事例的 logs 以了解准确的可供人类阅读的错误消息中。 错误似乎来自于依赖深层次的内部微服务系统，由于存在与 _trace ID_ 匹配的 _request ID_，所以可以跳转到 traces。多亏了这一点，我们确切的了解到哪个 service/process 导致了这个问题，并进一步挖掘更多的信息。

![image](https://user-images.githubusercontent.com/24193764/121791428-1c117e80-cbc0-11eb-9f12-39a2de1366f1.png)

* 我们去 debug 慢请求，我们使用 trace 采样手动触发请求并获得 _trace ID_。多亏了 tracing view，我们可以在请求方式的几个进程中看到，对于基本操作而说，ABC-1 请求的速度非常的慢。由于目标元数据和时间，我们选择了相关的 CPU 使用率 metrics。 我们看到 CPU 使用率很高，接近了机器的限制值，表明 CPU 已经饱和。为了了解 CPU 使用率高的原因(特别是当它是容器中仅存的进程)，我们使用相同的 _目标元数据_ 和 _time_ 选择导航到 CPU profile。

### 实际操作

在实际应用中可以实现吗？是的，但根据我们的经验，知道如何构建它的人并不多。争夺这个相关领域的不同供应商和分散的项目可能会混淆概述，并将一些简单的解决方案隐藏起来。幸运的是，开源社区正在努力的简化和商品化这些方法。 让我们看一下实现这种平滑的多信号关联的一些开源方案。为了简单起见, 假设你已经选择并定义了一些 metrics、logs和 trace 的技术栈(在实践中, 为了节省成本, 通常跳过 logs 或 traces)。

从更高层次的角度来看,我们需要确保三个要素:

1. 一致的_target_ 元数据被附加到了所有的信号内。

这可能已经是一项艰巨的任务，但我们可以走一些捷径。这样的捷径被称为 _pull model_。 例如，Prometheus 系统中一致性的元数据实现更容易，这要归功于用于目标指标收集具备单一性、集中管理的发现服务。在许多其他好处中，pull 模型允许 metrics clients （例如你的 Go 或 Python 应用）只关心他自己的 metrics 元数据，完全忽略了它当前运行的环境。相反，这对于 push 模型的系统来说很难维护，横跨流程的 logging 和 tracing 收集管道 （例如 Logstash，非pull 的 Otel receivers， Fluentd 和 Fluentbit 的非采样插件）。想象一下，一个应用定义了 `node`中运行的节点的 key，另一个应用在在 “machine” label 中提到了这一点，另外一个应用将其放在了 “instance” 的 tags 中。

实际上，我们有几个选择：

* 假设我们坚持 push 模型(在某些情况下, 比如强制批处理任务)。在这种情况下, 我们需要确保我们的 client tracing， loging 和 metrics 正确的添加了一致的目标元数据。跨语言的标准代码库是有帮助的，尽管我们使用的所有第三方软件(如Postgres)都需要实践(好几年!) 来采用这些代码库。 然而，如果你能控制你的软件，这也不是不可能的。 Service Meshes 可能对标准的 出入口的可观测性有所帮助，但会禁用任何 open 软件的可观测性。另外一种实现方式是使用 plugins，例如 Open Telemetry，提供了即时重写元数据(有时候被称为重新标记)。不幸的是，它在实践中可能非常的脆弱，而且随着实践的推移会很难维护。
* 第二个选项是使用 pull 模型，并在管理/操作端去定义目标元数据。我们已经在开源 [Prometheus](https://prometheus.io/)  或 [Agent](https://github.com/grafana/agent) 中这样做了，这要感谢 [OpenMetrics](https://openmetrics.io/) 不断的抓取 metrics，以及 [ConProf](https://github.com/conprof/conprof) 为 profiles 做相同的工作。同样的, 已经有很多解决方案可以将你从标准输出和错误logs中拖出来, 例如[Promtail](https://grafana.com/docs/loki/latest/clients/promtail/) 或 [OpenTelemetry tailing](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/logs/overview.md#via-file-or-stdout-logs) 收集器。不幸的是, 目前我们还没有发现任何提供来自某种介质的 tail traces 实现方案。

2. 使 Operation ID, Request ID 或 Trace ID 相同, 并附加到 logging 系统中。

这部分必须在仪表级别上得到保证。多亏了 Open Telemetry context 传播和 APIs， 我们可以通过获取 trace ID(理想情况下, 仅当trace 被采样时)并将其添加到与这类请求相关的所有 logs 中，在代码中非常容易的可以做到这一点，实现统一的一个好方法是利用中间件 (HTTP) 和 [拦截器](https://github.com/grpc-ecosystem/go-grpc-middleware) gRPC 代码案例。值得注意的是，即使你不想用 trace 系统，或者你的 trace 采样非常严格，在 logs 中生成和传播 request ID 仍然是有用的，这允许将单个 request 下的所有 logs 关联在一起。

3. Exemplars

Exemplars 在开源领域有点儿新颖，所以让我们来看看目前有哪些可能的，以及如何去采用他们。向 log 系统添加 exemplar 是非常简单的，我们可以以 `exemplar-request=<traceID>` key-value 的格式为聚合多个请求的 logs 添加一个 exemplar。

为 metrics 系统添加 exemplars 则是另外一回事儿了，可能值得我将来单独去写一篇文章，但是你可以想象，我们通常不能直接将 request ID 或 trace ID 立即添加到 metrics series 元数据中(例如 prometheus labels)。 这是因为它会用一个 sample 创建另外一个具备一次性、独特的 series(导致没有边界的“基数”)。然而，在开源中，最近我们可以使用[OpenMetrics 称为 Exemplar](https://github.com/OpenObservability/OpenMetrics/blob/main/specification/OpenMetrics.md#exemplars) 定义的一种相当新颖的模式。它是可以附加到 (任何) series sample中去，在主(高度indexed)标签之外的内容。 这是它在 Open Metrics 文本格式中的样子, 如Prometheus：

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

一旦定义好, 它们就会被 OpenMetrics 兼容的抓取工具(例如 Prometheus)与 metrics samples(确保在你的 客户端埋点启用 OpenMetrics 格式) 一起被抓取. 之后，你可方便的通过由 [Prometheus 社区定义的 _Exemplars API_](https://prometheus.io/docs/prometheus/latest/querying/api/#querying-exemplars)来查询这些样本:

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

注意的是，“query” 语法不是用于某个神奇的 ExemplarsQL 语言或其他。这个 API 期望在使用 PromQL 查询的任何地方包括你的 dashboard，告警或者规则查询上。该实现将解析对应的查询，并对所有使用的 series 如果存在的话，将返回这些 series 的所有相关 exemplars。

这个API 很快就被 Grafana 采用了，即使现在，在AGPLv3版本，你也可以使用 Grafana 来交付 exemplars 和快速跳转到 trace 视图中。

当然，这只是最基本的。Prometheus 在2021年初完成了完成的基础涉及和逻辑的建设以便支持 scraping， 存储,，查询甚至于在 remote write 中去复制这些数据。[Thanos][Thanos](http://thanos.io/) 已经开始支持 exemplars，Grafana 也是。

值得一提的是,OpenTelemtry 也从 Open Census 那里继承了一些 exemplars。这些与 Open Metrics one 非常相似，只是仅仅附加到了 histogrm buckets 中。然而，我们目前还不知道有谁在使用或者依赖于 Otel metrics 协议中的这一部分，以及相关实现。 像[GO](https://github.com/open-telemetry/opentelemetry-go/issues/559)。这意味着，如果你想拥有稳定的相关性，一个已经运行的生态系统，Open Metrics 可能是前近的方向。另外，[Open Telemetry 也慢慢采用了 [Open Metrics](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/metrics/semantic_conventions/openmetrics-guidelines.md)。

## 用户案例

### 基于黑白盒的监控类别

监控可以分为2大类:

* 白盒监控
* 黑盒监控

一般而言，黑盒监控是指从外部去观测系统，而操作人员对系统的内部工作没有控制或了解。另外一方，白盒监控是指去监控应用或系统更加“传统”的概念， 你可以控制并了解其是如何运作的，这样你就可以通过“可观测性”的三大支柱去更好的决定如何去观测它。

### 实现SLIsSLOs和SLAs

实现 SLI，SLO 和 SLA metrics 可以让你客观的衡量服务质量和客户满意度。更重要的是，它提供了统一组织内不同功能 (业务、产品和工程)的一套通用术语。在任何组织中，工程时间都是一种稀缺资源，但每个人都觉得他们的问题是一个迫在眉睫的问题。SLO 使得此类对话更加以数据为导向，因为每个人都了解违反 SLO 之后的业务后果。在解决内部冲突的同时，他还通过提供有意义的抽象来实现有意义且可操作的警告，从而使你更加关注客户。

在我们深入研究实现细节之前，我们应当清楚的了解这些定义，因为他们可能相当令人困惑，有时候还可以互换使用。

* 服务水平指标(SLI)：SLI 是一种服务水平指标——对所提供的服务水平的某些方面进行严格定义的定量衡量。
* 服务水平目标(SLO)：SLO是一个服务水平目标：关于你所能承受失败的频率的目标。由 SLI 衡量的服务级别的目标值或值的范围。
* 服务水平协议(SLA):包含违反 SLO 后果的商业协议。这是一个目标为百分百的指标。
  错误预算：在 SLO 确定的一段时间内，所能容忍的失败事件的比率。 结果依赖于 1 - SLO%。

为了使提倡的 SLO 有用和有效，你需要让所有相关人员都同意。产品经理必须同意这个阈值对客户来说已经足够好了。低于这个值的性能低的让人无法接受，值得花费工程时间来修复。产品开发人员需要同意，如果错误预算已经耗尽，他们将才去一些措施来降低用户的风险，知道服务回到预算以内。负责维护此 SLO 的生产环境团队一致认为，不需要付出巨大努力、过度劳累和筋疲力尽，这些都会长期损害团队和服务的健康。

![sli:o:a](https://user-images.githubusercontent.com/8470415/124545037-ede13080-de45-11eb-860f-d314625aebed.png)

### 可观测性数据告警

在官方采用 metrics 收集之前，大多数软件系统仅仅依靠 logs 去分类和解决问题，并获得对其系统的可见性。除了 logs 搜索和大盘展示，logs 还充当许多团队和工具的主要警告来源。这种方法现在仍然存在于许多现代可观测性系统中，但通常应避免使用，以支持对时序 metrics 发出警报。更具体的说，我们将研究使用你定义的 SLO 和 错误预算来执行具备可操作性的告警。

在你的时序数据中有许多可以作为告警来源的信号，其中许多可能是指定应用的。推荐的最佳做法是 使用你团队的 SLO 来驱动你的警告。如上所述，SLO 是服务水平目标，由服务水平指标衡量的服务水平目标值或者值得范围。例如，REST API 的 SLO 可能要求“95%的请求必须在 500毫秒内完成。”为了给你的团队提供有效的告警，你还应该定义错误预算。我们将看看如何结合 SLO 和 错误预算来驱动可操作的 警告。

#### __实践中的告警__

构建告警是非常复杂的，很容易被误报淹没并导致告警疲劳。警告应该是具备可操作性的，并指示某人需要才去行动的问题。下面我们将介绍两种可以实现的方式，一种是简单的方法，另一种是基于消耗率的方法.

##### __目标错误率__

对目标错误率发出对应的告警是你可以采用的最简单的方法。选择一个小的时间窗口，例如10分钟，如果该窗口的错误率超过了你的 SLO，则发出告警。

例如，如果 SLO 为99.9%，则在过去的十分钟的错误率大于等于 0.1%的时候发出告警。在 Prometheus 中，这看起来像这样(总的 HTTP 请求错误数除以过去10分钟内所有请求的总和):

```
(sum(rate(http_requests_total{code=~"5.*"}[10m])) / sum(rate(http_requests_total[10m]))) > 0.001
```

这样做的好处就是可以简单直观的查看告警逻辑中发生的情况，并且在遇到错误时快速发送警报。但是，有许多并没有违反你定义的 SLO 的事件上触发该告警。

##### __消耗率__

对损耗率发出告警是一种更加复杂的方法，可能会产生更多可以操作的告警。首先，让我们先更详细的定义什么是 消耗率和错误预算。

所有 SLO 定义中都有一个错误预算的概念。通过声明 99.9% 的 SLO， 你表示的是 0.1% 的故障率(即你的错误预算)对于预定义的时间 (SLO窗口) 是可以接受的。消耗率是相对于 SLO，服务消耗错误预算的速度。所以，例如，如果由一个 “服务使用的消耗率为1，则意味着它消耗错误预算的速度使你在 SLO 的时间窗口结束的时候，预算恰好为0。在30天的时间窗口内，SLO 为99.9%。 0.1% 的恒定错误率恰好使用了所有的错误预算：消耗率为1。”[8]

![image](https://user-images.githubusercontent.com/24193764/121790715-74448280-cbb8-11eb-9b66-ea432377449f.png)
(Errors relative to burn rate[8]相对于消耗率的误差)

| Burn rate | Error rate for a 99.9% SLO | time to exhaustion |
|-----------|----------------------------|--------------------|
| 1         | 0.1%                       | 30 days            |
| 2         | 0.2%                       | 15 days            |
| 10        | 1%                         | 3 days             |
| 1000      | 100%                       | 43 minutes         |
(消耗率和完成预算消耗的时间[8])

消耗率将允许我们减小窗口的大小并创建具有良好检测时间和高精度的告警。对于我们的示例，假设将告警窗口固定在1小时，并决定以 5% 的错误预算支出，足以通知一些人，你就可以得出用于告警的消耗率。

基于消耗速率的告警, 发出告警所需的时间为:

```
(1 - SLO / 错误率) * 告警窗口大小 * 消耗率
```

而告警时间消耗的错误预算为:

```
(消耗率 * 告警窗口大小) / 时间周期
```

所以，如果30天内的错误预算花费超过1小时，那么5%的消耗率就需要达到36。 告警规则变为：

```
(sum(rate(http_requests_total{code=~"5.*"}[1h])) / sum(rate(http_requests_total[1h]))) > 36 * .001
```

## 可观测性的差距

### 多个信号之间的关联性

希望上面的 paper 可以很好的解释如何考虑可观测性的关联性，它的含义以及现在可以实现的目标。然而，让我们快速列举当前多信号下可观测性关联的陷阱：

* 不一致的元数据

正如前面所提到的，即便是 labels 之间的些许不同，在使用过程也可能很麻烦。 重新标记或默认使用 pull 模式会有所帮助。

* 缺少 request ID 或当前 ID 与 logs 中的 Tracing ID 不同。

正如之前所言, 这些可以在仪器(采集端)方面来解决，这有时很难控制。中间件和 service meshes 也可以提供帮助。

* 棘手的 trace 采样案例

去收集所有请求的全部 traces 和 spans 可能非常昂贵。这就是为什么项目定义了不同的 采样规则，只允许“采样”(去收集)那些以后可能有用的 traces。很难说哪些是重要的，所以出现了复杂的采样规则。主要的问题是确保 log 系统中的 示例或直接的 trace ID 等相关的点指向采样的 traces。如果我们的前端系统暴露了一个死胡同 (存储中没有可用的 trace)的 exemplar 链接，那将会是一个糟糕的用户体验。

虽然可以在 UI 方面去改进这种体验(例如在展示 exemplar之前检查 trace 是否存在)，但这并非微不足道，而且给系统会带来更深一层的复杂性。在理想情况下，我们可以在将 exemplar 注入到 metrics 系统之前去检查是否对 trace 进行了采样。如果使用了预先采样的方法，OpenTelemetry 代码 API 允许通过例如 “IsSampled” 来获取采样的信息。如果我们讨论 “tail-based” 的采样方式或可能分析哪个trace有趣或不有趣的进一步过程的时候，问题就出现了。我们还没有看到一些更好的想法来改善这个小而烦人的问题。如果你采用全采样或预先抽烟采样(请求或用户选择的比例)，这个问题将会消失。

* Exemplars 是这个生态系统中的新事物

Prometheus 的用户体验特别好，因为在应用程序中展示 Prometheus/OpenMetrics 是标准。世界各地的软件都使用这种简单的机制来添加大量有用的 metrics。因为 Prometheus exemplars 是新的，OpenTelemetry tracing 也是新的，所以人们开始使用 exemplars去“监测他们的仪器”需要时间。

但是，你可以从自己的案例开始，将 Prometheus exemplars 支持添加到你的应用中。这种关联模式正在称为一种新的标准 (例如在 Thanos 中进行检测)，所以你和你的用户可以将它们一起叠加，从而轻松的将 tracing 和 metrics 联系起来。

* 更高级别的 metrics 聚合，向下采样。

尚未添加的功能是 增加用于记录规则和告警的 exemplars 的能力，这些可能附加 exemplars 的情况下聚合更多的 metrics。这个提议已经被提出来了，但是工作尚未完成。同样，我们为 Prometheus 的进一步迭代讨论的 向下采样技术必须考虑 向下采样 exemplars。

* 在 UI 中的本地关联支持。

Grafana 是多信号连接方面的先驱，但是考虑本文中风险的方式，其他许多 UI 将使用更好的关联支持。在 Grafana 之前，空间是相当分散的(每个信号都有自己的视图，很少考虑其他的信号)。 Prometheus UI 也不例外。 对于连接到其他信号或呈现 exemplars 的额外支持也将被[添加](https://github.com/prometheus/prometheus/issues/8797) 。

## 引用

<!-- TODO: please add extra references here -->
1. HARTMANN, Richard. Talk given at Fosdem (Brussels), Feb 2019. Available at: https://archive.fosdem.org/2019/schedule/event/on_observability_2019/. Accessed on: June 24, 2021.
1. SRIDHARAN, Cindy. _Distributed Systems Observability_. **Chapter 04, The Three Pillars of Observability**. 2018. Available at: https://www.oreilly.com/library/view/distributed-systems-observability/9781492033431/ch04.html. Accessed on: June 24, 2021.
1. BEYER, Betsy; JONES, Chris; MURPHY, Niall; PETOFF, Jennifer. _Site Reliability Engineering_. O'Reilly Media, 2016. Available at: https://sre.google/sre-book/table-of-contents/. Accessed on: June 24, 2021.
1. BEYER, Betsy; MURPHY, Niall; RENSIN, David; KAWAHARA, Kent; THORNE, Stephen. _The Site Reliability Workbook_. O'Reilly Media, 2018. Available at: https://sre.google/workbook/table-of-contents/. Accessed on: June 24, 2021.
1. SRIDHARAN, Cindy. _Monitoring and Observability_. Sep 5, 2017. Available at: https://copyconstruct.medium.com/monitoring-and-observability-8417d1952e1c. Accessed on: June 24, 2011.
1. MCCARTHY, Kate; FONG-JONES, Liz; FISHER, Danyel; MAHON, Deirdre; PERKINS, Rachel. _Observability Maturity: Community Research Findings Q1, 2020_. April, 2020. Available at: https://www.honeycomb.io/wp-content/uploads/2020/04/observability-maturity-report-4-3-2020-1-1.pdf. Accessed on: June 24, 2021.
1. Kalman R. E., _On the General Theory of Control Systems_, Proc. 1st Int. Cong. of IFAC, Moscow 1960 1481, Butterworth, London 1961. Available at: https://www.sciencedirect.com/science/article/pii/S1474667017700948?via%3Dihub. Accessed on: June 24, 2021.


## 贡献者列表

从第一个单词直到完成，这个白皮书是社区共同的努力。从我们双周会议期见的同步讨论，关于 [#tag-observability slack-channel](https://cloud-native.slack.com/archives/CTHCQKK7U) 的一步讨论或对我们草案的意见和建议，我们有更多预期的贡献者。以下是在这几个月中为我们提供帮助的贡献者（按字母顺序）。

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
[Krisztian Fekete]:       @
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



## 可贡献内容

这份白皮书仍然不是完整的！如果你想帮助我们，我们仍然想包括以下几个主题：

* *提高你的可观测性——“投资回报”* - 实现细粒度的可观测性可能非常的昂贵，尤其是如果做的很天真。通常， 我们建议从简单开始，并使用更多的信号、更多粒度和数据大小进行迭代。让我们在新的章节中讨论这些建议。我们还列举了我们应如何迭代以及必须满足哪些标准才能进行可观测性扩展。
* 用户案例
  * *数据可视化和探索*  - 构建仪表盘非常容易，但是构建“好的” 仪表盘是另外一回事。我们先告诉您构建仪表盘的最佳时间，并解释如何依据我们想要实现的目标不同而选择不同的构建方式。例如，分析例是数据，实时监控。
* 围绕可观测性的空白
  * *机器学习、异常检测和分析*。 - 关于机器学习/分析 在可观测性领域是否有用，存在一些非常强烈和反对的意见，我们需要有经验的人向社区解释他在哪里以及为什么有用，在哪里以及为什么不能用。
  * *监控流 APIs*  - 目前有两种非常知名的监控方法。USE方法监控计算资源，RED 方法监控基于请求的服务。这两种方法都不适用于流式 APIs，随着远程过程调用 (RPC) 的普及，我们需要提出一种明确的方法去监控他们。
  * *eBPF*  - eBPF 是一项革命性的技术，可以在 Linux 内核中运行沙箱程序，而无需更改内核源码或者加载内核模块。通过一些创新，他可以帮助我们实现长期以来的梦想，即在不增加额外的仪器情况下去观测系统。尽管这种可能性无穷无尽，但是 eBPF 并不是那么受欢迎。我们想告诉读者 eBPF 和 相关工具是如何改变可观测性领域的游戏规则，以及为什么他们仍然不是那么受欢迎。
  * *观测短暂存活的系统*。-  Faas/Serveless 空间的可观测性仍然很弱，我们想告诉我们的读者为什么观测这种系统是如此的困难。基于 pull 和 push 模型如何与他们进行交互，以及为什么性能开销一直是一个问题。

