#!/usr/bin/python
import sublime, sublime_plugin
import os, re

class ShebangSyntaxListener(sublime_plugin.EventListener):
    def on_load(self, view):
        view.run_command('shebang_syntax')

    def on_post_save(self, view):
        view.run_command('shebang_syntax')

class ShebangSyntaxCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # Only operate on files with no file extension (i.e. no dots)
        if not os.path.basename(self.view.file_name()).find('.'):
            return

        # Grab the first line's contents
        line = self.view.substr(self.view.full_line(1))

        # Get the current syntax type
        current_syntax = self.view.settings().get('syntax')

        # Get the shebang components
        m = re.match(r"#!\s*([^\s]+)\s*([^\s]+)?", line)

        if not m:
            return

        # Split the path component
        bits = m.group(1).split('/')

        # If the path component is 'env' then use the second regex group
        new_raw_syntax = m.group(2) if bits[-1] == 'env' else bits[-1]

        # Create syntax file path
        syntax_path = sublime.packages_path() + os.path.sep + \
            '%(dir)s' + os.path.sep + '%(file)s.tmLanguage'

        # Does this shebang match a capitalised version?
        cap_syntax_path = syntax_path % {'dir': new_raw_syntax.capitalize(), \
            'file': new_raw_syntax.capitalize()}

        if os.path.exists(cap_syntax_path):
            if current_syntax != cap_syntax_path:
                self.view.set_syntax_file(cap_syntax_path)
        else:
            # No, so we compare it against the settings file
            settings = sublime.load_settings('ShebangSyntax.sublime-settings')

            # Check for a match
            new_syntax_name = settings.get(new_raw_syntax)

            if new_syntax_name:
                # Special case as the file can sometimes be unchanged
                if len(new_syntax_name) == 1:
                    syntax_filename = new_syntax_name[0]
                else:
                    syntax_filename = new_syntax_name[1]

                new_syntax_path = syntax_path % {'dir': new_syntax_name[0], \
                   'file': syntax_filename}

                if not os.path.exists(new_syntax_path):
                    return

                if current_syntax != new_syntax_path:
                    self.view.set_syntax_file(new_syntax_path)