ShebangSyntax - a Sublime Text 2 plugin to set a file's syntax based upon a
shebang line (#!/path/to/something).

This plugin doesn't try to be too clever - it only operates on files without
an extension (that is, without a dot (i.e. a _period_) anywhere in the file name.
Anything with a file extension is probably best left to Sublime and other
plugins.

Next, the first line is checked to see if it contains a shebang (`#!`). If it
does, the path is matched along with an optional second group (after one or
more spaces). This allows the plugin to work with `/usr/bin/env ruby` without
thinking that _env_ is the syntax type.

Once the plugin has figured out what the syntax type is (i.e. _ruby_, _php_,
etc), it does a simple uppercase check to see if there's a match in the
_Packages_ directory. So for example, _ruby_ would be checked against
_Packages/Ruby/Ruby.tmLanguage_.

If there's no match (as in the case of _PHP_, due to all-capitals), then the
plugin refers to its _ShebangSyntax.sublime-settings_ file. You should make
your own copy of this file and add any additional associations.

You'll notice that in this file values are set as lists - this is because some
syntax types have differing directory and file names. More information on this
can be found within the settings file, and it's pretty self-explanatory.
