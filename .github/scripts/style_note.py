"""Style the vendor-page note: italic, with more space above it so it stands out.
Run by .github/workflows/style-vendor-note.yml, then removed."""
import io

P = "vendor.html"

OLD = ('<p class="vf-email-note" style="margin:0 0 14px;font-size:13px;'
       'line-height:1.55;color:#5C5A54;">')

NEW = ('<p class="vf-email-note" style="margin:22px 0 12px;font-size:13px;'
       'line-height:1.55;color:#5C5A54;font-style:italic;">')


def main():
    s = io.open(P, encoding="utf-8").read()
    n = s.count(OLD)
    print("note anchor matches:", n)
    if n != 1:
        raise SystemExit("ABORT: expected exactly 1 match, found %d" % n)

    s = s.replace(OLD, NEW)
    io.open(P, "w", encoding="utf-8").write(s)

    print("italic applied:", "font-style:italic" in s)
    print("top margin raised:", 'margin:22px 0 12px' in s)
    print("old style gone:", OLD not in s)


if __name__ == "__main__":
    main()
