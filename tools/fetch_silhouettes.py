import json, re, sys, time, urllib.request, urllib.parse

BUILD = 555
API = "https://api.phylopic.org"
PD = ("https://creativecommons.org/publicdomain/zero/1.0/",
      "https://creativecommons.org/publicdomain/mark/1.0/")

# id -> list of candidate taxon names, most specific first
TARGETS = [
 ("human",            ["homo sapiens", "homo"]),
 ("chimpanzee",       ["pan troglodytes", "pan"]),
 ("bonobo",           ["pan paniscus", "pan"]),
 ("gorilla_west",     ["gorilla gorilla", "gorilla"]),
 ("gorilla_east",     ["gorilla beringei", "gorilla"]),
 ("orangutan_borneo", ["pongo pygmaeus", "pongo"]),
 ("orangutan_sumatra",["pongo abelii", "pongo"]),
 ("elephant_asian",   ["elephas maximus", "elephas"]),
 ("elephant_african", ["loxodonta africana", "loxodonta"]),
 ("dolphin",          ["tursiops truncatus", "tursiops", "delphinidae"]),
 ("orca",             ["orcinus orca", "orcinus", "delphinidae"]),
 ("horse",            ["equus ferus caballus", "equus ferus", "equus"]),
 ("pig",              ["sus scrofa domesticus", "sus scrofa", "sus"]),
 ("dog",              ["canis lupus familiaris", "canis lupus", "canis"]),
 ("cattle",           ["bos taurus", "bos"]),
 ("chicken",          ["gallus gallus", "gallus"]),
 ("mouse",            ["mus musculus", "mus"]),
 ("magpie",           ["pica pica", "pica", "corvidae"]),
 ("house_crow",       ["corvus splendens", "corvus", "corvidae"]),
 ("nc_crow",          ["corvus moneduloides", "corvus", "corvidae"]),
 ("raven",            ["corvus corax", "corvus", "corvidae"]),
 ("pigeon",           ["columba livia", "columba", "columbidae"]),
 ("grey_parrot",      ["psittacus erithacus", "psittacus", "psittacidae"]),
 ("cleaner_wrasse",   ["labroides dimidiatus", "labroides", "labridae"]),
 ("manta",            ["mobula birostris", "manta birostris", "mobula", "mobulidae"]),
 ("octopus",          ["octopus vulgaris", "octopus", "octopodidae"]),
 ("cuttlefish",       ["sepia officinalis", "sepia", "sepiidae"]),
 ("squid",            ["loligo vulgaris", "loligo", "loliginidae"]),
 ("honeybee",         ["apis mellifera", "apis", "apidae"]),
 ("bumblebee",        ["bombus terrestris", "bombus", "apidae"]),
 ("myrmica",          ["myrmica rubra", "myrmica", "myrmicinae", "formicidae"]),
 ("ghost_crab",       ["ocypode quadrata", "ocypode", "ocypodidae"]),
 ("crayfish",         ["astacus astacus", "astacus", "astacidae"]),
]

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "reincarnation-html/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

def node_uuid(name):
    q = urllib.parse.quote(name)
    d = get(f"{API}/nodes?build={BUILD}&filter_name={q}&page=0")
    items = d["_links"].get("items") or []
    if not items:
        return None
    return items[0]["href"].split("/nodes/")[1].split("?")[0]

def images_for(uuid):
    out = []
    for key in ("filter_node", "filter_clade"):
        try:
            d = get(f"{API}/images?build={BUILD}&embed_items=true&{key}={uuid}&page=0")
        except Exception:
            continue
        for it in d.get("_embedded", {}).get("items", []) or []:
            if not it:
                continue
            lic = (it.get("_links", {}).get("license") or {}).get("href", "")
            vec = it.get("_links", {}).get("vectorFile") or {}
            if not vec.get("href"):
                continue
            out.append({
                "uuid": it.get("uuid"),
                "license": lic,
                "href": vec["href"],
                "sizes": vec.get("sizes", ""),
                "attribution": it.get("attribution") or "",
                "contributor": (it.get("_links", {}).get("contributor") or {}).get("title", ""),
                "public_domain": lic in PD,
            })
        if out:
            break
    return out

def fetch_svg(url):
    req = urllib.request.Request(url, headers={"User-Agent": "reincarnation-html/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")

def extract(svg):
    m = re.search(r'viewBox="([^"]+)"', svg)
    vb = m.group(1) if m else None
    if not vb:
        w = re.search(r'width="([\d.]+)', svg); h = re.search(r'height="([\d.]+)', svg)
        if w and h:
            vb = f"0 0 {w.group(1)} {h.group(1)}"
    ds = re.findall(r'\sd="([^"]+)"', svg)
    tr = re.search(r'<g[^>]*transform="([^"]+)"', svg)
    return vb, ds, (tr.group(1) if tr else None)

result = {}
report = []
for cid, names in TARGETS:
    chosen = None
    used_name = None
    for nm in names:
        try:
            u = node_uuid(nm)
        except Exception as e:
            report.append(f"{cid}: node error {nm}: {e}"); continue
        if not u:
            continue
        imgs = images_for(u)
        if not imgs:
            continue
        pd = [i for i in imgs if i["public_domain"]]
        pool = pd if pd else imgs
        def area(i):
            try:
                w, h = i["sizes"].split("x"); return int(w) * int(h)
            except Exception:
                return 10**9
        pool.sort(key=area)
        chosen = pool[0]
        used_name = nm
        break
    if not chosen:
        report.append(f"{cid}: NO IMAGE FOUND")
        continue
    try:
        svg = fetch_svg(chosen["href"])
    except Exception as e:
        report.append(f"{cid}: svg fetch failed: {e}"); continue
    vb, ds, tr = extract(svg)
    if not vb or not ds:
        report.append(f"{cid}: parse failed"); continue
    result[cid] = {
        "taxon": used_name, "exact": used_name == names[0],
        "viewBox": vb, "paths": ds, "transform": tr,
        "uuid": chosen["uuid"], "license": chosen["license"],
        "pd": chosen["public_domain"],
        "attribution": chosen["attribution"], "contributor": chosen["contributor"],
        "bytes": len(svg), "npaths": len(ds),
    }
    report.append(f"{cid}: OK {used_name} exact={used_name==names[0]} pd={chosen['public_domain']} paths={len(ds)} {len(svg)}B")
    time.sleep(0.15)

json.dump(result, open(sys.argv[1], "w"), ensure_ascii=False)
print("\n".join(report))
print(f"\n{len(result)}/{len(TARGETS)} collected")
