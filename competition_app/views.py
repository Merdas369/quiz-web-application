from django.shortcuts import render




api = "https://opentdb.com/api.php?amount=5&category=9&type=multiple"
# Create your views here.


def main_page(req):
    return render(req, "competition_app/index.html")