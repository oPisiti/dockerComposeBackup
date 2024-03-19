# Docker compose backup solution

This tool finds all the docker-compose.yml fiels inside a specified directory.

It then creates an archive containing all of them, while keeping the subdirectories structure. Encryption is supported.

## Customization and encryption

Inside the main function, the first few lines are meant to be changed by the user.

Please change accordingly, ESPECIALLY: 

- `docker_files_dir`
- `output_dir`
- `encrypt`

If `encrypt` is set to True, a password will be prompted twice, so this option is not ideal for automatic backups

## Example

Say your containers' files are inside ~/docker-Containers/ and the structure is simmilar to:

```
├── Caddy
│   ├── Caddyfile
│   ├── docker-compose.yml
│   ├── docker-compose.yml.bak
│   └── template.env
├── Syncthing
│   ├── config
│   └── docker-compose.yml
├── Vaultwarden
│   ├── docker-compose.yml
│   └── vw-data
├── Wireguard
│   ├── config
│   └── docker-compose.yml
```

Then, a file ~/docker-compose-archive.tar.7z will be created with the following structure:

```
├── Caddy
│   ├── docker-compose.yml
├── Syncthing
│   └── docker-compose.yml
├── Vaultwarden
│   ├── docker-compose.yml
├── Wireguard
│   └── docker-compose.yml
```
