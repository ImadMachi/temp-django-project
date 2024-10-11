from rest_framework.views import APIView
from rest_framework.response import Response
from ..agents.historical_data_agent import HistoricalDataAgent


class HistoricalDataView(APIView):
    def get(self, request, enterprise_id):
        description = request.query_params.get("description")
        result = HistoricalDataAgent.execute(enterprise_id, description)
        return Response(result)
