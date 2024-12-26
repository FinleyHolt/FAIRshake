import unittest
from pathlib import Path
from FAIRshake.execution_pipeline.pipeline import ExecutionPipeline

class TestExecutionPipeline(unittest.TestCase):

    def setUp(self):
        # Configuration Parameters
        self.input_base_dir = Path('/Users/finley/Downloads/GitHub/SHAKE/V5-7_insitu')
        self.output_base_dir = Path('/Users/finley/Downloads/GitHub/SHAKE/V5-7_insitu_fxye')
        self.output_base_dir.mkdir(parents=True, exist_ok=True)

        self.integration_config = {
            "poni_file_path": str(self.input_base_dir / "calibration_files" / "det0.poni"),
            "npt_radial": 500,
            "unit": "2th_deg",
            "do_solid_angle": False,
            "error_model": "poisson",
            "radial_range": (2.8, 11.2),
            "azimuth_range": (-180, 180),
            "polarization_factor": 0.99,
            "method": ("full", "histogram", "cython"),
            "safe": True,
        }

        self.exporting_config = {
            "output_directory": str(self.output_base_dir),
            "naming_convention": "{GE_filenumber}",
            "options": {"do_remove_nan": True, "unit": "2th_deg"},
            "file_format": "fxye"
        }

        self.preprocessing_config_full = {
            "dark_field_path": str(self.input_base_dir / "3/ff/ff_004326.ge2"),
            "mask_file_path": str(self.input_base_dir / "calibration_files/mask.edf"),
            "invert_mask": True,
            "min_intensity": 0.0,
            "max_intensity": None,
        }

        self.pipeline_params = {
            "input_base_dir": str(self.input_base_dir),
            "output_base_dir": str(self.output_base_dir),
            "batch_size": 10,
            "data_file_types": ['.ge2'],
            "metadata_file_types": ['.json'],
            "require_metadata": True,
            "load_metadata_files": True,
            "load_detector_metadata": False,
            "require_all_formats": False,
            "average_frames": True,
            "enable_profiling": True,
            "tf_data_debug_mode": False,
            "pattern": '*/*/*',
            "preprocessing_config": self.preprocessing_config_full,
            "enable_preprocessing": True,
            "enable_integration": True,
            "integration_config": self.integration_config,
            "enable_exporting": True,
            "exporting_config": self.exporting_config,
            "log_level": "INFO"
        }

    def test_pipeline_initialization(self):
        pipeline = ExecutionPipeline(**self.pipeline_params)
        self.assertIsNotNone(pipeline)

    def test_pipeline_run(self):
        pipeline = ExecutionPipeline(**self.pipeline_params)
        dataset = pipeline.run_all()
        self.assertIsNotNone(dataset)

if __name__ == "__main__":
    unittest.main()