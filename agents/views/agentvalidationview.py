from rest_framework.views import APIView
from rest_framework.response import Response
from ..agents.validation_agent import ValidationAgent


class AgentValidationView(APIView):
    def get(self, request, enterprise_id):
        result = ValidationAgent.execute(enterprise_id)
        return Response(result)
