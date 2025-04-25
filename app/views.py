from django.shortcuts import render
from .add_data import ImportToModel

def update_schedule(request):
    i = ImportToModel()
    import asyncio
    asyncio.run(i.import_data_async())