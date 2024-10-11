from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..agents.pred_globale_agent import PredGlobaleAgent
from urllib.parse import unquote
import logging
import traceback


logger = logging.getLogger(__name__)


class AgentPredGlobaleView(APIView):
    def get(self, request, enterprise_id):
        try:
            include_plot = (
                request.query_params.get("include_plot", "false").lower() == "true"
            )
            description = request.query_params.get("description")

            growth_rate_param = request.query_params.get("growth_rate")
            if growth_rate_param in [None, "undefined", ""]:
                growth_rate = 0.05
            else:
                try:
                    growth_rate = float(growth_rate_param)
                except ValueError:
                    return Response(
                        {"error": f"Invalid growth rate: {growth_rate_param}"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            if description:
                description = unquote(description.strip('"'))

            agent = PredGlobaleAgent()
            result = agent.execute(enterprise_id, description, growth_rate)

            if "error" in result:
                logger.error(f"Error in PredGlobaleAgent: {result['error']}")
                if "traceback" in result:
                    logger.error(f"Traceback: {result['traceback']}")
                return Response(result, status=status.HTTP_400_BAD_REQUEST)

            response_data = {
                "enterprise_id": enterprise_id,
                "enterprise_name": result["enterprise_name"],  # Include enterprise name
                "prediction_year": result["prediction_year"],
                "description": description,
                "growth_rate": growth_rate,
                "data_validity": result.get("data_validity"),
                "results": result["results"],
            }

            if include_plot:
                plot_path = agent.plot_prediction(result)
                response_data["plot_url"] = plot_path

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Unexpected error in AgentPredGlobaleView: {str(e)}")
            logger.error(traceback.format_exc())
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
