# Copyright 2017 Endless Mobile, Inc.

import os
import sys

here = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(here, '..', 'flapjack'))

from flapjack import commands

BASH_COMPLETION_TEMPLATE = os.path.join(here, "bash-completion.in")
BASH_COMPLETION_FILE = os.path.join(here, '..', 'dist', "flapjack.bash-completion")

def get_command_vars():
    all_commands = commands._command_registry.keys()
    commands_requiring_module = []
    commands_requiring_app = []
    other_commands = []
    for name in all_commands:
        command = commands.get_command(name)
        action_dests = []
        for action in command.parser._actions:
            action_dests.append(action.dest)

        if 'module' in action_dests:
            commands_requiring_module.append(name)
        elif 'app' in action_dests:
            commands_requiring_app.append(name)
        else:
            other_commands.append(name)

    return {
        'SUBCOMMANDS': ' '.join(all_commands),
        'SUBCOMMANDS_MODULE_MATCH': '|'.join(commands_requiring_module),
        'SUBCOMMANDS_APPS_MATCH': '|'.join(commands_requiring_app),
        'SUBCOMMANDS_OTHER_MATCH': '|'.join(other_commands),
    }

def fill_template(template_vars):
    with open(BASH_COMPLETION_TEMPLATE) as template:
        script_text = template.read()
        for var_name, value in template_vars.items():
            script_text = script_text.replace('%%' + var_name + '%%', value, 1)
        return script_text

def write_script(script_text):
    dirname = os.path.dirname(BASH_COMPLETION_FILE)
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    with open(BASH_COMPLETION_FILE, 'w') as script_file:
        script_file.write(script_text)

template_vars = get_command_vars()
script_text = fill_template(template_vars)
write_script(script_text)
