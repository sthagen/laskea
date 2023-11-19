import laskea
import laskea.env as env


def test_report_command():
    report_string = env.report()
    assert f'laskea : {laskea.__version__.split("+")[0]}' in report_string
