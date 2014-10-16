"""
Implentation of tomokiyo
"""
import nltk
import math
from nltk import FreqDist, ConditionalFreqDist, ConditionalProbDist, MLEProbDist


def pointwise_kl_divergence(word, p, q):
    prob_p = p(word)
    prob_q = q(word)
    return prob_p * math.log(prob_p/prob_q)


def build_language_models(corpus_words):
    unigram = FreqDist(corpus_words)
    unigram_prob = MLEProbDist(unigram)
    bigram = ConditionalFreqDist(nltk.bigrams(corpus_words))
    bigram_prob = ConditionalProbDist(bigram, MLEProbDist)

    def lm_1(words):
        p = 1.0
        for w in words:
            p = p * unigram_prob.prob(w)
        return p

    def lm_2(words):
        p = 1.0
        previous_word = None
        for w in words:
            if previous_word is None:
                p *= unigram_prob.prob(w)
            else:
                p *= bigram_prob[previous_word].prob(w)
            previous_word = w
        return p
    return lm_1, lm_2


def main():
    from nltk.corpus import brown
    words = [w.lower() for w in brown.words()]
    print 'building models ...'
    lm_1, lm_2 = build_language_models(words)
    print 'done'
    print pointwise_kl_divergence(['.', 'the'], lm_1, lm_2)


if __name__ == '__main__':
    main()
