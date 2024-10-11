from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from django.http import HttpRequest
from django.core.cache import cache
from datetime import datetime
import json
from .webrevenuhypoview import WebRevenuHypoView
from .agentpredglobaleview import AgentPredGlobaleView


class SystemBasedPredictionView(APIView):
    def create_mock_drf_request(self, params):
        mock_http_request = HttpRequest()
        mock_http_request.GET = params
        return Request(mock_http_request)

    def get_web_revenu_hypo(self, enterprise_id, growth_rate, prediction_year):
        cache_key = f"web_hypo_{enterprise_id}_{growth_rate}_{prediction_year}"
        cached_result = cache.get(cache_key)
        if cached_result:
            return cached_result

        view = WebRevenuHypoView()
        mock_request = self.create_mock_drf_request(
            {"growth_rate": str(growth_rate), "prediction_year": str(prediction_year)}
        )
        response = view.get(mock_request, enterprise_id)
        result = json.loads(response.content)

        cache.set(cache_key, result, 3600)  # Cache for 1 hour
        return result

    def get_pred_globale(self, enterprise_id, description, growth_rate):
        cache_key = f"pred_globale_{enterprise_id}_{description}_{growth_rate}"
        cached_result = cache.get(cache_key)
        if cached_result:
            return cached_result

        view = AgentPredGlobaleView()
        mock_request = self.create_mock_drf_request(
            {
                "description": description,
                "growth_rate": str(growth_rate),
                "include_plot": "false",
            }
        )
        response = view.get(mock_request, enterprise_id)
        result = response.data

        cache.set(cache_key, result, 3600)  # Cache for 1 hour
        return result

    def get(self, request, enterprise_id):
        try:
            description = request.GET.get("description")
            growth_rate = float(request.GET.get("growth_rate", 0.05))
            prediction_year = datetime.now().year + 1

            cache_key = f"combined_prediction_{enterprise_id}_{description}_{growth_rate}_{prediction_year}"
            cached_result = cache.get(cache_key)
            if cached_result:
                return Response(cached_result, status=status.HTTP_200_OK)

            # Get predictions from both views
            web_hypo = self.get_web_revenu_hypo(
                enterprise_id, growth_rate, prediction_year
            )
            pred_globale = self.get_pred_globale(
                enterprise_id, description, growth_rate
            )

            # Combine predictions
            combined_monthly_predictions = {}
            for month in range(1, 13):
                month_key = f"{prediction_year}-{month:02d}"
                web_hypo_value = web_hypo["monthly_predictions"].get(month_key, 0)
                pred_globale_value = pred_globale["results"][description][
                    str(prediction_year)
                ].get(str(month), 0)

                combined_value = (0.3 * web_hypo_value) + (0.7 * pred_globale_value)
                combined_monthly_predictions[month_key] = round(combined_value, 2)

            result = {
                "enterprise_id": enterprise_id,
                "enterprise_name": web_hypo["enterprise_info"]["enterprise_name"],
                "prediction_year": prediction_year,
                "description": description,
                "growth_rate": growth_rate,
                "monthly_predictions": combined_monthly_predictions,
            }

            cache.set(cache_key, result, 3600)  # Cache for 1 hour

            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
