# pylint
# Autogenerated from man page /usr/share/man/man1/pylint.1.gz
complete -c pylint -l version --description 'show program\'s version number and exit.'
complete -c pylint -l help -s h --description 'show this help message and exit.'
complete -c pylint -l long-help --description 'more verbose help.'
complete -c pylint -l init-hook --description 'Python code to execute, usually for sys. path manipulation such as pygtk.'
complete -c pylint -l errors-only -s E --description 'In error mode, checkers without error messages are disabled and for others, o…'
complete -c pylint -l py3k --description 'In Python 3 porting mode, all checkers will be disabled and only messages emi…'
complete -c pylint -l verbose -s v --description 'In verbose mode, extra non-checker-related info will be displayed.'
complete -c pylint -l ignore --description 'Add files or directories to the blacklist.'
complete -c pylint -l ignore-patterns --description 'Add files or directories matching the regex patterns to the blacklist.'
complete -c pylint -l persistent --description 'Pickle collected data for later comparisons.  [default: yes].'
complete -c pylint -l load-plugins --description 'List of plugins (as comma separated values of python module names) to load, u…'
complete -c pylint -l fail-under --description 'Specify a score threshold to be exceeded before program exits with error.'
complete -c pylint -l jobs -s j --description 'Use multiple processes to speed up Pylint.'
complete -c pylint -l limit-inference-results --description 'Control the amount of potential inferred values when inferring a single objec…'
complete -c pylint -l extension-pkg-whitelist --description 'A comma-separated list of package or module names from where C extensions may…'
complete -c pylint -l suggestion-mode --description 'When enabled, pylint would attempt to guess common misconfiguration and emit …'
complete -c pylint -l exit-zero --description 'Always return a 0 (non-error) status code, even if lint errors are found.'
complete -c pylint -l from-stdin --description 'Interpret the stdin as a python script, whose filename needs to be passed as …'
complete -c pylint -l rcfile --description 'Specify a configuration file to load.'
complete -c pylint -l help-msg --description 'Display a help message for the given message id and exit.'
complete -c pylint -l list-msgs --description 'Generate pylint\'s messages.'
complete -c pylint -l list-msgs-enabled --description 'Display a list of what messages are enabled and disabled with the given confi…'
complete -c pylint -l list-groups --description 'List pylint\'s message groups.'
complete -c pylint -l list-conf-levels --description 'Generate pylint\'s confidence levels.'
complete -c pylint -l full-documentation --description 'Generate pylint\'s full documentation.'
complete -c pylint -l generate-rcfile --description 'Generate a sample configuration file according to the current configuration.'
complete -c pylint -l confidence --description 'Only show warnings with the listed confidence levels.'
complete -c pylint -l enable -s e --description 'Enable the message, report, category or checker with the given id(s).'
complete -c pylint -l disable -s d --description 'Disable the message, report, category or checker with the given id(s).'
complete -c pylint -l output-format -s f --description 'Set the output format.'
complete -c pylint -l reports -s r --description 'Tells whether to display a full report or only the messages.  [default: no].'
complete -c pylint -l evaluation --description 'Python expression which should return a score less than or equal to 10.'
complete -c pylint -l score -s s --description 'Activate the evaluation score.  [default: yes].'
complete -c pylint -l msg-template --description 'Template used to display messages.'
complete -c pylint -l logging-modules --description 'Logging modules to check that the string format arguments are in logging func…'
complete -c pylint -l logging-format-style --description 'Format style used to check logging format string.'
complete -c pylint -l spelling-dict --description 'Spelling dictionary name.  Available dictionaries: none.'
complete -c pylint -l spelling-ignore-words --description 'List of comma separated words that should not be checked.  [default: none].'
complete -c pylint -l spelling-private-dict-file --description 'A path to a file that contains the private dictionary; one word per line.'
complete -c pylint -l spelling-store-unknown-words --description 'Tells whether to store unknown words to the private dictionary (see the --spe…'
complete -c pylint -l max-spelling-suggestions --description 'Limits count of emitted suggestions for spelling mistakes.  [default: 4].'
complete -c pylint -l notes --description 'List of note tags to take in consideration, separated by a comma.'
complete -c pylint -l notes-rgx --description 'Regular expression of note tags to take in consideration.'
complete -c pylint -l ignore-on-opaque-inference --description 'This flag controls whether pylint should warn about no-member and similar che…'
complete -c pylint -l ignore-mixin-members --description 'Tells whether missing members accessed in mixin class should be ignored.'
complete -c pylint -l ignore-none --description 'Tells whether to warn about missing members when the owner of the attribute i…'
complete -c pylint -l ignored-modules --description 'List of module names for which member attributes should not be checked (usefu…'
complete -c pylint -l ignored-classes --description 'List of class names for which member attributes should not be checked (useful…'
complete -c pylint -l generated-members --description 'List of members which are set dynamically and missed by pylint inference syst…'
complete -c pylint -l contextmanager-decorators --description 'List of decorators that produce context managers, such as contextlib.'
complete -c pylint -l missing-member-hint-distance --description 'The minimum edit distance a name should have in order to be considered a simi…'
complete -c pylint -l missing-member-max-choices --description 'The total number of similar names that should be taken in consideration when …'
complete -c pylint -l missing-member-hint --description 'Show a hint with possible names when a member name was not found.'
complete -c pylint -l signature-mutators --description 'List of decorators that change the signature of a decorated function.'
complete -c pylint -l init-import --description 'Tells whether we should check for unused import in __init__ files.'
complete -c pylint -l dummy-variables-rgx --description 'A regular expression matching the name of dummy variables (i. e.'
complete -c pylint -l additional-builtins --description 'List of additional names supposed to be defined in builtins.'
complete -c pylint -l callbacks --description 'List of strings which can identify a callback function by name.'
complete -c pylint -l redefining-builtins-modules --description 'List of qualified module names which can have objects that can redefine built…'
complete -c pylint -l ignored-argument-names --description 'Argument names that match this expression will be ignored.'
complete -c pylint -l allow-global-unused-variables --description 'Tells whether unused global variables should be treated as a violation.'
complete -c pylint -l max-nested-blocks --description 'Maximum number of nested blocks for function / method body [default: 5].'
complete -c pylint -l never-returning-functions --description 'Complete name of functions that never returns.'
complete -c pylint -l max-line-length --description 'Maximum number of characters on a single line.  [default: 100].'
complete -c pylint -l ignore-long-lines --description 'Regexp for a line that is allowed to be longer than the limit.'
complete -c pylint -l single-line-if-stmt --description 'Allow the body of an if to be on the same line as the test if there is no els…'
complete -c pylint -l single-line-class-stmt --description 'Allow the body of a class to be on the same line as the declaration if body c…'
complete -c pylint -l no-space-check --description 'List of optional constructs for which whitespace checking is disabled.'
complete -c pylint -l max-module-lines --description 'Maximum number of lines in a module.  [default: 1000].'
complete -c pylint -l indent-string --description 'String used as indentation unit.'
complete -c pylint -l indent-after-paren --description 'Number of spaces of indent required inside a hanging or continued line.'
complete -c pylint -l expected-line-ending-format --description 'Expected format of line ending, e. g.  empty (any line ending), LF or CRLF.'
complete -c pylint -l deprecated-modules --description 'Deprecated modules which should not be used, separated by a comma.'
complete -c pylint -l preferred-modules --description 'Couples of modules and preferred modules, separated by a comma.'
complete -c pylint -l import-graph --description 'Create a graph of every (i. e.'
complete -c pylint -l ext-import-graph --description 'Create a graph of external dependencies in the given file (report RP0402 must…'
complete -c pylint -l int-import-graph --description 'Create a graph of internal dependencies in the given file (report RP0402 must…'
complete -c pylint -l known-standard-library --description 'Force import order to recognize a module as part of the standard compatibilit…'
complete -c pylint -l known-third-party --description 'Force import order to recognize a module as part of a third party library.'
complete -c pylint -l allow-any-import-level --description 'List of modules that can be imported at any level, not just the top level one.'
complete -c pylint -l analyse-fallback-blocks --description 'Analyse import fallback blocks.'
complete -c pylint -l allow-wildcard-with-all --description 'Allow wildcard imports from modules that define __all__.  [default: no].'
complete -c pylint -l overgeneral-exceptions --description 'Exceptions that will emit a warning when being caught.'
complete -c pylint -l defining-attr-methods --description 'List of method names used to declare (i. e.  assign) instance attributes.'
complete -c pylint -l valid-classmethod-first-arg --description 'List of valid names for the first argument in a class method.  [default: cls].'
complete -c pylint -l valid-metaclass-classmethod-first-arg --description 'List of valid names for the first argument in a metaclass class method.'
complete -c pylint -l exclude-protected --description 'List of member names, which should be excluded from the protected access warn…'
complete -c pylint -l min-similarity-lines --description 'Minimum lines number of a similarity.  [default: 4].'
complete -c pylint -l ignore-comments --description 'Ignore comments when computing similarities.  [default: yes].'
complete -c pylint -l ignore-docstrings --description 'Ignore docstrings when computing similarities.  [default: yes].'
complete -c pylint -l ignore-imports --description 'Ignore imports when computing similarities.  [default: no].'
complete -c pylint -l max-args --description 'Maximum number of arguments for function / method.  [default: 5].'
complete -c pylint -l max-locals --description 'Maximum number of locals for function / method body.  [default: 15].'
complete -c pylint -l max-returns --description 'Maximum number of return / yield for function / method body.  [default: 6].'
complete -c pylint -l max-branches --description 'Maximum number of branch for function / method body.  [default: 12].'
complete -c pylint -l max-statements --description 'Maximum number of statements in function / method body.  [default: 50].'
complete -c pylint -l max-parents --description 'Maximum number of parents for a class (see R0901).  [default: 7].'
complete -c pylint -l max-attributes --description 'Maximum number of attributes for a class (see R0902).  [default: 7].'
complete -c pylint -l min-public-methods --description 'Minimum number of public methods for a class (see R0903).  [default: 2].'
complete -c pylint -l max-public-methods --description 'Maximum number of public methods for a class (see R0904).  [default: 20].'
complete -c pylint -l max-bool-expr --description 'Maximum number of boolean expressions in an if statement (see R0916).'
complete -c pylint -l good-names --description 'Good variable names which should always be accepted, separated by a comma.'
complete -c pylint -l good-names-rgxs --description 'Good variable names regexes, separated by a comma.'
complete -c pylint -l bad-names --description 'Bad variable names which should always be refused, separated by a comma.'
complete -c pylint -l bad-names-rgxs --description 'Bad variable names regexes, separated by a comma.'
complete -c pylint -l name-group --description 'Colon-delimited sets of names that determine each other\'s naming style when t…'
complete -c pylint -l include-naming-hint --description 'Include a hint for the correct naming format with invalid-name.'
complete -c pylint -l property-classes --description 'List of decorators that produce properties, such as abc. abstractproperty.'
complete -c pylint -l argument-naming-style --description 'Naming style matching correct argument names.  [default: snake_case].'
complete -c pylint -l argument-rgx --description 'Regular expression matching correct argument names.'
complete -c pylint -l attr-naming-style --description 'Naming style matching correct attribute names.  [default: snake_case].'
complete -c pylint -l attr-rgx --description 'Regular expression matching correct attribute names.'
complete -c pylint -l class-naming-style --description 'Naming style matching correct class names.  [default: PascalCase].'
complete -c pylint -l class-rgx --description 'Regular expression matching correct class names.'
complete -c pylint -l class-attribute-naming-style --description 'Naming style matching correct class attribute names.  [default: any].'
complete -c pylint -l class-attribute-rgx --description 'Regular expression matching correct class attribute names.'
complete -c pylint -l const-naming-style --description 'Naming style matching correct constant names.  [default: UPPER_CASE].'
complete -c pylint -l const-rgx --description 'Regular expression matching correct constant names.'
complete -c pylint -l function-naming-style --description 'Naming style matching correct function names.  [default: snake_case].'
complete -c pylint -l function-rgx --description 'Regular expression matching correct function names.'
complete -c pylint -l inlinevar-naming-style --description 'Naming style matching correct inline iteration names.  [default: any].'
complete -c pylint -l inlinevar-rgx --description 'Regular expression matching correct inline iteration names.'
complete -c pylint -l method-naming-style --description 'Naming style matching correct method names.  [default: snake_case].'
complete -c pylint -l method-rgx --description 'Regular expression matching correct method names.'
complete -c pylint -l module-naming-style --description 'Naming style matching correct module names.  [default: snake_case].'
complete -c pylint -l module-rgx --description 'Regular expression matching correct module names.'
complete -c pylint -l variable-naming-style --description 'Naming style matching correct variable names.  [default: snake_case].'
complete -c pylint -l variable-rgx --description 'Regular expression matching correct variable names.'
complete -c pylint -l no-docstring-rgx --description 'Regular expression which should only match function or class names that do no…'
complete -c pylint -l docstring-min-length --description 'Minimum line length for functions/classes that require docstrings, shorter on…'
complete -c pylint -l check-str-concat-over-line-jumps --description 'This flag controls whether the implicit-str-concat should generate a warning …'
complete -c pylint -l check-quote-consistency --description 'This flag controls whether inconsistent-quotes generates a warning when the c…'
