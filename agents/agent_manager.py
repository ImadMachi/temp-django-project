
import numpy as np
from sklearn.decomposition import PCA
from statsmodels.tsa.arima.model import ARIMA
from django.core.cache import cache
from financial_data.models import RevenuesView, SalesBudgetsView, OpportunityBookView

class AgentManager:
    @staticmethod
    def agent_validation(enterprise_id):
        years = RevenuesView.objects.filter(enterprise_id=enterprise_id).values('year').distinct().count()
        return years > 1

    @staticmethod
    def agent_acp_t_produit(industry_type):
        revenues = RevenuesView.objects.filter(enterprise__industry_type=industry_type)
        data = []
        for year in set(revenues.values_list('year', flat=True)):
            year_data = revenues.filter(year=year).values_list('real', flat=True)
            if len(year_data) == 12:
                data.append(year_data)
        
        if not data:
            return None

        pca = PCA(n_components=1)
        principal_component = pca.fit_transform(data)
        return principal_component.flatten().tolist()

    @staticmethod
    def agent_web_revenu_hypo(industry_type):
        cache_key = f'revenu_hypo_{industry_type}'
        cached_result = cache.get(cache_key)
        if cached_result is not None:
            return cached_result

        # Placeholder for web scraping and LLM logic
        result = 0.05  # Example: 5% growth hypothesis

        cache.set(cache_key, result, 3600)  # Cache for 1 hour
        return result

    @staticmethod
    def agent_pred_globale(enterprise_id, year):
        revenues = RevenuesView.objects.filter(enterprise_id=enterprise_id).order_by('year', 'month')
        data = [r.real for r in revenues]
        model = ARIMA(data, order=(1,1,1))
        results = model.fit()
        forecast = results.forecast(steps=12)
        
        sales_budget = SalesBudgetsView.objects.filter(enterprise_id=enterprise_id, year=year)
        opportunities = OpportunityBookView.objects.filter(enterprise_id=enterprise_id, year=year)
        
        alpha, beta1, beta2 = 0.7, 0.1, 0.1
        
        final_forecast = forecast * alpha + \
                         np.array([s.budget for s in sales_budget]) * beta1 + \
                         np.array([o.total_opportunity_value for o in opportunities]) * beta2
        
        return final_forecast.tolist()