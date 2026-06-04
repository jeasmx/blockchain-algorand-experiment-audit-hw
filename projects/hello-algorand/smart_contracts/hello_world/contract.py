from algopy import ARC4Contract, String, UInt64, Box, Bytes, Global, Txn
from algopy.arc4 import abimethod


class HelloWorld(ARC4Contract):
    """
    Smart contract para auditoría de resultados experimentales.

    Mantiene el nombre HelloWorld para no romper la estructura
    generada por AlgoKit, pero la lógica ya corresponde al proyecto...
    """

    def __init__(self) -> None:
        self.experiment_counter = UInt64(0)

        self.last_experiment_id = String("NONE")
        self.last_results_hash = String("NONE")
        self.last_throughput = String("0")
        self.last_collisions = String("0")

        self.last_author = Bytes(b"")
        self.last_round = UInt64(0)

    @abimethod()
    def hello(self, name: String) -> String:
        return String("Hello, ") + name

    @abimethod()
    def register_experiment(
        self,
        experiment_id: String,
        results_hash: String,
        throughput: String,
        collisions: String,
        timestamp: String,
    ) -> String:
        """
        Registra un experimento.

        Actualiza el Global State con el último experimento
        y además guarda un registro completo en una Box.
        """

        # Actualizar resumen global
        self.experiment_counter += 1
        self.last_experiment_id = experiment_id
        self.last_results_hash = results_hash
        self.last_throughput = throughput
        self.last_collisions = collisions
        self.last_author = Txn.sender.bytes
        self.last_round = Global.round

        # Crear una Box usando el ID del experimento como llave
        box_name = experiment_id.bytes
        experiment_box = Box(Bytes, key=box_name)

        # Guardar metadata estructurada y legible en la Box
        experiment_data = (
            b"experiment_id="
            + experiment_id.bytes
            + b";hash="
            + results_hash.bytes
            + b";throughput="
            + throughput.bytes
            + b";collisions="
            + collisions.bytes
            + b";timestamp="
            + timestamp.bytes
        )

        experiment_box.value = experiment_data

        return String("Experiment registered")

    @abimethod()
    def get_experiment_summary(self) -> String:
        """
        Regresa un resumen simple del último experimento registrado.
        """

        return (
            String("Experiment ID: ")
            + self.last_experiment_id
            + String(" | Hash: ")
            + self.last_results_hash
            + String(" | Throughput: ")
            + self.last_throughput
            + String(" | Collisions: ")
            + self.last_collisions
        )

    @abimethod()
    def get_experiment_box(
        self,
        experiment_id: String,
    ) -> String:
        """
        Consulta el registro completo de un experimento desde Box Storage.
        """

        box_name = experiment_id.bytes
        experiment_box = Box(Bytes, key=box_name)

        return String.from_bytes(experiment_box.value)
