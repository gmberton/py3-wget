import pytest
from unittest.mock import patch, MagicMock
from urllib.error import URLError

from py3_wget import download_file
from py3_wget.main import _get_output_path, validate_download_params, validate_cksums


# Test data
TEST_URL = "https://www.w3.org/TR/png/iso_8859-1.txt"
TEST_CKSUM_DOWNLOAD = 1017922820
TEST_MD5_DOWNLOAD = "8026e3af0d2e130dab1f5c530bf1c353"
TEST_SHA256_DOWNLOAD = "3aff1954277c4fc27603346901e4848b58fe3c8bed63affe6086003dd6c2b9fe"

TEST_FILE_CONTENT = b"Hello, World!"
TEST_CKSUM_FILE = 2609532967
TEST_MD5_FILE = "65a8e27d8879283831b664bd8b7f0ad4"
TEST_SHA256_FILE = "dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a362182986f"


class TestGetOutputPath:
    def test_default_filename_from_url(self):
        headers = {}
        url = "https://example.com/test.txt"
        output_path, partial_filename = _get_output_path(headers, url, None)
        assert output_path == "test.txt"
        assert partial_filename == "test.txt.part"

    def test_filename_from_content_disposition(self):
        headers = {"content-disposition": 'filename="custom.txt"'}
        url = "https://example.com/test.txt"
        output_path, partial_filename = _get_output_path(headers, url, None)
        assert output_path == "custom.txt"
        assert partial_filename == "custom.txt.part"

    def test_custom_output_path(self):
        headers = {}
        url = "https://example.com/test.txt"
        custom_path = "custom/path/file.txt"
        output_path, partial_filename = _get_output_path(headers, url, custom_path)
        assert output_path == custom_path
        assert partial_filename == "file.txt.part"


class TestValidateDownloadParams:
    def test_valid_params(self):
        validate_download_params(
            url="https://example.com",
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
                url="https://example.com",
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
        test_file.write_bytes(TEST_FILE_CONTENT)
        validate_cksums(str(test_file), cksum=TEST_CKSUM_FILE, md5=TEST_MD5_FILE, sha256=TEST_SHA256_FILE)

    def test_invalid_md5(self, tmp_path):
        test_file = tmp_path / "test.txt"
        test_file.write_bytes(TEST_FILE_CONTENT)
        with pytest.raises(RuntimeError, match="MD5 mismatch"):
            validate_cksums(str(test_file), cksum=None, md5="a" * 32, sha256=None)


class TestDownloadFile:
    @patch("urllib.request.urlopen")
    def test_successful_download(self, mock_urlopen, tmp_path):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.headers = {"content-length": str(len(TEST_FILE_CONTENT))}
        mock_response.read.side_effect = [TEST_FILE_CONTENT, b""]
        mock_urlopen.return_value.__enter__.return_value = mock_response

        # Test download
        output_path = tmp_path / "test.txt"
        download_file(
            TEST_URL,
            output_path,
            overwrite=True,
            verbose=False,
            cksum=TEST_CKSUM_DOWNLOAD,
            md5=TEST_MD5_DOWNLOAD,
            sha256=TEST_SHA256_DOWNLOAD,
        )

        assert output_path.exists()

    def test_invalid_url(self, tmp_path):
        with pytest.raises(RuntimeError):
            download_file(
                "https://invalid-url-that-does-not-exist.com/test.txt",
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
    def test_download_small_file(self, tmp_path):
        url = "https://httpbin.org/bytes/1024"  # 1KB file
        output_path = tmp_path / "test.bin"
        download_file(url, str(output_path), verbose=False)
        assert output_path.exists()
        assert output_path.stat().st_size == 1024

    def test_download_with_md5(self, tmp_path):
        # Using a known file with known MD5
        url = "https://raw.githubusercontent.com/python/cpython/3.11/LICENSE"
        output_path = tmp_path / "LICENSE"
        expected_md5 = "fcf6b249c2641540219a727f35d8d2c2"
        download_file(url, str(output_path), md5=expected_md5, verbose=False)
        assert output_path.exists()

    def test_overwrite_behavior(self, tmp_path):
        url = "https://httpbin.org/bytes/1024"
        output_path = tmp_path / "test.bin"
        
        # First download
        download_file(url, str(output_path), verbose=False)
        first_size = output_path.stat().st_size
        
        # Try to download again without overwrite
        download_file(url, str(output_path), overwrite=False, verbose=False)
        assert output_path.stat().st_size == first_size
        
        # Download with overwrite
        download_file(url, str(output_path), overwrite=True, verbose=False)
        assert output_path.stat().st_size == first_size
