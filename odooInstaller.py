import os
import subprocess

# Configuraciones de instalación
odoo_user = "odoo"
odoo_password = "Qwerty123@"  # Contraseña de usuario de Odoo
db_user = "odoo_db_user"
db_password = "Qwerty123@"  # Contraseña de usuario de base de datos

def run_command(command):
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    if result.returncode != 0:
        print(f"Error ejecutando: {command}\n{result.stderr}")
    else:
        print(f"Comando ejecutado correctamente: {command}")

# Actualización de repositorios
def update_repos():
    print("Actualizando repositorios...")
    run_command("sudo apt update && sudo apt upgrade -y")

# Instalación de dependencias de Odoo
def install_dependencies():
    print("Instalando dependencias necesarias para Odoo...")
    dependencies = [
        "git", "python3", "python3-dev", "python3-pip", "build-essential",
        "wget", "python3-venv", "libxslt-dev", "libzip-dev", "libldap2-dev",
        "libsasl2-dev", "nodejs", "npm", "libjpeg-dev", "libpq-dev", 
        "libffi-dev", "libssl-dev", "postgresql", "postgresql-contrib"
    ]
    run_command("sudo apt install -y " + " ".join(dependencies))

# Instalación de wkhtmltopdf para generación de PDF
def install_wkhtmltopdf():
    print("Instalando wkhtmltopdf para generación de PDF...")
    # Descarga la versión compatible de wkhtmltopdf
    run_command("wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-2/wkhtmltox_0.12.6.1-2.jammy_amd64.deb -P /tmp")
    # Instala el paquete
    run_command("sudo apt install -y /tmp/wkhtmltox_0.12.6.1-2.jammy_amd64.deb")

# Configuración de PostgreSQL
def setup_postgresql():
    print("Instalando y configurando PostgreSQL...")
    run_command("sudo systemctl enable postgresql")
    run_command("sudo systemctl start postgresql")
    run_command(f"sudo -u postgres createuser -s {db_user}")
    run_command(f"sudo -u postgres psql -c \"ALTER USER {db_user} WITH PASSWORD '{db_password}';\"")

    # Configuración de autenticación md5
    with open("/etc/postgresql/14/main/pg_hba.conf", "a") as pg_hba:
        pg_hba.write(f"local   all             {db_user}                                md5\n")
    run_command("sudo systemctl restart postgresql")

# Creación de usuario de sistema para Odoo
def create_odoo_user():
    print("Creando usuario de sistema para Odoo...")
    run_command(f"sudo adduser --system --home=/opt/{odoo_user} --group {odoo_user}")
    run_command(f"sudo mkdir /var/log/{odoo_user}")
    run_command(f"sudo chown {odoo_user}:{odoo_user} /var/log/{odoo_user}")

# Descarga de Odoo Community
def download_odoo():
    print("Descargando Odoo 17 Community...")
    run_command(f"sudo git clone --depth 1 --branch 17.0 https://github.com/odoo/odoo /opt/{odoo_user}")

# Configuración de ambiente virtual y dependencias Python
def setup_virtualenv():
    print("Configurando ambiente virtual y dependencias de Python...")
    run_command(f"sudo python3 -m venv /opt/{odoo_user}/venv")
    run_command(f"sudo chown -R {odoo_user}:{odoo_user} /opt/{odoo_user}/venv")
    # Utiliza directamente el pip del entorno virtual para instalar dependencias
    run_command(f"/opt/{odoo_user}/venv/bin/pip install -r /opt/{odoo_user}/requirements.txt --break-system-packages")

# Configuración de Odoo
def setup_odoo_config():
    print("Configurando archivo de configuración de Odoo...")
    odoo_config = f"""
[options]
db_host = False
db_port = False
db_user = {db_user}
db_password = {db_password}
addons_path = /opt/{odoo_user}/addons
data_dir = /opt/{odoo_user}/.local/share/Odoo
"""
    with open(f"/etc/{odoo_user}.conf", "w") as config_file:
        config_file.write(odoo_config)
    run_command(f"sudo chown {odoo_user}:{odoo_user} /etc/{odoo_user}.conf")
    run_command(f"sudo chmod 640 /etc/{odoo_user}.conf")

# Configuración del servicio de Odoo
def setup_odoo_service():
    print("Configurando el servicio de Odoo...")
    odoo_service = f"""
[Unit]
Description=Odoo
Documentation=http://www.odoo.com
[Service]
User={odoo_user}
Group={odoo_user}
ExecStart=/opt/{odoo_user}/venv/bin/python3 /opt/{odoo_user}/odoo-bin -c /etc/{odoo_user}.conf
[Install]
WantedBy=multi-user.target
"""
    with open(f"/etc/systemd/system/{odoo_user}.service", "w") as service_file:
        service_file.write(odoo_service)
    run_command("sudo systemctl daemon-reload")
    run_command(f"sudo systemctl enable {odoo_user}.service")
    run_command(f"sudo systemctl start {odoo_user}.service")

def main():
    update_repos()
    install_dependencies()
    install_wkhtmltopdf()
    setup_postgresql()
    create_odoo_user()
    download_odoo()
    setup_virtualenv()
    setup_odoo_config()
    setup_odoo_service()
    print("Instalación completa. Odoo está corriendo en el servidor.")

if __name__ == "__main__":
    main()

