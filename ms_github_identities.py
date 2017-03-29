"""Demo of mapping GitHub and Microsoft identities. Uses files in the /data
subfolder as data sources. Those files are populated from data retrieved via the
GitHub API, from Azure blob storage, or internal databases."""

class _settings:
    """Namespace for global settings.
    """
    alias_manager = None
    email_alias = None
    linkdata = None

def load_dictionary(datafile):
    """Return a dictionary created from the specified CSV file."""
    dictionary = dict()
    for line in open(datafile, 'r').readlines():
        key, value = line.strip().split(',')
        dictionary[key.lower()] = value.lower()
    return dictionary

def microsoft_vp(alias):
    """Return the alias of Satya's direct for a specified Microsoft alias.
    """
    if not _settings.alias_manager:
        _settings.alias_manager = load_dictionary('data/aliasManager.csv')

    current = alias # current person as we move up the mgmt chain
    while current:
        mgr = _settings.alias_manager[current]
        if mgr == 'satyan':
            break # this person reports to Satya, so we're done
        current = mgr # move up to the next manager

    return current

def microsoft_alias(email):
    """Return Microsoft alias for an email address."""
    if not _settings.email_alias:
        _settings.email_alias = load_dictionary('data/emailAlias.csv')
    return _settings.email_alias.get(email, '')

def microsoft_email(github_user):
    """Return Microsoft email address linked to a GitHub account."""
    if not _settings.linkdata:
        _settings.linkdata = load_dictionary('data/linkdata.csv')
    return _settings.linkdata.get(github_user.lower(), '')

if __name__ == '__main__':
    print(' -> '.join(['GitHub username', 'email address', 'MS alias',
                       'MS Exec VP']))
    for github_alias in ['meganbradley', 'dmahugh']:
        ms_email = microsoft_email(github_alias)
        ms_alias = microsoft_alias(ms_email)
        execvp = microsoft_vp(ms_alias)
        print(' -> '.join([github_alias, ms_email, ms_alias, execvp]))
