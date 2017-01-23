import textwrap


__all__ = ["format_h1", "format_h2", "fmt_error", "print_error", "menu", "format_progress", "markdown_table",
           "print_skipped", "format_exe_info", "format_box"]


NIND = 2  # Number of spaces per indentation level

# #################################################################################################
# # Text interface routines - routines that are useful for building a text interface


def format_underline(s, char="=", indents=0):
    """
    Traces a dashed line below string

    Args:
        s: string
        intents: number of leading intenting spaces
        format: string starting with "text" or "markdown"

    Returns: list

    >>> print("\\n".join(format_underline("Life of João da Silva", "^", 2)))
      Life of João da Silva
      ^^^^^^^^^^^^^^^^^^^^^
    """

    n = len(s)
    ind = " " * indents
    return ["{}{}".format(ind, s), "{}{}".format(ind, char*n)]


def format_h1(s, format="text", indents=0):
    """
    Encloses string in format text

    Args:
        s: string
        intents: number of leading intenting spaces
        format: string starting with "text" or "markdown"

    Returns: list

    >>> print("\\n".join(format_h2("Header 1", indents=10)))
              Header 1
              --------

    >>> print("\\n".join(format_h2("Header 1", "markdown", 0)))
    ## Header 1
    """

    if format.startswith("text"):
        return format_underline(s, "=", indents)
    elif format.startswith("markdown"):
        return ["# {}".format(s)]


def format_h2(s, format="text", indents=0):
    """
    Encloses string in format text

    Args:
        s: string
        format: string starting with "text" or "markdown"
        intents: number of leading intenting spaces

    Returns: list

    >>> print("\\n".join(format_h2("Header 2", indents=2)))
      Header 2
      --------

    >>> print("\\n".join(format_h2("Header 2", "markdown", 2)))
    ## Header 2
    """

    if format.startswith("text"):
        return format_underline(s, "-", indents)
    elif format.startswith("markdown"):
        return ["## {}".format(s)]



def fmt_error(s):
    """Standardized embellishment. Adds formatting to error message."""
    return "!! {0!s} !!".format(s)


def print_error(s):
    """Prints string as error message."""
    print((fmt_error(s)))


def menu(title, options, cancel_label="Cancel", flag_allow_empty=False, flag_cancel=True, ch='.'):
  """Text menu.

  Arguments:
    title -- menu title, to appear at the top
    options -- sequence of strings
    cancel_label='Cancel' -- label to show at last "zero" option
    flag_allow_empty=0 -- Whether to allow empty option
    flag_cancel=True -- whether there is a "0 - Cancel" option
    ch="." -- character to use to draw frame around title

  Returns:
    option -- an integer: None; 0-Back/Cancel/etc; 1, 2, ...

  Adapted from irootlab menu.m"""

  num_options, flag_ok = len(options), 0
  option = None  # result
  min_allowed = 0 if flag_cancel else 1  # minimum option value allowed (if option not empty)

  while True:
    print("")
    for line in format_box(title, ch):
        print("  "+line)
    for i, s in enumerate(options):
      print(("  {0:d} - {1!s}".format(i+1, s)))
    if flag_cancel: print(("  0 - << (*{0!s}*)".format(cancel_label)))
    try:
        s_option = input('? ')
    except KeyboardInterrupt:
        raise
    except:
        print("")

    n_try = 0
    while True:
      if n_try >= 10:
        print('You are messing up!')
        break

      if len(s_option) == 0 and flag_allow_empty:
        flag_ok = True
        break

      try:
        option = int(s_option)
        if min_allowed <= option <= num_options:
          flag_ok = True
          break
      except ValueError:
        print("Invalid integer value!")

      print(("Invalid option, range is [{0:d}, {1:d}]!".format(0 if flag_cancel else 1, num_options)))

      n_try += 1
      s_option = input("? ")

    if flag_ok:
      break
  return option


def format_box(title, ch="*"):
    """
    Encloses title in a box. Result is a list

    >>> for line in format_box("Today's TODO list"):
    ...     print(line)
    *************************
    *** Today's TODO list ***
    *************************
    """
    lt = len(title)
    return [(ch * (lt + 8)),
            (ch * 3 + " " + title + " " + ch * 3),
            (ch * (lt + 8))
           ]


def format_progress(i, n):
    """Returns string containing a progress bar, a percentage, etc."""
    if n == 0:
        fraction = 0
    else:
        fraction = float(i)/n
    LEN_BAR = 25
    num_plus = int(round(fraction*LEN_BAR))
    s_plus = '+'*num_plus
    s_point = '.'*(LEN_BAR-num_plus)
    return '[{0!s}{1!s}] {2:d}/{3:d} - {4:.1f}%'.format(s_plus, s_point, i, n, fraction*100)



def markdown_table(headers, data):
    """
    Creates MarkDown table. Returns list of strings

    Arguments:
      headers -- sequence of strings: (header0, header1, ...)
      data -- [(cell00, cell01, ...), (cell10, cell11, ...), ...]
    """

    maxx = [max([len(x) for x in column]) for column in zip(*data)]
    maxx = [max(ll) for ll in zip(maxx, [len(x) for x in headers])]
    mask = " | ".join(["%-{0:d}s".format(n) for n in maxx])

    ret = [mask % headers]



    ret.append(" | ".join(["-"*n for n in maxx]))
    for line in data:
        ret.append(mask % line)
    return ret


def print_skipped(reason):
    """Standardized printing for when a file was skipped."""
    print(("   ... SKIPPED ({0!s}).".format(reason)))



# #################################################################################################
# # Formatting for listing the programs available


def _format_exe_info(py_len, exeinfo, format, indlevel):
    """Renders ExeInfo object in specified format"""
    ret = []
    ind = " " * indlevel * NIND if format.startswith("text") else ""
    if format == "markdown-list":
        for si in exeinfo:
            ret.append("  - `{0!s}` -- {1!s}".format(si.filename, si.description))
    elif format == "markdown-table":
        mask = "%-{0:d}s | %s".format(py_len+2 )
        ret.append(mask % ("Script name", "Purpose"))
        ret.append("-" * (py_len + 3) + "|" + "-" * 10)
        for si in exeinfo:
            ret.append(mask % ("`{0!s}`".format(si.filename), si.description))
    elif format == "text":
        sbc = 1  # spaces between columns
        for si in exeinfo:
            ss = textwrap.wrap(si.description, 79 - py_len - sbc - indlevel*NIND)
            for i, s in enumerate(ss):
                if i == 0:
                    filecolumn = si.filename + " " + ("." * (py_len - len(si.filename)))
                else:
                    filecolumn = " " * (py_len + 1)

                ret.append("{}{}{}{}".format(ind, filecolumn, " "*sbc, s))

            # if si.flag_error:
            #     ret.append(piece+si.description)
            # else:
            #     ss = textwrap.wrap(si.description, 79 - py_len - 1)
            #     ret.append(piece+" "+(ss[0] if ss and len(ss) > 0 else "no doc"))
            #     for i in range(1, len(ss)):
            #         ret.append((" " * (py_len + 2))+ss[i])
    ret.append("")
    return ret


def format_exe_info(exeinfo, format="text", indlevel=0):
    """
    Generates listing of all Python scripts available as command-line programs.

    Args:
      exeinfo -- list of ExeInfo objects

      format -- One of the options below:
        "text" -- generates plain text for printing at the console
        "markdown-list" -- generates MarkDown as a list
        "markdown-table" -- generates MarkDown as a table

      indents -- indentation level ("text" format only)

    Returns: (list of strings, maximum filename size)
      list of strings -- can be joined with a "\n"
      maximum filename size
    """

    py_len = max([len(si.filename) for si in exeinfo])

    sisi_gra = [si for si in exeinfo if si.flag_gui == True]
    sisi_cmd = [si for si in exeinfo if si.flag_gui == False]
    sisi_none = [si for si in exeinfo if si.flag_gui is None]

    def get_title(x):
        return format_h2(x, format, indlevel*NIND) + [""]

    ret = []
    if len(sisi_gra) > 0:
        ret.extend(get_title("Graphical applications"))
        ret.extend(_format_exe_info(py_len, sisi_gra, format, indlevel + 1))
    if len(sisi_cmd) > 0:
        ret.extend(get_title("Command-line tools", ))
        ret.extend(_format_exe_info(py_len, sisi_cmd, format, indlevel + 1))
    if len(sisi_none) > 0:
        ret.extend(_format_exe_info(py_len, sisi_none, format, indlevel + 1))

    return ret, py_len

