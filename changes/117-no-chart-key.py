# changes/117-no-chart-key.py - home week chart: the key under the chart (Actual, Original projection, Projected) is removed


def change(t):
    i = t.find('      <div className="gx-key116" data-gx="116k">')
    if i < 0:
        if "gx117: chart key removed" in t:
            print("(install) 117: chart key removed: already done")
            return t
        fail("117: chart key not found")
    j = t.find("      </div>\n", i)
    if j < 0:
        fail("117: end of chart key not found")
    t = t[:i] + "      {/* gx117: chart key removed */}\n" + t[j + len("      </div>\n"):]
    print("(install) 117: chart key removed: updated")
    return t


edit(APP, change)
