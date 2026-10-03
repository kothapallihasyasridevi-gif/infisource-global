"""Revert the centred footer, and make the contact labels (Phone / Email /
Address / Suppliers) orange so they read as headings.
Run by .github/workflows/footer-tweak.yml, then removed."""
import io

P = "assets/css/polish.css"

CENTRED_MARK = "/* ---------- footer: centred ---------- */"
NEW_MARK = "/* ---------- footer contact labels in orange ---------- */"

NEW = ("\n" + NEW_MARK + "\n"
       ".foot-contact p::first-line{color:var(--orange-light);font-weight:800;"
       "letter-spacing:.02em;}\n")


def main():
    s = io.open(P, encoding="utf-8").read()

    i = s.find(CENTRED_MARK)
    if i >= 0:
        s = s[:i].rstrip() + "\n"
        print("centred-footer block removed")
    else:
        print("centred-footer block not present")

    if NEW_MARK not in s:
        s = s.rstrip() + "\n" + NEW
        print("orange label rule added")
    else:
        print("orange label rule already present")

    io.open(P, "w", encoding="utf-8").write(s)

    after = io.open(P, encoding="utf-8").read()
    print("centring gone:", CENTRED_MARK not in after)
    print("orange present:", NEW_MARK in after)
    print("size:", len(after))


if __name__ == "__main__":
    main()
