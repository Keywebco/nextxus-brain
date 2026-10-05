# Excluded from automatic zero-cash routing, checked 2026-10-05

An HTTP response from a keyless endpoint proves only reachability, not a free usable account. Entries below are excluded from the active router; some remain in the provider catalog for future review.

| Service | Reason | Provider source |
|---|---|---|
| Direct DeepSeek API | Metered per token, no guaranteed recurring free API allocation. Roger's existing vault key does not prove free balance. Free DeepSeek model on SambaNova is a different route. | [Pricing](https://api-docs.deepseek.com/quick_start/pricing) |
| Direct Xiaomi MiMo API | Pay-as-you-go charges tokens; complimentary balance is conditional, not a permanent free tier. Keep separate named-mind vault lanes. | [Pay-as-you-go](https://mimo.mi.com/docs/en-US/price/pay-as-you-go) |
| Cerebras | $5 credit requires verified payment method and expires in 30 days, explicitly no renewable free tier. Do not rely on it for 100 percent free operation. | [Rate limits and trial FAQ](https://inference-docs.cerebras.ai/support/rate-limits) |
| GitHub Models | Fully retired July 30, 2026, including inference API. Older free-tier articles are obsolete. | [Retirement notice](https://docs.github.com/en/github-models) |
| Together AI | No general free trial; minimum $5 credit purchase required. | [Credits](https://docs.together.ai/docs/billing-credits) |
| Cohere trial | Free trial keys prohibited for production/commercial use; not appropriate for a public Federation service. | [Pricing](https://cohere.com/pricing) |
| Perplexity API | No verified permanent no-cost search API tier; keyless guessed `/models` returned HTTP 404, not proof host is dead. | [Pricing](https://docs.perplexity.ai/docs/getting-started/pricing) |
| DeepAI API | Free web UI is not free API entitlement; API access depends on Pro/prepaid. An existing key name does not waive fees. | [API docs](https://deepai.org/docs) |
| Stability AI | 25 credits at signup are one-time, not a recurring free service. | [API docs](https://platform.stability.ai/docs) |
| NVIDIA Build NIM | Free evaluation credits are finite; no documented renewable zero-cost production allocation. Public model list HTTP 200 is not inference eligibility. | [Developer NIM trial announcement](https://developer.nvidia.com/blog/access-to-nvidia-nim-now-available-free-to-developer-program-members/) |
| Pollinations image/video | Not automatically enabled. Public model list HTTP 200 does not mean generation is free; current API requires a key and earned Pollen / prototype grants are conditional. Listed only as gated last-resort route. | [API docs](https://pollinations.ai/docs) |
| FAL | Existing FAL_KEY balance is exhausted per task brief; no free quota independently verified. | User-provided brief, 2026-10-05 |
| Emergent LLM gateway | EMERGENT_LLM_KEY is a paid-platform lane, not a 100 percent free fallback. | User-provided brief, 2026-10-05 |
| Video generation APIs | No durable, keyless, production-safe free video generation provider verified; do not promise video on free router. Pollinations requires Pollen and access grant. | [Pollinations docs](https://gen.pollinations.ai/docs) |

**Audio and local zero-cash options:** Groq documents Whisper STT free-plan limits [here](https://console.groq.com/docs/rate-limits). Cloudflare documents [Whisper](https://developers.cloudflare.com/workers-ai/models/whisper/) under its daily free Neuron allocation. Offline Piper TTS and whisper.cpp STT use local compute, not free hosted APIs; audit their licenses, deployment capacity and voice terms before production. No unrestricted hosted TTS tier has been validated. Free local vector alternatives require installed model and runtime; Cloudflare BGE embeddings and Gemini Embedding are the documented managed choices.
