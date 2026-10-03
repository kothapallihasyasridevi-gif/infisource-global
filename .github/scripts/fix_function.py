"""Fix the sending function:
  1. install its dependency at build time (root package.json + build command)
  2. wrap the handler so a failure reports the actual error instead of a blank one
Run by .github/workflows/fix-function.yml, then removed."""
import io

P = "netlify/functions/send.mjs"

OPEN = "export default async (req) => {\n"
END = ('    status: 200, headers: { "content-type": "application/json" },\n'
       '  });\n};')

CATCH = ('    status: 200, headers: { "content-type": "application/json" },\n'
         '  });\n'
         '  } catch (err) {\n'
         '    return new Response(JSON.stringify({ ok: false, error: String((err && err.message) || err) }), {\n'
         '      status: 200, headers: { "content-type": "application/json" },\n'
         '    });\n'
         '  }\n};')

ROOT_PKG = ('{\n  "name": "infisource-global",\n  "private": true,\n'
            '  "dependencies": {\n    "nodemailer": "^6.9.13"\n  }\n}\n')

TOML = ('[build]\n  command = "npm install"\n  publish = "."\n'
        '  functions = "netlify/functions"\n')


def main():
    s = io.open(P, encoding="utf-8").read()

    if s.count(OPEN) != 1:
        raise SystemExit("ABORT: handler opening not found")
    if "try {" not in s:
        s = s.replace(OPEN, OPEN + "  try {\n")

    if s.count(END) != 1:
        raise SystemExit("ABORT: handler ending not found")
    if "catch (err)" not in s:
        s = s.replace(END, CATCH)

    io.open(P, "w", encoding="utf-8").write(s)
    print("try/catch added:", "catch (err)" in s)

    io.open("package.json", "w", encoding="utf-8").write(ROOT_PKG)
    print("root package.json written")

    io.open("netlify.toml", "w", encoding="utf-8").write(TOML)
    print("netlify.toml updated")


if __name__ == "__main__":
    main()
