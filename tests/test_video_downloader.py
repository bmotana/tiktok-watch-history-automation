import unittest
from unittest.mock import mock_open, patch
import yaml
from scripts.video_downloader import VideoDownloader

class TestVideoDownloader(unittest.TestCase):

    def setUp(self):
        self.video_downloader = VideoDownloader(config_path="config/config.yaml")

    @patch('builtins.open', new_callable=mock_open, read_data="api_key: test_key\noutput_dir: /test/dir")
    def test_load_config_valid(self, mock_file):
        config = self.video_downloader._load_config('dummy_path.yaml')
        self.assertEqual(config['api_key'], 'test_key')
        self.assertEqual(config['output_dir'], '/test/dir')

    @patch('builtins.open', new_callable=mock_open, read_data="invalid_yaml:")
    def test_load_config_invalid_yaml(self, mock_file):
        with self.assertRaises(yaml.YAMLError):
            self.video_downloader._load_config('dummy_path.yaml')

    @patch('builtins.open', new_callable=mock_open, read_data="api_key: test_key")
    def test_load_config_missing_required_field(self, mock_file):
        with self.assertRaises(ValueError):
            self.video_downloader._load_config('dummy_path.yaml')

    @patch('builtins.open', new_callable=mock_open, read_data="api_key: test_key\noutput_dir: /test/dir\nextra_field: value")
    def test_load_config_extra_field(self, mock_file):
        config = self.video_downloader._load_config('dummy_path.yaml')
        self.assertNotIn('extra_field', config)

    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_load_config_file_not_found(self, mock_file):
        with self.assertRaises(FileNotFoundError):
            self.video_downloader._load_config('non_existent_file.yaml')

if __name__ == '__main__':
    unittest.main()
