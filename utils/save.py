from typing import Protocol
from pathlib import Path

from utils.meth_data import MethylationData


class DataWriter(Protocol):
    """Interphase to save data.
    """
    def save(self, data) -> None:
        ...


class WriteMethlation2CSV:
    """Saves class MethylationData to csv file.
    """
    def save(self, data: MethylationData) -> None:
        for d in data.data:
            save_name = d.file_name.strip(".sam") + ".csv"
            tag = Path.cwd() / save_name
            with open(tag, "w") as fh:
                fh.write("\n".join([str(i) for i in d.meth_levels]))


def save_data(data, datawriter: DataWriter) -> None:
    datawriter.save(data)