"""One-off patch: point the vendor form's mailto at info@infisource.in
and rebuild the email body so it reads as a document.
Run by .github/workflows/apply-forms-patch.yml, then removed."""
import io
import re

P = "assets/js/forms.js"

NEW_FN = r'''  function mailtoFallback(params, subject){
    var SECTIONS = [
      ['BUSINESS', ['company_name','brand_name','year_est','entity_type','website','business_types','business_other']],
      ['CONTACT', ['contact_name','designation','mobile','email','address','city','state','pincode']],
      ['TAX AND COMPLIANCE', ['gstin','pan','msme','udyam_no','other_certs','turnover']],
      ['WHAT WE SUPPLY', ['categories','other_categories','products_text','key_clients']],
      ['TERMS', ['payment_terms','lead_time','description']]
    ];
    var LABEL = {
      company_name:'Registered company name', brand_name:'Trade / brand name',
      year_est:'Year established', entity_type:'Entity type', website:'Website',
      business_types:'Business type', business_other:'Business (other)',
      contact_name:'Contact person', designation:'Designation', mobile:'Mobile / WhatsApp',
      email:'Email', address:'Registered address', city:'City', state:'State', pincode:'PIN code',
      gstin:'GSTIN', pan:'PAN', msme:'MSME / Udyam registered', udyam_no:'Udyam number',
      other_certs:'Other certifications', turnover:'Annual turnover',
      categories:'Categories', other_categories:'Other categories',
      products_text:'Products / brands', key_clients:'Key clients',
      payment_terms:'Payment terms', lead_time:'Lead time', description:'About the business'
    };
    var CATNAME = {
      'mep-solutions':'MEP Solutions', 'facility-maintenance':'Facility Maintenance',
      'safety-and-fire-protection':'Safety & Fire Protection', 'hvac-and-air-quality':'HVAC & Air Quality',
      'security-and-access-control':'Security & Access Control', 'stationery-and-office-supplies':'Stationery & Office Supplies',
      'housekeeping':'Housekeeping', 'pantry-and-cafeteria':'Pantry & Cafeteria',
      'office-furniture':'Office Furniture', 'office-appliances':'Office Appliances',
      'it-and-networking':'IT & Networking', 'av-and-meeting-rooms':'AV & Meeting Rooms',
      'printing-and-branding':'Printing & Branding', 'gifting-and-uniforms':'Gifting & Uniforms',
      'packaging-and-storage':'Packaging & Storage', 'plants-and-landscaping':'Plants & Landscaping',
      'recreation-and-engagement':'Recreation & Engagement', 'sustainability':'Sustainability'
    };
    function pretty(v, k){
      var parts = String(v).split('|').filter(Boolean);
      if (k === 'categories') parts = parts.map(function(s){ return CATNAME[s] || s; });
      return parts.join(', ');
    }
    var out = [];
    out.push('VENDOR REGISTRATION');
    out.push('===================');
    out.push('');
    out.push('Company: ' + (params.company_name || '-'));
    out.push('Submitted from: infisource.in');
    out.push('');
    out.push('** ACTION REQUIRED **');
    out.push('Please ATTACH your GST certificate, PAN card, cancelled');
    out.push('cheque and catalogue to this email before sending it.');
    out.push('');
    SECTIONS.forEach(function(sec){
      var rows = [];
      sec[1].forEach(function(k){
        var v = params[k];
        if (v === undefined || v === null || v === '') return;
        rows.push((LABEL[k] || k) + ': ' + pretty(v, k));
      });
      if (!rows.length) return;
      out.push(sec[0]);
      out.push('--------------------');
      out = out.concat(rows);
      out.push('');
    });
    var text = out.join('\n');
    if (text.length > 1700) text = text.slice(0, 1700) + '\n\n(remainder omitted - please email us the full details)';
    var url = 'mailto:info@infisource.in?subject=' + encodeURIComponent(subject) +
              '&body=' + encodeURIComponent(text);
    w.location.href = url;
  }'''

OLD_NOTE = ("'Your email app should open with all your details pre-filled. Please attach your "
            "catalogue and certificates to that email and send it. ' +\n"
            "            'Once the online form is connected to our sheet, submissions will be saved automatically.'")

NEW_NOTE = ("'Your email app should now open with all your details filled in and addressed to "
            "info@infisource.in. ' +\n"
            "            'Please attach your GST certificate, PAN card, cancelled cheque and "
            "catalogue, then press Send. ' +\n"
            "            'Once we receive it, our team will review your registration and reply on "
            "the same email.'")


def main():
    s = io.open(P, encoding="utf-8").read()
    original = s

    s, n1 = re.subn(r"function mailtoFallback\(params, subject\)\{.*?\n  \}",
                    lambda m: NEW_FN, s, count=1, flags=re.S)

    n2 = 1 if OLD_NOTE in s else 0
    s = s.replace(OLD_NOTE, NEW_NOTE)

    io.open(P, "w", encoding="utf-8").write(s)

    print("mailtoFallback replaced:", n1)
    print("success note replaced:", n2)
    print("file changed:", s != original)
    print("address is info@:", "mailto:info@infisource.in" in s)
    print("old address gone:", "infisourceglobal.in" not in s)

    if n1 != 1:
        raise SystemExit("mailtoFallback was not replaced - aborting so nothing half-applies")


if __name__ == "__main__":
    main()
