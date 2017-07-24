import a99
import os
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import pytest


# def test_NullEditor():
#     app = a99.get_QApplication()
#     obj = a99.NullEditor()
#

def test_Parameter():
    app = a99.get_QApplication()
    obj = a99.Parameter()


def test_Parameters():
    app = a99.get_QApplication()
    obj = a99.Parameters()


# def test_PythonHighlighter():
#     app = a99.get_QApplication()
#     obj = a99.PythonHighlighter()


# def test_SignalProxy():
#     app = a99.get_QApplication()
#     obj = a99.SignalProxy()


def test_VerticalLabel():
    app = a99.get_QApplication()
    obj = a99.VerticalLabel(a99.XLogDialog())


def test_WBase():
    app = a99.get_QApplication()
    obj = a99.WBase(a99.XLogDialog())


def test_WCollapsiblePanel():
    app = a99.get_QApplication()
    obj = a99.WCollapsiblePanel(a99.XLogDialog())


def test_WDBRegistry():
    app = a99.get_QApplication()
    obj = a99.WDBRegistry(a99.XLogDialog())


# def test_WParametersEditor():
#     app = a99.get_QApplication()
#     obj = a99.WParametersEditor(None, a99.Parameters([["field0", {"value": 0}], ["field1", {"value": 1}]]))


def test_WSelectDir():
    app = a99.get_QApplication()
    obj = a99.WSelectDir(a99.XLogMainWindow())


def test_WSelectFile():
    app = a99.get_QApplication()
    obj = a99.WSelectFile(a99.XLogMainWindow())


def test_XLogDialog():
    app = a99.get_QApplication()
    obj = a99.XLogDialog()


def test_XLogMainWindow():
    app = a99.get_QApplication()
    obj = a99.XLogMainWindow()


# def test_XParametersEditor():
#     app = a99.get_QApplication()
#     obj = a99.XParametersEditor()


# def test_are_you_sure():
#     app = a99.get_QApplication()
#     obj = a99.are_you_sure("msg")


# def test_check_return_space():
#     app = a99.get_QApplication()
#     obj = a99.check_return_space()

def test_enc_name():
    app = a99.get_QApplication()
    obj = a99.enc_name("name")


def test_enc_name_descr():
    app = a99.get_QApplication()
    obj = a99.enc_name_descr("name", "descr")


def test_format_title0():
    app = a99.get_QApplication()
    obj = a99.format_title0("aaa")


def test_format_title1():
    app = a99.get_QApplication()
    obj = a99.format_title1("aaa")


def test_format_title2():
    app = a99.get_QApplication()
    obj = a99.format_title2("aaa")


def test_get_QApplication():
    app = a99.get_QApplication()
    obj = a99.get_QApplication()


# TODO test non-existing icons
def test_get_icon():
    app = a99.get_QApplication()
    # assert isinstance(a99.get_icon("document-open"), QIcon)
    icon = a99.get_icon("document-open")
    assert icon is not None

    # Not like this, always returns a QIcon assert a99.get_icon("aaaaaaaa") == None

# TODO test non-existing icons
def test_get_ne_icon():
    app = a99.get_QApplication()
    # assert isinstance(a99.get_icon("document-open"), QIcon)
    with pytest.raises(FileNotFoundError) as e_info:
        _ = a99.get_icon("nerdology1234")

    # Not like this, always returns a QIcon assert a99.get_icon("aaaaaaaa") == None


def test_get_matplotlib_layout():
    app = a99.get_QApplication()
    obj = a99.get_matplotlib_layout(QWidget())


def test_get_window_title():
    app = a99.get_QApplication()
    obj = a99.get_window_title("prefix")


def test_keep_ref():
    app = a99.get_QApplication()
    obj = a99.keep_ref(QWidget())


def test_nerdify():
    app = a99.get_QApplication()
    obj = a99.nerdify(QWidget())


def test_place_center():
    app = a99.get_QApplication()
    obj = a99.place_center(QMainWindow())


def test_place_left_top():
    app = a99.get_QApplication()
    obj = a99.place_left_top(QMainWindow())


def test_reset_table_widget():
    app = a99.get_QApplication()
    t = QTableWidget()
    obj = a99.reset_table_widget(t, 10, 10)


# def test_show_edit_form():
#     app = a99.get_QApplication()
#     obj = a99.show_edit_form()
#
#
# def test_show_error():
#     app = a99.get_QApplication()
#     obj = a99.show_error("test")
#
#
# def test_show_message():
#     app = a99.get_QApplication()
#     obj = a99.show_message("test")
#
#
# def test_show_warning():
#     app = a99.get_QApplication()
#     obj = a99.show_warning("test")


def test_snap_left():
    app = a99.get_QApplication()
    obj = a99.snap_left(QMainWindow())


def test_snap_right():
    app = a99.get_QApplication()
    obj = a99.snap_right(QMainWindow())


# def test_style_checkboxes():
#     app = a99.get_QApplication()
#     obj = a99.style_checkboxes()


# def test_style_widget_changed():
#     app = a99.get_QApplication()
#     obj = a99.style_widget_changed()
#
#
# def test_style_widget_valid():
#     app = a99.get_QApplication()
#     obj = a99.style_widget_valid()


def test_table_info_to_parameters(tmpdir):
    fn = os.path.join(str(tmpdir), "testdb.sqlite")
    conn = a99.get_conn(fn)
    conn.execute("create table test (id integer primary key, name text)")
    ti = a99.get_table_info(conn, "test")

    app = a99.get_QApplication()
    obj = a99.table_info_to_parameters(ti)

    assert ti == {'id': {'cid': 0,
                         'name': 'id',
                         'type': 'integer',
                         'notnull': 0,
                         'dflt_value': None,
                         'pk': 1},
                  'name': {'cid': 1,
                           'name': 'name',
                           'type': 'text',
                           'notnull': 0,
                           'dflt_value': None,
                           'pk': 0}}


