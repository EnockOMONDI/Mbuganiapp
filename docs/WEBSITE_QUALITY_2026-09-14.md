# Website quality changes — 14 September 2026

Branch: `website-quality-2026-09`, based on `271b40f`.
Worktree: `/Users/djsean/Documents/ChatGPT/MBUGANI/website-quality`.
Changes are local. The owner deploys manually in Render after pushing.

## Implemented

- Public travel routes now use `/packages/`, `/destinations/`, `/accommodations/`, and related paths. Old `/adminside/` public links redirect permanently, preserving query strings. Django's internal app and database names remain compatible.
- New public navigation and cream/brown/gold page shell; simplified package detail, calendar-based quote, contact and quote success pages.
- Destinations directory redesigned with country cards, country/search filters, expandable city/place lists, and mobile layout. Existing destination images are retained; unavailable images use a neutral SVG fallback.
- Package card markup/styles preserved apart from functional, accessible booking/detail links. Pagination preserves filters and has deterministic ordering. Search uses ordinary GET navigation so card results and pagination cannot fall out of sync.
- Detail URL helpers corrected; legacy missing/invalid slugs fall back to ID-based detail pages instead of crashing entire lists. Missing image fields are handled and image attributes escaped.
- Booking confirmation requires owner login or email verification code. Codes expire after 10 minutes, are HMAC hashed, limited by persistent per-reference send/attempt buckets, and consumed on use. Verified guest access expires after 30 minutes; responses are not cached.
- Guest checkout does not attach bookings to an existing account solely by submitted email. New accounts have unusable passwords until a one-hour, single-use password invitation is completed. Duplicate confirmation send removed. Cart removal uses POST, and traveller input is validated.
- Email deliveries have persisted status, bounded request timeouts and up to three attempts. Successful bodies are cleared; expiring verification emails are not retried after expiry. Staff can retry eligible messages in admin or run `python manage.py retry_email_deliveries --settings=tours_travels.settings_prod`. A scheduled runner is NOT configured; retries require an operator or a separately configured scheduled command. A provider timeout can be ambiguous, so eventual duplicate delivery is still possible.
- Contact form saves an enquiry and uses the common mail path. House of Leather added without fabricating a floor or map pin. Correct phone/email/WhatsApp links added.
- Replaced blocking preloaders with a short, nonblocking gold progress line, CSS fail-safe and reduced-motion handling. Submit feedback blocks immediate repeat clicks and restores on stalled navigation.
- Sitemap, robots, public canonical metadata and TravelAgency structured data added. Language, focus, skip link, public form labels/errors, blog count, incorrect copied success-page text and several dead links fixed. Detailed health and metrics require staff access; the deliberate error test is development-only.

## Verification

- Django system check: no issues.
- Migration consistency check: no ungenerated changes.
- 22 targeted tests passed (`users.test_website_quality`, `users.test_service_inquiries`). Covers access/expiry, invitations, guest ownership, delivery failure/retry, pagination, invalid slugs, image escaping, date validation and nested destination search.
- 40 local public list/detail route checks returned 200.
- Computer-use review of desktop/mobile layouts, destination expansion and destination search.
- Two browser form submissions succeeded: package quote with dates and contact enquiry. Both marked `TEST ONLY — MBUGANI-QA-20260914`, using `kipekeestudio@gmail.com`. Two saved records and four console delivery records confirmed locally. Development console email does NOT prove inbox delivery.

## Manual deployment and remaining verification

1. Review and push this branch; merge it into the configured Render branch (`mugani2026b`) or explicitly change Render's branch. Merely pushing this feature branch will not change the configured deployment source.
2. Run the manual Render deployment. Existing build configuration runs collectstatic and migrate; migrations 0009 and 0010 are required before serving these changes.
3. After deployment verify `/packages/?page=2`, legacy redirects, `/blog/`, sitemap, guest access and email delivery with marked enquiries. Both old live blog and package page two returned 500 before deployment. Their exact production traceback was unavailable; local data fixes are verified, but a live resolution is NOT yet established.
4. Check both customer and business inboxes and provider logs. No production delivery test was run for this branch.
5. Optional operational follow-up: schedule the retry command, define retention/cleanup for challenge and delivery records, and run the original external scanner with its full findings available.

Broader unfinished audit items: business-approved privacy/booking/cancellation policy content (existing checkout Terms link remains a placeholder), full-site carousel/menu keyboard audit and plugin/CWV profiling, complete structured data per content type, and production data/image reconciliation. No scanner score improvement is claimed. The database and development log changed during local QA and must not be included in the source commit.

## Shared navigation follow-up

The homepage and both public template families now share Packages, Destinations, Services dropdown, Our story, Contact and Plan my trip. The logo is enlarged by framing its original transparent margins; the original image file is unchanged. Homepage navigation is transparent at the top and cream after scrolling; mobile uses an expandable menu. Desktop scroll/dropdown and mobile expansion were checked in the browser. Ten representative routes render the shared menu and all service fragment targets exist.

Image storage verification: live package images use Uploadcare CDN URLs. The committed local SQLite database already had empty image fields for all ten packages before this branch. No image files were deleted. Keep the existing production database on deployment; do not publish the development SQLite file.
