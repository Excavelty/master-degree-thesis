from abc import ABC, abstractmethod

class Engine(ABC):
    @abstractmethod
    def load_models_from_files(self, file_name: str, file_name_piece: str) -> None:
        pass

    @abstractmethod
    def predict_next_move(self, fen: str) -> str:
        pass
