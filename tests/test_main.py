import pytest
from unittest.mock import patch, MagicMock
from urllib.error import URLError

from py3_wget import download_file
from py3_wget.main import _get_output_path, validate_download_params, validate_cksums


# Test data
TEST_URL = "https://raw.githubusercontent.com/python/cpython/3.11/LICENSE"
DOWNLOAD_CKSUM = 922448126
DOWNLOAD_MD5 = "fcf6b249c2641540219a727f35d8d2c2"
DOWNLOAD_SHA256 = "3b2f81fe21d181c499c59a256c8e1968455d6689d269aa85373bfb6af41da3bf"

FILE_CONTENT = b"Hello, World!"
FILE_CKSUM = 2609532967
FILE_MD5 = "65a8e27d8879283831b664bd8b7f0ad4"
FILE_SHA256 = "dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a362182986f"

INVALID_URL = "https://invalid-url-that-does-not-exist.com/test.txt"



class TestGetOutputPath:
    def test_default_filename_from_url(self):
        headers = {}
        url = TEST_URL
        output_path, partial_filename = _get_output_path(headers, url, None)
        assert output_path == "LICENSE"
        assert partial_filename == "LICENSE.part"

    def test_filename_from_content_disposition(self):
        headers = {"content-disposition": 'filename="custom.txt"'}
        url = TEST_URL
        output_path, partial_filename = _get_output_path(headers, url, None)
        assert output_path == "custom.txt"
        assert partial_filename == "custom.txt.part"

    def test_custom_output_path(self):
        headers = {}
        url = TEST_URL
        custom_path = "custom/path/file.txt"
        output_path, partial_filename = _get_output_path(headers, url, custom_path)
        assert output_path == custom_path
        assert partial_filename == "file.txt.part"


class TestValidateDownloadParams:
    def test_valid_params(self):
        validate_download_params(
            url=TEST_URL,
            output_path="test.txt",
            overwrite=True,
            verbose=True,
            cksum=123,
            md5="a" * 32,
            sha256="b" * 64,
            max_tries=3,
            block_size_bytes=8192,
            retry_seconds=2,
            timeout_seconds=30,
        )

    def test_invalid_url(self):
        with pytest.raises(ValueError, match="The URL must be a string starting with 'http://' or 'https://'."):
            validate_download_params(
                url="ftp://example.com",
                output_path="test.txt",
                overwrite=True,
                verbose=True,
                cksum=None,
                md5=None,
                sha256=None,
                max_tries=3,
                block_size_bytes=8192,
                retry_seconds=2,
                timeout_seconds=30,
            )

    def test_invalid_md5(self):
        with pytest.raises(ValueError, match="The md5 parameter must be a 32-character hexadecimal string or None."):
            validate_download_params(
                url=TEST_URL,
                output_path="test.txt",
                overwrite=True,
                verbose=True,
                cksum=None,
                md5="invalid",
                sha256=None,
                max_tries=3,
                block_size_bytes=8192,
                retry_seconds=2,
                timeout_seconds=30,
            )


class TestValidateCksums:
    def test_valid_cksum(self, tmp_path):
        test_file = tmp_path / "test.txt"
        test_file.write_bytes(FILE_CONTENT)
        validate_cksums(str(test_file), cksum=FILE_CKSUM, md5=FILE_MD5, sha256=FILE_SHA256)

    def test_invalid_md5(self, tmp_path):
        test_file = tmp_path / "test.txt"
        test_file.write_bytes(FILE_CONTENT)
        with pytest.raises(RuntimeError, match="MD5 mismatch"):
            validate_cksums(str(test_file), cksum=None, md5="a" * 32, sha256=None)


class TestDownloadFile:
    @patch("urllib.request.urlopen")
    def test_successful_download(self, mock_urlopen, tmp_path):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.headers = {"content-length": str(len(FILE_CONTENT))}
        mock_response.read.side_effect = [FILE_CONTENT, b""]
        mock_urlopen.return_value.__enter__.return_value = mock_response

        # Test download
        output_path = tmp_path / "test.txt"
        download_file(
            TEST_URL,
            output_path,
            overwrite=True,
            verbose=False,
            cksum=DOWNLOAD_CKSUM,
            md5=DOWNLOAD_MD5,
            sha256=DOWNLOAD_SHA256,
        )

        assert output_path.exists()

    def test_invalid_url(self, tmp_path):
        with pytest.raises(RuntimeError):
            download_file(
                INVALID_URL,
                str(tmp_path / "test.txt"),
                max_tries=1,
            )

    def test_timeout(self, tmp_path):
        with pytest.raises(RuntimeError):
            download_file(
                TEST_URL,
                str(tmp_path / "test.txt"),
                timeout_seconds=0.0001,
                max_tries=1,
            )


class TestIntegration:
    def test_download_with_md5(self, tmp_path):
        output_path = tmp_path / "LICENSE"
        download_file(TEST_URL, str(output_path), verbose=False)
        assert output_path.exists()

    def test_overwrite_behavior(self, tmp_path):
        output_path = tmp_path / "test.bin"
        
        # First download
        download_file(TEST_URL, str(output_path), verbose=False)
        first_size = output_path.stat().st_size
        
        # Try to download again without overwrite
        download_file(TEST_URL, str(output_path), overwrite=False, verbose=False)
        assert output_path.stat().st_size == first_size
        
        # Download with overwrite
        download_file(TEST_URL, str(output_path), overwrite=True, verbose=False)
        assert output_path.stat().st_size == first_size
