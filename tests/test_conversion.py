"""Testing conversion routines"""


import a99



def test_str2bool(tmpdir):
    # xx = ["true", "T", "1", "True", "t"]
    xx = ["T"]
    assert(all([a99.str2bool(x) for x in xx]))

    # xx = ["false", "F", "f", "0", "False"]
    xx = ["F"]
    assert(all([not a99.str2bool(x) for x in xx]))

def test_bool2str(tmpdir):
    x = True
    assert(a99.bool2str(x) == "T")


def test_chunk_string(tmpdir):
    pass


def test_ordinal_suffix(tmpdir):
    xx = [0, 1, 2, 3]
    assert([a99.ordinal_suffix(x) for x in xx] == ["th", "st", "nd", "rd"])


def test_seconds2str(tmpdir):
    pass


def test_make_fits_keys_dict(tmpdir):
    a99.make_fits_keys_dict(["AAAAAAAAAAAAAAAAAA", "BBBBBBBBBBBBBBBBBBBBB"])


def test_valid_fits_key(tmpdir):
    a99.valid_fits_key("ABCD")


def test_eval_fieldnames(tmpdir):
    x = "['AAAAAAAAAAAAAAA', 'BBBBBBBBBBBBBBBB']"
    a99.eval_fieldnames(x)


def test_expr_to_fieldname(tmpdir):
    x = "aaa_bbb()"
    assert(a99.expr_to_fieldname(x))


def test_module_to_dict(tmpdir):
    a99.module_to_dict(a99.conversion)


def test_unicode_to_greek(tmpdir):
    x = '\u0391'
    assert(a99.unicode_to_greek(x) == 'Alpha')


def test_greek_to_unicode(tmpdir):
    x = 'Alpha'
    assert(a99.greek_to_unicode(x) == '\u0391')


def test_make_code_readable():
    a99.make_code_readable(", , , ")