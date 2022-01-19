from django.forms.widgets import Input


class LatexInput(Input):
    """ Custom widget for LaTeX format text input """
    input_type = 'text'
    template_name = 'reshuffle/widgets/latex_widget.html'
