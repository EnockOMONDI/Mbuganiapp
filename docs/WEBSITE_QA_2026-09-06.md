# Website QA — 6 September 2026

Base: mugani2026b at 38ebb0a. Changes prepared in an isolated worktree because the original checkout has unrelated edits and deleted assets.

## Live email tests before changes

Two owner-authorized, clearly labelled test enquiries were submitted through the browser. MICE and Student Travel both returned Internal Server Error after roughly 30 seconds. The owner confirmed no email receipt. Test identifiers: MBUGANI-QA-20260906-MICE and MBUGANI-QA-20260906-STUDENT. Dummy phone numbers were used; no real booking or event was requested.

The quote form was inspected but not submitted because its submit action explicitly accepts Terms of Service. Package checkout was not submitted.

The three service enquiry handlers used Gmail SMTP without a connection timeout. This is a plausible cause of the observed worker failure, but production logs were not available to prove the exact exception. The original handlers save the record before attempting email; the failed production submissions may therefore already exist in the database.

## Email changes

MICE, Student Travel and NGO enquiries use the existing Mailtrap HTTPS integration. Requests have a 3-second connect and 8-second read timeout. Admin notifications and customer acknowledgements are attempted. Templates escape visitor input. A saved enquiry redirects even on notification failure and tells the visitor not to resubmit. No database migration is introduced. Delivery failure does not delete the saved request. This does not implement an automatic email retry queue.

Seven automated tests cover all three forms, real persistence in a test database during notification failure, invalid forms, correct recipients, escaping, provider errors, timeouts and explicit provider success. External email calls are mocked in tests. Local checks cannot prove production delivery; live verification is recorded separately.

## Image audit and changes

| Template / section | Finding | Action |
|---|---|---|
| Services — Air Ticketing | Zebra safari photo | Airport traveller and aircraft |
| Services — Hotel Bookings | Lodge interior was relevant but reused elsewhere | Dedicated generic lodge bedroom |
| Services — Tours and Safaris | Relevant wildlife photo shared with unrelated services | Guided elephant-viewing scene |
| Services — MICE | Lodge bedroom | Conference delegates |
| Services — Group Travel | Zebra safari photo | Group and coordinator beside bus |
| Services — Team Building | Lodge bedroom | Outdoor collaborative activity |
| Services — Insurance | Zebra safari photo | Traveller and advisor reviewing documents |
| Services — Transfers | Lodge bedroom | Chauffeur greeting traveller |
| MICE — ten service panels | Same generic placeholder across unrelated subjects | Corresponding service assets, descriptive alt text |
| MICE — hero | Plain desktop background / relative mobile image URL | Conference image with readable overlay |
| Corporate — banner / assistance | Generic background and blog image | Airport scene / advisor scene |
| Homepage — split safari story | Repeated zebra photo with mismatched guest description | Guide and guests watching elephants |
| Homepage — About / About Us | Existing safari images match general safari positioning | Retained |
| Homepage slides | Database/Uploadcare image with static fallback | Database images preserved |
| Student / NGO | Gradient and text layout; no service-photo mismatch in templates | No decorative images added |
| Destination / package / accommodation pages | Record-specific image tags / uploaded assets | Preserved; named properties require verified photographs |
| Blog | Post-specific image fields and shared fallbacks | Preserved; article image review remains content-specific |

Eight generated illustrative images use natural editorial photography, warm earth/cream colours, realistic adult subjects, no logos, no readable text and no invented named properties. They are generic service illustrations, not documentary evidence of Mbugani staff, partners or properties. Original PNGs are retained in the marketing workspace. Deployed assets are WebP with 768px and 1536px versions, lazy loading, dimensions and descriptive alt text.

## Buttons

The theme gave every `.main-btn i` a 50px circular background. Service links forced inline-block, and navbar styles globally changed button size. A content-scoped stylesheet now uses horizontal flex alignment, normal-sized icons, a 48px minimum height, consistent spacing, keyboard focus outlines and reduced-motion support. Service button inline overrides were removed. Paired CTAs wrap and become full-width on small screens. Navbar behaviour and button destinations are unchanged.

## Follow-up content findings

The quote breadcrumb includes a Novustell URL, MICE panel links include a relative `about.html`, and the Student Travel introduction contains stray text. These are existing content/link issues recorded for a separate cleanup. Specific uploaded destination/package images still require record-by-record visual approval; no generated image was substituted for a named bookable property.
