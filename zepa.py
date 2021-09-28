# def solution(x):
#     stop_num = 0
#     new_num = 2
#     while new_num != 1:
#             if x % 2 == 0:
#                 new_num = x / 2
#                 stop_num = stop_num + 1
#                 x = new_num
#             else:
#                 new_num = 3 * x + 1
#                 stop_num = stop_num + 1
#                 x = new_num
#
#     return stop_num
# step=solution(10)
#
# print(step)
#
#
#
# def GetSteps(num):
#     stoping_time = 0
#     new_num = 0
#
#     while new_num != 1:
#         if num % 2 == 0:
#             new_num = num / 2
#             stoping_time = stoping_time + 1
#             x = new_num
#
#         else:
#             new_num = 3 * num + 1
#             stoping_time = stoping_time + 1
#             x = new_num
#     return stoping_time
# total_step = GetSteps(10)
# print(total_step)
#

n = 6
for i in range(n):
    for j in range(n):
        if i == 0 or j == (n-1) or i == j:
            print("*", end = "")
        else:
            print(end = " ")
    print()