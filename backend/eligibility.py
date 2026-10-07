def check_basic_eligibility(profile, scheme):
    """
    Preliminary rule-based eligibility check.

    IMPORTANT:
    This is only a matching layer.
    Final eligibility must always be verified
    against the current official scheme rules.
    """

    reasons = []
    score = 0

    age = profile.get("age")
    income = profile.get("income")
    occupation = profile.get("occupation")
    state = profile.get("state")

    criteria = scheme.get("eligibility", {})

    # Age
    min_age = criteria.get("min_age")
    max_age = criteria.get("max_age")

    if min_age is not None:
        if age >= min_age:
            score += 1
            reasons.append("Age requirement matched.")
        else:
            reasons.append("Minimum age requirement not matched.")

    if max_age is not None:
        if age <= max_age:
            score += 1
            reasons.append("Maximum age requirement matched.")
        else:
            reasons.append("Maximum age requirement not matched.")

    # Income
    max_income = criteria.get("max_income")

    if max_income is not None:
        if income <= max_income:
            score += 1
            reasons.append("Income requirement matched.")
        else:
            reasons.append("Income requirement may not be matched.")

    # Occupation
    occupations = criteria.get("occupations", [])

    if occupations:
        if occupation.lower() in [x.lower() for x in occupations]:
            score += 1
            reasons.append("Occupation requirement matched.")
        else:
            reasons.append("Occupation requirement may not be matched.")

    # State
    states = criteria.get("states", [])

    if states:
        if state.lower() in [x.lower() for x in states]:
            score += 1
            reasons.append("State requirement matched.")
        else:
            reasons.append("State requirement may not be matched.")

    total = 0

    if min_age is not None:
        total += 1

    if max_age is not None:
        total += 1

    if max_income is not None:
        total += 1

    if occupations:
        total += 1

    if states:
        total += 1

    percentage = round((score / total) * 100) if total else 0

    return {
        "scheme": scheme["name"],
        "match_percentage": percentage,
        "reasons": reasons,
        "official_source": scheme.get("official_source"),
        "verification_date": scheme.get("last_verified")
    }
