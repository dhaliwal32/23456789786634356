# changes/255-box-remember-side.py - Roster box opens on the side you left it on (Day, Win, Graph or Players), saved on each device

OLD = '''  const [k, setK] = useState(0);
  const [sel, setSel] = useState(null);
  const [full, setFull] = useState(false);
  const [dv, setDv] = useState(null);
  const [bp, setBp] = useState(null);
  const stg = React.useRef(null), pr = React.useRef(null), ang = React.useRef(0), drag = React.useRef(null);
'''
NEW = '''  const [k, setK] = useState(() => { const v = Number(uiGet().bx255); return v >= 0 && v <= 3 ? Math.floor(v) : 0; }); /* change 255: last side */
  const [sel, setSel] = useState(null);
  const [full, setFull] = useState(false);
  const [dv, setDv] = useState(null);
  const [bp, setBp] = useState(null);
  const stg = React.useRef(null), pr = React.useRef(null), ang = React.useRef(k * 90), drag = React.useRef(null);
  useEffect(() => { try { if (uiGet().bx255 !== k) uiSet("bx255", k); } catch (e) {} }, [k]);
'''

def change(t):
    t = lit(t, "255: remember the side", OLD, NEW, "/* change 255: last side */")
    return t

edit(APP, change)
