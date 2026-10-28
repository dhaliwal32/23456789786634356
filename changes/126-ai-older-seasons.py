# changes/126-ai-older-seasons.py - the AI now learns from older NHL seasons, as far back as testing showed it still helps for each kind of player: forwards and defence from 2014-15 (tested 0.7% and 0.4% more accurate), goalie start chance from 2021-22 (1.5%), goalie points if he starts stays on the last two seasons (older seasons made it worse). The older weeks of history are added to ai/history

OLDER = [('20142015', '2014-10-06', '2015-04-13'), ('20152016', '2015-10-05', '2016-04-12'), ('20162017', '2016-10-10', '2017-04-12'), ('20172018', '2017-09-28', '2018-04-10'), ('20182019', '2018-09-28', '2019-04-10'), ('20192020', '2019-09-28', '2020-03-15'), ('20202021', '2021-01-10', '2021-05-25'), ('20212022', '2021-10-01', '2022-05-05'), ('20222023', '2022-10-01', '2023-04-20'), ('20232024', '2023-10-01', '2024-04-25')]

TRAIN_FROM = {'F': '2014-10-01', 'D': '2014-10-01', 'G_start': '2021-10-01', 'G_cond': '2024-10-01'}


def change(t):
    t = lit(t, "126: older seasons", 'SEASONS = [("20242025", "2024-10-01", "2025-04-20"),',
            "SEASONS = [" + "".join(f'("{s}", "{a}", "{b}"), ' for s, a, b in OLDER) + '("20242025", "2024-10-01", "2025-04-20"),',
            '("' + OLDER[0][0] + '", "' + OLDER[0][1] + '"')
    t = lit(t, "126: how far back each group learns", "SK_STATS = [\"G\", \"A\", \"PM\", \"PPP\", \"SHP\", \"SOG\", \"HIT\", \"BLK\"]\n",
            "# change 126: how far back each kind of player learns from (tested in ai/research/history_exp.json)\nTRAIN_FROM = " + repr(TRAIN_FROM) + "\n"
            "SK_STATS = [\"G\", \"A\", \"PM\", \"PPP\", \"SHP\", \"SOG\", \"HIT\", \"BLK\"]\n", "TRAIN_FROM = ")
    t = lit(t, "126: use it when training", "        X, Y, dates, keys = data[grp]\n",
            "        X, Y, dates, keys = data[grp]\n"
            "        cut = TRAIN_FROM.get(grp)  # change 126\n"
            "        if cut and len(dates):\n"
            "            m = dates >= cut\n"
            "            if 0 < int(m.sum()) < len(dates) and int(m.sum()) >= cfg[\"min_train\"]:\n"
            "                X, Y, dates = X[m], Y[m], dates[m]\n"
            "                keys = [k for k, ok in zip(keys, m.tolist()) if ok] if keys is not None else None\n",
            "cut = TRAIN_FROM.get(grp)  # change 126")
    return t


edit("ai_learn.py", change)
