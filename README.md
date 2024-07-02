# RenManager

> **RenManager** 是一个基于 Python 的开源 *Ren'Py环境* 管理工具

## :cd: 安装与使用

1. 请确保你已经安装了 Python 3.12 版本（推荐使用虚拟环境）
2. 将项目克隆到本地或下载压缩包
3. 进入项目目录使用 `pip` 命令安装项目依赖
   ```
   pip install -r requirements.txt
   ```
4. 在终端中启动 RenManager
   ```
   python renm.py
   ```

## :bulb: 命令

### 环境管理

1. 创建一个新的 Ren'Py 环境
   ```
   Usage: create -n NAME [-h] [-v VERSION] [-p]

    required arguments:
    -n, --name NAME       新环境的名称

    optional arguments:
    -h, --help            show this help message and exit
    -v, --version VERSION
                            版本
    -p, --pre_release     指定版本为预发布版本
    ```

2. 删除一个 Ren'Py 环境
   ```
   Usage: remove -n NAME [-h]

    required arguments:
    -n, --name NAME  环境的名称

    optional arguments:
    -h, --help       show this help message and exit
   ```

3. 重命名一个 Ren'Py 环境
   ```
   Usage: rename -o OLD_NAME -n NEW_NAME [-h]

    required arguments:
    -o, --old_name OLD_NAME
                            旧环境的名称
    -n, --new_name NEW_NAME
                            新环境的名称

    optional arguments:
    -h, --help            show this help message and exit
    ```

4. 查看信息
   ```
   Usage: info [-h] (-e | -v)

    optional arguments:
    -h, --help      show this help message and exit
    -e, --env_dict  查看所有环境
    -v, --version   查看软件当前版本
   ```

5. 激活环境
   ```
   Usage: activate -n NAME [-h]

    required arguments:
    -n, --name NAME  环境的名称

    optional arguments:
    -h, --help       show this help message and exit
    ```

6. 退出环境
   ```
   deactivate
   ```

7. 重置 RenManager
   ```
   reset
   ```

### 环境操作

1. 调用 Ren'Py
   ```
   Usage: renpy [-h] (-l | -vsc | -c COMMAND)

   optional arguments:
   -h, --help            show this help message and exit
   -l, --launcher        打开启动器
   -vsc, --vscode        使用 vscode 打开 Ren'Py 源码目录
   -c, --command COMMAND
                           使用 Ren'Py 命令 需要使用引号包裹
    ```

2. 检查环境文件改动
   ```
   check
   ```

3. 忽略当前改动
    ```
    ignore
    ```


4. 打开环境内置文档
    ```
    doc
    ```

---

:heart: 感谢[@llfseik](https://github.com/llfseik)帮忙制作的程序图标

:star: 如果你喜欢这个项目，请给它一个 :star: 吧

:bug: 如果你发现了任何问题，请提交 [issues](https://github.com/ZYKsslm/RenManager/issues)