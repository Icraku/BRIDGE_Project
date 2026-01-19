import json
import glob
import ollama
from ollama import chat
from difflib import SequenceMatcher
import base64
import re

# ------------------------
# Model & image settings

model_name = "qwen3-vl:4b"

image_path = (
    "/home/ikutswa/data/BRIDGE/patient_documents/converted_images/"
    "17000006_NAR_2015_EEQsDZu_page_1.png"
)

def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


# ------------------------
# Load truth.json file

with open("truth.json") as f:
    GT = json.load(f)


# ------------------------
# Cleaning & Accuracy utils

def clean_json_output(text):
    """
    Removes Markdown triple-backtick such as:
    ```json
    [...]
    ```
    Returns a clean JSON string.
    """
    # Remove ```json or ```xyz
    cleaned = re.sub(r"```(\w+)?", "", text)
    # Remove closing ```
    cleaned = cleaned.replace("```", "")
    return cleaned.strip()


def fuzzy_equal(a, b, threshold=0.8):
    """Return True if a and b match with ≥ threshold similarity."""
    return SequenceMatcher(None, a, b).ratio() >= threshold


def compute_accuracy(pred, truth):
    """
    Handles dicts, lists and strings.
    Uses fuzzy matching for lists and exact matching for top-level strings.
    """

    # Normalize int/string mismatch to make both strings
    if isinstance(pred, int) and isinstance(truth, str):
        pred = str(pred)
    elif isinstance(pred, str) and isinstance(truth, int):
        truth = str(truth)

    # STRING
    if isinstance(truth, str):
        return 1.0 if pred == truth else 0.0

    # LIST
    if isinstance(truth, list):
        if not isinstance(pred, list):
            return 0.0

        correct = 0
        for t in truth:
            for p in pred:
                if fuzzy_equal(t, p):
                    correct += 1
                    break
        return correct / len(truth)

    # DICT
    if isinstance(truth, dict):
        if not isinstance(pred, dict):
            return 0.0

        correct = 0
        for key in truth:
            if (
                key in pred and
                (
                    pred[key] == truth[key] or
                    fuzzy_equal(str(pred[key]), str(truth[key]))
                )
            ):
                correct += 1

        return correct / len(truth)

    # fallback
    return 0.0

# ------------------------
# Convert list-of-strings output to dict

def list_to_dict(pred_list):
    """
    Converts a list of strings e.g. 'Key: Value' to a dictionary.
    Standardizes missing/blank/unreadable values to 'N/A'.
    """
    if not isinstance(pred_list, list):
        return pred_list

    d = {}
    for item in pred_list:
        if ":" in item:
            key, value = item.split(":", 1)
            key = key.strip()
            value = value.strip()

            # Standardize missing/blank values
            if value in ["", "-", "n/a", "N", "NA"]:
                value = "N/A"

            d[key] = value
    return d

# ------------------------
# Load prompts

def load_prompts():
    """
    Gets the prompt filename without the extension e.g., promptA_labels
    """
    prompts = {}
    for file in glob.glob("prompt_templates/*.txt"):
        name = file.split("/")[-1].replace(".txt", "")
        with open(file) as f:
            prompts[name] = f.read()
    return prompts


# ------------------------
# Run all prompts (MAIN)

def run_all():
    prompts = load_prompts()
    results = {}

    all_accuracies = []

    for prompt_name, prompt_text in prompts.items():
        print(f"\n\n>>> Running {prompt_name} ...")

        response = ollama.chat(
            model=model_name,
            messages=[
                {
                    "role": "user",
                    "content": prompt_text,
                    "images": [image_to_base64(image_path)]
                }
            ],
            options={
                "seed": 42
            }
        )

        output_text = response["message"]["content"]

        # -------- Clean model output --------
        cleaned = clean_json_output(output_text)

        try:
            prediction = json.loads(cleaned)
        except Exception:
            prediction = cleaned  # fallback to raw string

        # Map prompt to ground truth key
        if "_baseline" in prompt_name:
            gt_key = "baseline"
        elif "trial" in prompt_name:
            gt_key = "baseline"
        elif "A_labels" in prompt_name:
            gt_key = "labels"
        elif "B_section_entry" in prompt_name:
            gt_key = "name"
        elif "C_ip_no" in prompt_name:
            gt_key = "ip_no"
        elif "D_row1" in prompt_name:
            gt_key = "row1"
        elif "E_row2" in prompt_name:
            gt_key = "row2"
        elif "F_row3" in prompt_name:
            gt_key = "row3"
        else:
            gt_key = None

        truth = GT.get(gt_key)

        # -------- Compute accuracy --------
        accuracy = compute_accuracy(prediction, truth)
        all_accuracies.append(accuracy)

        results[prompt_name] = {
            "prediction": prediction,
            "truth": truth,
            "accuracy": round(accuracy, 3)
        }

        print(json.dumps(results[prompt_name], indent=2))

    # -------- Compute overall model accuracy --------
    if all_accuracies:
        overall_accuracy = sum(all_accuracies) / len(all_accuracies)
    else:
        overall_accuracy = 0.0

    results["_overall"] = {
        "num_prompts": len(all_accuracies),
        "overall_accuracy": round(overall_accuracy, 3)
    }

    print("\n=== OVERALL MODEL ACCURACY ===")
    print(json.dumps(results["_overall"], indent=2))

    # -------- Save full report --------
    with open("extraction_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print("\n\nSaved extraction_results.json")



if __name__ == "__main__":
    run_all()