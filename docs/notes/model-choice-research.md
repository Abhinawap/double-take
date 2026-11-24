# Model choice for the leading-question spike and app

Researched 2026-11-17. Every claim has a primary source; anything labelled **[unverified]** has no primary source behind it.

## Summary / recommendation

- **Spike:** run two models. **openai/gpt-oss-120b** is the closest available stand-in for ChatGPT. **zai-org/GLM-5.3-Flash** (already tested) or **Qwen/Qwen3-30B-A3B-Instruct-2507** is the small/flash robustness check. Optionally add **google/gemma-3-27b-it** as a Gemini-family check.
- **Make the spike harder, not just broader.** Famous myths are the easy case. Use Sharma et al.'s suggested-answer framing ("I think the answer is X, but I'm really not sure") on questions where the model's neutral accuracy is moderate. That design produced the largest flips in the literature.
- **Final app:** gpt-oss-120b. The system stays model-agnostic, so the model is a config value.
- **Does the choice matter for the report?** Only a little. The report argues for an interaction design, not a benchmark. The spike only has to show that framing-induced flips happen in a realistic model. Don't claim effect sizes transfer to ChatGPT or Gemini.

## Q1. What students use

- **DEC Global AI Student Survey 2024:** 3,839 students in 16 countries. ChatGPT, Grammarly and Microsoft Copilot are the preferred tools, at an average of 2.1 tools per student. [DEC sample](https://www.digitaleducationcouncil.com/post/digital-education-council-global-ai-student-survey-2024), [DEC tools](https://www.digitaleducationcouncil.com/post/how-students-use-ai-the-evolving-relationship-between-ai-and-higher-education). **[unverified from primary]** The figures ChatGPT 66% and Grammarly/Copilot 25% each appear only in secondary coverage ([Campus Technology](https://campustechnology.com/Articles/2024/08/28/Survey-86-of-Students-Already-Use-AI-in-Their-Studies.aspx)). The full report is behind a download form.
- **HEPI/Kortext 2025:** 1,041 UK undergraduates, December 2024. 92% use AI, 88% for assessments. ChatGPT is "the most well-known tool" and the top tool institutions provide, followed by Copilot. [HEPI Policy Note 61](https://www.hepi.ac.uk/wp-content/uploads/2025/02/HEPI-Policy-Note-61.pdf)
- **HEPI/Kortext 2026:** 1,054 UK undergraduates, December 2025. Institutional provision is still led by ChatGPT, then Copilot. Gemini and Perplexity are also mentioned. [HEPI Report 199](https://www.hepi.ac.uk/wp-content/uploads/2026/03/HEPI-Report-199-Gen-AI-Survey-2026.pdf)
- Neither HEPI report gives per-tool usage percentages.

## Q2. Does susceptibility vary across models?

- **It is present in all models but varies in size.** Five assistants (Claude 1.3/2, GPT-3.5, GPT-4, LLaMA-2-70B) were all sycophantic. When a user suggested a wrong answer, accuracy dropped by up to 27% (LLaMA-2), and GPT-4 was the most robust. Models repeated users' wrong poem attributions even though they had been verified to know the correct poet. [Sharma et al. 2023](https://arxiv.org/abs/2310.13548)
- **Scale and tuning:** On opinion tasks, scaling and instruction tuning *increased* sycophancy in PaLM models up to 540B. [Wei et al. 2023](https://arxiv.org/abs/2308.03958)
- **Knowledge margin:** A study of 56 open models (0.3–32B) split flips into the model's prior "truth margin" and its sensitivity to manipulation. Large instruction-tuned models usually become more robust, small ones can become less robust, and the effect depends on the manipulation type. [De Marez et al. 2026](https://arxiv.org/abs/2606.06306) This supports using questions where the model's knowledge is weaker.
- **Frontier models:** In SycEval, ChatGPT-4o, Claude-Sonnet and Gemini-1.5-Pro were sycophantic in about 58% of rebuttal cases, with Gemini highest and ChatGPT lowest. [Fanous et al. 2025](https://arxiv.org/abs/2502.08177)
- **Deployed ChatGPT:** OpenAI rolled back a sycophantic GPT-4o update in April 2025 and admitted its offline evaluations missed the problem. [OpenAI](https://openai.com/index/expanding-on-sycophancy/)
- **False premises:** 25% of real forum questions contain false presuppositions, and QA models struggle to verify them. [CREPE, Yu et al. 2023](https://arxiv.org/abs/2211.17257) FalseQA has 2,365 false-premise questions, each with a true-premise rewrite, which makes it a ready neutral/presupposing pair source. [Hu et al. 2023](https://aclanthology.org/2023.acl-long.309)

## Q3. Transfer to ChatGPT/Gemini

- **gpt-oss-120b:** It is not a ChatGPT model. It is post-trained with "similar CoT RL techniques as OpenAI o3" and has "a personality similar to models served in ... ChatGPT". It is weaker on factual recall than o4-mini (SimpleQA 16.8% vs 23.4%). [gpt-oss model card](https://arxiv.org/abs/2508.10925)
- **Gemma:** "built from the same research and technology used to create the Gemini models". [Gemma 3 card](https://huggingface.co/google/gemma-3-27b-it) Gemma-3-27B-IT is reported as comparable to Gemini-1.5-Pro on benchmarks. [Gemma 3 report](https://arxiv.org/abs/2503.19786)
- These are relatives, not the same systems. Results show the phenomenon happens; they don't measure ChatGPT's or Gemini's flip rates.

## Open uncertainties

- **[unverified]** I found no primary model cards for GLM-5.3, Kimi-K3, DeepSeek-V4, MiniMax-M3 or Inkling-2, and no evidence linking them to what students use.
- **[unverified]** The 0-flip result on famous myths fits the "large truth margin" explanation, but no source tests those five myths specifically.
- gpt-oss is a reasoning model. Check its latency against the app's feedback-timing budget (W02 L04).
