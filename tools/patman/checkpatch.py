from patman import tools
def CheckPatch(fname, verbose=False, show_types=False):
    """Run checkpatch.pl on a file.
        fname: Filename to check
        show_types: Tell checkpatch to show the type (number) of each message
            stdout: Full output of checkpatch
    chk = FindCheckPatch()
    item = {}
    args = [chk, '--no-tree']
    if show_types:
        args.append('--show-types')
    result.stdout = command.Output(*args, fname, raise_on_error=False)
    #pipe = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    #stdout, stderr = pipe.communicate()
    emacs_prefix = '(?:[0-9]{4}.*\.patch:[0-9]+: )?'
    emacs_stats = '(?:[0-9]{4}.*\.patch )?'
                          'total: (\\d+) errors, (\d+) warnings, (\d+)')
                               'total: (\\d+) errors, (\d+) warnings, (\d+)'
                               ' checks, (\d+)')
    re_ok = re.compile('.*has no obvious style problems')
    re_bad = re.compile('.*has style problems, please review')
    type_name = '([A-Z_]+:)?'
    re_error = re.compile('ERROR:%s (.*)' % type_name)
    re_warning = re.compile(emacs_prefix + 'WARNING:%s (.*)' % type_name)
    re_check = re.compile('CHECK:%s (.*)' % type_name)
    re_file = re.compile('#(\d+): (FILE: ([^:]*):(\d+):)?')
    re_note = re.compile('NOTE: (.*)')
    re_new_file = re.compile('new file mode .*')
    indent = ' ' * 6
    for line in result.stdout.splitlines():
            print(line)

        # A blank line indicates the end of a message
        if not line:
            if item:
                result.problems.append(item)
                item = {}
            continue
        if re_note.match(line):
            continue
        # Skip lines which quote code
        if line.startswith(indent):
            continue
        # Skip code quotes
        if line.startswith('+'):
            continue
        if re_new_file.match(line):
            continue
        match = re_stats_full.match(line)
            match = re_stats.match(line)
            continue
        elif re_ok.match(line):
            continue
        elif re_bad.match(line):
            continue
        err_match = re_error.match(line)
        warn_match = re_warning.match(line)
        file_match = re_file.match(line)
        check_match = re_check.match(line)
        subject_match = line.startswith('Subject:')
        if err_match:
            item['cptype'] = err_match.group(1)
            item['msg'] = err_match.group(2)
            item['type'] = 'error'
        elif warn_match:
            item['cptype'] = warn_match.group(1)
            item['msg'] = warn_match.group(2)
            item['type'] = 'warning'
        elif check_match:
            item['cptype'] = check_match.group(1)
            item['msg'] = check_match.group(2)
            item['type'] = 'check'
        elif file_match:
            err_fname = file_match.group(3)
            if err_fname:
                item['file'] = err_fname
                item['line'] = int(file_match.group(4))
            else:
                item['file'] = '<patch>'
                item['line'] = int(file_match.group(1))
        elif subject_match:
            item['file'] = '<patch subject>'
            item['line'] = None
            print('bad line "%s", %d' % (line, len(line)))