# changes/068-ai-lab-in-setup.py - adds AI Lab and Prediction history rows to Setup so the phone can reach them
OLD = '() => go("setup", "data"), 5)}'
NEW = OLD + r'''
        {/* change 068: AI Lab links for the phone */}
        {row("ailab", "AI Lab", "How each projection is doing", () => window.open("ai-dashboard.html", "_blank"), 6)}
        {row("history", "Prediction history", "Every projection and what happened", () => window.open("ai-history.html", "_blank"), 7)}'''


def change(t):
    return lit(t, "068: AI Lab rows in Setup", OLD, NEW, "change 068: AI Lab links")


edit(APP, change)
