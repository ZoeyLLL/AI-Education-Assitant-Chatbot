from transformers import AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import login
import os
import torch


PREFERED_MODEL = "pretrained"


if torch.cuda.is_available():
    print("Using GPU")
    device = torch.device("cuda")
    print("GPU:", torch.cuda.get_device_name(0))
else:
    print("Using CPU")
    device = torch.device("cpu")

# Login to huggingface
token = os.getenv('HF_TOKEN')
login(token = token)


if PREFERED_MODEL == "pretrained":
    #print("Using pretrained model")
    model_id = "meta-llama/Meta-Llama-3-8B"
    print("Loading model...")
    model = AutoModelForCausalLM.from_pretrained(model_id, device_map = "cuda", load_in_8bit = True)
    print("loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    print("Pretrained model loaded.")
elif PREFERED_MODEL == "fine-tuned":
    print("Using fine-tuned model")
    model_id = os.getenv('MODEL_ID')
    if model_id is None:
        raise ValueError("MODEL_ID is not set")
    print("Loading model...")
    model = AutoModelForCausalLM.from_pretrained(model_id, device_map = "cuda", load_in_8bit = True)
    print("loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    print("Fine-tuned model loaded.")

def answer(prompt):
    inputs = tokenizer.encode(prompt, add_special_tokens=False, return_tensors="pt").to(device)
    prompt_length = len(tokenizer.decode(inputs[0], skip_special_tokens=True, clean_up_tokenization_spaces=True))
    outputs = model.generate(inputs, max_length=150, do_sample=True, top_p=0.95, top_k=60, pad_token_id=tokenizer.eos_token_id)

    generated = tokenizer.decode(outputs[0])[prompt_length:]
    return generated

if __name__ == "__main__":
    prompt = "Who is Leonardo Da Vinci?"
    print(answer(prompt))