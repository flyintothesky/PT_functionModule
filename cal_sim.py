import math
import jieba


class Likelihood:
    '''
              计算余弦相似度的类
     1、汇总所有出现过的词
     2、计算词频
     3、向量转化
     4、计算余弦相似度
    '''
    def word2vec(self, seg_list_1, seg_list_2):

        total_seg_list = list(set(seg_list_1 + seg_list_2))
        seg_vec_1 = []
        seg_vec_2 = []
        for word_tol in total_seg_list:
            freq = 0
            for word in seg_list_1:
                if word_tol == word:
                    freq += 1
            seg_vec_1.append(freq)
            freq = 0
            for word in seg_list_2:
                if word_tol == word:
                    freq += 1
            seg_vec_2.append(freq)
        self.seg_vec_1, self.seg_vec_2 = seg_vec_1, seg_vec_2

    def cos_dist(self):
        if len(self.seg_vec_1) != len(self.seg_vec_2):
            return None
        part_up = 0.0
        a_sq = 0.0
        b_sq = 0.0
        for a1, b1 in zip(self.seg_vec_1, self.seg_vec_2):
            part_up += a1 * b1
            a_sq += a1 ** 2
            b_sq += b1 ** 2
        part_down = math.sqrt(a_sq * b_sq)
        if part_down == 0.0:
            return None
        else:
            return part_up / part_down

    def likelihood(self, word1, word2, punctuation=False):
        self.word1 = word1
        self.word2 = word2
        self.punctuation = punctuation
        self.word2vec(self.word1, self.word2)
        like_per = self.cos_dist()
        return like_per


if __name__ == '__main__':
    '''
    test case
    '''
    likelihood = Likelihood()
    print(likelihood.likelihood('人力资源管理', '资源管理系统', punctuation=True))