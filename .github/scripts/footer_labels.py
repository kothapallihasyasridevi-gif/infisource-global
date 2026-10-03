"""Footer: make the column headings clearly bold, and take the bold off the
Phone / Email / Address / Suppliers labels so they stop competing with them.
Run by .github/workflows/footer-labels.yml, then removed."""
import io

P = "assets/css/polish.css"

OLD = (".foot-contact p::first-line{color:var(--orange-light);font-weight:800;"
       "letter-spacing:.02em;}")

NEW = (".foot-h{font-weight:900;}\n"
       ".foot-contact p::first-line{color:var(--orange-light);letter-spacing:.02em;}")


def main():
    s = io.open(P, encoding="utf-8").read()
    if OLD not in s:
        raise SystemExit("ABORT: expected label rule not found")
    s = s.replace(OLD, NEW)
    io.open(P, "w", encoding="utf-8").write(s)

    after = io.open(P, encoding="utf-8").read()
    print("label bold removed:", "font-weight:800;letter-spacing:.02em" not in after)
    print("headings set to 900:", ".foot-h{font-weight:900;}" in after)
    print("labels still orange:", ".foot-contact p::first-line{color:var(--orange-light)" in after)
    print("size:", len(after))


if __name__ == "__main__":
    main()
