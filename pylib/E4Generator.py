#

import os
import numpy
import codecs
import pickle
import sys


class E4Generator(object):

    def __init__(self, entity2id_path, relation2id_path, entity2vec_path):
        self.ent_id__ent_embedding_dict = {}
        self.rel_name__rel_id_dict = {}
        self.__loadEntEmbeddingDict(entity2id_path, entity2vec_path)
        self.__loadRelDict(relation2id_path)
        print 'E4Generator has been initialized successfully-'

    def __loadEntEmbeddingDict(self, entity2id_path, entity2vec_path):
        entity2id_file = codecs.open(entity2id_path, 'r')
        entity_ids = []
        for line in entity2id_file:
            items = line.strip().split()
            # print items
            entity_ids.append(int(items[0]))
        entity2id_file.close()

        entity2vec_file = codecs.open(entity2vec_path, 'r')
        entity_vecs = []
        for line in entity2vec_file:
            items = [float(a) for a in line.strip().split()]
            entity_vecs.append(items)
        entity2vec_file.close()

        if len(entity_ids)!=len(entity_vecs):
            raise IOError('%s & %s mismatches in count(lines)'&(entity2id_path, entity2vec_path), sys.exc_info()[2])
        self.ent_id__ent_embedding_dict = dict(zip(entity_ids, entity_vecs))
        # pickle.dump(self.ent_id__ent_embedding_dict, open('dict.pkl', 'w'))

    def __loadRelDict(self, relation2id_path):
        relation2id_file = codecs.open(relation2id_path, 'r')
        name_id_list = []
        for line in relation2id_file:
            items = line.strip().split()
            name_id_list.append([items[0], int(items[1])])
        relation2id_file.close()
        self.rel_name__rel_id_dict = dict(name_id_list)
        print self.rel_name__rel_id_dict

    def tripletFile2E4File(self, triplet_file_path, output_path):
        triplet_file_file = codecs.open(triplet_file_path, 'r')
        triplet_list = []
        for line in triplet_file_file:
            items = line.strip().split()
            triplet_list.append([int(items[0]), int(items[1]), items[2]])
        triplet_file_file.close()
        e4_list = []
        e2_dif_list = []
        id_list = []
        for triplet in triplet_list:
            e4_list.append(
                                self.ent_id__ent_embedding_dict[triplet[0]]
                                + self.ent_id__ent_embedding_dict[triplet[1]]
            )
            e2_dif_list.append( map(lambda x, y: x-y,
                                self.ent_id__ent_embedding_dict[triplet[0]],
                                self.ent_id__ent_embedding_dict[triplet[1]]) )
            id_list.append(self.rel_name__rel_id_dict[triplet[2]])
        pickle.dump([id_list, e4_list, e2_dif_list], open(output_path, 'w'))

if __name__=='__main__':
    gen = E4Generator('dependency/WN18/entity2id.txt',
                'dependency/WN18/relation2id.txt',
                'dependency/TransR/entity2vec.bern')

    gen.tripletFile2E4File('dependency/WN18/train.txt', 'temp/train.pkl')
    print '## training data has been generated'
    gen.tripletFile2E4File('dependency/WN18/test.txt', 'temp/test.pkl')
    print '## test data has been generated'
    gen.tripletFile2E4File('dependency/WN18/valid.txt', 'temp/val.pkl')
    print '## val data has been generated'
