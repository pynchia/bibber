from django import forms


class GameSetUpForm(forms.Form):
    PLAYERS = (
            (2, 'Two'),
            (3, 'Three'),
    )
    num_players = forms.ChoiceField(choices=PLAYERS,
                                    widget=forms.RadioSelect)

