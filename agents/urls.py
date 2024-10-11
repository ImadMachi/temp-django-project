from django.urls import path

from agents.views.acp_t_produit_view import ACP_T_ProduitView
from agents.views.agentpredglobaleview import AgentPredGlobaleView
from agents.views.agentvalidationview import AgentValidationView
from agents.views.historicaldataview import HistoricalDataView
from agents.views.system_based_redictionView import SystemBasedPredictionView
from agents.views.unitrevenuepredictionapiview import UnitRevenuePredictionAPIView
from agents.views.webrevenuhypoview import WebRevenuHypoView


urlpatterns = [
    path(
        "validation/<int:enterprise_id>/",
        AgentValidationView.as_view(),
        name="agent-validation",
    ),
    path(
        "historical-data/<int:enterprise_id>/",
        HistoricalDataView.as_view(),
        name="historical-data",
    ),
    path(
        "acp-t-produit/<int:enterprise_id>/",
        ACP_T_ProduitView.as_view(),
        name="acp-t-produit",
    ),
    path(
        "web-revenu-hypo/<int:enterprise_id>/",
        WebRevenuHypoView.as_view(),
        name="web-revenu-hypo",
    ),
    path(
        "pred-globale/<int:enterprise_id>",
        AgentPredGlobaleView.as_view(),
        name="agent-pred-globale",
    ),
    path(
        "agent-pred-globale/<int:enterprise_id>/",
        AgentPredGlobaleView.as_view(),
        name="agent-pred-globale",
    ),
    path(
        "unit-pred-revenu/<int:enterprise_id>/",
        UnitRevenuePredictionAPIView.as_view(),
        name="unit-pred-revenu",
    ),
    path(
        "system-based-prediction/<int:enterprise_id>/",
        SystemBasedPredictionView.as_view(),
        name="system-based-prediction",
    ),
]
