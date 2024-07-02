# -*- coding: utf-8 -*-
#!user/bin/env_dict python3

import os
import sys
import shutil
import subprocess

import cmd2
import ujson
from rich.console import Console
from rich.prompt import Confirm

from argparser import Parser
from art import ENV_STYLE, PMT_STYLE, BOOT_TEXT, BOOT_TEXT_COLOR
from util import Installer, Render, Checker


class RenManagerApp(cmd2.Cmd):
    VERSION = "1.0"
    ENV = "manager"
    PROMPT = ">> "

    def __init__(self):
        super().__init__()
        self.set_window_title("RenManager")

        self._env = RenManagerApp.ENV
        self.prompt = ENV_STYLE + f"({RenManagerApp.ENV}) " + PMT_STYLE + RenManagerApp.PROMPT
        self.console = Console(color_system="truecolor")
        if BOOT_TEXT:
            self.console.print(BOOT_TEXT, style=BOOT_TEXT_COLOR, justify="center")

        with open("./env.json", "r") as f:
            self.env_dict: dict = ujson.load(f)

        self.sdk_path = None

    def update_env(self):
        with open("./env.json", "w") as f:
            ujson.dump(self.env_dict, f, sort_keys=True, indent=4)

    @property
    def env(self):
        return self._env

    @env.setter
    def env(self, value):
        self._env = value
        self.prompt = ENV_STYLE + f"({self._env}) " + PMT_STYLE + RenManagerApp.PROMPT
        if value == RenManagerApp.ENV:
            self.sdk_path = None
        else:
            self.sdk_path = os.path.normpath(os.path.join(os.getcwd(), "env", self.env, f"renpy-{self.env_dict[self.env]['version']}-sdk"))

    @cmd2.with_argparser(Parser.create_parser())
    def do_create(self, arg):
        env_name: str = arg.name
        sdk_version: str = arg.version
        pre_release: bool = arg.pre_release

        if pre_release and (not sdk_version):
            self.console.log("未指定版本！", style="red")
            return

        if env_name in self.env_dict.keys():
            self.console.log("该环境名与其他环境产生冲突！", style="red")
            return

        installer = Installer(self.console, env_name, sdk_version, pre_release)
        if installer.install():
            new_env = {
                env_name: {
                    "version": installer.version,
                    "hash": installer.hash_data
                }
            }
            self.env_dict.update(new_env)
            self.update_env()
            self.console.log(f"已成功创建环境 [bold italic cyan]{env_name}", style="green")

    @cmd2.with_argparser(Parser.remove_parser())
    def do_remove(self, arg):
        env = arg.name
        if env not in self.env_dict:
            self.console.log(f"未找到环境 [bold italic cyan]{env}", style="red")
            return

        res = Confirm.ask(f"确定要删除环境 [bold italic cyan]{env}[/bold italic cyan] 吗？", console=self.console)
        if res:
            shutil.rmtree(f"./env/{env}")
            del self.env_dict[env]
            self.update_env()
            self.console.log(f"已删除环境 [bold italic cyan]{env}", style="yellow3")
        else:
            self.console.log("已取消操作", style="yellow3")

    @cmd2.with_argparser(Parser.rename_parser())
    def do_rename(self, arg):
        old_name = arg.old_name
        new_name = arg.new_name

        if old_name not in self.env_dict:
            self.console.log(f"未找到环境 [bold italic cyan]{old_name} ", style="red")
            return

        res = Confirm.ask(
            f"确定要将环境 [bold italic cyan]{old_name}[/bold italic cyan] 重命名为 "
            f"[bold italic cyan]{new_name}[/bold italic cyan] 吗？",
            console=self.console
        )
        if res:
            os.rename(f"./env/{old_name}", f"./env/{new_name}")
            self.env_dict[new_name] = self.env_dict.pop(old_name)
            self.update_env()
            self.console.log(
                f"已将环境 [bold italic cyan]{old_name}[/bold italic cyan] 重命名为 "
                f"[bold italic cyan]{new_name}[/bold italic cyan]",
                style="green"
            )
        else:
            self.console.log("已取消操作", style="yellow3")

    @cmd2.with_argparser(Parser.info_parser())
    def do_info(self, arg):
        if arg.env_dict:
            if self.env:
                self.console.print(Render.render_env(self.env_dict))

        elif arg.version:
            self.console.print(f"当前版本为 [italic underline blue]{RenManagerApp.VERSION}", style="yellow3")

    @cmd2.with_argparser(Parser.activate_parser())
    def do_activate(self, arg):
        env_name = arg.name
        if env_name in self.env_dict:
            self.env = env_name
        else:
            self.console.log(f"没有名为 [orange3]{env_name}[/orange3] 的环境", style="yellow3")

    def do_deactivate(self, arg):
        self.env = RenManagerApp.ENV

    @cmd2.with_argparser(Parser.renpy_parser())
    def do_renpy(self, arg):
        if self.env == RenManagerApp.ENV:
            self.console.log("当前未激活任何环境", style="yellow3")
            return

        if arg.launcher:
            launcher_path = os.path.join(self.sdk_path, "renpy.exe")
            os.startfile(launcher_path)

        elif arg.command:
            args = arg.command.split(" ")
            if sys.platform.startswith("win"):
                renpy = os.path.join(self.sdk_path, "renpy.py")
                python_interpreter = os.path.join(self.sdk_path, "lib", "py3-windows-x86_64", "python.exe")
                rp = [python_interpreter, renpy]
            else:
                rp = [os.path.join(self.sdk_path, "renpy.sh")]

            subprocess.run(rp + args, stdout=subprocess.PIPE)

    def do_check(self, arg):
        if self.env == RenManagerApp.ENV:
            self.console.log("当前未激活任何环境", style="yellow3")
            return

        hash_data = self.env_dict[self.env]["hash"].copy()
        checker = Checker(self.console, self.env, hash_data)
        difference, lack, new = checker.check()
        if difference:
            self.console.print(Render.render_file_table("更改文件", difference))
        if lack:
            self.console.print(Render.render_file_table("缺少文件", lack))
        if new:
            self.console.print(Render.render_file_table("新增文件", new))
        if not difference and not lack and not new:
            self.console.log("当前环境文件无任何改动", style="yellow3")

    def do_doc(self, arg):
        if self.env == RenManagerApp.ENV:
            self.console.log("当前未激活任何环境", style="yellow3")
            return

        doc_path = os.path.join(self.sdk_path, "doc", "index.html")
        os.startfile(doc_path)

    def do_ignore(self, arg):
        if self.env == RenManagerApp.ENV:
            self.console.log("当前未激活任何环境", style="yellow3")
            return

        res = Confirm.ask(f"确定要忽略环境 [bold italic cyan]{self.env}[/bold italic cyan] 当前的文件更改吗？", console=self.console)
        if res:
            installer = Installer(self.console, self.env, None, None)
            hash_data = installer.hash()
            self.env_dict[self.env]["hash"] = hash_data
            self.update_env()
            self.console.log("已重置当前环境文件哈希值", style="green")
        else:
            self.console.log("已取消操作", style="yellow3")


if __name__ == '__main__':
    app = RenManagerApp()
    sys.exit(app.cmdloop())
