from gensim.models import word2vec


def most_similar(load_model_path, positive=None, negative=None):
    model = word2vec.Word2Vec.load(load_model_path)

    results = []
    if positive and negative:
        if positive in model.wv and negative in model.wv:
            results = model.wv.most_similar(
                positive=[positive],
                negative=[negative]
            )
    elif positive:
        if positive in model.wv:
            results = model.wv.most_similar(
                positive=[positive]
            )
    return results


if __name__ == "__main__":
    inputs = list(input().rstrip().split(' '))
    save_model_path = 'save.model'

    positive = inputs[0] if len(inputs) >= 1 else None
    negative = inputs[1] if len(inputs) >= 2 else None

    results = most_similar(save_model_path, positive, negative)
    print('results', results)
