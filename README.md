# Books2Movies

***More info*** in the <u>***[Team10_Poser.pdf](https://github.com/Yee172/Books2Movies/blob/master/Team10_Poster.pdf)***</u> and ***<u>[Team10_Presentation.pdf](https://github.com/Yee172/Books2Movies/blob/master/Team10_Presentation.pdf)*</u>**

***Our website:*** https://yee172.github.io/Books2Movies/

***Authors:***

***<u>Tian Fengrui,</u>*** 2017, Xi'an Jiaotong University

***<u>Peng Jiawei,</u>*** 2017, Zhejiang University

***<u>Ye Qihao,</u>*** 2016, Southern University of Science and Technology

***<u>Liu Yihong,</u>*** 2016, Sichuan University

## 项目描述

我们希望发现一种新的电影分类方式——***基于观众的喜好来分类***。我们选取[豆瓣](www.douban.com)的用户作为电影的观众，以阅读的书籍作为观众的偏好依据。我们将在以阅读书籍为参考的用户图上运行***社区发现算法***，从而将观众分类。然后对每一个社区的电影喜好进行整合，形成每个社区的偏好。最后用每个社区的偏好为依据构建电影图并进行新的社区发现，从而发现不同电影之间的隐藏联系。

## 预期结果

同类的电影应该会被同一类人所喜爱，因此，统一社区的人应该喜欢同一类型的电影。所以在电影社区中，大多数的电影应该属于同一类型。同时，由于一些电影是深受广大群众喜欢的，所以不同的社区的交集会形成一个中心区，代表最受欢迎的电影。

## 数据集

我们在***GitHub***上找到了一份关于**豆瓣电影评论**的数据集，同时，我们也通过网络数据爬虫获取了豆瓣书籍的***TOP250***榜单的评论及其用户。经过筛选，最终形成的数据集包含：用户的名称，用户在书籍***TOP250***榜单中评论的书籍，和用户在电影***TOP250***榜单上观看过的电影。

# Books2Movies    --*English Version*

## Project description

We hope to create a new method to classify movies, that is, ***according to the audience’s preferences***.  We decide to choose the users of [Douban](www.douban.com) as our sample of movie audience and select the books they read as the representation of audiences' preferences.  We will run ***Community Detection*** on the ***User Graph*** with the books as reference, so as to classify the audience.  By using this graph, we are able to integrate each community’s taste of movies.  Finally, we will build the Movie Graph based on the preferences of each community.  Then we can then run a new Community Detection on this graph, so as to discover the hidden relationship between different movies.

## Dataset & Subclasses

We found a data set on ***GitHub*** about ***Douban Movie Comments***. We also got the comments and users of the ***TOP250*** list of ***Douban Books*** through the ***web data crawler***. After screening, the final data set consists of the user's name, the book that the user reviews in the book ***TOP250*** list, and the movie that the user has watched on the movie ***TOP250*** list.

## Expected Analysis Results

Similar movies should be liked by the same kind of people, so people in the same community should like the same kind of movies. As a result, within the movie communities, most movies should belong to the same type. Meanwhile, because some movies are greatly loved by the masses, the gatherings of different communities will form a central area, representing the most popular movies.

# About Spider

*spider*目录下一共有四个文件夹，每一个文件夹爬取豆瓣中不同的信息。
程序需要`python3.6`的支持。

**在运行程序之前**，请先打开`cmd`输入以下命令：

`pip install requests`

`pip install beautifulsoup4`

`pip install selenium`

而在***Old_Spider***目录下的文件是在 ***Milestone 2*** 中爬取的数据，我们在 ***Milestone 3*** 中重新对书籍进行了分类并爬取了数据，这让我们的数据更加干净。

