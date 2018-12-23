
class PyRepoGenError(Exception):
    pass

class ExecuteCmdError(PyRepoGenError):
    def __init__(self, returncode, msg):
        super().__init__(msg)
        self.returncode = returncode