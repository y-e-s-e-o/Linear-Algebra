import numpy as np
from fractions import Fraction

# input.txt를 읽고, 유효한 줄을 반환하는 함수 구현
def read_line(file):
    line = file.readline().strip()

    # 첫번째 줄이 end인 경우 바로 종료되는 경우
    if line == 'end':
        quit(0)

    else:
        # 빈 줄 건너뛰기
        if line == '':
            line = file.readline().strip()

        # 종료신호인 경우 프로그램 종료(줄을 건너뛴 다음이 종료신호인 경우 프로그램이 종료됨)
        if line == 'end':
            quit(0)
            
    return line


# cofactor expansiond으로 행렬식을 구하는 함수 (1행 전개로 구현)
def determinant_cofactor(matrix):

    # determinant값 저장을 위해 초기화
    det = 0

    # 2x2 행렬일 경우 determinant 계산
    if len(matrix) == 2:
        det = matrix[0][0]*matrix[1][1] - matrix[1][0]*matrix[0][1]

        # output.txt파일에 쓰기
        output_file = open("output.txt",'a')
        output_file.write("=> Minor Determinant = " + str(det) + "\n\n")
        output_file.close()

        return det
    
    # 3x3 이상의 행렬일 경우
    else : 
        for col in range(len(matrix)):
            # 원소 a 추출
            a = int(matrix[0][col])
 
            # minor
            minor = np.delete(matrix, 0, axis=0) #1행전개
            minor = np.delete(minor, col, axis=1)

            # output.txt파일에 쓰기
            output_file = open("output.txt",'a')
            output_file.write("element = " + str(a) + "\n")
            output_file.close()
            write_matrix_1(minor)

            #sign
            sign = (-1)**(col)

            # 2x2까지 진행했을 때 determinant 값이 얻어짐
            Det = determinant_cofactor(minor)

            # determinant
            det += a * sign * Det
 
    return det


# 가우스 소거법으로 행렬식을 구하는 함수
def determinant_gauss(matrix):
    for i in range(len(matrix)-1): # 대각 원소    
        for r in range(len(matrix)-i-1): # [0,'0']이면 행 4번 반복
            x = - matrix[i+1+r][i] / matrix[i][i]

            for c in range(len(matrix)-i): # ['0',0]이면 열 5번 반복
                matrix[i+1+r][i+c] += (matrix[i][i+c] * x) # 하나의 열 변환
            
            # output.txt파일에 쓰기
            output_file = open("output.txt",'a')
            write_matrix_2(matrix)

    # determinant값 저장을 위해 초기화
    det = 1 

    # output.txt파일에 쓰기
    output_file = open("output.txt",'a')
    output_file.write("det(A) = ")

    for j in range(len(matrix)):
        output_file.write(str(Fraction(matrix[j][j]).limit_denominator(100)) + ' x ')
        det *= matrix[j][j]

    output_file.write("= " + str(det) + "\n")
    output_file.close()


# output.txt파일 초기화 함수
def output_txt_reset():
    # output.txt파일 열기
    file = open('output.txt','w')

    # 기존에 적혀있던 내용을 초기화
    file.write('')

    # 파일 닫기
    file.close()


# matrix를 output.txt에 쓰는 함수1: cofactor expansion을 사용하는 경우
def write_matrix_1(matrix):
    output_file = open("output.txt",'a')

    for row in matrix:
        # 실수를 정수로 변환하고 5칸 폭으로 출력
        formatted_row = " ".join(f"{int(elem):2d}" for elem in row)
        output_file.write(formatted_row + "\n")

    output_file.write("\n")
    output_file.close()


# matrix를 output.txt에 쓰는 함수2: properties of the determinant를 사용하는 경우
def write_matrix_2(matrix):
    output_file = open("output.txt",'a')

    for row in matrix:
        # 각 원소를 분수로 변환 후, 고정된 너비로 정렬 (15칸)
        formatted_row = " ".join(f"{str(Fraction(num).limit_denominator(100)):>7}" for num in row)
        output_file.write(formatted_row + "\n")

    output_file.write("\n")
    output_file.close()


# input.txt 읽기
def read_file():    

    # 파일 열기
    file = open('input.txt', 'r')
    # 파일 읽기
    line = read_line(file)

    # 더이상 읽을 줄이 없을 때까지 반복
    while line:
        # matrix 정보 입력인 경우
        if line.startswith('Matrix 정보:'):
            line = read_line(file)

            rows = int(line.split(' ')[1])
            cols = int(line.split(' ')[2])

            # 행렬 초기화
            matrix = np.zeros((rows,cols))

            # 행렬 정보 저장
            for r in  range(rows):
                line = read_line(file)

                for c in range(cols):
                    matrix[r][c] = int(line.split(' ')[c])

        # 연산 방법 입력인 경우
        else:
            # 연산 방법 수 읽기
            n_operation = int(line.split(' ')[2])

            # 연산 방법 수 만큼 반복
            for i in range(n_operation):
                line = read_line(file)

                # cofactor expansion
                if line.startswith('cofactor expansion'):
                    # output.txt파일에 쓰기
                    output_file = open("output.txt",'a')
                    output_file.write("1. cofactor expansion \n\n")
                    output_file.close()
                    write_matrix_1(matrix)

                    # determinant 구하기
                    det = determinant_cofactor(matrix)

                    # output.txt파일에 쓰기
                    output_file = open("output.txt",'a')
                    output_file.write("det(A) = " + str(det) + "\n")
                    output_file.close()
        
                # properties of the determinant
                else:
                    # output.txt파일에 쓰기
                    output_file = open("output.txt",'a')
                    output_file.write("\n-------------------------------------\n\n")
                    output_file.write("2. properties of the determinant \n\n")
                    output_file.close()
                    write_matrix_2(matrix)

                    # determinant 구하기
                    determinant_gauss(matrix)

        line = read_line(file)


def main():
    # output.txt 초기화
    output_txt_reset()

    # input.txt 파일 읽고 연산
    read_file()

# 파일 실행 시 호출되는 부분
if __name__ == '__main__':
    # main 함수 호출
    main()
