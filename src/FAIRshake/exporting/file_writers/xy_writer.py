# FAIRshake/exporting/file_writers/xy_writer.py

import logging
from pathlib import Path
from typing import Any

import numpy as np


class XyWriter:
    """
    A class for writing data to XY format files.
    """

    def __init__(self, output_directory: Path, logger: logging.Logger):
        """
        Initialize the XyWriter.

        Parameters
        ----------
        output_directory : Path
            Directory where XY files will be saved.
        logger : logging.Logger
            Logger instance for logging messages.
        """
        self.output_directory: Path = output_directory
        self.logger: logging.Logger = logger

    def write(self, x: np.ndarray, y: np.ndarray, filename: str) -> None:
        """
        Write the spectra data to an XY file.

        Parameters
        ----------
        x : np.ndarray
            Radial positions.
        y : np.ndarray
            Intensities.
        filename : str
            Name of the output file without extension.
        """
        safe_filename: str = self._sanitize_filename(filename)
        file_path: Path = self.output_directory / f"{safe_filename}.xy"

        # Write data to file
        try:
            with open(file_path, "w") as f:
                for xi, yi in zip(x, y):
                    f.write(f"{xi:.18e}\t{yi:.18e}\n")
            self.logger.debug(f"Successfully wrote XY file: {file_path}")
        except Exception as exc:
            self.logger.error(
                f"Error writing XY file {file_path}: {exc}", exc_info=True
            )

    def _sanitize_filename(self, filename: str) -> str:
        """
        Sanitize the filename by replacing or removing invalid characters.

        Parameters
        ----------
        filename : str
            The original filename with potential invalid characters.

        Returns
        -------
        str
            A sanitized filename safe for filesystem usage.
        """
        invalid_chars: str = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, "_")
        return filename.strip()