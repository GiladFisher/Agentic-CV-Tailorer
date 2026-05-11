"""Fetch a LinkedIn job posting by URL and save it to the jobs/ folder."""

import json
import re
import sys
from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text[:40]


def extract_linkedin_id(url: str) -> str:
    m = re.search(r"/view/(\d+)", url)
    if not m:
        raise ValueError(f"Cannot extract job ID from URL: {url}")
    return m.group(1)


def fetch_and_parse(linkedin_id: str) -> dict:
    api_url = f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{linkedin_id}"
    r = requests.get(api_url, headers=HEADERS, timeout=20)

    if r.status_code == 429:
        raise RuntimeError("LinkedIn rate-limited the request — wait a minute and retry.")
    if r.status_code != 200:
        raise RuntimeError(f"LinkedIn returned HTTP {r.status_code}.")

    soup = BeautifulSoup(r.text, "html.parser")

    # Primary: JSON-LD structured data (most reliable)
    for tag in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(tag.string or "")
            if data.get("@type") == "JobPosting":
                loc = data.get("jobLocation", {})
                if isinstance(loc, list):
                    loc = loc[0] if loc else {}
                address = loc.get("address", {})
                location = (
                    address.get("addressLocality", "")
                    or address.get("addressRegion", "")
                    or address.get("addressCountry", "")
                )
                raw_desc = data.get("description", "")
                description = BeautifulSoup(raw_desc, "html.parser").get_text(
                    separator="\n", strip=True
                )
                return {
                    "title": data.get("title", "").strip(),
                    "company": data.get("hiringOrganization", {}).get("name", "").strip(),
                    "location": location.strip(),
                    "description": description,
                }
        except (json.JSONDecodeError, AttributeError):
            continue

    # Fallback: HTML parsing
    def first_text(*selectors, default=""):
        for sel in selectors:
            el = soup.select_one(sel)
            if el:
                return el.get_text(strip=True)
        return default

    title = first_text(
        ".top-card-layout__title",
        ".topcard__title",
        "h1",
        "h2",
        default="Unknown Title",
    )
    company = first_text(
        ".topcard__org-name-link",
        "a[data-tracking-control-name='public_jobs_topcard-org-name']",
        ".topcard__flavor:not(.topcard__flavor--bullet)",
        default="Unknown Company",
    )
    location = first_text(
        ".topcard__flavor--bullet",
        ".topcard__flavor--bullet span",
        default="",
    )
    desc_el = (
        soup.select_one(".show-more-less-html__markup")
        or soup.select_one(".description__text")
        or soup.select_one("[class*='description']")
    )
    description = (
        desc_el.get_text(separator="\n", strip=True) if desc_el else ""
    )

    return {
        "title": title,
        "company": company,
        "location": location,
        "description": description,
    }


def main():
    if len(sys.argv) != 2:
        print("Usage: python src/fetch_job.py <linkedin-url>")
        sys.exit(1)

    url = sys.argv[1]

    try:
        linkedin_id = extract_linkedin_id(url)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    print(f"Fetching job {linkedin_id}...")

    try:
        data = fetch_and_parse(linkedin_id)
    except RuntimeError as e:
        print(f"Error: {e}")
        sys.exit(1)

    company_slug = slugify(data["company"])
    title_slug = slugify(data["title"])
    job_id = f"{linkedin_id}__{company_slug}__{title_slug}"

    job_dir = Path("jobs") / job_id
    if job_dir.exists():
        print(f"Already ingested: {job_id}")
        print(f"job-id: {job_id}")
        sys.exit(0)

    job_dir.mkdir(parents=True)

    job_record = {
        "id": job_id,
        "linkedin_id": linkedin_id,
        "title": data["title"],
        "company": data["company"],
        "location": data["location"],
        "url": url,
        "date_added": datetime.now().strftime("%Y-%m-%d"),
        "description": data["description"],
    }
    (job_dir / "job.json").write_text(
        json.dumps(job_record, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    state_file = Path("state") / "seen_jobs.json"
    state = {}
    if state_file.exists():
        try:
            state = json.loads(state_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    state[job_id] = {
        "date_added": job_record["date_added"],
        "status": "ingested",
        "title": data["title"],
        "company": data["company"],
    }
    state_file.write_text(
        json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    print(f"Saved:    jobs/{job_id}/")
    print(f"Title:    {data['title']}")
    print(f"Company:  {data['company']}")
    print(f"Location: {data['location']}")
    print(f"job-id: {job_id}")


if __name__ == "__main__":
    main()
