// Netlify Function: receives the vendor registration form (with documents)
// and emails it to info@infisource.in with the files attached.
// Reads the Zoho app password from the ZOHO_APP_PASSWORD environment variable.

import nodemailer from "nodemailer";

const TO = "info@infisource.in";
const FROM = "info@infisource.in";
const FROM_NAME = "InfiSource Vendor Portal";
const SMTP_HOST = "smtp.zoho.in";

const SECTIONS = [
  ["Business", ["company_name", "brand_name", "year_est", "entity_type", "website", "business_types", "business_other"]],
  ["Contact", ["contact_name", "designation", "mobile", "email", "address", "city", "state", "pincode"]],
  ["Tax and compliance", ["gstin", "pan", "msme", "udyam_no", "other_certs", "turnover"]],
  ["What they supply", ["categories", "other_categories", "products_text", "key_clients"]],
  ["Terms", ["payment_terms", "lead_time", "description"]],
];

const LABEL = {
  company_name: "Registered company name", brand_name: "Trade / brand name",
  year_est: "Year established", entity_type: "Entity type", website: "Website",
  business_types: "Business type", business_other: "Business (other)",
  contact_name: "Contact person", designation: "Designation", mobile: "Mobile / WhatsApp",
  email: "Email", address: "Registered address", city: "City", state: "State", pincode: "PIN code",
  gstin: "GSTIN", pan: "PAN", msme: "MSME / Udyam registered", udyam_no: "Udyam number",
  other_certs: "Other certifications", turnover: "Annual turnover",
  categories: "Categories", other_categories: "Other categories",
  products_text: "Products / brands", key_clients: "Key clients",
  payment_terms: "Payment terms", lead_time: "Lead time", description: "About the business",
};

const CATNAME = {
  "mep-solutions": "MEP Solutions", "facility-maintenance": "Facility Maintenance",
  "safety-and-fire-protection": "Safety & Fire Protection", "hvac-and-air-quality": "HVAC & Air Quality",
  "security-and-access-control": "Security & Access Control", "stationery-and-office-supplies": "Stationery & Office Supplies",
  "housekeeping": "Housekeeping", "pantry-and-cafeteria": "Pantry & Cafeteria",
  "office-furniture": "Office Furniture", "office-appliances": "Office Appliances",
  "it-and-networking": "IT & Networking", "av-and-meeting-rooms": "AV & Meeting Rooms",
  "printing-and-branding": "Printing & Branding", "gifting-and-uniforms": "Gifting & Uniforms",
  "packaging-and-storage": "Packaging & Storage", "plants-and-landscaping": "Plants & Landscaping",
  "recreation-and-engagement": "Recreation & Engagement", "sustainability": "Sustainability",
};

const esc = (s) =>
  String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

function pretty(value, key) {
  let parts = String(value).split("|").filter(Boolean);
  if (key === "categories") parts = parts.map((s) => CATNAME[s] || s);
  return parts.join(", ");
}

function buildHtml(fields) {
  const rows = [];
  for (const [heading, keys] of SECTIONS) {
    const inner = [];
    for (const k of keys) {
      const v = fields[k];
      if (v === undefined || v === null || v === "") continue;
      inner.push(
        `<tr><td style="padding:7px 14px 7px 0;color:#5C5A54;font-size:13.5px;vertical-align:top;width:38%;">${esc(LABEL[k] || k)}</td>` +
        `<td style="padding:7px 0;color:#1B1A18;font-size:13.5px;font-weight:600;">${esc(pretty(v, k))}</td></tr>`
      );
    }
    if (!inner.length) continue;
    rows.push(
      `<tr><td colspan="2" style="padding:20px 0 4px;font-size:11.5px;letter-spacing:1.6px;text-transform:uppercase;color:#C25A0E;font-weight:800;border-top:1px solid #E4DFD3;">${esc(heading)}</td></tr>` +
      inner.join("")
    );
  }
  const company = esc(fields.company_name || "New vendor");
  return `<!doctype html><html><body style="margin:0;padding:0;background:#F5F2EC;">
<div style="font-family:Arial,Helvetica,sans-serif;background:#F5F2EC;padding:24px 14px;">
  <div style="max-width:660px;margin:0 auto;background:#ffffff;border-radius:14px;overflow:hidden;border:1px solid #E4DFD3;">
    <div style="background:#1B1A18;padding:22px 30px;">
      <div style="font-size:17px;font-weight:700;color:#ffffff;">InfiSource Global</div>
      <div style="font-size:11.5px;letter-spacing:1.6px;text-transform:uppercase;color:#F29D55;margin-top:5px;">Vendor registration</div>
    </div>
    <div style="background:#FCE9D9;padding:13px 30px;font-size:13px;color:#7a4a1e;">
      <b>A new vendor has registered.</b> Details and documents are below.
    </div>
    <div style="padding:6px 30px 30px;">
      <h1 style="font-size:20px;color:#1B1A18;margin:22px 0 2px;">${company}</h1>
      <div style="font-size:12.5px;color:#8A867C;margin-bottom:6px;">Submitted from infisource.in</div>
      <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="border-collapse:collapse;">${rows.join("")}</table>
    </div>
    <div style="background:#F5F2EC;padding:16px 30px;font-size:12.5px;color:#5C5A54;border-top:1px solid #E4DFD3;">
      Reply to this email to reach the vendor directly.
    </div>
  </div>
</div>
</body></html>`;
}

export default async (req) => {
  if (req.method !== "POST") {
    return new Response("Method not allowed", { status: 405 });
  }

  const form = await req.formData();
  const fields = {};
  const attachments = [];

  for (const [key, value] of form.entries()) {
    if (typeof value === "string") {
      fields[key] = value;
    } else if (value && typeof value === "object" && value.name) {
      const buf = Buffer.from(await value.arrayBuffer());
      if (buf.length) {
        attachments.push({
          filename: value.name,
          content: buf,
          contentType: value.type || "application/octet-stream",
        });
      }
    }
  }

  if (!fields.company_name && !fields.contact_name) {
    return new Response(JSON.stringify({ ok: false, error: "empty submission" }), {
      status: 400, headers: { "content-type": "application/json" },
    });
  }

  const pass = process.env.ZOHO_APP_PASSWORD;
  if (!pass) {
    return new Response(JSON.stringify({ ok: false, error: "mail not configured" }), {
      status: 500, headers: { "content-type": "application/json" },
    });
  }

  const transporter = nodemailer.createTransport({
    host: SMTP_HOST, port: 465, secure: true,
    auth: { user: FROM, pass },
  });

  await transporter.sendMail({
    from: `"${FROM_NAME}" <${FROM}>`,
    to: TO,
    replyTo: fields.email || undefined,
    subject: "Vendor Registration - " + (fields.company_name || "New vendor"),
    html: buildHtml(fields),
    attachments,
  });

  return new Response(JSON.stringify({ ok: true, files: attachments.length }), {
    status: 200, headers: { "content-type": "application/json" },
  });
};
