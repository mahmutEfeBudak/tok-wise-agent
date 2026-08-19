import json
import os
from train import merge, pre_tokenize


def load_merges(merges_path: str = "merges.json") -> dict[tuple[int, int], int]:
    if not os.path.exists(merges_path):
        raise FileNotFoundError(f"'{merges_path}' bulunamadı. Önce train.py dosyasını çalıştırın.")

    with open(merges_path, "r", encoding="utf-8") as f:
        raw_merges = json.load(f)

    return {
        tuple(map(int, pair.split(","))): token_id
        for pair, token_id in raw_merges.items()
    }


def build_vocab(merges: dict[tuple[int, int], int]) -> dict[int, bytes]:
    """Token ID'lerinden karşılık gelen bayt/metin parçalarını oluşturan kelime hazinesi."""
    vocab = {i: bytes([i]) for i in range(256)}
    
    # merges sözlüğünü new_id sırasına göre diz
    sorted_merges = sorted(merges.items(), key=lambda item: item[1])
    for (p1, p2), new_id in sorted_merges:
        if p1 in vocab and p2 in vocab:
            vocab[new_id] = vocab[p1] + vocab[p2]
            
    return vocab


def encode(text: str, merges: dict[tuple[int, int], int] = None) -> list[int]:
    if merges is None:
        merges = load_merges()

    chunks = pre_tokenize(text)
    all_tokens = []

    for chunk in chunks:
        tokens = list(chunk.encode("utf-8"))

        while len(tokens) >= 2:
            pairs = zip(tokens, tokens[1:])
            valid_pairs = {pair: merges[pair] for pair in pairs if pair in merges}

            if not valid_pairs:
                break

            best_pair = min(valid_pairs, key=valid_pairs.get)
            tokens = merge(tokens, best_pair, merges[best_pair])

        all_tokens.extend(tokens)

    return all_tokens


def analyze_tokens(text: str, merges_path: str = "merges.json") -> dict:
    merges = load_merges(merges_path)
    token_ids = encode(text, merges)
    vocab = build_vocab(merges)

    # Token ID'lerini metin parçalarına (String) dönüştürme
    tokens_detailed = []
    for tid in token_ids:
        raw_bytes = vocab.get(tid, b"")
        decoded_str = raw_bytes.decode("utf-8", errors="replace")
        tokens_detailed.append({
            "id": tid,
            "text": decoded_str
        })

    char_count = len(text)
    byte_size = len(text.encode("utf-8"))
    token_count = len(token_ids)

    compression_ratio = (1 - (token_count / byte_size)) * 100 if byte_size > 0 else 0
    estimated_cost = (token_count / 1000) * 0.0001

    return {
        "character_count": char_count,
        "byte_size": byte_size,
        "compressed_token_count": token_count,
        "compression_ratio": f"%{compression_ratio:.2f}",
        "token_ids": token_ids,
        "tokens_detailed": tokens_detailed,
        "estimated_cost_usd": f"${estimated_cost:.6f}",
    }