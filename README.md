# 对于凡人修仙传的graphrag抽取和实践

- 李鲁鲁fork了这个项目，并且尝试将数据替换为凡人修仙传
- 原始的动机，是希望结合GraphRAG，每次询问一个修仙概念，然后建立修仙概念和现实世界自然科学的联系
- 逐步编写《修仙世界的自然原理》杂记
- 李鲁鲁把项目调整到可以在colab运行

## QuickStart



## 目录



# 在colab上建立graphrag的index

实际上可以直接访问这个链接并且运行

## 在colab上配置环境

```bash
!git clone https://github.com/LC1332/graphrag-practice-chinese
%cd ./graphrag-practice-chinese
# 安装项目运行所需的依赖
!pip install -q -r ./requirements.txt
# 创建 input 目录，用于构建索引的文本文件默认存放于该目录下，可以按需修改 settings.yaml 文件中的 input 部分来指定路径
!mkdir ./input

# 这一命令将在 graphrag-practice-chinese 目录中创建两个文件：.env 和 settings.yaml
!python -m graphrag.index --init --root ./
```

这个和原项目是一致的，只不过colab要用！作为行首来进行运行。

## 将GLM的key导入到.env文件

```python
from google.colab import userdata
glm_api_key = userdata.get('GLM_API_KEY')

# 将 GLM_API_KEY={glm_api_key}写入到.env
with open(".env", "w") as f:
  f.write(f"GLM_API_KEY={glm_api_key}")
```

这里需要你的colab中配置了GLM_API_Key，在左侧点击小钥匙就可以配置。

## 用settings.demo.yaml覆盖settings.yaml

```python
import shutil
import os

# 覆盖 settings.yaml
if os.path.exists("./settings.demo.yaml"):
  shutil.copyfile("./settings.demo.yaml", "./settings.yaml")
  print("settings.yaml has been overwritten by settings.demo.yaml")
else:
  print("settings.demo.yaml not found, settings.yaml remains unchanged.")
```

这里因为我GLM充了不少钱，所以模型我选用了GLM-4-Air，如果你没有充钱，或者钱比较少，可以去用免费的GLM-4-Flash。

另外我发现GLM-4-Air是可以使用json mode的，这里我把yaml里面的设置改为true了。

## 将输入文件复制到input

```python
import zipfile
import os

# 定义压缩文件路径和解压目标路径
zip_file_path = "lulu_exp/fanren_700.zip"
extract_path = "input"

# 创建解压目标目录，如果不存在
os.makedirs(extract_path, exist_ok=True)

# 打开压缩文件
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    # 提取所有文件到目标目录
    zip_ref.extractall(extract_path)
```

这里我选取到截止2025年3月接近动画片的外海剧情的小说前700章。

你可以在这里把input里面的文件替换为你自己想抽取GraphRAG的文件。

直觉来说，对小说进行合理的分章可以提升效果。

**初步做实验建议用fanren_20**来进行实验

这里我后面为了保险起见实际上是增量式逐步抽取的（我怕抽到一半给我error）

## 进行抽取

```bash
!python -m graphrag.index --root ./
```

我700章在colab上运行了大约一个小时

## 将抽取结果保存到zip文件


```python
import zipfile
import os

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file), 
                       os.path.relpath(os.path.join(root, file), 
                                       os.path.join(path, '..')))

def create_zip():
    zipf = zipfile.ZipFile('all_fanren_output_700.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir('cache', zipf)
    zipdir('output', zipf)
    zipf.close()

create_zip()
```

这个zip我直接放在项目里面了，这样clone项目之后，是可以直接query信息的

## 尝试query信息

```bash
!python -m graphrag.query --root ./ --method global "灵气是什么？"
```

回答

```
SUCCESS: Global Search Response: 灵气是一种在修仙世界中至关重要的神秘能量。它被认为是构成宇宙的基本元素之一，修炼者可以通过吸收和利用这种能量来提升自己的修为和法力。以下是对灵气概念的详细解释：

### 灵气的本质与作用
灵气不仅是修炼者提升实力的关键，也是施展各种法术和法宝的基础 [Data: Reports (220, 247, 127, 268, 143, 237, 88, 85, 76, 290, 5, 132, 33, 214, 258, 183, 63, 139)]。在修仙文化中，灵气是一种无形的、充满宇宙间的生命能量，被认为是万物生长和存在的基础 [Data: Reports (182)]。

### 灵根与修炼
拥有特殊体质，即灵根，是成为修仙者的先决条件 [Data: Reports (140)]。修炼者通过特定的修炼方法可以吸收和利用灵气，这对于他们的修炼进度和实力提升至关重要 [Data: Reports (141, 169, 306, 67, 78)]。

### 灵气的来源与分布
灵气的存在和分布与特定的地理环境、修炼场所和修炼者的修为等级有关。某些山脉、洞穴或修炼地被认为是灵气充沛的地方，有利于修仙者的修炼 [Data: Reports (128, 153, 191, 222, 283, +more)]。

### 灵气在故事中的表现
在修仙或奇幻故事中，灵气是修炼者提升自身能力的关键资源。它与修炼、法术和超自然能力的发展密切相关。修炼者通过吸收和运用灵气来增强自己的身体和心灵，以及施展各种法术 [Data: Reports (122, 225, 120, 97, 301)]。在某些故事中，灵气可能具有不同的形态和属性，例如，分为不同的等级或类型，每种都有其独特的用途和效果 [Data: Reports (122, 225, 120, 97, 301)]。

### 灵气的文化意义
灵气的概念在不同的故事和文化中可能有不同的解释和表现形式。在东方哲学和修炼文化中，它是一种无形的、充满宇宙间的生命能量，修炼者通过吸收和运用灵气来增强自身的修为和力量 [Data: Reports (182)]。

综上所述，灵气是修仙世界中不可或缺的元素，它不仅是修炼者提升实力的关键，也是修仙文化中的一个核心概念。
```


---

下面是原项目


# graphrag-practice-chinese

`graphrag-practice-chinese`是一个 GraphRAG 的应用实例，项目特点在于提供了替换 OpenAI 模型的方法，并通过修改原有提示和切分文档的方法，提高了 GraphRAG 处理中文内容的能力。

# 搭建环境(非常关键！)

```bash
git clone https://github.com/zhaoyingjun/graphrag-practice-chinese.git

cd ./graphrag-practice-chinese

# 安装项目运行所需的依赖
pip install -r ./requirements.txt

# 创建 input 目录，用于构建索引的文本文件默认存放于该目录下，可以按需修改 settings.yaml 文件中的 input 部分来指定路径
mkdir ./input

# 这一命令将在 graphrag-practice-chinese 目录中创建两个文件：.env 和 settings.yaml
python -m graphrag.index --init --root ./
```

# 修改配置文件

GraphRAG 主要的配置文件有两个：`.env` 和 `settings.yaml`：

- `.env` 包含运行 GraphRAG pipeline 所需的环境变量。该文件默认只定义了一个环境变量 `GRAPHRAG_API_KEY=<API_KEY>` 。

- `settings.yaml` 包含 pipeline 相关的设置。

**在项目根目录你可以找到作为参考的配置文件 [demo.env](./demo.env) 和 [settings.demo.yaml](./settings.demo.yaml)。**

你可以参考配置进行修改，也可以通过重命名覆盖初始化的配置文件。对于更多 settings.yaml 的配置选项，你可以参考官方文档：[Default Configuration Mode (using JSON/YAML)](https://microsoft.github.io/graphrag/config/json_yaml/)和[Fully Custom Config](https://microsoft.github.io/graphrag/config/custom/)

```
这里推荐使用大语言模型 glm-4-flash（首个免费调用的模型），因为在推理和总结阶段需要消耗大量的 Tokens。
我尝试对完整的《红楼梦》原文构建索引，最终消耗了大约 700W 个 Tokens，个人学习用的话尽力而为吧。
```

# 优化策略 — 使模型侧重中文

## 优化 1: 替换文档切分策略

官方分块把文档按照 token 数进行切分，对于中文来说容易在 chunk 之间出现乱码，这里参考 `Langchain-ChatChat` 开源项目，用中文字符数对文本进行切分。

复制文件 [splitter/tokens.py](./splitter/tokens.py) 替换掉 python 依赖库中的 `graphrag/index/verbs/text/chunk/strategies/tokens.py` 即可。

## 优化 2: 使用中文提示词(chinese-prompt)

初始化后，在 `prompts` 目录中可以看到 GraphRAG 的四个 prompt 文件的内容都由英文书写，并要求 LLM 使用英文输出。

为了更好地处理中文内容，这里我使用 `gpt-4o` 模型，将 [prompts/](./prompts/) 中的四个 prompt 文件都翻译成中文，并要求 LLM 用中文输出结果。

**如果你有更好的想法，想要自定义提示词，同样可以通过修改这四个 prompt 文件来实现，但注意不要修改提示词的文件名，以及不要修改和遗漏了在原提示词中有关输出的关键字段和格式，以免 GraphRAG 无法正常获取它们。**

## 优化 3: 模型调用

GraphRAG 默认使用 openai 进行模型调用，该模型为国外模型，对中文支持并不友好。为更好地支持中文，这里选择 `bigmodel` 进行模型调用，该模型为国内大模型厂商智谱 AI 提供。

## 优化 4: 模型选择

GraphRAG 默认使用 gpt-4o 模型，该模型为国外模型，对中文支持并不友好。为更好地支持中文，这里选择 `glm-4-plus` 模型，该模型为国内大模型厂商智谱 AI 提供。

# 构建索引

1. 通过运行如下命令， Graphrag 会在指定的文件路径下加载配置文件`.env`和`setting.yaml`，并按照你的配置开始构建索引。

```bash
python -m graphrag.index --root ./graphrag-practice-chinese
```

- 假设你当前的文件路径已经在`graphrag-practice-chinese`下的话，命令指定的构建路径应该为当前目录，则构建索引的命令应该是：

```bash
python -m graphrag.index --root ./
```

**你需要确保指定的文件路径下存在配置文件`.env`和`setting.yaml`，且配置了正确的`api_key`。**

**自定义样本数据**

GraphRAG 会默认为 `input` 路径下的 `txt` 文件构建索引，**如果需要指定文件的路径或类型，可以修改`settings.yaml`中的`input`部分**。

```
注意！GraphRAG 仅支持 `txt 或 csv` 类型的文件，编码格式必须为 `utf-8`。
```

在本项目中，我将红楼梦原文文本作为样本，所以在配置文件`setting.yaml`中将文件路径`base_dir`修改为`input/hongloumeng`，如下:

```yaml
# ... 其他设置保持不变 ...
input:
  type: file # or blob
  file_type: text # or csv
  base_dir: "input/hongloumeng"
  file_encoding: utf-8
  file_pattern: ".*\\.txt$"
# ... 其他设置保持不变 ...
```

**如果你也想要把红楼梦原文文本作为样本，可以通过我的另一个项目 [hongloumeng-txt](https://github.com/Airmomo/hongloumeng-txt) 获取到符合 GraphRAG 格式要求的文件，获取完成后将文件放在`input/hongloumeng`目录下即可。**

2. 在构建过程中会自动创建两个目录：

- `output` 目录，用于存放查询结果。
- `cache` 目录，用于存放缓存数据。

3. 索引构建完成后会提示：`All workflows completed successfully` ，说明即可构建完成，随时可以进行查询。（如果没有 GPU 加持的话，构建的过程还是比较久的，可以在控制台你看到每一个步骤的进度条。）

# 查询测试

## global 全局查询

```bash
python -m graphrag.query --root ./graphrag-practice-chinese --method global "故事的主旨是什么？"
```

查询结果示例：

```markdown
SUCCESS: Global Search Response:
《红楼梦》的主旨在于通过对贾、王、史、薛四大家族的兴衰描写，展现了封建社会的各种矛盾和冲突，揭示了封建社会的腐朽和衰落。故事中的人物关系错综复杂，反映了当时社会的风俗习惯和道德观念。小说通过对宝玉、黛玉、宝钗等主要人物的爱情悲剧，探讨了人性、命运、社会关系等主题，反映了作者对封建礼教和封建制度的批判。

此外，小说还探讨了人生、命运、爱情、婚姻等主题，反映了作者对人生和社会的深刻思考。通过对贾宝玉、林黛玉、薛宝钗等主要人物的塑造，展现了封建社会中人性的复杂性和悲剧性，反映了人性的光辉与阴暗面。故事中的人物命运和家族兴衰反映了当时社会的现实，同时也表达了作者对美好人性的追求和对理想社会的向往。

综上所述，《红楼梦》的主旨不仅揭示了封建社会的腐朽和衰落，还探讨了人性、命运、社会关系等主题，具有深刻的思想内涵和艺术价值。
```

## local 本地查询

```bash
python -m graphrag.query --root ./graphrag-practice-chinese --method local "贾母对宝玉的态度怎么样？"
```

查询结果示例：

```markdown
SUCCESS: Local Search Response:
贾母对宝玉的态度可以从多个方面进行总结：

1. 溺爱与关心：贾母对宝玉有着深厚的溺爱。在《红楼梦》中，贾母多次探望宝玉，甚至亲自到园中看望他，表现出对宝玉的关心和爱护。例如，在贾母探视宝玉的情况中，贾母和王夫人一同探望宝玉，并询问他的病情，显示出贾母对宝玉的关心（Data: Entities (4704, 2929, 3895, 5470, 5868)）。

2. 宠爱与宽容：贾母对宝玉的宠爱还体现在对宝玉行为的宽容上。宝玉性格顽劣，有时甚至有些荒唐，但贾母却总是以宽容的态度对待他。例如，贾母对宝玉的干妈“老东西”的指责，显示出贾母对宝玉的宠爱（Data: Relationships (528, 2124)）。

3. 期望与教育：尽管贾母对宝玉宠爱有加，但她也关心宝玉的教育。在贾母房中，贾母关注宝玉的教育，并关心他的成长（Data: Entities (2702, 5524, 5868)）。

4. 情感交流：贾母与宝玉之间有着深厚的情感交流。在贾母与宝玉的互动中，贾母不仅关心宝玉的身体健康，还关心他的心理状态，体现出两人之间深厚的感情（Data: Sources (607, 314, 481)）。

综上所述，贾母对宝玉的态度是溺爱、关心、宠爱、宽容，同时也有期望和教育。这种复杂的情感关系，体现了贾母对宝玉的深厚感情。
```

## Tip：全局查询和本地查询的区别

| 特征         | 本地查询 (Local Search)    | 全局查询 (Global Search)         |
| ------------ | -------------------------- | -------------------------------- |
| 查询范围     | 以特定实体为入口点         | 基于预先计算的实体社区摘要       |
| **查询方法** | **使用实体嵌入和图遍历**   | **向每个社区提问并汇总答案**     |
| **适用场景** | **针对特定实体的精确查询** | **广泛的主题性问题**             |
| 性能         | 对简单直接任务更高效       | 适合处理复杂的多步骤查询         |
| 复杂度       | 相对较低                   | 较高，需要更多计算资源           |
| 响应速度     | 通常更快                   | 可能较慢，取决于查询复杂度       |
| 洞察深度     | 适中                       | 更深入，能更全面理解上下文和关系 |
| Token 使用量 | 较低                       | 较高，due to 多次 LLM 调用       |
| 实现依赖     | 向量搜索和图遍历           | 预计算的社区摘要和多次 LLM 调用  |
| 最佳使用场景 | 需要快速直接答案的情况     | 需要深入洞察和复杂推理的场景     |
