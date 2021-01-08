import os

# makes a list of all files in a directory,
# with its full pathname.
class DirTree():
    def __init__(self):
        pass

    def files(self, dir = "."):
        self.result = []
        for root, dirs, files in os.walk(dir):
            if (len(files) > 0):
                files = [ root + "/" + file for file in files ];
                self.result.extend(files);

        return(self.result)
