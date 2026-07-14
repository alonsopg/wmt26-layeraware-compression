POLICIES = {
    "global_bnb_q4": {"backend": "bitsandbytes", "bits": 4, "deployment_relevant": True},
    "global_bnb_q8": {"backend": "bitsandbytes", "bits": 8, "deployment_relevant": True},
    "layeraware_mlp_q4_attention_preserved": {"backend": "experimental", "deployment_relevant": False},
}
