## Jupyter Lab 安装、配置和常见操作

Jupyter Lab 是一个基于 Web 的交互式开发环境，适用于 Jupyter Notebook、代码和数据。它是 Jupyter Notebook 的下一代产品，提供了更强大、更灵活的用户界面，支持更多的工作流。

## 1. 安装和配置 Jupyter Lab

上述开发环境安装完成后，使用 Miniconda 安装 Jupyter Lab：

```Bash
conda install -c conda-forge jupyterlab
```

使用 Jupyter Lab 开发的最佳实践是后台常驻，下面是相关配置（以 root 用户为例）：

```Bash
# 生成 Jupyter Lab 配置文件，
jupyter lab --generate-config
```

输出信息

```Bash
 # 生成 Jupyter Lab 配置文件，
jupyter lab --generate-config
Writing default config to: /root/.jupyter/jupyter_lab_config.py
```

打开上面执行输出的`jupyter_lab_config.py`配置文件后，修改以下配置项：

```Bash
# 允许 root 用户启动
c.ServerApp.allow_root = True

# 考虑修改服务器默认目录
#c.ServerApp.root_dir= '/Agent101/code/jike-peng-openai-quickstart'
c.ServerApp.root_dir= '/Agent101/code'

# 修改默认端口，以免被别人进入自己的notebook
# 尤其是服务器，要修改端口避免冲突
c.ServerApp.port = 8000

# 设置notebook可登陆的ip, 全0为不限制
c.ServerApp.ip = '0.0.0.0'

# 关闭登陆密码，确保本地安全才可以，否则切勿关闭
c.ServerApp.token = 'fly123'
```

## 2. 启动 Jupyter Lab

使用 nohup 后台启动 Jupyter Lab

```Bash
$ nohup jupyter lab  &
```

Jupyter Lab 输出的日志将会保存在 `nohup.out` 文件（已在 .gitignore中过滤）。

## 3. 设置 Jupyter Lab 开机自启

对于使用 systemd 作为 init 系统的 Linux 发行版（如 Ubuntu, Fedora, CentOS, Debian 等），我们可以创建一个 systemd 服务单元文件来实现 Jupyter Lab 的开机自启。

**步骤 1: 创建 Jupyter Lab 服务单元文件**

使用文本编辑器（如 `vim`, `vim`）创建名为 `jupyter.service` 的服务单元文件，并将其放置在 `/etc/systemd/system/` 目录下。 您需要使用 sudo 权限来创建和编辑该文件。

 `vim`:

```Bash
sudo vim /etc/systemd/system/jupyter.service
```

**步骤 2: 编辑服务单元文件**

在打开的 `jupyter.service` 文件中，粘贴以下内容。 **请根据您的实际情况修改以下配置：**

```bash
[Unit]
Description=JupyterLab
After=network.target
[Service]
Type=simple

# 设置环境变量
# 激活conda环境并启动jupyterlab
ExecStart=/bin/bash -c "source /root/miniconda3/bin/activate agent101 && exec jupyter-lab --config=/root/.jupyter/jupyter_lab_config.py --no-browser"
User=root
Group=root

# Jupyter Lab 启动时的工作目录
WorkingDirectory=/Agent101/code

Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**配置项** **说明 (重要):**

- **`Description=Jupyter Lab Server`**: 服务的描述信息，可以自定义。
- **`After=network.target`**: 表示该服务在网络服务启动后启动。
- **`Type=simple`**: 服务类型为简单服务。
- **`WorkingDirectory=/home/your_username`**: **工作目录**。 Jupyter Lab 启动后，默认的工作目录。您可以将其设置为您常用的 Jupyter 工作目录，例如您的 home 目录 `/home/your_username`，或者其他存放 notebook 的目录。
- `ExecStart=/home/your_username/.local/bin/jupyter lab --no-browser`:
- Jupyter Lab 启动命令
  - **`/home/your_username/.local/bin/jupyter lab`**: **请务必确认您的** **`jupyter lab`** **命令的实际路径**。 如果您不确定，可以在终端中输入 `which jupyter lab` 命令来查找 Jupyter Lab 可执行文件的路径，并替换这里。 如果您的 Jupyter Lab 是通过 pip 安装到用户本地环境，通常路径会类似 `~/.local/bin/jupyter-lab` 或 `~/.local/bin/jupyter`。 如果是系统级别安装，可能是 `/usr/bin/jupyter-lab` 或 `/usr/bin/jupyter`。
  - **`--no-browser`**: 添加此参数后，Jupyter Lab 启动时不会自动打开浏览器。 因为我们是开机自启，通常不需要自动打开浏览器，您可以在需要时手动打开浏览器并访问 Jupyter Lab 地址。
  - **`--port=8888`**: 指定 Jupyter Lab 运行的端口为 `8888`。您可以根据需要修改端口号，但请确保端口没有被其他程序占用。
- **`Restart=on-failure`**: 如果 Jupyter Lab 服务意外失败退出，systemd 会自动尝试重启该服务。
- **`RestartSec=10`**: 服务重启前等待 10 秒。
- **`[Install] WantedBy=multi-user.target`**: 表示该服务在多用户模式下启动，通常在系统启动的正常运行级别下启动。

**步骤 3: 保存并退出编辑器**

- 如果您使用 `vim` 编辑器，按下 `Ctrl + X`，然后输入 `y` 确认保存，最后按 `Enter` 键退出。
- 如果您使用 `vim` 编辑器，按下 `Esc` 键，然后输入 `:wq` 并按 `Enter` 键保存并退出。

**步骤 4: 启用并启动 Jupyter Lab 服务**

在终端中执行以下命令来启用并启动 Jupyter Lab 服务：

```Bash
sudo systemctl enable jupyter.service
sudo systemctl start jupyter.service
```

- `sudo systemctl enable jupyter.service`: 启用该服务，使其在开机时自动启动。
- `sudo systemctl start jupyter.service`: 立即启动 Jupyter Lab 服务。

**步骤 5: 检查服务状态 (可选)**

您可以检查 Jupyter Lab 服务的运行状态，确认服务是否成功启动：

```Bash
sudo systemctl status jupyter.service
```

如果服务成功启动，您应该看到类似 `active (running)` 的状态信息。

## 4.  解决- Conda命令不能使用

修改 `jupyter.service`，使其执行位于 **`/Agent101/app/jupyter/start_jupyter.sh`** 的启动脚本，从而解决 Conda 路径丢失的问题。

### 步骤 1: 创建 Conda 启动脚本（指定路径）

首先，创建名为 `start_jupyter.sh` 的脚本文件，确保路径正确。

1. 创建目录 (如果不存在)：
2. 如果` /Agent101/app/jupyter/` 目录不存在，请先创建它。

```bash
sudo mkdir -p /Agent101/app/jupyter/
```

1. **创建文件：**

```bash
sudo vim /Agent101/app/jupyter/start_jupyter.sh
```

1. 粘贴并保存以下内容：
2. 请确保 /root/miniconda3 是您 Conda 的实际安装路径。脚本内容沿用您提供的官方 Conda 初始化逻辑。

```bash
# ==========================================================
# 1. 完整的 Conda 初始化逻辑 (从您的 .bashrc 复制)
#    这确保了 conda 命令和 activate 功能可以正常使用。
# ==========================================================
__conda_setup="$('/root/miniconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/root/miniconda3/etc/profile.d/conda.sh" ]; then
        . "/root/miniconda3/etc/profile.d/conda.sh"
    else
        export PATH="/root/miniconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# ==========================================================


# 2. 激活您的目标环境
#    这一步将使 jupyter-lab 的主进程和它启动的所有终端会话
#    默认都处于 agent101 环境中。
conda activate agent101


# 3. 运行 Jupyterlab 主程序
#    使用 exec 可以确保 jupyter-lab 进程替换掉当前的 shell 进程
#    这样 systemd 就能正确跟踪主程序。
exec /usr/local/bin/jupyter-lab --config=/root/.jupyter/jupyter_lab_config.py --no-browser
```

1. **添加执行权限：**

```bash
sudo chmod +x /Agent101/app/jupyter/start_jupyter.sh
```

### 步骤 2: 修改 Systemd 服务文件

修改 `jupyter.service` 文件，将启动命令指向新的脚本路径。

1. **编辑服务文件：**

```bash
sudo vim /etc/systemd/system/jupyter.service
```

1. **修改** **`ExecStart`** **行：**
2. 在 `[Service]` 段落中，将 `ExecStart` 行替换为指向新脚本的命令。

```bash
ExecStart=/Agent101/app/jupyter/start_jupyter.sh
```

1. **注意：** 检查 `WorkingDirectory=/Agent101/code`，确保这个目录存在，因为您之前遇到的 `CHDIR` 错误也可能与此有关。

### 步骤 3: 重载和重启服务

1. **重载** **systemd** **配置：**

```bash
sudo systemctl daemon-reload
```

1. **重启** **Jupyterlab 服务：**

```bash
sudo systemctl restart jupyter.service
```

1. **检查状态（确认启动成功）：**

```bash
systemctl status jupyter.service
```

### 步骤 4: 验证结果

在 Jupyterlab 界面打开一个新的 **Terminal** 窗口，运行 `conda env list` 验证是否能找到 `conda` 命令，并且环境是否已激活。

## 5.将 Conda 环境添加到 Jupyter Lab 内核列表 (如果内核列表没有显示 conda 环境):

这个流程的核心是：**在** **Conda** **环境中安装** **`ipykernel`****，然后将其注册为 Jupyter 内核。**

#### 步骤一：创建或激活目标 Conda 环境

首先，您需要在终端中准备好您想要在 Notebook 中使用的环境。

1. **打开您的终端**。
2. **激活**您要使用的 Conda 环境。
   1. 如果环境已存在（例如 `agent101`）：
   2. conda activate agent101
   3. **（可选）** 如果您需要创建一个全新的环境：
   4. conda create -n agent101 python=3.11 -y conda activate agent101

#### 步骤二：安装 Jupyter 内核桥梁 (`ipykernel`)

Jupyter Notebook 需要一个特殊的包来与您的 Conda 环境进行通信，这个包就是 `ipykernel`。

在您**已激活**的 Conda 环境（例如 `(flyai``_agent_in_action)`）中执行以下命令：

```Bash
#使用 pip 安装：
pip install ipykernel -i https://pypi.tuna.tsinghua.edu.cn/simple
```

*提示：使用* *`conda`* *安装通常更好，因为它能更好地管理环境依赖。*

#### 步骤三：将环境注册为 Jupyter 内核

现在，您需要告诉 Jupyter 应用程序：“嗨，我这里有一个新的 Python 环境，请把它添加到你的菜单里。”

在**已激活**的环境中执行注册命令：

```Bash
python -m ipykernel install --user --name=agent101 --display-name="Python (agent101)"
```

| 参数            | 解释 (初学者友好)                                            | 建议值                 |
| --------------- | ------------------------------------------------------------ | ---------------------- |
| --user          | 允许您在自己的用户权限下安装，不需要管理员权限。             | 保持不变               |
| --name=         | 这是 Jupyter 系统内部用来识别内核的名字，通常使用 Conda 环境名。 | agent101               |
| --display-name= | 这是您在 Jupyter 菜单上看到的名字，设置为容易理解的名称。    | "Python (FlyAI Agent)" |

执行成功后，您会看到类似这样的提示：

```Bash
Installed kernelspec agent101 in /root/.local/share/jupyter/kernels/agent101
```

#### 步骤四：在 Jupyter Notebook 中切换内核

最后一步，打开您的 Notebook，开始使用新环境。

1. **启动 Jupyter Notebook 或 JupyterLab**。
   1. 如果您是从终端启动的，请先退出 Conda 环境（`conda deactivate`），然后用启动 Jupyter 的主环境来启动它：`jupyter notebook`。
2. **方法 A：创建新文件时**
   1. 在 Jupyter 的主界面，点击右上角的 **New (新建)** 按钮。
   2. 在下拉列表中，您将看到 **`Python (FlyAI Agent)`** 这个新的选项。点击它即可开始使用新环境的 Notebook。
3. **方法 B：更改现有文件的内核**
   1. 打开一个已有的 `.ipynb` 文件。
   2. 在顶部菜单栏，选择 **Kernel (内核)** → **Change kernel (更改内核)**。
   3. 选择 **`Python (FlyAI Agent)`** 完成切换。

您现在已成功设置并切换到您的 Conda 环境！您可以随意在这个 Notebook 中安装或卸载软件包，而不会影响到其他环境或您的基础环境。

#### 步骤五：在 Jupyter Notebook 中切换内核

在 Jupyter Notebook 或 JupyterLab 的代码单元格顶部，使用以下命令：

```Bash
%%script bash
eval "$(conda shell.bash hook)"
```

| 命令/结构                       | 为什么需要                                                   |
| ------------------------------- | ------------------------------------------------------------ |
| %%script bash                   | 确保整个单元格作为一个完整的 bash 脚本运行，而不是多个独立的命令。 |
| eval "$(conda shell.bash hook)" | 这是在非交互式 Shell 环境（如 Jupyter 单元格）中启用 conda activate 命令的官方且唯一的正确方法。它将 Conda 的功能加载到当前的 bash 会话中。 |

**什么是 Hook？** `conda shell.bash hook` 是一个 Conda 脚本，它会输出一系列环境变量设置和函数定义（即所谓的 "hook" 代码），这些代码允许 `conda` 命令（尤其是 `conda activate`）在当前 Shell 中正常工作。

**`eval`** **的作用：** `eval` 命令的作用是**在当前运行的 Shell 中执行**其后面的字符串（即 Conda Hook 代码）。

- 通过 `eval "$(conda shell.bash hook)"`，您实际上是在**单元格的 bash 环境中**加载了 Conda 的全部功能和路径配置。
- 一旦 Hook 加载成功，后续的 `conda activate agent101` 命令就能找到并正确修改当前 `bash` 进程的环境变量，从而实现环境切换。

##### Magic 命令格式

Jupyter/IPython 只定义了两种 Magic 命令格式：

1. **`%`** **(单百分号)：** **行 Magic 命令** (Line Magic)，只对当前一行代码生效。
2. **`%%`** **(双百分号)：** **单元格 Magic 命令** (Cell Magic)，对整个代码单元格生效，且必须位于单元格的第一行。

例如：

- **`%run script.py`**: 运行一个外部 Python 脚本。
- **`%matplotlib inline`**: 在 Notebook 中显示 Matplotlib 图表。
- **`%%html`**: 将整个单元格内容渲染为 HTML 代码。
- **`%%bash`** **/** **`%%script bash`**: 将整个单元格内容作为 Bash 脚本执行。

## 6. Jupyter Lab 常用快捷键与操作

Jupyter Lab 提供了丰富的快捷键和操作，可以大大提高你的工作效率。以下是一些常用的：

#### 6.1 通用快捷键

- **Ctrl/Cmd + Shift + C**: 打开命令面板 (Command Palette)，可以搜索和执行各种操作。
- **Ctrl/Cmd + Shift + P**: 与命令面板相同。
- **Ctrl/Cmd + S**: 保存当前文件。
- **Ctrl/Cmd + B**: 切换左侧文件浏览器面板的可见性。

#### 6.2 Notebook 快捷键 (命令模式 - 按 `Esc` 进入)

在 Notebook 中，有两种模式：编辑模式 (绿色边框) 和命令模式 (蓝色边框)。

- **A**: 在当前单元格上方插入新单元格。
- **B**: 在当前单元格下方插入新单元格。
- **X**: 剪切当前单元格。
- **C**: 复制当前单元格。
- **V**: 粘贴单元格（在当前单元格下方）。
- **D, D (按两次 D)**: 删除当前单元格。
- **Z**: 撤销删除单元格。
- **Y**: 将当前单元格类型更改为代码 (Code)。
- **M**: 将当前单元格类型更改为 Markdown。
- **R**: 将当前单元格类型更改为 Raw NBConvert。
- **Enter**: 进入编辑模式。
- **Shift + Enter**: 运行当前单元格并选中下一个。
- **Ctrl/Cmd + Enter**: 运行当前单元格。
- **Alt + Enter**: 运行当前单元格并在下方插入新单元格。
- **L**: 切换当前单元格行号的显示。
- **K**: 向上移动当前单元格。
- **J**: 向下移动当前单元格。
- **Shift + K/J**: 选中多个单元格。
- **Shift + L**: 合并选中的单元格。
- **H**: 显示所有快捷键帮助。

#### 6.3 Notebook 快捷键 (编辑模式 - 按 `Enter` 进入)

- **Tab**: 代码自动补全。
- **Shift + Tab**: 显示函数或方法的文档字符串（Docstring）。
- **Ctrl/Cmd + ]**: 增加缩进。
- **Ctrl/Cmd + [**: 减少缩进。
- **Ctrl/Cmd + Z**: 撤销。
- **Ctrl/Cmd + Y**: 重做。
- **Ctrl/Cmd + D**: 删除当前行。
- **Ctrl/Cmd + Up/Down**: 移动到单元格的开头/结尾。

#### 6.4 其他常用操作

- **文件浏览器**：
  - 拖放文件或文件夹进行上传。
  - 右键点击文件或文件夹进行复制、剪切、删除、重命名等操作。
- **终端**：在 Jupyter Lab 中打开终端，可以直接运行 shell 命令，方便进行文件操作、环境管理等。
- **代码控制台 (Console)**：可以打开一个独立的 Python 控制台，进行即时代码测试和调试。
- **Markdown 编辑器**：Jupyter Lab 内置了强大的 Markdown 编辑器，支持实时预览。
- **拖放和多标签页**：你可以将文件选项卡拖放到不同的区域，实现分屏显示，方便同时查看和编辑多个文件