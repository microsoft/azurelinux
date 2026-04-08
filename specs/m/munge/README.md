# MUNGE

The munge package.

MUNGE (**M**UNGE **U**id '**N**' **G**id **E**mporium) is an authentication service for creating and validating credentials.

A secret key must be created before starting the service for the first time. This can be done with the following command:

```bash
sudo -u munge /usr/sbin/mungekey -v
```

Please read `man 8 mungekey` for more information.
In the second step you can start and enable the munge service.

```bash
systemctl start munge
systemctl enable munge
```
