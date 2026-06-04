from algopy import ARC4Contract, String
from algopy.arc4 import abimethod


class HelloWorld(ARC4Contract):
    @abimethod()
    def hello(self, name: String) -> String:
        return "Hello, " + name



from algopy import ARC4Contract, String, UInt64, Box, Bytes, Global, Txn
from algopy.arc4 import abimethod


class  HelloWorld(ARC4Contract):
    """
    Contrato base del proyecto.

    Conservamos HelloWorld para no romper la configuración
    generada por AlgoKit.
    """

    def __init__(self) -> None:
        """
        Inicializa el estado global del contrato.
        Inicializa variables persistentes del contrato.
        experiment_counter empieza en 0.
        """
        self.experiment_counter = UInt64(0)
        self.last_experiment_id = String("NONE")
        self.last_results_hash = String("NONE")
        self.last_throughput = UInt64(0)
        self.last_collisions = UInt64(0)
        self.last_author = Bytes(b"")
        self.last_round = UInt64(0)

    @abimethod()
    def hello(self, name: String) -> String:
        """
        Método original del quick start.
        """
        return String("Hello, ") + name

    @abimethod()
    def register_experiment(
        self,
        experiment_id: String,
        results_hash: String,
        throughput: UInt64,
        collisions: UInt64,
    ) -> String:
        """
        Registra un experimento y guarda metadata básica.
        """

        # Guardar datos en blockchain state
        # Incrementar contador
        self.experiment_counter += 1
        self.last_experiment_id = experiment_id
        self.last_results_hash = results_hash
        self.last_throughput = throughput
        self.last_collisions = collisions
        self.last_author = Txn.sender.bytes
        self.last_round = Global.round

        return String("Experiment registered")
    @abimethod()


    def get_experiment_summary(self) -> String:
        """
        Regresa un resumen simple del último experimento registrado.

        Por ahora regresamos solo ID y hash porque es lo más importante
        para verificar integridad.
        """

        return (
            String("Experiment ID: ")
            + self.last_experiment_id
            + String(" | Hash: ")
            + self.last_results_hash
        )
    
    @abimethod()
    def save_experiment_hash_box(
        self,
        experiment_id: String,
        results_hash: String,
    ) -> String:
        """
        Guarda el hash de un experimento usando Box Storage.

        Cada experimento se guarda en una box diferente.

        experiment_id:
            Se usará como nombre o llave de la box.

        results_hash:
            Se guardará como valor dentro de la box.
        """

        # Convertimos el identificador del experimento a bytes.
        # Las boxes usan nombres tipo bytes.
        box_name = experiment_id.bytes

        # Creamos una box asociada a ese nombre.
        # El valor será de tipo Bytes.
        experiment_box = Box(Bytes, key=box_name)

        # Guardamos el hash como bytes dentro de la box.
        experiment_box.value = results_hash.bytes


        return String("Experiment hash saved in box")
    

    @abimethod()
    def get_experiment_hash_box(
        self,
        experiment_id: String,
    ) -> String:
        """
        Consulta el hash de resultados guardado en una Box.

        experiment_id:
            Identificador del experimento que queremos consultar.

        Retorna:
            El hash almacenado para ese experimento.
        """

        # Convertimos el ID del experimento a bytes,
        # porque el nombre de una Box se maneja como bytes.
        box_name = experiment_id.bytes

        # Abrimos la Box asociada a ese experimento.
        experiment_box = Box(Bytes, key=box_name)

        # Leemos el valor de la Box y lo convertimos de nuevo a String.
        return String.from_bytes(experiment_box.value)
