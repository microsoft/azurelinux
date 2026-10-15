import hashlib
import os
import re

# Apply once from the architecture config after channel-specific root selection.
config_dir = os.path.dirname(os.path.realpath(config_opts['config_file']))
include_dir = os.path.realpath(config_opts['config_path'])
if config_dir != include_dir:
    raise ValueError(
        'Selected mock configuration directory must match --configdir: '
        f'{config_dir!r} != {include_dir!r}'
    )

config_dir_id = hashlib.sha256(os.fsencode(config_dir)).hexdigest()[:12]
# Keep the end of long paths so the worktree and configuration remain readable.
config_dir_label = re.sub(r'[^A-Za-z0-9._-]+', '-', config_dir).strip('-')
config_dir_label = config_dir_label[-120:].lstrip('-') or 'config'
config_opts['root'] = (
    f"{config_opts['root']}-v2-{config_dir_label}-{config_dir_id}"
)
