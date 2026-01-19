import json
import glob
import ollama
from ollama import chat
from difflib import SequenceMatcher
import base64
import re
import os

# ------------------------
# Model & image settings

model_name = "qwen3-vl:4b"

# ------------------------
# Load images

IMAGE_EXTS = ("*.png", "*.jpg", "*.jpeg")  # make sure this is correct
IMAGE_DIR = "/home/ikutswa/data/BRIDGE/patient_documents/converted_images/"

def load_images():
    images = []
    for ext in IMAGE_EXTS:
        images.extend(glob.glob(f"{IMAGE_DIR}/{ext}"))
    return sorted(images)

def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# ------------------------
# Load truth.json file

with open("/home/ikutswa/PycharmProjects/BRIDGEProject/truth.json") as f:
    GT = json.load(f)


# ------------------------
# Cleaning & Accuracy utils

def clean_json_output(text):
    """
    Removes Markdown triple-backtick fences such as:
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
    Handles dicts, lists, and strings gracefully.
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
# Load Prompts

def load_prompts():
    """
    Load all .txt prompts from prompt_templates folder relative to script location.
    """
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    prompt_dir = os.path.join(BASE_DIR, "prompt_templates")

    if not os.path.exists(prompt_dir):
        print(f"❌ Prompt folder not found: {prompt_dir}")
        return {}

    prompts = {}
    for file in glob.glob(os.path.join(prompt_dir, "*.txt")):
        name = os.path.basename(file).replace(".txt", "")
        with open(file, "r") as f:
            prompts[name] = f.read()

    if not prompts:
        print(f"❌ No .txt files found in {prompt_dir}")

    return prompts


# ------------------------
# Merge predictions from multiple prompts

def merge_predictions(pred_list):
    """
    Merge a list of predictions (dicts or JSON-like outputs) into a single dict.

    Rules:
    1. If the prediction is a dict, merge key-values directly.
    2. If the prediction is a list of 'Key: Value' strings, convert to dict first.
    3. If a key already exists, the first non-empty value is kept.
    4. Standardizes missing/blank/unreadable values to 'N/A'.
    """
    merged = {}

    for pred in pred_list:
        # Convert list-of-strings to dict if needed
        if isinstance(pred, list):
            pred = list_to_dict(pred)
        elif not isinstance(pred, dict):
            # skip if it's a plain string or unexpected type,
            continue

        for key, value in pred.items():
            if key in merged:
                # Standardize by replacing current value if empty or 'N/A'
                if merged[key] in ["", "N/A", None] and value not in ["", "N/A", None]:
                    merged[key] = value
            else:
                # Standardize missing/blank
                if value in ["", "-", "n/a", "N", "NA", None]:
                    value = "N/A"
                merged[key] = value

    return merged

# ------------------------
# Run all prompts (MAIN)

def run_all():
    prompts = load_prompts()
    images = load_images()

    if not images:
        print("No images found in:", IMAGE_DIR)
        return

    if not prompts:
        print("No prompts found in prompt_templates/")
        return

    final_results = []   # list of image-level results

    for image_path in images:
        print(f"\n\n===== Processing image: {image_path.split('/')[-1]} =====")

        image_predictions = []
        image_accuracies = []

        for prompt_name, prompt_text in prompts.items():
            print(f">>> Running prompt: {prompt_name}")

            try:
                response = ollama.chat(
                    model=model_name,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt_text,
                            "images": [image_to_base64(image_path)]
                        }
                    ],
                    options={"seed": 42}
                )
            except Exception as e:
                print(f" Failed to get response for {prompt_name}: {e}")
                continue

            output_text = response["message"]["content"]

            # Print raw output from model
            print("Raw model output:\n", output_text)

            # Print the standardized JSON output
            cleaned = clean_json_output(output_text)

            try:
                prediction = json.loads(cleaned)
            except Exception:
                # fallback: keep raw string or list
                prediction = cleaned

            # Print cleaned prediction
            print("Cleaned prediction:\n",
                      json.dumps(prediction, indent=2) if isinstance(prediction, dict) else prediction)

            # Map prompt name to GT key
            if "_baseline" in prompt_name or "trial" in prompt_name or "whole" in prompt_name:
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

            truth = GT.get(gt_key) if gt_key else None

            # Compute accuracy if ground truth exists
            accuracy = compute_accuracy(prediction, truth) if truth else None

            if accuracy is not None:
                print(f"Accuracy vs GT ({gt_key}): {accuracy}")
                image_accuracies.append(accuracy)

            image_predictions.append(prediction)

        # Merge all predictions into a single extraction
        merged_extraction = merge_predictions(image_predictions)

        # Print merged output for specific image
        print("\n>>> Merged extraction for this image:")
        print(json.dumps(merged_extraction, indent=2))

        # Compute overall image accuracy
        overall_accuracy = round(sum(image_accuracies) / len(image_accuracies), 3) if image_accuracies else 0.0

        result = {
            "image": image_path.split("/")[-1],
            "extraction": merged_extraction,
            "accuracy": overall_accuracy
        }

        final_results.append(result)

        # Final result
        print("\n=== Final result for this image ===")
        print(json.dumps(result, indent=2))

    # Save final results
    with open("extraction_results.json", "w") as f:
        json.dump(final_results, f, indent=2)

    print("\n Saved extraction_results.json with", len(final_results), "images.")


if __name__ == "__main__":
    run_all()
