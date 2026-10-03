"""Footer: put the bold back on the Phone / Email / Address / Suppliers labels.
Run by .github/workflows/footer-bold-labels.yml, then removed."""
import io

P = "assets/css/polish.css"

OLD = ".foot-contact p::first-line{color:var(--orange-light);letter-spacing:.02em;}"
NEW = (".foot-contact p::first-line{color:var(--orange-light);font-weight:800;"
       "letter-spacing:.02em;}")


def main():
    s = io.open(P, encoding="utf-8").read()
    if OLD not in s:
        raise SystemExit("ABORT: expected label rule not found")
    s = s.replace(OLD, NEW)
    io.open(P, "w", encoding="utf-8").write(s)

    after = io.open(P, encoding="utf-8").read()
    print("labels bold again:", NEW in after)
    print("headings still 900:", ".foot-h{font-weight:900;}" in after)
    print("size:", len(after))


if __name__ == "__main__":
    main()
