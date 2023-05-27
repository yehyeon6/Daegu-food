from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import *
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import sqlite3
from django.core.paginator import Paginator



con = sqlite3.connect("db.sqlite3")
sejong = pd.read_sql("SELECT * FROM Sejong_A", con)

# 카테고리 코유
count_vect_category = TfidfVectorizer(min_df=0, ngram_range=(1,3))
place_category = count_vect_category.fit_transform(sejong['catemix'])
place_simi_cate = cosine_similarity(place_category, place_category)
# 리뷰 코유
count_vect_review = TfidfVectorizer(min_df=0.05, ngram_range=(1,3))
place_review = count_vect_review.fit_transform(sejong['review_okt']) 
place_simi_review = cosine_similarity(place_review, place_review)
# 타입 코유
count_vect_type = TfidfVectorizer(min_df=0, ngram_range=(1,3))
place_type = count_vect_type.fit_transform(sejong['store_type']) 
place_simi_type = cosine_similarity(place_type, place_type)

place_simi_co = (
                + place_simi_cate * 0.7 # 공식 1. 카테고리 유사도
                + place_simi_review * 0.3
                + place_simi_type * 0.7
                + np.repeat([sejong['positive'].values], len(sejong['positive']) , axis=0) * 0.02
                )


# 아래 place_simi_co_sorted_ind 는 그냥 바로 사용하면 됩니다.
place_simi_co_sorted_ind = place_simi_co.argsort()[:, ::-1] # ::-1 은 거꾸로 출력


# 최종 구현 함수
def find_simi_place(df, sorted_ind, place_name, top_n=5):

    compare = 0
    index = 0
    
    place_title = df[df['name'].str.contains(place_name)]
#     place_title = place_title.iloc[0:1]
    
    if place_title.empty:
        place_title = df[df['review_okt'].str.contains(place_name)]
        
        for i in range(len(place_title['review_okt'])): # 리뷰에서 키워드를 검색하여 가장 많이 출력되는 값 리턴
            if place_title['review_okt'].iloc[i].count(place_name) > compare:
                compare = place_title['review_okt'].iloc[i].count(place_name)
                index = i
        if index==0:
            return place_title
        place_title = place_title.iloc[index]
    
    place_index = place_title.id
    similar_indexes = sorted_ind[place_index, :(top_n)]
    similar_indexes = similar_indexes.reshape(-1)[:(top_n)]
    return df.iloc[similar_indexes]
    
def search(request):
    if request.method == 'GET':
        return render(request, 'main/main.html')
    search = request.POST.get('search_key')

    sejong_place = find_simi_place(sejong, place_simi_co_sorted_ind, search, 10)
    if sejong_place.empty:
        return HttpResponse("<script>alert('검색결과가 없습니다.다른 단어로 검색해주세요');location.href='../';</script>")
    else:
        sejong1 = sejong_place['id'].values
        sejong2 = sejong_place['name'].values
        sejong3 = sejong_place['store_type'].values
        sejong4 = sejong_place['address'].values
        sejong_zip = zip(sejong1, sejong2, sejong3, sejong4)
        return render(request, 'main/sejong.html', {'sejong_list':sejong_zip})

def find_simi_place_d(df, sorted_ind, place_name, top_n=5):

    place_title = df[df['name'].str.contains(place_name)]
    place_index = place_title.id
    similar_indexes = sorted_ind[place_index, :(top_n)]
    similar_indexes = similar_indexes.reshape(-1)[:(top_n)][1:]
    return df.iloc[similar_indexes]

def detail(request, pk):
    food = Sejong_A.objects.get(id=pk)
    if food.star == None:
        food.star = '없음'
    if food.menu_keyword != None:
        food.menu_keyword = food.menu_keyword.replace(',',' ')
    else:
        food.menu_keyword = '없음'

    sejong_place = find_simi_place_d(sejong, place_simi_co_sorted_ind, food.name, 6)
    sejong1 = sejong_place['id'].values
    sejong2 = sejong_place['name'].values
    sejong3 = sejong_place['store_type'].values
    sejong4 = sejong_place['address'].values
    sejong_zip = zip(sejong1, sejong2, sejong3, sejong4)

    return render(request, 'main/detail.html', {'food':food, 'sejong_list':sejong_zip})

def cate(request):
    cates = request.GET.get('cates')
    if cates=="ALL" or cates==None or cates == "모든식당":
        cate1 = Sejong_A.objects.all()
        cates = "모든식당"
    else:
        cate1 = Sejong_A.objects.filter(cate1=cates)
    
    page_info = {
        "startPage" : 1,
        "endPage" : 10,
        "underPageCount" : 10,
        "currentPage" : 1,
        "totalPage" : 0,
        "countPerPage" : 10,
    }

    page_info["currentPage"] = request.GET.get('page')

    if not page_info["currentPage"]:
        page_info["currentPage"] = 1
    else:
        page_info["currentPage"] = int(page_info["currentPage"])
        if page_info["currentPage"] <= 0:
            page_info["currentPage"] = 1

    page_info["totalPage"] = (cate1.count() // page_info["countPerPage"]) + 1
    if (cate1.count() % page_info["countPerPage"]) == 0:
        page_info["totalPage"] -= 1

    if (page_info["currentPage"] % page_info["underPageCount"]) == 0:
        page_info["startPage"] = ((page_info["currentPage"] // page_info["underPageCount"]) - 1) * page_info["underPageCount"] + 1
    else:
        page_info["startPage"] = (page_info["currentPage"] // page_info["underPageCount"]) * page_info["underPageCount"] + 1

    page_info["endPage"] = page_info["startPage"] + page_info["underPageCount"] - 1
    if page_info["currentPage"] >= page_info["totalPage"]:
        page_info["currentPage"] == page_info["totalPage"]
    if page_info["endPage"] > page_info["totalPage"]:
        page_info["endPage"] = page_info["totalPage"]

    pageRange = range(page_info["startPage"], page_info["endPage"] + 1)
    paginator = Paginator(cate1, page_info["countPerPage"]) 
    cate_list = paginator.get_page(page_info["currentPage"]) 


    return render(request, 'main/cate.html', {"cate_list":cate_list, "page_info":page_info, "pageRange":pageRange,"cate_title":cates})

def map(request, pk):
    food = Sejong_A.objects.get(id=pk)

    return render(request, 'main/map.html', {'food':food})

