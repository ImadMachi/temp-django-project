from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from ..agents.agent_manager import AgentManager
from ..agents.validation_agent import ValidationAgent
from ..agents.historical_data_agent import HistoricalDataAgent
from ..agents.agent_acp_t_produit import AgentACP_T_produit
from ..agents.web_revenu_hypo_agent import WebRevenuHypoAgent
from ..agents.pred_globale_agent import PredGlobaleAgent
from ..agents.unit_solde_renvenu_pred import UnitBasedRevenuePrediction
from financial_data.models import EnterpriseIndustryView, Enterprise, IndustryType
from urllib.parse import unquote


class UnitRevenuePredictionAPIView(APIView):
    def get(self, request, enterprise_id):
        try:
            growth_rate = float(request.GET.get("growth_rate", 0.05))
            description = request.GET.get("description")

            if growth_rate < -1 or growth_rate > 1:
                return Response(
                    {"error": "Growth rate must be between -1 and 1"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if not description:
                return Response(
                    {"error": "Description is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            description = unquote(description.strip('"'))

            agent = UnitBasedRevenuePrediction(enterprise_id, description, growth_rate)
            prediction_data = agent.get_prediction_data()

            return Response(prediction_data, status=status.HTTP_200_OK)

        except ValueError as e:
            return Response(
                {"error": f"Invalid input: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
