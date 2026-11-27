
import re
from urllib.parse import urlparse
import ipaddress

SHORTENERS = {
    "bit.ly", "tinyurl.com", "t.co",
    "goo.gl", "is.gd", "cutt.ly",
    "rb.gy", "shorturl.at"
}

SUSPICIOUS_TLDS = {
    "xyz", "top", "click", "work",
    "loan", "gq", "tk", "ml", "cf"
}


def analyze_url(url):
    url = str(url).strip()

    if not url:
        return {
            "risk_score": 0,
            "flags": [],
            "error": "No URL provided"
        }

    parsed = urlparse(
        url if "://" in url else "http://" + url
    )

    domain = parsed.hostname or ""
    flags = []
    score = 0

    if len(url) > 75:
        flags.append("Unusually long URL")
        score += 15

    if url.count(".") >= 4:
        flags.append("Excessive dots or subdomains")
        score += 15

    if "@" in url:
        flags.append("Contains @ symbol")
        score += 20

    try:
        ipaddress.ip_address(domain)
        flags.append("Uses IP address instead of domain")
        score += 25
    except ValueError:
        pass

    if domain.lower() in SHORTENERS:
        flags.append("Uses URL shortener")
        score += 20

    tld = domain.rsplit(".", 1)[-1].lower() if "." in domain else ""

    if tld in SUSPICIOUS_TLDS:
        flags.append("Uncommon or suspicious TLD")
        score += 15

    if re.search(r"%[0-9a-fA-F]{2}", url):
        flags.append("Contains encoded characters")
        score += 10

    if "-" in domain:
        flags.append("Hyphenated domain")
        score += 5

    return {
        "risk_score": min(score, 100),
        "flags": flags
    }


if __name__ == "__main__":
    test_url = "http://secure-login-account.xyz/verify"
    result = analyze_url(test_url)

    print("URL:", test_url)
    print("Analysis:", result)
