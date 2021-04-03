import traceback
import os

class ConfReader:

    def __init__(self):
        pass

    def readConf(self, path):
        res = dict()
        with open(path, "r", encoding="utf-8") as f:
            for line in f.readlines():
                if line.strip().startswith("#") or not line.strip():
                    continue
                try:
                    key = line.split('=')[0].strip()
                    value = line.split('=')[1].strip()
                    res[key] = value
                    if key == "port":
                        res[key] = int(value)
                except Exception as e:
                    traceback.print_exc()
                    print("config file error,", e)
        important_kes = ["host", "port"]
        for key in important_kes:
            if key not in res.keys():
                print("fatal error, miss {} key in config file at path {}".format(key, path))
        return res


# conf = ConfReader().readConf(os.path.join("..", "config\conf"))  # 在次级目录测试的时候
conf = ConfReader().readConf(os.path.join("config", "conf"))


if __name__ == '__main__':
    print(ConfReader().readConf(os.path.join("..", "config\conf")))
