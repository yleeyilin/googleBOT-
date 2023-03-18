from transformers import pipeline, AutoTokenizer, AutoModelWithLMHead
import torch

# Load a pre-trained GPT model
model_name = "gpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelWithLMHead.from_pretrained(model_name)

# Fine-tune the model on your own dataset
train_data = ["Some example text 1", "Some example text 2", ...]
tokenizer.pad_token = tokenizer.eos_token
train_encodings = tokenizer(train_data, padding=True, truncation=True)
train_dataset = torch.utils.data.TensorDataset(torch.tensor(train_encodings["input_ids"]),
                                               torch.tensor(train_encodings["attention_mask"]))
model.train()
optim = torch.optim.AdamW(model.parameters(), lr=5e-5)
train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=8, shuffle=True)

for epoch in range(3):
    for batch in train_loader:
        optim.zero_grad()
        input_ids, attention_mask = tuple(t.to(torch.device) for t in batch)
        outputs = model(input_ids, attention_mask=attention_mask, labels=input_ids)
        loss = outputs.loss
        loss.backward()
        optim.step()

# Use the fine-tuned model to generate responses
generator = pipeline('text-generation', model=model, tokenizer=tokenizer)
response = generator("Some prompt text")
