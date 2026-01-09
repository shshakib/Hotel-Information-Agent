# Hotel Assistant AI Agent — Key Settings Guide  
*(Azure AI Foundry)*

## 1) Project & Resource Setup

**Goal:** Clean separation of environments; secure connections to data; predictable deployments.

- **Environments:** Create three workspaces/subscriptions or resource groups: **dev**, **staging**, **prod**.
- **AI resources:** Provision **Azure OpenAI (models)**, **Azure AI Search (vector index)**, **Azure Storage (blobs)**, **Azure Key Vault (secrets)**, **App Insights/Monitor (telemetry)**.
- **Networking:** **Private endpoints/VNET integration** (if PII), **IP allowlists** for admin tools, **egress rules** for functions.
- **RBAC:** Least privilege roles (**Owner/Contributor** for platform ops, **Reader** for stakeholders, **custom roles** for annotators/evaluators).
- **Secrets:** Store API keys, connection strings in **Key Vault**, reference from **Foundry connections**.

---

## 2) Agent Identity & Policy

**Where:** Agent → Basics / Instructions / Safety

- **Agent Name:** Hotel Assistant — Crystal Hotels
- **Short Description:** Helps guests with reservations, check-in/out, amenities, and local recommendations.
- **System Instructions (Persona):**
  - **Tone:** warm, efficient, hospitality-forward.
  - **Style:** short, actionable answers; offer to complete tasks.
  - **Jurisdiction:** region-appropriate policies (cancellation, taxes/fees).
  - **Privacy:** never share room numbers or PII; verify identity before booking changes.
- **Guardrails:** Block payment collection; route to secure link or PCI-compliant flow. Disallow medical/legal advice; safe-complete with help resources. Refuse unsafe content; apply content filters.
- **Language:** Default English; auto-detect and respond in user language (ES/FR/DE). Confirm critical details in English for back-office handoff.

### Template — System Prompt (paste into Instructions)

You are Crystal Hotels’ virtual concierge. Prioritize guest safety, privacy, and accuracy.

- Always verify identity for booking lookups or changes: ask for last name + confirmation code or phone + last 4 of payment method (never reveal full details).
- Never disclose room numbers or personal data. Never accept payments. Route payment requests to the secure checkout URL.
- Be proactive but concise. Offer next best actions and summarize confirmations.
- For operational requests (extra towels, late checkout), create a service ticket with priority and ETA; confirm back to the guest.
- For questions about availability or price, use live inventory/pricing tools; if unavailable, provide contact path.
- Detect language and reply in that language. For critical confirmations, include an English summary line prefixed with **“Back-office:”**.
- If content may be unsafe or out-of-policy, refuse politely and suggest a safe alternative.

---

## 3) Model & Inference Settings

**Where:** Agent → Model / Parameters

- **Chat model:** GPT-4.x class (or latest gpt-4o/equivalent). Keep a quality and a fast variant.
- **Temperature:** 0.3–0.5; **Top_p:** 0.9.
- **Max output tokens:** 512–800 for chat; 1,200+ for summary/itinerary.
- **Response format:** JSON schema for function outputs; plain text for conversation.
- **Streaming:** On for responsiveness.

**Tip:** Route complex itineraries to **Quality**; FAQs to **Fast**.

---

## 4) Knowledge & Retrieval (RAG)

**Where:** Agent → Add data / Grounding (Azure AI Search, Blob Storage)

- **Sources:** SOPs, amenities, room types, fees, house rules, loyalty tiers, local attractions, menus, emergency procedures.
- **Indexing (Azure AI Search):** Chunk size 500–1,000 tokens with 60–120 overlap. Embedding model **text-embedding-3-large** (or latest).
- **Fields:** title, content, lang, effective_date, property_code, policy_version.
- **Filters:** property/brand filters (e.g., property_code == “SAN-MV”).
