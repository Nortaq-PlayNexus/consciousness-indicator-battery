"""EXP-C002: score Qwen2.5-0.5B via the consciousness-indicator-battery.

Scaffold only: loads the model, prints architecture, and stubs the measurement
step. Full J-space measurement requires jlens fitting on a corpus.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

MODEL_ID = "Qwen/Qwen2.5-0.5B"

def main():
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    print(f"loading {MODEL_ID} ...")
    tok = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(MODEL_ID, torch_dtype=torch.float16)
    model.eval()
    print("model loaded")
    print("num layers:", model.config.num_hidden_layers)
    print("hidden size:", model.config.hidden_size)
    print("vocab size:", model.config.vocab_size)

    # jlens smoke: fit on a tiny corpus
    try:
        from jlens.fitting import fit
        print("jlens fit import ok")
    except Exception as e:
        print("jlens API check:", repr(e))

    # Battery import
    import battery
    state = battery.calibration_state()
    print("calibration:", state)

if __name__ == "__main__":
    main()
