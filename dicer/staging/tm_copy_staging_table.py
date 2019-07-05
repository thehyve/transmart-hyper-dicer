import inspect
import logging
from abc import ABC, abstractmethod
from pathlib import Path

from pandas import DataFrame


class TmCopyStagingTable(ABC):
    out_file_name = None

    @abstractmethod
    def build_transmart_copy_df(self) -> DataFrame:
        pass

    def write_to_file(self, df: DataFrame, output_root_dir: Path) -> None:
        # Get name of directory the class is in
        i2b2_table = Path(inspect.getfile(self.__class__)).parent.name

        out_path = output_root_dir / i2b2_table / self.out_file_name
        logging.info(f'Writing file at {out_path}')
        df.to_csv(out_path, sep='\t', index=False)
