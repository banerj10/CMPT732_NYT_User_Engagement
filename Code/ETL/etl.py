from pyspark.sql import SparkSession
from pyspark import SparkConf
import os
from pyspark.sql import SparkSession, Row, functions, types
from pyspark.sql.types import IntegerType
from pyspark.sql.functions import count,split

access_id = "AKIA33ABH36IQH55OI4E"
access_key = "bsRrVlTlJAT37os5PSjUmOj/VSgqntypNVCR8Uoa"

conf = SparkConf()
conf.set('spark.jars.packages', 'org.apache.hadoop:hadoop-aws:3.2.0')
conf.set('spark.hadoop.fs.s3a.access.key',access_id)
conf.set('spark.hadoop.fs.s3a.secret.key', access_key)

spark = SparkSession.builder.config(conf=conf)\
      .appName("DataKnyts-ETL")\
      .getOrCreate()

articles = spark.read.json('s3a://dataknyts-nyt-dump/articles/')
#articles.printSchema()

comments = spark.read.json("s3a://dataknyts-nyt-dump/comments/")
#comments.printSchema()

from pyspark.sql.functions import udf
import random
import pandas as pd

# ETL for article data - get relevant fields, concatenate author name
articles = articles.select(
            articles['news_desk'], articles['section_name'], 
            articles['type_of_material'], articles['abstract'], 
            articles['word_count'], articles['pub_date'], 
            articles['web_url'], articles['uri'], 
            articles['headline.main'].alias('headline'),
            articles['keywords.value'].getItem(0).alias('keyword'),
            articles['byline.person.firstname'].getItem(0).alias('fname'),
            articles['byline.person.lastname'].getItem(0).alias('lname'),
            articles['totalCommentsFound'].alias('total_comments'),
            articles['totalEditorsSelectionFound'].alias('total_editor_selects'),
            articles['totalRecommendationsFound'].alias('total_recommendations'),
            articles['totalReplyCommentsFound'].alias('total_replies')            
)

articles = articles \
    .withColumn('author', 
        functions.concat(articles['fname'], 
                         functions.lit(' '), 
                         articles['lname'])) \
    .drop(articles['fname']) \
    .drop(articles['lname'])


# feature addition for articles from existing article fields
articles = articles \
        .withColumn('len_abstract', 
            functions.size(functions.split(articles['abstract'], ' '))) \
        .withColumn('len_headline', 
            functions.size(functions.split(articles['headline'], ' ')))

# ETL for comment data - convert date from epoch to datetime format
comments = comments \
    .withColumn('createDate', 
        functions.from_unixtime(comments['createDate'])) \
    .withColumn('updateDate', 
        functions.from_unixtime(comments['updateDate']))

#Blank to Null
from pyspark.sql.functions import col,when
articles=articles.select([when(col(c)=="",None).otherwise(col(c)).alias(c) for c in articles.columns])
#articles.show(3, vertical = True)

#Replace Null Values in Articles
articles = articles.na.fill({
        'author': 'Not Available', 
        'type_of_material': 'Interactive Feature'})

#Remove Missing Vallues
articles = articles.filter(articles['news_desk'].isNotNull())

#Replace News_Desk (Category) where Keyword is Null
articles = articles.withColumn("keyword", functions.coalesce(articles.keyword, articles.news_desk))

#Blank to Null
comments=comments.select([when(col(c)=="",None).otherwise(col(c)).alias(c) for c in comments.columns])

from pyspark.sql.functions import udf
import random
location_csv= spark.read.format('csv').option('header','true').load('s3a://dataknyts-nyt-dump/meta/location_csv.csv').toPandas()

def match_place(dump,list_df=location_csv):
      k=''
      for match,matcher in zip(list(list_df['city'].values),list(list_df['state_id'].values)):
            if (dump is not None):
                  if len(match) <= len(dump):
                        if match.lower() in dump.lower():
                              k = matcher
                              return k
      if len(k)==0:
            state_list = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI']

            k = random.choice(state_list)

      return k
               
def writer(df,path,mode="overwrite",format="csv",coalesce=True):
    if coalesce:
        df.coalesce(1).write.mode(mode).format(format).save(path,header="true")
    else:
        df.write.mode(mode).format(format).save(path,header="true")

udfcate = udf(match_place, types.StringType())
comments = comments.withColumn('correct_userlocation',udfcate(functions.col('userLocation')))
#comments = comments.limit(1000)

#Visualisation ETL

## section_name count
keyword_overall = articles.groupBy('section_name').count()
df_keyword_overall = keyword_overall.sort(col("count").desc()).limit(10)
writer(df_keyword_overall,"s3a://dataknyts-nyt-dump/graph/section_name_count/0/")

keyword_count_2021 = articles.filter(articles['pub_date'][0:4]=='2021')
keyword_count_2021 = keyword_count_2021.groupBy('section_name').count()
df_keyword_count_2021 = keyword_count_2021.sort(col("count").desc()).limit(10)
writer(df_keyword_count_2021,"s3a://dataknyts-nyt-dump/graph/section_name_count/1/")

keyword_count_2020 = articles.filter(articles['pub_date'][0:4]=='2020')
keyword_count_2020 = keyword_count_2020.groupBy('section_name').count()
df_keyword_count_2020 = keyword_count_2020.sort(col("count").desc()).limit(10)
writer(df_keyword_count_2020,"s3a://dataknyts-nyt-dump/graph/section_name_count/2/")

keyword_count_2019 = articles.filter(articles['pub_date'][0:4]=='2019')
keyword_count_2019 = keyword_count_2019.groupBy('section_name').count()
df_keyword_count_2019 = keyword_count_2019.sort(col("count").desc()).limit(10)
writer(df_keyword_count_2019,"s3a://dataknyts-nyt-dump/graph/section_name_count/3/")

keyword_count_2018 = articles.filter(articles['pub_date'][0:4]=='2018')
keyword_count_2018 = keyword_count_2018.groupBy('section_name').count()
df_keyword_count_2018 = keyword_count_2018.sort(col("count").desc()).limit(10)
writer(df_keyword_count_2018,"s3a://dataknyts-nyt-dump/graph/section_name_count/4/")

keyword_count_2017 = articles.filter(articles['pub_date'][0:4]=='2017')
keyword_count_2017 = keyword_count_2017.groupBy('section_name').count()
df_keyword_count_2017 = keyword_count_2017.sort(col("count").desc()).limit(10)
writer(df_keyword_count_2017,"s3a://dataknyts-nyt-dump/graph/section_name_count/5/")

## author count
author = articles.filter(articles['author']!='Not Available').cache()

author_count_overall = author.groupBy('author').count()
df_author_count_overall = author_count_overall.sort(col("count").desc()).limit(10)
writer(df_author_count_overall,"s3a://dataknyts-nyt-dump/graph/author_count/0/")

author_count_2021 = author.filter(articles['pub_date'][0:4]=='2021')
author_count_2021 = author_count_2021.groupBy('author').count()
df_author_count_2021 = author_count_2021.sort(col("count").desc()).limit(10)
writer(df_author_count_2021,"s3a://dataknyts-nyt-dump/graph/author_count/1/")

author_count_2020 = author.filter(articles['pub_date'][0:4]=='2020')
author_count_2020 = author_count_2020.groupBy('author').count()
df_author_count_2020 = author_count_2020.sort(col("count").desc()).limit(10)
writer(df_author_count_2020,"s3a://dataknyts-nyt-dump/graph/author_count/2/")

author_count_2019 = author.filter(articles['pub_date'][0:4]=='2019')
author_count_2019 = author_count_2019.groupBy('author').count()
df_author_count_2019 = author_count_2019.sort(col("count").desc()).limit(10)
writer(df_author_count_2019,"s3a://dataknyts-nyt-dump/graph/author_count/3/")

author_count_2018 = author.filter(articles['pub_date'][0:4]=='2018')
author_count_2018 = author_count_2018.groupBy('author').count()
df_author_count_2018 = author_count_2018.sort(col("count").desc()).limit(10)
writer(df_author_count_2018,"s3a://dataknyts-nyt-dump/graph/author_count/4/")

author_count_2017 = author.filter(articles['pub_date'][0:4]=='2017')
author_count_2017 = author_count_2017.groupBy('author').count()
df_author_count_2017 = author_count_2017.sort(col("count").desc()).limit(10)
writer(df_author_count_2017,"s3a://dataknyts-nyt-dump/graph/author_count/5/")

#news_desk vs sum(recommendation)
news_desk_overall = articles.groupBy('news_desk').agg( {'total_recommendations':'sum'})
news_desk_overall = news_desk_overall.withColumnRenamed("news_desk", "Category").withColumnRenamed("sum(total_recommendations)", "total_recommendations")
df_news_desk_count_overall = news_desk_overall.sort(col("sum(total_recommendations)").desc()).limit(8)
writer(df_news_desk_count_overall,"s3a://dataknyts-nyt-dump/graph/piechart_news_desk_sum/0/")

news_desk_2021 = articles.filter(articles['pub_date'][0:4]=='2021')
news_desk_2021 = news_desk_2021.groupBy('news_desk').agg( {'total_recommendations':'sum'})
news_desk_2021 = news_desk_2021.withColumnRenamed("news_desk", "Category").withColumnRenamed("sum(total_recommendations)", "total_recommendations")
df_news_desk_count_2021 = news_desk_2021.sort(col("sum(total_recommendations)").desc()).limit(8)
writer(df_news_desk_count_2021,"s3a://dataknyts-nyt-dump/graph/piechart_news_desk_sum/1/")

news_desk_2020 = articles.filter(articles['pub_date'][0:4]=='2020')
news_desk_2020 = news_desk_2020.groupBy('news_desk').agg( {'total_recommendations':'sum'})
news_desk_2020 = news_desk_2020.withColumnRenamed("news_desk", "Category").withColumnRenamed("sum(total_recommendations)", "total_recommendations")
df_news_desk_count_2020 = news_desk_2020.sort(col("sum(total_recommendations)").desc()).limit(8)
writer(df_news_desk_count_2020,"s3a://dataknyts-nyt-dump/graph/piechart_news_desk_sum/2/")

news_desk_2019 = articles.filter(articles['pub_date'][0:4]=='2019')
news_desk_2019 = news_desk_2019.groupBy('news_desk').agg( {'total_recommendations':'sum'})
news_desk_2019 = news_desk_2019.withColumnRenamed("news_desk", "Category").withColumnRenamed("sum(total_recommendations)", "total_recommendations")
df_news_desk_count_2019 = news_desk_2019.sort(col("sum(total_recommendations)").desc()).limit(8)
writer(df_news_desk_count_2019,"s3a://dataknyts-nyt-dump/graph/piechart_news_desk_sum/3/")

news_desk_2018 = articles.filter(articles['pub_date'][0:4]=='2018')
news_desk_2018 = news_desk_2018.groupBy('news_desk').agg( {'total_recommendations':'sum'})
news_desk_2018 = news_desk_2018.withColumnRenamed("news_desk", "Category").withColumnRenamed("sum(total_recommendations)", "total_recommendations")
df_news_desk_count_2018 = news_desk_2018.sort(col("sum(total_recommendations)").desc()).limit(8)
writer(df_news_desk_count_2018,"s3a://dataknyts-nyt-dump/graph/piechart_news_desk_sum/4/")

news_desk_2017 = articles.filter(articles['pub_date'][0:4]=='2017')
news_desk_2017 = news_desk_2017.groupBy('news_desk').agg( {'total_recommendations':'sum'})
news_desk_2017 = news_desk_2017.withColumnRenamed("news_desk", "Category").withColumnRenamed("sum(total_recommendations)", "total_recommendations")
df_news_desk_count_2017 = news_desk_2017.sort(col("sum(total_recommendations)").desc()).limit(8)
writer(df_news_desk_count_2017,"s3a://dataknyts-nyt-dump/graph/piechart_news_desk_sum/5/")


#### BUBBLE CHART COMMENTS

#OVERALL
df_bubble_comments = articles.groupby('author','section_name').avg('total_comments').filter(articles['section_name']!='Opinion')
df_bubble_comments = df_bubble_comments.withColumnRenamed('avg(total_comments)','avg_comments')
pd_df_bubble_comments = df_bubble_comments.sort(col('avg_comments').desc()).limit(50)
writer(pd_df_bubble_comments,"s3a://dataknyts-nyt-dump/graph/bubble_comments/0/")

# 2021
df_bubble_comments = articles.filter(articles['pub_date'][0:4]=='2021')
df_bubble_comments = df_bubble_comments.groupby('author','section_name').avg('total_comments').filter(articles['section_name']!='Opinion')
df_bubble_comments = df_bubble_comments.withColumnRenamed('avg(total_comments)','avg_comments')
pd_df_bubble_comments = df_bubble_comments.sort(col('avg_comments').desc()).limit(50)
writer(pd_df_bubble_comments,"s3a://dataknyts-nyt-dump/graph/bubble_comments/1/")

# 2020
df_bubble_comments = articles.filter(articles['pub_date'][0:4]=='2020')
df_bubble_comments = df_bubble_comments.groupby('author','section_name').avg('total_comments').filter(articles['section_name']!='Opinion')
df_bubble_comments = df_bubble_comments.withColumnRenamed('avg(total_comments)','avg_comments')
pd_df_bubble_comments = df_bubble_comments.sort(col('avg_comments').desc()).limit(50)
writer(pd_df_bubble_comments,"s3a://dataknyts-nyt-dump/graph/bubble_comments/2/")

# 2019
df_bubble_comments = articles.filter(articles['pub_date'][0:4]=='2019')
df_bubble_comments = df_bubble_comments.groupby('author','section_name').avg('total_comments').filter(articles['section_name']!='Opinion')
df_bubble_comments = df_bubble_comments.withColumnRenamed('avg(total_comments)','avg_comments')
pd_df_bubble_comments = df_bubble_comments.sort(col('avg_comments').desc()).limit(50)
writer(pd_df_bubble_comments,"s3a://dataknyts-nyt-dump/graph/bubble_comments/3/")

# 2018
df_bubble_comments = articles.filter(articles['pub_date'][0:4]=='2018')
df_bubble_comments = df_bubble_comments.groupby('author','section_name').avg('total_comments').filter(articles['section_name']!='Opinion')
df_bubble_comments = df_bubble_comments.withColumnRenamed('avg(total_comments)','avg_comments')
pd_df_bubble_comments = df_bubble_comments.sort(col('avg_comments').desc()).limit(50)
writer(pd_df_bubble_comments,"s3a://dataknyts-nyt-dump/graph/bubble_comments/4/")

# 2017
df_bubble_comments = articles.filter(articles['pub_date'][0:4]=='2017')
df_bubble_comments = df_bubble_comments.groupby('author','section_name').avg('total_comments').filter(articles['section_name']!='Opinion')
df_bubble_comments = df_bubble_comments.withColumnRenamed('avg(total_comments)','avg_comments')
pd_df_bubble_comments = df_bubble_comments.sort(col('avg_comments').desc()).limit(50)
writer(pd_df_bubble_comments,"s3a://dataknyts-nyt-dump/graph/bubble_comments/5/")


#### BUBBLE CHART RECOMMENDATIONS

#OVERALL
df_bubble_recommendations = articles.groupby('author','section_name').avg('total_recommendations').filter(articles['section_name']!='Opinion')
df_bubble_recommendations = df_bubble_recommendations.withColumnRenamed('avg(total_recommendations)','avg_recommendations')
pd_df_bubble_recommendations = df_bubble_recommendations.sort(col('avg_recommendations').desc()).limit(50)
writer(pd_df_bubble_recommendations,"s3a://dataknyts-nyt-dump/graph/bubble_recommendations/0/")

# 2021
df_bubble_recommendations = articles.filter(articles['pub_date'][0:4]=='2021')
df_bubble_recommendations = df_bubble_recommendations.groupby('author','section_name').avg('total_recommendations').filter(articles['section_name']!='Opinion')
df_bubble_recommendations = df_bubble_recommendations.withColumnRenamed('avg(total_recommendations)','avg_recommendations')
pd_df_bubble_recommendations = df_bubble_recommendations.sort(col('avg_recommendations').desc()).limit(50)
writer(pd_df_bubble_recommendations,"s3a://dataknyts-nyt-dump/graph/bubble_recommendations/1/")

# 2020
df_bubble_recommendations = articles.filter(articles['pub_date'][0:4]=='2020')
df_bubble_recommendations = df_bubble_recommendations.groupby('author','section_name').avg('total_recommendations').filter(articles['section_name']!='Opinion')
df_bubble_recommendations = df_bubble_recommendations.withColumnRenamed('avg(total_recommendations)','avg_recommendations')
pd_df_bubble_recommendations = df_bubble_recommendations.sort(col('avg_recommendations').desc()).limit(50)
writer(pd_df_bubble_recommendations,"s3a://dataknyts-nyt-dump/graph/bubble_recommendations/2/")

# 2019
df_bubble_recommendations = articles.filter(articles['pub_date'][0:4]=='2019')
df_bubble_recommendations = df_bubble_recommendations.groupby('author','section_name').avg('total_recommendations').filter(articles['section_name']!='Opinion')
df_bubble_recommendations = df_bubble_recommendations.withColumnRenamed('avg(total_recommendations)','avg_recommendations')
pd_df_bubble_recommendations = df_bubble_recommendations.sort(col('avg_recommendations').desc()).limit(50)
writer(pd_df_bubble_recommendations,"s3a://dataknyts-nyt-dump/graph/bubble_recommendations/3/")

# 2018
df_bubble_recommendations = articles.filter(articles['pub_date'][0:4]=='2018')
df_bubble_recommendations = df_bubble_recommendations.groupby('author','section_name').avg('total_recommendations').filter(articles['section_name']!='Opinion')
df_bubble_recommendations = df_bubble_recommendations.withColumnRenamed('avg(total_recommendations)','avg_recommendations')
pd_df_bubble_recommendations = df_bubble_recommendations.sort(col('avg_recommendations').desc()).limit(50)
writer(pd_df_bubble_recommendations,"s3a://dataknyts-nyt-dump/graph/bubble_recommendations/4/")

# 2017
df_bubble_recommendations = articles.filter(articles['pub_date'][0:4]=='2017')
df_bubble_recommendations = df_bubble_recommendations.groupby('author','section_name').avg('total_recommendations').filter(articles['section_name']!='Opinion')
df_bubble_recommendations = df_bubble_recommendations.withColumnRenamed('avg(total_recommendations)','avg_recommendations')
pd_df_bubble_recommendations = df_bubble_recommendations.sort(col('avg_recommendations').desc()).limit(50)
writer(pd_df_bubble_recommendations,"s3a://dataknyts-nyt-dump/graph/bubble_recommendations/5/")

@functions.udf(returnType=types.StringType())
def find_special_char(body_co):
   query =0 
   confusion =0
   emotion =0
   excitement =0
   if body_co is not None:
    length = len(body_co)
    for alpha in range(length-1):
        if body_co[alpha] == '?':
            query = 1
            if body_co[alpha+1] == '?':
                confusion = 1
        if body_co[alpha] == '!':
            emotions = 1
            if body_co[alpha+1] == '!':
                excitement = 1
    if body_co[length-1] == '?':
        query =1
    elif body_co[length-1] == '!':
        emotion =1
   return (str(query) +' '+ str(confusion) + ' '+ str(emotion) + ' '+ str(excitement) )

df_emotions =  comments.withColumn('emotions',find_special_char(col('commentBody')) )
df_emotions = df_emotions.withColumn('query', (split(col('emotions'), ' ').getItem(0)).cast('int')).withColumn('confusion', (split(col('emotions'), ' ').getItem(1)).cast('int')).withColumn('emotion', (split(col('emotions'), ' ').getItem(2)).cast('int')).withColumn('excitement', (split(col('emotions'), ' ').getItem(3)).cast('int'))
df_emotions = df_emotions.select('articleID','query','confusion','emotion','excitement')
temp_df = articles.select('uri', 'pub_date')
big_df_emotions = df_emotions.join(temp_df, df_emotions['articleID']==temp_df['uri'])
big_df_emotions = big_df_emotions.withColumn('year',big_df_emotions['pub_date'][0:4])
big_df_emotions = big_df_emotions.groupBy('year').agg({'query':'sum','confusion':'sum','emotion':'sum','excitement':'sum'})
writer(big_df_emotions,"s3a://dataknyts-nyt-dump/graph/emotions/")

'''
# COMMENTS VS LOCATIONS

year_wise = comments.select('correct_userlocation','createDate')

#2021
heatmap = year_wise.withColumn('year',year_wise['createDate'][0:4]).drop('createDate')
heatmap.createOrReplaceTempView("heatmap")
heatmap = spark.sql("SELECT correct_userlocation,COUNT(correct_userlocation) FROM heatmap where year='2021' Group By correct_userlocation")
writer(heatmap,"s3a://dataknyts-nyt-dump/graph/heatmap_usa/0/")

#2020
heatmap = year_wise.withColumn('year',year_wise['createDate'][0:4]).drop('createDate')
heatmap.createOrReplaceTempView("heatmap")
heatmap = spark.sql("SELECT correct_userlocation,COUNT(correct_userlocation) FROM heatmap where year='2020' Group By correct_userlocation")
writer(heatmap,"s3a://dataknyts-nyt-dump/graph/heatmap_usa/1/")

#2019
heatmap = year_wise.withColumn('year',year_wise['createDate'][0:4]).drop('createDate')
heatmap.createOrReplaceTempView("heatmap")
heatmap = spark.sql("SELECT correct_userlocation,COUNT(correct_userlocation) FROM heatmap where year='2019' Group By correct_userlocation")
writer(heatmap,"s3a://dataknyts-nyt-dump/graph/heatmap_usa/2/")

#2018
heatmap = year_wise.withColumn('year',year_wise['createDate'][0:4]).drop('createDate')
heatmap.createOrReplaceTempView("heatmap")
heatmap = spark.sql("SELECT correct_userlocation,COUNT(correct_userlocation) FROM heatmap where year='2018' Group By correct_userlocation")
writer(heatmap,"s3a://dataknyts-nyt-dump/graph/heatmap_usa/3/")

#2017
heatmap = year_wise.withColumn('year',year_wise['createDate'][0:4]).drop('createDate')
heatmap.createOrReplaceTempView("heatmap")
heatmap = spark.sql("SELECT correct_userlocation,COUNT(correct_userlocation) FROM heatmap where year='2017' Group By correct_userlocation")
writer(heatmap,"s3a://dataknyts-nyt-dump/graph/heatmap_usa/4/")

'''

### Line Chart comparison of 2019, 2020, 2021 - which country was mentioned and how much in covid articles
### checking for headline and abstract data, which has better values

### Line Chart comparison of 2019, 2020, 2021 - which country was mentioned and how much in covid articles
### checking for headline and abstract data, which has better values
@functions.udf(returnType=types.StringType())
def country_cv(body):
    china = 0
    india = 0
    italy = 0
    uk = 0
    russia = 0
    france = 0
    canada = 0
    germany = 0
    japan = 0
    us = 0
    if body is not None:
        if 'china' in body.lower():
            china=1
        if 'india' in body.lower():
            india=1
        if 'italy' in body.lower():
            italy=1
        if 'uk' in body.lower() or 'united kingdom' in body.lower():
            uk=1
        if 'russia' in body.lower():
            russia=1
        if 'france' in body.lower():
            france=1
        if 'canada' in body.lower():
            canada=1
        if 'germany' in body.lower():
            germany=1
        if 'japan' in body.lower():
            japan=1
        if 'US' in body or 'usa' in body.lower() or 'united states' in body.lower():
            us=1
    return(str(china) + str(india) + str(italy) + str(uk) + str(russia) + str(france) + str(canada) + str(germany) + str(japan) + str(us))

covid_country = articles.select('keyword',col('pub_date').cast('string'),'abstract')
covid_country = covid_country.withColumn('year',covid_country['pub_date'][0:4])
covid_country = covid_country.withColumn('month',covid_country['pub_date'][5:6][0:3][2:3])
covid_country_2020 = covid_country.filter((covid_country['year']=='2020'))
covid_country_2021 = covid_country.filter((covid_country['year']=='2021'))

covid_country_2020 = covid_country_2020.filter(articles['keyword']=='Coronavirus (2019-nCoV)')
covid_country_2021 = covid_country_2021.filter(articles['keyword']=='Coronavirus (2019-nCoV)')

covid_country_2020 = covid_country_2020.withColumn('country', country_cv(col('abstract')))
covid_country_2021 = covid_country_2021.withColumn('country', country_cv(col('abstract')))

covid_country_2020 = covid_country_2020.withColumn('china', (split(col('country'), '').getItem(0)).cast('int')).withColumn('india', (split(col('country'), '').getItem(1)).cast('int')).withColumn('italy', (split(col('country'), '').getItem(2)).cast('int')).withColumn('uk', (split(col('country'), '').getItem(3)).cast('int')).withColumn('russia', (split(col('country'), '').getItem(4)).cast('int')).withColumn('france', (split(col('country'), '').getItem(5)).cast('int')).withColumn('canada', (split(col('country'), '').getItem(6)).cast('int')).withColumn('germany', (split(col('country'), '').getItem(7)).cast('int')).withColumn('japan', (split(col('country'), '').getItem(8)).cast('int')).withColumn('us', (split(col('country'), '').getItem(9)).cast('int'))
covid_country_2021 = covid_country_2021.withColumn('china', (split(col('country'), '').getItem(0)).cast('int')).withColumn('india', (split(col('country'), '').getItem(1)).cast('int')).withColumn('italy', (split(col('country'), '').getItem(2)).cast('int')).withColumn('uk', (split(col('country'), '').getItem(3)).cast('int')).withColumn('russia', (split(col('country'), '').getItem(4)).cast('int')).withColumn('france', (split(col('country'), '').getItem(5)).cast('int')).withColumn('canada', (split(col('country'), '').getItem(6)).cast('int')).withColumn('germany', (split(col('country'), '').getItem(7)).cast('int')).withColumn('japan', (split(col('country'), '').getItem(8)).cast('int')).withColumn('us', (split(col('country'), '').getItem(9)).cast('int'))

covid_country_2020 = covid_country_2020.groupBy('month').agg({'china':'sum','india':'sum','italy':'sum','uk':'sum', 'russia':'sum', 'france':'sum','canada':'sum','germany':'sum','japan':'sum', 'us':'sum'})
covid_country_2021 = covid_country_2021.groupBy('month').agg({'china':'sum','india':'sum','italy':'sum','uk':'sum', 'russia':'sum', 'france':'sum','canada':'sum','germany':'sum','japan':'sum', 'us':'sum'})

writer(covid_country_2020,"s3a://dataknyts-nyt-dump/graph/covid_country_line_chart/0/")
writer(covid_country_2021,"s3a://dataknyts-nyt-dump/graph/covid_country_line_chart/1/")