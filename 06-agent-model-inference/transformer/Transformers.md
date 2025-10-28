# Transformers

Transformers 是一个用于推理和训练的预训练自然语言处理库。开发者可以使用 Transformers 在自己的数据上训练模型、构建推理应用，并通过大型语言模型生成文本。

## 环境配置

- `transformers>=4.51.0`
- 推荐使用 `torch>=2.6`
- 推荐使用 GPU

## 基本用法

你可以使用 `pipeline()` 接口或 `generate()` 接口在 transformers 中通过 Qwen3 生成文本。

通常，pipeline 接口需要的样板代码更少，如下所示。以下展示了一个使用 pipeline 进行多轮对话的基本示例：

```
from transformers import pipeline

model_name_or_path = "Qwen/Qwen3-8B"

generator = pipeline(
    "text-generation", 
    model_name_or_path, 
    torch_dtype="auto", 
    device_map="auto",
)

messages = [
    {"role": "user", "content": "Give me a short introduction to large language models."},
]
messages = generator(messages, max_new_tokens=32768)[0]["generated_text"]
# print(messages[-1]["content"])

messages.append({"role": "user", "content": "In a single sentence."})
messages = generator(messages, max_new_tokens=32768)[0]["generated_text"]
# print(messages[-1]["content"])
```

创建 pipeline 时有一些重要的参数：

- **模型**：`model_name_or_path` 可以是像 `Qwen/Qwen3-8B` 这样的模型 ID，也可以是本地路径。

  要将模型文件下载到本地目录，可以使用

  ```
  huggingface-cli download --local-dir ./Qwen3-8B Qwen/Qwen3-8B
  ```

  如果你在中国大陆，还可以使用 ModelScope 下载模型文件

  ```
  modelscope download --local_dir ./Qwen3-8B Qwen/Qwen3-8B
  ```

- **设备分配**：如果可用，`device_map="auto"` 将自动将模型参数加载到多个设备上。它依赖于 `accelerate` 包。如果你想使用单个设备，可以传递 `device` 而不是 `device_map`。`device=-1` 或 `device="cpu"` 表示使用 CPU，`device="cuda"` 表示使用当前 GPU，`device="cuda:1"` 或 `device=1` 表示使用第二个 GPU。不要同时使用 `device_map` 和 `device`！

- **计算精度**：`torch_dtype="auto"` 将根据检查点的原始精度和设备支持的精度自动确定要使用的数据类型。对于现代设备，确定的精度将是 `bfloat16`。

  如果你不传递 `torch_dtype="auto"`，默认数据类型为 `float32`，这将占用两倍的内存并且计算速度较慢。

调用文本生成 pipeline 时，将使用模型文件中的生成配置，例如 `generation_config.json`。这些配置可以通过直接向调用传递参数来覆盖。默认配置等效于

```
messages = generator(messages, do_sample=True, temperature=0.6, top_k=2, top_p=0.95, eos_token_id=[151645, 151643])[0]{"generated_text"}
```

有关配置生成参数的最佳实践，请参阅模型卡片。

## 思考与非思考模式

默认情况下，Qwen3 模型会在回复前进行思考，`pipeline()` 接口也是如此。要切换思考与非思考模式，可以使用以下两种方法：

- 追加一条仅包含 `<think>\n\n</think>\n\n` 的最终助手 (assistant) 消息。此方法是无状态的，意味着它仅对当前轮对话生效，并且会严格阻止模型生成思考内容。例如：

  ```
  messages = [
      {"role": "user", "content": "Give me a short introduction to large language models."},
      {"role": "assistant", "content": "<think>\n\n</think>\n\n"},
  ]
  messages = generator(messages, max_new_tokens=32768)[0]["generated_text"]
  # print(messages[-1]["content"])
  
  messages.append({"role": "user", "content": "In a single sentence."})
  messages = generator(messages, max_new_tokens=32768)[0]["generated_text"]
  # print(messages[-1]["content"])
  ```

- 在用户 (user) 或系统 (system) 消息中添加 `/no_think` 以禁用思考、添加 `/think` 以启用思考。此方法是有状态的，意味着在多轮对话中，模型将遵循最近的指令。你还可以使用自然语言指令。

  ```
  messages = [
      {"role": "user", "content": "Give me a short introduction to large language models./no_think"},
  ]
  messages = generator(messages, max_new_tokens=32768)[0]["generated_text"]
  # print(messages[-1]["content"])
  
  messages.append({"role": "user", "content": "In a single sentence./think"})
  messages = generator(messages, max_new_tokens=32768)[0]["generated_text"]
  # print(messages[-1]["content"])
  ```

## 解析思考内容

如果你希望获得更结构化的助手消息格式，可以使用以下函数将思考内容提取到名为 `reasoning_content` 的字段中，该字段的格式类似于 vLLM、SGLang 等使用的格式。

```
import copy
import re

def parse_thinking_content(messages):
    messages = copy.deepcopy(messages)
    for message in messages:
        if message["role"] == "assistant" and (m := re.match(r"<think>\n(.+)</think>\n\n", message["content"], flags=re.DOTALL)):
            message["content"] = message["content"][len(m.group(0)):]
            if thinking_content := m.group(1).strip():
                message["reasoning_content"] = thinking_content
    return messages
```

## 解析工具调用

有关使用 Transformers 进行工具调用的信息，请参阅[函数调用指南](https://qwen.readthedocs.io/zh-cn/latest/framework/function_call.html#hugging-face-transformers)。

## 使用量化模型

Qwen3 提供了两种类型的预量化模型：FP8 和 AWQ。使用这些模型的命令与原始模型相同，只是名称有所更改：

```
from transformers import pipeline

model_name_or_path = "Qwen/Qwen3-8B-FP8" # FP8 models
# model_name_or_path = "Qwen/Qwen3-8B-AWQ" # AWQ models

generator = pipeline(
    "text-generation", 
    model_name_or_path, 
    torch_dtype="auto", 
    device_map="auto",
)
```

备注

FP8 计算在计算能力 > 8.9 的 NVIDIA GPU 上受支持，即 Ada Lovelace、Hopper 及更新的 GPU。

为了获得更好的性能，请确保安装了 `triton` 和与环境中 `torch` 的 CUDA 版本兼容的 CUDA 编译器。

重要

在 4.51.0 版本中，在**跨 GPU**的情况下运行 FP8 存在一些与 Transformers 相关的问题。可以使用以下方法来解决这些问题：

- 在运行脚本之前设置环境变量 `CUDA_LAUNCH_BLOCKING=1`；或者
- 取消注释你本地安装的 `transformers` 中的[这一行](https://github.com/huggingface/transformers/blob/0720e206c6ba28887e4d60ef60a6a089f6c1cc76/src/transformers/integrations/finegrained_fp8.py#L340)。

## 启用长上下文

Qwen3 模型在预训练中的最大上下文长度为 32,768 个 token。通过 RoPE 缩放技术，它可以扩展到 131,072 个 token。我们已使用 YaRN 验证了性能。

Transformers 支持 YaRN，可以通过修改模型文件或在加载模型时覆盖默认参数来启用。

- 修改模型文件：在 `config.json` 文件中，添加 rope_scaling 字段：

  ```
  {
      ...,
      "max_position_embeddings": 131072,
      "rope_scaling": {
          "rope_type": "yarn",
          "factor": 4.0,
          "original_max_position_embeddings": 32768
      }
  }
  ```

- 覆盖默认参数：

  ```
  from transformers import pipeline
  
  model_name_or_path = "Qwen/Qwen3-8B"
  
  generator = pipeline(
      "text-generation", 
      model_name_or_path, 
      torch_dtype="auto", 
      device_map="auto",
      model_kwargs={
          "max_position_embeddings": 131072,
          "rope_scaling": {
              "rope_type": "yarn",
              "factor": 4.0,
              "original_max_position_embeddings": 32768,
          },
      }
  )
  ```

注意

在 Transformers 4.52.3 版本中，无论指定的 `rope_scaling.factor` 是多少，它都会使用 `max_position_embeddings/rope_scaling.original_max_position_embeddings` 作为 `rope_scaling.factor`。更多信息请参阅[此问题](https://github.com/huggingface/transformers/issues/38224)。

备注

Transformers 实现了静态 YaRN，这意味着无论输入长度如何，缩放因子保持不变，**这可能会对较短文本的性能产生影响。** 我们建议仅在需要处理长上下文时添加 `rope_scaling` 配置。还建议根据需要修改 `factor`。例如，如果你的应用程序的典型上下文长度为 65,536 个 token，则最好将 `factor` 设置为 2.0。

## 流式输出

借助 `TextStreamer` ，你可以将与 Qwen3 的对话切换到流式传输模式。下面是一个关于如何使用它的示例：

```
from transformers import pipeline, TextStreamer

model_name_or_path = "Qwen/Qwen3-8B"

generator = pipeline(
    "text-generation", 
    model_name_or_path, 
    torch_dtype="auto", 
    device_map="auto",
)

streamer = TextStreamer(pipe.tokenizer, skip_prompt=True, skip_special_tokens=True)

messages= generator(messages, max_new_tokens=32768, streamer=streamer)[0]["generated_text"]
```

除了使用 `TextStreamer` 之外，我们还可以使用 `TextIteratorStreamer` ，它将可打印的文本存储在一个队列中，以便下游应用程序作为迭代器来使用：

```
from transformers import pipeline, TextIteratorStreamer

model_name_or_path = "Qwen/Qwen3-8B"

generator = pipeline(
    "text-generation", 
    model_name_or_path, 
    torch_dtype="auto", 
    device_map="auto",
)

streamer = TextIteratorStreamer(pipe.tokenizer, skip_prompt=True, skip_special_tokens=True)

# Use Thread to run generation in background
# Otherwise, the process is blocked until generation is complete
# and no streaming effect can be observed.
from threading import Thread
generation_kwargs = dict(text_inputs=messages, max_new_tokens=32768, streamer=streamer)
thread = Thread(target=pipe, kwargs=generation_kwargs)
thread.start()

generated_text = ""
for new_text in streamer:
    generated_text += new_text
    print(generated_text)
```

## 批处理

备注

批处理不总能提速。

```
from transformers import pipeline

model_name_or_path = "Qwen/Qwen3-8B"

generator = pipeline(
    "text-generation", 
    model_name_or_path, 
    torch_dtype="auto", 
    device_map="auto",
)
generator.tokenizer.padding_side="left"

batch = [
    [{"role": "user", "content": "Give me a short introduction to large language models."}],
    [{"role": "user", "content": "Give me a detailed introduction to large language models."}],
]

results = generator(batch, max_new_tokens=32768, batch_size=2)
batch = [result[0]["generated_text"] for result in results]
```

## 常见问题解答

你可能会发现使用 Transformers 进行分布式推理的速度不如预期。Transformers 使用 `device_map="auto"` 时并未应用张量并行 (Tensor Parallelism)，且一次仅使用一个 GPU。如需支持张量并行的 Transformers，请参阅[其文档](https://huggingface.co/docs/transformers/v4.51.3/en/perf_infer_gpu_multi)。