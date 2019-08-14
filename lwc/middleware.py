from joins.models import Join
from django.utils.deprecation import MiddlewareMixin

class ReferMiddlware(MiddlewareMixin):
    def process_request(self,request):
        ref_id = request.GET.get("ref","")
        try:
            obj = Join.objects.get(ref_id=ref_id)
        except:
            obj = None
        if obj:
            request.session["join_id_ref"] = obj.id

