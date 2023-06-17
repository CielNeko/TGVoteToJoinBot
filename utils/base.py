import rtoml


class Dict(dict):
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__


class Tool(object):

    def dictToObj(self, dictObj):
        if not isinstance(dictObj, dict):
            return dictObj
        d = Dict()
        for k, v in dictObj.items():
            d[k] = self.dictToObj(v)
        return d


class readconfig(object):
    def __init__(self, config=None):
        """
        read some further config!

        param paths: the file path
        """
        self.config = config

    def get(self):
        return self.config

    def parseFile(self, paths: str, toObj: bool = False):
        data = rtoml.load(open(paths, 'r', encoding='utf-8'))
        self.config = Tool().dictToObj(data) if toObj else data
        return self.config
