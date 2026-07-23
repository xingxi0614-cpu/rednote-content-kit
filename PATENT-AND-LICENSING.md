# Patent and Licensing Decision

This document is operational guidance, not legal advice.

## Recorded software-license decision

The selected public software license is **MIT**. The complete standard text is installed in `LICENSE`, and the Plugin manifest records the SPDX identifier `MIT`.

This decision favors broad adoption and service-led commercialization. It does not authorize public disclosure: the patent-first rule and every remaining item in `RELEASE-HOLD.md` still apply.

## Patent-first rule

Public disclosure can become prior art and may destroy patent novelty in jurisdictions without a broad grace period. Do not publish code, detailed workflows, demos, papers, screenshots, or public downloads until a qualified patent professional has reviewed whether there is a patentable technical invention and whether filing should happen first.

WIPO recommends filing before public disclosure because grace periods vary by jurisdiction. China's Patent Law defines prior art broadly and provides only specified exceptions; it also excludes rules and methods for intellectual activities from patent protection. A content workflow or prompt may therefore rely more on copyright, trade secret, trademark, or service execution than on patents, while a genuinely technical implementation may require a different analysis.

Owning a patent and licensing software are separate questions. An open-source license normally does not transfer patent ownership, but some licenses expressly grant users a patent license, and other licenses may carry legal uncertainty about implied rights. The exact effect must be reviewed for the jurisdictions and claims involved.

## Considered public-license paths

### MIT — maximum adoption

- Simple and permissive.
- Allows anyone, including competitors, to use, modify, redistribute, and sell the software.
- Good for reach, consulting, training, templates, sponsorship, and reputation-led monetization.
- Weak leverage for selling proprietary exceptions because recipients already receive broad rights.
- Contains no express patent license text, but that does not guarantee that every patent issue is reserved in every jurisdiction.

### AGPL-3.0-only plus a commercial license — stronger dual-license leverage

- Keeps distributed and network-served modified versions under strong source-sharing obligations.
- The copyright holder may also sell a separate commercial license for proprietary use.
- Requires control of contribution copyright or contributor agreements that permit relicensing.
- Contains patent provisions and should not be chosen before professional patent review.

### Source-available/non-commercial — maximum commercial control

- Can reserve commercial use for paid customers.
- Must not be described as “open source” unless the license is OSI-approved.
- May reduce adoption and community contributions.

## Recorded implementation decision

1. Keep this candidate private.
2. Obtain a patentability and prior-art assessment before public disclosure.
3. MIT has been selected because adoption and service-led revenue are the current priorities.
4. Do not promise exclusive use or code royalties: every recipient receives MIT's commercial-use rights.
5. If the business later depends on proprietary licensing, apply that model only to separately owned future components after legal review; already released MIT versions remain available under their granted terms.
6. Run and document the release gate before any public disclosure.

## Primary references

- WIPO, “How to Protect Inventions through Patents”: https://www.wipo.int/en/web/patents/protection
- China National Intellectual Property Administration, Patent Law Articles 22-25: https://english.cnipa.gov.cn/art/2022/10/13/art_3068_179273.html
- Open Source Initiative FAQ: https://opensource.org/faq
