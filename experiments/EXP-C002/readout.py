"""Preliminary J-space readout: apply the fitted lens to a sample prompt."""
import sys, json, torch
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, r"C:\Users\natha\Documents\Default Project\restore\jacobian-lens")

from transformers import AutoModelForCausalLM, AutoTokenizer
from jlens.hf import from_hf
from jlens.lens import JacobianLens

MODEL_ID = "Qwen/Qwen2.5-0.5B"
LENS_PATH = ROOT / "experiments" / "EXP-C002" / "lens.pt"

def main():
    tok = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(MODEL_ID, torch_dtype=torch.float16).to("cuda")
    model.eval()
    lm = from_hf(model, tok)
    lens = JacobianLens.load(str(LENS_PATH))

    prompt = "The quick brown fox jumps over the lazy dog."
    lens_logits, model_logits, input_ids = lens.apply(lm, prompt, max_seq_len=64)

    out = {"prompt": prompt, "layers": {}}
    for layer, ll in lens_logits.items():
        # top-5 tokens at the last position
        top = torch.topk(ll[-1], k=5)
        toks = [tok.decode([i]) for i in top.indices.tolist()]
        out["layers"][str(layer)] = {"top5": toks, "top5_scores": top.values.tolist()}

    outdir = ROOT / "RESULTS" / "EXP-C002"
    outdir.mkdir(parents=True, exist_ok=True)
    with open(outdir / "readout.json", "w") as f:
        json.dump(out, f, indent=2)
    print("saved readout to", outdir / "readout.json")
    # print a short summary
    for layer in sorted(lens_logits)[:3]:
        print(f"layer {layer}: {out['layers'][str(layer)]['top5']}")

if __name__ == "__main__":
    main()
