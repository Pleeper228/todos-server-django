from .models import List_Task, List_Item
from django.http import Http404, JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.db.models import F
from .serializers import List_Task_Serializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime


# from django.template import loader

def asss(request):
    return render(request)

def index(request):
    latest_list_task_list = List_Task.objects.order_by('-pub_date')[:5]
    context = {'latest_list_task_list': latest_list_task_list}
    return render(request, 'todos/index.html', context)

def detail(request, list_task_id):
    list_task = get_object_or_404(List_Task, pk=list_task_id)
    return render(request, 'todos/detail.html', {
        'list_task': list_task,
        'incompleted_items': list_task.list_item_set.filter(completed = False),
    })

def detail_json(request, list_task_id):
    try:
        list_task = List_Task.objects.get(pk=list_task_id)
    except List_Task.DoesNotExist:
        raise Http404("Task does not exist")

    serializer = List_Task_Serializer(list_task, many = False)
    return JsonResponse(serializer.data, safe = False)

def list_json(request):
    list_tasks = List_Task.objects.all()
    serializer = List_Task_Serializer(list_tasks, many = True)
    return JsonResponse(serializer.data, safe = False)

@csrf_exempt
def create_item(request, list_task_id):
    data= JSONParser().parse(request)
    list_task = List_Task.objects.get(pk=list_task_id)
    new_item = List_Item.objects.create(list_task=list_task, list_item_text=data['list_item_text'])
    serializer = List_Task_Serializer(list_task, many=False)
    return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def create_task_json(request):
    if request.method != 'POST':
        return JsonResponse({"message":"You can only POST to this!"}, status=405)
    data = JSONParser().parse(request)
    if "list_task_text" not in data:
        return JsonResponse({"message":"You must enter a value for list_task_text"}, status=422)
    elif type(data['list_task_text']) is not str:
        return JsonResponse({"message":"list_task_text must be a string!"}, status=422)

    new_task = List_Task.objects.create(list_task_text=data['list_task_text'])

    serializer = List_Task_Serializer(new_task, many = False)
    return JsonResponse(serializer.data, safe = False)

def results(request, list_task_id):
    list_task = get_object_or_404(List_Task, pk=list_task_id)
    return render(request, 'todos/results.html', {'list_task': list_task})

def item_completed(request, list_task_id, list_item_id):
    list_task = get_object_or_404(List_Task, pk=list_task_id)
    try:
        selected_list_item = list_task.items.get(pk=list_item_id)
    except (KeyError, List_Item.DoesNotExist):
        raise Http404("Item does not exist!")

    selected_list_item.completed = True
    selected_list_item.save()
    serializer = List_Task_Serializer(list_task, many = False)
    return JsonResponse(serializer.data, safe = False)

def completing(request, list_task_id):
    message = None
    list_task = get_object_or_404(List_Task, pk=list_task_id)
    try:
        amount_of_incompleted_items = request.POST['incompleted_items_length']
        selected_list_item = None
        selected_list_item_id_set = []
        for item in range(1, (int(amount_of_incompleted_items)) + 1):
            try:
                selected_list_item = list_task.list_item_set.get(pk=request.POST['list_item-' + str(item)])
            except (KeyError):
                message = 'im gay'
            else:
                if selected_list_item:
                    selected_list_item_id_set.append(selected_list_item)

        # list_item_id = request.POST['list_item-1']
        # selected_list_item = list_task.list_item_set.get(pk=list_item_id)
    except (List_Item.DoesNotExist):
        message = "You didn't select an item."
    else:
        if len(selected_list_item_id_set) < 1:
            message = "No task selected."
        else:
            message = "Thanks for completing that task!"
        for item in selected_list_item_id_set:
            item.completed = True
            item.save()
    return render(request, 'todos/detail.html', {
        'incompleted_items': list_task.list_item_set.filter(completed = False),
        'list_task': list_task,
        'message': message,
        'asss': selected_list_item_id_set,
    })

class IndexView(generic.ListView):
    template_name = 'todos/index.html'
    context_object_name = 'latest_list_task_list'

    def get_queryset(self):
        """Return the last five published tasks."""
        return List_Task.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = List_Task
    template_name = 'todos/detail.html'


class ResultsView(generic.DetailView):
    model = List_Task
    template_name = 'todos/results.html'
