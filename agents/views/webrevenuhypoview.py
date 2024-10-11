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
from datetime import datetime


class WebRevenuHypoView(APIView):  # type: ignore
    def get(self, request, enterprise_id):
        try:
            enterprise = EnterpriseIndustryView.objects.get(enterprise_id=enterprise_id)
            growth_rate = float(request.GET.get("growth_rate", 0.05))
            prediction_year = int(
                request.GET.get("prediction_year", datetime.now().year + 1)
            )

            agent = WebRevenuHypoAgent()
            enterprise_info = {
                "enterprise_id": enterprise.enterprise_id,
                "enterprise_name": enterprise.enterprise_name,
                "industry_type": enterprise.industry_type_label,
                "founding_date": enterprise.founding_date.isoformat(),
                "employees_count": enterprise.employees_count,
                "enterprise_active": enterprise.enterprise_active,
            }

            result = agent.execute(
                enterprise.industry_type_label,
                growth_rate,
                enterprise_info,
                prediction_year,
            )

            return JsonResponse(result)
        except EnterpriseIndustryView.DoesNotExist:
            return JsonResponse({"error": "Enterprise not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
