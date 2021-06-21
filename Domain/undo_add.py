from Domain.undo_operation import UndoRedoOperation
from Repo.file_repository import FileRepository


class UndoAdd(UndoRedoOperation):
    """
    Clasa de undo pentru add
    """
    def __init__(self, entitate, repository: FileRepository):
        super().__init__(repository)
        self.__entitate_salvata = entitate

    def undo(self):
        self._repository.delete(self.__entitate_salvata.id_entitate)

    def redo(self):
        self._repository.create(self.__entitate_salvata)