import pandas as pd
import time
from scholarly import scholarly

# ==============================
# CONFIG
# ==============================
INPUT_CSV = "Scientist Google Scholar and H-index Data Submission (Responses) - Form responses .csv"
OUTPUT_CSV = "scholar_metrics_fetched.csv"
DELAY_SECONDS = 10  # IMPORTANT: avoids Google blocking

print("📄 Loading input CSV...")
df = pd.read_csv(INPUT_CSV)

# ==============================
# HELPER FUNCTION
# ==============================
def extract_author_id(profile_url):
    """
    Extracts Google Scholar author ID from profile URL
    Example:
    https://scholar.google.com/citations?user=XXXXXXX&hl=en
    """
    if isinstance(profile_url, str) and "user=" in profile_url:
        return profile_url.split("user=")[1].split("&")[0]
    return None

# ==============================
# FETCH METRICS
# ==============================
fetched_hindex = []
fetched_citations = []

print("🔍 Starting Google Scholar metric extraction...\n")

for idx, row in df.iterrows():
    name = row.get("Name of the Scientist", f"Scientist {idx+1}")
    profile_url = row.get("Google Scholar Profile Link", None)

    print(f"➡️ Processing: {name}")

    author_id = extract_author_id(profile_url)

    if author_id is None:
        print("   ❌ Invalid or missing Scholar link")
        fetched_hindex.append(None)
        fetched_citations.append(None)
        continue

    try:
        author = scholarly.search_author_id(author_id)
        author = scholarly.fill(author)

        hindex = author.get("hindex", None)
        citations = author.get("citedby", None)

        fetched_hindex.append(hindex)
        fetched_citations.append(citations)

        print(f"   ✅ h-index: {hindex} | citations: {citations}")

        time.sleep(DELAY_SECONDS)

    except Exception as e:
        print(f"   ⚠️ Error fetching data: {e}")
        fetched_hindex.append(None)
        fetched_citations.append(None)
        time.sleep(DELAY_SECONDS)

# ==============================
# SAVE OUTPUT
# ==============================
df["Fetched H-index"] = fetched_hindex
df["Fetched Citations"] = fetched_citations

df.to_csv(OUTPUT_CSV, index=False)

print("\n✅ Fetching complete!")
print(f"📁 Output saved as: {OUTPUT_CSV}")