
# Odoo Installation Script

This repository contains a Python script to automate the installation of Odoo 17 Community on an Ubuntu 22.04.1 LTS virtual machine. The script installs and configures PostgreSQL, sets up an isolated virtual environment for Odoo dependencies, and configures the Odoo service.

## Features
- Automatic installation and configuration of PostgreSQL
- Sets up a Python virtual environment for Odoo
- Configures Odoo to run as a service on Ubuntu
- Ensures compatibility with Odoo 17 Community version

## Prerequisites
- Ubuntu 22.04.1 LTS
- Python 3.7 or higher

## Installation

1. **Clone this repository**:

    ```bash
    git clone https://github.com/darky404/odoo.git
    cd odoo
    ```

2. **Run the installation script**:

    ```bash
    sudo python3 install_odoo.py
    ```

## Manual Configuration
After the script completes, open your browser and go to `http://localhost:8069`. You will be prompted to configure the master password, database name, and other settings for your Odoo instance.

## Verifying the Installation
To check the status of the Odoo service, use:

```bash
sudo systemctl status odoo
```

## Troubleshooting
For any errors, check the Odoo log file at `/var/log/odoo/odoo.log` for more details.

## License
This project is licensed under the MIT License.

---

You can find more information and support on my GitHub page: [darky404](https://github.com/darky404/odoo).
