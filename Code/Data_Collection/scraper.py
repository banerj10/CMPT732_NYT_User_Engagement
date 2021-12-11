import requests
import sys
import json
import random
import uuid
from time import sleep

api_key_pointer = -1
SLEEP = 0.2
article_threshold = 5000
comments_threshold = 50
nyt_api_daily_limit = 4000
our_estimated_max_monthly_article_requests = 1
our_estimated_max_monthly_comment_requests = (article_threshold * 2) + 100

def read_api_key(number):
    lines = []
    with open('nyt-keys.txt') as f:
        lines = f.readlines()
    return lines[(number-1)].split('-')[3].strip()

def read_api_keys():
    keys = []
    keys_dict = {}
    global nyt_api_daily_limit
    with open('nyt-keys.txt') as f:
        lines = f.readlines()
        for line in lines:
            key = line.split("-")[3].strip()
            keys.append(key)
            keys_dict[key] = {}
            keys_dict[key]['articles'] = nyt_api_daily_limit 
            keys_dict[key]['comments'] = nyt_api_daily_limit 
    return (keys,keys_dict)

def update_api_key():
    global api_key_pointer
    api_key_pointer += 1
    api_key_pointer = api_key_pointer % len(api_keys)

def remove_keys_from_articles(articles):
    keys_articles = {'abstract', 'web_url', 'headline', 'keywords', 'pub_date', 'news_desk', 'section_name', 'byline', 'type_of_material', 'word_count', 'uri'}
    temp_key = list(articles.keys())
    for i in temp_key:
        if i not in keys_articles: 
            try:
                articles.pop(i)
            except:
                pass
    return articles

def remove_keys_from_comment(comment):
    keys_to_retain = {'commentID','userID','userLocation','commentBody','createDate','updateDate','recommendations','editorsSelection','replyCount'}
    keys = list(comment.keys())
    for key in keys:
        if key not in keys_to_retain:
            comment.pop(key)

def read_write_json_file(fname,option,to_dump = {}):
    if option == 'r':
        with open(fname,option) as f:
            data = json.load(f)
    elif option == 'w':
        with open(fname,option) as f:
            json.dump(to_dump, f)
            data = to_dump
    return data

def set_start_month_year(years,months,resume_from,month_year):
    for y in years:
        if(y <= resume_from['year']):
            for m in months:
                if(y == resume_from['year'] and m >= resume_from['month']):
                    month_year.append((m,y))
                elif(y != resume_from['year']):
                    month_year.append((m,y))

def are_keys_usable():
    global api_keys_dict 
    global our_estimated_max_monthly_requests
    l = len(api_keys_dict.keys())
    for key in api_keys_dict.keys():
       if(api_keys_dict[key]['comments'] < our_estimated_max_monthly_comment_requests/l and api_keys_dict[key]['articles'] < our_estimated_max_monthly_article_requests):
            return False
    return True

def get_hold_of_comments_for_article(web_url,article_comments,uri,article_ptr,year_month):
    totalCommentsFound = 0
    totalParentCommentsFound = 0
    totalReplyCommentsFound = 0
    totalEditorsSelectionFound = 0
    totalRecommendationsFound = 0
    global SLEEP
    global comments_threshold
    for offset in range(0,comments_threshold,25):
        update_api_key()
        api_keys_dict[api_keys[api_key_pointer]]['comments'] = api_keys_dict[api_keys[api_key_pointer]]['comments'] - 1
        print("key used : "+api_keys[api_key_pointer])
        comment_get_url = "https://api.nytimes.com/svc/community/v3/user-content/url.json?api-key="+api_keys[api_key_pointer]+"&url="+web_url+"&offset="+str(offset)
        comment_get_response = requests.get(comment_get_url)
        if(comment_get_response.status_code == 200):
            sleep(SLEEP)
            print("Comment data for article "+str(article_ptr)+","+str(year_month)+" fetched using API KEY "+str(api_key_pointer+1))
            comment_resp = comment_get_response.json()
            comments = comment_resp['results']['comments']
            totalCommentsFound = comment_resp['results']['totalCommentsFound']
            totalParentCommentsFound = comment_resp['results']['totalParentCommentsFound']
            totalReplyCommentsFound = comment_resp['results']['totalReplyCommentsFound']
            totalEditorsSelectionFound = comment_resp['results']['totalEditorsSelectionFound']
            totalRecommendationsFound = comment_resp['results']['totalRecommendationsFound']
            for comment in comments:
                remove_keys_from_comment(comment)
                comment['articleID'] = uri
                article_comments.append(comment)
            if len(comments) < 25:
                break
        else:
            print("Failed to fetch comments for article"+str(article_ptr)+","+str(year_month)+" status code "+str(comment_get_response.status_code))
    return(totalCommentsFound,totalParentCommentsFound,totalReplyCommentsFound,totalEditorsSelectionFound,totalRecommendationsFound)

api_keys,api_keys_dict = read_api_keys()
#why 2100? We will be fetching 1000 articles at the max for one month, which comes in one API call. After that, comments pertaining to
#a single article come in chunks of 25 through a single API call. We will be fetching at most 50 comments, thus 2 additional calls
#will follow. Thus 1 API call to fetch all articles of a month + 2*1000(because we will be fetching comments for at most 1000 articles) + 100(buffer)

if __name__ == "__main__" :
    year = 2019
    month = 1
    month_year = []
    months = [1,2,3,4,5,6,7,8,9,10,11,12]
    years = [2021,2020,2019]
    article_comments = []
    fname = 'resume_from.json' 
    resume_from = read_write_json_file(fname,'r')

    set_start_month_year(years,months,resume_from,month_year)

    for month_year_tuple in month_year:
        year_month = str(month_year_tuple[1]) + "/" + str(month_year_tuple[0])
        update_api_key()
        if are_keys_usable():
            api_keys_dict[api_keys[api_key_pointer]]['articles'] = api_keys_dict[api_keys[api_key_pointer]]['articles'] - 1
            print("key being used to fetch articles for "+str(year_month)+" : "+str(api_keys[api_key_pointer]))
            article_get_url = "https://api.nytimes.com/svc/archive/v1/"+year_month+".json?api-key="+api_keys[api_key_pointer]
            article_get_response = requests.get(article_get_url)
            sleep(SLEEP)
            if article_get_response.status_code == 200:
                article_resp = article_get_response.json()
                articles = article_resp['response']['docs']
                article_comments=[]
                #write code to randomly extract at most 1000 articles
                if(len(articles) >= article_threshold):
                    articles = random.sample(articles,article_threshold)
                print("Article data "+str(year_month)+" fetched using API KEY "+str(api_key_pointer+1))
                extra_pop_items = []
                for articles_dict in range(0,len(articles)):
                    needed_articles = remove_keys_from_articles(articles[articles_dict])
                    articles[articles_dict] = needed_articles
                    comment_data = ()
                    if ('web_url' in articles[articles_dict].keys()) and ('uri' in articles[articles_dict].keys()):
                        web_url = articles[articles_dict]['web_url']
                        uri = articles[articles_dict]['uri']
                        print()
                        #fetch at most 50 comments for article
                        comment_data = get_hold_of_comments_for_article(web_url,article_comments,uri,articles_dict,year_month)
                        articles[articles_dict]['totalCommentsFound'] = comment_data[0]
                        articles[articles_dict]['totalParentCommentsFound'] = comment_data[1]
                        articles[articles_dict]['totalReplyCommentsFound'] = comment_data[2]
                        articles[articles_dict]['totalEditorsSelectionFound'] = comment_data[3]
                        articles[articles_dict]['totalRecommendationsFound'] = comment_data[4]
                    else:
                        extra_pop_items.append(articles_dict)
                for pop_it in extra_pop_items:
                    articles.pop(pop_it)
                #write data as json
                read_write_json_file('./articles/'+uuid.uuid4().hex[:6]+'_articles_'+str(month_year_tuple[1]) + '_' + str(month_year_tuple[0])+'.json','w',articles)
                read_write_json_file('./comments/'+uuid.uuid4().hex[:6]+'_comments_'+str(month_year_tuple[1]) + '_' + str(month_year_tuple[0])+'.json','w',article_comments)
            else:
                print("Failed to fetch articles for "+str(year_month)+" with status code "+str(article_get_response.status_code))
        else:
            #save checkpoint
            print("Daily limit for a key has exceeded")
            resume_from['year'] = month_year_tuple[1]
            resume_from['month'] = month_year_tuple[0]
            read_write_json_file(fname,'w',resume_from)
            break