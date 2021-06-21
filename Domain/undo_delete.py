from Domain.undo_operation import UndoRedoOperation
from Repo.file_repository import FileRepository


class UndoDelete(UndoRedoOperation):
    """
    clasa de undo pentru delete
    """
    def __init__(self, entitate_stearsa, repository: FileRepository):
        super().__init__(repository)
        self.__entitate_stearsa = entitate_stearsa

    def undo(self):
        self._repository.create(self.__entitate_stearsa)

    def redo(self):
        self._repository.delete(self.__entitate_stearsa.id_entitate)