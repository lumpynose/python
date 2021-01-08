import os

class DirTree():
    def __init__(self):
        pass

    def files(self, dir):
        self.result = []
        # for root, dirs, files in os.walk("/home/rusty/pics"):
        for root, dirs, files in os.walk(dir):
            # print(root, dirs)
            if (len(files) > 0):
                for file in files:
                    self.result.append(root + "/" + file)

        return(self.result)
