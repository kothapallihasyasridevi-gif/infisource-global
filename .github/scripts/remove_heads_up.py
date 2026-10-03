"""Remove the 'Heads up ... press Send' note from the vendor page.
Run by .github/workflows/remove-heads-up.yml, then removed."""
import io
import re

P = "vendor.html"

PAT = re.compile(r'[ \t]*<p class="vf-email-note"[\s\S]*?</p>\n')


def main():
    s = io.open(P, encoding="utf-8").read()
    print("note occurrences before:", s.count("vf-email-note"))

    s2, n = PAT.subn("", s, count=1)
    print("removed:", n)
    if n != 1:
        raise SystemExit("ABORT: expected to remove exactly one note block")

    io.open(P, "w", encoding="utf-8").write(s2)

    after = io.open(P, encoding="utf-8").read()
    print("note gone:", "vf-email-note" not in after)
    print("submit button intact:", 'id="vf-submit"' in after)
    print("size:", len(after))


if __name__ == "__main__":
    main()
