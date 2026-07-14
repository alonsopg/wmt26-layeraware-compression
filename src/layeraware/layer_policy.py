import re

MLP_PATTERN = re.compile(r"(?:^|\.)(?:mlp|gate_proj|up_proj|down_proj)(?:\.|$)")
ATTENTION_PATTERN = re.compile(r"(?:^|\.)(?:self_attn|q_proj|k_proj|v_proj|o_proj)(?:\.|$)")

def classify(name: str) -> str:
    if MLP_PATTERN.search(name): return "mlp_q4_candidate"
    if ATTENTION_PATTERN.search(name): return "attention_preserve_candidate"
    if any(x in name for x in ("embed", "lm_head", "norm")): return "output_critical_preserve"
    return "other"
