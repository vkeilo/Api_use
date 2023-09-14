# 项目说明文档

## 项目概述

该项目旨在**动态审查网页文本文件内容更新**，能够为新添加的内容进行威胁程度打分，以供后续安全分析

项目包含多功能工具集，分别用于实现**目录监测、目录备份、文本差异获取和威胁评估**等多个功能。项目通过结合这些不同的 Python 脚本和工具，提供一种用于监测文件目录中文件内容的变化、备份目录、比较文本差异并进行自然语言处理的综合解决方案。

## 项目文件

以下是项目中包含的主要文件和模块：

### 1. `agent_use.py`

- `agent_use.py` 包含了一个名为 `gpt_agent` 的 Python 类，用于与 用户定义的大模型（现支持chatglm2-6b/OpenAI GPT-3）进行交互。交互接口采用openai规范，该类提供了以下功能：

    - 根据 JSON 对话内容进行角色扮演初始化
    - 角色回滚（删除对话记录）
    - 新增历史消息
    - 获取回答
    - 与用户进行实时交互（用以模型行为纠正）

### 2. `dir_back.py`

- `dir_back.py` 为项目提供了是用于备份目录的接口。它允许用户创建目录的副本，以供后续内容对比或其他用途。功能包括：

    - 复制源文件夹到备份文件夹

### 3. `fwatch.py`

- `fwatch.py` 为项目提供了监测目录中文件变化的接口。它使用了 `fswatch` 命令来实时监测指定目录下的特定文件变化事件，并根据事件类型进行相应的处理。功能包括：

    - 免监测白名单制定（现含swp/swpx缓存文件类型）
    - 目录变化事件检测（现包括文件内容更新）
    - 待审查文件目录列表的更新

### 4. `get_diff.py`

- `get_diff.py` 为项目提供了比较两个文本文件之间差异的接口。借助 Python 标准库中的 `difflib` 模块来生成文本差异的比较结果。功能包括：

    - 比较两个文件差异信息，提取更改或新增的行的内容

### 5. `examiner.json`

- `examiner.json` 为包含了对话记录的 JSON 文件，其中的对话内容包含了对审查员角色的任务描述，用于提供给 api_use.py 进行角色的指定，在当前的指定下，该角色将提供的输入作为网页目录中新增加的内容，并对内容的威胁程度进行1-100的评分。

### 6. `dir_examiner.py`

- `dir_examiner.py` 是项目的核心脚本，整合调用了以上所有的功能接口，并执行监测目录、备份目录、文本差异获取和自然语言处理等任务。它的核心功能包括：

    - 备份目录
    - 监测目录中文件的变化
    - 比较新内容与备份内容的差异
    - 使用用户指定的接口连接大模型，进行评估威胁程度
    - 与用户的实时交互（实现模型行为纠正）

## 使用方法

以下是项目具体运行方法：

### 环境准备
- 开发使用系统为 `ubuntu 22.04LTS` ，python版本为3.9.5,请根据`requirements.txt`中内容在安装好需要的依赖库（推荐使用miniconda虚拟环境）
    ```sh
    pip install -r requirements.txt
    ```
- 确保系统中安装了fswatch工具:
    ```sh
    sudo apt-get install fswatch
    ```
- 进入`ChatGLM2-6B/THUDM/chatglm2-6b-int4`目录，补充下载大模型权重文件（需要至少8GB设备显存），该模型为[chatglm2-6b](https://github.com/THUDM/ChatGLM2-6B)的4bit量化版本
    ```
    wget https://cloud.tsinghua.edu.cn/seafhttp/files/f31dd790-1f21-4940-a9b6-12df04930532/pytorch_model.bin
    ```
    
    或者
    ```
    wget http://47.110.127.221/tmp/pytorch_model.bin
    ```
- 进入`ChatGLM2-6B`目录，运行大模型API接口
    ```sh
    python openai_api.py
    ```

### 运行
- 文件路径指定：
    - 更改 `dir_examiner.py` 中的 `target_dir` 和 `backup_dir` 参数，分别对应待监视目录和备份目录的绝对路径（备份目录会自主创建，但不要设置在监视目录路径下） 
- 主程序启动(确保使用的是正确的python环境)
    -   ```sh
        python dir_examiner.py
        ```