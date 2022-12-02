from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import Upload_Form
from .models import upload_model
import pandas as pd
from django.core.paginator import Paginator
import math
import os
from random import randint

IMAGE_FILE_TYPES = ['csv']

def check_cache(request):
    if request.method == "GET":
        file = request.session.get('chart_upload_path')
        if(file != None):
            return get_table_data(request)
        return JsonResponse({"status": "error", "message": "no cache file exist"})
def clear_media():
    pass #method ot clear old data
def clear_chart(request):

    file_path = request.session.pop('chart_upload_path')
    remove_file = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + file_path
    print("removing {}".format(remove_file))
    try:
        os.remove(remove_file)
    except:
        print("Failed to remove setup for later")
    return JsonResponse({"table_content" : "", 'status': "sucess"})


def get_data_filters(request):
    file = request.session.get('chart_upload_path')[1:]
    df = pd.read_csv(file)
    filter_json = {}
    for key, val in df.dtypes.iteritems() :
        filter_json[key] = f"{val}"
    return JsonResponse({"filters" : filter_json})
    
def get_table_data(request):
    file = request.session.get('chart_upload_path')[1:]
    page_id = int(request.GET.get('page_id')) if request.GET.get('page_id') != None else 0
    step = int(request.GET.get('per_page')) if request.GET.get('per_page') != None else 10

    print("getting {} records for page for {}".format(step, page_id))
    df = pd.read_csv(file)
    table_content = df.loc[page_id*step:page_id*step+step].to_json(orient="split")
    return JsonResponse({"table_content" : table_content, "total_records":len(df.index), 'status': "sucess"})

def get_bar_chart(request):
    filter_list, group_filter, default_filters, filter_param, df =__parse_filters(request)
    print("Filter on: {} , group by: {}".format(filter_list, group_filter))
    rs = df.groupby(group_filter)[filter_list].agg("sum")
    categories = list(rs.index)
    values = rs.to_json(orient="values")
    return JsonResponse({"categories": categories, "values": values, "columns": filter_param, "default_filters": default_filters})

def upload(request):
    if request.method == "POST":
        form = Upload_Form(request.POST, request.FILES)
        if form.is_valid():
            file_form = form.save(commit=False)
            file_form.data_file = request.FILES['data_file']
            file_type = file_form.data_file.url.split('.')[-1]
            file_type = file_type.lower()
            print(file_type)
            if file_type not in IMAGE_FILE_TYPES:
                return JsonResponse({"status" : "failed"})
            request.session['chart_upload_path'] = file_form.data_file.url 
            file_form.save()
            return JsonResponse({"status" : "sucess"})
        else: print("Valid File Not Uploaded")
    return JsonResponse({"status" : "failed"})

def __parse_filters(request):
    file = request.session.get('chart_upload_path')[1:]
    df = pd.read_csv(file)
    filter_param = request.POST.get("filters")
    filter_list = []
    if(filter_param != None):
        filter_list = filter_param.split(",")
    group_filter = request.POST.get("group_by")

    header = list(df.columns)
    default_filters = {}
    
    if(group_filter == ""):
        group_filter = header[randint(0, len(header)-1)]
        default_filters["group_filter"] = group_filter

    if(filter_list == ['']):
        filter_list.pop()
        filter_list.append(header[randint(0, len(header)-1)])
        default_filters["filter_list"] = filter_list
    return filter_list, group_filter, default_filters, filter_param, df

def get_line_chart(request):
    if request.method == "POST":
        filter_list, group_filter, default_filters, filter_param, df =__parse_filters(request)
        JsonResponse({"status" : "success"})
    JsonResponse({"status" : "failed"})