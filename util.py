import hashlib
import os
import time
import zipfile

import httpx
from lxml import html
from rich.console import Console
from rich import box
from rich.table import Table
from rich.prompt import Prompt
from rich.progress import (
    SpinnerColumn,
    Progress,
    TextColumn,
    BarColumn,
    DownloadColumn,
    TransferSpeedColumn,
    TimeElapsedColumn,
    TimeRemainingColumn
)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0"
}
latest_ver_url = "https://www.renpy.org/channels.json"
release_ver_url = "http://update.renpy.org"
pre_release_ver_url = "https://nightly.renpy.org"


class Render:

    @staticmethod
    def render_latest_version(releases):
        table = Table(
            title="[italic]Ren'Py SDK[/italic] 最新发布版本",
            title_style="bold magenta",
        )
        table.add_column("编号", style="bright_white", justify="center", vertical="middle")
        table.add_column("通道", style="orange3", justify="center", vertical="middle")
        table.add_column("版本", style="cyan", justify="center", vertical="middle")
        table.add_column("描述", style="green", justify="center", vertical="middle")
        table.add_column("时间", style="yellow", justify="center", vertical="middle")

        choices = []
        for i, release in enumerate(releases):
            i = str(i + 1)
            channel = release["channel"]
            version = release["pretty_version"]
            desc = release["description"]
            t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(release["timestamp"])))
            table.add_row(i, channel, version, desc, t)
            table.add_section()

            choices.append(i)

        return table, choices

    @staticmethod
    def parse_pre_version_table(text):
        etree = html.etree.HTML(text)
        tr = etree.xpath(f'/html/body/div/table/tr')
        table = []
        for i in range(0, len(tr), 4):
            row = tr[i:i + 4]
            for j in row:
                th = j.xpath("th/text()")
                if th:
                    title = ["Time"] + [i.strip() for i in th]
                    table.append(title)
                t = j.xpath("td/text()")
                if t:
                    td = j.xpath("td")[1:]
                    ver = [t[0].strip()]
                    for t in td:
                        v = t.xpath("a/text()")
                        if v:
                            ver.append(v[0].strip().replace("+nightly", ""))
                        else:
                            ver.append("")
                    if ver:
                        table.append(ver)
        del table[1:3]
        return table

    @staticmethod
    def render_pre_release_version(text):
        version_table = Render.parse_pre_version_table(text)
        table = Table(
            box=box.ROUNDED,
            title="[bold yellow3]Ren'Py预发布版本",
            show_lines=True
        )
        for column in version_table[0]:
            table.add_column(column, style="bright_white", justify="center", vertical="middle")
        for row in version_table[1:]:
            table.add_row(*row)

        return table

    @staticmethod
    def render_file_table(title, files):
        if title == "更改文件":
            style = "yellow3"
        elif title == "缺少文件":
            style = "red"
        elif title == "新增文件":
            style = "cyan"
        else:
            style = "bright_white"

        table = Table(title=title, box=box.HEAVY_EDGE, show_lines=True)
        table.add_column("文件", style=style, justify="center")
        for f in files:
            table.add_row(f)

        return table

    @staticmethod
    def render_env(env: dict):
        table = Table(
            box=box.ROUNDED,
            title="[bold yellow3]已有环境",
            show_lines=True
        )
        table.add_column("环境名称", style="orange3", justify="center", vertical="middle")
        table.add_column("环境版本", style="magenta", justify="center", vertical="middle")
        for n, d in env.items():
            table.add_row(n, d["version"])

        return table

    @staticmethod
    def render_progress(name):
        progress = Progress(
            SpinnerColumn(),
            TextColumn(f"[bold cyan]{name}"),
            BarColumn(),
            DownloadColumn(),
            TimeRemainingColumn(),
            TimeElapsedColumn(),
            TransferSpeedColumn()
        )

        return progress


class Checker:

    def __init__(self, console: Console, name, hash_data: dict):
        self.console = console
        self.name = name
        self.hash_data = hash_data

    @staticmethod
    def gen_hash_data(file):
        with open(file, "rb") as f:
            size = len(data := f.read())
            hash_data = hashlib.sha512(data).hexdigest()

        return hash_data, size

    def check(self):
        difference = []
        new = []
        sdk_path = f"./env/{self.name}"
        with self.console.status("[yellow3]开始检测环境文件"):
            for base_path, folders, files in os.walk(sdk_path):
                for file in files:
                    path = os.path.normpath(os.path.join(base_path, file))
                    if path in self.hash_data:
                        hash_data, size = Checker.gen_hash_data(path)
                        origin_data = self.hash_data.pop(path)
                        if hash_data != origin_data:
                            difference.append(path.replace(f"env\\{self.name}\\", ""))
                    else:
                        new.append(path.replace(f"env\\{self.name}\\", ""))

            lack = [f.replace(f"env\\{self.name}\\", "") for f in self.hash_data.keys()]

        return difference, lack, new


class Installer:

    def __init__(self, console: Console, name, version, pre_release):
        self.console = console
        self.name = name
        self.version = version
        self.pre_release = pre_release

        self.env_path = f"./env/{self.name}"
        self.client = httpx.Client(headers=HEADERS, timeout=5)

        self.package_size = None
        self.hash_data = None

    def install(self):
        res = self.get_package()
        if res:
            package_name, package_size, package_url = res
        else:
            return False

        self.download(package_name, package_size, package_url)
        self.extract(package_name)
        self.hash_data = self.hash()

        return True

    def extract(self, zip_name):
        zip_path = f"{self.env_path}/{zip_name}"
        zip_file = zipfile.ZipFile(zip_path)
        file_info_list = zip_file.infolist()
        self.package_size = sum(file_info.file_size for file_info in file_info_list)

        progress = Render.render_progress(zip_name)
        extract_task = progress.add_task("解压", total=self.package_size)

        self.console.log(f"开始解压 [bold italic cyan]{zip_name}", style="yellow3")
        with progress:
            for file_info in file_info_list:
                zip_file.extract(file_info, self.env_path)
                progress.update(extract_task, advance=file_info.file_size)
        zip_file.close()
        os.remove(zip_path)

        self.console.log(f"[bold italic cyan]{zip_name}[/bold italic cyan] 解压完成", style="green")

    def req(self, url, method="get"):
        try:
            resp: httpx.Response = getattr(self.client, method)(url)
        except httpx.TransportError:
            self.console.print_exception(show_locals=True)
            return False
        else:
            return resp

    def get_package_info(self, base_url):
        name = f"renpy-{self.version}-sdk.zip"
        url = f"{base_url}/{self.version}/{name}"
        resp = self.req(url, "head")
        if not resp:
            return False
        if resp.status_code == 200:
            size = int(resp.headers["content-length"])
            return name, size, url
        else:
            return None

    def get_package(self):
        if self.version:
            if self.pre_release:
                res = self.get_package_info(pre_release_ver_url)
                if res is None:
                    resp = self.req(pre_release_ver_url)
                    if not resp:
                        return
                    table = Render.render_pre_release_version(resp.text)
                    self.console.print(table, justify="center")
                    version = Prompt.ask("未找到指定版本 请手动输入", console=self.console)
                    self.version = version + "+nightly"
                    self.console.log(f"已选择 [bold italic cyan]{version}", style="green")
                    return self.get_package_info(pre_release_ver_url)
                else:
                    return res
            else:
                return self.get_package_info(release_ver_url)
        else:
            self.console.log("未指定 [bold italic cyan]Ren'Py SDK[/bold italic cyan] 版本 开始获取最新发布版本......",
                             style="yellow3")
            resp = self.req(latest_ver_url)
            if not resp:
                return False
            else:
                releases = resp.json()["releases"]

            self.console.log("获取成功！", style="green")
            table, choices = Render.render_latest_version(releases)
            self.console.print(table, justify="center")
            n = Prompt.ask("请选择版本 ", console=self.console, choices=choices)

            release = releases[int(n) - 1]
            pretty_version = release['pretty_version']
            self.console.log(f"已选择 [bold italic cyan]{pretty_version}", style="green")
            if "nightly" in release["pretty_version"]:
                self.version = pretty_version
                return self.get_package_info(pre_release_ver_url)
            else:
                split_version = release["split_version"]
                self.version = f"{split_version[0]}.{split_version[1]}.{split_version[2]}"
                return self.get_package_info(release_ver_url)

    def download(self, package_name, package_size, package_url):
        package_path = f"{self.env_path}/{package_name}"
        if not os.path.exists(self.env_path):
            os.makedirs(self.env_path)

        progress = Render.render_progress(package_name)
        download_task = progress.add_task("下载", total=package_size)
        with self.client.stream("get", package_url) as r:
            self.console.log(f"开始下载 [bold italic cyan]{package_name}", style="yellow3")
            with progress:
                with open(package_path, "wb") as f:
                    for data in r.iter_bytes(chunk_size=1024):
                        s = f.write(data)
                        progress.update(download_task, advance=s)

        self.console.log(f"[bold italic cyan]{package_name}[/bold italic cyan] 下载完成", style="green")

    def hash(self):
        sdk_path = f"./env/{self.name}"
        progress = Render.render_progress("生成哈希值")
        hash_task = progress.add_task("生成哈希值", total=self.package_size)
        data = {}

        self.console.log("开始为文件生成哈希值", style="yellow3")
        with progress:
            for base_path, folders, files in os.walk(sdk_path):
                for file in files:
                    path = os.path.normpath(os.path.join(base_path, file))
                    hash_data, size = Checker.gen_hash_data(path)
                    data[path] = hash_data
                    progress.update(hash_task, advance=size)

        self.console.log("哈希值生成完成", style="green")
        return data
