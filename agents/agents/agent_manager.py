from .validation_agent import ValidationAgent
from .agent_acp_t_produit import AgentACP_T_produit
from .web_revenu_hypo_agent import WebRevenuHypoAgent
from .pred_globale_agent import PredGlobaleAgent

class AgentManager:
    @staticmethod
    def agent_validation(enterprise_id):
        return ValidationAgent.execute(enterprise_id)

    @staticmethod
    def agent_acp_t_produit(industry_type):
        return AgentACP_T_produit.execute(industry_type)

    @staticmethod
    def agent_web_revenu_hypo(industry_type):
        return WebRevenuHypoAgent.execute(industry_type)

    @staticmethod
    def agent_pred_globale(enterprise_id, year):
        return PredGlobaleAgent.execute(enterprise_id, year)