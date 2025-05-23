# Automatización Cartera

A Python-based automation system for managing and synchronizing client portfolio files across different storage locations. The system automatically processes and updates files at specified times, ensuring data consistency across Synology and NAS storage systems.

## Features

- Automated file processing and synchronization
- Scheduled updates at configurable times
- Support for multiple file types:
  - Client Portfolio files
  - Stock Inventory files
  - Inventory Quotation files
- Robust error handling and logging
- Configurable retry mechanisms
- Environment-based configuration

## Prerequisites

- Python 3.x
- Windows operating system (uses pywin32)
- Access to Synology and NAS storage systems
- MongoDB (for potential database operations)

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd "Automatizacion Cartera"
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
# On Windows
.venv\Scripts\activate
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with the following variables:
```env
SYNOLOGY_PATH=your_synology_path
NAS_PATH=your_nas_path
STOCK_PATH=your_stock_path
INVCOTIZAR_PATH=your_invcotizar_path
SYNOLOGY_DEST=your_synology_destination
NAS_DEST=your_nas_destination
```

## Configuration

The system's behavior can be configured through `config.py`:

- File paths and destinations
- Update schedules
- Retry settings
- Logging configuration

Default update times:
- Stock Inventory: 06:00
- Synology files: 06:03
- NAS files: 06:05
- Inventory Quotation: 06:08

## Usage

Run the main script:
```bash
python main.py
```

The system will:
1. Initialize file objects for each configured file
2. Monitor the current time
3. Process files at their scheduled update times
4. Log all operations to `procesos.log`

## Logging

Logs are stored in `procesos.log` with the following information:
- Timestamp
- Log level
- Operation details
- Error messages (if any)

## Project Structure

- `main.py`: Main program entry point
- `config.py`: Configuration settings
- `utils.py`: Utility functions and classes
- `service.py`: Service-related functionality
- `requirements.txt`: Project dependencies
- `procesos.log`: Operation logs

## Error Handling

The system includes comprehensive error handling:
- File operation errors
- Connection issues
- Unexpected exceptions
- Automatic retry mechanism

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Add your license information here] 