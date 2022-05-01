from openfisca_us.model_api import *


class eitc_phased_in(Variable):
    value_type = float
    entity = TaxUnit
    label = "EITC phase-in amount"
    unit = "currency-USD"
    documentation = "EITC maximum amount, taking into account earnings."
    definition_period = YEAR

    def formula(tax_unit, period, parameters):
        maximum = tax_unit("eitc_maximum", period)
        phasein_rate = tax_unit("eitc_phasein_rate", period)
        earned_income = max_(0, tax_unit("filer_earned", period))
        phased_in_amount = earned_income * phasein_rate
        return min_(maximum, phased_in_amount)
