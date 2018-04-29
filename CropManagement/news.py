import requests
import json


# for day in range(1,2):
#     news_data= requests.get("https://dev132-toi-times-of-india-v1.p.mashape.com/news?token=YUhSMGNEb3ZMM1JwYldWemIyWnBibVJwWVM1cGJtUnBZWFJwYldWekxtTnZiUzltWldWa2N5OXVaWGR6Wm1WbFpDOHRNakV5T0Rrek5qZ3pOUzVqYlhNL1ptVmxaSFI1Y0dVOWMycHpiMjQ9NTc1ZDZlMzE0MmViMA%3D%3D&page=" + str(day),
#       headers={
#         "X-Mashape-Key": "LHiNQrpnLDmshvCbHJYqZfi43l2ep1jr01OjsnMA1Jv5SemEcf",
#         "Accept": "application/json"
#       }
#     )
#     data = news_data.json()
#     with open('news.txt', 'a') as outp:
#         json.dump(data, outp)
# t c
# # with open('news.txt','r') as readfile:
# #     data =json.load(readfile)
# #     print(data['NewsItem']['Keywords'])
#
#
# import reportlab
#
# from reportlab.pdfgen import canvas
#
#
# p = canvas.Canvas(res)s