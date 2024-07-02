from cmd2 import Cmd2ArgumentParser


class Parser:

    # 当环境为 "manager" 时使用的参数

    @staticmethod
    def create_parser():
        parser = Cmd2ArgumentParser()
        parser.add_argument("-n", "--name", type=str, required=True, help="新环境的名称")
        parser.add_argument("-v", "--version", type=str, help="版本")
        parser.add_argument("-p", "--pre_release", action="store_true", help="指定版本为预发布版本")

        return parser

    @staticmethod
    def remove_parser():
        parser = Cmd2ArgumentParser()
        parser.add_argument("-n", "--name", type=str, required=True, help="环境的名称")

        return parser

    @staticmethod
    def rename_parser():
        parser = Cmd2ArgumentParser()
        parser.add_argument("-o", "--old_name", type=str, required=True, help="旧环境的名称")
        parser.add_argument("-n", "--new_name", type=str, required=True, help="新环境的名称")

        return parser

    @staticmethod
    def info_parser():
        parser = Cmd2ArgumentParser()
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument("-e", "--env_dict", action="store_true", help="查看所有环境")
        group.add_argument("-v", "--version", action="store_true", help="查看软件当前版本")

        return parser

    @staticmethod
    def activate_parser():
        parser = Cmd2ArgumentParser()
        parser.add_argument("-n", "--name", type=str, required=True, help="环境的名称")

        return parser

    # 激活环境后使用的参数

    @staticmethod
    def renpy_parser():
        parser = Cmd2ArgumentParser()
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument("-l", "--launcher", action="store_true", help="打开启动器")
        group.add_argument("-vsc", "--vscode", action="store_true", help="使用 vscode 打开 Ren'Py 源码目录")
        group.add_argument("-c", "--command", type=str, help="使用 Ren'Py 命令 需要使用引号包裹")

        return parser
