import pulumi
from pulumi import Config
from components.ssh_key import SshKey

# Read the configuration
config = Config()

# Retrieve the ssh_keys
ssh_keys = config.get_object("ssh_keys")

# Create the SSH keys using the SshKey component
if ssh_keys:
    for key_name, public_key in ssh_keys.items():
        SshKey(key_name, public_key)
