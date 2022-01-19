from django.forms.widgets import Input


class LatexInput(Input):
    input_type = 'text'
    template_name = 'reshuffle/widgets/latex_widget.html'
