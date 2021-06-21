from Domain.undo_operation import UndoRedoOperation
from Repo.file_repository import FileRepository


class UndoUpdate(UndoRedoOperation):
    """
    Clasa de undo pentru update
    """
    def __init__(self, entitate_veche,enitate_noua, repository: FileRepository):
        super().__init__(repository)
        self.__entitate_veche = entitate_veche
        self.__entitate_noua = enitate_noua

    def undo(self):
        self._repository.update(self.__entitate_veche)

    def redo(self):
        self._repository.update(self.__entitate_noua)