from rest_framework.views import APIView
from rest_framework.response import Response
from ..agents.agent_acp_t_produit import AgentACP_T_produit


class ACP_T_ProduitView(APIView):
    def get(self, request, enterprise_id):
        description = request.query_params.get("description")
        if not description:
            return Response({"error": "Description parameter is required"}, status=400)

        result = AgentACP_T_produit.execute(enterprise_id, description)
        return Response(result)
