import logging
import os
import re
import json
import shutil
import patoolib
from string import digits, ascii_lowercase, ascii_uppercase, punctuation, whitespace
from itertools import product

# 设置日志格式
logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s %(asctime)s | %(message)s',
                    datefmt='%Y-%m-%d %H-%M-%S')

# 支持的扩展名
ZIP_EXTENSIONS = (".zip", ".rar", ".tar", ".7z")
TEXT_EXTENSIONS = (".txt", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".pdf")
MULTIPART_EXTENSIONS = (".001", ".part1.rar")

# 提取目录
OUTPUT_DIR = os.path.join(os.getcwd(), "extracted")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 密码配置提示
CONF_DESC = {
    "num_ok": "number",
    "lowercase_ok": "lower case letter",
    "uppercase_ok": "upper case letter",
    "special_symbol_ok": "special symbol",
    "space_ok": "space"
}

def check_files() -> tuple[dict, dict]:
    """扫描目录中的压缩包和字典文本文件"""
    zip_files = {}
    text_files = {}

    for root, _, files in os.walk(os.getcwd(), topdown=True):
        if OUTPUT_DIR in root:
            continue
        for file in files:
            filepath = os.path.join(root, file)
            filename_no_ext = file.split('.')[0]

            if file.endswith(MULTIPART_EXTENSIONS):
                pattern = re.compile(rf"^{re.escape(filename_no_ext)}(\.|_)")
                parts = [os.path.join(root, f) for f in files if pattern.match(f)]
                zip_files[filename_no_ext] = parts
                continue

            if file.endswith(ZIP_EXTENSIONS):
                zip_files[filename_no_ext] = filepath
            elif file.endswith(TEXT_EXTENSIONS):
                text_files[file] = filepath

    return zip_files, text_files

def prompt_config() -> dict:
    """与用户交互获得破解密码的设置"""
    config = {}
    for key, desc in CONF_DESC.items():
        while True:
            choice = input(f"Use {desc}? (Y/N): ").strip().lower()
            if choice in ('y', 'n'):
                config[key] = (choice == 'y')
                break
            logging.warning("Invalid input. Please enter Y or N.")
    
    while True:
        try:
            length = int(input("Input maximum brute-force password length (>0): "))
            if length > 0:
                config["code_len"] = length
                break
        except ValueError:
            pass
        logging.warning("Invalid number. Try again.")

    return config

def load_config() -> dict:
    """加载或更新配置"""
    if os.path.exists("config.json"):
        with open("config.json", "r") as f:
            config = json.load(f)
        if input("Config exists. Change it? (Y/N): ").strip().lower() == 'y':
            return prompt_config()
        return config
    return prompt_config()

class ZipExtractor:
    def __init__(self, config: dict) -> None:
        self.zip_paths = config.get("zippath", {})
        self.text_dicts = config.get("txtpath", {})
        self.code_len = config.get("code_len", 0)

        # 字符表生成
        self.charset = ''
        if config.get("num_ok"): self.charset += digits
        if config.get("lowercase_ok"): self.charset += ascii_lowercase
        if config.get("uppercase_ok"): self.charset += ascii_uppercase
        if config.get("special_symbol_ok"): self.charset += punctuation
        if config.get("space_ok"): self.charset += whitespace

    def _find_extension(self, path: str | list) -> str:
        """获取压缩文件的真实扩展名"""
        if isinstance(path, list):
            path = path[0]
        for ext in ZIP_EXTENSIONS:
            if ext in path:
                return ext
        return ""

    def _extract_archive(self, archive_path: str, target_path: str, password: str | None = None) -> bool:
        """尝试解压文件"""
        try:
            if os.path.exists(target_path):
                shutil.rmtree(target_path)
            patoolib.extract_archive(archive=archive_path, outdir=target_path, password=password, verbosity=-1)
            logging.info(f"Extract success: {os.path.basename(archive_path)} (Password: {password or 'None'})")
            return True
        except patoolib.util.PatoolError as e:
            logging.debug(e)
            return False

    def _combine_parts(self, parts: list[str], output_path: str) -> None:
        """合并分卷压缩包"""
        with open(output_path, "wb") as outfile:
            for part in parts:
                with open(part, "rb") as infile:
                    shutil.copyfileobj(infile, outfile)

    def extract_all(self):
        for name, path in self.zip_paths.items():
            extension = self._find_extension(path)
            temp_path = os.path.join(OUTPUT_DIR, f"temp_{name}{extension}")
            target_path = os.path.join(OUTPUT_DIR, name)

            if isinstance(path, list):
                self._combine_parts(path, temp_path)
            else:
                shutil.copy(path, temp_path)

            success = self._extract_archive(temp_path, target_path)
            if not success:
                success = self._try_passwords(temp_path, target_path, os.path.basename(temp_path))

            os.remove(temp_path)
            if not success:
                logging.warning(f"Failed to extract: {name}{extension}")

    def _try_passwords(self, archive_path: str, target_path: str, filename: str) -> bool:
        """尝试从字典或生成密码破解压缩包"""
        # 先尝试字典破解
        for dict_path in self.text_dicts.values():
            try:
                with open(dict_path, "r", encoding="utf-8") as f:
                    for line in f:
                        password = line.strip()
                        if self._extract_archive(archive_path, target_path, password):
                            return True
            except Exception as e:
                logging.debug(f"Error reading dictionary {dict_path}: {e}")

        # 然后尝试暴力破解
        for i in range(1, self.code_len + 1):
            for combo in product(self.charset, repeat=i):
                password = ''.join(combo)
                if self._extract_archive(archive_path, target_path, password):
                    return True
        return False

def main():
    zip_files, text_files = check_files()
    config = load_config()

    config["zippath"] = zip_files
    config["txtpath"] = text_files

    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)

    extractor = ZipExtractor(config)
    extractor.extract_all()

if __name__ == "__main__":
    main()
    os.system("pause")
