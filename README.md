# py3-wget

A Python library for downloading files of any size, especially optimized for large file downloads, with support for progress bars, checksum verification, timeout handling, and automatic retry on failed downloads.

## Features

- 🚀 Optimized for large file downloads
- 📊 Progress bar visualization (optional)
- 🔄 Automatic retry on failed downloads
- 🔍 Optional integrity checks (cksum, MD5, SHA256)
- ⏱️ Configurable timeout and retry settings
- 🛡️ Safe file handling, optional overwrite
- 📦 Simple and intuitive API

## Installation

```bash
pip install py3-wget
```

## Quick Start

### Basic Download
```python
from py3_wget import download_file

# Simple download with progress bar
download_file("https://raw.githubusercontent.com/python/cpython/3.11/LICENSE")
```

![Basic Download Demo](assets/e1.gif)

### Advanced Usage

#### Retry on Failure
The library automatically retries failed downloads with exponential backoff:
```python
download_file(
    "https://raw.githubusercontent.com/python/cpython/3.11/LICENSE",
    max_tries=5,  # Maximum number of retry attempts
    retry_seconds=2  # Initial retry delay in seconds
)
```

#### Checksum Verification
Verify downloaded files using checksums:
```python
download_file(
    "https://raw.githubusercontent.com/python/cpython/3.11/LICENSE",
    md5="fcf6b249c2641540219a727f35d8d2c2",  # MD5 checksum
    sha256="3aff1954277c4fc27603346901e4848b58fe3c8bed63affe6086003dd6c2b9fe"  # SHA256 checksum
)
```

![Checksum Verification Demo](assets/e4.gif)

#### File Overwrite Control
```python
download_file(
    "https://raw.githubusercontent.com/python/cpython/3.11/LICENSE",
    output_path="downloads/test.bin",
    overwrite=True  # Overwrite existing file
)
```

![Overwrite Demo](assets/e3.gif)

## API Reference

### `download_file`

```python
download_file(
    url: str,
    output_path: Optional[Union[str, Path]] = None,
    overwrite: bool = False,
    verbose: bool = True,
    cksum: Optional[int] = None,
    md5: Optional[str] = None,
    sha256: Optional[str] = None,
    max_tries: int = 5,
    block_size_bytes: int = 8192,
    retry_seconds: Union[int, float] = 2,
    timeout_seconds: Union[int, float] = 60,
) -> None
```

#### Parameters

- `url` (str): URL of the file to download
- `output_path` (str or Path, optional): Path to save the file. If None, derived from URL
- `overwrite` (bool): Overwrite existing file (default: False)
- `verbose` (bool): Show progress bar and messages (default: True)
- `cksum` (int, optional): Expected checksum value
- `md5` (str, optional): Expected MD5 hash
- `sha256` (str, optional): Expected SHA256 hash
- `max_tries` (int): Maximum retry attempts (default: 5)
- `block_size_bytes` (int): Download block size in bytes (default: 8192)
- `retry_seconds` (int/float): Initial retry delay in seconds (default: 2)
- `timeout_seconds` (int/float): Download timeout in seconds (default: 60)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
