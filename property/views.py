from django.shortcuts import render, redirect
from .forms import PropertyForm
from .models import Property
import pickle
import django_tables2 as tables
from .table import Mytable
# Create your views here.
def add_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        if form.is_valid():
            data = list(form.cleaned_data.values())
            f_status = data.pop(-2)
            if f_status == 'furnished':
                data.extend([1,0,0])
            elif f_status == 'unfurnished':
                data.extend([0,1,0])
            else:
                data.extend([0,0,1])
            regressor = pickle.load(open("random_forest.pkl",'rb'))
            result = regressor.predict([data[:-1]])
            form.cleaned_data['predictedprice'] = result[0]
            form.save()
            result = "Predict House Price :"+f"\u20B9{int(result[0])}"
            form = PropertyForm()
            return render(request, 'add_property.html', {'form': form,"result2":result})
    else:
        form = PropertyForm()
        return render(request, 'add_property.html', {'form': form})
def property_list(request):
    properties = Property.objects.all().order_by('-predictedprice')
    table = Mytable(properties)
    return render(request, 'property_list.html', {'table': table})