from Exceptions.undoredo_exception import UndoRedoException


class UndoRedoService:

    def __init__(self):
        self.__redo_stack = []
        self.__undo_stack = []

    def add_to_undo(self, operation):
        self.__undo_stack.append(operation)

    def do_undo(self):
        if len(self.__undo_stack) == 0:
            raise UndoRedoException("Lista de undo este goala")
        undo_operation = self.__undo_stack.pop()
        undo_operation.undo()
        self.__redo_stack.append(undo_operation)

    def do_redo(self):
        if len(self.__redo_stack) == 0:
            raise UndoRedoException("Lista de redo este goala!")
        redo_operation = self.__redo_stack.pop()
        redo_operation.redo()
        self.__undo_stack.append(redo_operation)

    def clear_redo(self):
        self.__redo_stack.clear()
