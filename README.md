# KB2E 调研报告

## 1. KB2E概述

KB2E项目[1]，由清华大学自然语言处理实验室发起，对2013年以来Learning Entity and Relation Embedding(之后简称 **LERE**)方法中效果最突出的以下4种方法进行的统一实现、评估：

* TransE[2]、

* TransH[3]

* TransR[4]

* CTransR[4]

完成了代码实现，并进行了结果评估。

**从测试结果看，非常明显，这几种方法效果很差，没法实用。**（和图像分类的ImageNet ilsvrc类似，Alexnet的top5 error达到）

报告的第2章，针对4种LERE方法的效果问题，进行原理探讨。

报告的第3章，针对第2章提出的问题，提出改进方法。

报告第4章将对第3章的假设，设计实验进行验证。

-----------
## 2. LERE存在问题的原因

项目提到的4种LERE方法，都是基于以下3个基础：

1. Entity可以用R^k空间的向量表示（Entity Embedding）

2. Relation可以用R^d空间一个或一组向量差来表示，该矢量为R^d空间上 head-tail（Relation Embedding）

3. 通过整体参数的mini-batch SGD优化，将Entity和Relation的Embedding一起得到

然而，基础2，存在的问题在于：

无论用单一、还是一组c个向量差的模型，LERE都**对于relation描述得过于简单**。

事实上的relation会复杂的多。举个用动词当relation例子，“reserve”作vt有预定、保护、提供等含义：

1. "she reserved ticket", "she reserved hotel"，若用一个向量描述"reserve"这个relation，则会让"ticket"，"hotel"的entity embedding尽量靠近；但是事实上在很多语境中，将"ticket"和"hotel"算成相似的word embedding，是很勉强的。正如她可以住在"hotel"中，但不能住在"ticket"中。

2. 另外如"government reserved Indians", "country reserved army"等，每个词的具体含义数量不一致，用CTransR[4]中描述的piecewise linear regression方法，将每个关系强制规定为c种子关系，这个模型也过与简单粗暴。

更何况WordNet（WN）词典储存的relation是词语之间上位词、下位词、词缀等描述；FreeBase（FB15K）知识图谱存储的relation是概念之间的抽象关系。这些都比上例动词relation的情况更加复杂。

因此，用上述4中LERE描述relation，**模型虽然在数学上清晰、漂亮，但赶不上实际问题的复杂度**。仅类似于R^d空间平均值的kNN(大体是这个意思)。

--------
## 3. 解决LERE问题的一个方向

简而言之，用更加有力的空间描述工具，将relation确认的问题变成分类问题。如CNN，随即森林，SVM。

1. Entity仍旧用R^k空间的向量表示（可以是TransR得到的entity embedding，也可以用Word2Vec等经典word Embedding）

2. 描述head--tail entity关系的时候，将其看作分类问题，而非用（一个或一组）向量差代表。

3. 用更有力的分类器处理此问题。
* 用SVM对head-tail的Entity
* 用CNN进行end-to-end的训练。（Convolution可看作对head、tail词概念的辨析、关联、理解等。）

因为这个方法输入是head、tail的各自Entity Embedding，之后通过CNN做relation预测，所以之后用**E4-CNN**来指代这个方法。用**E2-SVM**来代指SVM的相应方法。

-------
## 4. 实验设计

本章只对WN数据集做处理，且只做Hits@10(Raw)的实验。

### 4.1 TransR的E4-CNN

### 4.2 Word2Vec的E4-CNN

### 4.3 TransR的E2-SVM

### 4.4 Word2Vec的E2-SVM

----------
来源参考：

[1] [thunlp/KB2E项目主页](https://github.com/thunlp/KB2E)

[2] [TransE: "Translating embeddings for modeling multi-relational data." A Bordes, NIPS2013](https://www.utc.fr/~bordesan/dokuwiki/_media/en/transe_nips13.pdf)

[3] [TransH: "Knowledge Graph Embedding by Translating on Hyperplanes" Z Wang, AAAI2014](http://www.aaai.org/ocs/index.php/AAAI/AAAI14/paper/viewFile/8531/8546)

[4] [TransR: "Learning Entity and Relation Embeddings for Knowledge Graph Completion." Y Lin, AAAI 2015](http://www.aaai.org/ocs/index.php/AAAI/AAAI15/paper/viewFile/9571/9523)

[5] [WN15标准数据集](https://everest.hds.utc.fr/doku.php?id=en:transe)