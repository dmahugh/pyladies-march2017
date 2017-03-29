"""azhelp.py

Capture azure-cli help output and recursively crawl all help commands for
subgroups. The nested hierarchy of help commands is printed to console.
"""
import subprocess
import sys

def getcommands(helpcmd):
    """Recursively crawl all subgroups, starting from specified help command.
    Passed command assumed to end with -h. For example, 'az vm -h'
    """
    indentation = 4 * (len(helpcmd.split(' ')) - 3)
    print(indentation*' ' + helpcmd)

    stdoutdata = subprocess.getoutput(helpcmd) # capture help command output
    subgroups = False # flag to track whether inside the subgroup section
    for line in stdoutdata.split('\n'):

        if line.strip() == 'Subgroups:':
            subgroups = True # found start of subgroup section
            continue # skip the 'Subgroups:' line
        if not subgroups:
            continue # skip all lines before subgroup section
        if subgroups and (not line.strip() or line.lstrip() == line):
            break # blank or non-indented line is end of subgroup section

        subhelp = subcommand(helpcmd, line) # create help command for subgroup
        getcommands(subhelp) # enumerate help commands for this subgroup

def subcommand(helpcmd, line):
    """Return a help command for a subgroup.

    helpcmd = an Azure CLI help command (e.g., 'az vm -h')
    line = line of text beginning with a subgroup
        (e.g., 'create        : Create an Azure Virtual Machine.')

    Returns the command for getting help on this subgroup
    (e.g., 'az vm create -h')
    """
    # sometimes need to remove trailing ':'
    subgroup = line.strip().split(' ')[0].rstrip(':')

    # create list of arguments before the -h
    rootcommand = helpcmd.split(' ')[:-1]

    # add this subgroup and -h
    rootcommand.extend([subgroup, '-h'])

    return ' '.join(rootcommand) # re-assemble into a help command string

if __name__ == '__main__':
    if len(sys.argv) == 2:
        # a help command was passed on command line, so use that
        getcommands(sys.argv[1])
    else:
        # default: start at top-level help command for Azure CLI
        getcommands('az -h')
