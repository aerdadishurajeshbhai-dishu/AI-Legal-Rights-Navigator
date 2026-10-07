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
    total = 0

    age = profile.get("age")
    income = profile.get("income")
    occupation = profile.get("occupation", "")
    state = profile.get("state", "")

    criteria = scheme.get("eligibility", {})

    # Age - Minimum
    min_age = criteria.get("min_age")

    if min_age is not None and age is not None:
        total += 1

        if age >= min_age:
            score += 1
            reasons.append("Minimum age requirement matched.")
        else:
            reasons.append("Minimum age requirement not matched.")

    # Age - Maximum
    max_age = criteria.get("max_age")

    if max_age is not None and age is not None:
        total += 1

        if age <= max_age:
            score += 1
            reasons.append("Maximum age requirement matched.")
        else:
            reasons.append("Maximum age requirement not matched.")

    # Income
    max_income = criteria.get("max_income")

    if max_income is not None and income is not None:
        total += 1

        if income <= max_income:
            score += 1
            reasons.append("Income requirement matched.")
        else:
            reasons.append("Income requirement not matched.")

    # Occupation
    occupations = criteria.get("occupations", [])

    if occupations and occupation:
        total += 1

        if occupation.lower() in [
            x.lower() for x in occupations
        ]:
            score += 1
            reasons.append("Occupation requirement matched.")
        else:
            reasons.append(
                "Occupation requirement not matched."
            )

    # State
    states = criteria.get("states", [])

    if states and state:
        total += 1

        if state.lower() in [
            x.lower() for x in states
        ]:
            score += 1
            reasons.append("State requirement matched.")
        else:
            reasons.append(
                "State requirement not matched."
            )

    # Match percentage
    percentage = (
        round((score / total) * 100)
        if total > 0
        else 0
    )

    return {
        "scheme": scheme.get("name"),
        "match_percentage": percentage,
        "reasons": reasons,
        "official_source": scheme.get(
            "official_source"
        ),
        "verification_date": scheme.get(
            "last_verified"
        )
    }
