from rest_framework import serializers as se
from prj_constants import NUM_CARDS


class GameSerializer(se.Serializer):
    num_players = se.IntegerField(min_value=1, max_value=3)


class CardSerializer(se.Serializer):
    pos = se.IntegerField(min_value=0, max_value=NUM_CARDS-1)
    occupants = se.ListField(child=se.IntegerField(min_value=0,
                                                   max_value=NUM_CARDS-1))
    covered = se.BooleanField(default=True)
    captured = se.BooleanField(default=False)
    filename = se.ReadOnlyField()


