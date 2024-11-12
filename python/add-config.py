import netmiko

def configure_switch(device, commands):
    """Connects to a Cisco switch and executes a list of commands."""

    try:
        with netmiko.ConnectHandler(**device) as ssh_conn:
            ssh_conn.enable()
            output = ssh_conn.send_config_set(commands)
            print(output)
    except netmiko.NetmikoTimeoutException:
        print(f"Timeout connecting to device: {device['host']}")
    except netmiko.NetmikoAuthenticationException:
        print(f"Authentication failure: {device['host']}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":

    devices = [
        {
            "device_type": "cisco_ios",
            "host": "192.168.1.1",
            "username": "admin",
            "password": "password",
            "secret": "password"  # Enable password if needed
        },
        # Add more devices as needed
    ]

    commands = [
        "interface vlan 1",
        "ip address 192.168.1.254 255.255.255.0",
        "no shutdown"
    ]

    for device in devices:
        configure_switch(device, commands)