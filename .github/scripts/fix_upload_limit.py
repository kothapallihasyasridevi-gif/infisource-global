"""Fix: keep vendor uploads under the Netlify Function payload ceiling (~4 MB),
so a large submission can never fail silently.
Run by .github/workflows/fix-upload-limit.yml, then removed."""
import io

P = "assets/js/forms.js"

CAPS = [
    ("'#catalog-zone', '#catalog-list', catalog, { multiple: true, "
     "accept: '.pdf,.png,.jpg,.jpeg,.webp,.xlsx,.xls,.csv,.doc,.docx', maxMB: 10, maxFiles: 6 }",
     "'#catalog-zone', '#catalog-list', catalog, { multiple: true, "
     "accept: '.pdf,.png,.jpg,.jpeg,.webp,.xlsx,.xls,.csv,.doc,.docx', maxMB: 3, maxFiles: 4 }"),
    ("'#gstc-zone', '#gstc-list', gstCert, { accept: '.pdf,.png,.jpg,.jpeg', maxMB: 8, maxFiles: 1 }",
     "'#gstc-zone', '#gstc-list', gstCert, { accept: '.pdf,.png,.jpg,.jpeg', maxMB: 2, maxFiles: 1 }"),
    ("'#msme-zone', '#msme-list', msmeCert, { accept: '.pdf,.png,.jpg,.jpeg', maxMB: 8, maxFiles: 1 }",
     "'#msme-zone', '#msme-list', msmeCert, { accept: '.pdf,.png,.jpg,.jpeg', maxMB: 2, maxFiles: 1 }"),
    ("'#deal-zone', '#deal-list', dealCert, { accept: '.pdf,.png,.jpg,.jpeg', maxMB: 8, maxFiles: 2 }",
     "'#deal-zone', '#deal-list', dealCert, { accept: '.pdf,.png,.jpg,.jpeg', maxMB: 2, maxFiles: 2 }"),
]

ANCHOR = "      submitToFunction(params, files, function(res){"

GUARD = """      var totalBytes = files.reduce(function(n, f){ return n + (f.file && f.file.size ? f.file.size : 0); }, 0);
      if (totalBytes > 4 * 1048576){
        btn.disabled = false; btn.textContent = 'Submit Registration';
        toast('Your documents total ' + fmtSize(totalBytes) + '. The limit is 4 MB - please compress them, or email larger files to info@infisource.in.');
        return;
      }
"""


def main():
    s = io.open(P, encoding="utf-8").read()

    for old, new in CAPS:
        if s.count(old) != 1:
            raise SystemExit("ABORT: expected 1 match for cap rule:\n" + old[:70])
        s = s.replace(old, new)
    print("per-file caps lowered:", all(new.split("maxMB: ")[1][0] in s for _, new in CAPS))

    if s.count(ANCHOR) != 1:
        raise SystemExit("ABORT: submitToFunction call site not found")
    s = s.replace(ANCHOR, GUARD + ANCHOR)
    print("total-size guard added:", "The limit is 4 MB" in s)

    io.open(P, "w", encoding="utf-8").write(s)
    print("size:", len(s))


if __name__ == "__main__":
    main()
