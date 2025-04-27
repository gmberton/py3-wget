# py3-wget

A Python library for downloading files with support for progress bars, checksum verification, timeout handling, and automatic retry on failed downloads.

## Features

- 📊 Progress bar visualization (optional)
- 🔄 Automatic retry on failed downloads
- 🔍 Checksum verification (cksum, MD5, SHA256)
- ⏱️ Configurable timeout and retry settings
- 🛡️ Safe file handling with overwrite protection
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
download_file("https://example.com/file.zip")
```

![Basic Download Demo](assets/e1.gif)

### Advanced Usage

#### Retry on Failure
The library automatically retries failed downloads with exponential backoff:
```python
download_file(
    "https://example.com/large-file.zip",
    max_tries=5,  # Maximum number of retry attempts
    retry_seconds=2  # Initial retry delay in seconds
)
```

#### Checksum Verification
Verify downloaded files using checksums:
```python
download_file(
    "https://example.com/important-file.zip",
    md5="d41d8cd98f00b204e9800998ecf8427e",  # MD5 checksum
    sha256="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"  # SHA256 checksum
)
```

![Checksum Verification Demo](assets/e4.gif)

#### File Overwrite Control
```python
download_file(
    "https://example.com/file.zip",
    output_path="downloads/file.zip",
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
