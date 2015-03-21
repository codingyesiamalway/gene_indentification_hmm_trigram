__author__ = 'Yu Zhao'
import unicodedata
import codecs
from count_freqs import *



_RARE_ = '_RARE_'

def getTagCountTagWordCountDict(fileName):
    tagToCount = {}
    tagToWordToCount = {}
    f = codecs.open(fileName, encoding= 'utf-16')
    for line in f:
        line = unicodedata.normalize('NFKD', line).encode('ascii', 'ignore')
        toks = str(line).split()
        if 'WORDTAG' in toks:
            tag = toks[2]
            word = toks[3]
            count = int(toks[0])

            if tag not in tagToCount:
                tagToCount[tag] = int(count)
            else:
                tagToCount[tag] += int(count)

            if tag not in tagToWordToCount:
                tagToWordToCount[tag] = {word : count}
            elif word not in tagToWordToCount[tag]:
                tagToWordToCount[tag][word] = count
            else:
                tagToWordToCount[tag][word] += count
    f.close()
    return tagToCount, tagToWordToCount

def addRARE_to_TagToWordToCount(tagToWordToCount, minWordCount):
    res = {}
    for tag in tagToWordToCount:
        if tag not in res:
            res[tag] = {}
        for word in tagToWordToCount[tag]:
            count = tagToWordToCount[tag][word]
            if count < minWordCount:
                word = _RARE_
            if word not in res[tag]:
                res[tag][word] = count
            else:
                res[tag][word] += count
    return res

def tagToFile(inFile, outFile, tagToCount, tagToWordToCount):
    f = open(inFile)
    out_f = open(outFile, mode= 'w')
    for line in f:
        tok = str(line)
        greatesTag = ''
        greatestProb = 0
        for tag in tagToCount:
            tok = tok.strip("\t\n\r")
            real_tok = tok
            tok = tok
            if tok not in tagToWordToCount[tag]:
                tok = _RARE_
            p = float(tagToWordToCount[tag][tok]) / tagToCount[tag]
            if p > greatestProb:
                greatestProb = p
                greatesTag = tag
        out_f.write(real_tok + ' ' + greatesTag + '\n')

    f.close()
    out_f.close()

def main():
    tagToCount, tagToWordToCount = getTagCountTagWordCountDict('gene.counts')
    tagToWordToCount = addRARE_to_TagToWordToCount(tagToWordToCount, 5)
    # for i in tagToWordToCount:
    #     print i, tagToWordToCount[i]

    tagToFile('gene.dev', 'gene.dev.p1.out', tagToCount, tagToWordToCount)


def test():
    with codecs.open('gene.counts', encoding= 'utf-16') as f:
        hmm = Hmm(f)
        hmm.modifyRareWords(5)
    f = open('gene.dev')
    out_f = open('gene.dev.p1.out', mode= 'w' )
    hmm.tagFile(f, out_f)

    # print hmm.word_counts
    # print hmm.words
if __name__ == "__main__":
    test()