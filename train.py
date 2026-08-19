import json


def get_stats(tokens):
    counts = {}
    for pair in zip(tokens, tokens[1:]):
        counts[pair] = counts.get(pair, 0) + 1
    return counts


def merge(tokens, pair, idx):
    new_tokens = []
    i = 0
    while i < len(tokens):
        if i < len(tokens) - 1 and tokens[i] == pair[0] and tokens[i + 1] == pair[1]:
            new_tokens.append(idx)
            i += 2
        else:
            new_tokens.append(tokens[i])
            i += 1
    return new_tokens


def pre_tokenize(text):
    current_chunk = []
    chunks = []

    for char in text:
        if not current_chunk:
            current_chunk.append(char)
            continue
        prev_char = current_chunk[-1]

        same_type = (
            (prev_char.isalpha() and char.isalpha())
            or (prev_char.isdigit() and char.isdigit())
            or (prev_char.isspace() and char.isspace())
            or (prev_char == "'" and char.isalpha())
        )
        if same_type:
            current_chunk.append(char)
        else:
            chunks.append("".join(current_chunk))
            current_chunk = [char]

    if current_chunk:
        chunks.append("".join(current_chunk))

    return chunks


def train_bpe(
    corpus_path: str = "corpus.txt",
    num_merges: int = 20000,
    output_path: str = "merges.json",
):
    print("1/4. Metin dosyası (corpus.txt) okunuyor...")
    with open(corpus_path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    print("2/4. Pre-tokenization uygulanıyor...")
    chunks = pre_tokenize(raw_text)
    token_chunks = [list(chunk.encode("utf-8")) for chunk in chunks]

    merges = {}
    vocab_size = 256

    print(f"3/4. {num_merges} adet birleştirme kuralı eğitiliyor...")
    for i in range(num_merges):
        stats = {}
        for chunk in token_chunks:
            chunk_stats = get_stats(chunk)
            for pair, count in chunk_stats.items():
                stats[pair] = stats.get(pair, 0) + count

        if not stats:
            print("⚠️ Birleştirilecek ikili kalmadı, işlem erken sonlandırıldı.")
            break

        best_pair = max(stats, key=stats.get)
        new_token_id = vocab_size + i

        merges[best_pair] = new_token_id
        token_chunks = [merge(chunk, best_pair, new_token_id) for chunk in token_chunks]

        if (i + 1) % 1000 == 0 or (i + 1) == num_merges:
            print(
                f"   ➜ İlerleme: {i + 1}/{num_merges} kural hazır | Son Token ID: {new_token_id}"
            )

    serializable_merges = {f"{p[0]},{p[1]}": token_id for p, token_id in merges.items()}

    print("4/4. Sözlük merges.json dosyasına yazılıyor...")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(serializable_merges, f, indent=4, ensure_ascii=False)

    print(f"✅ Başarıyla tamamlandı! '{output_path}' dosyası hazır.")


if __name__ == "__main__":
    train_bpe("corpus.txt", num_merges=20000)
