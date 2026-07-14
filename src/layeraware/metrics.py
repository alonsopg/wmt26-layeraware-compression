def corpus_scores(hypotheses, references):
    import sacrebleu
    return {"chrf": sacrebleu.corpus_chrf(hypotheses, [references]).score,
            "bleu": sacrebleu.corpus_bleu(hypotheses, [references]).score}
