# Usage and Maintenance Guide

This document provides detailed instructions for using and maintaining the Dev Environment Readyifier tool.

## Installation

### Prerequisites

- Python 3.8 or higher
- Tkinter (usually included with Python)
- Git

### Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/k3ss-official/dev-env-readyifier.git
   ```

2. Navigate to the repository directory:
   ```bash
   cd dev-env-readyifier
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Tool

1. From the repository root directory, run:
   ```bash
   python setup.py
   ```

2. The GUI will launch, guiding you through the setup process:
   - Detection: The tool will scan your system for installed IDEs and tools
   - Selection: Choose which tools to configure or install
   - Configuration: Set security level, AI personality, and reference structure options
   - Installation: The tool will install missing tools and apply configurations
   - Summary: Review the changes made to your environment

### GUI Navigation

- **Next/Back**: Navigate between steps
- **Select All**: Quickly select all tools for configuration or installation
- **Clear All**: Clear all selections

## Configuration Options

### Security Levels

- **Standard**: Recommended security practices for most development environments
- **Enhanced**: Additional security measures and hardening for sensitive projects

### AI Personality

- **Default**: Based on the provided personality profile
- **Custom**: (Coming soon) Customize AI assistant behavior

### Reference Structure

When enabled, creates a standardized directory structure for organizing:
- Organization information
- Technical specifications
- Security policies
- API documentation
- Workflow processes

## Maintenance

### Updating the Tool

1. Pull the latest changes:
   ```bash
   git pull origin main
   ```

2. Run the setup script again:
   ```bash
   python setup.py
   ```

### Adding New Tools

To add support for new tools:

1. Update the `detector.py` script to detect the new tool
2. Add installation logic in `installer.py`
3. Create configuration templates in the `templates` directory
4. Update the GUI to display and configure the new tool

### Troubleshooting

If you encounter issues:

1. Check the logs in the Installation tab
2. Ensure you have the necessary permissions to install software
3. For VS Code extensions, ensure the VS Code CLI is in your PATH
4. For tool-specific issues, refer to the tool's documentation

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
