from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from financial_data.views import (
    EnterpriseViewSet,
    IndustryTypeViewSet,
    AssetsViewViewSet,
    EquitiesViewViewSet,
    ExpensesViewViewSet,
    LiabilitiesViewViewSet,
    MarketingExpensesViewViewSet,
    OpportunityBookViewViewSet,
    OrderBookViewViewSet,
    RevenuesViewViewSet,
    SalaryExpensesViewViewSet,
    SalesBudgetsViewViewSet,
    EnterpriseIndustryViewSet,
    RevenueDescriptionViewSet,
    LatestOrderBookViewSet,
)
from django.views.generic import RedirectView

from financial_data.views.bulkIncomeDetailCreateView import BulkIncomeDetailCreateView
from financial_data.views.latestopportunitybookviewSet import (
    LatestOpportunityBookViewSet,
)


router = DefaultRouter()
router.register(r"enterprises", EnterpriseViewSet)
router.register(r"industry-types", IndustryTypeViewSet)
router.register(r"assets", AssetsViewViewSet)
router.register(r"equities", EquitiesViewViewSet)
router.register(r"expenses", ExpensesViewViewSet)
router.register(r"liabilities", LiabilitiesViewViewSet)
router.register(r"marketing-expenses", MarketingExpensesViewViewSet)
router.register(r"opportunity-book", OpportunityBookViewViewSet)
router.register(r"order-book", OrderBookViewViewSet)
router.register(r"revenues", RevenuesViewViewSet)
router.register(r"salary-expenses", SalaryExpensesViewViewSet)
router.register(r"sales-budgets", SalesBudgetsViewViewSet)
router.register(r"enterprise-industry", EnterpriseIndustryViewSet)
router.register(
    r"revenue-descriptions", RevenueDescriptionViewSet, basename="revenue-description"
)
router.register(
    r"latest-orderbooks", LatestOrderBookViewSet, basename="latest-orderbook"
)
router.register(
    r"latest-opportunitybooks",
    LatestOpportunityBookViewSet,
    basename="latest-opportunitybook",
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path(
        "", RedirectView.as_view(url="api/", permanent=False)
    ),  # Redirect root to API root
    path("api/agents/", include("agents.urls")),
    path(
        "api/bulk-income-detail/",
        BulkIncomeDetailCreateView.as_view(),
        name="bulk-income-detail-create",
    ),
]
