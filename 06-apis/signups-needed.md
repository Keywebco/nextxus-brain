# Accounts and actions requiring a human, checked 2026-10-05

**No account was created in this audit.** Vault names for DeepSeek, MiMo and Gemini were supplied in the brief, but account status, usable free quotas and presence of those names in GitHub Actions were not verified. Roger creates or authorizes new accounts himself. These are *candidate* signups, not claims that he lacks an account.

| Service | Signup or console | Unlocks | Required vault name (proposed if not in brief) |
|---|---|---|---|
| Groq | https://console.groq.com/ | Fast chat, code backup, free-plan Whisper transcription | `GROQ_API_KEY` (proposed) |
| SambaNova Cloud | https://cloud.sambanova.ai/ | Free-tier DeepSeek reasoning and fast fallback; confirm no payment method and current per-model quota | `SAMBANOVA_API_KEY` (proposed) |
| Mistral Experiment | https://console.mistral.ai/ | Evaluation-only free fallback, phone verification; confirm commercial-use eligibility before production | `MISTRAL_API_KEY` (proposed) |
| OpenRouter | https://openrouter.ai/ | Explicit `:free` model fallback, 50/day without qualifying purchased credits | `OPENROUTER_API_KEY` (proposed) |
| Cloudflare Workers AI | https://dash.cloudflare.com/sign-up | Image, embeddings, speech, within 10000 Neurons/day; also requires account ID | `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` (proposed) |
| Hugging Face | https://huggingface.co/join | $0.10/month inference credit for MiMo/DeepSeek experiments and model gateway fallback | `HF_TOKEN` (proposed) |
| Google AI Studio | https://aistudio.google.com/ | Gemini vision, code, embeddings; `GEMINI_API_KEY` name exists in supplied brief, confirm entitlement | `GEMINI_API_KEY` (existing name only) |
| Pollinations | https://enter.pollinations.ai/ | Earned Pollen image/video only if grant exists, not guaranteed free production; no public client secret | `POLLINATIONS_API_KEY` (proposed) |

Never send keys through chat or add them to this public repository. If Roger elects a provider, its secret VALUE belongs in the encrypted vault and, for GitHub Actions use, the corresponding GitHub Actions secret. Account signup and paid plan activation are human-only decisions.
