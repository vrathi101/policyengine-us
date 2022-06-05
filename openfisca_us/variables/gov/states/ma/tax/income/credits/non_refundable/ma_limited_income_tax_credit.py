from openfisca_us.model_api import *


class ma_limited_income_tax_credit(Variable):
    value_type = float
    entity = TaxUnit
    label = "MA Limited Income Credit"
    unit = USD
    definition_period = YEAR
    is_eligible = in_state("MA")
    reference = "https://www.mass.gov/doc/2021-schedule-nts-l-nrpy-no-tax-status-and-limited-income-credit/download"

    def formula(tax_unit, period, parameters):
        agi = tax_unit("ma_agi", period)
        exemption_threshold = tax_unit(
            "ma_income_tax_exemption_threshold", period
        )
        lic = parameters(
            period
        ).states.ma.tax.income.credits.non_refundable.limited_income_credit
        income_level = agi / exemption_threshold
        eligible = income_level <= lic.income_limit
        other_credits = ["ma_dependent_credit", "ma_eitc"]
        income_tax = tax_unit("ma_income_tax_before_credits", period)
        other_credits_value = add(tax_unit, period, other_credits)
        income_tax -= other_credits_value
        income_over_threshold = max_(0, agi - exemption_threshold)
        tax_cap = lic.percent * income_over_threshold
        excess_tax = max_(0, income_tax - tax_cap)
        return eligible * excess_tax
