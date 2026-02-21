from .models import Activity

class FeedService:
    @staticmethod
    def log_activity(actor, target, event_type, amount=None, content=""):
        return Activity.objects.create(
            actor=actor,target=target,event_type=event_type,amount=amount,content=content)