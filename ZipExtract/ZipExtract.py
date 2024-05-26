import logging
import os
from string import digits,ascii_lowercase,ascii_uppercase,punctuation,whitespace,printable
import re
from itertools import product
import json
import shutil
import patoolib

logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s %(asctime)s | %(message)s',
                    datefmt='%Y-%m-%d %H-%M-%S')

zipextension = (".zip",".rar",".tar",".7z")
textextension = (".txt",".doc",".docx",".xls",".xlsx",".ppt",".pptx",".pdf")
multipartextension = (".001",".part1.rar")
outdirectory = f"{os.getcwd()}\\extracted"
os.makedirs(outdirectory,exist_ok=True)

def CheckFile() -> dict:
    zipfiles = {}
    txtfiles = {}

    for root,dirs,files in os.walk(os.getcwd(),topdown=True):
        if outdirectory in root:
            continue

        for file in files:
            filepath = os.path.join(root,file)
            filesplit:list = file.split('.')
            filename = filesplit[0]
            pattern = re.compile(rf"({filename})+")

            if file.endswith(multipartextension):
                path = []
                for f in os.listdir(root):
                    if re.match(pattern,f):
                        path.append(os.path.join(root,f))
                zipfiles[filename] = path
                del path
                continue

            if file.endswith(zipextension) and not filename in zipfiles:
                filename = file.rsplit('.', 1)[0]
                zipfiles[filename] = filepath
            elif file.endswith(textextension) and not file in txtfiles:
                filename = file.rsplit('.', 1)[0]
                txtfiles[file] = filepath

    return zipfiles,txtfiles

def ChangeConf() -> dict:
    conf = {}
    while True:
        temp = input("Using number? (Y/N) \n")
        if temp in ['Y','y']:
            conf["Numok"] = True
            temp = ''
            break
        elif temp in ['N','n']:
            conf["Numok"] = False
            temp = ''
            break
        else:
            logging.warning("Input Failed! Please input again. ")
            continue
    while True:
        temp = input("Using lower case letter? (Y/N) \n")
        if temp in ['Y','y']:
            conf["LowercaseOK"] = True
            temp = ''
            break
        elif temp in ['N','n']:
            conf["LowercaseOK"] = False
            temp = ''
            break
        else:
            logging.warning("Input Failed! Please input again. ")
            continue
    while True:
        temp = input("Using upper case letter? (Y/N) \n")
        if temp in ['Y','y']:
            conf["UppercaseOK"] = True
            temp = ''
            break
        elif temp in ['N','n']:
            conf["UppercaseOK"] = False
            temp = ''
            break
        else:
            logging.warning("Input Failed! Please input again. ")
            continue
    while True:
        temp = input("Using special symbol? (Y/N) \n")
        if temp in ['Y','y']:
            conf["SpecialsymbolOK"] = True
            temp = ''
            break
        elif temp in ['N','n']:
            conf["SpecialsymbolOK"] = False
            temp = ''
            break
        else:
            logging.warning("Input Failed! Please input again. \n")
            continue
    while True:
        temp = input("Using space? (Y/N) ")
        if temp in ['Y','y']:
            conf["SpaceOK"] = True
            temp = ''
            break
        elif temp in ['N','n']:
            conf["SpaceOK"] = False
            temp = ''
            break
        else:
            logging.warning("Input Failed! Please input again. ")
            continue
    while True:
        temp = input("Input crack number. (>0) \n")
        try:
            assert isinstance(temp,int) and int(temp) > 0
            conf["Codelen"] = int(temp)
            break
        except AssertionError as e:
            logging.warning("Wrong number! Please input the correct one. \n")
            continue
    return conf

class ZipExtract:
    def __init__(self,config:dict = {}) -> None:
        self.filepath = config["zippath"] if config["zippath"] is not None else {}
        self.numOK = config["Numok"] if config["Numok"] is not None else False
        self.lowercaseOK = config["LowercaseOK"] if config["LowercaseOK"] is not None else False
        self.uppercaseOK = config["UppercaseOK"] if config["UppercaseOK"] is not None else False
        self.specialsymbolOK = config["SpecialsymbolOK"] if config["SpecialsymbolOK"] is not None else False
        self.spaceOK = config["SpaceOK"] if config["SpaceOK"] is not None else False
        self.dictext = config["txtpath"] if config["txtpath"] is not None else {}
        self.codelen = config["Codelen"] if config["Codelen"] is not None else 0
        self.pattstr = ""
    
    def FindExt(self,path:list|str = None):
        fileextension = ""
        try:
            assert isinstance(path,list)
            path = path[0]
        except AssertionError as e:
            logging.debug(e)
            pass
        for ext in zipextension:
            if ext in path:
                fileextension = ext
                break
        return fileextension

    def ExtractFiles(self):
        if self.numOK: self.pattstr += digits
        if self.lowercaseOK: self.pattstr += ascii_lowercase
        if self.uppercaseOK: self.pattstr += ascii_uppercase
        if self.specialsymbolOK: self.pattstr += punctuation
        if self.spaceOK: self.pattstr += whitespace

        for filename,filepath in self.filepath.items():
            targetpath = f"{outdirectory}\\{filename}"
            fileextension = self.FindExt(filepath)
            temppath = f"{outdirectory}\\temp.{filename}{fileextension}"

            try:
                assert isinstance(filepath,list)

                with open(temppath,"wb") as outfile:
                    for file in filepath:
                        with open(file,"rb") as infile:
                            shutil.copyfileobj(infile,outfile)

            except AssertionError as e:
                logging.debug(e)
                with open(temppath,"wb") as outfile:
                    with open(filepath,"rb") as infile:
                        shutil.copyfileobj(infile,outfile)

            self.DeFiles(targetpath,temppath,filename+fileextension)
            os.remove(temppath)

    def DeFiles(self,target:str = None,root:str = None,filename:str = None) -> None:
        try:
            if os.path.exists(target):
                shutil.rmtree(target)
            patoolib.extract_archive(archive = root, outdir = target, verbosity = -1)
            logging.info(f"File {filename} extract successed.")
        except patoolib.util.PatoolError as e:
            logging.debug(e)
            if self.dictext:
                for path in self.dictext.values():
                    with open(path,"r") as f:
                        passwords = f.readlines()
                        for password in passwords:
                            password = password.strip()
                            try:
                                shutil.rmtree(target)
                                patoolib.extract_archive(archive = root, outdir = target, password = password, verbosity=-1)
                                logging.info(f"File {filename} extract successed. Password = {password}.")
                                return
                            except:
                                continue
            for i in range(1,self.codelen+1):
                for patt in product(self.pattstr,repeat=i):
                    password = "".join(patt)
                    try:
                        shutil.rmtree(target)
                        patoolib.extract_archive(archive = root, outdir = target, password = password, verbosity=-1)
                        logging.info(f"File {filename} extract successed. Password = {password}.")
                        return
                    except patoolib.util.PatoolError as e:
                        logging.debug(e)
                        continue

def main():
    zpf,txtf = CheckFile()
    conf = {}

    if os.path.exists("config.json"):
        with open("config.json","r") as js:
            conf = json.load(js)
        choose = input("Config already existed! Change again?")
        if choose in ('Y','y'):
            conf = ChangeConf()
        elif choose in ('N','n'):
            pass
        else:
            conf = ChangeConf()
    else:
        conf = ChangeConf()
    
    conf["zippath"] = zpf
    conf["txtpath"] = txtf

    confjs = json.dumps(conf, indent = 4)
    with open("config.json","w") as js:
        js.write(confjs)
    
    zipex = ZipExtract(conf)
    zipex.ExtractFiles()

if __name__ == "__main__":
    main()
    os.system("pause")
