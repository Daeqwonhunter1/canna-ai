import argparse
import json
from pathlib import Path

from app.scraper.leafly_scraper import LeaflyScraper


OUTPUT_DIR = Path("scraped_output")


def run(strain_slugs: list[str]) -> None:

    OUTPUT_DIR.mkdir(exist_ok=True)

    good = []
    needs_review = []

    scraper = LeaflyScraper()

    total = len(strain_slugs)

    for done, slug in enumerate(strain_slugs, start=1):

        print(
            f"[{done}/{total}] "
            f"scraping strain: {slug}"
        )

        try:

            profile = scraper.get_strain(slug)

        except Exception as e:

            print(
                f"[ERROR] Failed to scrape "
                f"{slug}: {e}"
            )

            needs_review.append({
                "slug": slug,
                "reason": str(e),
            })

            continue

        print(f"Profile: {profile}")

        if profile is None:

            needs_review.append({
                "slug": slug,
                "reason": (
                    "fetch or extraction failed"
                ),
            })

            continue

        # Depending on your confidence logic
        if profile:

            good.append(
                profile.model_dump(mode="json")
            )

        else:

            needs_review.append(
                profile.model_dump(mode="json")
            )

    (
        OUTPUT_DIR / "profiles.json"
    ).write_text(
        json.dumps(
            good,
            indent=2,
            default=str,
        )
    )

    (
        OUTPUT_DIR / "needs_review.json"
    ).write_text(
        json.dumps(
            needs_review,
            indent=2,
            default=str,
        )
    )

    print(
        f"\nDone. "
        f"{len(good)} high-confidence, "
        f"{len(needs_review)} need review."
    )

    print(
        f"See "
        f"{OUTPUT_DIR}/profiles.json "
        f"and "
        f"{OUTPUT_DIR}/needs_review.json"
    )


def main() -> None:

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--strains",
        nargs="*",
        default=[],
        help=(
            "Leafly strain slugs, "
            "e.g. blue-dream"
        ),
    )

    args = parser.parse_args()

    slugs = list(args.strains)

    if not slugs:

        parser.error(
            "Provide --strains"
        )

    run(slugs)


if __name__ == "__main__":
    main()