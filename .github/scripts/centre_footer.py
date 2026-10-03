"""Centre the site footer. Appends rules to polish.css (loaded last, so they win).
Run by .github/workflows/centre-footer.yml, then removed."""
import io

P = "assets/css/polish.css"

CSS = """

/* ---------- footer: centred ---------- */
footer.site-foot{text-align:center;}
.foot-grid{display:grid;grid-template-columns:repeat(3,auto);justify-content:center;align-items:start;gap:30px 56px;}
.foot-brand{grid-column:1/-1;align-items:center;}
.foot-brand p{margin-left:auto;margin-right:auto;}
.foot-links{align-items:center;}
.foot-contact{text-align:center;}
.foot-note{justify-content:center;text-align:center;gap:22px;}
@media(max-width:820px){.foot-grid{grid-template-columns:1fr;gap:26px;}}
"""


def main():
    s = io.open(P, encoding="utf-8").read()
    if "footer: centred" in s:
        print("already applied - nothing to do")
        return
    io.open(P, "a", encoding="utf-8").write(CSS)
    after = io.open(P, encoding="utf-8").read()
    print("appended chars:", len(CSS))
    print("marker present:", "footer: centred" in after)
    print("file size now:", len(after))


if __name__ == "__main__":
    main()
