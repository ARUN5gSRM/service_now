import os
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["HF_DATASETS_OFFLINE"] = "1"

from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    r"C:\Users\venka\PycharmProjects\mail\agent_mail_system\mailer\model",
    config_kwargs={"trust_remote_code": True},
    model_kwargs={"trust_remote_code": True},
    device="cpu"
)

text = "hello world"

embedding = model.encode(text, normalize_embeddings=True)

print(f'Text encoded: "{text}"')
print("Embedding dimension:", embedding.shape[0])
print("Embedding vector:")
print(embedding)
