# Dev Environment Readyifier

An automated tool to detect, configure, and optimize development environments with AI-enhanced tools, security hardening, and best practices.

## Overview

This repository provides a comprehensive solution for setting up and configuring development environments across multiple IDEs and AI coding assistants. It automatically detects installed tools, allows customization of configurations, and applies best practices for security and efficiency.

## Features

- **Automatic Detection**: Scans your system for installed IDEs and AI tools
- **Interactive Configuration**: Select which tools to configure and customize settings
- **Security Hardening**: Implements security best practices across all environments
- **AI Assistant Rules**: Configures AI coding assistants with optimal behavior rules
- **Extension Management**: Installs and configures recommended extensions
- **Reference Structure**: Creates standardized reference data organization

## Supported Tools

- VS Code / VS Code Insiders
- Trae IDE
- VOID IDE
- Cline
- Roo Code
- Aider
- And more (automatically detected)

## Requirements

- Python 3.8+
- Conda environment (recommended)
- Git

## Quick Start

```bash
# Clone the repository
git clone https://github.com/k3ss-official/dev-env-readyifier.git

# Navigate to the repository
cd dev-env-readyifier

# Run the setup script
python setup.py
```

## Repository Structure

```
dev-env-readyifier/
├── scripts/              # Python scripts for automation
│   ├── detector.py       # Tool detection logic
│   ├── configurator.py   # Configuration application
│   ├── installer.py      # Extension installation
│   └── validator.py      # Setup validation
├── templates/            # Configuration templates
│   ├── ai_rules/         # AI assistant rules
│   ├── extensions/       # Extension recommendations
│   ├── security/         # Security configurations
│   └── reference/        # Reference data structures
├── configs/              # Tool-specific configurations
│   ├── vscode/           # VS Code configurations
│   ├── trae/             # Trae IDE configurations
│   └── ...               # Other tool configurations
├── docs/                 # Documentation
│   ├── usage.md          # Usage instructions
│   ├── customization.md  # Customization guide
│   └── maintenance.md    # Maintenance instructions
├── setup.py              # Main setup script
└── README.md             # Repository documentation
```

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
