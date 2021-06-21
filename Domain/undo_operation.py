from Repo.file_repository import FileRepository


class UndoRedoOperation:
    """
    Clasa virtuala exstinsa de clase undo pentru fiecare operatie
    """
    def __init__(self, repository: FileRepository):
        self._repository = repository

    def undo(self):
        raise NotImplemented('Should use a derived class!')

    def redo(self):
        raise NotImplemented('Should use a derived class!')