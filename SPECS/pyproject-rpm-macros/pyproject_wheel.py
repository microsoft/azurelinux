import argparse
import sys
import subprocess


def parse_config_settings_args(config_settings):
    """
    Given a list of config `KEY=VALUE` formatted config settings,
    return a dictionary that can be passed to PEP 517 hook functions.
    """
    if not config_settings:
        return config_settings
    new_config_settings = {}
    for arg in config_settings:
        key, _, value = arg.partition('=')
        if key in new_config_settings:
            if not isinstance(new_config_settings[key], list):
                # convert the existing value to a list
                new_config_settings[key] = [new_config_settings[key]]
            new_config_settings[key].append(value)
        else:
            new_config_settings[key] = value
    return new_config_settings


def get_config_settings_args(config_settings):
    """
    Given a dictionary of PEP 517 backend config_settings,
    yield --config-settings args that can be passed to pip's CLI
    """
    if not config_settings:
        return
    for key, values in config_settings.items():
        if not isinstance(values, list):
            values = [values]
        for value in values:
            if value == '':
                yield f'--config-settings={key}'
            else:
                yield f'--config-settings={key}={value}'


def build_wheel(*, wheeldir, stdout=None, config_settings=None):
    command = (
        sys.executable,
        '-m', 'pip',
        'wheel',
        '--wheel-dir', wheeldir,
        '--no-deps',
        '--use-pep517',
        '--no-build-isolation',
        '--disable-pip-version-check',
        '--no-clean',
        '--progress-bar', 'off',
        '--verbose',
        *get_config_settings_args(config_settings),
        '.',
    )
    cp = subprocess.run(command, stdout=stdout)
    return cp.returncode


def parse_args(argv=None):
    parser = argparse.ArgumentParser(prog='%pyproject_wheel')
    parser.add_argument('wheeldir', help=argparse.SUPPRESS)
    parser.add_argument(
        '-C',
        dest='config_settings',
        action='append',
        help='Configuration settings to pass to the PEP 517 backend',
    )
    args = parser.parse_args(argv)
    args.config_settings = parse_config_settings_args(args.config_settings)
    return args


if __name__ == '__main__':
    sys.exit(build_wheel(**vars(parse_args())))
