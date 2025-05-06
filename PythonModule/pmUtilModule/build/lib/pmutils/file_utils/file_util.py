# coding:utf-8
import os
import shutil


class FileUtils:

    @staticmethod
    def getDirFile(path: str):
        """ get directory all files|directory """
        return os.listdir(path)

    @staticmethod
    def isDir(path: str):
        """ check whether is directory """
        return os.path.isdir(path)

    @staticmethod
    def getAbsPath(path: str):
        """ get absolute path from path """
        return os.path.abspath(path)

    @staticmethod
    def getBaseName(path: str):
        """ get file dir name """
        return os.path.basename(path)

    @staticmethod
    def getDirName(path: str):
        """ get dir name """
        return os.path.dirname(path)

    @staticmethod
    def joinPath(p1: str, p2: str):
        """ stitching path """
        return os.path.join(p1, p2)

    @staticmethod
    def getFileName(path: str):
        """ get file name, not contains suffix"""
        return os.path.splitext(path)[0]

    @staticmethod
    def getFileSuffixName(path: str):
        """ get file suffix name"""
        return os.path.splitext(path)[1].replace('.', '')

    @staticmethod
    def exist(path: str):
        return os.path.exists(path)

    @staticmethod
    def readFile(path: str):
        """ read file """
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()

    @staticmethod
    def readFiles(path: list[str]):
        """ read files """
        result = []
        for path in path:
            with open(path, 'r', encoding='utf-8') as f:
                result.append(f.read())
        return result

    def createDir(self, path: str):
        """ create directory, if exist not create directory """
        if self.exist(path):
            raise "directory already exist"
        os.mkdir(path)

    def createRecursionDir(self, path: str):
        """ create recursion directory, if exist not create directory """
        if self.exist(path):
            raise "directory already exist"
        os.makedirs(path)

    def createFile(self, path: str):
        """ create file, if exist not create file """
        if self.exist(path):
            raise "file already exist"
        with open(path, 'w', encoding='utf-8'):
            pass

    def removeFile(self, path: str):
        """ delete file"""
        if self.exist(path):
            raise "file not exist"
        os.remove(path)

    def removeEmptyDir(self, path: str):
        """ delete empty directory"""
        if not self.exist(path):
            raise "directory not exist"
        os.rmdir(path)

    def removeDir(self, path: str):
        """ delete empty | not empty directory """
        if not self.exist(path):
            raise "directory not exist"
        shutil.rmtree(path)

    def rename(self, src: str, dst: str):
        """ rename file or directory, if exist not rename"""
        if not self.exist(src) or self.exist(dst):
            raise "file or directory already exist"
        os.rename(src, dst)