# changes/127-ai-history-2008.py - the AI's forwards and defence now learn from 2008-09 on (tested: forwards 0.9% and defence 0.7% more accurate than with this season's history only; going back to 2005-06 made forwards worse again). Goalie start chance stays from 2021-22, goalie points if he starts from 2024-25

OLDER = [('20082009', '2008-10-03', '2009-04-14'), ('20092010', '2009-09-30', '2010-04-13'), ('20102011', '2010-10-06', '2011-04-12'), ('20112012', '2011-10-05', '2012-04-09'), ('20122013', '2013-01-18', '2013-04-30'), ('20132014', '2013-09-29', '2014-04-15')]


def change(t):
    t = lit(t, "127: seasons from 2008-09", 'SEASONS = [("20142015", "2014-10-06", "2015-04-13"),',
            "SEASONS = [" + "".join(f'("{s}", "{a}", "{b}"), ' for s, a, b in OLDER) + '("20142015", "2014-10-06", "2015-04-13"),',
            '("20082009", "2008-10-03", "2009-04-14")')
    t = lit(t, "127: forwards and defence from 2008-09", "TRAIN_FROM = {'F': '2014-10-01', 'D': '2014-10-01',",
            "TRAIN_FROM = {'F': '2008-10-01', 'D': '2008-10-01',", "TRAIN_FROM = {'F': '2008-10-01', 'D': '2008-10-01',")
    return t


edit("ai_learn.py", change)
