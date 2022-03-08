from django.forms.widgets import Input


class LatexInput(Input):
    """ Custom widget for LaTeX format text input """
    input_type = 'text'
    template_name = 'reshuffle/widgets/latex_widget.html'


class TestNumInput(Input):
    """ Custom widget for TestNum format text input """
    input_type = 'number'
    template_name = 'reshuffle/widgets/test_num_widget.html'
