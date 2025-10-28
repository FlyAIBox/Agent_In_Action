# 一文读懂「Lang Chain」langchain

Author: banana · 分类： [人工智能技术](https://www.baihezi.com/category/ai/ai-tech) ·   2024年10月 · tags: [ai](https://www.baihezi.com/tag/ai) [langchain](https://www.baihezi.com/tag/langchain) [人工智能](https://www.baihezi.com/tag/人工智能)

## 一、什么是LangChain？

------

LangChain是一个强大的框架，旨在帮助开发人员使用语言模型构建端到端的应用程序。它提供了一套工具、组件和接口，可简化创建由大型语言模型 (LLM) 和聊天模型提供支持的应用程序的过程。LangChain 可以轻松管理与语言模型的交互，将多个组件链接在一起，并集成额外的资源，例如 API 和[数据库](https://www.baihezi.com/tag/数据库)。
官方文档：[https://python.langchain.com/en/latest/](https://www.baihezi.com/goto?url=https%3A%2F%2Fpython.langchain.com%2Fen%2Flatest%2F)
中文文档：[https://www.langchain.com.cn/](https://www.baihezi.com/goto?url=https%3A%2F%2Fwww.langchain.com.cn%2F)

> LangChain本身并不开发LLMs，它的核心理念是**为各种LLMs提供通用的接口，降低开发者的学习成本，方便开发者快速地开发复杂的LLMs应用**。

官方的定义：LangChain是一个基于语言模型开发应用程序的框架。它可以实现以下应用程序：

数据感知：将语言模型连接到其他数据源自主性：允许语言模型与其环境进行交互
主要价值在于：

组件化：为使用语言模型提供抽象层，以及每个抽象层的一组实现。组件是模块化且易于使用的，无论你是否使用LangChain框架的其余部分。现成的链：结构化的组件集合，用于完成特定的高级任务
现成的链使得入门变得容易。对于更复杂的应用程序和微妙的用例，组件化使得定制现有链或构建新链变得更容易。

要使用 LangChain，开发人员首先要导入必要的组件和工具，例如 LLMs, chat models, agents, chains, 内存功能。这些组件组合起来创建一个可以理解、处理和响应用户输入的应用程序。

LangChain 为特定用例提供了多种组件，例如个人助理、文档问答、聊天机器人、查询表格数据、与 API 交互、提取、评估和汇总。

## 二、模型分类和特点

------

LangChain model 是一种抽象，表示框架中使用的不同类型的模型。

## LangChain 中的模型分类

：

LLM（大型语言模型）：这些模型将文本字符串作为输入并返回文本字符串作为输出。它们是许多语言模型应用程序的支柱。聊天模型( Chat Model)：聊天模型由语言模型支持，但具有更结构化的 API。他们将聊天消息列表作为输入并返回聊天消息。这使得管理对话历史记录和维护上下文变得容易。文本嵌入模型(Text Embedding Models)：这些模型将文本作为输入并返回表示文本嵌入的浮点列表。这些嵌入可用于文档检索、聚类和相似性比较等任务。

## LangChain 的特点

：

LLM 和提示：LangChain 使管理提示、优化它们以及为所有 LLM 创建通用界面变得容易。此外，它还包括一些用于处理 LLM 的便捷实用程序。链(Chain)：这些是对 LLM 或其他实用程序的调用序列。LangChain 为链提供标准接口，与各种工具集成，为流行应用提供端到端的链。数据增强生成：LangChain 使链能够与外部数据源交互以收集生成步骤的数据。例如，它可以帮助总结长文本或使用特定数据源回答问题。Agents：Agents 让 LLM 做出有关行动的决定，采取这些行动，检查结果，并继续前进直到工作完成。LangChain 提供了代理的标准接口，多种代理可供选择，以及端到端的代理示例。内存：LangChain 有一个标准的内存接口，有助于维护链或代理调用之间的状态。它还提供了一系列内存实现和使用内存的链或代理的示例。评估：很难用传统指标评估生成模型。这就是为什么 LangChain 提供提示和链来帮助开发者自己使用 LLM 评估他们的模型。

## 三、主要包含组件

------

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/Fly0905/note-picture@main/imag/202508022142083.png)

Model I/O：管理大语言模型（Models），及其输入（Prompts）和格式化输出（Output Parsers）

Data connection：管理主要用于建设私域知识（库）的向量数据存储（Vector Stores）、内容数据获取（Document Loaders）和转化（Transformers），以及向量数据查询（Retrievers）

Memory：用于存储和获取 对话历史记录 的功能模块

Chains：用于串联 Memory ↔️ Model I/O ↔️ Data Connection，以实现 串行化 的连续对话、推测流程

Agents：基于 Chains 进一步串联工具（Tools），从而将大语言模型的能力和本地、云服务能力结合

Callbacks：提供了一个回调系统，可连接到 LLM 申请的各个阶段，便于进行日志记录、追踪等数据导流

### 3.1 Model I/O

模型接入 LLM 的交互组件，用于和不同类型模型完成业务交互，LangChain 将模型分为 LLMS、Chat Model两种模型方式，分别通过不同template操作完成三种模型的业务交互。
![在这里插入图片描述](https://cdn.jsdelivr.net/gh/Fly0905/note-picture@main/imag/202508022142053.png)

#### 1. Prompt（Format）

提示（Prompt）指的是模型的输入，这个输入一般很少是硬编码的，而是从使用特定的模板组件构建而成的，这个模板组件就是 PromptTemplate 提示模板，可以提供提示模板作为输入，模板指的是我们希望获得答案的具体格式和蓝图。LangChain 提供了预先设计好的提示模板，可以用于生成不同类型任务的提示。当预设的模板无法满足要求时，也可以使用自定义的提示模板。

在 LangChain 中，我们可以根据需要设置提示模板，并将其与主链相连接以进行输出预测。此外，LangChain 还提供了输出解析器的功能，用于进一步精炼结果。输出解析器的作用是指导模型输出的格式化方式，以及将输出解析为所需的格式。
LangChain 提供了几个类和函数，使构建和处理提示变得容易：

PromptTemplate 提示模板：可以生成文本模版，通过变量参数的形式拼接成完整的语句；FewShotPromptTemplate 选择器：将提示的示例内容同样拼接到语句中，让模型去理解语义含义进而给出结果。ChatPromptTemplate 聊天提示模版：以聊天消息作为输入生成完整提示模版。

#### 2. Predict

##### 方式 1：LLMS

指具备语言理解和生成能力的商用大型语言模型，以文本字符串作为输入，并返回文本字符串作为输出。LangChain 中设计 LLM 类用于与大语言模型进行接口交互，该类旨在为 LLM 提供商提供标准接口，如 OpenAI、Cohere、Hugging Face。

##### 方式2：Chat Model

聊天模型是语言模型的一个变体，聊天模型以语言模型为基础，其内部使用语言模型，不再以文本字符串为输入和输出，而是将聊天信息列表为输入和输出，他们提供更加结构化的 API。通过聊天模型可以传递一个或多个消息。

LangChain 目前支持四类消息类型：分别是 AIMessage、HumanMessage、SystemMessage 和 ChatMessage 。

AIMessage：就是 AI 输出的消息，可以是针对问题的回答

HumanMessage：人类消息就是用户信息，由人给出的信息，如提问；使用 Chat Model 模型就得把系统消息和人类消息放在一个列表里，然后作为 Chat Model 模型的输入

SystemMessage：系统消息是用来设定模型的一种工具，可以用于指定模型具体所处的环境和背景，如角色扮演等；

ChatMessage：Chat 消息可以接受任意角色的参数

大多数情况下，只需要处理 HumanMessage、AIMessage 和 SystemMessage 消息类型。此外聊天模型支持多个消息作为输入。

#### 3. Parser：StructuredOutputParser 输出解析器

对模型生成的结果进行解析和处理的组件。它的主要功能是将模型生成的文本进行解析，提取有用的信息并进行后续处理。如对模型生成的文本进行解析、提取有用信息、识别实体、分类和过滤结果，以及对生成文本进行后处理，从而使生成结果更易于理解和使用。它在与大型语言模型交互时起到解析和处理结果的作用，增强了模型的应用和可用性。

语言模型输出文本。但是很多时候，可能想要获得比文本更结构化的信息。这就是输出解析器的作用。即输出解析器是帮助结构化语言模型响应的类，LangChain 中主要提供的类是 PydanticOutputParser。

### 3.2 Data connection

打通外部数据的管道，包含文档加载，文档转换，文本嵌入，向量存储几个环节，此模块包含用于处理文档的实用工具函数、不同类型的索引，以及可以在链中使用这些索引
![在这里插入图片描述](https://img-blog.csdnimg.cn/direct/4bd2d9995cc2452abae3d7ddb361d4d0.png)
LangChain 可以将外部数据和 LLM 进行结合来理解和生成自然语言，其中外部数据可以是本地文档、[数据库](https://www.baihezi.com/tag/数据库)等资源，将这些数据进行分片向量化存储于向量存储[数据库](https://www.baihezi.com/tag/数据库)中，再通过用户的 Prompt 检索向量数据库中的相似信息传递给大语言模型进行生成和执行 Action。

## Document loaders 文档加载器

重点包括了 txt（TextLoader）、csv（CSVLoader），html（UnstructuredHTMLLoader），json（JSONLoader），markdown（UnstructuredMarkdownLoader）以及 pdf（因为 pdf 的格式比较复杂，提供了 PyPDFLoader、MathpixPDFLoader、UnstructuredPDFLoader，PyMuPDF 等多种形式的加载引擎）几种常用格式的内容解析。

## Document transformers 文档转换器

LangChain 有许多内置的文档转换器，可以轻松地拆分、组合、过滤和以其他方式操作文档，重点关注按照字符递归拆分的方式 RecursiveCharacterTextSplitter 。

## Text embedding models 文本嵌入模型

LangChain 中的 Embeddings 基类公开了两种方法：一种用于嵌入文档，另一种用于嵌入查询。前者采用多个文本作为输入，而后者采用单个文本。将它们作为两种单独方法的原因是，某些嵌入提供程序对文档（要搜索的）与查询（搜索查询本身）有不同的嵌入方法。

文本嵌入模型是将文本进行向量表示，从而可以在向量空间中对文本进行诸如语义搜索之类的操作，即在向量空间中寻找最相似的文本片段。而这些在 LangChain 中是通过 Embedding 类来实现的。（ Embedding 类是一个用于与文本嵌入进行交互的类。这个类旨在为提供商（有许多嵌入提供商，如 OpenAI、Cohere、Hugging Face 等）提供一个标准接口）

## VectorStores 向量存储

存储和搜索非结构化数据的最常见方法之一是嵌入它并存储生成的嵌入向量，然后在查询时嵌入非结构化查询并检索与嵌入查询“最相似”的嵌入向量。
![在这里插入图片描述](https://img-blog.csdnimg.cn/direct/2ff2abccfb98460dad34fc2dcb518a5c.png)

矢量存储负责存储嵌入数据并执行矢量搜索。处理向量存储的关键部分是创建要放入其中的向量，这通常是通过 embedding 来创建的。这个就是对常用矢量数据库（Chroma、FAISS，Milvus，Pinecone，PGVector 等）封装接口的说明，大概流程：初始化数据库连接信息——>建立索引——>存储矢量——>相似性查询。

## Retrievers 查询

检索器是一个接口，它根据非结构化查询返回文档。它比矢量存储更通用。检索器不需要能够存储文档，只需返回（或检索）它。矢量存储可以用作检索器的骨干，但也有其他类型的检索器。

检索器接口是一种通用接口，使文档和语言模型易于组合。LangChain 中公开了一个 get_relevant_documents 方法，该方法接受查询（字符串）并返回文档列表。

重点关注数据压缩，目的是获得相关性最高的文本带入 prompt 上下文，这样既可以减少 token 消耗，也可以保证 LLM 的输出质量。

## Caching Embeddings 缓存嵌入

嵌入可以被存储或临时缓存以避免需要重新计算它们。缓存嵌入可以使用CacheBackedEmbeddings。

### 3.3 Memory

Memory 是在用户与语言模型的交互过程中始终保持状态的概念。体现在用户与语言模型的交互聊天消息过程，这就涉及为从一系列聊天消息中摄取、捕获、转换和提取知识。Memory 在 Chains/Agents 调用之间维持状态，默认情况下，Chains 和 Agents 是无状态的，这意味着它们独立地处理每个传入的查询，但在某些应用程序中，如：聊天机器人，记住以前的交互非常重要，无论是在短期的还是长期的。“Memory”这个概念就是为了实现这一点。
![在这里插入图片描述](https://img-blog.csdnimg.cn/direct/c07271beee964e2e9d60f041564db0ba.png)
LangChain 提供了两种方式使用记忆存储 Memory 组件，一种是提供了管理和操作以前的聊天消息的辅助工具来从消息序列中提取信息；另一种是在 Chains 中进行关联使用。Memory 可以返回多条信息，如最近的 N 条消息或所有以前消息的摘要等。返回的信息可以是字符串，也可以是消息列表。

LangChain 提供了从聊天记录、缓冲记忆、Chains 中提取记忆信息的方法类以及接口，如 ChatMessageHistory 类，一个超轻量级的包装器，提供了一些方便的方法来保存人类消息、AI 消息，然后从中获取它们；再如 ConversationBufferMemory 类，它是 ChatMessageHistory 的一个包装器，用于提取变量中的消息等等。

### 3.4 Chains

通常我们使用单独的 LLM 也可以解决问题，但是对于更加复杂的应用程序需要在 LLM 之间或与其他系统进行链接来完成任务，这个通常称为链接 LLM。

链允许将模型或系统间的多个组件组合起来，创建一个单一的、一致的应用程序。举例来说，我们创建一个链，该链接受用户的输入，通过 PromptTemplate 模板对输入进行格式化并传递到 LLM 语言模型。还可以将多个链组合起来，或者将链与其他系统组件组合起来，来构建更复杂的链，实现更强大的功能。LangChain 为链提供了标准接口以及常见实现，与其他工具进行了大量集成，并为常见应用程序提供了端到端链。

### 3.5 Agents

通常用户的一个问题可能需要应用程序的多个逻辑处理才能完成相关任务，而且往往可能是动态的，会随着用户的输入不同而需要不同的 Action，或者 LLM 输出的不同而执行不同的 Action。因此应用程序不仅需要预先确定 LLM 以及其他工具调用链，而且可能还需要根据用户输入的不同而产生不同的链条。使用代理可以让 LLM 访问工具变的更加直接和高效，工具提供了无限的可能性，LLM 可以搜索网络、进行数学计算、运行代码等等相关功能。

LangChain 中代理使用 LLM 来确定采取哪些行动及顺序，查看观察结果，并重复直到完成任务。LangChain 库提供了大量预置的工具，也允许修改现有工具 或创建新工具。当代理被正确使用时，它们可以非常强大。在 LangChain 中，通过“代理人”的概念在这些类型链条中访问一系列的工具完成任务。根据用户的输入，代理人可以决定是否调用其中任何一个工具。

### 3.6 Callbacks

LangChain 提供了一个回调系统，允许你连接到 LLM 申请的各个阶段。这对于日志记录、监控、流传输和其他任务非常有用。

可以使用整个 API 中可用的参数来订阅这些事件。该参数是处理程序对象的列表，这些对象预计将实现下面更详细描述的一个或多个方法。

## 四、使用langChain构建应用

------

![在这里插入图片描述](https://img-blog.csdnimg.cn/direct/457845818fae48c080c1d34dd9e151be.png)

特定文档的问答：从Notion数据库中提取信息并回答用户的问题。聊天机器人：使用Chat-LangChain模块创建一个与用户交流的机器人。代理：使用GPT和WolframAlpha结合，创建一个能够执行数学计算和其他任务的代理。文本摘要：使用外部数据源来生成特定文档的摘要。

## 五、典型应用

------

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/Fly0905/note-picture@main/imag/202508022142074.png)
LangChain 作为一款先进的语言模型应用开发框架，它赋能开发者基于底层语言模型打造出各种智能语言应用。常见用例如下：

自治的代理：LangChain支持自治代理的开发，如AutoGPT和BabyAGI，它们是长时间运行的代理，执行多个步骤以实现目标。

代理模拟：LangChain促进了创建沙盒环境，其中代理可以相互交互或对事件做出反应，提供对其长期记忆能力的洞察。

个人助理：LangChain非常适合构建个人助理，它可以执行操作、记住交互并访问你的数据，提供个性化的帮助。

问答：LangChain在回答特定文档中的问题方面表现出色，利用这些文档中的信息构建准确和相关的答案。

聊天机器人：利用语言模型的文本生成能力，LangChain赋予了创造引人入胜的聊天机器人的能力。

查询表格数据：LangChain提供了使用语言模型查询存储在表格格式中的数据（如CSV文件、SQL数据库或数据框）的指南。

代码理解：LangChain协助使用语言模型查询和理解来自GitHub等平台的源代码。

与API交互：LangChain使语言模型能够与API交互，为它们提供最新信息，并能够根据实时数据采取行动。

提取：LangChain帮助从非结构化文本中提取结构化信息，简化数据分析和解释。

摘要：LangChain支持将较长的文档摘要成简洁、易于消化的信息块，使其成为数据增强的强大工具。

评估：由于生成模型难以使用传统指标进行评估，LangChain提供提示和链来辅助使用语言模型本身进行评估过程。

## 六、总结

------

LangChain赋予了开发人员将LLM与其他计算和知识来源相结合以构建应用程序的能力。使用LangChain，开发人员可以使用一个抽象LLM应用程序的核心构建块的框架。探索LangChain的能力并尝试其各个组件，会发现可能性几乎无限。LangChain框架提供了一种灵活和模块化的语言生成方法，允许创建根据用户特定需要量身定制的定制解决方案。

## 七、拓展学习

------

13分钟解读LangChain：[https://www.bilibili.com/video/BV14o4y1K7y3/?spm_id_from=333.337.search-card.all.click&vd_source=f27f081fc77389ca006fcebf41bede2dhttps://space.bilibili.com/267440912/channel/collectiondetail?sid=1428550](https://www.baihezi.com/goto?url=https%3A%2F%2Fwww.bilibili.com%2Fvideo%2FBV14o4y1K7y3%2F%3Fspm_id_from%3D333.337.search-card.all.click%26amp%3Bamp%3Bvd_source%3Df27f081fc77389ca006fcebf41bede2dhttps%3A%2F%2Fspace.bilibili.com%2F267440912%2Fchannel%2Fcollectiondetail%3Fsid%3D1428550)

一图带你了解 LangChain 的内部结构！

[https://www.bilibili.com/video/BV1214y1X7Aq/?spm_id_from=333.337.search-card.all.click&vd_source=f27f081fc77389ca006fcebf41bede2dhttps://space.bilibili.com/28357052/channel/collectiondetail?sid=1611560](https://www.baihezi.com/goto?url=https%3A%2F%2Fwww.bilibili.com%2Fvideo%2FBV1214y1X7Aq%2F%3Fspm_id_from%3D333.337.search-card.all.click%26amp%3Bamp%3Bvd_source%3Df27f081fc77389ca006fcebf41bede2dhttps%3A%2F%2Fspace.bilibili.com%2F28357052%2Fchannel%2Fcollectiondetail%3Fsid%3D1611560)

## 参考
[构建高效 Agent [译]](https://baoyu.io/translations/building-effective-agents)