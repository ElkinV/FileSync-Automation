# FileSync Automation

A Python-based automation system for managing and synchronizing business-critical files across multiple storage locations. Provides automated file processing, scheduled updates, and ensures data consistency.

## Key Features

- **File Management**
  - Scheduled processing and updates
  - Multi-location synchronization
  - Automatic file relocation
  - Configurable schedules

- **Reliability**
  - Comprehensive logging
  - Error detection and recovery
  - Configurable retry mechanisms
  - Real-time monitoring

## Requirements

- Python 3.x
- Windows OS
- Network storage access
- MongoDB (optional)

## Quick Start

1. Clone and setup:
```bash
git clone [repository-url]
cd portfolio-automation
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

2. Configure `.env`:
```env
STORAGE_PATH_1=your_primary_storage_path
STORAGE_PATH_2=your_secondary_storage_path
```

3. Run:
```bash
python main.py
```

## Configuration

Configure through `config.py`:
- Storage locations
- Processing schedules
- Error handling
- Logging preferences

## System Components

- `main.py`: System orchestrator
- `config.py`: Configuration
- `utils.py`: Core utilities
- `service.py`: Service layer
- `procesos.log`: System logs

## Development

1. Fork repository
2. Create feature branch
3. Implement changes
4. Submit PR

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
