"""Run Jacobian lens fitting on a small corpus, then score with the battery."""
import sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, r"C:\Users\natha\Documents\Default Project\restore\jacobian-lens")

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from jlens.protocol import LensModel
from jlens.fitting import fit

MODEL_ID = "Qwen/Qwen2.5-0.5B"

# A small diverse corpus (prompts). Kept small for a 1-hour budget.
CORPUS = [
    "The quick brown fox jumps over the lazy dog while the sun sets over the horizon and the wind blows through the trees.",
    "In a distant galaxy far beyond our own, stars are born from vast clouds of gas and dust that collapse under their own gravity.",
    "She opened the book carefully and began to read the first chapter, which described the history of an ancient civilization.",
    "The scientist carefully recorded the results of the experiment, noting every detail and anomaly that appeared during the trials.",
    "Music filled the concert hall as the orchestra played the symphony with great passion and precision throughout the evening.",
    "The child laughed and ran across the playground, chasing butterflies and enjoying the warm afternoon sunshine with friends.",
    "Water flows downhill through rivers and streams, seeking the lowest point in the landscape over many years of erosion.",
    "The computer processed the large dataset and returned the results within seconds, surprising everyone with its speed.",
    "He thought about the difficult problem for a long time before answering, considering every possible angle and solution.",
    "The sun set behind the mountains, painting the sky in shades of orange, pink, and purple as the day ended.",
    "A good scientific theory explains many observations with few assumptions and makes testable predictions about new phenomena.",
    "The river winds through the valley between the hills, carrying sediment and nutrients to the fertile plains below.",
    "She remembered the day they first met at the cafe, when the rain started and they shared an umbrella together.",
    "The machine learned to recognize patterns in the images after being trained on thousands of labeled examples over weeks.",
    "Rain fell softly on the roof throughout the night, creating a soothing rhythm that helped everyone sleep peacefully.",
    "The team worked together to solve the difficult puzzle, combining their different skills and perspectives to find the answer.",
    "Light travels faster than sound in any medium, which is why we see lightning before we hear thunder during storms.",
    "He felt a deep sense of wonder looking up at the stars, contemplating the vastness of the universe and our place in it.",
    "The book contained stories from many different cultures, each offering unique insights into human nature and experience.",
    "The engine roared as the car accelerated down the highway, leaving the city behind and heading toward the open countryside.",
]

def main():
    print("loading model...")
    tok = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(MODEL_ID, torch_dtype=torch.float16).to("cuda")
    model.eval()
    from jlens.hf import from_hf
    lm = from_hf(model, tok)
    print("model ready, layers:", lm.n_layers, "d_model:", lm.d_model)

    ckpt = ROOT / "experiments" / "EXP-C002" / "lens_ckpt.pt"
    t0 = time.time()
    lens = fit(lm, CORPUS, checkpoint_path=str(ckpt), checkpoint_every=1, max_seq_len=64, skip_first=4)
    print(f"fit done in {time.time()-t0:.1f}s")
    lens.save(str(ROOT / "experiments" / "EXP-C002" / "lens.pt"))
    print("saved lens")

if __name__ == "__main__":
    main()
