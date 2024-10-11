from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status

from .agentvalidationview import AgentValidationView
from .historicaldataview import HistoricalDataView
from .webrevenuhypoview import WebRevenuHypoView
from .agentpredglobaleview import AgentPredGlobaleView
from .unitrevenuepredictionapiview import UnitRevenuePredictionAPIView
