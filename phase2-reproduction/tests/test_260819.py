import numpy as np

# 1. 4행 3열의 랜덤 값을 가진 배열 생성
array1 = np.random.rand(4, 3)
print("1번")
print(array1)


# 2. 0부터 24까지의 값으로 5×5 배열 생성
array2 = np.arange(25).reshape(5, 5)
print("\n2번")
print(array2)


# 3. 0~31까지의 값으로 2개의 4×4 배열 생성
array3 = np.arange(32).reshape(2, 4, 4)
print("\n3번")
print(array3)


# 4. 리스트를 배열로 변환
my_list = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
array4 = np.array(my_list)
print("\n4번")
print(array4)


# 5. 0의 값으로 3×5 배열 생성
array5 = np.zeros((3, 5))
print("\n5번")
print(array5)


# 6. 7의 값으로 7×7 배열 생성
array6 = np.full((7, 7), 7)
print("\n6번")
print(array6)


# 7. 3~45까지 15개의 값을 균등 간격으로 생성
array7 = np.linspace(3, 45, 15)
print("\n7번")
print(array7)


# 8. 3~45까지 간격을 3으로 배열 생성
array8 = np.arange(3, 46, 3)
print("\n8번")
print(array8)


# 9. eye() 함수를 사용하여 10×10 단위행렬 생성
array9 = np.eye(10)
print("\n9번")
print(array9)


# 10. 두 배열의 합을 add() 메소드를 활용하여 계산
a = np.array([
    [2, 4, 6, 8, 10],
    [12, 14, 16, 18, 20]
])

b = np.array([
    [30, 27, 24, 21, 18],
    [15, 12, 9, 6, 3]
])

result = np.add(a, b)

print("\n10번")
print(result)