# coding:utf-8
import json


class JsonUtils:
    def readJsonFile(self, path: str) -> dict:
        """ read json file """
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def readJsonFiles(self, path: list[str]):
        """ read json files"""
        result = []
        for path in path:
            with open(path, 'r', encoding='utf-8') as f:
                result.append(json.load(f))
        return result

    def appendJsonFile(self, path: str, data: dict, indent=4):
        """ append json file """
        with open(path, 'r+', encoding='utf-8') as f:
            result = json.load(f)
            result.update(data)
            f.seek(0)
            f.truncate()
            json.dump(result, f, ensure_ascii=False, indent=indent)
        return f

    def writeJsonFile(self, path: str, data: dict, indent=4):
        """ write json file """
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=indent)
            return f