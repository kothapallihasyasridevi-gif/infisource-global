"""Add a short note so vendors know the registration is only complete
once they actually send the email their mail app opens.
Run by .github/workflows/apply-site-note.yml, then removed."""
import io

# ---- vendor.html ----------------------------------------------------------
P_HTML = "vendor.html"

NOTE = ('<p class="vf-email-note" style="margin:0 0 14px;font-size:13px;'
        'line-height:1.55;color:#5C5A54;">Heads up: pressing Submit opens your email app '
        'with your details already filled in. Attach your documents and press '
        '<b style="color:#1B1A18;">Send</b> &mdash; your registration reaches us only when '
        'you send that email.</p>\n')

ANCHOR = '<div class="vf-submit-row" style="margin-top:26px;">'
OLD_H = '<h2>Registration Received</h2>'
NEW_H = '<h2>One step left</h2>'
OLD_P = ('<p id="vf-succ-note">Thank you for registering with InfiSource Global. '
         'Our team has received your details and will reach out with next steps.</p>')
NEW_P = ('<p id="vf-succ-note">One step left: your email app should now be open with your '
         'details filled in. Attach your documents and press Send &mdash; we receive your '
         'registration only once you send that email.</p>')

# ---- assets/js/forms.js ---------------------------------------------------
P_JS = "assets/js/forms.js"

OLD_JS = ("'Your email app should now open with all your details filled in and addressed to "
          "info@infisource.in. ' +\n"
          "            'Please attach your GST certificate, PAN card, cancelled cheque and "
          "catalogue, then press Send. ' +\n"
          "            'Once we receive it, our team will review your registration and reply on "
          "the same email.'")

NEW_JS = ("'One step left: your email app should now be open with your details filled in. ' +\n"
          "            'Attach your GST certificate, PAN card, cancelled cheque and catalogue, "
          "then press Send. ' +\n"
          "            'We receive your registration only once you send that email.'")


def must(count, label):
    if count != 1:
        raise SystemExit("ABORT: expected exactly 1 match for %s, found %d" % (label, count))


def main():
    s = io.open(P_HTML, encoding="utf-8").read()
    before = s

    must(s.count(ANCHOR), "submit-row anchor")
    s = s.replace(ANCHOR, NOTE + "            " + ANCHOR)

    must(s.count(OLD_H), "success heading")
    s = s.replace(OLD_H, NEW_H)

    must(s.count(OLD_P), "success paragraph")
    s = s.replace(OLD_P, NEW_P)

    io.open(P_HTML, "w", encoding="utf-8").write(s)
    print("vendor.html changed:", s != before)

    t = io.open(P_JS, encoding="utf-8").read()
    before2 = t
    must(t.count(OLD_JS), "success note in forms.js")
    t = t.replace(OLD_JS, NEW_JS)
    io.open(P_JS, "w", encoding="utf-8").write(t)
    print("forms.js changed:", t != before2)

    # sanity
    print("note present:", "Heads up: pressing Submit" in s)
    print("heading changed:", "<h2>One step left</h2>" in s)
    print("js updated:", "only once you send that email" in t)


if __name__ == "__main__":
    main()
