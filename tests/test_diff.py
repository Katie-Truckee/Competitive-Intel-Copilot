from competitive_intel.diff import compute_diff, is_meaningful


def test_identical_text_has_no_meaningful_diff():
    text = "Pricing: $10/month\nPlan: Pro"
    diff_text = compute_diff(text, text)
    assert not is_meaningful(diff_text)


def test_changed_line_is_meaningful():
    old = "Pricing: $10/month"
    new = "Pricing: $15/month"
    diff_text = compute_diff(old, new)
    assert is_meaningful(diff_text)
