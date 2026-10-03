"""Wire the vendor form to the Netlify function so submissions (with documents)
are emailed to info@ directly. Leaves the contact form untouched.
Run by .github/workflows/wire-vendor-form.yml, then removed."""
import io

PJS = "assets/js/forms.js"
PH = "vendor.html"

NEWFN = """  function submitToFunction(params, files, done){
    var fd = new FormData();
    Object.keys(params).forEach(function(k){
      fd.append(k, params[k] == null ? '' : String(params[k]));
    });
    files.forEach(function(f){
      if (f.file) fd.append('documents', f.file, f.name || f.file.name || 'document');
    });
    fetch('/.netlify/functions/send', { method: 'POST', body: fd })
      .then(function(r){ return r.json(); })
      .then(function(j){ done(j && j.ok ? { ok: true } : { error: (j && j.error) || 'Server error' }); })
      .catch(function(){ done({ mailto: true }); });
  }

"""

ANCHOR_FN = "  function submitToSheet(params, files, done){"
VENDOR_CALL = "      submitToSheet(params, files, function(res){"
NEW_CALL = "      submitToFunction(params, files, function(res){"

OLD_OK = ("          try { localStorage.removeItem(DKEY); } catch(e){}\n"
          "          $('#vf-success').classList.add('show');")
NEW_OK = ("          try { localStorage.removeItem(DKEY); } catch(e){}\n"
          "          $('#vf-succ-note').textContent = 'Thank you. Your registration has been "
          "received and our team will review it shortly. We will write to you at the email "
          "address you gave us.';\n"
          "          $('#vf-success').classList.add('show');")

OLD_H = "<h2>One step left</h2>"
NEW_H = "<h2>Registration received</h2>"
OLD_P = ('<p id="vf-succ-note">One step left: your email app should now be open with your '
         'details filled in. Attach your documents and press Send &mdash; we receive your '
         'registration only once you send that email.</p>')
NEW_P = ('<p id="vf-succ-note">Thank you. Your registration has been received and our team '
         'will review it shortly.</p>')


def one(count, what):
    if count != 1:
        raise SystemExit("ABORT: expected 1 match for %s, found %d" % (what, count))


def main():
    s = io.open(PJS, encoding="utf-8").read()

    one(s.count(ANCHOR_FN), "submitToSheet definition")
    s = s.replace(ANCHOR_FN, NEWFN + ANCHOR_FN)

    i = s.find(VENDOR_CALL)
    if i < 0:
        raise SystemExit("ABORT: vendor call site not found")
    s = s[:i] + NEW_CALL + s[i + len(VENDOR_CALL):]
    print("vendor call switched:", s.count(NEW_CALL) == 1)

    one(s.count(OLD_OK), "vendor success branch")
    s = s.replace(OLD_OK, NEW_OK)

    io.open(PJS, "w", encoding="utf-8").write(s)
    print("forms.js updated:", "submitToFunction" in s)

    h = io.open(PH, encoding="utf-8").read()
    one(h.count(OLD_H), "heading")
    h = h.replace(OLD_H, NEW_H)
    one(h.count(OLD_P), "success paragraph")
    h = h.replace(OLD_P, NEW_P)
    io.open(PH, "w", encoding="utf-8").write(h)
    print("vendor.html updated:", NEW_H in h and NEW_P in h)


if __name__ == "__main__":
    main()
