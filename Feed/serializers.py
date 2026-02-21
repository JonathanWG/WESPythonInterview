from rest_framework import serializers
from .models import Activity

class ActivitySerializer(serializers.ModelSerializer):

    display_text = serializers.SerializerMethodField()

    class Meta:
        model = Activity
        fields = ['id', 'display_text', 'timestamp']

    def get_display_text(self, obj):
        actor_name = obj.actor.username
        target_name = obj.target.username

        if obj.event_type == Activity.PAYMENT:
            return f"{actor_name} paid {target_name} ${obj.amount:.2f} for {obj.content}"
        
        elif obj.event_type == Activity.FRIENDSHIP:
            return f"{actor_name} and {target_name} are now friends"
        
        return "Unknown activity"