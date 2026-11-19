"""Illustrative unit economics, never a claim of validated demand or actual costs."""
import math


def break_even(price=499, variable_cost=80, payment_fee_pct=3, fixed_monthly_cost=15000):
    values=[price,variable_cost,payment_fee_pct,fixed_monthly_cost]
    if not all(math.isfinite(x) for x in values) or price<=0 or min(variable_cost,payment_fee_pct,fixed_monthly_cost)<0 or payment_fee_pct>100:
        raise ValueError("Invalid cost assumptions")
    contribution=price*(1-payment_fee_pct/100)-variable_cost
    return {"price":price,"variable_cost":variable_cost,"payment_fee_pct":payment_fee_pct,
            "fixed_monthly_cost":fixed_monthly_cost,"contribution_per_paid_user":round(contribution,2),
            "break_even_paid_users":math.ceil(fixed_monthly_cost/contribution) if contribution>0 else None,
            "basis":"Illustrative assumptions; excludes acquisition, tax, founder salaries and unquoted data/compliance costs."}
